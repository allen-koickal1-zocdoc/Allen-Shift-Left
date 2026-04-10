# 20260106-[SEV1] Insurance Booking Failures

**Incident:** [OUT-6419](https://zocdoc.atlassian.net/browse/OUT-6419)  
**Postmortem:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/INFRA/pages/2541978219)  
**Commander:** Oliver Wright

## Timeline

| Milestone | Timestamp |
|-----------|-----------|
| Started | Jan 6, 2026 7:00 AM EST |
| Detected | Jan 6, 2026 7:07 AM EST |
| Mitigated | Jan 6, 2026 7:13 AM EST |
| Resolved | Jan 12, 2026 12:39 PM EST |
| **TTM** | 13 minutes |
| **TTR** | 6 days, 5 hours |

## Summary

From 12:00 to 12:13 UTC on January 6th, 227 bookings were lost due to a bug in checking insurance in-network status in the booking service for providers who don't accept OON bookings. From January 8 to January 12, we saw increased cancellations from patients for in-network bookings incorrectly displayed as out-of-network on the iOS upcoming appointment details screen.

## Root Cause

As part of the `Support Provider Insurance Mapping OOM` epic (PINATA-5715), code changes were made under feature flags using the legacy feature flag mechanism.

### Stage 1: Initial enabling (Jan 6, 7:00-7:13 AM)
- Feature flag `ShouldUseNonPhiGqlForProviderInsurance` enabled
- Query to fetch insurance information was sent incorrect parameters
- **Fix:** [PR #64010](https://github.com/Zocdoc/zocdoc_web/pull/64010)

### Stage 2: Second enabling (Jan 8, 4:00 AM - Jan 12, 12:40 PM)
- Feature flag re-enabled after Stage 1 fix
- Another case of incorrect parameters, but affecting iOS appointment display
- iOS app displayed in-network bookings as out-of-network
- Much harder to notice since it didn't affect booking rates directly
- **Fix:** [PR #64032](https://github.com/Zocdoc/zocdoc_web/pull/64032)

### Technical Factors
1. Monolith support for OOM feature flags not suitable for high-traffic path
2. Legacy FF do not support granular enablement
3. Monolith code differs in terminology from OOM code (Provider vs. Professional)
4. GQL accepts both cloud & monolith IDs — incorrect ID type was passed
5. iOS used a different field than web for showing insurance status

## Business Impact

### Stage 1
- **227 bookings lost**
- Estimated revenue: ~$8,853 (assuming 60% premium eligible, $65 avg booking fee)

### Stage 2
- **~2,300 bookings lost** (from patient cancellations)
- Estimated revenue: ~$88,335

### Total Revenue Impact: ~$97,200

## Detection

### Stage 1
- Datadog Monitor
- Post-FF enabled manual testing
- Monitoring of Datadog dashboards

### Stage 2
- Engineer found additional incorrect codepath during teardown
- Product Analytics flagged increased patient cancellations
- Data from Looker

## What Was Learned

1. Behavior was verified on web with assumption mobile apps would have same behavior — **incorrect**
2. iOS was using a different field than others for showing insurance status after booking
3. GQL accepting both cloud & monolith IDs creates risk — should generally only accept cloud IDs

## Action Items

### Immediate Actions

| Action | Ticket | Status |
|--------|--------|--------|
| Add GQL fake support for automated testing | [PINATA-5860](https://zocdoc.atlassian.net/browse/PINATA-5860) | TBD |
| iOS FEMv2 metrics for appointment details | [PINATA-6236](https://zocdoc.atlassian.net/browse/PINATA-6236) | TBD |
| Android FEMv2 metrics for appointment details | [PINATA-6237](https://zocdoc.atlassian.net/browse/PINATA-6237) | TBD |
| Web FEMv2 metrics for appointment details | [PINATA-6159](https://zocdoc.atlassian.net/browse/PINATA-6159) | TBD |

### Preventative Actions

| Action | Ticket | Status |
|--------|--------|--------|
| GQL resolver cleanup - deprecate monolith IDs | [PINATA-6253](https://zocdoc.atlassian.net/browse/PINATA-6253) | TBD |
| Monitors on cancellation spiking / realization dropping | TBD | TBD |
| Automated regression tests on bookings | [PINATA-6254](https://zocdoc.atlassian.net/browse/PINATA-6254) | TBD |
| Migrate appointment page API dependencies OOM | [PINATA-4029](https://zocdoc.atlassian.net/browse/PINATA-4029) | TBD |

## Related Triage Tickets

- TRIAG-22693, TRIAG-22479, TRIAG-22472, TRIAG-22467
- TRIAG-22259, TRIAG-22256, TRIAG-22544, TRIAG-22538
