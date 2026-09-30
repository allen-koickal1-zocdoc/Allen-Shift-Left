"""Platform & Devices table, built from what people post in #qa-team-global.

Every row comes from the channel: testers post what they tested on that day under
the 6:30 PM "share updates on the regression status" reminder, one short line each
("iPhone 13 mini 4.231", "Windows Chrome 151", "Safari 26.4"). This reads those
posts and prints the table they support. Nothing is inferred from Jira or from a
previous day's email.

A row nobody posted is reported as NO POST, not silently filled from a default.
`--crosscheck` adds two independent confirmations for those rows only.
"""
# PEP 604 annotations below must not be evaluated at import: a cron job that gets
# the system /usr/bin/python3 (3.9) would otherwise die on `list | None`.
from __future__ import annotations

import argparse, collections, datetime, html, json, os, re, subprocess, sys
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# The report day is the TEAM's day, and the team works to IST. Resolving it in
# the machine's local zone -- which is what a bare datetime.fromtimestamp() does
# -- silently moves the day boundary with the laptop: on an ET-configured machine
# every post after 14:30 ET landed on the next day and dropped out of the table,
# and the same history bucketed two different ways on two different laptops.
# nudge.py already pins its gate to this zone; this is the same clock.
TEAM_TZ = ZoneInfo("Asia/Kolkata")

CHANNEL = "C056DQA8DP1"  # #qa-team-global
SELF = "allen.koickal@zocdoc.com"
DEFAULTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "platform-defaults.json")
ROWS = ["Desktop Web", "Mobile Web", "iOS Mobile App", "Android Mobile App"]

# A named handset. Shared by the app rows and by OS_HINT, so a model the app
# row already recognises can never be a device OS_HINT does not know -- that
# mismatch is what sent "Samsung S25 Ultra Chrome 151" to ASK.
ANDROID_MODEL = re.compile(r"\b(samsung|galaxy|pixel|oneplus)\b", re.I)
IOS_MODEL = re.compile(r"\b(iphone|ipad)\b", re.I)

APP_ROWS = [("iOS Mobile App", IOS_MODEL),
            ("Android Mobile App", ANDROID_MODEL)]
BROWSER = re.compile(r"\b(chrome|safari|firefox|edge)\b\s*(?:version\s*)?v?([\d.]+)", re.I)
APPVER = re.compile(r"\b(\d+\.\d[\d.]*)\b")
# Derived from the model patterns above rather than repeating their alternatives:
# the hand-maintained copy had drifted -- it listed samsung/galaxy/pixel but not
# oneplus, so "OnePlus 12 Chrome 151" was classified Desktop Web.
MOBILE_CTX = re.compile(r"\b(android|ios|mobile)\b|" + ANDROID_MODEL.pattern
                        + "|" + IOS_MODEL.pattern, re.I)
# Ordered: a stated model wins over a bare OS word, so "Samsung S25 Ultra
# Chrome 151" reports the model the tester actually posted rather than a
# flattened "Android". `None` means "keep the posted model verbatim" -- the
# device string is then taken from the text, never invented.
OS_HINT = [(re.compile(r"\bwindows\b", re.I), "Windows"),
           (re.compile(r"\bmac(book)?\b", re.I), "MacBook"),
           (ANDROID_MODEL, None),
           (IOS_MODEL, None),
           (re.compile(r"\bandroid\b", re.I), "Android")]
MWEB_DAY = re.compile(r"MOBILE WEB REGRESSION DAY", re.I)
# The 18:30 IST / 09:00 ET Slackbot reminder whose thread the device posts hang
# off. Matched on the stable middle of the string, not the whole line, because
# the surrounding <!here>/bold markup differs between the daily reminders.
STATUS_REMINDER = re.compile(r"share updates on the regression status", re.I)
EMOJI = re.compile(r":[a-z0-9_+\-]+:")


def day_of(ts: str | float) -> datetime.date:
    """The team-local (IST) calendar day a Slack ts falls on.

    Every day comparison in this module goes through here so the answer cannot
    depend on the machine's TZ. Slack ts values are epoch seconds (UTC).
    """
    return (datetime.datetime.fromtimestamp(float(ts), tz=datetime.timezone.utc)
            .astimezone(TEAM_TZ).date())


def time_of(ts: str | float) -> datetime.datetime:
    """The team-local (IST) wall clock for a Slack ts, for display."""
    return (datetime.datetime.fromtimestamp(float(ts), tz=datetime.timezone.utc)
            .astimezone(TEAM_TZ))


def is_bot(msg):
    """Slackbot reminders carry :iphone:/:android: emoji; they are not device posts."""
    return bool(msg.get("user") == "USLACKBOT" or msg.get("bot_id")
                or msg.get("subtype") == "bot_message")


def slack(method, **fields):
    cmd = ["/opt/zocdoc/bin/zd-slack", "api", method]
    for k, v in fields.items():
        cmd += ["-F", f"{k}={v}"]
    for _ in range(3):
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode == 0:
            try:
                return json.loads(p.stdout)
            except json.JSONDecodeError:
                pass
    raise SystemExit(f"zd-slack {method} failed: {p.stderr.strip()[:300]}")


