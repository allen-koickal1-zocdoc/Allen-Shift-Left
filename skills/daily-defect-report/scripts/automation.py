"""Automation row, from TeamCity (NOT Xray).

The dashboard gadget mirrors the TeamCity Playwright build: `total` is the
suite size and gadget PASSED = TeamCity passed + muted. Verified against the
2026-08-19 gadget screenshot (754/20/774) vs build #624 (753 passed, 20 failed,
1 muted, 774 total).
"""
import argparse, collections, json, subprocess, sys
from common import xray_token, xray_graphql

BUILD_TYPE = "ProdTests_Sandbox_AllPlaywrightTests"


def tc_api(path):
    p = subprocess.run(["teamcity", "api", path], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"teamcity api failed: {p.stderr.strip()[:400]}")
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        raise SystemExit(f"teamcity api returned non-JSON:\n{p.stdout[:400]}")


PW_QUERY = (
    '{ getTestExecutions(jql: "project = ZPR AND labels = playwright AND created >= '
    '\\"%s\\" AND created < \\"%s\\"", limit: 100, start: %d) { total results { '
    'jira(fields: ["summary"]) testRuns(limit: 100) { results { status { name } } } } } }')


def xray_batches(day, nextday):
    """Independent view of the same runs: the Playwright reporter files one Xray
    TE per spec, stamped `PW <date> HH:MM ...` in UTC. Grouping by HH gives a
    per-run tally to reconcile against TeamCity."""
    tok = xray_token()
    start, tes, total = 0, [], None
    while True:
        g = xray_graphql(PW_QUERY % (day, nextday, start), tok)["getTestExecutions"]
        tes += g["results"]
        total = g["total"]
        start += 100
        if start >= total:
            break
    batches = collections.defaultdict(collections.Counter)
    for te in tes:
        parts = te["jira"]["summary"].split()
        hh = parts[2][:2] if len(parts) > 2 and ":" in parts[2] else "??"
        for r in te["testRuns"]["results"]:
            batches[hh][r["status"]["name"]] += 1
    return batches


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="report date, YYYY-MM-DD")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-crosscheck", action="store_true",
                    help="skip the Xray reconciliation (network-heavy)")
    a = ap.parse_args()

    data = tc_api(f"/app/rest/builds?locator=buildType:{BUILD_TYPE},count:10"
                  "&fields=build(number,state,finishDate,"
                  "testOccurrences(count,passed,failed,muted,ignored))")
    builds = data.get("build", [])
    if not builds:
        raise SystemExit("No TeamCity builds returned.")

    running = [b for b in builds if b.get("state") != "finished"]
    finished = [b for b in builds if b.get("state") == "finished"]
    if not finished:
        raise SystemExit("No finished build available yet.")

    b = finished[0]
    t = b.get("testOccurrences") or {}
    total, passed = t.get("count", 0), t.get("passed", 0)
    failed, muted = t.get("failed", 0), t.get("muted", 0)
    if not total:
        raise SystemExit(f"Build #{b['number']} reports no tests; refusing to guess.")

    gadget_passed = passed + muted
    if gadget_passed + failed != total:
        raise SystemExit(f"Build #{b['number']} does not reconcile: "
                         f"{passed}+{muted}+{failed} != {total}")

    row = [gadget_passed, 0, 0, failed, 0, 0, 0, 0, total]
    stamp = b.get("finishDate", "")
    day = f"{stamp[0:4]}-{stamp[4:6]}-{stamp[6:8]}" if len(stamp) >= 8 else "?"

    warn = []
    if day != a.date:
        warn.append(f"latest finished build is from {day}, not {a.date}")
    if running:
        warn.append(f"{len(running)} build(s) still running — numbers may move")

    cross = None
    if not a.no_crosscheck:
        import datetime
        nxt = (datetime.date.fromisoformat(a.date)
               + datetime.timedelta(days=1)).isoformat()
        try:
            batches = xray_batches(a.date, nxt)
        except SystemExit as e:
            warn.append(f"Xray cross-check unavailable: {e}")
        else:
            # The build's own batch is the one whose PASSED+FAILED matches the
            # suite size; retried specs inflate other batches above it.
            match = [hh for hh, c in batches.items()
                     if c.get("PASSED", 0) + c.get("FAILED", 0) == total
                     and c.get("FAILED", 0) == failed]
            cross = {hh: dict(c) for hh, c in sorted(batches.items())}
            if not match:
                warn.append(
                    f"no Xray batch reconciles with TeamCity #{b['number']} "
                    f"({gadget_passed} passed / {failed} failed / {total}); "
                    f"batches seen: {cross}")

    out = {"row": row, "build": b["number"], "finished": stamp,
           "teamcity": {"passed": passed, "muted": muted, "failed": failed,
                        "total": total},
           "xray_batches": cross, "warnings": warn}
    if a.json:
        print(json.dumps(out))
    else:
        print(f"Build #{b['number']} finished {stamp}")
        print(f"  TeamCity: passed={passed} muted={muted} failed={failed} total={total}")
        print(f"  Gadget:   PASSED={gadget_passed} FAILED={failed} Total={total}")
        if cross:
            print("  Xray batches (UTC):")
            for hh, c in cross.items():
                print(f"    {hh}  {c}")
    for w in warn:
        print(f"WARNING: {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
