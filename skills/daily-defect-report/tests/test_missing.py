"""missing.py: summary normalization and the roster diff.

The failure this guards is the 2026-09-04 one: six suites had merely been
RENAMED (the `Exploratory Testing` prefix churns in both directions) and the
diff reported them as missing, which would have pinged five people who had done
nothing wrong -- every day, unattended.
"""
import pytest

import missing


class TestNormalize:
    @pytest.mark.parametrize("summary", [
        "TE 2026Aug24 Homepage Smoke",
        "TE  2026Aug24  Homepage Smoke",
        "TE 2026-08-24 Homepage Smoke",
        "Homepage Smoke",
        "TE 2026Aug24 - Homepage Smoke",
    ])
    def test_normalize_strips_prefix_and_date_however_spaced(self, summary):
        assert missing.normalize(summary) == "Homepage Smoke"

    @pytest.mark.parametrize("summary,expected", [
        ("Exploratory Testing - Inbox Daily Regression", "Inbox Daily Regression"),
        ("Exploratory Testing Inbox Daily Regression", "Inbox Daily Regression"),
        ("Inbox Daily Regression", "Inbox Daily Regression"),
        ("Exploratory Testing Patient Intake Smoke", "Patient Intake Smoke"),
        ("Patient Intake Smoke", "Patient Intake Smoke"),
    ])
    def test_normalize_collapses_the_churning_mode_prefix(self, summary, expected):
        """Both spellings must land on one key, in both directions, or a rename
        reads as a missing suite."""
        assert missing.normalize(summary) == expected

    def test_normalize_keeps_a_suite_genuinely_named_daily_regression(self):
        """Only the dashed form is a mode marker. Stripping a bare leading
        "Daily Regression " would eat the start of a real suite name."""
        assert missing.normalize("Daily Regression Checks") == "Daily Regression Checks"
        assert missing.normalize("Daily Regression - ZVS") == "ZVS"

    def test_normalize_is_idempotent(self):
        """The roster is normalized on load and today's side on fetch; applying
        it twice must not keep eating words."""
        once = missing.normalize("TE 2026Aug24 Exploratory Testing Homepage Smoke")
        assert missing.normalize(once) == once == "Homepage Smoke"


class TestDiff:
    ROSTER = {"Smoke": {"Homepage Smoke": "Shriya Belsare",
                        "ZVS Smoke": "Mervis Mascarenhas"}}

    def test_diff_reports_a_genuinely_absent_suite(self):
        """The control for every "nothing missing" pass below: the same diff
        demonstrably flags an injected absence."""
        m, u = missing.diff(self.ROSTER, {"Smoke": {"Homepage Smoke": "x"}})
        assert [d["suite"] for d in m] == ["ZVS Smoke"]
        assert u == []

    def test_diff_is_clean_when_only_the_prefix_changed(self):
        """The 2026-09-04 false positive. Today's summary carries the mode
        prefix; normalized, it is the same suite, so nothing is missing."""
        today = {"Smoke": {missing.normalize("Exploratory Testing Homepage Smoke"): "x",
                           missing.normalize("ZVS Smoke"): "y"}}
        m, u = missing.diff(self.ROSTER, today)
        assert m == [] and u == []

    def test_diff_reports_an_unknown_suite_as_roster_rot(self):
        today = {"Smoke": {"Homepage Smoke": "x", "ZVS Smoke": "y",
                           "Brand New Smoke": "z"}}
        m, u = missing.diff(self.ROSTER, today)
        assert m == [] and [d["suite"] for d in u] == ["Brand New Smoke"]


class TestNormalizeRoster:
    def test_normalize_roster_makes_the_fix_retroactive(self):
        """The stored roster was seeded from raw summaries, so it holds the mode
        prefix on whatever suites carried it that day. Normalizing only today's
        side would leave those permanently unmatched."""
        roster = {"Smoke": {"Exploratory Testing Patient Intake Smoke": "Jyoti"}}
        norm, collisions = missing.normalize_roster(roster)
        assert norm == {"Smoke": {"Patient Intake Smoke": "Jyoti"}}
        assert collisions == []

    def test_normalize_roster_reports_a_duplicate_rather_than_hiding_it(self):
        """Two roster entries collapsing onto one key means one suite is
        invisible to the diff, so "nothing missing" would be unproven."""
        roster = {"Smoke": {"Patient Intake Smoke": "A",
                            "Exploratory Testing Patient Intake Smoke": "B"}}
        _, collisions = missing.normalize_roster(roster)
        assert len(collisions) == 1
        assert collisions[0]["suite"] == "Patient Intake Smoke"

    def test_shipped_roster_normalizes_without_collisions(self):
        """The real expected-tes.json must survive normalization cleanly, or the
        unattended path withholds the missing half every day."""
        import json
        with open(missing.ROSTER, encoding="utf-8") as fh:
            _, collisions = missing.normalize_roster(json.load(fh))
        assert collisions == [], collisions
