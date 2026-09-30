"""Manual rows (Smoke / Daily Regression) from the saved Jira filters.

Scope MUST come from the dashboard's own saved filters, never from matching
TE summary strings. On 2026-08-20 string matching found 9 Daily Regression TEs
where the filter held 11: it missed three created mid-morning and wrongly
included a superseded Inbox TE.

Xray's getTestExecutions accepts arbitrary JQL, including `filter = "<name>"`,
so this resolves the filters itself — no Jira MCP round-trip. Pass --keys only
to override the scope (e.g. to add the Friday weekly group).
"""
import argparse, collections, json, sys
from common import xray_token, xray_graphql, row_from_counter, STATUSES

FILTERS = {"Smoke": "EOD Daily Smoke Report - Filter",
           "Daily Regression": "EOD Daily Regression Report - Filter"}

# Friday only, and tallied WITHOUT --date: the weekly scope is week-of, so its
# TEs are created Mon-Fri and the created-on-report-date assertion would fire on
# four fifths of them. Recovered 2026-08-21 by probing candidate names -- Xray
# answers a filter name that does not exist with total: 0 instead of an error, so
# a name is only proven by a non-empty result, which tally() enforces.
WEEKLY_LABEL = "Weekly"
WEEKLY_FILTER = "EOD Weekly Regression Report - Filter"

KEYS_QUERY = ('{ getTestExecutions(jql: "filter = \\\"%s\\\"", limit: 100) '
              '{ total results { jira(fields: ["key"]) } } }')

QUERY = ('{ getTestExecutions(jql: "key in (%s)", limit: 100) { total results { '
         'jira(fields: ["key","summary","created","assignee","reporter"]) '
         'testRuns(limit: 100) { total results { status { name } } } } } }')


def owner_of(jira):
    """Who to chase about an unfinished TE. Assignee first, then whoever created
    it; both come back in the same query. Never invent one -- an unowned TE is
    reported as such so it can be asked about."""
    for src in ("assignee", "reporter"):
        user = jira.get(src) or {}
        if user.get("displayName"):
            return user["displayName"], src
    return None, None


class ScopeRace(Exception):
    """The saved filter's key list and the key-in tally disagreed.

    Raised only for that one mismatch, so main() can re-resolve and retry it
    without also swallowing the >100-run, unmapped-status or wrong-date guards.
    """


def filter_keys(name, token, label):
    g = xray_graphql(KEYS_QUERY % name, token)["getTestExecutions"]
    if g["total"] > len(g["results"]):
        raise SystemExit(f"{label}: filter holds {g['total']} TEs, page returned "
                         f"{len(g['results'])}; add pagination.")
    return [r["jira"]["key"] for r in g["results"]]


