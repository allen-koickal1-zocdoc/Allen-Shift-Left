# Verified Test Gaps (v3 — current HEAD)

Each gap below was re-verified at the SHA in [README.md](README.md). A gap is recorded only when **direct** coverage is absent (a class can still be hit indirectly through API/integration tests).

## Critical — production logic with zero direct test coverage

| Repo | Class / Surface | Evidence |
|------|-----------------|----------|
| practice-authorization-proxy | `AuthorizationImpl` (183 LOC, primary `IAuthorization` impl: `IsPracticeAuthorized`, `IsOrganizationAuthorized`, `BatchIsPracticeAuthorized`, `BatchIsOrganizationAuthorized`) | `grep -rln "AuthorizationImpl" tests/` → no matches. Exercised only via API tests. [src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs](https://github.com/Zocdoc/practice-authorization-proxy/blob/88ed06931303fe57e1d3cb948e86d029037fe881/src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs) |
| practice-user-permissions | `PracticeBlockedService` | No `PracticeBlockedServiceTests.cs`; all 18 test refs are `Mock<IPracticeBlockedService>`. [src/PracticeUserPermissions/Service/PracticeBlockedService.cs](https://github.com/Zocdoc/practice-user-permissions/blob/e484112be9b04a2c5b6b2d3cd0c36ad613e367c7/src/PracticeUserPermissions/Service/PracticeBlockedService.cs) |
| practice-user-permissions | `AuditLoggingMetadataService` | No sibling test; only DI registration in `Cron.IntegrationTests/IntegrationTestsBase.cs:94`. [src/PracticeUserPermissions/Service/AuditLoggingMetadataService.cs](https://github.com/Zocdoc/practice-user-permissions/blob/e484112be9b04a2c5b6b2d3cd0c36ad613e367c7/src/PracticeUserPermissions/Service/AuditLoggingMetadataService.cs) |
| provider-grouping | `DynamicGroupingUpdateExecutor` | `grep -rln "DynamicGroupingUpdateExecutor" tests/` → no matches. [src/ProviderGrouping/Service/DynamicGrouping/DynamicGroupingUpdateExecutor.cs](https://github.com/Zocdoc/provider-grouping/blob/b7e65e81484cb41823073398d28563b2d5f80b73/src/ProviderGrouping/Service/DynamicGrouping/DynamicGroupingUpdateExecutor.cs) |
| provider-join-service | `StepFunctionService` | All test refs are `Mock<IStepFunctionService>`; no test for the impl. [src/SelfSignup.Infrastructure/Services/StepFunctionService/StepFunctionService.cs](https://github.com/Zocdoc/provider-join-service/blob/a7635199696e49f35fdd1cf73f346e86a99cfdbd/src/SelfSignup.Infrastructure/Services/StepFunctionService/StepFunctionService.cs) |
| provider-join-service | `CreatePracticeDtoFactory` | 0 references in `tests/`. [src/SelfSignup.Infrastructure/Services/PracticeAndProviderCreation/CreatePracticeDtoFactory.cs](https://github.com/Zocdoc/provider-join-service/blob/a7635199696e49f35fdd1cf73f346e86a99cfdbd/src/SelfSignup.Infrastructure/Services/PracticeAndProviderCreation/CreatePracticeDtoFactory.cs) |
| provider-join-service | `UpdatesDefinitionFactory` | 0 references in `tests/`. [src/SelfSignup.Infrastructure/Services/Factories/UpdatesDefinitionFactory.cs](https://github.com/Zocdoc/provider-join-service/blob/a7635199696e49f35fdd1cf73f346e86a99cfdbd/src/SelfSignup.Infrastructure/Services/Factories/UpdatesDefinitionFactory.cs) |
| provider-fe-monorepo | `createProviderOrStaffPage` UI (7 source files) | 0 Jest/Vitest unit tests; only 26 in-app Cypress + 2 stories. See [frontend.md](frontend.md). |

## Thin coverage on high-fan-in surfaces

| Repo | Surface | Issue |
|------|---------|-------|
| practice-user-permissions | `Lambda.IntegrationTests` | **1** integration test (`ProviderGroupMembershipSqsEventsLambdaTests`) for the largest source surface (many handlers: FgaLambdaHandler, FgaReadLambdaHandler, OrganizationMembershipProcessor, ScopedOrganizationChangeProcessor, …). |
| provider-grouping | `SalesforceAccountBackfillCron` | **0 tests.** |
| provider-grouping | `StrategicLambda` | Only 1 active test; the other (`Verify_Handler_Processes_Correctly`) is `[Ignore("Test Not Completed")]` with a commented-out body. |

## Trivial / placeholder tests to replace or remove

| Repo | Test | Issue |
|------|------|-------|
| practice-authorization-proxy | `UnitTests/ExampleTests.TokenEmptyTest` | `(1 + 1).Should().Be(2);` — [line 11](https://github.com/Zocdoc/practice-authorization-proxy/blob/88ed06931303fe57e1d3cb948e86d029037fe881/tests/PracticeAuthorizationProxy.UnitTests/ExampleTests.cs#L11) |
| practice-authorization-proxy | `IntegrationTests/ExampleTests.TokenEmptyTest` | `(1 + 1).Should().Be(2);` — [line 11](https://github.com/Zocdoc/practice-authorization-proxy/blob/88ed06931303fe57e1d3cb948e86d029037fe881/tests/PracticeAuthorizationProxy.IntegrationTests/ExampleTests.cs#L11) |
| practice-authorization-proxy | `Web.IntegrationTests/ExampleTests.TokenEmptyTest` | `(1 + 1).Should().Be(2);` — [line 11](https://github.com/Zocdoc/practice-authorization-proxy/blob/88ed06931303fe57e1d3cb948e86d029037fe881/tests/PracticeAuthorizationProxy.Web.IntegrationTests/ExampleTests.cs#L11) |
| provider-join-service | `AbandonmentLambda.Tests/FunctionTest.TestReturnsId` | Echo-back: sets `DynamoRowId = "hello"`, asserts function returns `"hello"`. |
| provider-grouping | `LambdaTests/Lambdas/StrategicLambdaTests.Verify_Handler_Processes_Correctly` | `[Ignore("Test Not Completed")]`, body commented out. |

## Empty test projects

| Repo | Project |
|------|---------|
| provider-join-service | `SelfSignup.Tests.Unit` (only `Usings.cs`) |

> Note: `practice-user-permissions.Worker.UnitTests`, **empty in v2**, now has **8 tests** — this gap is closed.

## Infrastructure / surfaces absent everywhere

| Surface | Status |
|---------|--------|
| CDK / infrastructure tests | **0** in all 4 backend repos, despite each shipping a `cdk/jest.config.js` (and `"test": "jest"` scripts). No `cdk/test/` dirs, no `*.test.ts`. |
| Playwright (Account-User-Setup E2E) | **0** specs — folders scaffolded with `.gitkeep`; migration from Cypress not started. |
| Datadog Synthetics-as-code, Pact/contract, k6, Verify snapshot, mutation, a11y | Not present in any repo (cannot verify Datadog UI-side synthetics). |
