"""Nudge the owners of unfinished Test Executions in #qa-team-global.

Open TO DO/EXECUTING runs mean the day has not closed, which disqualifies the
report (see Preflight). This turns manual.py's `pending_tes` into one channel
post that @-mentions whoever owns each TE, so the report is held on a question
that has been asked rather than on silence. With --missing it adds a second
section for roster suites that have no TE at all today (see missing.py).

Dry-run by default: it renders the message and the name -> Slack ID resolutions
and sends nothing. --send does the write.

A display name is only accepted when `zd-slack user` returns that exact person.
A fuzzy or ambiguous hit is left UNRESOLVED and printed, never mentioned as
somebody else. If nothing resolved at all the post is refused outright -- a
mention-less nudge reaches no one and would otherwise read as a clean pass.

The post is a reply under that day's "share updates on the regression status"
reminder -- the same thread devices.py harvests the Platform & Devices rows from
(devices.regression_thread is the one resolver, so the two cannot disagree). That
keeps the whole day's regression traffic in one place instead of adding a second
top-level ping to a channel that already has six reminders a day. If the thread
cannot be resolved exactly, the post is refused rather than dropped into the
nearest day's thread or silently promoted to channel level: --thread-ts names a
parent by hand, --no-thread opts out on purpose.

It runs twice an evening. The 19:30 IST first pass asks; the 20:00 second pass
asks again about whatever has not closed in between, and says that it is asking
again. Which pass this is comes from --state, not from the clock: the follow-up
names only the TEs the first pass actually posted about, so somebody who closed
theirs at 19:50 is not pinged a second time, and a TE that opened after 19:30 is
listed as new rather than as ignored. With no state file it is a first pass --
a missed 19:30 run degrades to one ask at 20:00 rather than to a message
claiming it already asked.

This is the automated form of the "is everyone done with their regression
modules?" ask a rotating tester has been posting by hand, and it fires at the
same point in the day: 19:30 IST, Monday to Friday. It is refused before that,
and on a weekend, because --date used to be decorative -- rendered into the
message but never compared to the clock -- so an early run would ask the owner
of an untouched suite whether they were "on leave or not running today" when the
suite simply was not due yet. Dry-run still renders so the message can be read,
but it is stamped EARLY or WEEKEND on stderr and --send is refused unless
--force is given.
"""
import argparse, json, os, re, subprocess, sys
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from devices import (CHANNEL as QA_TEAM_GLOBAL, permalink,   # noqa: E402
                     regression_thread, slack)

# Live: nudges go to the team channel, in-thread. --channel overrides; the target
# is resolved to its name and the thread to a clickable permalink, both printed in
# the dry run, so a post never lands somewhere unnoticed.
DEFAULT_CHANNEL = QA_TEAM_GLOBAL   # #qa-team-global
PARKED_CHANNEL = "C095XR1DN1F"     # #personal -- pass --channel here to rehearse

# The team's working day, not the laptop's clock: pinning this to Asia/Kolkata
# keeps the gate on the same wall clock the testers work to even if this machine
# is somewhere else.
TEAM_TZ = ZoneInfo("Asia/Kolkata")
# Ten hand-posted "is everyone done" asks between 2026-08-10 and 2026-09-03 landed
# 19:18-20:54 IST (median ~20:05), so 19:30 sits early in that window: alongside the
# 19:30 reminder, well before the 20:00 "before logging out" one, and while the team
# is still online to act on it.
#
# Deliberately NOT the report's 16:00 ET gate (= 01:30 IST, hours after this team
# logs off). That gate exists because automation batches land as late as 19:00 UTC
# -- but this nudge only ever covers *manual* TEs (manual.py, missing.py), so the
# automation batch has no bearing on it. Steps 5 and 6 still wait for 16:00 ET.
NUDGE_AFTER = (19, 30)
NUDGE_AFTER_STR = f"{NUDGE_AFTER[0]:02d}:{NUDGE_AFTER[1]:02d} IST"

ZD = "/opt/zocdoc/bin/zd-slack"
ID_LINE = re.compile(r"^ID:\s+(\S+)", re.M)
NAME_LINE = re.compile(r"^Name:\s+(.+?)\s*$", re.M)


