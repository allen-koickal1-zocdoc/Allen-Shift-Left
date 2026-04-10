# 20260130-[SEV?] Web Appointment Pages Showing Wrong Insurance Network Status

**Incident:** [OUT-6452](https://zocdoc.atlassian.net/browse/OUT-6452)  
**Postmortem:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/INFRA/pages/2605285380)  
**Assignee:** Anand Sundaram

## Timeline

| Milestone | Timestamp |
|-----------|-----------|
| Started | Jan 29, 2026 3:51 PM EST |
| Detected | Jan 30, 2026 5:16 PM EST |
| Mitigated | Jan 30, 2026 5:16 PM EST |
| Resolved | Jan 30, 2026 5:16 PM EST |
| **TTR** | 1 day, 1 hour, 25 minutes |

## Summary

Appointment details pages on web were incorrectly displaying insurance network status. This was the **3rd issue in 2 months around showing out-of-network errors at elevated rates in product**.

## Root Cause

A code change affecting `my-accounts-web-app` triggered the visible bug, but there was an **underlying issue since October 28, 2025** when the `apax_past_appointments_with_off_platform` feature flag was turned on to 100%.

### Technical Factors
1. **Monolith dependency** — complex reconciliation logic between monolith and GraphQL data
2. **Complex legacy code** — GQL and monolith data interactions
3. **Poor test coverage** — no automated tests caught this on the affected code branch
4. **Poor observability** — no FEMv2 metrics on INN vs OON UI display until recently
5. **Inconsistent appointment times** — GQL and monolith returned inconsistent appointment times for a subset of users

## Business Impact

| Category | Impact |
|----------|--------|
| Revenue Impact | $24,000 (lost PEB revenue from cancellations) |
| Human Impact | ~$500 |

## Detection

**Method:** QA forwarded a bug report from an end user  
**Issue:** No automated signals detected this issue

## Relationship to Other Insurance Incidents

This was part of a pattern of insurance display issues:

| Incident | Date | Platform | Root Cause |
|----------|------|----------|------------|
| [OUT-6419](https://zocdoc.atlassian.net/browse/OUT-6419) Stage 1 | Jan 6 | Booking service | Incorrect parameters to insurance query |
| [OUT-6419](https://zocdoc.atlassian.net/browse/OUT-6419) Stage 2 | Jan 8-12 | iOS | Different field used for insurance status |
| **OUT-6452** | Jan 29-30 | **Web** | Monolith/GQL reconciliation + legacy FF |

### Systemic Issues (Shared Across All 3)
1. Complex reconciliation logic between monolith and GraphQL
2. Lack of automated tests on insurance network status display
3. Lack of FEMv2 metrics on INN vs OON UI display
4. Poor observability on patient cancellations by platform/reason
5. Migration of insurance provider mappings OOM creates risk due to terminology differences (Provider vs. Professional) and ID format differences (cloud vs. monolith)

## Action Items

### Immediate Actions

| Action | Ticket | Owner |
|--------|--------|-------|
| Add metrics and alerts on INN vs OON display across patient site | [PINATA-6337](https://zocdoc.atlassian.net/browse/PINATA-6337) | Booking |
| Related work | [PINATA-6323](https://zocdoc.atlassian.net/browse/PINATA-6323) | Booking |
| Add assertions on insurance network status to appointment details smoke/production tests | TBD | Insurance |

### Preventative Actions

| Action | Ticket | Timeline | Owner |
|--------|--------|----------|-------|
| Move page's data fully OOM | [PINATA-5990](https://zocdoc.atlassian.net/browse/PINATA-5990) | April 2026 | Booking |
| Look into creating an insurance network status backend service | TBD | TBD | Insurance |

## Related Triage Tickets

These tickets from the analysis period relate to the insurance display issues across OUT-6419 and OUT-6452:

| Ticket | Date | Likely Source |
|--------|------|---------------|
| TRIAG-22693 | Feb 21 | OUT-6452 cascade |
| TRIAG-22479 | Feb 2 | OUT-6452 |
| TRIAG-22472 | Jan 30 | OUT-6452 |
| TRIAG-22467 | Jan 30 | OUT-6452 |
| TRIAG-22259 | Jan 12 | OUT-6419 Stage 2 |
| TRIAG-22256 | Jan 12 | OUT-6419 Stage 2 |

## Key Lesson

> "This was the 3rd issue in 2 months around showing out-of-network errors at elevated rates in product"

The insurance network status display is a high-risk area due to:
1. Multiple data sources (monolith, GQL, various APIs)
2. Multiple platforms (iOS, Android, Web)
3. Multiple entry points (booking flow, appointment details, search)
4. Migration in progress (OOM work)

**Recommendation:** Implement centralized insurance network status backend service to eliminate reconciliation complexity.
