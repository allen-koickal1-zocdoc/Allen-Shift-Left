# zocdoc_web Monolith — Pterodactyl HTTP API Tests

**SHA:** `35bc2f17109578b3ba13dbd543a4300d2c20bf3c`
**Location:** `SeleniumTests/SeleniumTests/Tests/` (directory name is misleading — see classification).

## The v2 counting error

v2 reported 255 tests across 13 files and noted those numbers came from "a deep-audit subagent" that was **never grepped**. v3 grepped every file and found two problems:

1. **The custom `[CiTest]` attribute.** Zocdoc's monolith uses `[CiTest]` as its per-test marker, *not* NUnit's `[Test]`. Many of these files contain **zero** `[Test]` attributes and dozens of `[CiTest]`. v2's `grep -cE "[Test]|[TestCase("` was blind to them.
2. **14 missing files.** v2 listed 13 Pterodactyl-relevant files; v3 found **27** under the same directory.

## Per-file counts (current HEAD)

| File | Base fixture | `OpenQA.Selenium`? | `[CiTest]` | `[Test]` | `[TestCase]` |
|------|--------------|:------------------:|----------:|--------:|------------:|
| PracticeUserRolesPrivateApiTest | BaseZocHttpApiTestFixture | No | 66 | 6 | 22 |
| ProviderDashboardRbacControllerHttpTests | DashboardTestBase → BaseZocHttpApiTestFixture | No | 64 | 0 | 19 |
| ProviderSelfSignUpControllerTests | BaseZocHttpApiTestFixture | No | 50 | 0 | 0 |
| OrganizationUserApiTests | BaseZocHttpApiTestFixture | No | 48 | 0 | 0 |
| SelfSignUpControllerTests | BaseZocHttpApiTestFixture | No | 28 | 0 | 6 |
| ProviderConfigApiControllerTest | BaseZocHttpApiTestFixture | No | 22 | 6 | 8 |
| PracticeUserManagementApiTests | BaseZocHttpApiTestFixture | No | 18 | 1 | 15 |
| ProfessionalProfileSettingsFgaAuthTests | ProfessionalProfileSettingsApiTestBase → BaseZocHttpApiTestFixture | No | 15 | 0 | 0 |
| PracticeLocationsSettingsFgaAuthTests | BaseZocHttpApiTestFixture | No | 13 | 0 | 0 |
| MultiPracticeProfileSettingsFgaAuthTests | BaseZocHttpApiTestFixture | No | 12 | 0 | 0 |
| CalendarAvailabilityFgaAuthTests | BaseZocHttpApiTestFixture | No | 8 | 0 | 0 |
| PermissionCheckerFgaTest | BaseZocHttpApiTestFixture | No | 8 | 0 | 0 |
| ProviderVisitReasonFgaAuthTests | BaseZocHttpApiTestFixture | No | 8 | 0 | 8 |
| UserManagementApiTests | BaseZocHttpApiTestFixture | No | 7 | 0 | 4 |
| BulkProfileCompletionFgaAuthTests | BaseZocHttpApiTestFixture | No | 6 | 0 | 4 |
| ProfessionalProfileSettingsApiTestsSelfSignUp | ProfessionalProfileSettingsApiTestBase → BaseZocHttpApiTestFixture | No | 6 | 0 | 0 |
| ProviderConfigApiFgaAuthTests | BaseZocHttpApiTestFixture | No | 6 | 0 | 0 |
| SelfSignUpFgaAuthTests | BaseZocHttpApiTestFixture | No | 6 | 0 | 0 |
| ProviderNotificationsFgaAuthTests | BaseZocHttpApiTestFixture | No | 5 | 0 | 4 |
| ProviderSelfSignUpFgaAuthTests | BaseZocHttpApiTestFixture | No | 5 | 0 | 0 |
| ProviderSelfSignUpPrivateControllerTests | BaseZocHttpApiTestFixture | No | 5 | 0 | 0 |
| SelfSignUpUserProviderSettingsPageAccessHttpTests | BaseZocHttpApiTestFixture | No | 5 | 0 | 0 |
| ReminderDashboardFgaIntegrationTests | BaseZocHttpApiTestFixture | No | 0 | 3 | 0 |
| CalendarAppointmentsFgaIntegrationTests | BaseZocHttpApiTestFixture | No | 0 | 2 | 8 |
| FeeAggregationFgaIntegrationTests | BaseZocHttpApiTestFixture | No | 2 | 0 | 0 |
| RemindersFgaIntegrationTests | BaseZocHttpApiTestFixture | No | 0 | 1 | 4 |
| PracticeUserPermissionsMultiProviderLoginLogic | BaseZocHttpApiTestFixture | No | 1 | 0 | 0 |

## Totals

- **27 files.**
- **433 test methods** = 414 `[CiTest]` + 19 `[Test]`.
- **535** if `[TestCase(...)]` rows (102) are counted as individual cases the way v2 counts NUnit cases.
- An additional **14 `[TestCaseSource]`** attributes expand to an unknown number of rows at runtime (not counted).

## Classification: zero real Selenium tests — CONFIRMED

All 27 files have **0** `OpenQA.Selenium` references. Base-class chain:

- 24 files directly extend `BaseZocHttpApiTestFixture`.
- 2 extend `ProfessionalProfileSettingsApiTestBase : BaseZocHttpApiTestFixture`.
- 1 extends `DashboardTestBase : BaseZocHttpApiTestFixture`.
- `BaseZocHttpApiTestFixture` is `public abstract class BaseZocHttpApiTestFixture` (no base, 0 Selenium refs). It holds an `ISeleniumHttpClient` field, but that is a plain HTTP-client interface — *not* the WebDriver.

The `SeleniumTests/` directory name is historical; the contents are HTTP API tests.

## New files vs v2 (all HTTP API, 0 Selenium)

FeeAggregationFgaIntegrationTests, ProfessionalProfileSettingsApiTestsSelfSignUp, ProfessionalProfileSettingsFgaAuthTests, CalendarAppointmentsFgaIntegrationTests, RemindersFgaIntegrationTests, ProviderSelfSignUpControllerTests, ProviderSelfSignUpPrivateControllerTests, SelfSignUpControllerTests, ReminderDashboardFgaIntegrationTests, CalendarAvailabilityFgaAuthTests, ProviderNotificationsFgaAuthTests, ProviderConfigApiControllerTest, ProviderVisitReasonFgaAuthTests, SelfSignUpUserProviderSettingsPageAccessHttpTests.

No v2 file disappeared.
