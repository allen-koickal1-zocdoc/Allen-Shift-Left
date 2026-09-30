"""nudge.py: the due-date gate, the follow-up split, and state handling.

These are the guards that stop the nudge pinging people about work that is not
due, or telling somebody they were "already asked" when they were not.
"""
import datetime
import json

import pytest
from conftest import IST

import nudge


def at(y, m, d, hh, mm):
    return datetime.datetime(y, m, d, hh, mm, tzinfo=IST)


# 2026-09-22 is a Monday, 2026-09-26 a Saturday, 2026-09-27 a Sunday.
class TestDayStatus:
    @pytest.mark.parametrize("hh,mm,expected", [
        (19, 29, "early"),   # one minute before the gate
        (19, 30, "due"),     # exactly on it
        (20, 0,  "due"),     # the second pass
        (4, 0,   "early"),   # a 4am scheduler misfire
    ])
    def test_day_status_boundary_on_the_report_day(self, hh, mm, expected):
        assert nudge.day_status("2026-09-22",
                                at(2026, 9, 22, hh, mm))[0] == expected

    @pytest.mark.parametrize("date,now", [
        ("2026-09-26", at(2026, 9, 26, 20, 0)),   # Saturday, on the day
        ("2026-09-27", at(2026, 9, 27, 20, 0)),   # Sunday, on the day
    ])
    def test_day_status_weekend_is_never_due(self, date, now):
        """No regression runs on a weekend, so every line the message would
        render is a false positive -- even at 20:00."""
        assert nudge.day_status(date, now)[0] == "weekend"

    def test_day_status_future_date_is_refused(self):
        assert nudge.day_status("2026-09-23", at(2026, 9, 22, 20, 0))[0] == "future"

    def test_day_status_past_weekday_is_due_at_any_hour(self):
        """A past weekday is due whatever the clock says -- the day is over."""
        assert nudge.day_status("2026-09-21", at(2026, 9, 22, 4, 0))[0] == "due"

    def test_day_status_past_weekend_stays_weekend(self):
        """Being in the past does not make a Saturday worth chasing."""
        assert nudge.day_status("2026-09-26", at(2026, 9, 28, 10, 0))[0] == "weekend"

    def test_day_status_rejects_malformed_date(self):
        with pytest.raises(SystemExit):
            nudge.day_status("22-09-2026", at(2026, 9, 22, 20, 0))


class TestRender:
    TES = [{"key": "ZPR-1", "summary": "Homepage Smoke", "label": "Smoke",
            "todo": 2, "executing": 0, "owner": "Astha Singh"},
           {"key": "ZPR-2", "summary": "ZVS Smoke", "label": "Smoke",
            "todo": 0, "executing": 1, "owner": "Akash Nair"}]
    MENTIONS = {"Astha Singh": "U1", "Akash Nair": "U2"}

    def test_render_first_pass_mentions_every_owner(self):
        out = nudge.render("2026-09-22", self.TES, [], self.MENTIONS)
        assert "<@U1>" in out and "<@U2>" in out
        assert "Already asked" not in out

    def test_render_followup_splits_asked_from_new(self):
        """A TE asked about before gets "already asked"; one that appeared since
        must not, or its owner is told about a reminder they never got."""
        out = nudge.render("2026-09-22", self.TES, [], self.MENTIONS,
                           prior={"ZPR-1"})
        assert "Already asked" in out
        asked, also = out.split("Also open")
        assert "ZPR-1" in asked and "ZPR-2" not in asked
        assert "ZPR-2" in also

    def test_render_followup_omits_closed_tes_entirely(self):
        """ZPR-2 closed in the gap: it is not in `tes` any more, so nobody is
        pinged twice for work they already finished."""
        out = nudge.render("2026-09-22", self.TES[:1], [], self.MENTIONS,
                           prior={"ZPR-1", "ZPR-2"})
        assert "ZPR-2" not in out

    def test_render_never_states_a_time_it_cannot_prove(self):
        """The state file records THAT a TE was asked about, not when. Claiming
        "asked at 19:30" would be unsupported from the third pass onward."""
        out = nudge.render("2026-09-22", self.TES, [], self.MENTIONS,
                           prior={"ZPR-1"})
        assert "19:30" not in out

    def test_render_leaves_an_unresolved_name_as_plain_text(self):
        """Never mention somebody else: a bare "Allen" matches three people."""
        out = nudge.render("2026-09-22", self.TES, [], {"Astha Singh": "U1"})
        assert "<@U1>" in out
        assert "*Akash Nair*" in out and "<@U2>" not in out

    def test_render_unowned_te_is_flagged_not_dropped(self):
        tes = [{"key": "ZPR-9", "summary": "Orphan", "label": "Smoke",
                "todo": 1, "executing": 0, "owner": None}]
        out = nudge.render("2026-09-22", tes, [], {})
        assert "ZPR-9" in out and "owner unknown" in out

    def test_render_missing_section_asks_rather_than_accuses(self):
        """A legitimate absence is indistinguishable from a miss, so the missing
        half must be phrased as a question."""
        missing = [{"suite": "ZVS Smoke", "label": "Smoke", "owner": "Astha Singh"}]
        out = nudge.render("2026-09-22", [], missing, self.MENTIONS)
        assert "On leave or not running today?" in out


class TestState:
    def test_load_prior_ignores_another_days_state(self, tmp_path):
        """A stale state file would mark all of today's TEs as already asked."""
        f = tmp_path / "s.json"
        f.write_text(json.dumps({"date": "2026-09-21", "tes": ["ZPR-1"]}))
        assert nudge.load_prior(str(f), "2026-09-22") is None

    def test_load_prior_missing_file_is_a_first_pass(self, tmp_path):
        assert nudge.load_prior(str(tmp_path / "nope.json"), "2026-09-22") is None

    def test_load_prior_unreadable_file_is_a_first_pass(self, tmp_path):
        f = tmp_path / "s.json"
        f.write_text("{not json")
        assert nudge.load_prior(str(f), "2026-09-22") is None

    def test_save_state_accumulates_across_passes(self, tmp_path):
        """Pass three must still know what pass one asked about."""
        f = str(tmp_path / "s.json")
        nudge.save_state(f, "2026-09-22", [{"key": "ZPR-1"}], [])
        nudge.save_state(f, "2026-09-22", [{"key": "ZPR-2"}], [])
        st = json.loads(open(f).read())
        assert st["tes"] == ["ZPR-1", "ZPR-2"]

    def test_save_state_keeps_tes_and_suites_separate(self, tmp_path):
        """Flattening the two buckets emptied `tes` and broke the next pass."""
        f = str(tmp_path / "s.json")
        nudge.save_state(f, "2026-09-22", [{"key": "ZPR-1"}],
                         [{"suite": "ZVS Smoke"}])
        nudge.save_state(f, "2026-09-22", [{"key": "ZPR-1"}],
                         [{"suite": "ZVS Smoke"}])
        st = json.loads(open(f).read())
        assert st["tes"] == ["ZPR-1"] and st["suites"] == ["ZVS Smoke"]

    def test_save_state_discards_another_days_record(self, tmp_path):
        f = str(tmp_path / "s.json")
        nudge.save_state(f, "2026-09-21", [{"key": "ZPR-OLD"}], [])
        nudge.save_state(f, "2026-09-22", [{"key": "ZPR-1"}], [])
        assert json.loads(open(f).read())["tes"] == ["ZPR-1"]
