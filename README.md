# Pterodactyl Team Test Coverage Analysis

Comprehensive test coverage analysis for the **Provider Account & User Setup (Pterodactyl)** team's repositories.

## Team Overview

| Attribute | Value |
|-----------|-------|
| **Team Name** | Provider Account & User Setup (Pterodactyl) |
| **GitHub Team** | @Zocdoc/user-permissions |
| **Email** | technology-provider-pterodactyl@zocdoc.com |
| **Jira Project** | PTERODACTL |

## Repositories Analyzed

| Repository | Description | Environment | Analysis |
|------------|-------------|-------------|----------|
| [practice-user-permissions](https://github.com/Zocdoc/practice-user-permissions) | Fine-grained authorization for practice users (PUP) | PR201 (PHI) | [Report](analysis/practice-user-permissions.md) |
| [practice-authorization-proxy](https://github.com/Zocdoc/practice-authorization-proxy) | Proxy for OKTA FGA requests | PR201 (PHI) | [Report](analysis/practice-authorization-proxy.md) |
| [provider-grouping](https://github.com/Zocdoc/provider-grouping) | Provider Organizations & Groups (POGS) | PR001 | [Report](analysis/provider-grouping.md) |
| [provider-join-service](https://github.com/Zocdoc/provider-join-service) | Provider self-signup flow | TBD | [Report](analysis/provider-join-service.md) |

## Services & Infrastructure

### Lambdas/Workers
- FGA Lambda
- Monolith Backfill Lambda
- Provider Group Membership Lambda
- DDB Stream Consumer Lambda
- Provider Profile Churn Lambda
- Provider Sibling Practice Lambda
- Tuple Audit Retry Lambda

### Dashboards
- [Practice User Permissions](https://zocdoc.datadoghq.com/dashboard/7mu-gds-gc2/practice-user-permissions)
- [Provider Grouping (POGS)](https://zocdoc.datadoghq.com/dashboard/6ht-4ex-qws/provider-grouping)

## Analysis Reports

Each repository has a dedicated analysis report containing:
- **Executive Summary** - Coverage percentage and key findings
- **Test Inventory** - Complete list of all tests and what they cover
- **Gap Analysis** - Missing test coverage
- **Obsolete Tests** - Tests that may no longer be needed
- **Recommendations** - Prioritized action items

## Quick Links

- [Consolidated Summary](analysis/SUMMARY.md) - Cross-repo findings and priorities
- [Gap Analysis](analysis/GAPS.md) - All missing tests across repos
- [Obsolete Tests](analysis/OBSOLETE.md) - Tests to consider removing

---

*Generated: 2026-04-09*
*Analysis performed by Claude Code*
