---
name: daily-defect-report
description: Build and send the daily QA "FAIL[n] - Defect Report" email. Use when the user says "defect report", "daily report", "FAIL report", or asks to create/send the QA end-of-day report.
---

# Daily QA Defect Report

Produces the `FAIL[n] - Defect Report` email. Every number comes from a script or an
explicit query — **never** from a previous run, a screenshot, or memory.

`$SK` below = `~/.claude/skills/daily-defect-report`. All scripts take `--date YYYY-MM-DD`,
the report date. Where a day boundary has to be resolved from a timestamp — `devices.py` reading
Slack, `nudge.py` gating the first check — it is the team's day in **IST** (`Asia/Kolkata`), never
the machine's local zone. Work in a scratch dir: `mkdir -p /tmp/ddr && cd /tmp/ddr`.

## Preflight

**Run this only after the working day has closed (after ~4pm ET).** The one exception is
the Step 2a first check, which deliberately fires at 19:30 IST while the team is still
online — everything else here waits. Automation batches land
as late as 19:00 UTC and manual runs flip from TO DO all afternoon. A mid-day report is
wrong and will be rejected. If asked earlier, say so, and only produce a provisional report
if the user insists.

Never reuse data from earlier in the session — re-pull everything.

## Step 1 — Automation row (TeamCity)

```bash
python3 $SK/scripts/automation.py --date <DATE> --json
```

TeamCity, **not** Xray, is the source. The script picks the latest *finished* build of
`ProdTests_Sandbox_AllPlaywrightTests`, maps `passed + muted → gadget PASSED`, and asserts
`PASSED + FAILED == total`.

It then **cross-checks against Xray independently**: the Playwright reporter files one TE per
spec stamped `PW <date> HH:MM` (UTC), so grouping runs by hour gives a second, unrelated view of
the same build. One batch must reconcile exactly with TeamCity's passed/failed. Note the two
sources only agree when a run had no retries — retried specs inflate the Xray raw count above the
suite size (2026-08-20 15 UTC: 782 raw vs TeamCity 774), which is why TeamCity stays the source.

Any stderr warning — build not from `--date`, a build still running, no reconciling batch —
**must be surfaced to the user, never swallowed**. Both guards are tested to fire.

