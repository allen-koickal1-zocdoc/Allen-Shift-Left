"""devices.py: day bucketing, thread resolution, and post classification.

The two things under test here are the two things that have actually shipped
wrong numbers: a post being attributed to the wrong day, and a post being
placed in the wrong Platform row.
"""
import datetime

import pytest
from conftest import ET, IST, msg, reminder, ts_at

import devices


# --------------------------------------------------------------------------
# Day bucketing. The report day is the TEAM's day (IST) -- these testers are
# India-based and the report tracks the day they worked. The bug this pins is
# that a naive fromtimestamp() resolves the day in whatever zone the laptop
# happens to be in, so the same history bucketed differently on a machine in
# ET than on one in IST.
# --------------------------------------------------------------------------
class TestDayBucketing:
    def test_collect_day_is_independent_of_machine_tz(self, fake_slack, monkeypatch):
        """Same history, same answer, whatever TZ the laptop is set to.

        Run under an explicit TZ env far from both ET and IST; a naive
        implementation shifts the boundary and drops the post.
        """
        want = datetime.date(2026, 9, 22)
        history = [reminder(ts_at(2026, 9, 22, 18, 30)),
                   msg("Windows Chrome 151", ts_at(2026, 9, 22, 20, 5))]
        fake_slack(history)

        results = {}
        for tz in ("Asia/Kolkata", "America/New_York", "UTC", "Pacific/Kiritimati"):
            monkeypatch.setenv("TZ", tz)
            datetime.datetime.now()          # force libc to pick the new zone up
            posts, _, _ = devices.collect(want)
            results[tz] = [(p[2]) for p in posts]

        assert all(v == results["Asia/Kolkata"] for v in results.values()), results
        assert results["Asia/Kolkata"] == [("Desktop Web", "Windows", "Chrome 151")]

    def test_collect_keeps_late_evening_ist_post(self, fake_slack):
        """A 23:30 IST post belongs to that IST day.

        Under the old naive bucketing on an ET-configured machine this landed on
        the previous day and vanished from the table.
        """
        want = datetime.date(2026, 9, 22)
        fake_slack([reminder(ts_at(2026, 9, 22, 18, 30)),
                    msg("Samsung S25 Ultra 3.252", ts_at(2026, 9, 22, 23, 30))])
        posts, _, _ = devices.collect(want)
        assert [p[2][0] for p in posts] == ["Android Mobile App"]

    def test_collect_excludes_next_ist_day_post(self, fake_slack):
        """00:30 IST the following day is NOT the report day. Proves the
        boundary rejects as well as accepts -- otherwise the test above would
        pass for a function that accepted everything."""
        want = datetime.date(2026, 9, 22)
        fake_slack([reminder(ts_at(2026, 9, 22, 18, 30)),
                    msg("Samsung S25 Ultra 3.252", ts_at(2026, 9, 23, 0, 30))])
        posts, _, _ = devices.collect(want)
        assert posts == []

    def test_regression_thread_resolves_in_team_tz(self, fake_slack, monkeypatch):
        """The nudge's parent thread must not move with the laptop's TZ.

        devices.regression_thread is the single resolver the nudge and the
        Platform table share, so a TZ-dependent answer here would silently
        point the two steps at different days.
        """
        want = datetime.date(2026, 9, 22)
        fake_slack([reminder(ts_at(2026, 9, 22, 18, 30))])
        seen = set()
        for tz in ("Asia/Kolkata", "America/New_York", "UTC"):
            monkeypatch.setenv("TZ", tz)
            datetime.datetime.now()
            ts, why = devices.regression_thread(want)
            assert ts, why
            seen.add(ts)
        assert len(seen) == 1, f"thread ts moved with TZ: {seen}"

    def test_post_in_yesterdays_thread_still_counted(self, fake_slack):
        """People answer whichever reminder is scrolled up. Only the post's own
        timestamp decides the day -- the Aug 20 Android post sat in the Aug 19
        thread and reading just that day's thread lost it."""
        want = datetime.date(2026, 9, 22)
        old = ts_at(2026, 9, 21, 18, 30)
        fake_slack(
            [reminder(old, replies=1), reminder(ts_at(2026, 9, 22, 18, 30))],
            replies={old: [msg("Samsung S25 Ultra 3.252",
                               ts_at(2026, 9, 22, 20, 10))]},
        )
        posts, _, (thread_ts, _) = devices.collect(want)
        assert [p[2][0] for p in posts] == ["Android Mobile App"]
        # and it is flagged as having come from another day's thread
        assert posts[0][3] == old != thread_ts
        assert posts[0][4] == "Samsung S25 Ultra 3.252"   # the matched line


