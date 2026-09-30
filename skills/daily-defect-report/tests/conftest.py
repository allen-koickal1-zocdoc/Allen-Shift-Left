"""Shared fixtures. Everything here mocks at the network boundary only.

The scripts' own logic is never stubbed -- a test that patched `classify` or
`normalize` would pass while the thing the report depends on stayed broken.
Only `slack()` and `xray_graphql()` are replaced, because those are the two
calls that leave the machine.
"""
import datetime
import os
import sys

import pytest
from zoneinfo import ZoneInfo

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "scripts")
sys.path.insert(0, SCRIPTS)

IST = ZoneInfo("Asia/Kolkata")
ET = ZoneInfo("America/New_York")


def ts_at(y, m, d, hh, mm, tz=IST) -> str:
    """A Slack `ts` string for a wall-clock time in a named zone.

    Tests state the time in the zone the humans actually posted in, so a
    failure reads as "a 01:00 IST post was dropped" rather than as a float.
    """
    return f"{datetime.datetime(y, m, d, hh, mm, tzinfo=tz).timestamp():.6f}"


def msg(text, ts, user="U1", real_name="Astha Singh", **extra):
    m = {"text": text, "ts": ts, "user": user,
         "user_profile": {"real_name": real_name}}
    m.update(extra)
    return m


def reminder(ts, text="Reminder: <!here> Can everyone share updates on the "
                      "regression status before logging out?", replies=0):
    """The 18:30 IST Slackbot post whose thread the device posts hang off.

    `replies` sets `reply_count`, which is what collect() keys off to decide
    whether to fetch the thread at all -- a parent without it is never expanded,
    exactly as in real Slack.
    """
    m = {"text": text, "ts": ts, "user": "USLACKBOT", "subtype": "bot_message"}
    if replies:
        m["reply_count"] = replies
    return m


@pytest.fixture
def fake_slack(monkeypatch):
    """Replace devices.slack with a canned channel history.

    Returns a setter so each test declares the history it needs. Replies are
    keyed by parent ts to exercise the "post landed in an older thread" path.
    """
    import devices

    state = {"messages": [], "replies": {}}

    def _slack(method, **fields):
        if method == "conversations.history":
            return {"messages": state["messages"]}
        if method == "conversations.replies":
            parent = fields["ts"]
            return {"messages": [{"ts": parent}] + state["replies"].get(parent, [])}
        if method == "conversations.info":
            return {"channel": {"name": "qa-team-global"}}
        raise AssertionError(f"unexpected slack method {method}")

    monkeypatch.setattr(devices, "slack", _slack)

    def setup(messages, replies=None):
        state["messages"] = messages
        state["replies"] = replies or {}
        return state

    return setup
