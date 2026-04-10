# Batch 3: Mixed Issues Analysis

**Tickets Analyzed:** 13  
**Report Generated:** April 10, 2026

---

## Overview

This batch contains 13 tickets with **mixed root causes** — unlike previous batches which had single dominant patterns.

---

## Summary by Category

| Category | Count | % | Tickets |
|----------|-------|---|---------|
| IP/Security Blocking | 5 | 38% | TRIAG-22871, 22902, 22951, 22863, 22333 |
| Actual Functional Bugs | 4 | 31% | TRIAG-22711, 22550, 22609, 22213 |
| Data Propagation | 2 | 15% | TRIAG-22381, 22230 |
| Working as Intended | 1 | 8% | TRIAG-22828 |
| Misfiled (Hardware) | 1 | 8% | TRIAG-22637 |

---

## Category 1: IP/Security Blocking (5 tickets)

**Root Cause:** Security mechanisms (IP blocking, rate limiting) working as designed — not software bugs.

| Ticket | Summary | Product Area | Labels | Resolution |
|--------|---------|--------------|--------|------------|
| TRIAG-22871 | Access Blocked/IP address blocked | Provider-Auth, SRE | `Redirected`, `issue-type-functional` | Won't Fix |
| TRIAG-22902 | Provider Can't Access Account | Provider-Auth | `Redirected`, `issue-type-security` | Done |
| TRIAG-22951 | Access temporarily restricted | SRE | `Redirected`, `issue-type-usability` | Closed |
| TRIAG-22863 | Login Access Error | SRE | `Redirected`, `issue-type-functional` | Won't Do |
| TRIAG-22333 | Users unable to login | SRE | `Redirected`, `issue-type-security` | Done |

**Recommendation:** Create CX playbook for IP blocking — these shouldn't need engineering involvement.

---

## Category 2: Actual Functional Bugs (4 tickets)

| Ticket | Summary | Product Area | Labels | Resolution |
|--------|---------|--------------|--------|------------|
| TRIAG-22711 | Time zone issue across multiple locations | Integrated-Availability | `Redirected`, `issue-type-functional` | Closed |
| TRIAG-22550 | Availability not showing on Marketplace | Practice-SKU-Management | `Redirected`, `issue-type-functional` | Done |
| TRIAG-22609 | Error while setting disposition | Salesforce | `Redirected` | Closed |
| TRIAG-22213 | Review Count Discrepancy | Reviews(Provider) | `Redirected`, `issue-type-functional` | Done |

**Details:**
- **TRIAG-22711:** Timezone/DST handling bug for multi-location providers (MST/PST)
- **TRIAG-22550:** Marketplace availability not propagating
- **TRIAG-22609:** Salesforce disposition error
- **TRIAG-22213:** Review count mismatch (8 total vs 10 in 5-star filter)

---

## Category 3: Data Propagation (2 tickets)

| Ticket | Summary | Product Area | Labels | Resolution |
|--------|---------|--------------|--------|------------|
| TRIAG-22381 | Request for engineering support | Pulse | `Redirected`, `issue-type-data` | Done |
| TRIAG-22230 | Clone-Patient availability/calendar desync | Calendar-Integration | `Original-Bug-Contained-PHI`, `Redirected` | Closed |

**Details:**
- **TRIAG-22381:** Legacy Interface mappings and deleted entities re-propagating after refresh
- **TRIAG-22230:** Calendar integration showing availability internally but not patient-facing

---

## Category 4: Working as Intended (1 ticket)

| Ticket | Summary | Product Area | Labels | Resolution |
|--------|---------|--------------|--------|------------|
| TRIAG-22828 | Location Deletion Irvine Boulevard | Location-Management | `Redirected`, `Working-as-Intended` | Working as Intended |

---

## Category 5: Misfiled (1 ticket)

| Ticket | Summary | Product Area | Labels | Resolution |
|--------|---------|--------------|--------|------------|
| TRIAG-22637 | Desk Dock Issues | Third-Party-Issue | `Redirected` | Closed |

**Note:** Internal employee hardware issue (desk dock). Should not have been in TRIAG queue.

---

## Key Insights

1. **38% are IP/Security blocks** — Not bugs, security working as designed. CX playbook needed.
2. **Mixed patterns** — No single dominant root cause like previous batches.
3. **Timezone bugs persist** — Multi-location providers and DST transitions are problematic.
4. **Misfiled tickets** — Better triage routing could catch hardware issues earlier.
