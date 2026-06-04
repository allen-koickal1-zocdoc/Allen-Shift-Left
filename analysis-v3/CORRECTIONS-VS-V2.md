# Corrections vs v2

Each v2 claim that v3 re-evaluated is graded **CONFIRMED** (still true), **CHANGED** (count moved — usually real new tests), or **REFUTED** (v2 was wrong).

## zocdoc_web monolith — the headline correction

| v2 Claim | Status | v3 Evidence |
|----------|--------|-------------|
| 255 tests across 13 files | **REFUTED** | 433 test methods across 27 files. v2's numbers came from an un-grepped subagent and the grep it documented (`[Test]`/`[TestCase(`) is blind to the `[CiTest]` attribute that actually marks tests in the monolith. |
| Zero real Selenium tests | **CONFIRMED (strengthened)** | All 27 files: 0 `OpenQA.Selenium`; all chain to `BaseZocHttpApiTestFixture`. |
| 13 Pterodactyl-relevant files | **CHANGED** | 27 files — 14 new (ProviderSelfSignUpControllerTests, SelfSignUpControllerTests, ProviderConfigApiControllerTest, etc.). No v2 file disappeared. |

## practice-user-permissions

| v2 Claim | Status | v3 Evidence |
|----------|--------|-------------|
| 1,043 tests / 94 files | **CHANGED** | 1,075 tests / 98 files (real growth). |
| `Worker.UnitTests` is empty | **REFUTED (gap closed)** | Now 8 tests. New `Cron.UnitTests` (13) and `SmokeTests` (3) also appeared. |
| `PracticeBlockedService` untested | **CONFIRMED** | No `PracticeBlockedServiceTests.cs`; 18 refs are all `Mock<I...>`. |
| `AuditLoggingMetadataService` untested | **CONFIRMED** | Only a DI registration in a test base; no direct test. |
| No `[Ignore]`/`[Explicit]` anywhere | **CONFIRMED** | None found. |
| 0 CDK tests | **CONFIRMED** | `cdk/jest.config.js` present; no `cdk/test/`, 0 `*.test.ts`. |
| Test/source ratio 2.43× | **CHANGED** | 2.38× (18,168 / 43,420). |

## practice-authorization-proxy

| v2 Claim | Status | v3 Evidence |
|----------|--------|-------------|
| 26 tests / 7 files | **CHANGED** | 31 tests / 8 files (new `SmokeTests` project, 5). |
| 3 `(1+1)` placeholder tests | **CONFIRMED** | All three `ExampleTests.cs` still assert `(1 + 1).Should().Be(2)` at line 11. |
| `AuthorizationImpl` 183 LOC, 0 unit tests | **CONFIRMED** | `grep -rln "AuthorizationImpl" tests/` → none. |
| 0 CDK tests | **CONFIRMED** | jest config present, 0 test files. |

## provider-grouping

| v2 Claim | Status | v3 Evidence |
|----------|--------|-------------|
| 471 tests / 36 files | **CHANGED** | 558 tests / 45 files. |
| `StrategicLambdaTests` `[Ignore]`d | **CONFIRMED** | Line 56 `[Ignore("Test Not Completed")]`; 1 of 2 tests stubbed. |
| `MonolithSyncLambda` 23 tests | **CONFIRMED** | 14 integration + 9 lambda-unit. |
| `DynamicGroupingUpdateExecutor` untested | **CONFIRMED** | 0 refs in `tests/`. |
| (new) `SalesforceAccountBackfillCron` | **NEW GAP** | 0 tests. |
| 0 CDK tests | **CONFIRMED** | jest config present, 0 test files. |

## provider-join-service

| v2 Claim | Status | v3 Evidence |
|----------|--------|-------------|
| 634 tests / 54 files | **CHANGED** | 642 tests / 55 files (new `SmokeTests`, 4). |
| `SelfSignup.Tests.Unit` empty | **CONFIRMED** | Only `Usings.cs`. |
| `AbandonmentLambda` echo-back test | **CONFIRMED** | `DynamoRowId="hello"` → asserts `"hello"`. |
| `StepFunctionService` / `CreatePracticeDtoFactory` / `UpdatesDefinitionFactory` untested | **CONFIRMED** | StepFunctionService only mocked; other two have 0 refs. |
| 0 CDK tests | **CONFIRMED** | jest config present, 0 test files. |

## Frontend (provider-fe-monorepo)

| v2 Claim | Status | v3 Evidence |
|----------|--------|-------------|
| 5 Jest/Vitest unit tests | **REFUTED (undercount)** | 20 unit tests / 6 files. v2 missed the 15 `signUpPortal` unit tests (`Context`, `Footer`, `RepositionConfirmEmail`, `steps`) because they use the dotted `*.test.tsx` convention. |
| 149 in-app Cypress tests | **CHANGED** | 151 across 4 files. |
| 13 Chromatic stories | **CHANGED** | 12 stories. |
| 3 owned UI areas (CODEOWNERS) | **CONFIRMED** | Unchanged: practiceUsersPage, createProviderOrStaffPage, signUpPortal. |
| (new) `createProviderOrStaffPage` | **NEW GAP** | 0 unit tests. |

## sandbox E2E

| v2 Claim | Status | v3 Evidence |
|----------|--------|-------------|
| 72 Cypress `it()` / 9 files | **CHANGED** | 71 / 8 files (Flows 60, Pages 11). |
| (new) Playwright migration | **NOT STARTED** | Account-User-Setup Playwright folders contain only `.gitkeep`; 0 specs. |
