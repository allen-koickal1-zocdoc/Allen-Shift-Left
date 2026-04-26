# Corrections vs v1

For each v1 claim that v2 evaluated, status is one of **CONFIRMED**, **REFUTED**, or **PARTIAL**.

## practice-user-permissions

| v1 Claim | Status | v2 Evidence |
|----------|--------|-------------|
| ~870 total tests | **REFUTED** | 1,043 tests across 94 files. Source: per-project tally in [MASTER-INVENTORY.md](MASTER-INVENTORY.md). |
| 94 test files | **CONFIRMED** | `find tests -name "*.cs" -exec grep -lE "^\s*\[Test\]\|^\s*\[TestCase\(" {} \;` → 94. |
| `TupleAuditServiceTests` = 61 tests | **REFUTED** | 70 tests (47 `[Test]` + 23 `[TestCase(`). [Source](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.UnitTests/Services/TupleAuditServiceTests.cs). |
| `UserRolesApiTests` = 123 tests | **REFUTED** | 122 tests (112 `[Test]` + 10 `[TestCase(`). [Source](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Web.ApiTests/UserRolesApiTests.cs). |
| `BatchGetEntityDirectUsersCount` has no API tests | **REFUTED** | 11 tests in `UserRolesApiTests.cs` lines 4361–4706 under `#region BatchGetEntityDirectUsersCount`. [Source](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Web.ApiTests/UserRolesApiTests.cs#L4335). |
| `PracticeBlockedService` has only persistence-level tests, no service-level unit tests | **CONFIRMED** | No file matching `PracticeBlockedServiceTests.cs` in `tests/`. [Source class](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/src/PracticeUserPermissions/Service/PracticeBlockedService.cs). |
| `AuditLoggingMetadataService` has no direct tests | **CONFIRMED** | No file matching `AuditLoggingMetadataServiceTests.cs`. [Source class](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/src/PracticeUserPermissions/Service/AuditLoggingMetadataService.cs). |
| `Worker.UnitTests` project exists but is empty | **CONFIRMED** | Project contains only `AssemblyInfo.cs`, `BUILD`, and `.csproj`. [Source dir](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Worker.UnitTests). |
| 21 untested core logic classes | **PARTIAL** | v2 directly verified 3 untested service classes (`PracticeBlockedService`, `AuditLoggingMetadataService`, `DlqRedriveSettings`). The other 18 were not individually re-verified — see [GAPS.md](GAPS.md). |
| No `[Ignore]` or `[Explicit]` attributes anywhere | **CONFIRMED** | `grep -rn "\[Ignore\(" tests/` and `grep -rn "\[Explicit\]" tests/` → no matches. |
| Test/Source LOC ratio: 2.33x | **PARTIAL** | v2 measures **2.43x** (43,603 / 17,958). v1 was approximately right. |

## practice-authorization-proxy

| v1 Claim | Status | v2 Evidence |
|----------|--------|-------------|
| `AuthorizationImpl` is 184 lines with 0 unit tests | **PARTIAL** | File is **183** lines (off by 1). Confirmed 0 unit tests: `grep -rln "AuthorizationImpl" tests/` → no results. [Source](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs). |
| 3 placeholder `1+1==2` tests | **CONFIRMED** | All three `ExampleTests.cs` files contain a `TokenEmptyTest` asserting `(1 + 1).Should().Be(2);`. See [practice-authorization-proxy.md](practice-authorization-proxy.md) for direct line links. |
| 30 tests across 4 files | **REFUTED** | **26 tests across 7 files** (v1 missed 3 files including the placeholders). |

## provider-grouping

| v1 Claim | Status | v2 Evidence |
|----------|--------|-------------|
| `StrategicLambdaTests.cs` test is `[Ignore("Test Not Completed")]` | **CONFIRMED** | Line 56: `[Ignore("Test Not Completed")]`. [Source](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests/Lambdas/StrategicLambdaTests.cs#L56). |
| `MonolithSyncLambda` has zero tests | **REFUTED** | 23 tests across two files: 14 in `IntegrationTests/MonolithSyncLambdaHandlerTests.cs` + 9 in `LambdaTests/Lambdas/MonolithSyncLambdaHandlerTests.cs`. |
| ~200 total tests | **REFUTED** | **471 tests across 36 files**. v1 was off by more than 2x. |
| `DynamicGroupingUpdateExecutor` has no unit tests | **CONFIRMED** | `grep -rln "DynamicGroupingUpdateExecutor" tests/` → no matches. [Source class](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/src/ProviderGrouping/Service/DynamicGrouping/DynamicGroupingUpdateExecutor.cs). |

## provider-join-service

| v1 Claim | Status | v2 Evidence |
|----------|--------|-------------|
| `StepFunctionService` has 0 direct tests | **CONFIRMED** | All references in tests are `Mock<IStepFunctionService>`, no test class for the implementation. [Source class](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/src/SelfSignup.Infrastructure/Services/StepFunctionService/StepFunctionService.cs). |
| `CreatePracticeDtoFactory` has 0 tests | **CONFIRMED** | `grep -rln "CreatePracticeDtoFactory" tests/` → no matches. [Source class](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/src/SelfSignup.Infrastructure/Services/PracticeAndProviderCreation/CreatePracticeDtoFactory.cs). |
| `UpdatesDefinitionFactory` has 0 tests | **CONFIRMED** | `grep -rln "UpdatesDefinitionFactory" tests/` → no matches. [Source class](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/src/SelfSignup.Infrastructure/Services/Factories/UpdatesDefinitionFactory.cs). |
| `DdbRepository` `shouldIgnoreNullValues=false` only covered in integration | **PARTIAL (UNVERIFIED)** | Not specifically re-verified in v2. `DdbRepositoryTests.cs` has 4 unit tests; deeper integration coverage check skipped. |
| `InsuranceWizardTest` = 26 tests | **REFUTED** | 34 tests. [Source](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/InsuranceWizardTest.cs). |
| `AccountCreationTests` = 15 tests | **CONFIRMED** | 15 tests. [Source](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/AccountCreationTests.cs). |
| `SignUpFlowTest` = 10 tests | **CONFIRMED** | 10 tests. [Source](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/SignUpFlowTest.cs). |
| `SelfSignupLeadStatusBuilderTest` = 70+ tests | **CONFIRMED** | 73 tests. [Source](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/SelfSignupLeadStatusBuilderTest.cs). |
| `AbandonmentLambda` `FunctionTest` is trivial echo-back assertion | **CONFIRMED** | `Assert.AreEqual("hello", test.Result);` — test inputs `DynamoRowId = "hello"` and asserts the function returns `"hello"`. [Source line](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/ProviderJoinService.AbandonmentLambda.Tests/FunctionTest.cs#L19). |
| 11 untested core logic classes | **PARTIAL** | 3 specifically re-verified (above); other 8 not individually re-checked. |
| Source LOC 8,115 / Test LOC 11,563 | **CONFIRMED** | Counts re-run in v2 match exactly. |

## zocdoc_web monolith — "Selenium" (mislabeled)

| v1 Claim | Status | v2 Evidence |
|----------|--------|-------------|
| 89+ Selenium / WebDriver tests | **REFUTED — biggest correction in this audit** | Zero tests use `OpenQA.Selenium`. All 255 extend `BaseZocHttpApiTestFixture`. The directory `SeleniumTests/SeleniumTests/Tests/` is misnamed; the contents are HTTP API tests. |
| `PracticeUserRolesPrivateApiTest.cs` = 29 | **REFUTED** | 72 tests. |
| `ProviderDashboardRbacControllerHttpTests.cs` = 31 | **REFUTED** | 51 tests. |
| `OrganizationUserApiTests.cs` = 1 | **REFUTED** | 34 tests. |
| `PracticeUserManagementApiTests.cs` = 17 | **PARTIAL** | 22 tests (slight under-count). |
| `BulkProfileCompletionFgaAuthTests.cs` (missed) | **REFUTED — file missed entirely** | 19 tests. |
| `PracticeLocationsSettingsFgaAuthTests.cs` (missed) | **REFUTED — file missed entirely** | 15 tests. |
| `MultiPracticeProfileSettingsFgaAuthTests.cs` (missed) | **REFUTED — file missed entirely** | 9 tests. |
| `PermissionCheckerFgaTest.cs` = 2 | **REFUTED** | 7 tests. |
| `UserManagementApiTests.cs` = 5 | **REFUTED** | 7 tests. |
| `ProviderConfigApiFgaAuthTests.cs` = 3 | **REFUTED** | 6 tests. |
| `PracticeUserPermissionsMultiProviderLoginLogic.cs` = 1 | **REFUTED** | 2 tests. |
| `SelfSignUpFgaAuthTests.cs` = TBD | resolved | 6 tests. |
| `ProviderSelfSignUpFgaAuthTests.cs` = TBD | resolved | 5 tests. |

(Source-of-truth for these counts is the deep-audit subagent run that classified files by `using OpenQA.Selenium` and base-class inheritance. Monolith was not cloned locally for v2 — see [METHODOLOGY.md](METHODOLOGY.md).)

## Cypress E2E

| v1 Claim | Status | v2 Evidence |
|----------|--------|-------------|
| ~70 tests across 4 files | **REFUTED** | **72 tests across 9 files** under `cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/` (Flows + Pages). See [cypress-e2e.md](cypress-e2e.md). |

## Frontend (provider-fe-monorepo)

| v1 Claim | Status | v2 Evidence |
|----------|--------|-------------|
| Zero frontend unit tests for the Users Page | **CONFIRMED** | `find provider-fe-monorepo/apps/settings -type f \( -name "*.test.tsx" -o -name "*.test.ts" -o -name "*.spec.tsx" -o -name "*.spec.ts" \)` → no results. The correct repo for the Users Page is `provider-fe-monorepo` (not "frontend-monorepo" as v1 implied). |
