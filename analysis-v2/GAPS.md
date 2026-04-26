# Verified Test Gaps

Only gaps re-verified in v2 are listed here. Each row links to the source class at the pinned SHA. If v1 claimed a gap that v2 could not reproduce, it is **not** listed here — it was moved to [CORRECTIONS-VS-V1.md](CORRECTIONS-VS-V1.md) under "REFUTED".

## Critical (production logic with zero direct test coverage)

| Repo | Class | Source link | Notes |
|------|-------|-------------|-------|
| practice-authorization-proxy | `AuthorizationImpl` (183 LOC, primary `IAuthorization` contract impl) | [src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs) | 0 references in `tests/`. The 4 public methods (`IsPracticeAuthorized`, `IsOrganizationAuthorized`, `BatchIsPracticeAuthorized`, `BatchIsOrganizationAuthorized`) are exercised only via API tests. |
| provider-join-service | `StepFunctionService` (67 LOC) | [src/SelfSignup.Infrastructure/Services/StepFunctionService/StepFunctionService.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/src/SelfSignup.Infrastructure/Services/StepFunctionService/StepFunctionService.cs) | All test references are `Mock<IStepFunctionService>`. No tests for the implementation itself. |
| provider-join-service | `CreatePracticeDtoFactory` (33 LOC) | [src/SelfSignup.Infrastructure/Services/PracticeAndProviderCreation/CreatePracticeDtoFactory.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/src/SelfSignup.Infrastructure/Services/PracticeAndProviderCreation/CreatePracticeDtoFactory.cs) | 0 references in `tests/`. |
| provider-join-service | `UpdatesDefinitionFactory` (190 LOC) | [src/SelfSignup.Infrastructure/Services/Factories/UpdatesDefinitionFactory.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/src/SelfSignup.Infrastructure/Services/Factories/UpdatesDefinitionFactory.cs) | 0 references in `tests/`. |
| provider-grouping | `DynamicGroupingUpdateExecutor` | [src/ProviderGrouping/Service/DynamicGrouping/DynamicGroupingUpdateExecutor.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/src/ProviderGrouping/Service/DynamicGrouping/DynamicGroupingUpdateExecutor.cs) | 0 references in `tests/`. |
| practice-user-permissions | `PracticeBlockedService` | [src/PracticeUserPermissions/Service/PracticeBlockedService.cs](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/src/PracticeUserPermissions/Service/PracticeBlockedService.cs) | No `PracticeBlockedServiceTests.cs`; only persistence-level tests reference the table. |
| practice-user-permissions | `AuditLoggingMetadataService` | [src/PracticeUserPermissions/Service/AuditLoggingMetadataService.cs](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/src/PracticeUserPermissions/Service/AuditLoggingMetadataService.cs) | No matching `*Tests.cs` file. |

## Trivial / placeholder tests that should be replaced or removed

| Repo | Test | Source link | Issue |
|------|------|-------------|-------|
| practice-authorization-proxy | `PracticeAuthorizationProxy.UnitTests/ExampleTests.TokenEmptyTest` | [tests/PracticeAuthorizationProxy.UnitTests/ExampleTests.cs#L8](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.UnitTests/ExampleTests.cs#L8) | `(1 + 1).Should().Be(2);` |
| practice-authorization-proxy | `PracticeAuthorizationProxy.IntegrationTests/ExampleTests.TokenEmptyTest` | [tests/PracticeAuthorizationProxy.IntegrationTests/ExampleTests.cs#L8](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.IntegrationTests/ExampleTests.cs#L8) | `(1 + 1).Should().Be(2);` |
| practice-authorization-proxy | `PracticeAuthorizationProxy.Web.IntegrationTests/ExampleTests.TokenEmptyTest` | [tests/PracticeAuthorizationProxy.Web.IntegrationTests/ExampleTests.cs#L8](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.Web.IntegrationTests/ExampleTests.cs#L8) | `(1 + 1).Should().Be(2);` |
| provider-join-service | `ProviderJoinService.AbandonmentLambda.Tests.FunctionTest.TestReturnsId` | [tests/ProviderJoinService.AbandonmentLambda.Tests/FunctionTest.cs#L19](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/ProviderJoinService.AbandonmentLambda.Tests/FunctionTest.cs#L19) | Sets `DynamoRowId = "hello"`, asserts function returns `"hello"`. Echo-back, no real behaviour exercised. |
| provider-grouping | `LambdaTests/Lambdas/StrategicLambdaTests.Verify_Handler_Processes_Correctly` | [tests/LambdaTests/Lambdas/StrategicLambdaTests.cs#L56](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests/Lambdas/StrategicLambdaTests.cs#L56) | `[Ignore("Test Not Completed")]` — body is fully commented out. |

## Empty test projects

| Repo | Project | Path |
|------|---------|------|
| practice-user-permissions | `PracticeUserPermissions.Worker.UnitTests` | [tests/PracticeUserPermissions.Worker.UnitTests/](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Worker.UnitTests) |
| provider-join-service | `SelfSignup.Tests.Unit` | [tests/SelfSignup.Tests.Unit/](https://github.com/Zocdoc/provider-join-service/tree/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Tests.Unit) |

## Frontend

| Repo | Surface | Result |
|------|---------|--------|
| provider-fe-monorepo | `apps/settings/` Jest/Vitest unit tests | **0 files**: no `*.test.tsx`, `*.test.ts`, `*.spec.tsx`, `*.spec.ts` anywhere under `apps/settings/`. [Tree at SHA](https://github.com/Zocdoc/provider-fe-monorepo/tree/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings). |

## Items v1 raised that v2 could **not** verify

These are listed here so the reader can see them, but they should not be treated as confirmed gaps:

| Item | Reason not verified |
|------|---------------------|
| 21 untested core logic classes in practice-user-permissions | v2 verified 3 of 21 directly; the remaining 18 were named without per-class evidence in v1 and were not individually re-checked. |
| 11 untested core logic classes in provider-join-service | v2 verified 3 of 11 directly; remaining 8 not individually re-checked. |
| `DdbRepository` `shouldIgnoreNullValues=false` only covered in integration | Not specifically re-traced; `DdbRepositoryTests.cs` has 4 unit tests but coverage of that flag was not branch-traced. |
