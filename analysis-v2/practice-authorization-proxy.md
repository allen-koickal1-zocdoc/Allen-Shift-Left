# practice-authorization-proxy

SHA: `e8c72baef19e1031dd0c753eb019d67a2d36aaf2`
Repo: [Zocdoc/practice-authorization-proxy](https://github.com/Zocdoc/practice-authorization-proxy/tree/e8c72baef19e1031dd0c753eb019d67a2d36aaf2)

## Headline

| | |
|--|--|
| Test files | **7** |
| Total tests | **26** |
| Source LOC | 733 |
| Test LOC | 858 |
| Placeholder `1+1==2` tests | **3** |
| Real tests after subtracting placeholders | 23 |

## Per-file inventory

| File | Tests | Notes |
|------|-----:|-------|
| [tests/PracticeAuthorizationProxy.UnitTests/Service/AuthorizationServiceTests.cs](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.UnitTests/Service/AuthorizationServiceTests.cs) | 12 | Unit tests for the `AuthorizationService` |
| [tests/PracticeAuthorizationProxy.Web.UnitTests/ConversionExtensionsTests.cs](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.Web.UnitTests/ConversionExtensionsTests.cs) | 5 | DTO conversion extensions |
| [tests/PracticeAuthorizationProxy.Web.ApiTests/PracticeAuthorizationTests.cs](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.Web.ApiTests/PracticeAuthorizationTests.cs) | 3 | API-level tests |
| [tests/PracticeAuthorizationProxy.Web.ApiTests/OrganizationAuthorizationTests.cs](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.Web.ApiTests/OrganizationAuthorizationTests.cs) | 3 | API-level tests |
| [tests/PracticeAuthorizationProxy.UnitTests/ExampleTests.cs#L8](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.UnitTests/ExampleTests.cs#L8) | 1 | **Placeholder** `(1 + 1).Should().Be(2);` |
| [tests/PracticeAuthorizationProxy.IntegrationTests/ExampleTests.cs#L8](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.IntegrationTests/ExampleTests.cs#L8) | 1 | **Placeholder** `(1 + 1).Should().Be(2);` |
| [tests/PracticeAuthorizationProxy.Web.IntegrationTests/ExampleTests.cs#L8](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.Web.IntegrationTests/ExampleTests.cs#L8) | 1 | **Placeholder** `(1 + 1).Should().Be(2);` |
| **Total** | **26** | |

## Critical gap: `AuthorizationImpl` has no unit tests

| Item | Detail |
|------|--------|
| File | [src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs) |
| Lines | **183** (v1 said 184) |
| Public methods | `IsPracticeAuthorized` ([L27](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs#L27)), `IsOrganizationAuthorized` ([L66](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs#L66)), `BatchIsPracticeAuthorized` ([L102](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs#L102)), `BatchIsOrganizationAuthorized` ([L136](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs#L136)) |
| Direct unit tests | `grep -rln "AuthorizationImpl" tests/` → no results. Indirectly covered only by `PracticeAuthorizationTests` and `OrganizationAuthorizationTests` (3 + 3 API tests). |

## v1 corrections

| v1 said | v2 verified |
|---------|-------------|
| 30 tests across 4 files | **26 tests across 7 files** |
| 3 placeholder `1+1==2` tests | **CONFIRMED** |
| `AuthorizationImpl` 184 LOC, 0 unit tests | 183 LOC, 0 unit tests confirmed |
