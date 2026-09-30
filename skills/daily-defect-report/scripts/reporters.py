#!/usr/bin/env python3
"""The `reporter in (...)` clause for the Step 3 label-hygiene query.

Derived from expected-tes.json rather than typed into SKILL.md. The
hand-maintained copy had rotted to 6 of the 13 owners, so bugs filed by the
other seven never reached the hygiene check -- and because the query still
returned rows for the six it did list, nothing looked broken. Step 2 already
keeps the roster current (`missing.py --update-roster`), so deriving the clause
from it means the two cannot drift apart again.

    scripts/reporters.py            # the clause, ready to paste into the JQL
    scripts/reporters.py --list     # one address per line
"""
import json
import os
import sys

ROSTER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "expected-tes.json")


def email_of(name: str) -> str:
    """first.last@zocdoc.com for a roster display name.

    Verified against Jira for all 13 current owners: Jira rejects an unknown
    reporter outright, so the Step 3 query returning results is itself the
    check that every derived address resolves.
    """
    parts = name.split()
    if len(parts) < 2:
        raise ValueError(f"cannot derive an email from {name!r}: need first and "
                         f"last name. Add the address by hand if this is real.")
    return f"{parts[0].lower()}.{parts[-1].lower()}@zocdoc.com"


def emails(roster: dict) -> list[str]:
    """Every distinct owner in the roster, as a sorted address list."""
    return sorted({email_of(owner)
                   for suites in roster.values()
                   for owner in suites.values()})


def clause(roster: dict) -> str:
    """The JQL fragment. Addresses are quoted: unquoted, Jira reads the dot as
    a field path and 400s."""
    return "reporter in (" + ", ".join(f'"{e}"' for e in emails(roster)) + ")"


def main() -> None:
    with open(ROSTER, encoding="utf-8") as fh:
        roster = json.load(fh)
    if "--list" in sys.argv:
        print("\n".join(emails(roster)))
    else:
        print(clause(roster))


if __name__ == "__main__":
    main()
