# Triage Tickets Analyzed

## Summary

| Category | Count | % |
|----------|-------|---|
| Email/SMS Notifications | 9 | 28% |
| Insurance Network Status | 7 | 22% |
| Pulse/Internal Tools | 4 | 12% |
| Authentication/Login | 3 | 9% |
| Platform Outage | 3 | 9% |
| Review Verification | 4 | 12% |
| Other | 2 | 6% |

---

## Full Ticket List

### Insurance Network Status Issues (6 tickets)
*Root Causes: OUT-6419 (Jan 6) + OUT-6452 (Jan 30)*

#### From OUT-6419 (Jan 6 SEV1 - iOS display issues)
| Ticket | Summary | Created | Resolution |
|--------|---------|---------|------------|
| [TRIAG-22259](https://zocdoc.atlassian.net/browse/TRIAG-22259) | Inconsistent Insurance Network Status (App vs Web) | Jan 12 | Cannot Reproduce |
| [TRIAG-22256](https://zocdoc.atlassian.net/browse/TRIAG-22256) | In-Network Patient Received OON Notification | Jan 12 | Fixed |

#### From OUT-6452 (Jan 30 - Web display issues)
| Ticket | Summary | Created | Resolution |
|--------|---------|---------|------------|
| [TRIAG-22693](https://zocdoc.atlassian.net/browse/TRIAG-22693) | PR not showing as in-network with insurances | Feb 21 | Done |
| [TRIAG-22479](https://zocdoc.atlassian.net/browse/TRIAG-22479) | INN showing as OON to patients | Feb 2 | Closed |
| [TRIAG-22472](https://zocdoc.atlassian.net/browse/TRIAG-22472) | Insurance issue - OON notification for INN patient | Jan 30 | Closed |
| [TRIAG-22467](https://zocdoc.atlassian.net/browse/TRIAG-22467) | PT's booking incorrectly showing as "out-of-network" | Jan 30 | Fixed |

### Insurance Settings UI Issues (2 tickets)
*Related to insurance data but distinct from display bugs*

| Ticket | Summary | Created | Resolution |
|--------|---------|---------|------------|
| [TRIAG-22544](https://zocdoc.atlassian.net/browse/TRIAG-22544) | Practice user unable to change or update insurances | Feb 6 | Done |
| [TRIAG-22538](https://zocdoc.atlassian.net/browse/TRIAG-22538) | Insurance settings screen stuck, cannot view plans | Feb 5 | Fixed |

---

### Email/SMS Notification Issues (9 tickets)
*Root Cause: Feb 13 SEV2 - Messaging Service Failures*

| Ticket | Summary | Created | Resolution |
|--------|---------|---------|------------|
| [TRIAG-22632](https://zocdoc.atlassian.net/browse/TRIAG-22632) | Provider did not receive appointment confirmation emails | Feb 15 | Fixed |
| [TRIAG-22628](https://zocdoc.atlassian.net/browse/TRIAG-22628) | Not Receiving Email Notifications | Feb 13 | Closed |
| [TRIAG-22627](https://zocdoc.atlassian.net/browse/TRIAG-22627) | Multiple Notification Emails for Same Appointment | Feb 13 | Closed |
| [TRIAG-22622](https://zocdoc.atlassian.net/browse/TRIAG-22622) | Practice not receiving email appointment notifications | Feb 13 | Closed |
| [TRIAG-22621](https://zocdoc.atlassian.net/browse/TRIAG-22621) | PR didn't receive appointment notification | Feb 13 | Fixed |
| [TRIAG-22618](https://zocdoc.atlassian.net/browse/TRIAG-22618) | Multiple Notification Emails for Single Appointment | Feb 13 | Fixed |
| [TRIAG-22617](https://zocdoc.atlassian.net/browse/TRIAG-22617) | Appt notification emails (multiple received) | Feb 13 | Fixed |
| [TRIAG-22616](https://zocdoc.atlassian.net/browse/TRIAG-22616) | Multiple Zocdoc Notifications (12 texts for one appt) | Feb 13 | Fixed |
| [TRIAG-22613](https://zocdoc.atlassian.net/browse/TRIAG-22613) | Automatic appointment cancellation | Feb 13 | Fixed |

---

### Platform Outage - Jan 20 (3 tickets)
*Root Cause: GQL Query Spike + Firewall Bandwidth*

| Ticket | Summary | Created | Resolution |
|--------|---------|---------|------------|
| [TRIAG-22330](https://zocdoc.atlassian.net/browse/TRIAG-22330) | Pulse Outage | Jan 20 | Done |
| [TRIAG-22328](https://zocdoc.atlassian.net/browse/TRIAG-22328) | URGENT: Providers receiving 504 error | Jan 20 | Fixed |
| [TRIAG-22327](https://zocdoc.atlassian.net/browse/TRIAG-22327) | Patient cards bug (page reloads and closes) | Jan 20 | Fixed |

---

### Authentication/Login Issues (3 tickets)
*Root Cause: Mar 16 SEV1 - Provider Login (FGA Misconfiguration)*

| Ticket | Summary | Created | Resolution |
|--------|---------|---------|------------|
| [TRIAG-22914](https://zocdoc.atlassian.net/browse/TRIAG-22914) | Provider Login Error Loop | Mar 16 | Closed |
| [TRIAG-22913](https://zocdoc.atlassian.net/browse/TRIAG-22913) | Error message when logging into Zocdoc | Mar 16 | Fixed |
| [TRIAG-22190](https://zocdoc.atlassian.net/browse/TRIAG-22190) | Unable to verify phone number (2FA) | Jan 6 | Cannot Reproduce |

---

### Pulse/Internal Tools Issues (4 tickets)
*Root Cause: Mar 19 SEV3 - Monolith Sync Delayed*

| Ticket | Summary | Created | Resolution |
|--------|---------|---------|------------|
| [TRIAG-22961](https://zocdoc.atlassian.net/browse/TRIAG-22961) | Pulse update issue | Mar 19 | Fixed |
| [TRIAG-22957](https://zocdoc.atlassian.net/browse/TRIAG-22957) | Issue with Pulse and QPQ Tool | Mar 19 | Fixed |
| [TRIAG-22707](https://zocdoc.atlassian.net/browse/TRIAG-22707) | "Providers" tab bug in Pulse | Feb 24 | Closed |
| [PE-4967](https://zocdoc.atlassian.net/browse/PE-4967) | Provider not appearing in Advanced Location Mapping Tool | Jan 14 | Done |

---

### Review Verification Issues (4 tickets)
*Root Cause: Unknown - No dedicated postmortem found*

| Ticket | Summary | Created | Resolution |
|--------|---------|---------|------------|
| [TRIAG-22858](https://zocdoc.atlassian.net/browse/TRIAG-22858) | Patients Unable to Submit Review Verification Codes | Mar 11 | Fixed |
| [TRIAG-22853](https://zocdoc.atlassian.net/browse/TRIAG-22853) | Review request link does not allow entry of verification code | Mar 10 | Working as Intended |
| [TRIAG-22843](https://zocdoc.atlassian.net/browse/TRIAG-22843) | Patients Unable to Enter Code for Verification | Mar 10 | Fixed |
| [PINATA-6532](https://zocdoc.atlassian.net/browse/PINATA-6532) | Unable to Request Additional Reviews | Mar 4 | Duplicate |

---

### Other (2 tickets)

| Ticket | Summary | Created | Resolution |
|--------|---------|---------|------------|
| [TRIAG-22215](https://zocdoc.atlassian.net/browse/TRIAG-22215) | Atlassian outage | Jan 8 | Duplicate |

---

## Labels Distribution

All tickets share these common labels:
- `bug-due-to-outage` (100%)
- `triage-issue` (100%)
- `issue-type-functional` (87.5%)

---

## Resolution Summary

| Resolution | Count | % |
|------------|-------|---|
| Fixed | 17 | 53% |
| Closed | 7 | 22% |
| Done | 4 | 12% |
| Cannot Reproduce | 2 | 6% |
| Duplicate | 2 | 6% |
| Working as Intended | 1 | 3% |