def day_status(date_str, now=None):
    """('future'|'weekend'|'early'|'due', explanation) for the report date.

    'due' is what used to be called 'closed'. At 19:30 IST the working day has
    not closed, and that is the point -- the ask has to reach people while they
    can still act on it. Only the report itself (Steps 5-6) waits for the day to
    close. Before 19:30 a TO DO run is not late and an absent TE is not missing;
    on a Saturday or Sunday there is no regression run at all, so every line the
    message would render is a false positive either way. `now` is injectable so
    the boundary can be tested at both sides.
    """
    now = now or datetime.now(TEAM_TZ)
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise SystemExit(f"--date must be YYYY-MM-DD, got '{date_str}'")
    stamp = now.strftime("%H:%M IST on %Y-%m-%d")
    if d > now.date():
        return "future", f"{date_str} is in the future (now {stamp})"
    if d.weekday() >= 5:
        return "weekend", (f"{date_str} is a {d:%A}; there is no regression run "
                           f"to chase (now {stamp})")
    if d < now.date():
        return "due", f"{date_str} is a past day (now {stamp})"
    if (now.hour, now.minute) < NUDGE_AFTER:
        return "early", f"it is {stamp}; the check is due at {NUDGE_AFTER_STR}"
    return "due", stamp


def slack_id(display_name):
    """(slack_id, None) on an exact match, else (None, reason)."""
    p = subprocess.run([ZD, "user", display_name], capture_output=True, text=True)
    if p.returncode != 0:
        return None, f"lookup failed: {p.stderr.strip()[:120] or 'no match'}"
    ids, names = ID_LINE.findall(p.stdout), NAME_LINE.findall(p.stdout)
    if not ids:
        return None, "no Slack user found"
    if len(ids) > 1:
        return None, f"ambiguous, matched {len(ids)}: {', '.join(names)}"
    if not names or names[0].strip().lower() != display_name.strip().lower():
        return None, f"fuzzy match returned '{names[0] if names else '?'}'"
    return ids[0], None


def channel_name(cid):
    try:
        return "#" + slack("conversations.info", channel=cid)["channel"]["name"]
    except Exception:                                       # noqa: BLE001
        return cid


def tag_for(who, mentions):
    """Never mention somebody else: an unresolved name stays plain text."""
    if who and mentions.get(who):
        return f"<@{mentions[who]}>"
    return f"*{who}*" if who else "*owner unknown*"


def te_line(te, mentions):
    bits = [f"{te['todo']} TO DO"] if te["todo"] else []
    if te["executing"]:
        bits.append(f"{te['executing']} EXECUTING")
    summary = te["summary"] or te["label"]
    return (f"• {tag_for(te.get('owner'), mentions)} — {te['key']} "
            f"_{summary}_ — {', '.join(bits)}")


def render(date, tes, missing, mentions, prior=None):
    """The post. `prior` = TE keys/suites an earlier pass already asked about.

    Passing it switches the wording to a second ask and splits the list, because
    the two halves need different questions: something asked about 20 minutes ago
    and still open is a "carrying over?", something that appeared since is just an
    open run. Without the split the follow-up would tell the owner of a brand-new
    TE that they had been reminded already.
    """
    lines = []
    if tes:
        if prior is None:
            lines += [f":hourglass_flowing_sand: *Open test executions — {date}*",
                      "The daily defect report is held until these close out:"]
            for te in tes:
                lines.append(te_line(te, mentions))
        else:
            still = [t for t in tes if t["key"] in prior]
            fresh = [t for t in tes if t["key"] not in prior]
            lines.append(f":repeat: *Still open — {date}*")
            if still:
                # NOT "asked at 19:30": the state file records *that* a TE was
                # asked about, not when, and from the third pass onward most of
                # these were first asked at 20:53 or later. Stating a time the
                # record cannot support is the one thing this skill must not do.
                lines.append("Already asked — these have not closed yet:")
                for te in still:
                    lines.append(te_line(te, mentions))
            if fresh:
                if still:
                    lines.append("")
                # "Also open", not "Also open since then": on a Friday the weekly
                # group is queried for the first time in this pass, so a TE absent
                # from the state file may have been open all along rather than
                # newly opened. The neutral label is true in both cases.
                lines.append("Open as of now:" if not still else "Also open:")
                for te in fresh:
                    lines.append(te_line(te, mentions))
        lines.append("Please close these out, or reply here if they're carrying over.")
    if missing:
        if lines:
            lines.append("")
        lines += [f":warning: *No Test Execution created — {date}*",
                  "These suites have no TE for today:"]
        for m in missing:
            lines.append(f"• {tag_for(m.get('owner'), mentions)} — "
                         f"_{m['suite']}_ ({m['label']})")
        lines.append("On leave or not running today? Reply here — otherwise "
                     "please raise the TE.")
    return "\n".join(lines)


