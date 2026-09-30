"""The Step 3 label-hygiene reporter clause.

The list used to be typed into SKILL.md by hand and had rotted to 6 of 13
owners, so six weeks of bugs filed by the other seven were invisible to the
hygiene check while the query still looked like it passed. These tests pin the
clause to the roster file that Step 2 already maintains.
"""
import json

import pytest

import reporters


ROSTER = {
    "Daily Regression": {"A Daily Regression": "Astha Singh",
                         "B Daily Regression": "Allen Koickal"},
    "Smoke": {"C Smoke": "Yash Meshram",
              "D Smoke": "Astha Singh"},
}


def test_emails_covers_every_owner_in_the_roster():
    assert reporters.emails(ROSTER) == ["allen.koickal@zocdoc.com",
                                        "astha.singh@zocdoc.com",
                                        "yash.meshram@zocdoc.com"]


def test_emails_dedupes_an_owner_who_owns_several_suites():
    """Astha Singh owns two suites above and must appear once."""
    assert sum(1 for e in reporters.emails(ROSTER)
               if e == "astha.singh@zocdoc.com") == 1


@pytest.mark.parametrize("name,expected", [
    ("Astha Raghuwanshi", "astha.raghuwanshi@zocdoc.com"),
    ("Mervis Mascarenhas", "mervis.mascarenhas@zocdoc.com"),
    ("  Imroza   Ashrafi ", "imroza.ashrafi@zocdoc.com"),
])
def test_email_of_builds_the_zocdoc_address(name, expected):
    assert reporters.email_of(name) == expected


def test_email_of_refuses_a_mononym_rather_than_guessing():
    """A one-word owner cannot be turned into first.last, and inventing an
    address would put a silently-wrong name into the filter."""
    with pytest.raises(ValueError):
        reporters.email_of("Slackbot")


def test_shipped_roster_yields_all_thirteen_owners():
    with open(reporters.ROSTER, encoding="utf-8") as fh:
        got = reporters.emails(json.load(fh))
    assert len(got) == 13
    # The seven that the hand-maintained SKILL.md list had lost.
    for missed in ("anjana.somanath", "anushka.kumar", "astha.raghuwanshi",
                   "astha.singh", "imroza.ashrafi", "shriya.belsare",
                   "yash.meshram"):
        assert f"{missed}@zocdoc.com" in got


def test_clause_is_pasteable_jql():
    clause = reporters.clause(ROSTER)
    assert clause.startswith('reporter in (')
    assert clause.endswith(')')
    assert '"allen.koickal@zocdoc.com"' in clause


def test_clause_quotes_every_address():
    """An unquoted address makes Jira read the dot as a field path and 400."""
    for part in reporters.clause(ROSTER)[len("reporter in ("):-1].split(","):
        assert part.strip().startswith('"') and part.strip().endswith('"')
