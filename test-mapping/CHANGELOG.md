# Test Mapping Changelog

Identity key for a row: `<repo-relative-path>::<MethodName>[ (CaseName)]`.

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
