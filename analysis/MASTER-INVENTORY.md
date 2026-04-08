# Master Test Inventory - Pterodactyl Team

## Total Test Count Summary

| Category | Test Count | Location |
|----------|------------|----------|
| **Backend Unit Tests** | ~1,100 | 4 repos |
| **Backend Integration Tests** | ~200 | 4 repos |
| **Backend API Tests** | ~100 | 4 repos |
| **Cypress E2E Tests** | ~70 | sandbox repo |
| **Selenium Tests** | 89+ | zocdoc_web monolith |
| **Frontend Unit Tests** | 0 | frontend-monorepo |
| **TOTAL** | **~1,560+** | |

---

## 1. practice-user-permissions (~870 tests)

### Unit Tests (~520 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `Services/UserRolesServiceTests.cs` | 17 | SetUserRoles, GetUserRoles, QueryUserRolesByEntity |
| `Services/UserServiceTests.cs` | 18 | GetUserPractices, GetOverlappingUsers |
| `Services/Auth0UserServiceTests.cs` | 3 | SSO user detection (samlp prefix) |
| `Services/FgaModelServiceTests.cs` | 1 | GetLatestModelId |
| `Services/UserInvitationServiceTests.cs` | 9 | Invitation CRUD, filtering |
| `Services/UserRolesHierarchyServiceTests.cs` | 10 | Role inheritance, hierarchy traversal |
| `Services/UserRolesServicePaginationTests.cs` | 9 | Pagination, V2 filtering, BatchGetUserVersions |
| `Services/ScopedOrganizationMemberServiceTests.cs` | 8 | Scoped org membership CRUD |
| `Services/DlqRedriveServiceTests.cs` | 7 | DLQ redrive operations |
| `Services/TupleAuditServiceTests.cs` | 61 | FGA tuple auditing |
| `Services/OrganizationMembersServiceTests.cs` | 27 | Org membership CRUD, hierarchy |
| `Services/UserEditAuthorizationServiceTests.cs` | 7 | Edit authorization checks |
| `Services/UserRoleChangeNotificationServiceTests.cs` | 4 | Notification queueing |
| `Services/PracticeChurnCalculatorTests.cs` | 11 | Practice churn logic |
| `Services/UltimateParentOrganizationServiceTests.cs` | 16 | Ultimate parent resolution |
| `Services/NonceIdServiceTests.cs` | 4 | Nonce ID generation |
| `Services/InternalMigrationServiceTests.cs` | 8 | Migration operations |
| `Clients/FgaRelationConverterTests.cs` | 59 | FGA relation conversions |
| `Clients/MessagingServiceClientTests.cs` | 7 | Messaging client |
| `Clients/PracticeUserRolesApiCallerTests.cs` | 11 | API caller |
| `Clients/ProviderGroupingClientTests.cs` | 1 | POGS client |
| `Helpers/FgaTupleParsingHelperTests.cs` | 17 | Tuple parsing |
| `Dtos/*.cs` | ~30 | DTO serialization |
| `Converters/*.cs` | ~5 | DateTime/JSON converters |
| **Lambda Unit Tests** | | |
| `FgaUpdates/FgaTupleCreatorTests.cs` | 11 | Tuple creation |
| `FgaUpdates/FgaUpdateServiceTests.cs` | 8 | Update processing |
| `FgaUpdates/FgaUpdatesGeneratorTests.cs` | 4 | Update generation |
| `AuditLogging/AuditLogGeneratorTests.cs` | 7 | Audit log generation |
| `AuditLogging/AuditLoggingServiceTests.cs` | 6 | Logging service |
| `OrganizationMembershipUpdates/*.cs` | ~50 | Org membership events |
| `OrganizationHierarchyRoleFixes/*.cs` | ~54 | Hierarchy role fixes |
| `ProviderMapping/*.cs` | 13 | Provider mapping |
| `ScopedOrganizationChanges/*.cs` | 15 | Scoped org changes |
| `UserRoleChangeNotificationLambda/*.cs` | 16 | Role change notifications |
| `SqsEventParserTests.cs` | 8 | SQS parsing |
| `SqsEventClassifierTests.cs` | 6 | Event classification |
| **Web Unit Tests** | | |
| `UserRolesValidatorTests.cs` | 24 | Request validation |
| `AuthorizationCheckerTests.cs` | 1 | Batch auth checks |
| `AuthorizationUnderAuditTests.cs` | 6 | Audit authorization |
| `ScopeValidationServiceTests.cs` | 3 | Scope validation |
| `PreviewUserPermissionChangesImplTests.cs` | 4 | Preview changes |
| `Helpers/Access/*.cs` | 18 | Access helpers |

