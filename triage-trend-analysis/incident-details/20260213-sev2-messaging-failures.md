# 20260213-[SEV2] Increase in Messaging Failures

**Incident:** [OUT-6470](https://zocdoc.atlassian.net/browse/OUT-6470)  
**Postmortem:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/INFRA/pages/2668953777)  
**Commander:** Laureen Lubin

## Timeline

| Milestone | Timestamp |
|-----------|-----------|
| Started | Feb 13, 2026 7:30 AM EST |
| Detected | Feb 13, 2026 7:59 AM EST |
| Mitigated | Feb 13, 2026 4:30 PM EST |
| Resolved | Feb 13, 2026 4:55 PM EST |
| **TTM** | 9 hours |
| **TTR** | 9 hours 25 minutes |
| **True Fix** | Feb 20, 2026 |

## Summary

Timeouts and lambda errors in the messaging service events processor caused:
- **Duplicate messages** (up to 5x per event) sent to patients and providers
- **Delayed messages**
- **Unknown number of messages permanently lost**

Initially declared SEV3, escalated to SEV2 when duplicate messaging was discovered.

## Root Cause

**SQL Server chose an incorrect execution plan** due to:
- Inaccurate data statistics
- Parameter sniffing
- Changes in the database environment

The query optimizer relied on wrong estimates, leading to suboptimal performance on a critical query in the messaging event processor.

**True fix deployed February 20th:** Forced the problematic query to use the appropriate index, eliminating timeout errors.

## Detailed Timeline

| Time | Event |
|------|-------|
| 7:30 AM | Issue begins |
| 7:59 AM | PagerDuty alerts detected |
| 8:46 AM | Incident created, SEV3 declared |
| 9:35 AM | Elevated CPU on PrimeDB observed |
| 10:29 AM | Duplicate emails reported by internal user |
| 11:02 AM | Request to disable Lambda event source mapping |
| 11:19 AM | Kinesis stream disabled for messaging-events-processor-lambda |
| 12:48 PM | Lambda trigger re-enabled |
| 1:02 PM | Timeouts resumed, trigger disabled again |
| 1:47 PM | Batch size reduced to 50 |
| 2:05 PM | New batch size deployed |
| 2:29 PM | Lambda concurrency increased to 5 |
| 3:42 PM | Severity upgraded to SEV2 |
| 4:30 PM | Trigger re-enabled, incident mitigated |
| 4:55 PM | Incident resolved, DLQ redriven |

## Recovery Attempts

| Action | Result |
|--------|--------|
| Batch size 1000 → 400 | Did not resolve |
| Batch size 400 → 50 | Achieved stability |
| Batch calls to monolith | Did not fix but good practice |
| Reduced Lambda concurrency to 1 | Helped stabilize |
| Stopped processing temporarily | Should have done earlier; would have prevented duplicates |
| Limit re-entry on CRM canvases | Prevented additional spam |
| Index fragmentation rebuild | Did not work |
| **Force query to use correct index** | **Fixed the issue** (deployed Feb 20) |

## Business Impact

- **Revenue Impact:** $0 (no booking impact)
- **Human Impact:** HIGH
  - Engineers from Messaging Platform, Intake, SRE, and DBRE engaged 8:00am to 5:30pm
  - Three engineers continued investigation over the following week
  - CRM engaged to update canvases and communicate with affected users
  - Product Analytics assessed business impact

### Customer Impact
- Patients and providers received **duplicate messages** (up to 5x per event)
- Some messages were **delayed**
- **Unknown number of messages permanently lost**

## Key Lessons

1. **Lambda-level errors lead to duplicate messaging** — SRE can disable ESM to stop this
2. **SQL execution plans can suddenly become non-performant** — query duration and execution plans should be monitored closely with DBRE
3. **Should have halted message processing earlier** once duplicates were discovered
4. DBRE investigation was deprioritized too early (showed no blocking initially)

## Action Items

### Immediate Actions

| Action | Status |
|--------|--------|
| Address duplicate messaging handling | TBD |
| Separate out entities for processing | TBD |

### Preventative Actions

| Action | Status |
|--------|--------|
| Add idempotency tracking for sent messages | TBD |
| Circuit breaker for Lambda failures/retries | TBD |
| Process manager for pre-timeout handling | TBD |
| Handle failed Kinesis records to prevent message loss | TBD |
| Additional anomaly detection alerts | TBD |
| DBRE: Database maintenance on statistics | TBD |
| Instrument missing Honeycomb spans for Braze calls | TBD |
| Fix message opt-out API issues | TBD |

## Related Triage Tickets

- TRIAG-22632: Provider did not receive appointment confirmation emails
- TRIAG-22628: Not Receiving Email Notifications
- TRIAG-22627: Multiple Notification Emails for Same Appointment
- TRIAG-22622: Practice not receiving email appointment notifications
- TRIAG-22621: PR didn't receive appointment notification
- TRIAG-22618: Multiple Notification Emails for Single Appointment
- TRIAG-22617: Appt notification emails (multiple received)
- TRIAG-22616: Multiple Zocdoc Notifications (12 texts for one appt)
- TRIAG-22613: Automatic appointment cancellation