The row is a snapshot of the latest build **at send time**, so it legitimately changes during the
day (2026-08-20: #629 → 772/2/774 at 09:19 ET, #631 → 774/0/774 at 15:38 ET). That is why the
report must wait for the day to close.

## Step 2 — Manual rows (Smoke / Daily Regression)

```bash
python3 $SK/scripts/manual.py --date <DATE> --json
```

Scope comes from the two saved Jira filters that back the dashboard gadgets. Xray's
`getTestExecutions` accepts `filter = "<name>"` JQL, so the script resolves them itself:

- `EOD Daily Smoke Report - Filter` → **Smoke** gadget `10317?maximized=11994`
- `EOD Daily Regression Report - Filter` → **Daily Regression** gadget `10317?maximized=11985`

Never reconstruct the scope from TE summary strings — that heuristic missed 3 TEs and included
a superseded one. The filters are the definition.

It hard-fails on an empty filter, >100 TEs, a TE truncated at 100 runs, an unmapped status, or —
with `--date` — any TE not created on the report date, which catches the filter dragging in
another day's runs. Always pass `--date`. The saved filters are live and roll over at midnight, so this step
only works for the **current** day — asking for yesterday makes the date assertion fire. It warns on TO DO/EXECUTING (day not closed). Runs are counted **raw** — never dedupe by test key.

Alongside the aggregate warning it emits `pending_tes` — one entry per TE holding
TO DO/EXECUTING runs, with the owner taken from the TE's `assignee`, falling back to its
`reporter`. Both come back in the same query; a TE with neither is reported `UNOWNED`,
never assigned to someone by guess.

On Fridays there is also a weekly gadget (`10317?maximized=11984`), backed by
`EOD Weekly Regression Report - Filter` (recovered 2026-08-21 by probing candidate names).
Pass `--weekly` and it resolves that filter itself and renders a third table. The weekly group
is the **one** exemption from the `--date` assertion — its scope is week-of, so its TEs are
created Mon–Fri — and the exemption is keyed on the group *name*, so every other group must
still prove it belongs to the report date. `--keys` still works for a hand-pinned scope:

```json
{"Smoke": ["ZPR-1"], "Daily Regression": ["ZPR-2"], "Weekly": ["ZPR-3"]}
```

`first-check.sh` passes `--weekly` automatically on a Friday, because weekly TEs hold the
report exactly like daily ones: on 2026-09-04 they contributed **6 TEs and 49 open runs** that
the 19:40 pass never saw, which would have let the evening look far closer to done than it was.
It is passed to `manual.py` only, never `missing.py`, whose roster was seeded from the two daily
filters — weekly suites would land there as bogus roster rot and withhold the missing half.

With `--keys`, resolve the Weekly keys from that filter and tally them **without** `--date`: the weekly
scope is week-of, so its TEs are created across Mon-Fri and the date assertion would fire.
Run Smoke/Daily Regression with `--date` as usual, Weekly as a separate `--keys` call.
Beware that Xray returns `total: 0` for a filter name that does not exist rather than erroring,
so a name probe only proves a match when it comes back non-empty.

## Step 2a — Nudge on open and missing executions

Two things hold the report: TEs still running, and TEs never raised at all.

```bash
python3 $SK/scripts/manual.py  --date <DATE> --json > manual.json     # open runs
python3 $SK/scripts/missing.py --date <DATE> --json > missing.json    # no TE at all
python3 $SK/scripts/nudge.py --data manual.json --missing missing.json --date <DATE>
python3 $SK/scripts/nudge.py --data manual.json --missing missing.json --date <DATE> --send
```

`missing.py` diffs today's filter contents against `expected-tes.json`, a roster of
normalized suite name → expected owner (26 suites, seeded 2026-08-24). It is a stored
roster, not an inferred one, because the saved filters are scoped to today and a prior
day cannot be replayed: `filter = "EOD Daily Smoke Report - Filter" AND created` returns
0 for 2026-08-21 and 15 for 2026-08-24. Inferring the baseline from recent days would
also decay silently — a suite skipped twice would drop out and never be flagged again.

Suites running today that the roster does not know about print as `NEW` on stderr;
`--update-roster` rewrites it from today's actual set, which is also how a reassignment
is recorded. Run that only on a day you know was complete. Both halves of the diff are
always printed, so roster rot is visible rather than silent.

Summaries are normalized by stripping the `TE` prefix and the `2026Aug24` token and
collapsing whitespace — the spacing is inconsistent between testers. A summary that
normalizes to nothing is a hard failure, not a silent skip.

Like every other number here, this only means anything after the day closes: on
2026-08-24 the smoke filter grew from 3 TEs at 09:00 ET to 15 by 15:45.

It posts **one** message @-mentioning each owner — open TEs with their keys and counts,
then missing suites phrased as a question ("On leave or not running today?"), since a
legitimate absence is indistinguishable from a miss and a wrong ping costs one reply.
Dry-run is the default and sends nothing — show the user the rendered message and send only
on their confirmation. The target channel is resolved to its name and printed in that
preview, so a post cannot land somewhere unnoticed.

**It posts to `#qa-team-global` (`C056DQA8DP1`), as a reply in that day's
regression-status thread** — the same thread Step 4 reads the device and version posts
from. `devices.regression_thread()` is the single resolver both steps call, so the nudge
and the Platform table cannot end up pointing at different days. `devices.py` prints the
thread it resolved as a permalink, along with how many of that day's device posts actually
came from it, so the two can be eyeballed against each other.

The parent is matched exactly: the `share updates on the regression status` reminder whose
own timestamp falls on the report date (18:30 IST / 09:00 ET). It is never resolved to the
nearest day — this channel keeps several days of threads live at once, and a nudge sitting
in yesterday's thread reads as being about yesterday. Nor is it silently promoted to a
top-level post: `#qa-team-global` already carries six reminders a day. If zero or two
reminders match, `--send` is refused before any Slack lookup and the reason is printed;
`--thread-ts <ts>` names a parent by hand and `--no-thread` opts out to channel level, both
deliberate and both shown in the preview. The other daily reminders (`QAE on extended`,
`MOBILE WEB REGRESSION DAY`, `Automation Thread`, `reassign regression modules`) are
verified not to match.

`--channel C095XR1DN1F` (`#personal`) still rehearses the whole thing privately. The
preview always prints the resolved channel *name* and a clickable thread permalink for the
channel being posted to, so read those two before confirming.

Names resolve through `zd-slack user "<display name>"`, and **only an exact match is
accepted**. A fuzzy or ambiguous hit is printed as `UNRESOLVED` and left as plain text in the
post rather than mentioned as the wrong person — a bare `Allen` matches three people. If not
one name resolves it refuses to post at all: a nudge that mentions nobody reaches nobody
while still looking like the step ran.

**It fires twice, 19:30 and 20:00 IST, Monday to Friday** (`NUDGE_AFTER = (19, 30)`,
`TEAM_TZ = Asia/Kolkata`). The 19:30 pass asks; the 20:00 pass asks again about whatever has
not closed in between and says that it is asking again. This is the automated form of the "is everyone done with their regression
modules?" ask a rotating tester posted by hand — ten of those between 2026-08-10 and
2026-09-03 landed 19:18–20:54 IST, median ~20:05, so 19:30 beats the human by ~35 min while
the team is still online to act on it.

It is deliberately **not** the report's 16:00 ET gate, which is 01:30 IST — hours after this
team logs off. That gate exists because automation batches land as late as 19:00 UTC, but the
nudge only ever covers *manual* TEs (`manual.py`, `missing.py`), so the automation batch has
no bearing on it. Steps 5 and 6 still wait for 16:00 ET.

#### The second pass

Which pass a run is comes from `--state`, **not from the clock**, so a run that slips does not
misdescribe itself. `nudge.py --state <file>` records the TE keys it posted about — only after
a confirmed send, never on a dry run or a failed write — and `--followup` reads it back:

- a TE in the state file and still open → *"Asked at 19:30 IST — these have not closed yet"*
- a TE not in it → listed under *"Also open"*, deliberately **not** "since then": on a Friday
  the weekly group is queried for the first time in the second pass, so its TEs may have been
  open all along rather than newly opened
- a TE that closed in between → **not mentioned at all**, so nobody is pinged twice for work
  they already finished
- no usable state file (or one dated another day) → treated as a first ask, with a note on
  stderr. A missed 19:30 run degrades to one ask at 20:00 rather than to a message claiming it
  had already asked.

Worth knowing it works: on 2026-09-04 the 19:40 pass named 7 TEs, 5 of them closed within 20
minutes, and the 20:00 follow-up correctly re-asked about only the other 2.

`--date` used to be decorative — rendered into the message but never compared to the clock —
so an early run asked the owner of an untouched suite whether they were "on leave or not
running today" when the suite simply was not due yet. Before 19:30 IST, and on a Saturday or
Sunday, every line it renders is a false positive by construction, so `--send` exits non-zero
(before any Slack lookup) and dry-run stamps `EARLY` or `WEEKEND` on stderr; `--force`
overrides and says so. A future `--date` is refused outright; a past weekday counts as due, a
past *weekend* day stays `weekend`. Boundary is tested at 19:29/19:30 IST on both sides, on a
weekday and on a Monday.

### Running it unattended

```bash
scripts/first-check.sh              # today (IST); the whole chain, then --send
scripts/first-check.sh 2026-09-04   # a specific day
DRY=1 scripts/first-check.sh        # render only, send nothing, write no state
```

Runs `manual.py` → `missing.py` → `nudge.py --send` with no Claude in the loop, logging to
`$TMPDIR/ddr-first-check/<date>.log`. The same script serves both passes — it adds
`--followup` when `<date>.state.json` already exists — and adds `--weekly` on a Friday.

Scheduled by a **LaunchAgent**, not cron: agents run inside the logged-in GUI session, so
`zd-slack` can reach its Keychain credentials; cron cannot. `com.zocdoc.qa.first-check.plist`
holds 10 `StartCalendarInterval` entries (19:30 and 20:00, Weekday 1–5) and `RunAtLoad false`,
so loading it at 14:00 cannot post at 14:00. `nudge.py` refuses weekends independently, so a
mistake in the plist cannot produce a Saturday ping. Install it from a **normal Terminal** —
`~/Library/LaunchAgents` and `crontab` are both denied inside the Zocdoc sandbox:

```bash
cp ~/.claude/skills/daily-defect-report/com.zocdoc.qa.first-check.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.zocdoc.qa.first-check.plist
launchctl list | grep first-check
```

Note `plutil -lint` validates XML only, not key names — it passed a fabricated
`StartCalendarIntervalRunMissed` key that launchd would have silently ignored. No key is needed:
launchd already runs a missed calendar job on wake, and if it wakes the next day `nudge.py`'s
date check refuses rather than posting stale counts.

**All clear does not send the report.** When the open-run count reaches 0 the wrapper logs
`ALL CLEAR` and touches `<date>.allclear`, and stops. Step 3 (defects) is Jira MCP run by the
agent — there is no defects script and no Jira credential outside `.xray-credentials` — so
`data.json` cannot be assembled unattended, and Step 6 requires a human to see the rows and
subject first. The marker is a handoff, not a send. When the missing-TE half was withheld,
`ALL CLEAR` is also logged with the caveat that it establishes *"every TE that exists is
closed"*, **not** *"every suite ran"*.

**A scope mismatch retries once, then hard-fails.** Resolving a saved filter and tallying its
keys are two separate Xray calls, so a TE leaving scope between them is a race, not a
discrepancy — it fired for real at 20:11 IST on 2026-09-04 (13 listed, 12 tallied) while the
team was still closing TEs, and killed the unattended pass. `tally` now raises a narrow
`ScopeRace` for that one mismatch; `main` re-resolves the filter once and says so on stderr. A
mismatch that survives the retry is genuine and still exits non-zero, and with `--keys` it is
never re-resolved at all, since a hand-pinned scope that disagrees is wrong rather than racing. It pins Python 3.10 because cron hands out
`/usr/bin/python3` (3.9); `devices.py` also carries `from __future__ import annotations` so a
bare `python3` no longer dies on `list | None` at import.

**Unattended, it withholds the missing-TE section whenever the roster is stale.** Open TEs
come straight out of Xray and are always trustworthy, but the missing half is a diff against
`expected-tes.json`, and a suite that was merely *renamed* reads as missing — on 2026-09-04
six of fifteen "missing" suites were `Exploratory Testing` prefix churn (7 by 20:15), which would have
pinged five people who had done nothing wrong, every day, with nobody watching. So the
missing half only ships when the diff is clean in both directions. Clear it with
`missing.py --date <a complete day> --update-roster`.

Related: `missing.py --json` used to return before printing its `NEW` lines, so roster rot was
invisible in exactly the mode the unattended path uses. It now writes `NEW` to stderr before
the early return, leaving stdout pure JSON.

**Then stop.** Report who was pinged and wait for the user before continuing. Open runs mean
the day has not closed, which Preflight already treats as disqualifying — the report is held
on the answer, not sent past the question.

## Step 3 — Defects (Jira MCP, you run these)

```
issuetype = Bug AND labels = testing-type-exploratory AND created >= "<DATE>" AND created < "<DATE+1>"
```
→ **Defects Logged by QA**; its count is the `n` in `FAIL[n]`.

```
issuetype = Bug AND labels = testing-type-automation AND created >= "<DATE>" AND created < "<DATE+1>"
```
→ **Automation Test Failures Logged by QA**.

`testing-type-acceptance` belongs to neither — exclude it. Read summaries fresh at send time;
they get edited during the day. Capture key / summary / reporter display name / priority.

**Then check for label hygiene** — the count is only as good as the labels, so confirm no QA-filed
bug is missing one. Get the reporter clause from the roster instead of typing names:

```bash
python3 $SK/scripts/reporters.py   # reporter in ("akash.nair@zocdoc.com", ... )  — 13 owners
```

```
issuetype = Bug AND created >= "<DATE>" AND created < "<DATE+1>"
  AND <paste the clause from reporters.py>
  AND (labels IS EMPTY OR labels NOT IN (testing-type-exploratory, testing-type-automation,
       testing-type-acceptance, "testing-type-dailyWeekly-regression"))
```

Anything returned is unclassified: read it and decide which bucket it belongs to (on 2026-08-20
`SQUAWK-7040` came back — Environment: QA, siblings all acceptance, so correctly excluded).

Do **not** hand-maintain the name list here. It was inlined until 2026-09-22 and had rotted to 6
of 13 owners, so bugs from the other seven never reached this check — and because the six it did
list still returned rows, the query looked healthy. Re-running the widened clause over
2026-09-15..21 surfaced six unlabeled bugs the old list had missed (`PROVPERF-3038/3039/3040`,
`PATINS-4418/4419/4430`). `reporters.py` derives from `expected-tes.json`, which Step 2 already
keeps current, so the two cannot drift apart.

Keep the reporter filter. Dropping it is not a safe simplification: unfiltered, that same week
returns 184 bugs org-wide against 15 from the QA roster.

Do **not** use `membersOf("jira-qa-team")` — that group does not exist and silently returns 0,
which looks like a clean pass. Any query that filters on a group or label must be paired with a
control that proves it can return rows.

These MCP queries return full descriptions regardless of the `fields` argument and can blow past
the token limit. Use `searchResultMode: "count"` first, and when the output overflows to a file,
pull what you need with `jq`, not `Read`.

## Step 4 — Platform & Devices

```bash
python3 $SK/scripts/devices.py --date <DATE>            # --crosscheck for uncovered rows
```

**The table is whatever #qa-team-global says that day.** Testers post what they tested on,
one short line each, under the 6:30 PM "share updates on the regression status" reminder:
`iPhone 13 mini 4.231`, `Samsung S25 Ultra 3.252`, `Windows Chrome 151`, `Safari 26.4`.
Nothing here is derived from Jira or copied from a previous day's email.

Five things the script handles that reading the thread by eye gets wrong:

- **Posts land in the previous day's thread.** People answer whichever reminder is still
  scrolled up, so only the post's own timestamp decides the day. On 2026-08-20 the day's
  only Android post sat in the Aug 19 thread — reading just that day's thread loses it.
- **The day is the team's day, in IST.** `--date` means an `Asia/Kolkata` calendar day
  (`devices.py` `TEAM_TZ`, the same clock `nudge.py` gates the nudge on). Every day comparison
  goes through one helper so it cannot depend on the laptop: while the timestamps were resolved
  naively, an ET-configured machine moved the boundary to 14:30 ET and silently dropped every
  post after it, and the same history bucketed two different ways on two different machines.
- **One post can state two devices.** Each line is classified on its own words. Classifying the
  whole message both lost the second device and mislabelled the first — on 2026-09-16 a message
  carrying `Edge 152` and `Android Chrome 149` reported the Edge line as Mobile Web, because it
  borrowed the `Android` belonging to the other line. Lines that are not device posts classify
  to nothing and drop out, so splitting cannot invent rows.
- **A bare browser post is ambiguous — ask, do not guess.** Only the OS the tester prefixed
  decides the row: `Android Chrome 151` is Mobile Web, `Windows Chrome 151` is Desktop Web.
  A plain `Safari 26.4` says neither, so the script lists it under **ASK** and refuses to
  place it. Put the question to the user (or in the channel) before building the table.
  Whether the 10:00 `MOBILE WEB REGRESSION DAY` reminder fired is printed as a hint, not an
  answer. Guessing here is what put a wrong `Mobile Web / iPhone` row in the 2026-08-20
  email. Precedent: the Aug 20 bare Safari posts were confirmed as **Desktop Web / MacBook**.
  Blocking and asking is the required behaviour even on an unattended run — do not fall back
  to the mobile-web-day inference. A *named handset* is not ambiguous, though:
  `Samsung S25 Ultra Chrome 151` is Mobile Web and reports the model the tester posted, not a
  flattened `Android`. The model patterns are shared with the app rows, so a handset the app row
  recognises can never be one the web rows send to ASK — that mismatch, plus a `MOBILE_CTX` list
  that had drifted out of sync and filed OnePlus under Desktop Web, is what sent real posts to
  ASK. Device strings always come from the post; nothing is invented.
- **Slackbot reminders look like device posts** — that mobile-web reminder carries
  `:iphone:` and `:android:` emoji. Bot messages are dropped and emoji stripped.

A row nobody posted prints as `-- NO POST TODAY --`. **Drop it, or ask in the channel.**
Carry a default forward only if you can confirm it is still current, and never invent a
device model — `iPhone 17` was a fabrication that shipped in the 2026-08-20 email.
`--crosscheck` confirms an uncovered app row against the Xray `PT - <platform> <version>`
build-acceptance ladder; the table tracks the *shipped* build, which lags PT by ~5-9 days,
so the newest PT is normally still in acceptance.

Backtested against Aug 18 / 19 / 20 2026; the Aug 19 reconstruction matches the report
that was actually sent that day on every posted row. Re-backtested on Sep 16 / 17 / 18 2026 after
the timezone and per-line fixes: no row changed except Sep 16, which correctly went from 6 counted
posts to 7.

## Step 5 — Build

Write `data.json`:

```json
{
  "date": "2026-08-20",
  "defects": [{"key": "PS-14760", "summary": "...", "reporter": "Harsh Khadde", "priority": "Minor"}],
  "automation_defects": [],
  "platforms": [["Desktop Web", "MacBook", "Safari 26.4 / 26.5 / 26.6 / 27"],
                ["Android Mobile App", "Samsung S25 Ultra", "3.252"]],
  "rows": {"Smoke": [68,0,0,0,0,0,1,0,69], "Daily Regression": [28,0,0,0,0,0,0,0,28]},
  "automation_row": [772,0,0,2,0,0,0,0,774]
}
```

```bash
python3 $SK/scripts/build_report.py --data data.json --out report.html   # prints the subject
```

Only include the platform rows the channel actually supported that day — the example above
is the real 2026-08-20 table, which had no iOS or Mobile Web post.

Rows are `[PASSED, TO DO, EXECUTING, FAILED, ABORTED, BLOCKED, PASS MINOR BUG, SKIPPEDPASS, Total]`;
the builder rejects any row that does not sum. With zero defects the subject is
`PASS - Defect Report | <Mon D>`, not `FAIL[0]`.

## Verification (not optional)

The behaviours claimed below are pinned by a regression suite. Run it after touching anything in
`scripts/`:

```bash
$SK/tests/run.sh                 # whole suite
$SK/tests/run.sh -k devices      # one module
```

It mocks only the two calls that leave the machine (`slack()`, `xray_graphql()`) — never the
scripts' own logic, so a test cannot pass while the thing the report depends on is broken. Each
module carries its own rejecting control, because a suite of only-green cases proves nothing.

Every number in this email is checked before it is shown to the user, and the check is only
trusted if it could have failed:

- **Automation** — TeamCity reconciles internally *and* against an independent Xray batch.
- **Manual** — per-TE created dates match the report date, runs sum to the total, no TE near the
  100-run cap, zero TO DO/EXECUTING.
- **Defects** — the label query plus the unlabelled-QA-bug sweep above.
- **Platforms** — every row traces to a #qa-team-global post that day. A row with no
  post is dropped or queried in the channel, never filled in from memory; a bare
  browser+version post is asked about, never assigned to a row by guess.
- **Nudge timing** — refused before 19:30 IST and on weekends, so neither a 4am run nor a
  Sunday run can ping anyone about work that is not due. Verified by injecting `now` either
  side of the boundary (19:29/19:30, weekday and Monday) and on both weekend days, not by
  reading the clock.
- **Second pass** — the follow-up names only TEs the first pass actually posted about, proven
  by a state file it re-reads rather than by the clock. Verified on 2026-09-04: 5 of 7 closed in
  the 20-minute gap and none of the 5 was pinged again. A state file dated another day is
  refused, not trusted, so a follow-up cannot claim an ask that never happened.
- **Scope race** — the single re-resolve is only trusted because a mismatch that *persists*
  across it still fails, and a `--keys` scope refuses to be re-resolved; both are tested.
- **Roster trust** — the unattended path proves `unknown` is empty before it will ship the
  missing-TE section; on a rotten roster it logs the count and ships only the open-TE half.
- **Open executions** — every unfinished TE is nudged with a real `<@Uxxxx>` mention. An
  `UNRESOLVED` or `UNOWNED` line is surfaced to the user, never dropped, and a nudge that
  resolved zero mentions is a failure to surface, not a clean pass.
- **Nudge target** — the parent ts resolves to that day's regression-status reminder and
  nothing else; checked on 2026-09-01/02/03, where every device post that day came from the
  resolved thread, and against injected history for the no-reminder, two-reminder,
  decoy-reminder and post-in-yesterday's-thread cases. A thread that cannot be resolved is
  a refusal, not a top-level post.
- **Missing executions** — `missing.py` reporting nothing missing is only a pass because
  the same diff demonstrably flags an injected suite; the roster's own staleness is
  reported as `NEW` every run rather than assumed away.
- A query returning 0 is only a pass once a control query proves the same filter can return rows.

If a number cannot be verified, say so plainly instead of sending it.

## Step 6 — Send

Show the user the three rows, the defect list and the subject **before** sending. Draft first,
then send after they confirm:

```bash
zd-gws gmail draft list --timeout 4m | grep "FAIL\["            # orphan check FIRST
zd-gws gmail draft create --to <recipient> --subject "<subject>" --html --timeout 4m < report.html
zd-gws gmail draft send <draft-id> --timeout 4m                  # id is POSITIONAL
zd-gws gmail draft list --timeout 4m | grep "FAIL\["            # must be empty
```

Default recipient `allen.koickal@zocdoc.com`. The real distribution list is
`technology-qa-regressionreport@zocdoc.com` — confirmed from the `To:` header on every peer
report. Only use it when the user names it explicitly.

`--timeout` needs a unit (`4m`). `warning: failed to save refreshed token: exit status 161` is
benign. A client-side timeout can still create the draft server-side, hence the orphan checks.

**PHI:** the email leaves this machine. Defect summaries occasionally quote real data — if any
summary could identify a patient, stop and ask the user to review before sending. This cannot
be overridden.

## Gotchas

- Xray auth intermittently drops TLS (`EOF ... _ssl.c:997`); `common.py` already retries.
- A JQL containing `"` must escape them as `\"` inside a GraphQL string literal, or Xray 400s.
- The latest automation build can be *smaller* than an earlier one after a partial rerun — that
  is correct, do not adjust it upward.
- Credentials live in `$SK/.xray-credentials` (chmod 600). Never echo them.
