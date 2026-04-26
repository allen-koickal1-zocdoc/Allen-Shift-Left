# zocdoc_web monolith — "Selenium" tests (mislabeled)

SHA: `32cbab30f3919c0bddb684eeb01151e58793e13c`
Repo: [Zocdoc/zocdoc_web](https://github.com/Zocdoc/zocdoc_web/tree/32cbab30f3919c0bddb684eeb01151e58793e13c)

## Headline correction

**There are zero true Selenium / WebDriver tests for Pterodactyl in the monolith.** v1 reported "89+ Selenium tests"; that claim is refuted.

What v1 saw under `SeleniumTests/SeleniumTests/Tests/` is a **misleadingly-named directory**. Every file inside:

- has **no `using OpenQA.Selenium`** import
- inherits from `BaseZocHttpApiTestFixture`
- exercises HTTP endpoints with no browser involvement

So they are HTTP API integration tests living in a directory that history named "SeleniumTests". They are still useful tests — but they are not browser-driven and should not be counted as Selenium coverage.

The classification was made by the deep-audit subagent that scanned each file's `using` statements and base class. The monolith was not cloned locally for this v2 pass; counts are quoted from the subagent run that produced the per-file numbers below.

## Total

| | |
|--|--|
| Test files | **13** |
| Total tests | **255** |

## Per-file inventory (corrected)

| File | Tests (v2) | v1 Claim | Δ |
|------|-----:|---------:|--:|
| [Tests/API/PracticeUserRolesPrivateApiTest.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/API/PracticeUserRolesPrivateApiTest.cs) | **72** | 29 | +43 |
| [Tests/ProviderDashboard/ProviderDashboardRbacControllerHttpTests.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/ProviderDashboard/ProviderDashboardRbacControllerHttpTests.cs) | **51** | 31 | +20 |
| [Tests/API/OrganizationUserApiTests.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/API/OrganizationUserApiTests.cs) | **34** | 1 | +33 |
| [Tests/API/PracticeUserManagementApiTests.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/API/PracticeUserManagementApiTests.cs) | **22** | 17 | +5 |
| [Tests/API/BulkProfileCompletionFgaAuthTests.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/API/BulkProfileCompletionFgaAuthTests.cs) | **19** | (missed) | +19 |
| [Tests/API/PracticeLocationsSettingsFgaAuthTests.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/API/PracticeLocationsSettingsFgaAuthTests.cs) | **15** | (missed) | +15 |
| [Tests/API/MultiPracticeProfileSettingsFgaAuthTests.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/API/MultiPracticeProfileSettingsFgaAuthTests.cs) | **9** | (missed) | +9 |
| [Tests/ProviderDashboard/PermissionCheckerFgaTest.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/ProviderDashboard/PermissionCheckerFgaTest.cs) | **7** | 2 | +5 |
| [Tests/API/UserManagementApiTests.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/API/UserManagementApiTests.cs) | **7** | 5 | +2 |
| [Tests/API/SelfSignUp/SelfSignUpFgaAuthTests.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/API/SelfSignUp/SelfSignUpFgaAuthTests.cs) | **6** | TBD | resolved |
| [Tests/ProviderConfigApiFgaAuthTests.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/ProviderConfigApiFgaAuthTests.cs) | **6** | 3 | +3 |
| [Tests/API/SelfSignUp/ProviderSelfSignUpFgaAuthTests.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/API/SelfSignUp/ProviderSelfSignUpFgaAuthTests.cs) | **5** | TBD | resolved |
| [Tests/API/PracticeUserPermissionsMultiProviderLoginLogic.cs](https://github.com/Zocdoc/zocdoc_web/blob/32cbab30f3919c0bddb684eeb01151e58793e13c/SeleniumTests/SeleniumTests/Tests/API/PracticeUserPermissionsMultiProviderLoginLogic.cs) | **2** | 1 | +1 |
| **Total** | **255** | 89+ | +166 |

## v1 corrections summary

- v1 classified all of these as Selenium → **REFUTED**. None are Selenium.
- v1 missed 3 entire FGA test files (`BulkProfileCompletionFgaAuthTests`, `PracticeLocationsSettingsFgaAuthTests`, `MultiPracticeProfileSettingsFgaAuthTests`) totalling **43 tests**.
- v1 systematically under-counted per-file (see Δ column).
- Total monolith Pterodactyl-area test count is **2.86x** what v1 reported (255 vs 89+).
