# Lambdas, Crons & Workers Inventory - Pterodactyl Team

## Ownership Clarification

**Confirmed Pterodactyl-owned repositories** (owner-email: technology-provider-pterodactyl@zocdoc.com):
1. practice-user-permissions
2. practice-authorization-proxy
3. provider-grouping

**NOT owned by Pterodactyl:**
- `provider-join-service` - Owned by provider-peacock-team (technology-providergrowth@zocdoc.com)

---

## provider-grouping

### Lambdas

| Lambda Name | Purpose | Has Tests? | Test Location |
|-------------|---------|------------|---------------|
| `provider-grouping-change-stream-forwarder` | DynamoDB stream handler - forwards changes to SNS | YES | `tests/LambdaTests/Lambdas/ChangeStreamLambdaTests.cs` |
| `provider-grouping-group-update` | Processes group updates from internal Kinesis stream | YES | `tests/LambdaTests/Lambdas/GroupUpdateLambdaTests.cs` |
| `provider-grouping-provider-change-processor` | Processes provider changes from Kinesis | YES | `tests/LambdaTests/Lambdas/ReferenceDataChangeLambdaTests.cs` |
| `provider-grouping-location-change-processor` | Processes location changes from Kinesis | YES | `tests/LambdaTests/Lambdas/ReferenceDataChangeLambdaTests.cs` |
| `provider-grouping-provloc-change-processor` | Processes provider-location mapping changes | YES | `tests/LambdaTests/Lambdas/ReferenceDataChangeLambdaTests.cs` |
| `provider-grouping-strategic-practice-change-processor` | Processes practice changes for strategics | YES | `tests/LambdaTests/Lambdas/StrategicLambdaTests.cs` |
| `provider-grouping-strategic-strategic-change-processor` | Processes strategic info changes | YES | `tests/LambdaTests/Lambdas/StrategicLambdaTests.cs` |
| `provider-grouping-strategic-strategicmapping-change-processor` | Processes strategic mapping changes | YES | `tests/LambdaTests/Lambdas/StrategicLambdaTests.cs` |
| `provider-grouping-monolith-sync` | Syncs org membership/metadata to monolith | **NO** | **MISSING** |

### Crons

| Cron Name | Schedule | Purpose | Has Tests? |
|-----------|----------|---------|------------|
| `provider-grouping-salesforce-cron` | Every 5 min | Syncs org data with Salesforce via Jitterbit | YES (partial) |

### Workers

| Worker Name | Purpose | Has Tests? |
|-------------|---------|------------|
| `provider-grouping-dynamic-grouping-auditing-worker` | Audits dynamic group membership | YES |

---

## practice-user-permissions

### Lambdas

| Lambda Name | Purpose | Has Tests? | Test Location |
|-------------|---------|------------|---------------|
| `{prefix}-ddb-stream-consumer-lambda` | Processes DynamoDB stream events, publishes to SNS | YES | `Lambda.UnitTests/` |
| `{prefix}-monolith-backfill-lambda` | Syncs user changes back to monolith | YES | `ActiveUserBackfillHandlerTests.cs`, `DeletedUserBackfillHandlerTests.cs` |
| `{prefix}-fga-lambda` | Writes tuple changes to OKTA FGA | YES | `FgaTupleCreatorTests.cs`, `FgaUpdateServiceTests.cs` |
| `{prefix}-org-membership-refresh-lambda` | Refreshes user versions when org memberships change | YES | `OrganizationMembershipProcessorTests.cs` |
| `{prefix}-org-hierarchy-role-fixes-lambda` | Adjusts roles when orgs move in hierarchy | YES | `OrganizationHierarchyRoleFixesTests.cs` |
| `{prefix}-scoped-org-changes-lambda` | Sets scopedOrganization for users | YES | `ScopedOrganizationChangeProcessorTests.cs` |
| `{prefix}-audit-logging-*` (4 instances) | Writes audit logs to Firehose | YES | `AuditLogGeneratorTests.cs` |
| `{prefix}-notify-user-role-changes-lambda` | Sends notifications on role changes | YES | `UserRoleChangeNotifierTests.cs` |
| `{prefix}-provider-group-membership-lambda` | Processes provider group events from POGS | YES | External subscription tests |
| `{prefix}-provider-sibling-practice-lambda` | Processes sibling practice events from POGS | YES | External subscription tests |
| `{prefix}-provider-profile-churn-lambda` | Processes practice churn events | YES | `ProviderProfile/SqsEventParserTests.cs` |
| `{prefix}-tuple-audit-retry-lambda` | Retries failed FGA tuple audits | YES | `TupleAuditFailureRetryServiceTests.cs` |

### Crons

| Cron Name | Schedule | Purpose | Has Tests? |
|-----------|----------|---------|------------|
| `practice-user-permissions-cron` | 4x daily (5, 11, 17, 23 UTC) | Backfills scoped org membership | YES |

### Workers

| Worker Name | Purpose | Has Tests? |
|-------------|---------|------------|
| `practice-user-permissions-worker` | Continuously audits FGA tuples | PARTIAL (integration only, no unit tests) |

---

## practice-authorization-proxy

**No lambdas, crons, or workers** - Pure HTTP proxy service to OKTA FGA.

---

## Summary

### Total Background Jobs

| Repository | Lambdas | Crons | Workers | Total |
|------------|---------|-------|---------|-------|
| provider-grouping | 9 | 1 | 1 | 11 |
| practice-user-permissions | 12 | 1 | 1 | 14 |
| practice-authorization-proxy | 0 | 0 | 0 | 0 |
| **Total** | **21** | **2** | **2** | **25** |

### Test Coverage Gaps

| Component | Repository | Issue | Priority |
|-----------|------------|-------|----------|
| `provider-grouping-monolith-sync` | provider-grouping | **NO TESTS** | P0 |
| `practice-user-permissions-worker` | practice-user-permissions | No unit tests (only integration) | P1 |

---

## Recommendations

### P0 - Critical

1. **Add tests for `provider-grouping-monolith-sync` lambda** - This lambda handles syncing organization membership/metadata changes to the monolith with zero test coverage.

### P1 - High

2. **Add unit tests for `practice-user-permissions-worker`** - The worker unit tests directory exists but is empty.

### P2 - Medium

3. **Add more comprehensive cron tests** - Salesforce sync cron has partial coverage.

---

*Generated: 2026-04-09*