def regression_thread(want: datetime.date,
                      messages: list | None = None
                      ) -> tuple[str | None, str | None]:
    """(parent_ts, None) for that day's regression-status thread, else (None, why).

    This is the thread the device and version posts are replies to, so it is also
    where the nudge belongs. Resolution is exact: the reminder whose *own*
    timestamp falls on `want`, using the same local-day convention as collect().
    Zero matches or two are returned as a reason to surface, never resolved to the
    nearest day -- a nudge landing in yesterday's thread reads as being about
    yesterday, and this channel demonstrably keeps several days of threads live at
    once.
    """
    if messages is None:
        messages = slack("conversations.history", channel=CHANNEL,
                         limit=60).get("messages", [])
    hits = [m["ts"] for m in messages
            if STATUS_REMINDER.search(m.get("text", ""))
            and day_of(m["ts"]) == want]
    if not hits:
        return None, (f'no "regression status" reminder dated {want} in the last '
                      f"{len(messages)} channel messages")
    if len(hits) > 1:
        return None, f"{len(hits)} candidate reminders on {want}: {', '.join(hits)}"
    return hits[0], None


def permalink(ts: str, channel: str = CHANNEL) -> str:
    """Clickable parent link for the dry-run preview.

    `channel` is a parameter, not CHANNEL: --channel can retarget the post, and a
    preview linking to #qa-team-global while posting elsewhere would be worse than
    no link at all.
    """
    return (f"https://zocdoc.enterprise.slack.com/archives/{channel}"
            f"/p{ts.replace('.', '')}")


AMBIGUOUS = "Web (device not stated)"


def classify_all(text):
    """Every device a single post states, one entry per line.

    Testers do put two devices in one message -- 2026-09-16 carried
    "Edge 152\nAndroid Chrome 149" -- and classifying the message as a whole both
    lost the second device and mislabelled the first, because the bare "Edge 152"
    matched the "Android" belonging to the *other* line and was reported as
    Mobile Web. Each line is classified on its own words only. Lines that are not
    device posts (prose, thanks, "done with my modules") classify to None and drop
    out, so splitting cannot invent rows.
    """
    out, seen = [], set()
    for line in text.splitlines():
        line = line.strip()
        hit = classify(line)
        if hit and hit not in seen:
            seen.add(hit)
            out.append((hit, line))
    return out


def classify(text):
    """One channel post -> (row, device, version), or None if it isn't a device post.

    A browser + version is a web row, but only the OS the tester prefixed says which
    one: "Android Chrome 151" is Mobile Web, "Windows Chrome 151" is Desktop Web. A
    bare "Safari 26.4" says neither, so it is returned as AMBIGUOUS to be asked about
    rather than guessed - guessing is what put a wrong Mobile Web row in the
    2026-08-20 email. A device model plus a bare x.y version is an app row.
    """
    b = BROWSER.search(text)
    if b:
        hit = next(((rx, n) for rx, n in OS_HINT if rx.search(text)), None)
        if hit:
            rx, name = hit
            # A named model (name is None) is reported as posted: the tester
            # wrote "Samsung S25 Ultra", and the Device column should say so.
            # Everything up to the browser token is the model.
            dev = name or text[:b.start()].strip(" -|,") or None
            row = "Mobile Web" if MOBILE_CTX.search(text) else "Desktop Web"
        else:
            dev, row = None, AMBIGUOUS
        return (row, dev, f"{b.group(1).title()} {b.group(2)}")
    for row, rx in APP_ROWS:
        m = rx.search(text)
        if m:
            v = APPVER.search(text)
            if not v:
                return (row, text.strip(" -|,") or None, None)
            # The model is on whichever side of the version it was posted on --
            # "Pixel 10 pro 3.257" and "3.257 - Pixel 10 pro" are the same post.
            # Taking the prefix unconditionally left the version-first form with
            # no device, and the table then filled the gap from team defaults,
            # reporting a Samsung for a post that plainly said Pixel.
            before, after = text[:v.start()], text[v.end():]
            dev = (before if m.start() < v.start() else after).strip(" -|,") or None
            return (row, dev, v.group(1))
    return None


def collect(want):
    """Every device post made ON that date, wherever in the channel it landed.

    Testers answer whichever reminder is still scrolled up, so replies routinely
    sit in an older day's thread. Only the post's own timestamp decides the day.
    """
    msgs = slack("conversations.history", channel=CHANNEL,
                 limit=60).get("messages", [])
    mweb = any(MWEB_DAY.search(m.get("text", "")) and day_of(m["ts"]) == want
               for m in msgs)
    thread = regression_thread(want, msgs)

    candidates, seen = [], set()
    for m in msgs:
        day = day_of(m["ts"])
        if not (0 <= (want - day).days <= 4):
            continue
        candidates.append((m, m["ts"]))
        if m.get("reply_count"):
            for r in slack("conversations.replies", channel=CHANNEL,
                           ts=m["ts"]).get("messages", [])[1:]:
                candidates.append((r, m["ts"]))

    posts = []
    for msg, parent_ts in candidates:
        when = time_of(msg["ts"])
        if when.date() != want or msg["ts"] in seen:
            continue
        seen.add(msg["ts"])
        if is_bot(msg):
            continue
        for hit, line in classify_all(EMOJI.sub(" ", msg.get("text", ""))):
            posts.append((when, msg, hit, parent_ts, line))
    return sorted(posts, key=lambda p: p[0]), mweb, thread


