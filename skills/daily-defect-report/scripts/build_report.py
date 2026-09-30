"""Render the FAIL[n] defect report HTML from a data JSON."""
import argparse, datetime, html, json

D = {
    "hl":      "https://zocdoc.atlassian.net/jira/dashboards/10317?maximized=11991",
    "def":     "https://zocdoc.atlassian.net/jira/dashboards/10317?maximized=11989",
    "autodef": "https://zocdoc.atlassian.net/jira/dashboards/20822?maximized=46739",
    "man":     "https://zocdoc.atlassian.net/jira/dashboards/10317",
    "smoke":   "https://zocdoc.atlassian.net/jira/dashboards/10317?maximized=11994",
    "dreg":    "https://zocdoc.atlassian.net/jira/dashboards/10317?maximized=11985",
    "weekly":  "https://zocdoc.atlassian.net/jira/dashboards/10317?maximized=11984",
    "auto":    "https://zocdoc.atlassian.net/jira/dashboards/20822?maximized=46749",
}
HEADERS = ["PASSED", "TO DO", "EXECUTING", "FAILED", "ABORTED", "BLOCKED",
           "PASS MINOR BUG", "SKIPPEDPASS", "Total"]
TH = ('style="background:#c9daf8;border:1px solid #666;padding:5px 9px;'
      'text-align:left;"')
TD = 'style="border:1px solid #666;padding:5px 9px;"'
E = html.escape


def hdr(text, link=None, label=None):
    inner = f'{text}: (<a href="{link}">{label}</a>)' if link else f"{text}:"
    return f'<p><b><span style="color:#1155cc;">{inner}</span></b></p>'


def table(headers, rows):
    h = "".join(f"<th {TH}>{c}</th>" for c in headers)
    body = "".join("<tr>" + "".join(f"<td {TD}>{c}</td>" for c in r) + "</tr>"
                   for r in rows)
    return ('<table style="border-collapse:collapse;font-size:13px;">'
            f"<tr>{h}</tr>{body}</table>")


def gadget(row):
    if len(row) != len(HEADERS):
        raise SystemExit(f"row has {len(row)} cells, expected {len(HEADERS)}")
    if sum(row[:-1]) != row[-1]:
        raise SystemExit(f"row does not sum: {row[:-1]} != {row[-1]}")
    return table(HEADERS, [row])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = json.load(open(a.data))

    defects = d.get("defects", [])
    autodefects = d.get("automation_defects", [])
    n = len(defects)
    noun = "defect was" if n == 1 else "defects were"
    rows = d["rows"]

    p = ['<div style="font-family:Arial,sans-serif;font-size:14px;color:#000;">']
    p.append("<p>Hey team,</p><p>Please find the defect report below.</p>")

    p.append(hdr("Key Highlights"))
    p.append("<ul>")
    p.append(f'<li>Executed exploratory regression. (Link: <a href="{D["hl"]}">Dashboard</a>)</li>')
    p.append(f"<li>{n} new {noun} logged today during exploratory regression.</li>")
    p.append("<li>" + (f"{len(autodefects)} new defect(s) were detected by QA automation tests."
                       if autodefects else
                       "No new defects were detected by QA automation tests.") + "</li>")
    p.append("</ul>")

    def defect_table(items):
        return table(["Key", "Summary", "Reporter", "Priority"],
                     [[f'<a href="https://zocdoc.atlassian.net/browse/{E(i["key"])}">'
                       f'{E(i["key"])}</a>', E(i["summary"]), E(i["reporter"]),
                       E(i["priority"])] for i in items])

    p.append(hdr("Defects Logged by QA", D["def"], "Link to Defects"))
    p.append(f"<p>{n} new {noun} logged today.</p>")
    if defects:
        p.append(defect_table(defects))

    p.append(hdr("Automation Test Failures Logged by QA", D["autodef"], "Link to Defects"))
    if autodefects:
        p.append(f"<p>{len(autodefects)} new defect(s) were logged today.</p>")
        p.append(defect_table(autodefects))
    else:
        p.append("<p>No new defects were logged today.</p>")

    p.append(hdr("Platform &amp; Devices"))
    p.append(table(["Platform", "Device", "Version"],
                   [[E(x) for x in r] for r in d["platforms"]]))

    p.append(hdr("Manual Test Execution Results", D["man"],
                 "QA Manual Test Coverage Dashboard"))
    p.append("<p><i>These numbers reflect exploratory regression results</i></p>")
    p.append(f'<p style="margin-bottom:4px;"><b><a href="{D["smoke"]}">Smoke</a></b></p>')
    p.append(gadget(rows["Smoke"]))
    p.append(f'<p style="margin:12px 0 4px;"><b><a href="{D["dreg"]}">Daily Regression</a></b></p>')
    p.append(gadget(rows["Daily Regression"]))
    if "Weekly" in rows:
        p.append(f'<p style="margin:12px 0 4px;"><b><a href="{D["weekly"]}">Weekly Regression</a></b></p>')
        p.append(gadget(rows["Weekly"]))

    p.append(hdr("Automation Test Execution Results", D["auto"],
                 "QA Automation Test Coverage Dashboard"))
    p.append(gadget(d["automation_row"]))
    p.append("<p>Thanks,<br/>QA Team</p></div>")

    open(a.out, "w").write("".join(p))
    dt = datetime.date.fromisoformat(d["date"])
    # A clean day is 'PASS', not 'FAIL[0]' (cf. 'PASS - Defect Report | Aug 07').
    tag = f"FAIL[{n}]" if n else "PASS"
    print(f'{tag} - Defect Report | {dt.strftime("%b %-d")}')


if __name__ == "__main__":
    main()
