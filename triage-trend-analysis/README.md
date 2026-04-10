# Triage Ticket Trend Analysis Report

**Analysis Period:** January 6 - March 19, 2026  
**Total Tickets Analyzed:** 32  
**Report Generated:** April 10, 2026

## Executive Summary

This analysis examined 32 triage tickets filed between January and March 2026. All tickets were tagged with `bug-due-to-outage`, indicating they stemmed from production incidents rather than isolated bugs.

### Key Finding

**100% of these triage tickets trace back to 6 major production incidents.** The triage tickets are symptoms, not root causes. Addressing the underlying incident action items will prevent recurrence.

| Incident | Date | Severity | Triage Tickets | Revenue Impact |
|----------|------|----------|----------------|----------------|
| [Insurance Booking Failures](#1-jan-6-2026--sev1-insurance-booking-failures) | Jan 6 | SEV1 | 2 | ~$97,200 |
| [Platform Outage (GQL Spike)](#2-jan-20-2026--platform-outage) | Jan 20 | SEV2/3 | 3 | TBD |
| [Insurance Display (Web)](#3-jan-30-2026--insurance-display-web) | Jan 30 | - | 4 | $24,000 |
| [SCP Policy Change](#4-feb-12-2026--sev1-booking-down-scp-policy) | Feb 12 | SEV1 | 0 (cascade) | $13,610 |
| [Messaging Service Failures](#5-feb-13-2026--sev2-messaging-service-failures) | Feb 13 | SEV2 | 9 | $0 (human cost high) |
| [Provider Login (FGA)](#6-mar-16-2026--sev1-provider-login-fga-misconfiguration) | Mar 16 | SEV1 | 3 | $0 |
| [Monolith Sync Delayed](#7-mar-19-2026--sev3-monolith-sync-delayed) | Mar 19 | SEV3 | 3 | TBD |

**Note:** Insurance-related issues (OUT-6419 + OUT-6452) represent **~$121,200 in revenue impact** — the single largest category.

---

## Incident Details

### 1. Jan 6, 2026 — SEV1: Insurance Booking Failures

**Incident:** [OUT-6419](https://zocdoc.atlassian.net/browse/OUT-6419)  
**Postmortem:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/INFRA/pages/2541978219)

#### Related Triage Tickets (2)
| Ticket | Issue |
|--------|-------|
| TRIAG-22259 | Inconsistent Insurance Network Status (App vs Web) |
| TRIAG-22256 | In-Network Patient Received OON Notification |

#### Root Cause
Code change in the `Support Provider Insurance Mapping OOM` epic introduced bugs in checking insurance in-network status:

1. **Stage 1 (Jan 6, 7:00-7:13 AM):** Query sent incorrect parameters for provider insurance lookup → 227 bookings lost
2. **Stage 2 (Jan 8-12):** iOS app displayed in-network bookings as out-of-network on appointment details screen → ~2,300 additional bookings lost due to patient cancellations

**Technical details:**
- GQL accepts both cloud & monolith IDs — incorrect ID type was passed
- iOS used a different field than web for showing insurance status
- Legacy feature flag mechanism doesn't support granular rollout

#### Revenue Impact
- **Stage 1:** ~$8,853 (227 bookings)
- **Stage 2:** ~$88,335 (2,300 bookings from cancellations)
- **Total:** ~$97,200

#### Action Items (from postmortem)

| Action | Ticket | Status | Owner |
|--------|--------|--------|-------|
| Add GQL fake support for automated testing | [PINATA-5860](https://zocdoc.atlassian.net/browse/PINATA-5860) | TBD | Insurance |
| iOS FEMv2 metrics for appointment details | [PINATA-6236](https://zocdoc.atlassian.net/browse/PINATA-6236) | TBD | Mobile |
| Android FEMv2 metrics for appointment details | [PINATA-6237](https://zocdoc.atlassian.net/browse/PINATA-6237) | TBD | Mobile |
| Web FEMv2 metrics for appointment details | [PINATA-6159](https://zocdoc.atlassian.net/browse/PINATA-6159) | TBD | Web |
| GQL resolver cleanup - deprecate monolith IDs | [PINATA-6253](https://zocdoc.atlassian.net/browse/PINATA-6253) | TBD | Platform |
| Automated regression tests on bookings | [PINATA-6254](https://zocdoc.atlassian.net/browse/PINATA-6254) | TBD | QA |
| Migrate appointment page API dependencies OOM | [PINATA-4029](https://zocdoc.atlassian.net/browse/PINATA-4029) | TBD | Insurance |

---

### 2. Jan 20, 2026 — Platform Outage

**Incidents:**
- [OUT-6434](https://zocdoc.atlassian.net/browse/OUT-6434) - Higher B.W utilization in PR201 firewall
- [OUT-6435](https://zocdoc.atlassian.net/browse/OUT-6435) - Performance dashboard not loading
- [OUT-6436](https://zocdoc.atlassian.net/browse/OUT-6436) - Provider Dashboard data not loading due to spike in GQL queries

#### Related Triage Tickets (3)
| Ticket | Issue |
|--------|-------|
| TRIAG-22330 | Pulse Outage |
| TRIAG-22328 | URGENT: Providers receiving 504 error |
| TRIAG-22327 | Patient cards bug (page reloads and closes) |

#### Root Cause
Large spike in GQL queries caused failures in provider dashboard loads. This correlated with higher-than-usual bandwidth utilization on PR201 firewalls.

#### Action Items
Status: Pending Action Items on OUT-6434, OUT-6435

---

### 3. Jan 30, 2026 — Insurance Display (Web)

**Incident:** [OUT-6452](https://zocdoc.atlassian.net/browse/OUT-6452)  
**Postmortem:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/INFRA/pages/2605285380)

#### Related Triage Tickets (4)
| Ticket | Issue |
|--------|-------|
| TRIAG-22693 | Provider not showing as in-network with insurances |
| TRIAG-22479 | INN showing as OON to patients |
| TRIAG-22472 | Insurance issue - OON notification for INN patient |
| TRIAG-22467 | PT's booking incorrectly showing as "out-of-network" |

#### Root Cause
Code change in `my-accounts-web-app` triggered a visible bug, but there was an **underlying issue since October 28, 2025** when the `apax_past_appointments_with_off_platform` feature flag was turned on to 100%.

**Technical details:**
- Complex reconciliation logic between monolith and GraphQL data
- GQL and monolith returned inconsistent appointment times for a subset of users
- No FEMv2 metrics on INN vs OON UI display
- No automated tests caught this on the affected code branch

> **"This was the 3rd issue in 2 months around showing out-of-network errors at elevated rates in product"** — Postmortem

#### Revenue Impact
- **$24,000** (lost PEB revenue from cancellations)

#### Action Items (from postmortem)

| Action | Ticket | Status | Owner |
|--------|--------|--------|-------|
| Add metrics and alerts on INN vs OON display | [PINATA-6337](https://zocdoc.atlassian.net/browse/PINATA-6337) | TBD | Booking |
| Move page's data fully OOM | [PINATA-5990](https://zocdoc.atlassian.net/browse/PINATA-5990) | April 2026 | Booking |
| Create insurance network status backend service | TBD | TBD | Insurance |

---

### 4. Feb 12, 2026 — SEV1: Booking DOWN (SCP Policy)

**Incident:** [OUT-6465](https://zocdoc.atlassian.net/browse/OUT-6465)  
**Postmortem:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/INFRA/pages/2668134427)

#### Root Cause
The `FullAWSAccess` Service Control Policy was removed from the `ProdApplication` OU with the assumption that identical attachment to the parent OU would inherit permissions. **SCPs do not inherit like other policies** — they must be applied at every level.

This caused **all AWS actions from all services** to fail with privilege failures for 16 minutes.

#### Timeline
- **10:18 AM:** SCP policy removed
- **10:19 AM:** PagerDuty alerts fire
- **10:34 AM:** Policy restored, incident mitigated
- **TTR:** 16 minutes

#### Revenue Impact
- **208 PE Bookings / 435 total bookings lost**
- **$13,610 revenue impact**

#### Action Items (from postmortem)

| Action | Ticket | Status |
|--------|--------|--------|
| Create staging OU for testing SCP changes | [SRE-2922](https://zocdoc.atlassian.net/browse/SRE-2922) | TBD |
| Permissions for Lambda restart for developers | TBD | TBD |
| Force argument for pants/teamcity during outages | TBD | TBD |
| Tune autogenerated incident to prevent duplicate SEV1s | TBD | TBD |
| Automate Lambda restart after permission issues | TBD | TBD |
| Don't make manual SCP changes during org-wide meetings | Process | N/A |

---

### 5. Feb 13, 2026 — SEV2: Messaging Service Failures

**Incident:** [OUT-6470](https://zocdoc.atlassian.net/browse/OUT-6470)  
**Postmortem:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/INFRA/pages/2668953777)

#### Related Triage Tickets (9)
| Ticket | Issue |
|--------|-------|
| TRIAG-22627 | Multiple Notification Emails for Same Appointment |
| TRIAG-22618 | Multiple Notification Emails for Single Appointment |
| TRIAG-22617 | Appt notification emails (multiple received) |
| TRIAG-22616 | Multiple Zocdoc Notifications (12 texts for one appt) |
| TRIAG-22632 | Provider did not receive appointment confirmation emails |
| TRIAG-22628 | Not Receiving Email Notifications |
| TRIAG-22622 | Practice not receiving email appointment notifications |
| TRIAG-22621 | PR didn't receive appointment notification |
| TRIAG-22613 | Automatic appointment cancellation |

#### Root Cause
**SQL Server chose an incorrect execution plan** due to:
- Inaccurate data statistics
- Parameter sniffing
- Changes in database environment

The query optimizer used wrong estimates, causing suboptimal performance on a critical query in the messaging event processor Lambda.

**True fix deployed Feb 20:** Forced the problematic query to use the appropriate index.

#### Timeline
| Time | Event |
|------|-------|
| 7:30 AM | Issue begins |
| 7:59 AM | PagerDuty alerts |
| 10:29 AM | Duplicate emails reported |
| 11:19 AM | Kinesis stream disabled to stop duplicate spam |
| 4:30 PM | Incident mitigated |
| **Feb 20** | Root cause fixed (query index) |

#### Impact
- **Duplicate messages:** Up to 5x per event to patients/providers
- **Delayed messages:** Unknown count
- **Lost messages:** Unknown count
- **TTR:** 9 hours 25 minutes

#### Action Items (from postmortem)

| Action | Status |
|--------|--------|
| Address duplicate messaging handling | TBD |
| Add idempotency tracking for sent messages | TBD |
| Circuit breaker for Lambda failures/retries | TBD |
| Handle failed Kinesis records to prevent message loss | TBD |
| Additional anomaly detection alerts | TBD |
| DBRE: Database maintenance on statistics | TBD |
| Instrument missing Honeycomb spans for Braze calls | TBD |

---

### 6. Mar 16, 2026 — SEV1: Provider Login (FGA Misconfiguration)

**Incident:** [OUT-6517](https://zocdoc.atlassian.net/browse/OUT-6517)  
**Postmortem:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/INFRA/pages/2784657434)

#### Related Triage Tickets (3)
| Ticket | Issue |
|--------|-------|
| TRIAG-22914 | Provider Login Error Loop |
| TRIAG-22913 | Error message when logging into Zocdoc |
| TRIAG-22190 | Unable to verify phone number (2FA) |

#### Root Cause
Chain of 3 PRs in `client-side-webapp-host`:

1. **PR #206:** Set up FGA SDK but repo was missing spec config provider
2. **PR #213:** Enabled audit mode — appeared to pass but silently missed misconfiguration (audit exceptions weren't surfaced)
3. **PR #226:** Moved to production usage — exposed broken configuration

The navbar component depended on FGA, so **every provider-facing page failed to load**.

#### Timeline
- **9:36 AM:** Auth synthetic fires
- **9:48 AM:** Incident created
- **9:55 AM:** Carlos Deleon re-runs previous good build
- **10:02 AM:** Mitigated
- **10:24 AM:** Resolved
- **TTM:** 14 minutes | **TTR:** 36 minutes

#### Action Items (from postmortem)

| Action | Ticket | Status |
|--------|--------|--------|
| Fix CSWH FGA Connection + audit mode metrics | [PTERODACTL-1749](https://zocdoc.atlassian.net/browse/PTERODACTL-1749) | **Closed** |
| Investigate Sentry gap (CloudWatch errors not in Sentry) | TBD | TBD |
| Verify spec config provider across older repos | All teams | TBD |

---

### 7. Mar 19, 2026 — SEV3: Monolith Sync Delayed

**Incident:** [OUT-6521](https://zocdoc.atlassian.net/browse/OUT-6521)  
**Postmortem:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/INFRA/pages/2810052633)

#### Related Triage Tickets (3)
| Ticket | Issue |
|--------|-------|
| TRIAG-22961 | Pulse update issue |
| TRIAG-22957 | Issue with Pulse and QPQ Tool |
| PE-4967 | Provider not appearing in Advanced Location Mapping Tool |

#### Root Cause
**Bulk activation of ~3,100 providers** (from a large practice with ~2,500 providers) in batches of 50 created unexpected load on the monolith sync Lambda.

Contributing factors:
1. **PR #1630** added `GetLiveByPracticeAsync` call during activation → increased processing time (6-8 seconds per call for this practice)
2. **SQS visibility timeout (5 min) = Lambda timeout (5 min)** → messages became visible again before Lambda completed → duplicate processing
3. **Lambda concurrency of 5** insufficient for 3,000+ message backlog

#### Timeline
- **7:00 AM:** PDO submits 3,000+ activation requests
- **8:33 AM:** SEV3 declared
- **9:54 AM:** Concurrency increased to 15
- **10:10 AM:** SQS queue cleared
- **10:29 AM:** Mitigated
- **TTR:** 385 minutes (6.4 hours)

#### Fixes Applied

| Fix | PR | Status |
|-----|-----|--------|
| Cache live locations per practice | [PR #1866](https://github.com/Zocdoc/provider-profile/pull/1866) | Merged |
| Increase SQS visibility timeout to 7 min | [PR #1861](https://github.com/Zocdoc/provider-profile/pull/1861) | Merged |
| Handle already-synced provider exception | [PR #1858](https://github.com/Zocdoc/provider-profile/pull/1858) | Merged |

#### Action Items (from postmortem)

| Action | Ticket | Status | Owner |
|--------|--------|--------|-------|
| Rate limiting for BulkActivateTool | TBD | TBD | Provider Roster Management |
| Fix recursive expired-task loop in TaskDispatch | [SYNC-11489](https://zocdoc.atlassian.net/browse/SYNC-11489) | **To Do** | Interop |
| PDO team process guidelines for large batch operations | TBD | TBD | PDO + Provider Roster |

---

## Consolidated Open Action Items

### High Priority (Prevent Recurrence)

| Area | Action | Owner | Ticket |
|------|--------|-------|--------|
| **Insurance** | Deprecate monolith IDs in GQL resolvers | Platform | PINATA-6253 |
| **Insurance** | Add FEMv2 metrics for appointment details (iOS, Android, Web) | Mobile/Web | PINATA-6236, 6237, 6159 |
| **Messaging** | Add idempotency tracking for sent messages | Messaging | TBD |
| **Messaging** | Circuit breaker for Lambda failures | Messaging | TBD |
| **Sync** | Rate limiting for bulk operations | Provider Roster | TBD |
| **Sync** | Fix TaskDispatch expired-task loop | Interop | SYNC-11489 |
| **SRE** | Create staging OU for SCP testing | SRE | SRE-2922 |

### Medium Priority (Improve Detection)

| Area | Action | Owner |
|------|--------|-------|
| **Monitoring** | Monitors on cancellation spiking / realization rate dropping | Platform Analytics |
| **Monitoring** | Additional anomaly detection for messaging | Messaging |
| **Auth** | Investigate Sentry gap (CloudWatch errors not appearing) | SRE |
| **DBRE** | Database maintenance on statistics (prevent bad execution plans) | DBRE |

---

## Patterns & Recommendations

### Pattern 1: Cascading Failures from Bulk Operations
**Incidents:** Mar 19 Sync, Feb 13 Messaging

**Recommendation:** Implement rate limiting and circuit breakers for bulk operations. Add capacity planning for operations affecting >500 entities.

### Pattern 2: Configuration/Feature Flag Rollout Failures
**Incidents:** Jan 6 Insurance, Mar 16 Provider Login

**Recommendation:** 
- Ensure audit mode exceptions are visible in monitoring
- Match dev/test environments to production configuration
- Add automated regression tests before feature flag enablement

### Pattern 3: Database Performance Surprises
**Incidents:** Feb 13 Messaging

**Recommendation:** 
- Monitor query execution plans for critical paths
- Establish regular database statistics maintenance
- Add circuit breakers that trip on query duration spikes

### Pattern 4: Permission/Policy Changes
**Incidents:** Feb 12 SCP

**Recommendation:**
- Create staging environment for SCP/policy testing
- Require change management for organization-level changes
- Never make manual infrastructure changes during company meetings

---

## Files in This Analysis

- `README.md` - This summary report
- `incident-details/` - Full postmortem details for each incident
- `triage-tickets.md` - Complete list of analyzed triage tickets

---

## Related Analyses

### [Audit Request Analysis](audit-request-analysis/README.md)
**45 tickets** — Providers dispute account changes, CX requests audit logs

| Cluster | Count | Root Cause |
|---------|-------|------------|
| SPO Audits | 9 | Provider denies enabling SPO |
| VR Audits | 9 | VRs allegedly changed without authorization |
| Insurance Audits | 8 | Insurance settings disputes |
| Calendar Audits | 7 | OOO/availability change disputes |
| Spend Audits | 5 | Budget/spend setting disputes |
| Working Hours | 2 | Working hours change disputes |
| Google Settings | 2 | Google booking setting reverting |

**Key Finding:** 91% share meta-root-cause — CX lacks self-service audit logs

---

### [Propagation Delay Analysis](propagation-delay-analysis/README.md)
**8 tickets** — Data sync/propagation delays between systems

| Cluster | Count | Root Cause |
|---------|-------|------------|
| VR Propagation | 3 | VR updates not reflecting on patient side |
| Salesforce Sync | 2 | Pulse ↔ SF status mismatch |
| Availability Propagation | 1 | Marketplace activation issues |
| Profile Media | 1 | Headshot caching delays |
| Billing/Reports | 1 | Report loading failures |

**Key Finding:** All have `Updation-Delay-Required-Action` label