### Integration Tests (~260 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `Persistence/UserRolesPersistenceTests.cs` | 38 | DynamoDB user roles CRUD |
| `Persistence/OrganizationMembersPersistenceTests.cs` | 22 | DynamoDB org members |
| `Persistence/ScopedOrganizationMemberPersistenceTests.cs` | 15 | DynamoDB scoped org |
| `Persistence/UserInvitationPersistenceTests.cs` | 12 | DynamoDB invitations |
| `Persistence/PracticeBlockedPersistenceTests.cs` | 10 | DynamoDB blocked practices |
| `Persistence/PracticeMemberPersistenceTests.cs` | 10 | DynamoDB practice members |
| `Persistence/LockPersistenceTests.cs` | 6 | DynamoDB locking |
| `Persistence/ContinuationTokenPersistenceTests.cs` | 6 | Continuation tokens |
| **Lambda Integration Tests** | ~100 | |
| `FgaLambdaTests.cs` | 4 | FGA lambda with real SQS |
| `StreamConsumerLambdaTests.cs` | 20+ | DDB stream to SQS |
| `MonolithBackfillLambdaTests.cs` | Multiple | Monolith backfill |

### API Tests (~90 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `UserRolesApiTests.cs` | 123 | SetUserRoles, GetEntityUsersRoles, queries |
| `UserApiTests.cs` | 19 | AuthorizeEditUserData, AuthorizeViewUserData |
| `InternalApiTests.cs` | 33 | Internal admin endpoints |
| `MplPracticesApiTests.cs` | 11 | SetMplPractices |
| `PracticeChurnApiTests.cs` | 8 | BackfillPracticeChurn |
| `PreviewAccessChangesApiTests.cs` | 8 | Preview access changes |
| `FgaModelApiTest.cs` | 2 | FGA model operations |
| `AuthorizationRequirementApiTests.cs` | 8 | Authorization requirements |

---

## 2. practice-authorization-proxy (30 tests)

### Unit Tests (17 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `Service/AuthorizationServiceTests.cs` | 12 | IsPracticeAuthorized, IsOrganizationAuthorized, batch operations |
| `ConversionExtensionsTests.cs` | 5 | PermissionFilter conversions, batch result conversions |

### API Tests (10 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `PracticeAuthorizationTests.cs` | 5 | Practice authorization endpoints (401, 403, 200, batch limits) |
| `OrganizationAuthorizationTests.cs` | 5 | Organization authorization endpoints |

### Placeholder Tests (3 - TO REMOVE)

| Test File | Test Count | Status |
|-----------|------------|--------|
| `UnitTests/ExampleTests.cs` | 1 | PLACEHOLDER (1+1=2) |
| `IntegrationTests/ExampleTests.cs` | 1 | PLACEHOLDER (1+1=2) |
| `Web.IntegrationTests/ExampleTests.cs` | 1 | PLACEHOLDER (1+1=2) |

---

## 3. provider-grouping (~200 tests)

### API Tests (~104 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `GroupControllerTests.cs` | 26 | Group CRUD, member management |
| `GroupRuleControllerTests.cs` | 18 | Rule preview, update, refresh |
| `OrganizationControllerTests.cs` | 60+ | Org CRUD, hierarchy, membership |

### Integration Tests (~35 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `AuditLoggingMetadataServiceTests.cs` | 1 | Audit logging metadata |
| `GroupPersistenceTests.cs` | 10 | DynamoDB group CRUD |
| `MembershipValidatorExecutorTests.cs` | 2 | Hierarchy refresh |
| `OrganizationPersistenceTests.cs` | 16 | DynamoDB org CRUD, locking |
| `OrganizationSyncServiceTests.cs` | 6 | Salesforce sync |

### Lambda Tests (~25 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `ChangeStreamLambdaTests.cs` | 8 | DynamoDB stream notifications |
| `GroupUpdateLambdaTests.cs` | 3 | Single/multi-level org processing |
| `MetadataChangeProcessorTests.cs` | 6 | New org processing, error handling |
| `MonolithSyncLambdaHandlerTests.cs` | 7 | Event routing, batch failures |
| `ReferenceDataChangeLambdaTests.cs` | 4 | Provider/location handling |
| `StrategicLambdaTests.cs` | 2 | Entry point + 1 IGNORED |

