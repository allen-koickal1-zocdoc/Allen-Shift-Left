# 20260319-[SEV3] Monolith Sync Delayed

**Incident:** [OUT-6521](https://zocdoc.atlassian.net/browse/OUT-6521)  
**Postmortem:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/INFRA/pages/2810052633)  
**Incident Commander:** Priyanka Ahirwar  
**Retrospective Lead:** Gaurav Pandey

## Timeline

| Milestone | Timestamp |
|-----------|-----------|
| Started | Mar 19, 2026 7:00 AM EST |
| Detected | Mar 19, 2026 ~7:31 AM EST |
| Mitigated | Mar 19, 2026 10:29 AM EST |
| Resolved | Mar 19, 2026 11:57 AM EST |
| **TTM** | 280 minutes |
| **TTR** | 385 minutes (6.4 hours) |

## Summary

Provider activations blocked, Pulse updates not reflecting, operations teams paused all Pulse operations. Downstream Document Services iterator age spiked due to 11.4M ProviderLocationMapping updates.

## Root Cause

### Primary Root Cause: Large Practice Updates
- 3,000+ provider activation requests submitted
- Most were from a **large practice with ~2,500 providers**
- Added unexpected load on the monolith sync lambda

### Secondary Root Cause: Visibility Timeout Mismatch (PR #1861)
- **SQS visibility timeout (5 min) = Lambda timeout (5 min)**
- When processing approached 5 minutes, messages became visible again before Lambda completed
- Caused duplicate processing

### Contributing Factor: PR #1630
- Added `GetLiveByPracticeAsync` call during provider activation
- This method fetches all providers of practice, then provider-location mappings, then locations
- For a practice with ~2,500 providers, this took 6-8 seconds **per call**
- With batch size of 30, Lambda took >5 minutes and timed out
- Same providers were reprocessed repeatedly

### Capacity Constraint
- Lambda concurrency was set to 5
- Insufficient to process 3,000+ message backlog in reasonable time

## Detailed Timeline

| Time (EST) | Event |
|------------|-------|
| ~7:00 AM | PDO team submits 3,000+ activation requests |
| ~7:31 AM | Priyanka Ahirwar notified in #provider-roster-management |
| ~8:33 AM | Incident channel created, SEV3 declared |
| ~8:35 AM | Lambda concurrency increased from 5 to 8 |
| ~9:37 AM | CDK deployment initiated for additional fixes |
| ~9:54 AM | Concurrency increased to 15 via AWS console (Carlos Deleon) |
| ~10:10 AM | SQS queue cleared |
| ~10:29 AM | Incident marked as mitigated |
| ~11:57 AM | Incident fully resolved |

## Business Impact

| Category | Impact |
|----------|--------|
| Revenue Impact | TBD |
| Human Impact | TBD |
| Affected Teams | PDO, Enterprise Support, QA, Provider Roster Management |
| Downstream Systems | Document Services Event Processor (11.4M events backlog) |

### Symptoms Reported (TRIAG-22957)
- Pending locations not reflecting in QPQ
- Providers/locations built through BOSS not reflecting in Pulse
- Education entries not getting auto-approved
- Bulk headshot tool not working
- Activations delayed — Pulse not updating after "Activate" clicked
- Deleted profiles not reflecting correctly

## Mitigation Steps

1. **Increased Lambda concurrency** from 5 → 8 → 15
2. **Reprocessed Dead Letter Queue (DLQ)**
3. **Three PRs deployed** addressing root causes

## Fixes Applied

| Fix | PR | Status |
|-----|-----|--------|
| Cache live locations per practice in monolith sync lambda | [PR #1866](https://github.com/Zocdoc/provider-profile/pull/1866) | Merged |
| Increase SQS visibility timeout from 5 to 7 min, Lambda timeout from 5 to 6 min | [PR #1861](https://github.com/Zocdoc/provider-profile/pull/1861) | Merged |
| Handle already synced provider exception from monolith (consider it success) | [PR #1858](https://github.com/Zocdoc/provider-profile/pull/1858) | Merged |
| Increase Lambda concurrency | [PR #1859](https://github.com/Zocdoc/provider-profile/pull/1859) | Merged and **Reverted** (can't risk monolith saturation) |

### Performance Improvement from PR #1866
- Before: 120-160 seconds per batch of 20 messages
- After: 6-8 seconds per batch
- **Improvement:** 15-20x faster

## Detection & Signals

- **How detected:** PDO team reported activations not working; Pager alerts for DLQ and failures
- **Early signals missed:** 2 days earlier had few related errors — created backlog ticket but not prioritized

## What Worked

- Manual concurrency increase via AWS console (faster than CDK deploy)

## What Didn't Work

- Initial concurrency increase to 8 was insufficient; needed to go to 15

## Action Items

### Immediate Actions (Completed)

| Action | PR/Ticket | Status |
|--------|-----------|--------|
| Cache live locations per practice | PR #1866 | Merged |
| Increase SQS visibility timeout to 7 min and lambda timeout to 6 min | PR #1861 | Merged |
| Increase Lambda concurrency | PR #1859 | Merged and Reverted |
| Failure handle in monolith sync | PR #1858 | Merged |

### Preventative Actions (To Be Prioritized)

| Action | Description | Owner | Ticket |
|--------|-------------|-------|--------|
| **Rate limiting for bulk operations** | Implement throttling/queuing for BulkActivateTool to prevent pipeline flooding | Provider Roster Management | TBD |
| **PDO team process guidelines** | Create runbook for submitting large batch operations: max batch size, scheduling off-peak, notification requirements | PDO + Provider Roster Management | TBD |
| **Fix recursive expired-task loop in TaskDispatch** | Circuit breaker for cascading failures | Interop | [SYNC-11489](https://zocdoc.atlassian.net/browse/SYNC-11489) |

## Key Lessons

1. **Large bulk operations need capacity planning** — 3,000+ activations from a single large practice overwhelmed the system
2. **SQS visibility timeout must exceed Lambda timeout** — otherwise messages get reprocessed while still being worked on
3. **Caching is critical for N+1 query patterns** — calling `GetLiveByPracticeAsync` per message in a batch caused exponential slowdown
4. **Lambda concurrency limits need headroom** — 5 was insufficient for unexpected spikes

## Related Triage Tickets

- TRIAG-22961: Pulse update issue
- TRIAG-22957: Issue with Pulse and QPQ Tool
- PE-4967: Provider not appearing in Advanced Location Mapping Tool

## Key Participants

| Role | Person |
|------|--------|
| Incident Commander | Priyanka Ahirwar |
| Retrospective Lead | Gaurav Pandey |
| On-call | Eftal Sogukoglu |
| Key Contributors | Anand Desai, Carlos Deleon, James Collins, Avinash Patwari, Aayush Tripathi |
