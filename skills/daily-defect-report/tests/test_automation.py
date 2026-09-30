"""automation.py: the TeamCity reconciliation and its Xray cross-check.

TeamCity is the source; the guards here are what stop a wrong automation row.
Both warnings must actually fire -- a cross-check that cannot fail proves nothing.
"""
import json
import subprocess
import sys

import pytest

import automation

SCRIPT = automation.__file__


def build(number, passed, failed, muted, total, state="finished",
          finish="20260922T160000+0000"):
    return {"number": str(number), "state": state, "finishDate": finish,
            "testOccurrences": {"count": total, "passed": passed,
                                "failed": failed, "muted": muted, "ignored": 0}}


def run(builds, batches, date="2026-09-22", extra=()):
    """Drive main() with TeamCity and Xray both stubbed at the boundary."""
    stub = f"""
import json, sys
sys.path.insert(0, {str(automation.__file__.rsplit("/", 1)[0])!r})
import automation
automation.tc_api = lambda path: {{"build": {json.dumps(builds)}}}
automation.xray_batches = lambda a, b: {{k: __import__("collections").Counter(v)
                                        for k, v in {json.dumps(batches)}.items()}}
sys.argv = ["automation.py", "--date", {date!r}, "--json", *{list(extra)!r}]
automation.main()
"""
    return subprocess.run([sys.executable, "-c", stub],
                          capture_output=True, text=True)


class TestReconciliation:
    def test_gadget_passed_is_teamcity_passed_plus_muted(self):
        """Verified against the 2026-08-19 gadget: build #624 was 753 passed /
        20 failed / 1 muted / 774, and the gadget read 754 / 20 / 774."""
        p = run([build(624, passed=753, failed=20, muted=1, total=774)],
                {"15": {"PASSED": 754, "FAILED": 20}})
        assert p.returncode == 0, p.stderr
        out = json.loads(p.stdout)
        assert out["row"] == [754, 0, 0, 20, 0, 0, 0, 0, 774]
        assert out["warnings"] == []

    def test_build_that_does_not_reconcile_is_refused(self):
        p = run([build(1, passed=700, failed=20, muted=1, total=774)], {})
        assert p.returncode != 0
        assert "does not reconcile" in p.stderr

    def test_build_reporting_no_tests_is_refused(self):
        p = run([build(1, passed=0, failed=0, muted=0, total=0)], {})
        assert p.returncode != 0
        assert "no tests" in p.stderr

    def test_latest_finished_build_is_used_not_a_running_one(self):
        """The row is a snapshot of the latest FINISHED build; a running build is
        warned about but never counted."""
        p = run([build(9, 0, 0, 0, 0, state="running"),
                 build(8, passed=774, failed=0, muted=0, total=774)],
                {"15": {"PASSED": 774, "FAILED": 0}})
        out = json.loads(p.stdout)
        assert out["build"] == "8"
        assert any("still running" in w for w in out["warnings"])


class TestWarnings:
    def test_warns_when_the_latest_build_is_from_another_day(self):
        """Guards against reporting yesterday's automation row as today's."""
        p = run([build(1, passed=774, failed=0, muted=0, total=774,
                       finish="20260921T160000+0000")],
                {"15": {"PASSED": 774, "FAILED": 0}})
        out = json.loads(p.stdout)
        assert any("2026-09-21" in w and "not 2026-09-22" in w
                   for w in out["warnings"]), out["warnings"]

    def test_warns_when_no_xray_batch_reconciles(self):
        """The cross-check has to be able to fail, or it proves nothing."""
        p = run([build(1, passed=774, failed=0, muted=0, total=774)],
                {"15": {"PASSED": 700, "FAILED": 3}})
        out = json.loads(p.stdout)
        assert any("no Xray batch reconciles" in w for w in out["warnings"])

    def test_retry_inflated_batch_does_not_block_a_matching_one(self):
        """Retries inflate a batch above the suite size (2026-08-20: 782 raw vs
        774). The matching batch still has to be found."""
        p = run([build(1, passed=774, failed=0, muted=0, total=774)],
                {"09": {"PASSED": 780, "FAILED": 2}, "15": {"PASSED": 774,
                                                            "FAILED": 0}})
        out = json.loads(p.stdout)
        assert out["warnings"] == []

    def test_a_clean_day_emits_no_warnings(self):
        """The control: the warning list is not simply always populated."""
        p = run([build(1, passed=774, failed=0, muted=0, total=774)],
                {"15": {"PASSED": 774, "FAILED": 0}})
        assert json.loads(p.stdout)["warnings"] == []