def load_prior(path, date):
    """Keys/suites an earlier pass posted about today, or None for a first pass.

    A state file from another date is ignored rather than trusted: it would mark
    every one of today's TEs as "asked at 19:30" when nobody was asked at all.
    """
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            st = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"state file {path} unreadable ({exc}); treating this as a first "
              f"pass", file=sys.stderr)
        return None
    if st.get("date") != date:
        print(f"state file is for {st.get('date')}, not {date}; treating this as "
              f"a first pass", file=sys.stderr)
        return None
    return set(st.get("tes", [])) | set(st.get("suites", []))


def save_state(path, date, tes, missing):
    """Union with what is already recorded: pass three must still know what pass
    one asked about.

    Re-reads the file rather than taking load_prior()'s return value, which
    deliberately flattens TE keys and suite names into one set for membership
    tests. Unioning that flat set back into both buckets is wrong -- it put every
    key into `suites` too, and the "not in suites" filter then dropped them from
    `tes`, quietly emptying the record the next pass depends on.
    """
    prev = {}
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                prev = json.load(fh)
        except (OSError, json.JSONDecodeError):
            prev = {}
        if prev.get("date") != date:
            prev = {}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"date": date, "written": datetime.now(TEAM_TZ).isoformat(),
                   "tes": sorted(set(prev.get("tes", []))
                                 | {te["key"] for te in tes}),
                   "suites": sorted(set(prev.get("suites", []))
                                    | {m["suite"] for m in missing})},
                  fh, indent=1)
        fh.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True,
                    help="manual.py --json output, or - for stdin")
    ap.add_argument("--date", required=True, help="report date YYYY-MM-DD")
    ap.add_argument("--missing", help="missing.py --json output (optional)")
    ap.add_argument("--channel", default=DEFAULT_CHANNEL,
                    help=f"target channel id (default {DEFAULT_CHANNEL} "
                         f"#qa-team-global; {PARKED_CHANNEL} is #personal, for "
                         f"rehearsing)")
    ap.add_argument("--thread-ts",
                    help="parent message ts to reply under, when the day's "
                         "regression-status reminder cannot be resolved")
    ap.add_argument("--no-thread", action="store_true",
                    help="post at channel level instead of in-thread")
    ap.add_argument("--send", action="store_true",
                    help="actually post; omit to dry-run")
    ap.add_argument("--state",
                    help="json file recording which TEs were posted about, so a "
                         "later pass can ask again about only what is still open")
    ap.add_argument("--followup", action="store_true",
                    help="second pass: word it as asking again, using --state")
    ap.add_argument("--force", action="store_true",
                    help=f"nudge before {NUDGE_AFTER_STR}, or on a weekend, "
                         f"anyway")
    ap.add_argument("--note",
                    help="one trailing line, e.g. that this repeats and when it "
                         "stops. A post that reappears on a timer looks identical "
                         "to the previous one without it")
    a = ap.parse_args()

    raw = json.load(sys.stdin if a.data == "-" else open(a.data))
    tes = raw.get("pending_tes", raw) if isinstance(raw, dict) else raw
    missing = json.load(open(a.missing)).get("missing", []) if a.missing else []
    if not tes and not missing:
        print("No open Test Executions and no missing TEs — nothing to nudge.")
        return

    state, day_why = day_status(a.date)
    if state == "future":
        raise SystemExit(f"Refusing to nudge: {day_why}.")
    blocked = state in ("early", "weekend") and not a.force
    if blocked and a.send:
        open_runs = sum(te.get("todo", 0) + te.get("executing", 0) for te in tes)
        tail = (f"Re-run after {NUDGE_AFTER_STR}, or pass --force to nudge early "
                f"anyway." if state == "early" else
                "Pass --force to nudge on a weekend anyway.")
        raise SystemExit(
            f"Refusing to send: {day_why}. Nothing is late yet - {open_runs} "
            f"open run(s) across {len(tes)} TE(s) and {len(missing)} suite(s) "
            f"with no TE are simply not due. {tail}")

    prior = load_prior(a.state, a.date) if a.followup else None
    if a.followup and prior is None:
        print("--followup but no usable state for today: nothing has been asked "
              "yet, so this is being sent as a first ask.", file=sys.stderr)

    thread_ts, thread_why = a.thread_ts, None
    if not thread_ts and not a.no_thread:
        thread_ts, thread_why = regression_thread(
            datetime.strptime(a.date, "%Y-%m-%d").date())
        if not thread_ts and a.send:
            raise SystemExit(
                f"Refusing to send: no regression-status thread resolved for "
                f"{a.date} - {thread_why}. The nudge belongs under the same "
                f"thread the device and version posts come from. Check the "
                f"channel, then pass --thread-ts <ts> to name the parent, or "
                f"--no-thread to post at channel level on purpose.")

    owners = [te["owner"] for te in tes if te.get("owner")]
    owners += [m["owner"] for m in missing if m.get("owner")]
    mentions, unresolved = {}, []
    for who in dict.fromkeys(owners):
        sid, why = slack_id(who)
        if sid:
            mentions[who] = sid
        else:
            unresolved.append((who, why))

    msg = render(a.date, tes, missing, mentions, prior)
    if a.note and msg:
        msg += f"\n\n_{a.note}_"
    target = channel_name(a.channel)
    if thread_ts:
        where = (f"{target} ({a.channel}) in-thread -> "
                 f"{permalink(thread_ts, a.channel)}")
    elif a.no_thread:
        where = f"{target} ({a.channel}) at channel level (--no-thread)"
    else:
        where = (f"{target} ({a.channel}) -- NO THREAD RESOLVED: {thread_why}; "
                 f"--send will be refused")
    if blocked:
        print(f"{state.upper()}: {day_why}. Every line below is a false positive; "
              f"--send is refused.", file=sys.stderr)
    elif state in ("early", "weekend"):
        print(f"{state.upper()}, overridden by --force: {day_why}.",
              file=sys.stderr)
    print(f"--- {where} ---\n{msg}\n---")
    for who, sid in mentions.items():
        print(f"resolved: {who} -> {sid}")
    for who, why in unresolved:
        print(f"UNRESOLVED: {who} — {why}", file=sys.stderr)
    for te in tes:
        if not te.get("owner"):
            print(f"UNOWNED: {te['key']} has no assignee or reporter",
                  file=sys.stderr)
    for m in missing:
        if not m.get("owner"):
            print(f"UNOWNED: roster suite '{m['suite']}' has no owner",
                  file=sys.stderr)

    if not mentions:
        raise SystemExit("Refusing to post: not one owner resolved to a Slack "
                         "user, so the nudge would mention nobody. Resolve the "
                         "names above or post it by hand.")

    if not a.send:
        if blocked:
            print(f"\nDry run — nothing sent, and --send would be refused: "
                  f"{day_why}.")
        else:
            print("\nDry run — nothing sent. Re-run with --send to post.")
        return

    cmd = ([ZD, "thread", a.channel, thread_ts, msg] if thread_ts
           else [ZD, "write", a.channel, msg])
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"zd-slack {cmd[1]} failed: {p.stderr.strip()[:300]}")
    print(f"\nPosted to {where}. {p.stdout.strip()[:200]}")
    # Only after the post is confirmed. Recording it on a dry run or a failed
    # write would make the next pass say "asked at 19:30" about an ask that never
    # reached the channel.
    if a.state:
        save_state(a.state, a.date, tes, missing)
        print(f"state -> {a.state}")


if __name__ == "__main__":
    main()
