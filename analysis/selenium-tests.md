# Selenium Tests - Pterodactyl Team Features

## Summary

**Total: 89+ tests** in zocdoc_web monolith under `SeleniumTests/SeleniumTests/Tests/`

---

## Test Inventory

### User & Practice User Management (23 tests)

| File | Tests | Description |
|------|-------|-------------|
| `Tests/API/UserManagementApiTests.cs` | 5 | User management API tests |
| `Tests/API/PracticeUserManagementApiTests.cs` | 17 | Practice user management API tests |
| `Tests/API/OrganizationUserApiTests.cs` | 1 | Organization user API tests |

### Permissions & Authorization (FGA/RBAC) (37 tests)

| File | Tests | Description |
|------|-------|-------------|
| `Tests/ProviderDashboard/PermissionCheckerFgaTest.cs` | 2 | FGA permission checker tests |
| `Tests/API/PracticeUserPermissionsMultiProviderLoginLogic.cs` | 1 | Multi-provider login permissions |
| `Tests/ProviderConfigApiFgaAuthTests.cs` | 3 | Provider config FGA auth tests |
| `Tests/ProviderDashboard/ProviderDashboardRbacControllerHttpTests.cs` | 31 | Provider dashboard RBAC tests |
| `Tests/API/SelfSignUp/SelfSignUpFgaAuthTests.cs` | TBD | Self sign-up FGA auth tests |
| `Tests/API/SelfSignUp/ProviderSelfSignUpFgaAuthTests.cs` | TBD | Provider self sign-up FGA auth |

### Role Management (29 tests)

| File | Tests | Description |
|------|-------|-------------|
| `Tests/API/PracticeUserRolesPrivateApiTest.cs` | 29 | Practice user roles private API tests |

### Practice Authorization

| File | Description |
|------|-------------|
| `Tests/API/PracticeProfileSettingsApiTests.cs` | Practice profile settings (uses PracticeAuthorization) |
| `Tests/API/Provider/CalendarPopulatorAuthorizationTests.cs` | Calendar populator authorization tests |

### Authentication (Related)

| File | Description |
|------|-------------|
| `Tests/API/AuthenticationApiV2Tests.cs` | Authentication API v2 tests |
| `Tests/Auth/ZdJwtV2CookieHttpTests.cs` | JWT v2 cookie tests |
| `Tests/MultiProvider/MultiProviderTests.cs` | Multi-provider tests |

### Supporting Infrastructure

| File | Description |
|------|-------------|
| `Seeding/ProfessionalSeeding.cs` | Test data seeding for professionals/users |
| `ZocUtility/SeleniumCookie.cs` | Cookie utilities for permissions |
| `TestingBackdoor.Client/ProviderGroupingHelper.cs` | Provider grouping test helper |

---

## Location

All tests in: `Zocdoc/zocdoc_web/SeleniumTests/SeleniumTests/Tests/`

---

## Gap Analysis

These Selenium tests need further analysis to determine:
1. Which specific test methods exist in each file
2. Current pass/fail status
3. Whether they're actively maintained
4. Coverage gaps compared to Cypress tests

---

*Generated: 2026-04-09*
