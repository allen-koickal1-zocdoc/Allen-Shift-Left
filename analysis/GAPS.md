# Test Coverage Gaps - All Repositories

## Critical Gaps (No Tests)

### practice-authorization-proxy

| Component | File | Description |
|-----------|------|-------------|
| AuthorizationImpl | `src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs` | 184-line controller with zero unit tests |
| BatchPracticeAuthorizationException | `src/PracticeAuthorizationProxy/AuthorizationExceptions.cs` | Custom exception class untested |
| BatchOrganizationAuthorizationException | `src/PracticeAuthorizationProxy/AuthorizationExceptions.cs` | Custom exception class untested |
| SetupExtensions | `src/PracticeAuthorizationProxy/SetupExtensions.cs` | AWS service registration untested |
| FakeAuthorizationService | `src/PracticeAuthorizationProxy.Web.Fake/Services/` | Fake service behavior untested |

### practice-user-permissions

| Component | File | Description |
|-----------|------|-------------|
| PracticeBlockedService | `src/PracticeUserPermissions/Service/` | Core service - only persistence tests exist |
| AuditLoggingMetadataService | `src/PracticeUserPermissions/Service/` | No direct tests |
| BatchGetEntityDirectUsersCount endpoint | `UserRolesImpl` | No API tests visible |

### provider-grouping

| Component | File | Description |
|-----------|------|-------------|
| StrategicLambdaHandler | Lambda handler | Test exists but IGNORED - "Test Not Completed" |
| SalesforceApiCaller | `src/` | External API caller with no unit tests |
| ProviderReferenceApiCaller | `src/` | External API caller with no tests |
| ProviderReferenceDataService | `src/` | No direct tests |
| DynamicGroupingUpdateExecutor | `src/` | Core orchestration logic untested |
| GroupMembershipUpdater | `src/` | Only tested via integration |
| SalesforceDebuggingTempService | `src/` | Temp service with no tests |
| StrategicUpdater | `src/` | Only tested through worker tests |
| RequestValidator | `src/` | Input validation untested |
| IdValidator | `src/` | Input validation untested |
| CloudIdGenerator | `src/` | ID generation untested |
| EntityIdUtils | `src/` | Utility untested |
| ParallelUtils | `src/` | Utility untested |
| LambdaUtils | `src/` | Utility untested |
| KinesisEventParser | `src/` | Parser untested |
| DateTimeUtils | `src/` | Utility untested |
| CronTask | `src/` | Cron service untested |
| SalesforceSyncService | `src/` | Cron service untested |
| DynamicGroupingAuditingWorker | `src/` | Worker untested |
| GroupImpl (error paths) | `src/` | Unit tests missing |
| GroupRulesImpl | `src/` | Unit tests missing |
| TempDebugImpl | `src/` | Temp code without tests |
| MembershipChangeProcessor | `src/` | Only indirect tests |

### provider-join-service

| Component | File | Description |
|-----------|------|-------------|
| StepFunctionService | `src/SelfSignup.Infrastructure/Services/StepFunctionService/` | **Critical** - No tests, handles abandonment flow |
| CreatePracticeDtoFactory | `src/SelfSignup.Infrastructure/Services/PracticeAndProviderCreation/` | Core DTO creation untested |
| MonolithApi (base class) | `src/SelfSignup.Infrastructure/Services/Monolith/` | Abstract class partially covered |

---

## Missing Edge Cases

### All Repositories

| Category | Missing Tests |
|----------|---------------|
| Concurrent access | Race conditions in database operations |
| DynamoDB throttling | Service degradation scenarios |
| Network timeouts | External API call failures |
| Large batch operations | Boundary conditions (>100 items) |
| Null/empty input handling | Many services lack null checks |

### practice-authorization-proxy

| Endpoint | Missing Tests |
|----------|---------------|
| `GET /practice/{id}/is_authorized` | Empty permissions array |
| `GET /practice/{id}/is_authorized` | Invalid PermissionFilter value |
| `GET /practice/{id}/is_authorized` | Malformed practice_id format |
| `GET /organization/{id}/is_authorized` | Empty permissions array |
| `GET /organization/{id}/is_authorized` | Invalid PermissionFilter value |
| `PUT /practice/is_authorized~batchGet` | Empty practice_ids array |
| `PUT /practice/is_authorized~batchGet` | Empty practice_permissions array |
| `PUT /practice/is_authorized~batchGet` | Invalid permission string |
| `PUT /practice/is_authorized~batchGet` | FGA service 500 error |
| `PUT /organization/is_authorized~batchGet` | Empty organization_ids array |
| `PUT /organization/is_authorized~batchGet` | Empty organization_permissions array |
| `PUT /organization/is_authorized~batchGet` | Invalid permission string |
| `PUT /organization/is_authorized~batchGet` | FGA service 500 error |

### practice-user-permissions

| Area | Missing Tests |
|------|---------------|
| SSO user flows | Edge cases for samlp users |
| Optimistic locking | Conflict resolution beyond retry |
| FGA rate limiting | Rate limit handling |
| GenerateInvitation | Error case tests |
| GetCurrentUserRoles | Authentication edge cases |

### provider-grouping

| Area | Missing Tests |
|------|---------------|
| Salesforce API | Rate limiting scenarios |
| Kinesis/SQS | Malformed message handling |
| Organization locks | Concurrent access race conditions |
| Large batch processing | Performance limits |

### provider-join-service

| Area | Missing Tests |
|------|---------------|
| DdbRepository | `shouldIgnoreNullValues=false` |
| LeadSalesforceService | Duplicate lead handling, retry logic |
| InsuranceWizardImpl | Partial data saves, concurrent updates |
| AccountCreationService | Race conditions in email verification caching |
| StepFunctionService | Stop execution failure, start execution timeout |
| Error recovery | Retry after transient failures |
| Salesforce failures | More edge cases |

---

## Missing Integration Tests

| Repository | Missing Test |
|------------|--------------|
| practice-user-permissions | Full user role change notification flow |
| practice-user-permissions | Integration with actual provider-grouping service |
| practice-user-permissions | DLQ processing verification |
| provider-grouping | Cross-service integration tests |
| provider-join-service | Concurrent request handling |
| provider-join-service | Salesforce API failure scenarios |

---

## Missing API Tests

| Repository | Endpoint | Gap |
|------------|----------|-----|
| practice-user-permissions | BatchGetEntityDirectUsersCount | No API tests |
| practice-user-permissions | GenerateInvitation | Only minimal tests |
| practice-user-permissions | GetCurrentUserRoles | Minimal coverage |
| practice-authorization-proxy | Invalid input scenarios | Not tested at API level |
| practice-authorization-proxy | FGA service errors | Not tested at API level |

---

## Summary by Priority

### Must Fix (P0)

1. `StepFunctionService` - 0 tests, critical production component
2. `StrategicLambdaHandler` - IGNORED test in production Lambda
3. `AuthorizationImpl` - 0 unit tests for 184-line controller

### Should Fix (P1)

4. `BatchGetEntityDirectUsersCount` endpoint
5. `PracticeBlockedService` unit tests
6. `DynamicGroupingUpdateExecutor` unit tests
7. `CreatePracticeDtoFactory` tests

### Nice to Have (P2/P3)

8. Utility classes across all repos
9. Edge case coverage
10. Concurrent access tests

---

*Generated: 2026-04-09*
