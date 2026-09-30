"""Suites with no Test Execution created for the day.

The saved filters are scoped to today, so a prior day's roster cannot be
replayed out of Xray -- `filter = "..." AND created` on 2026-08-21 returns 0
while the same shape on 2026-08-24 returns 15. The expectation therefore has to
be stored, and it is stored explicitly in expected-tes.json rather than inferred
from a rolling window of previous days: a suite skipped two days running would
drop out of an inferred baseline and silently stop being flagged forever.

A roster can still go stale, so both sides of the diff are always printed --
suites missing today, and suites running today that the roster does not know
about. `--update-roster` rewrites it from today's actual set.

Only meaningful once the day has closed: the filters fill up all afternoon
(2026-08-24 smoke went 3 -> 15 TEs between 09:00 and 15:45 ET).
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import xray_token, xray_graphql          # noqa: E402
from manual import FILTERS, owner_of                 # noqa: E402

ROSTER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "expected-tes.json")

QUERY = ('{ getTestExecutions(jql: "filter = \\\"%s\\\"", limit: 100) { total '
         'results { jira(fields: ["key","summary","created","assignee",'
         '"reporter"]) } } }')

# "TE  2026Aug24  Homepage Smoke" -> "Homepage Smoke". Spacing around the date
# token is inconsistent between testers, so collapse whitespace afterwards.
NOISE = re.compile(r"\b(TE|20\d\d[A-Za-z]{3}\d{1,2}|\d{4}-\d\d-\d\d)\b", re.I)

# A leading mode marker, stripped so the same suite matches whichever way it was
# labelled that day. Confirmed with the team 2026-09-04: the prefix is a mode on
# one suite, not a separate TE, and it churns in BOTH directions -- `Branded
# Directory Daily Regression` gained the prefix while `Patient Intake Smoke` lost
# it, which is why matching on the raw summary reported six renames as six
# missing suites and pinged six people who had done nothing wrong.
#
# `Daily Regression` requires the dash; `Exploratory Testing` does not. Only the
# dashed form has been observed for the former, and stripping a bare leading
# "Daily Regression " would eat the start of any suite genuinely named that way.
MODE = re.compile(r"^(?:Exploratory Testing\s*-?\s*|Daily Regression\s*-\s*)", re.I)


def normalize(summary):
    core = re.sub(r"\s+", " ", NOISE.sub("", summary)).strip(" -")
    return MODE.sub("", core).strip(" -")


def today_set(token, date):
    """({label: {normalized suite: owner}}, collisions) for the TEs that exist now."""
    out, collisions, seen_key = {}, [], {}
    for label, fname in FILTERS.items():
        g = xray_graphql(QUERY % fname, token)["getTestExecutions"]
        if g["total"] > len(g["results"]):
            raise SystemExit(f"{label}: filter holds {g['total']} TEs, page "
                             f"returned {len(g['results'])}; add pagination.")
        if not g["results"]:
            raise SystemExit(f"{label}: filter returned no Test Executions.")
        offday = [r["jira"]["key"] for r in g["results"]
                  if not r["jira"].get("created", "").startswith(date)]
        if offday:
            raise SystemExit(f"{label}: TEs not created on {date}: "
                             + ", ".join(offday))
        suites = {}
        for r in g["results"]:
            suite = normalize(r["jira"]["summary"])
            if not suite:
                raise SystemExit(f"{label}: {r['jira']['key']} summary "
                                 f"{r['jira']['summary']!r} normalizes to "
                                 "nothing; fix NOISE before trusting the diff.")
            # Stripping the mode prefix means two summaries can now collapse onto
            # one key. Under the confirmed model that should not happen on a single
            # day, so it is reported rather than resolved: picking one of the two
            # owners would chase the wrong person, and dropping the pair would hide
            # a suite. Non-fatal on purpose -- a hard exit here would take the
            # open-TE nudge down with it, and open TEs are never in doubt.
            if suite in suites:
                collisions.append({"suite": suite, "label": label,
                                   "keys": sorted([seen_key[(label, suite)],
                                                   r["jira"]["key"]])})
            else:
                seen_key[(label, suite)] = r["jira"]["key"]
            suites[suite] = owner_of(r["jira"])[0]
        out[label] = suites
    return out, collisions


def normalize_roster(roster):
    """Apply normalize() to the stored keys too, so the fix is retroactive.

    The roster was seeded from raw summaries, so it holds the mode prefix on whatever
    suites happened to carry it that day. Normalizing only today's side would leave
    every prefixed roster entry permanently unmatched -- the exact false-positive this
    is meant to remove. Doing it on load rather than rewriting the file keeps the
    stored owners intact, which a --update-roster would overwrite with today's
    assignees.
    """
    out, collisions, seen = {}, [], {}
    for label, suites in roster.items():
        norm = {}
        for suite, owner in suites.items():
            key = normalize(suite)
            if key in norm:
                collisions.append({"suite": key, "label": f"{label} (roster)",
                                   "keys": sorted([seen[(label, key)], suite])})
            else:
                seen[(label, key)] = suite
            norm[key] = owner
        out[label] = norm
    return out, collisions


def diff(roster, today):
    missing, unknown = [], []
    for label in sorted(set(roster) | set(today)):
        expected, actual = roster.get(label, {}), today.get(label, {})
        for suite in sorted(expected):
            if suite not in actual:
                missing.append({"suite": suite, "label": label,
                                "owner": expected[suite]})
        for suite in sorted(actual):
            if suite not in expected:
                unknown.append({"suite": suite, "label": label,
                                "owner": actual[suite]})
    return missing, unknown


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="report date YYYY-MM-DD")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--update-roster", action="store_true",
                    help="rewrite expected-tes.json from today's actual set")
    a = ap.parse_args()

    today, collisions = today_set(xray_token(), a.date)

    # Before the --update-roster early return as well: adopting a roster built from a
    # colliding day would bake the loss in permanently -- one of the two suites simply
    # would not be in the file, and would never be flagged again.
    for c in collisions:
        print(f"COLLISION {c['suite']} [{c['label']}] — {', '.join(c['keys'])} both "
              "normalize to this suite; owner is ambiguous, diff is not trustworthy",
              file=sys.stderr)

    if a.update_roster:
        with open(ROSTER, "w") as fh:
            json.dump(today, fh, indent=1, sort_keys=True)
            fh.write("\n")
        for label, suites in sorted(today.items()):
            print(f"{label}: {len(suites)} suites, "
                  f"{len({o for o in suites.values() if o})} owners")
        print(f"wrote {ROSTER}")
        return

    if not os.path.exists(ROSTER):
        raise SystemExit(f"No roster at {ROSTER}. Seed it on a day you know is "
                         "complete with: missing.py --date <DATE> --update-roster")
    with open(ROSTER, encoding="utf-8") as fh:
        roster, roster_collisions = normalize_roster(json.load(fh))
    for c in roster_collisions:
        print(f"COLLISION {c['suite']} [{c['label']}] — {', '.join(c['keys'])} both "
              "normalize to this suite; the roster has a duplicate to merge by hand",
              file=sys.stderr)
    collisions += roster_collisions
    missing, unknown = diff(roster, today)

    # stderr, before the early return: --json is the mode the unattended path uses,
    # and it used to swallow this half of the diff entirely -- so roster rot was
    # invisible exactly when nobody was watching, which is when it does the damage.
    # stdout stays pure JSON.
    for u in unknown:
        print(f"NEW      {u['suite']} [{u['label']}] — {u['owner']} "
              "(not in roster; --update-roster to adopt)", file=sys.stderr)

    if a.json:
        print(json.dumps({"missing": missing, "unknown": unknown,
                          "collisions": collisions}))
        return

    for m in missing:
        who = m["owner"] or "UNOWNED in roster"
        print(f"MISSING  {m['suite']} [{m['label']}] — {who}")
    if not missing:
        print(f"Every roster suite has a TE for {a.date}.")


if __name__ == "__main__":
    main()
