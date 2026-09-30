"""Shared helpers: Xray auth + status column layout."""
import json, os, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
CREDS = os.path.join(os.path.dirname(HERE), '.xray-credentials')
TOKEN_CACHE = os.path.join(HERE, '.xray_token')

# Column order of the Jira "Test Runs Summary" gadget. Xray reports the
# PASS MINOR BUG status as the single token PASSMINORBUG.
STATUSES = ["PASSED", "TO DO", "EXECUTING", "FAILED", "ABORTED", "BLOCKED",
            "PASSMINORBUG", "SKIPPEDPASS"]
HEADERS = ["PASSED", "TO DO", "EXECUTING", "FAILED", "ABORTED", "BLOCKED",
           "PASS MINOR BUG", "SKIPPEDPASS", "Total"]


def _creds():
    for key in ("XRAY_CLIENT_ID", "XRAY_CLIENT_SECRET"):
        if key not in os.environ and os.path.exists(CREDS):
            for line in open(CREDS):
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    os.environ.setdefault(k, v)
    cid, sec = os.environ.get("XRAY_CLIENT_ID"), os.environ.get("XRAY_CLIENT_SECRET")
    if not cid or not sec:
        raise SystemExit(f"Missing Xray credentials. Set XRAY_CLIENT_ID/"
                         f"XRAY_CLIENT_SECRET or populate {CREDS}")
    return cid, sec


def xray_token(max_attempts=4):
    """Mint a JWT. The auth endpoint intermittently drops TLS
    ('EOF occurred in violation of protocol') so retry before giving up."""
    if os.path.exists(TOKEN_CACHE) and time.time() - os.path.getmtime(TOKEN_CACHE) < 3000:
        tok = open(TOKEN_CACHE).read().strip().strip('"')
        if tok:
            return tok
    cid, sec = _creds()
    last = None
    for attempt in range(1, max_attempts + 1):
        try:
            req = urllib.request.Request(
                "https://xray.cloud.getxray.app/api/v1/authenticate",
                data=json.dumps({"client_id": cid, "client_secret": sec}).encode(),
                headers={"Content-Type": "application/json"})
            raw = urllib.request.urlopen(req, timeout=60).read().decode()
            open(TOKEN_CACHE, "w").write(raw)
            os.chmod(TOKEN_CACHE, 0o600)
            return raw.strip().strip('"')
        except Exception as e:                                  # noqa: BLE001
            last = e
            time.sleep(3 * attempt)
    raise SystemExit(f"Xray auth failed after {max_attempts} attempts: {last}")


def xray_graphql(query, token, max_attempts=4):
    """Run a GraphQL query. Same transient TLS drop as the auth endpoint, so
    retry the network layer; HTTP and GraphQL errors are deterministic and fail
    immediately."""
    last = None
    for attempt in range(1, max_attempts + 1):
        req = urllib.request.Request(
            "https://xray.cloud.getxray.app/api/v2/graphql",
            data=json.dumps({"query": query}).encode(),
            headers={"Authorization": "Bearer " + token,
                     "Content-Type": "application/json"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=120))
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:400]
            raise SystemExit(
                f"Xray GraphQL HTTP {e.code}. Unescaped quotes in JQL?\n{body}")
        except Exception as e:                                  # noqa: BLE001
            last = e
            time.sleep(3 * attempt)
            continue
        if "errors" in r:
            raise SystemExit(f"Xray GraphQL errors: {r['errors']}")
        return r["data"]
    raise SystemExit(f"Xray GraphQL failed after {max_attempts} attempts: {last}")


def row_from_counter(counter):
    row = [counter.get(s, 0) for s in STATUSES]
    return row + [sum(row)]
