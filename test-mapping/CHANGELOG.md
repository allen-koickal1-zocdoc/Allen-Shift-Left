# Test Mapping Changelog

Identity key for a row: `<repo-relative-path>::<MethodName>[ (CaseName)]`.

## 2026-08-21 — initial mapping: `Zocdoc/auth0-infrastructure` @ cac1149

Scope: whole repo, branch `main`. Granularity: one row per test method.

- 18 test files mapped, 200 tests total — 57 C# (NUnit) and 143 JS (142 Jest + 1 Cypress).
  - `__tests__/unit/challenge-mfa-tests.js` — 37 tests
  - `tests/UnitTests/EventProducerHandlerTests.cs` — 32 tests
  - `__tests__/unit/add-internal-services-role-claims-tests.js` — 31 tests
  - `__tests__/unit/add-external-api-user-metadata-tests.js` — 15 tests
  - `__tests__/unit/add-provider-claims-tests.js` — 15 tests
  - `tests/UnitTests/PopulateDataForDatadogHelperTests.cs` — 14 tests (one is a 48-case table)
  - `__tests__/unit/database-get-user-by-email-action-script-tests.js` — 13 tests
  - `__tests__/unit/database-login-action-script-tests.js` — 13 tests
  - `__tests__/unit/add-zocdoc-claims-tests.js` — 6 tests
  - `__tests__/unit/log-post-login-event-tests.js`, `log-provider-post-login-event-tests.js` — 5 tests each
  - `tests/UnitTests/EventProducerServicesTests.cs` — 4 tests
  - `tests/UnitTests/Auth0TenantResolverTests.cs` — 3 tests
  - `tests/UnitTests/HandlerTests.cs`, `__tests__/unit/add-internal-services-claims-tests.js` — 2 tests each
  - `tests/IntegrationTests/SsmConfigSourceIntegrationTests.cs`, `tests/UnitTests/FakeTests.cs`, `__tests__/cypress/e2e/3-auth0-tests/auth0-smoke-tests.cy.js` — 1 test each
- Coverage gaps recorded: `actions/patient/add_patient_role.js`, `redirect.js`, and `require_zd_app_for_marketplace.js` have no tests; `cdk/jest.config.js` targets a `cdk/test/` directory that does not exist.
- Correction: the earlier index figure of "66 C# + 141 JS" was wrong in both directions. The C# extractor emitted one row per `[TestCase]` attribute (57 distinct methods, not 66), and the JS extractor missed two `test.each` blocks whose title string sits on the following line (143, not 141).

## 2026-08-21 — initial mapping: `Zocdoc/ServiceMockEndpoints` @ 90eacfb

Scope: whole repo, branch `master`. Granularity: one row per test method.

- 12 test files mapped, 99 test methods total (54 declared `TestCase` cases across 10 of them).
  - `auth-dotnet/test/Zocdoc.Auth.Mock.Tests/FgaControllerTests.cs` — 34 tests
  - `auth-dotnet/test/Zocdoc.Auth.Mock.Tests/TestingControllerTests.cs` — 21 tests
  - `auth-dotnet/test/Zocdoc.Auth.Mock.Tests/JwtAuthenticationControllerTests.cs` — 10 tests
  - `auth-dotnet/test/Zocdoc.Auth.Mock.Tests/OAuth2TokenControllerTests.cs` — 9 tests
  - `auth-dotnet/test/Zocdoc.Auth.Mock.Tests/IdentityControllerTests.cs` — 6 tests
  - `auth-dotnet/test/Zocdoc.Auth.Mock.Tests/WellKnownControllerTests.cs` — 6 tests
  - `auth-dotnet/test/Zocdoc.Auth.Mock.Tests/AuthorizationControllerTests.cs` — 5 tests
  - `auth-dotnet/test/Zocdoc.Auth.Mock.Tests/AuthenticationControllerTests.cs` — 3 tests
  - `auth-dotnet/test/Zocdoc.Auth.Mock.Tests/Auth0EndpointsTests.cs` — 2 tests
  - `auth-dotnet/test/Zocdoc.Auth.Mock.Tests/JwtAuthenticationServiceTests.cs`, `ShowPayloadExampleControllerTests.cs` — 1 test each
  - `auth-dotnet/test/Zocdoc.Auth.Mock.Tests/ApiParityTests.cs` — 1 test, `[Ignore]`d and never executed

## 2026-08-21 — initial mapping: `Zocdoc/user-accounts` @ 0271f52

Scope: whole repo, branch `main`. Granularity: one row per test method.

- 7 test files mapped, 85 test methods total (1 `TestCase` pair; 8 `[Values]` tests expand over whole enums at run time).
  - `tests/UserAccounts.Web.ApiTests/AccountsApiTests.cs` — 23 tests (14 `[Category("FakeOnly")]`)
  - `tests/UserAccounts.UnitTests/FakeUserAccountDynamoPersistenceTests.cs` — 19 tests
  - `tests/UserAccounts.Web.UnitTests/ConversionExtensionsTests.cs` — 19 tests
  - `tests/UserAccounts.Web.UnitTests/AccountsImplTests.cs` — 14 tests
  - `tests/UserAccounts.IntegrationTests/DynamoUserAccountDynamoPersistenceTests.cs` — 8 tests
  - `tests/*/ExampleTests.cs` (×2) — 2 scaffold placeholders, no product coverage

