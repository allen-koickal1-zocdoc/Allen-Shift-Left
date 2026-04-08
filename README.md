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

### Lambdas (21 total)

**practice-user-permissions (12 lambdas):**
- DDB Stream Consumer Lambda
- Monolith Backfill Lambda
- FGA Lambda
- Org Membership Refresh Lambda
- Org Hierarchy Role Fixes Lambda
- Scoped Org Changes Lambda
- Audit Logging Lambdas (4 instances)
- User Role Change Notification Lambda
- Provider Group Membership Lambda
- Provider Sibling Practice Lambda
- Provider Profile Churn Lambda
- Tuple Audit Retry Lambda

**provider-grouping (9 lambdas):**
- Change Stream Forwarder Lambda
- Group Update Lambda
- Provider/Location/ProvLoc Change Processors (3)
- Strategic Practice/Strategic/StrategicMapping Processors (3)
- Monolith Sync Lambda (**NO TESTS**)

### Crons (2 total)
- `practice-user-permissions-cron` - Scoped org backfill (4x daily)
- `provider-grouping-salesforce-cron` - Salesforce sync (every 5 min)

### Workers (2 total)
- `practice-user-permissions-worker` - FGA tuple auditing
- `provider-grouping-dynamic-grouping-auditing-worker` - Dynamic group auditing

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

## Cypress E2E Tests

~70+ E2E tests for Pterodactyl features. See [full report](analysis/cypress-e2e-tests.md).

| Test Suite | Tests | File |
|------------|-------|------|
| User Management | 9 | `cypress/e2e/rbac/user-management-smoke.spec.js` |
| RBAC | 10 | `cypress/e2e/rbac/rbac-smoke.spec.js` |
| Practice Management | 26 | `cypress/e2e/rbac/practicemgmt-smoke.spec.js` |
| Providers Page | 9 | `cypress/e2e/provider/provider-providerspage-regression.spec.js` |

## Quick Links

- **[MASTER INVENTORY](analysis/MASTER-INVENTORY.md) - Complete count of ALL tests**
- [Consolidated Summary](analysis/SUMMARY.md) - Cross-repo findings and priorities
- [Gap Analysis](analysis/GAPS.md) - All missing tests across repos
- [Obsolete Tests](analysis/OBSOLETE.md) - Tests to consider removing
- [Test Inventory](analysis/TEST-INVENTORY.md) - Detailed list of every test
- [Lambdas/Crons/Workers](analysis/lambdas-crons-workers.md) - Background jobs inventory
- [Cypress E2E Tests](analysis/cypress-e2e-tests.md) - End-to-end test coverage
- [Frontend Unit Tests](analysis/frontend-tests.md) - **CRITICAL: Zero tests exist**
- [Selenium Tests](analysis/selenium-tests.md) - Monolith Selenium tests

---

*Generated: 2026-04-09*
*Analysis performed by Claude Code*