# --------------------------------------------------------------------------
# Classification. A wrong row here is exactly the failure that shipped a bogus
# "Mobile Web / iPhone" row in the 2026-08-20 email.
# --------------------------------------------------------------------------
class TestClassify:
    @pytest.mark.parametrize("text,expected", [
        ("Windows Chrome 151",     ("Desktop Web", "Windows", "Chrome 151")),
        ("MacBook Safari 26.6",    ("Desktop Web", "MacBook", "Safari 26.6")),
        ("Android Chrome 151",     ("Mobile Web", "Android", "Chrome 151")),
        ("iPhone Safari 26.4",     ("Mobile Web", "iPhone", "Safari 26.4")),
    ])
    def test_classify_os_prefixed_browser_picks_row(self, text, expected):
        assert devices.classify(text) == expected

    @pytest.mark.parametrize("text", [
        "Samsung S25 Ultra Chrome 151",
        "Galaxy S24 Chrome 150",
        "Pixel 8 Chrome 151",
        "OnePlus 12 Chrome 151",
    ])
    def test_classify_device_model_plus_browser_is_mobile_web(self, text):
        """A named Android handset plus a browser is Mobile Web.

        The model names it by itself -- nobody runs Chrome on a Samsung
        desktop. Before the fix these fell through to ASK because OS_HINT only
        knew the bare word "android", so a real, unambiguous Mobile Web post
        blocked the table on a question that had already been answered.
        """
        row, dev, ver = devices.classify(text)
        assert row == "Mobile Web", (row, dev, ver)
        assert dev and dev != "Android", "the posted model should be kept verbatim"

    @pytest.mark.parametrize("text", ["Safari 26.4", "Chrome 151", "Firefox 153"])
    def test_classify_bare_browser_is_ambiguous_never_guessed(self, text):
        """A bare browser+version states no device. Guessing the row is what
        put a wrong Mobile Web row in a sent email, so it must surface as ASK."""
        row, dev, _ = devices.classify(text)
        assert row == devices.AMBIGUOUS
        assert dev is None

    @pytest.mark.parametrize("text,row", [
        ("iPhone 13 mini 4.231",   "iOS Mobile App"),
        ("iPad 4.231",             "iOS Mobile App"),
        ("Samsung S25 Ultra 3.252", "Android Mobile App"),
    ])
    def test_classify_model_plus_bare_version_is_app_row(self, text, row):
        assert devices.classify(text)[0] == row

    def test_classify_ignores_non_device_chatter(self):
        assert devices.classify("I'll be 15 minutes late to the standup") is None

    def test_slackbot_reminder_is_not_a_device_post(self, fake_slack):
        """The MOBILE WEB reminder carries :iphone:/:android: emoji and would
        otherwise classify as a device post."""
        want = datetime.date(2026, 9, 22)
        fake_slack([
            reminder(ts_at(2026, 9, 22, 18, 30)),
            reminder(ts_at(2026, 9, 22, 10, 0),
                     "Reminder: *<!here>* MOBILE WEB REGRESSION DAY :iphone: "
                     ":android: Chrome 151"),
        ])
        posts, mweb, _ = devices.collect(want)
        assert posts == []
        assert mweb is True


# --------------------------------------------------------------------------
# One message, several devices. Real posts do this: on 2026-09-16 a tester
# posted "Edge 152\nAndroid Chrome 149" as a single message and only one of the
# two was counted -- and the surviving one was mislabelled, because the bare
# "Edge 152" got paired with the "Android" from the *other* line and reported as
# Mobile Web. A swallowed line is a missing Platform row.
# --------------------------------------------------------------------------
class TestMultiDevicePosts:
    def test_collect_splits_a_multi_line_post(self, fake_slack):
        want = datetime.date(2026, 9, 22)
        fake_slack([reminder(ts_at(2026, 9, 22, 18, 30)),
                    msg("Windows Edge 152\nAndroid Chrome 149",
                        ts_at(2026, 9, 22, 19, 37))])
        posts, _, _ = devices.collect(want)
        assert [p[2] for p in posts] == [("Desktop Web", "Windows", "Edge 152"),
                                        ("Mobile Web", "Android", "Chrome 149")]

    def test_one_line_post_is_unaffected(self, fake_slack):
        """The split must not change the single-line case, which is the norm."""
        want = datetime.date(2026, 9, 22)
        fake_slack([reminder(ts_at(2026, 9, 22, 18, 30)),
                    msg("Samsung S25 Ultra 3.256", ts_at(2026, 9, 22, 19, 37))])
        posts, _, _ = devices.collect(want)
        assert [p[2][0] for p in posts] == ["Android Mobile App"]

    def test_bare_browser_line_does_not_borrow_another_lines_os(self, fake_slack):
        """The 2026-09-16 failure exactly: a bare "Edge 152" line next to an
        "Android Chrome 149" line must still be ASK, not Mobile Web. It has to
        be asked about, not inherit a device from a neighbouring line."""
        want = datetime.date(2026, 9, 22)
        fake_slack([reminder(ts_at(2026, 9, 22, 18, 30)),
                    msg("Edge 152\nAndroid Chrome 149",
                        ts_at(2026, 9, 22, 19, 37))])
        posts, _, _ = devices.collect(want)
        rows = [p[2] for p in posts]
        assert (devices.AMBIGUOUS, None, "Edge 152") in rows
        assert ("Mobile Web", "Android", "Chrome 149") in rows

    def test_narrative_line_beside_a_device_line_is_ignored(self, fake_slack):
        """Splitting must not turn prose into device rows."""
        want = datetime.date(2026, 9, 22)
        fake_slack([reminder(ts_at(2026, 9, 22, 18, 30)),
                    msg("Done with my modules\niPhone 13 mini 4.235",
                        ts_at(2026, 9, 22, 19, 37))])
        posts, _, _ = devices.collect(want)
        assert [p[2][0] for p in posts] == ["iOS Mobile App"]
