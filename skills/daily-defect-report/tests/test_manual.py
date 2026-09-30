"""manual.py: the guards that decide whether a manual row can be trusted.

Every one of these exists because a wrong number shipped: the >100-run cap, an
unmapped Xray status, a TE from another day dragged in by the saved filter, and
the scope race that killed an unattended run on 2026-09-04.
"""
import pytest

import common
import manual


def te(key, statuses, created="2026-09-22T10:00:00.000+0530",
       assignee="Astha Singh", reporter="Akash Nair", total=None,
       summary="TE 2026Sep22 Homepage Smoke"):
    def user(n):
        return {"displayName": n} if n else None
    return {"jira": {"key": key, "summary": summary, "created": created,
                     "assignee": user(assignee), "reporter": user(reporter)},
            "testRuns": {"total": total if total is not None else len(statuses),
                         "results": [{"status": {"name": s}} for s in statuses]}}


@pytest.fixture
def fake_xray(monkeypatch):
    """Canned getTestExecutions payload, keyed by nothing -- each test supplies
    one response. Mocks the network boundary only."""
    box = {}

    def _gql(query, token, **kw):
        assert "getTestExecutions" in query
        return {"getTestExecutions": box["resp"]}

    monkeypatch.setattr(manual, "xray_graphql", _gql)
    return lambda resp: box.__setitem__("resp", resp)


class TestTally:
    def test_tally_counts_runs_raw_never_deduped(self, fake_xray):
        """The same case run on iOS and Android Smoke is platform coverage, not
        duplication, so runs are counted raw."""
        fake_xray({"total": 2,
                   "results": [te("ZPR-1", ["PASSED", "PASSED"]),
                               te("ZPR-2", ["PASSED", "FAILED"])]})
        row, n, counter, pending = manual.tally(["ZPR-1", "ZPR-2"], "t", "Smoke")
        assert n == 2
        assert counter["PASSED"] == 3 and counter["FAILED"] == 1
        assert row[-1] == 4 and sum(row[:-1]) == row[-1]
        assert pending == []

    def test_tally_row_matches_the_gadget_column_order(self, fake_xray):
        fake_xray({"total": 1, "results": [te("ZPR-1", ["PASSED", "PASSMINORBUG"])]})
        row, *_ = manual.tally(["ZPR-1"], "t", "Smoke")
        assert row[common.STATUSES.index("PASSED")] == 1
        assert row[common.STATUSES.index("PASSMINORBUG")] == 1

    def test_tally_refuses_an_unmapped_status(self, fake_xray):
        """An unknown status would vanish from the row while still inflating the
        total, so it is a hard stop rather than a silent drop."""
        fake_xray({"total": 1, "results": [te("ZPR-1", ["PASSED", "WONTFIX"])]})
        with pytest.raises(SystemExit, match="unmapped Xray status"):
            manual.tally(["ZPR-1"], "t", "Smoke")

    def test_tally_refuses_a_te_truncated_at_the_run_cap(self, fake_xray):
        """testRuns(limit:100) caps silently; past the cap the number is wrong."""
        fake_xray({"total": 1, "results": [te("ZPR-1", ["PASSED"] * 100, total=140)]})
        with pytest.raises(SystemExit, match=">100 runs"):
            manual.tally(["ZPR-1"], "t", "Smoke")

    def test_tally_refuses_a_te_from_another_day(self, fake_xray):
        """Catches the saved filter dragging in another day's runs."""
        fake_xray({"total": 1,
                   "results": [te("ZPR-1", ["PASSED"],
                                  created="2026-09-21T10:00:00.000+0530")]})
        with pytest.raises(SystemExit, match="not created on 2026-09-22"):
            manual.tally(["ZPR-1"], "t", "Smoke", date="2026-09-22")

    def test_tally_accepts_the_report_date(self, fake_xray):
        fake_xray({"total": 1, "results": [te("ZPR-1", ["PASSED"])]})
        row, *_ = manual.tally(["ZPR-1"], "t", "Smoke", date="2026-09-22")
        assert row[-1] == 1

    def test_tally_refuses_an_empty_filter(self, fake_xray):
        with pytest.raises(SystemExit, match="no Test Executions"):
            manual.tally([], "t", "Smoke")

    def test_tally_refuses_more_keys_than_one_page(self, fake_xray):
        with pytest.raises(SystemExit, match="exceeds the 100 page size"):
            manual.tally([f"ZPR-{i}" for i in range(101)], "t", "Smoke")

    def test_tally_raises_scope_race_only_for_a_count_mismatch(self, fake_xray):
        """A TE leaving scope between the two calls is a race, so it must be the
        narrow ScopeRace -- not SystemExit, which main() would not retry."""
        fake_xray({"total": 1, "results": [te("ZPR-1", ["PASSED"])]})
        with pytest.raises(manual.ScopeRace):
            manual.tally(["ZPR-1", "ZPR-2"], "t", "Smoke")

    def test_tally_reports_open_runs_with_an_owner(self, fake_xray):
        fake_xray({"total": 1, "results": [te("ZPR-1", ["PASSED", "TO DO",
                                                        "EXECUTING"])]})
        _, _, _, pending = manual.tally(["ZPR-1"], "t", "Smoke")
        assert len(pending) == 1
        assert pending[0]["todo"] == 1 and pending[0]["executing"] == 1
        assert pending[0]["owner"] == "Astha Singh"
        assert pending[0]["owner_source"] == "assignee"

    def test_tally_omits_a_closed_te_from_pending(self, fake_xray):
        """The control for the test above: a fully closed TE must not be nudged."""
        fake_xray({"total": 1, "results": [te("ZPR-1", ["PASSED", "FAILED"])]})
        _, _, _, pending = manual.tally(["ZPR-1"], "t", "Smoke")
        assert pending == []


class TestOwnerOf:
    def test_owner_prefers_assignee(self):
        assert manual.owner_of({"assignee": {"displayName": "A"},
                                "reporter": {"displayName": "B"}}) == ("A", "assignee")

    def test_owner_falls_back_to_reporter(self):
        assert manual.owner_of({"assignee": None,
                                "reporter": {"displayName": "B"}}) == ("B", "reporter")

    def test_owner_is_never_invented(self):
        """An unowned TE is reported as such so it can be asked about."""
        assert manual.owner_of({"assignee": None, "reporter": None}) == (None, None)


class TestFilters:
    def test_weekly_is_not_one_of_the_daily_filters(self):
        """first-check.sh passes --weekly to manual.py only; missing.py's roster
        was seeded from the two daily filters, so weekly suites there would read
        as roster rot and withhold the missing half."""
        assert manual.WEEKLY_LABEL not in manual.FILTERS
        assert set(manual.FILTERS) == {"Smoke", "Daily Regression"}
