# ZIP - Misbehavior Lock Revamp Analysis

**Epic:** [AUTH-3025](https://zocdoc.atlassian.net/browse/AUTH-3025)  
**Tech Spec:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/TECH/pages/2470379521/ZIP+-+Misbehavior+lock+revamp)  
**Author:** Ben Lee  
**Analysis Date:** 2026-04-10

## Overview

Analysis of the ZIP Misbehavior Lock Revamp initiative, which proposes:
- Separating login blocks from booking blocks
- Granting amnesty to ~8K previously locked users
- Building Retool tooling for T&S manual management
- Eventually implementing auto-lock logic based on collected data

## Key Decision

| Outcome | Count |
|---------|-------|
| Users remaining booking-blocked | ~12K (from CISTERN list) |
| Users granted amnesty | ~8K |
| Login blocks | Reserved for compromised accounts only |

## Documents

| File | Description |
|------|-------------|
| [PRD-GAP-ANALYSIS.md](PRD-GAP-ANALYSIS.md) | Comprehensive gap analysis with stakeholder questions |
| [CURRENT-TEST-COVERAGE.md](CURRENT-TEST-COVERAGE.md) | Current E2E test coverage and gaps |

## Key Findings

### Spec Gaps
- No microservice API contract defined
- No data model schema
- No success metrics defined
- No appeal process for contested blocks
- HIPAA concerns around "drug seeking" as block reason

### Test Gaps
- No T&S misbehavior block tests
- No login-allowed-but-booking-blocked tests
- No phone number block tests
- No test accounts for blocked states

## Critical Questions

1. What's the API contract for the new locking microservice?
2. Where in the booking flow does the block surface?
3. Has legal reviewed the amnesty plan?
4. How does this interact with MFA work (AUTH-3195)?
5. What's the appeal process for contested blocks?

## Next Steps

1. Get API contract from engineering
2. Define success metrics with product
3. Provision test accounts for E2E automation
4. Coordinate with AUTH-3195 (MFA) on login block behavior
