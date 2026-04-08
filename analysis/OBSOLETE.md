# Potentially Obsolete Tests

## Tests to Remove

### practice-authorization-proxy

| Test File | Test Name | Reason | Action |
|-----------|-----------|--------|--------|
| `PracticeAuthorizationProxy.UnitTests/ExampleTests.cs` | `TokenEmptyTest` | Placeholder test: `(1 + 1).Should().Be(2)` | **DELETE** |
| `PracticeAuthorizationProxy.IntegrationTests/ExampleTests.cs` | `TokenEmptyTest` | Placeholder test: `(1 + 1).Should().Be(2)` | **DELETE** |
| `PracticeAuthorizationProxy.Web.IntegrationTests/ExampleTests.cs` | `TokenEmptyTest` | Placeholder test: `(1 + 1).Should().Be(2)` | **DELETE** |

**Impact:** These 3 tests provide zero value and inflate test counts. The test projects may need at least one real test added after deletion.

---

### provider-grouping

| Test File | Test Name | Reason | Action |
|-----------|-----------|--------|--------|
| `StrategicLambdaTests.cs` | `Verify_Handler_Processes_Correctly` | Marked `[Ignore("Test Not Completed")]` | **Complete or DELETE** |
| `OrganizationTests.cs` | `GetDeleteTransactionItems_ThrowsNotImplementedException` | Tests that a method throws NotImplementedException - indicates dead code | **Investigate** - remove test or implement method |

---

### provider-join-service

| Test File | Test Name | Reason | Action |
|-----------|-----------|--------|--------|
| `FunctionTest.cs` | `TestReturnsId` | Trivial assertion - simply checks handler returns input ID | **Enhance** - add meaningful assertions |

---

## Tests to Update/Review

### practice-authorization-proxy

| Test File | Issue | Recommendation |
|-----------|-------|----------------|
| `PracticeAuthorizationTests.cs` | Duplicate test cases in `AllowedTestCases` - same method called with same params in different syntax | Review and deduplicate |
| `OrganizationAuthorizationTests.cs` | Same duplication pattern | Review and deduplicate |

---

### practice-user-permissions

| Test File | Issue | Recommendation |
|-----------|-------|----------------|
| `FakeSqsEvents` test fixtures | Contains hardcoded malformed event samples | Review if still needed or update |
| `AuthorizationRequirementTestController` tests | Test controller for authorization testing | Verify if controller is still active |
| Tests using `[Retry(n)]` attribute | Integration tests with retries may mask flaky behavior | Investigate root cause of flakiness |
| `TupleAuditServiceTests.cs` | 61 tests in one file - maintainability issue | Consider splitting |

---

### provider-join-service

| Test File | Issue | Recommendation |
|-----------|-------|----------------|
| `SelfSignupLeadStatusBuilderTest.cs` | 70+ test cases only validate invalid combinations - no positive test cases | Add positive test cases |
| `LocalStackDemoRequestTests.cs` | Hardcoded validation (`PracticeName_CharCount_GreaterThan_50`) may have changed | Verify current business rules |
| Authorization handler tests | `CsrAuthorizationHandlerTests`, `PracticeAuthorizationHandlerTests`, `SelfSignUpPracticeAuthorizationHandlerTests` have similar patterns | Consolidate with shared base class |
| `ValidationExtensionsTests` + `RequestValidatorTest` | Some email/phone validation overlap | Review for duplication |

---

## Summary

| Category | Count | Action |
|----------|-------|--------|
| **Remove immediately** | 3 | Placeholder tests in PAP |
| **Complete or remove** | 2 | IGNORED test, NotImplemented test |
| **Enhance** | 1 | Trivial lambda test |
| **Review for duplication** | 6 | Various duplicate/overlapping tests |
| **Review for flakiness** | ~5 | Tests with Retry attribute |
| **Split for maintainability** | 1 | Large test file |

---

## Quick Wins

1. **Delete 3 placeholder tests** - 5 minutes, immediate improvement
2. **Address IGNORED test** - Either complete it or delete the skeleton
3. **Enhance trivial lambda test** - Add meaningful assertions

---

*Generated: 2026-04-09*
