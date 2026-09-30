#!/bin/bash
# The evening "is everyone done with their regression modules?" ask, automated --
# the thing a rotating tester used to post by hand.
#
# Fires twice: 19:30 IST asks, 20:00 IST asks again about whatever has not closed
# in the 30 minutes between. Which pass this is comes from the state file, not the
# clock, so a missed 19:30 run degrades to a single ask at 20:00 instead of a
# message claiming it already asked.
#
# Runs the whole chain unattended -- manual.py, missing.py, then nudge.py --send
# -- so a scheduler can invoke it without Claude in the loop. Every safety rail
# that does not need a human is still enforced inside nudge.py: the 19:30 IST /
# weekday gate, the exact regression-status thread, and the refusal to post if
# not one owner resolves to a Slack user.
#
#   ./first-check.sh              # today (IST), posts to #qa-team-global
#   ./first-check.sh 2026-09-04   # a specific day
#   DRY=1 ./first-check.sh        # render only, send nothing, write no state
#
# Exit 0 = posted, or nothing left to nudge. Non-zero = refused or failed; the
# reason is in the log, which is the only place anyone sees it when unattended.
set -uo pipefail

SK="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Pinned, not `python3`: a scheduler can hand out /usr/bin/python3 (3.9) and the
# scripts are developed against 3.10. Override with PY= if this moves.
PY="${PY:-/Library/Frameworks/Python.framework/Versions/3.10/bin/python3}"
[ -x "$PY" ] || PY=python3

DATE="${1:-$(TZ=Asia/Kolkata date +%F)}"
WORK="${TMPDIR:-/tmp}/ddr-first-check"
mkdir -p "$WORK"
STATE="$WORK/$DATE.state.json"

exec >>"$WORK/$DATE.log" 2>&1
if [ -f "$STATE" ]; then PASS="second (follow-up)"; else PASS="first"; fi
echo "=== $(date '+%F %H:%M:%S %Z')  $PASS pass for $DATE  (DRY=${DRY:-0})"

# Friday pulls the weekly regression group too. Those TEs hold the report exactly
# like the daily ones, so leaving them out would let a Friday be declared ALL
# CLEAR with weekly runs still open. Passed to manual.py only -- NOT to
# missing.py, whose roster was seeded from the two daily filters, so weekly
# suites would land in it as bogus roster rot and withhold the missing half.
WEEKLY=""
if [ "$(date -j -f '%Y-%m-%d' "$DATE" +%u 2>/dev/null)" = "5" ]; then
    WEEKLY="--weekly"
    echo "$DATE is a Friday: including the Weekly regression group."
fi

"$PY" "$SK/manual.py"  --date "$DATE" $WEEKLY --json > "$WORK/manual.json"  || {
    echo "manual.py failed; nothing sent"; exit 1; }
"$PY" "$SK/missing.py" --date "$DATE" --json > "$WORK/missing.json" || {
    echo "missing.py failed; nothing sent"; exit 1; }

set -- --data "$WORK/manual.json" --date "$DATE" --state "$STATE"
[ -f "$STATE" ] && set -- "$@" --followup

# The open-TE half comes straight out of Xray and is always trustworthy. The
# missing-TE half is a diff against a stored roster, so a suite that was merely
# RENAMED reads as missing and pings someone who did nothing wrong -- on
# 2026-09-04 six of fifteen "missing" suites were `Exploratory Testing` prefix
# churn. Unattended, nobody sees that and the wrong ping repeats every day, so
# the missing half only ships when the roster and reality agree in both
# directions. Fix with: missing.py --date <a complete day> --update-roster
#
# A collision counts as rot too: two summaries collapsing onto one suite name
# means one of them is invisible to the diff, so "nothing missing" would be an
# unproven claim rather than a clean pass.
ROT=$("$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); print(len(d["unknown"]) + len(d.get("collisions", [])))' \
      "$WORK/missing.json" 2>/dev/null || echo unknown)
if [ "$ROT" = "0" ]; then
    set -- "$@" --missing "$WORK/missing.json"
    MISSING_SHIPPED=1
else
    echo "roster rot: $ROT suite(s) running today are not in expected-tes.json," \
         "so the missing-TE section is withheld (it cannot tell a rename from a" \
         "skip). Open TEs are still nudged. Run --update-roster on a complete day."
    MISSING_SHIPPED=0
fi

[ "${DRY:-0}" = "1" ] || set -- "$@" --send
"$PY" "$SK/nudge.py" "$@"
RC=$?

# All clear = nothing left holding the report. Counted off manual.json rather
# than off nudge.py's exit code, which is 0 both for "posted" and for "nothing to
# nudge" and so cannot distinguish them. Only the open-TE half gates this: when
# the missing half was withheld above, its contents are unproven either way, so
# it can neither block the report nor be waved through silently.
OPEN=$("$PY" -c 'import json,sys
d = json.load(open(sys.argv[1]))
t = d.get("pending_tes", [])
print(sum(x.get("todo",0) + x.get("executing",0) for x in t), len(t))' \
      "$WORK/manual.json" 2>/dev/null || echo "unknown unknown")
set -- $OPEN; RUNS="${1:-unknown}"; TES="${2:-unknown}"

if [ "$RUNS" = "0" ]; then
    echo "ALL CLEAR: 0 open runs across $TES TE(s) for $DATE."
    if [ "$MISSING_SHIPPED" = "0" ]; then
        echo "  Caveat: the missing-TE half was withheld ($ROT unknown suite(s)), so" \
             "'every suite ran' is NOT established -- only 'every TE that exists is" \
             "closed'. Check the roster before treating this as a complete day."
    fi
    # Deliberately does not send the report. Step 3 (defects) is Jira MCP run by
    # an agent -- there is no defects script and no Jira credential outside
    # .xray-credentials -- so data.json cannot be assembled here, and Step 6
    # requires a human to see the rows and subject before the email goes out.
    # This marker is the handoff: it says the blocking question got answered.
    [ "${DRY:-0}" = "1" ] || date '+%F %H:%M:%S %Z' > "$WORK/$DATE.allclear"
    echo "  Report NOT sent: Steps 3 and 5-6 need the agent (defects come from" \
         "Jira MCP, and the rows/subject are shown before sending). Marker:" \
         "$WORK/$DATE.allclear"
else
    echo "HOLD: $RUNS open run(s) across $TES TE(s) still out."
fi
exit $RC