## 2026-08-21 — initial mapping: `Zocdoc/user-locking` @ a0de1bc

Scope: whole repo, branch `main`. Granularity: one row per test method.

- 8 test files mapped, 80 test methods total (1 `TestCaseSource` with 3 cases).
  - `tests/UserLocking.Web.ApiTests/UserLockingApiTests.cs` — 38 tests
  - `tests/UserLocking.Web.UnitTests/UserLockingImplTests.cs` — 12 tests
  - `tests/UserLocking.LoginLockPropagatorLambda.UnitTests/HandlerTests.cs` — 11 tests
  - `tests/UserLocking.Web.IntegrationTests/UserLockDynamoPersistenceTests.cs` — 9 tests
  - `tests/UserLocking.LoginLockPropagatorLambda.IntegrationTests/LambdaTests.cs` — 7 tests
  - `tests/*/ExampleTests.cs` (×3) — 3 scaffold placeholders, no product coverage

## 2026-08-21 — initial mapping: `Zocdoc/external-developer-api-auth` @ 198ebb4

Scope: whole repo, branch `main`. Granularity: one row per test.

- 1 test file mapped, 4 tests total.
  - `cdk/test/auth0-app-clients.test.ts` — 4 tests (Jest)

## 2026-08-21 — initial mapping: `Zocdoc/audit-logging-service` @ 2d5e6ad

Scope: whole repo, branch `main`. Granularity: one row per test method.

- 17 test files mapped, 56 test methods total (11 declared `TestCase`/`TestCaseSource` cases across 6 of them).
  - `tests/ApiTests/AuthorizationLogApiTests.cs` — 7 tests
  - `tests/UnitTests/AuthorizationLogImplTest.cs` — 6 tests
  - `tests/UnitTests/PatientRefresh.Worker/ScanServiceTests.cs` — 6 tests
  - `tests/UnitTests/LogConverterTest.cs` — 5 tests
  - `tests/UnitTests/PatientIdEnqueue.Lambda/S3LogParserTests.cs` — 4 tests
  - `tests/UnitTests/PatientIdEnqueue.Lambda/ReportingModelToDdbDtoServiceTest.cs` — 4 tests
  - `tests/UnitTests/PatientRefresh.Worker/PatientResponseToDdbDtoServiceTests.cs` — 4 tests
  - `tests/UnitTests/PatientRefresh.Worker/WorkerTests.cs` — 4 tests
  - `tests/IntegrationTests/PatientWorkerIntegrationTests.cs` — 3 tests
  - `tests/UnitTests/LegalReportingPatientDynamoPersistenceTest.cs` — 3 tests
  - `tests/UnitTests/PatientRefresh.Worker/PatientServiceTests.cs` — 3 tests
  - `tests/UnitTests/DynamoKeyServiceTest.cs` — 2 tests
  - `tests/IntegrationTests/FirehoseClientWrapperIntegrationTests.cs`, `tests/UnitTests/FirehoseClientWrapperTest.cs`, `tests/UnitTests/GuidGeneratorTest.cs`, `tests/UnitTests/PatientNamespaceContractTests.cs` — 1 test each
  - `monolithInvestigationScripts/BitmaskDecode.cs` — 1 `[Test]`-annotated developer script, no assertions

## 2026-08-21 — initial mapping: `Zocdoc/legal-agreement` @ fdc9ad0

Scope: whole repo, branch `main`. Granularity: one row per test method.

- 8 test files mapped, 52 test methods total.
  - `tests/LegalAgreement.Web.ApiTests/PracticeUserAgreementApiTests.cs` — 28 tests
  - `tests/LegalAgreement.IntegrationTests/PracticeUserAgreementDynamoPersistenceTests.cs` — 10 tests
  - `tests/LegalAgreement.Web.UnitTests/PracticeUserAgreementServiceTests.cs` — 8 tests
  - `tests/LegalAgreement.Web.UnitTests/ConversionExtensionsTests.cs` — 2 tests
  - `tests/*/ExampleTests.cs` (×4) — 4 scaffold placeholders, no product coverage

## 2026-08-21 — restructure

- Moved `sandbox-auth-test-mapping.md` → `auth/sandbox-test-mapping.md`; mappings are now grouped in a per-team directory. No rows changed.
- `README.md` index rewritten to track every Auth-owned repo, not just the sandbox suite.

## 2026-08-21 — initial mapping: `Zocdoc/sandbox` @ 89a501e

Scope: `playwright/BU/Infrastructure/Auth` (Infrastructure / Auth team, per `OWNERSHIP.md`), branch `main`.

- 6 test files mapped, 24 tests total.
  - `Flows/password-recovery-flow.spec.ts` — 4 tests
  - `Flows/patient-signin-flow.spec.ts` — 5 tests
  - `Flows/provider-signin-flow.spec.ts` — 2 tests
  - `Pages/create-user-page.spec.ts` — 2 tests
  - `Pages/forgot-password-page.spec.ts` — 5 tests
  - `Pages/signin-page.spec.ts` — 6 tests
