# Selenium Tests - Pterodactyl Team Features

## Summary

Selenium tests for Pterodactyl features are located in **zocdoc_web monolith** under `SeleniumTests/SeleniumTests/Tests/`.

---

## Test Inventory

### User & Practice User Management

| File | Description |
|------|-------------|
| `Tests/API/UserManagementApiTests.cs` | User management API tests |
| `Tests/API/PracticeUserManagementApiTests.cs` | Practice user management API tests |
| `Tests/API/OrganizationUserApiTests.cs` | Organization user API tests |

### Permissions & Authorization (FGA/RBAC)

| File | Description |
|------|-------------|
| `Tests/ProviderDashboard/PermissionCheckerFgaTest.cs` | FGA permission checker tests |
| `Tests/API/PracticeUserPermissionsMultiProviderLoginLogic.cs` | Multi-provider login permissions |
| `Tests/ProviderConfigApiFgaAuthTests.cs` | Provider config FGA auth tests |
| `Tests/API/BulkProfileCompletionFgaAuthTests.cs` | Bulk profile completion FGA auth |
| `Tests/API/SelfSignUp/SelfSignUpFgaAuthTests.cs` | Self sign-up FGA auth tests |
| `Tests/API/SelfSignUp/ProviderSelfSignUpFgaAuthTests.cs` | Provider self sign-up FGA auth |
| `Tests/ProviderDashboard/ProviderDashboardRbacControllerHttpTests.cs` | Provider dashboard RBAC tests |

### Role Management

| File | Description |
|------|-------------|
| `Tests/API/PracticeUserRolesPrivateApiTest.cs` | Practice user roles private API tests |

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