### Unit Tests (~36 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `DeleteOrganizationImplTests.cs` | 5 | Deletion validation |
| `DtoTests.cs` | 15 | DTO serialization |
| `OrganizationTests.cs` | 1 | Exception handling |
| `WebDtoTests.cs` | 4 | Enum mapping |
| `GroupServiceTests.cs` | 5 | Member validation |
| `GroupSyncServiceTests.cs` | 5 | Lock validation |
| `GroupValidationServiceTests.cs` | 12 | Membership validation |
| `JitterbitServiceTests.cs` | 1 | S3 upload |
| `KinesisNotificationServiceTests.cs` | 1 | Kinesis publishing |
| `OrganizationEntityServiceTests.cs` | 3 | Provider/location retrieval |
| `OrganizationGraphValidationServiceTests.cs` | 17 | Cycle detection |
| `OrganizationHierarchyServiceTests.cs` | 4 | Hierarchy traversal |
| `OrganizationServiceTests.cs` | 20+ | Org operations |
| `OrganizationSyncServiceTests.cs` | 4 | Sync operations |
| `RuleServiceTests.cs` | 18 | Rule evaluation |
| `SnsServiceTests.cs` | 4 | SNS publishing |
| `StrategicBackfillWorkerTests.cs` | 9 | Backfill scenarios |

---

## 4. provider-join-service (~300 tests)

### Integration Tests (~82 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `InsuranceWizardTest.cs` | 26 | Insurance onboarding wizard |
| `LocalStackDemoRequestTests.cs` | 4 | Demo request validation |
| `LocalStackDynamoDbTests.cs` | 4 | DynamoDB operations |
| `PostSubmissionUpdatesTest.cs` | 2 | Step function trigger |
| `LeadRetrievalTest.cs` | 12 | Lead data retrieval |
| `CcpaTest.cs` | 2 | CCPA data deletion |
| `ClaimProfileTest.cs` | 2 | Profile claim removal |
| `UserAgreementTests.cs` | 3 | User agreement PDF |
| `PricingTest.cs` | 2 | Signup pricing |
| `SignUpFlowTest.cs` | 10 | Full signup flow |
| `AccountCreationTests.cs` | 15 | Account creation, email confirmation |

### API Unit Tests (~150 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `ProviderJoinServiceReadWriteDataRequirementHandlerTests.cs` | 14 | Read/write authorization |
| `RequestDemoImplTest.cs` | 5 | Demo request creation |
| `PricingImplTest.cs` | 2 | Pricing endpoint |
| `AccountCreationImplTest.cs` | ~20 | Account creation errors |
| `SelfSignUpPracticeAuthorizationHandlerTests.cs` | 8 | Practice auth |
| `CsrAuthorizationHandlerTests.cs` | 2 | CSR auth |
| `PracticeAuthorizationHandlerTests.cs` | 8 | Practice auth |
| `LeadHelperTests.cs` | 14 | Test lead detection |
| `ValidationExtensionsTests.cs` | 22 | Email/phone/zip validation |
| `SelfSignupLeadStatusBuilderTest.cs` | 70+ | State/view validation |
| `LeadSubmissionImplTest.cs` | ~15 | Salesforce submission |
| `InsuranceWizardImplTest.cs` | ~20 | Insurance wizard logic |
| `LeadRetrievalImplTest.cs` | ~25 | Lead retrieval |
| `LeadGenerationImplTest.cs` | ~15 | Lead generation |
| `UpdateLeadStatusPostSubmissionImplTest.cs` | ~15 | Post-submission updates |
| `RequestValidatorTest.cs` | ~15 | Request validation |
| Others | ~20 | Various endpoints |