def tally(keys, token, label, date=None):
    if not keys:
        raise SystemExit(f"{label}: filter returned no Test Executions.")
    if len(keys) > 100:
        raise SystemExit(f"{label}: {len(keys)} TEs exceeds the 100 page size; "
                         "add pagination before trusting this number.")
    g = xray_graphql(QUERY % ",".join(keys), token)["getTestExecutions"]
    if g["total"] != len(keys):
        # Resolving the filter and tallying its keys are two separate calls, so a
        # TE leaving scope between them is a race, not a discrepancy -- it fired
        # for real at 20:11 IST on 2026-09-04 (13 listed, 12 tallied) while the
        # team was still closing TEs, and an unattended run died on it. main()
        # re-resolves once; a mismatch that survives that is genuine and still
        # hard-fails.
        raise ScopeRace(f"{label}: filter listed {len(keys)} TEs but Xray "
                        f"returned {g['total']}.")
    counter, truncated, unknown = collections.Counter(), [], set()
    offday, pending_tes = [], []
    for te in g["results"]:
        if date and not te["jira"].get("created", "").startswith(date):
            offday.append(te["jira"]["key"] + " (" +
                          te["jira"].get("created", "?")[:10] + ")")
        runs = te["testRuns"]
        if runs["total"] != len(runs["results"]):
            truncated.append(f"{te['jira']['key']} ({runs['total']} runs)")
        te_counter = collections.Counter()
        for x in runs["results"]:
            name = x["status"]["name"]
            if name not in STATUSES:
                unknown.add(name)
            counter[name] += 1
            te_counter[name] += 1
        todo, executing = te_counter.get("TO DO", 0), te_counter.get("EXECUTING", 0)
        if todo or executing:
            who, src = owner_of(te["jira"])
            pending_tes.append({"key": te["jira"]["key"],
                                "summary": (te["jira"].get("summary") or "").strip(),
                                "label": label, "todo": todo, "executing": executing,
                                "owner": who, "owner_source": src})
    if truncated:
        raise SystemExit(f"{label}: >100 runs on {', '.join(truncated)}; "
                         "paginate testRuns before trusting this number.")
    if unknown:
        raise SystemExit(f"{label}: unmapped Xray status {sorted(unknown)} — "
                         "add it to STATUSES in common.py.")
    if offday:
        raise SystemExit(f"{label}: TEs not created on {date}: "
                         + ", ".join(offday)
                         + ". The saved filter is pulling another day's runs.")
    return row_from_counter(counter), len(keys), counter, pending_tes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keys", help="optional keys JSON, overrides the saved filters")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--date", help="report date YYYY-MM-DD; asserts every TE "
                                   "was created that day")
    ap.add_argument("--weekly", action="store_true",
                    help=f"add the Friday '{WEEKLY_LABEL}' group from the saved "
                         f"filter, exempt from the --date assertion")
    a = ap.parse_args()

    token = xray_token()
    if a.keys:
        groups = json.load(open(a.keys))
    else:
        groups = {label: filter_keys(name, token, label)
                  for label, name in FILTERS.items()}
    if a.weekly and WEEKLY_LABEL not in groups:
        groups[WEEKLY_LABEL] = filter_keys(WEEKLY_FILTER, token, WEEKLY_LABEL)
    # The weekly group is the one exemption from the date assertion, and it is
    # named rather than inferred: every other group must still prove it belongs
    # to the report date.
    dates = {label: (None if label == WEEKLY_LABEL else a.date) for label in groups}

    def resolve(label):
        if label == WEEKLY_LABEL:
            return filter_keys(WEEKLY_FILTER, token, label)
        return filter_keys(FILTERS[label], token, label)

    out, pending, pending_tes = {}, {}, []
    for label, keys in groups.items():
        try:
            row, n, counter, tes = tally(keys, token, label, dates[label])
        except ScopeRace as race:
            # Only re-resolvable when the scope came from a saved filter. With
            # --keys the caller pinned the scope by hand, so a mismatch there means
            # the pinned list is wrong and must not be quietly replaced.
            if a.keys:
                raise SystemExit(f"{race} Scope came from --keys, so it cannot be "
                                 f"re-resolved; fix the key list.")
            print(f"{race} Re-resolving the filter once -- a TE most likely left "
                  f"scope between the two calls.", file=sys.stderr)
            keys = resolve(label)
            try:
                row, n, counter, tes = tally(keys, token, label, dates[label])
            except ScopeRace as again:
                # Twice is not a race. Re-raised as SystemExit so an unattended
                # log gets one readable line instead of a traceback.
                raise SystemExit(f"{again} Still mismatched after re-resolving, so "
                                 f"this is a real discrepancy, not a race. Do not "
                                 f"trust the count until it is explained.")
            print(f"{label}: reconciled on retry at {n} TEs.", file=sys.stderr)
        out[label] = row
        pending_tes.extend(tes)
        todo = counter.get("TO DO", 0) + counter.get("EXECUTING", 0)
        if todo:
            pending[label] = todo
        if not a.json:
            detail = " ".join(f"{s}={counter[s]}" for s in STATUSES if counter.get(s))
            print(f"{label}: TEs={n} {detail} TOTAL={row[-1]}")

    if a.json:
        print(json.dumps({"rows": out, "pending": pending,
                          "pending_tes": pending_tes}))
    elif pending:
        print("\nWARNING: unfinished runs — the day is not closed:", file=sys.stderr)
        for label, n in pending.items():
            print(f"  {label}: {n} TO DO/EXECUTING", file=sys.stderr)
        for te in pending_tes:
            bits = [f"{te['todo']} TO DO"] if te["todo"] else []
            if te["executing"]:
                bits.append(f"{te['executing']} EXECUTING")
            who = (f"{te['owner']} ({te['owner_source']})" if te["owner"]
                   else "UNOWNED — ask before chasing")
            print(f"  {te['key']} [{te['label']}] {', '.join(bits)} — {who}",
                  file=sys.stderr)
        print("  -> nudge.py can post these to #qa-team-global", file=sys.stderr)


if __name__ == "__main__":
    main()
