# Test Coverage Analysis: practice-user-permissions

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Test Files** | 94 files |
| **Total Test Methods** | ~870 individual tests |
| **Unit Tests** | ~60% |
| **Integration Tests** | ~30% |
| **API Tests** | ~10% |
| **Overall Assessment** | Substantial coverage with well-organized test suites |

**Key Findings:** The codebase has good test coverage overall. Notable gaps exist in certain services and edge cases that should be addressed.

---

## Test Inventory by Category

### 1. Unit Tests (PracticeUserPermissions.UnitTests)

| File | Test Class | Tests | What It Tests |
|------|------------|-------|---------------|
| Services/UserRolesServiceTests.cs | UserRolesServiceTests | 17 | SetUserRolesGivenUserVersion, GetUserRoles, GetUserVersion, QueryUserRolesByEntity, filtering logic |
| Services/UserServiceTests.cs | UserServiceTests | 18 | GetUserPractices (various scenarios), GetOverlappingUsers |
| Services/Auth0UserServiceTests.cs | Auth0UserServiceTests | 3 | ShouldSkipAuth0Users for samlp prefixed users |
| Services/FgaModelServiceTests.cs | FgaModelServiceTests | 1 | GetLatestModelId |
| Services/UserInvitationServiceTests.cs | UserInvitationServiceTests | 9 | Create/Get/Invalidate invitations, filtering |
| Services/UserRolesHierarchyServiceTests.cs | UserRolesHierarchyServiceTests | 10 | GetUserRolesFromEntityHierarchy, BreakUserRolesFromOrganizationToPractices |
| Services/UserRolesServicePaginationTests.cs | UserRolesServicePaginationTests | 9 | QueryUserRolesByEntityPaginated, V2 user filtering, BatchGetUserVersions |
| Services/ScopedOrganizationMemberServiceTests.cs | ScopedOrganizationMemberServiceTests | 8 | Get/Set/Delete scoped org membership, version handling |
| Services/DlqRedriveServiceTests.cs | DlqRedriveServiceTests | 7 | StartRedriveAsync, error handling, configuration validation |
| Services/TupleAuditServiceTests.cs | TupleAuditServiceTests | 61 | FGA tuple auditing (large test class) |
| Services/OrganizationMembersServiceTests.cs | OrganizationMembersServiceTests | 27 | Org membership CRUD, hierarchy traversal |
| Services/UserEditAuthorizationServiceTests.cs | UserEditAuthorizationServiceTests | 7 | GetUserIdsAuthorizedForEditRoles, authorization checks |
| Services/UserRoleChangeNotificationServiceTests.cs | UserRoleChangeNotificationServiceTests | 4 | Role change notification queue |
| Services/PracticeChurnCalculatorTests.cs | PracticeChurnCalculatorTests | 11 | ArePracticesChurned logic with providers |
| Services/UltimateParentOrganizationServiceTests.cs | UltimateParentOrganizationServiceTests | 16 | Get/validate ultimate parent org |
| Services/NonceIdServiceTests.cs | NonceIdServiceTests | 4 | Nonce ID generation |
| Services/InternalMigrationServiceTests.cs | InternalMigrationServiceTests | 8 | Internal migration operations |
| Clients/FgaRelationConverterTests.cs | FgaRelationConverterTests | 59 | FGA relation type conversion |
| Clients/MessagingServiceClientTests.cs | MessagingServiceClientTests | 7 | Messaging service integration |
| Clients/PracticeUserRolesApiCallerTests.cs | PracticeUserRolesApiCallerTests | 11 | Practice user roles API calls |
| Clients/ProviderGroupingClientTests.cs | ProviderGroupingClientTests | 1 | Provider grouping client |
| Dtos/*.cs | Various DTO tests | ~30 | DTO serialization/mapping |
| Converters/*.cs | Various converter tests | ~5 | DateTime/JSON converters |
| Helpers/FgaTupleParsingHelperTests.cs | FgaTupleParsingHelperTests | 17 | FGA tuple parsing |

### 2. Lambda Unit Tests (PracticeUserPermissions.Lambda.UnitTests)

| File | Test Class | Tests | What It Tests |
|------|------------|-------|---------------|
| FgaUpdates/FgaTupleCreatorTests.cs | FgaTupleCreatorTests | 11 | FGA tuple creation |
| FgaUpdates/FgaUpdateServiceTests.cs | FgaUpdateServiceTests | 8 | FGA update processing |
| FgaUpdates/FgaUpdatesGeneratorTests.cs | FgaUpdatesGeneratorTests | 4 | FGA update generation |
| AuditLogging/AuditLogGeneratorTests.cs | AuditLogGeneratorTests | 7 | Audit log generation |
| AuditLogging/AuditLoggingServiceTests.cs | AuditLoggingServiceTests | 6 | Audit logging service |
| OrganizationMembershipUpdates/*.cs | Various | ~50 | Org membership event processing |
| OrganizationHierarchyRoleFixes/*.cs | Various | ~54 | Role fixes for hierarchy changes |
| ProviderMapping/*.cs | Various | 13 | Provider mapping events |
| ScopedOrganizationChanges/*.cs | Various | 15 | Scoped org change processing |
| UserRoleChangeNotificationLambda/*.cs | Various | 16 | User role change notifications |
| SqsEventParserTests.cs | SqsEventParserTests | 8 | SQS event parsing |
| SqsEventClassifierTests.cs | SqsEventClassifierTests | 6 | SQS event classification |

### 3. Integration Tests (PracticeUserPermissions.IntegrationTests)

| File | Test Class | Tests | What It Tests |
|------|------------|-------|---------------|
| Persistence/UserRolesPersistenceTests.cs | UserRolesPersistenceTests | 38 | User roles DynamoDB operations |
| Persistence/OrganizationMembersPersistenceTests.cs | OrganizationMembersPersistenceTests | 22 | Org members DynamoDB ops |
| Persistence/ScopedOrganizationMemberPersistenceTests.cs | ScopedOrganizationMemberPersistenceTests | 15 | Scoped org DynamoDB ops |
| Persistence/UserInvitationPersistenceTests.cs | UserInvitationPersistenceTests | 12 | User invitation DynamoDB ops |
| Persistence/PracticeBlockedPersistenceTests.cs | PracticeBlockedPersistenceTests | 10 | Practice blocked DynamoDB ops |
| Persistence/PracticeMemberPersistenceTests.cs | PracticeMemberPersistenceTests | 10 | Practice member DynamoDB ops |
| Persistence/LockPersistenceTests.cs | LockPersistenceTests | 6 | Lock mechanism DynamoDB ops |
| Persistence/ContinuationTokenPersistenceTests.cs | ContinuationTokenPersistenceTests | 6 | Continuation tokens |

### 4. Lambda Integration Tests (PracticeUserPermissions.Lambda.IntegrationTests)

| File | Test Class | Tests | What It Tests |
|------|------------|-------|---------------|
| FgaLambdaTests.cs | FgaLambdaTests | 4 | FGA lambda with real SQS/FGA |
| StreamConsumerLambdaTests.cs | StreamConsumerLambdaTests | 20+ | DDB stream to SQS |
| MonolithBackfillLambdaTests.cs | MonolithBackfillLambdaTests | Multiple | Monolith backfill |
| Various SQS event tests | Multiple | Multiple | Event processing pipelines |

### 5. Web API Tests (PracticeUserPermissions.Web.ApiTests)

| File | Test Class | Tests | What It Tests |
|------|------------|-------|---------------|
| UserRolesApiTests.cs | UserRolesApiTests | 123 | SetUserRoles, GetEntityUsersRoles, etc. |
| UserApiTests.cs | UserApiTests | 19 | AuthorizeEditUserData, AuthorizeViewUserData |
| InternalApiTests.cs | InternalApiTests | 33 | Internal admin endpoints |
| MplPracticesApiTests.cs | MplPracticesApiTests | 11 | SetMplPractices |
| PracticeChurnApiTests.cs | PracticeChurnApiTests | 8 | BackfillPracticeChurn |
| PreviewAccessChangesApiTests.cs | PreviewAccessChangesApiTests | 8 | Preview access changes |
| FgaModelApiTest.cs | FgaModelApiTest | 2 | FGA model operations |
| AuthorizationRequirementApiTests.cs | AuthorizationRequirementApiTests | 8 | Authorization requirements |

### 6. Web Unit Tests (PracticeUserPermissions.Web.UnitTests)

| File | Test Class | Tests | What It Tests |
|------|------------|-------|---------------|
| UserRolesValidatorTests.cs | UserRolesValidatorTests | 24 | Request validation rules |
| AuthorizationCheckerTests.cs | AuthorizationCheckerTests | 1 | Batch authorization checks |
| AuthorizationUnderAuditTests.cs | AuthorizationUnderAuditTests | 6 | Authorization under audit |
| ScopeValidationServiceTests.cs | ScopeValidationServiceTests | 3 | Scope validation |
| PreviewUserPermissionChangesImplTests.cs | PreviewUserPermissionChangesImplTests | 4 | Preview permission changes |
| Helpers/Access/*.cs | Access helper tests | 18 | GainAccessHelper, LoseAccessHelper, PreviewAccessOrchestrator |

---

## Gap Analysis

### 1. Services Without Direct Unit Tests

| Service | Location | Current Coverage | Recommendation |
|---------|----------|-----------------|----------------|
| **PracticeBlockedService** | src/PracticeUserPermissions/Service/ | Only persistence integration tests | Add unit tests for MarkPracticeAsBlocked, ArePracticesBlocked |
| **AuditLoggingMetadataService** | src/PracticeUserPermissions/Service/ | No direct tests | Add unit tests for BuildAuditLoggingMetadata |
| **ScopeValidationService** | src/PracticeUserPermissions.Web/ | Only 3 tests | Expand coverage for edge cases |

### 2. Missing Edge Case Coverage

| Area | Gap Description | Priority |
|------|-----------------|----------|
| **Concurrent access** | Limited testing for optimistic locking conflicts beyond retry | Medium |
| **Error handling** | DynamoDB throttling scenarios not tested | Low |
| **Boundary conditions** | Large batch operations (>100 items) | Medium |
| **SSO user flows** | Additional edge cases for samlp users | High |
| **Rate limiting** | FGA rate limit handling | Medium |

### 3. Missing Integration Tests

| Area | Gap Description | Priority |
|------|-----------------|----------|
| **End-to-end flows** | Full user role change notification flow | Medium |
| **Cross-service** | Integration with actual provider-grouping service | Low |
| **Failure scenarios** | DLQ processing verification | Medium |

### 4. API Endpoints Without Full Coverage

| Endpoint | Implementation | Tests | Gap |
|----------|---------------|-------|-----|
| GenerateInvitation | UserRolesImpl | Minimal | Need error case tests |
| BatchGetEntityDirectUsersCount | UserRolesImpl | None visible | Add API tests |
| GetCurrentUserRoles | UserRolesImpl | Minimal | Need authentication edge cases |

---

## Potentially Obsolete Tests

| File/Test | Reason | Recommendation |
|-----------|--------|----------------|
| **FakeSqsEvents test fixtures** | Contains hardcoded malformed event samples | Review if still needed or update |
| **AuthorizationRequirementTestController tests** | Test controller for authorization testing | Verify if this controller is still active |
| **Tests using `[Retry(n)]` attribute** | Integration tests with retries may mask flaky behavior | Investigate root cause of flakiness |

---

## Test Quality Observations

### Good Practices Observed

- Consistent use of `FluentAssertions` for readable assertions
- Good separation between unit and integration tests
- Use of `ServiceTestFixture<T>` base class for consistent mocking
- Parameterized tests with `[Values]` attribute for comprehensive coverage

### Areas for Improvement

- Some test files exceed 1000 lines (TupleAuditServiceTests) - consider splitting
- Test data helpers could be centralized (some duplication across test files)
- Missing negative test cases for several services

---

## Recommendations

### High Priority

1. Add unit tests for `PracticeBlockedService`
2. Expand SSO user validation test coverage
3. Add tests for `BatchGetEntityDirectUsersCount` endpoint

### Medium Priority

4. Add integration tests for DLQ processing flow
5. Test concurrent modification scenarios more thoroughly
6. Add boundary condition tests for large batches

### Low Priority

7. Consolidate duplicate test helpers
8. Split large test files (>500 lines)
9. Add mutation testing to verify test effectiveness

---

*Generated: 2026-04-09*