def crosscheck(missing, want):
    """Only for rows the channel did not cover. Two independent confirmations."""
    from common import xray_token, xray_graphql
    print("\n--- cross-check for rows with no post")
    q = ('{ getTestExecutions(jql: "project = ZPR AND summary ~ \\"PT\\" AND created >= '
         '\\"%s\\" ORDER BY created DESC", limit: 100) { results { '
         'jira(fields: ["summary","created"]) } } }' %
         (want - datetime.timedelta(days=60)).isoformat())
    pt = re.compile(r"PT\s*-\s*(iOS|Android)\s+([\d.]+?)\s*-\s*Build\s*\((\d+)\)", re.I)
    latest = {}
    for te in xray_graphql(q, xray_token())["getTestExecutions"]["results"]:
        m = pt.search(te["jira"]["summary"])
        day = datetime.date.fromisoformat(te["jira"]["created"][:10])
        if not m or day > want:
            continue
        k = (m.group(1).title(), re.sub(r"\.0$", "", m.group(2)))
        if k not in latest or day > latest[k][0]:
            latest[k] = (day, m.group(3))
    for row in missing:
        plat = "Ios" if row.startswith("iOS") else "Android" if row.startswith("Android") else None
        if not plat:
            continue
        rows = sorted(((v, d, b) for (p, v), (d, b) in latest.items() if p == plat),
                      key=lambda r: r[1], reverse=True)
        pick = next((r for r in rows if (want - r[1]).days >= 5), None)
        print(f"  {row}: newest PT = {rows[0][0]} ({(want-rows[0][1]).days}d, still in "
              f"acceptance); shipped build is likely {pick[0]}" if pick else
              f"  {row}: no PT history")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="report date, YYYY-MM-DD (local)")
    ap.add_argument("--crosscheck", action="store_true",
                    help="confirm rows the channel did not cover")
    a = ap.parse_args()
    want = datetime.date.fromisoformat(a.date)

    posts, mweb, (thread_ts, thread_why) = collect(want)
    print(f"--- #qa-team-global device posts, {want}"
          f"   (MOBILE WEB REGRESSION DAY: {'yes' if mweb else 'no'})")
    if thread_ts:
        n = sum(1 for p in posts if p[3] == thread_ts)
        print(f"  regression-status thread (nudges reply here): "
              f"{permalink(thread_ts)}\n"
              f"    {n} of {len(posts)} device post(s) came from it; "
              f"{len(posts) - n} landed elsewhere in the channel")
    else:
        print(f"  no regression-status thread for {want}: {thread_why}\n"
              f"    nudge.py will refuse to post until this is resolved by hand")

    if not posts:
        raise SystemExit("No device posts that day. Ask in the channel before "
                         "inventing a table.")

    agg = collections.OrderedDict()
    for when, msg, (row, dev, ver), parent_ts, line in posts:
        who = (msg.get("user_profile") or {}).get("real_name") or msg.get("user", "?")
        # The matched line, not the whole message: a post carrying two devices
        # would otherwise print its full text once per row.
        clean = line
        parent_day = day_of(parent_ts)
        note = "" if parent_day == want else f"  [in the {parent_day} thread]"
        print(f'  {when:%H:%M}  {who:<14} {clean[:42]:<44} -> '
              f'{row}{note}')
        d, v = agg.setdefault(row, ([], []))
        for lst, val in ((d, dev), (v, ver)):
            if val and val not in lst:
                lst.append(val)

    if AMBIGUOUS in agg:
        devs, vers = agg.pop(AMBIGUOUS)
        print("\n--- ASK: bare browser + version, no device or OS stated")
        for v in vers:
            print(f"    {v}")
        print(f'  Nobody said whether these were desktop or mobile. The 10:00 '
              f'MOBILE WEB\n  REGRESSION DAY reminder {"DID" if mweb else "did NOT"} '
              f'fire, which is a hint, not an answer.\n'
              f'  Ask before placing them. Do not guess the row or the device.')

    defaults = json.load(open(DEFAULTS))
    print("\n--- Platform & Devices")
    missing = []
    for row in ROWS:
        if row in agg:
            devs, vers = agg[row]
            dev = " / ".join(devs) or defaults.get(row, ["?"])[0]
            src = "" if devs else "   (device not posted; team default)"
            print(f'  {row:<20} {dev:<26} {" / ".join(vers)}{src}')
        else:
            missing.append(row)
    for row in missing:
        print(f"  {row:<20} -- NO POST TODAY --")

    if missing:
        print("\nDrop a row nobody posted, or carry its default forward only if you can "
              "confirm\nit is still current. Do not invent a device model.")
        if a.crosscheck:
            crosscheck(missing, want)


if __name__ == "__main__":
    main()
