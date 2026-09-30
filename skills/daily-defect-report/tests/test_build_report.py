"""build_report.py: the subject line and the row arithmetic.

The builder is the last gate before an email leaves the machine, so a row that
does not add up must stop it rather than render.
"""
import json
import subprocess
import sys

import pytest

import build_report

SCRIPT = build_report.__file__


def run(data, tmp_path):
    """Invoke the builder as the skill does -- through the CLI."""
    d = tmp_path / "data.json"
    d.write_text(json.dumps(data))
    out = tmp_path / "r.html"
    p = subprocess.run([sys.executable, SCRIPT, "--data", str(d),
                        "--out", str(out)], capture_output=True, text=True)
    return p, (out.read_text() if out.exists() else "")


BASE = {
    "date": "2026-09-22",
    "defects": [],
    "automation_defects": [],
    "platforms": [["Desktop Web", "MacBook", "Chrome 151"]],
    "rows": {"Smoke": [68, 0, 0, 0, 0, 0, 1, 0, 69],
             "Daily Regression": [28, 0, 0, 0, 0, 0, 0, 0, 28]},
    "automation_row": [772, 0, 0, 2, 0, 0, 0, 0, 774],
}
DEFECT = {"key": "PS-1", "summary": "Thing broke", "reporter": "Harsh Khadde",
          "priority": "Minor"}


class TestSubject:
    def test_subject_is_pass_when_no_defects(self, tmp_path):
        """A clean day is PASS, not FAIL[0]."""
        p, _ = run(BASE, tmp_path)
        assert p.returncode == 0
        assert p.stdout.strip() == "PASS - Defect Report | Sep 22"

    def test_subject_counts_only_exploratory_defects(self, tmp_path):
        """n is the exploratory count; automation defects have their own
        section and must not inflate it."""
        data = dict(BASE, defects=[DEFECT, dict(DEFECT, key="PS-2")],
                    automation_defects=[dict(DEFECT, key="PS-3")])
        p, _ = run(data, tmp_path)
        assert p.stdout.strip() == "FAIL[2] - Defect Report | Sep 22"

    def test_subject_day_is_not_zero_padded(self, tmp_path):
        p, _ = run(dict(BASE, date="2026-09-07"), tmp_path)
        assert p.stdout.strip().endswith("| Sep 7")


class TestRowValidation:
    @pytest.mark.parametrize("row", [
        [68, 0, 0, 0, 0, 0, 1, 0, 70],      # does not sum
        [68, 0, 0, 0, 0, 0, 1, 69],         # too few cells
        [68, 0, 0, 0, 0, 0, 1, 0, 0, 69],   # too many cells
    ])
    def test_builder_refuses_a_row_that_does_not_reconcile(self, row, tmp_path):
        """A bad row must stop the email, not render a wrong table."""
        data = dict(BASE, rows=dict(BASE["rows"], Smoke=row))
        p, html = run(data, tmp_path)
        assert p.returncode != 0
        assert html == ""

    def test_builder_refuses_a_bad_automation_row(self, tmp_path):
        p, _ = run(dict(BASE, automation_row=[1, 0, 0, 0, 0, 0, 0, 0, 2]), tmp_path)
        assert p.returncode != 0


class TestHtml:
    def test_weekly_table_only_rendered_when_present(self, tmp_path):
        _, html = run(BASE, tmp_path)
        assert "Weekly Regression" not in html
        weekly = dict(BASE, rows=dict(BASE["rows"],
                                      Weekly=[10, 0, 0, 0, 0, 0, 0, 0, 10]))
        _, html = run(weekly, tmp_path)
        assert "Weekly Regression" in html

    def test_defect_summary_is_html_escaped(self, tmp_path):
        """Summaries are free text from Jira; an unescaped one would corrupt the
        email body."""
        data = dict(BASE, defects=[dict(DEFECT, summary='A <b>& "x"</b> break')])
        _, html = run(data, tmp_path)
        assert "&lt;b&gt;" in html and "<b>& \"x\"" not in html

    def test_only_posted_platform_rows_are_rendered(self, tmp_path):
        """The table is whatever the channel supported that day -- a row nobody
        posted must not appear."""
        _, html = run(BASE, tmp_path)
        assert "Desktop Web" in html
        for absent in ("Mobile Web", "iOS Mobile App", "Android Mobile App"):
            assert absent not in html

    def test_no_automation_defects_says_so_explicitly(self, tmp_path):
        _, html = run(BASE, tmp_path)
        assert "No new defects were detected by QA automation tests." in html