### Infrastructure Unit Tests (~65 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `LocationHelperTests.cs` | 5 | Zip to state mapping |
| `DdbRepositoryTests.cs` | 4 | DynamoDB CRUD |
| `EnumExtensionsTests.cs` | 3 | Enum conversion |
| `CollectionExtensionsTests.cs` | 3 | Collection utilities |
| `LeadDdbDtoFactoryTest.cs` | 3 | DTO factory |
| `UserAgreementApiTests.cs` | 3 | Monolith API |
| `FoundationalSupplementalMappingServiceTests.cs` | 4 | Specialty mapping |
| `LeadsServiceTests.cs` | 14 | Lead service |
| `SignupPortalServiceTest.cs` | 10 | Signup portal |
| `SalesforceRepositoryTest.cs` | 5 | Salesforce repository |
| `SignUpServiceTest.cs` | 15 | SignUp service |
| `LeadSalesforceServiceTests.cs` | ~25 | Salesforce lead ops |
| `InsuranceOnboardingServiceTest.cs` | 13 | Insurance onboarding |
| `PricingServiceTests.cs` | 6 | Pricing calculation |
| `AccountCreationServiceTest.cs` | ~20 | Account creation |
| Others | ~10 | Various services |

### Lambda Tests (3 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `FunctionTest.cs` | 1 | Returns ID (trivial) |
| `FunctionalTests/FunctionTest.cs` | 2 | Success/error logging |

---

## 5. Cypress E2E Tests (~70 tests)

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `rbac/user-management-smoke.spec.js` | 9 | Users page, add/edit/delete user |
| `rbac/rbac-smoke.spec.js` | 10 | Role-based access for all user types |
| `rbac/practicemgmt-smoke.spec.js` | 26 | Practice settings, providers, VR, dashboard |
| `rbac/spomgmt-smoke.spec.js` | 5 | SPO campaigns |
| `rbac/billingmgmt-smoke.spec.js` | 1 | Billing functionality |
| `rbac/appointmentmgmt-smoke.spec.js` | 6+ | Appointment CRUD, inbox filters |
| `provider/provider-providerspage-regression.spec.js` | 9 | Providers page filters, search, columns |
| `BU/Infrastructure/Auth/*` | 7 | Provider signin, MFA, validation |

---

## 6. Selenium Tests (zocdoc_web monolith) - 89 tests

| Test File | Test Count | What It Tests |
|-----------|------------|---------------|
| `Tests/API/UserManagementApiTests.cs` | 5 | User management API |
| `Tests/API/PracticeUserManagementApiTests.cs` | 17 | Practice user management |
| `Tests/API/OrganizationUserApiTests.cs` | 1 | Organization user API |
| `Tests/ProviderDashboard/PermissionCheckerFgaTest.cs` | 2 | FGA permission checker |
| `Tests/API/PracticeUserPermissionsMultiProviderLoginLogic.cs` | 1 | Multi-provider login |
| `Tests/ProviderConfigApiFgaAuthTests.cs` | 3 | Provider config FGA |
| `Tests/API/PracticeUserRolesPrivateApiTest.cs` | 29 | Practice user roles |
| `Tests/ProviderDashboard/ProviderDashboardRbacControllerHttpTests.cs` | 31 | RBAC controller |
| `Tests/API/SelfSignUp/SelfSignUpFgaAuthTests.cs` | TBD | Self sign-up FGA |
| `Tests/API/SelfSignUp/ProviderSelfSignUpFgaAuthTests.cs` | TBD | Provider self sign-up FGA |
| **TOTAL** | **89+** | |

---

## 7. Frontend Unit Tests

| Category | Test Count | Status |
|----------|------------|--------|
| Users Page components | 0 | **CRITICAL GAP** |
| Role management components | 0 | **CRITICAL GAP** |
| Permission components | 0 | **CRITICAL GAP** |
| org-management webapp | 1 scaffold | Placeholder only |

---

## Summary by Test Type

| Test Type | Count | Percentage |
|-----------|-------|------------|
| Backend Unit | ~1,100 | 71% |
| Backend Integration | ~200 | 13% |
| Backend API | ~100 | 6% |
| Selenium (monolith) | 89 | 6% |
| Cypress E2E | ~70 | 4% |
| Frontend Unit | 0 | 0% |
| **TOTAL** | **~1,560** | **100%** |

---

## Visual Summary

```
Test Distribution:
Backend Unit:        ████████████████████████████████████████ 71%
Backend Integration: ███████ 13%
Backend API:         ███ 6%
Selenium:            ███ 6%
Cypress E2E:         ██ 4%
Frontend Unit:       ░ 0% (CRITICAL GAP)
```

---

*Generated: 2026-04-09*
*Total: ~1,560 tests across all test types*
