# Test Coverage Analysis: practice-authorization-proxy

## Executive Summary

| Metric | Value |
|--------|-------|
| **Test Projects** | 5 |
| **Actual Test Files** | 4 (with real tests) |
| **Placeholder Tests** | 3 (trivial 1+1=2 tests) |
| **Total Test Methods** | 30 |
| **Unit Test Methods** | 19 |
| **API/Integration Test Methods** | 11 |
| **Estimated Code Coverage** | ~70-75% |
| **Key Gaps Identified** | 8 |
| **Obsolete/Trivial Tests** | 3 |

---

## Test Inventory

### 1. Unit Tests - AuthorizationServiceTests.cs

**File:** `tests/PracticeAuthorizationProxy.UnitTests/Service/AuthorizationServiceTests.cs`  
**Test Class:** `AuthorizationServiceTests`  
**Type:** Unit Test

| Test Method | What It Tests |
|-------------|---------------|
| `Verify_IsPracticeAuthorized_ReturnsExpectedResult_SendsMetricsCorrectly` | Practice authorization returns correct bool based on FGA result (parameterized for all EntityAuthorizationResult values) |
| `Verify_IsPracticeAuthorized_FgaAuthzServiceThrows_ReturnsExpectedResult_SendsMetricsCorrectly` | Practice authorization returns false when FGA service throws exception |
| `Verify_IsOrganizationAuthorized_ReturnsExpectedResult_SendsMetricsCorrectly` | Organization authorization returns correct bool based on FGA result (parameterized) |
| `Verify_IsOrganizationAuthorized_FgaAuthzServiceThrows_ReturnsExpectedResult_SendsMetricsCorrectly` | Organization authorization returns false when FGA service throws |
| `Verify_BatchIsPracticeAuthorized_ReturnsSuccess` | Batch practice authorization returns successful results |
| `Verify_BatchIsPracticeAuthorized_FgaAuthzServiceThrows_ThrowsGenericException` | Batch practice authorization propagates exceptions |
| `Verify_BatchIsPracticeAuthorized_FgaReturnsError_ThrowsCustomExceptionWithMessage` | Batch practice throws BatchPracticeAuthorizationException with correct message |
| `Verify_BatchIsPracticeAuthorized_FgaReturnsError_ThrowsCustomExceptionWithCorrectProperties` | Batch practice exception contains correct PracticeIds and error result |
| `Verify_BatchIsOrganizationAuthorized_ReturnsSuccess` | Batch organization authorization returns successful results |
| `Verify_BatchIsOrganizationAuthorized_FgaAuthzServiceThrows_ThrowsException` | Batch organization authorization propagates exceptions |
| `Verify_BatchIsOrganizationAuthorized_FgaReturnsError_ThrowsCustomExceptionWithMessage` | Batch organization throws BatchOrganizationAuthorizationException |
| `Verify_BatchIsOrganizationAuthorized_FgaReturnsError_ThrowsCustomExceptionWithCorrectProperties` | Batch organization exception contains correct OrganizationIds and error result |

### 2. Unit Tests - ConversionExtensionsTests.cs

**File:** `tests/PracticeAuthorizationProxy.Web.UnitTests/ConversionExtensionsTests.cs`  
**Test Class:** `ConversionExtensionsTests`  
**Type:** Unit Test

| Test Method | What It Tests |
|-------------|---------------|
| `VerifyAllPermissionsFiltersRepresentedInPracticeAuthorizationProxy` | All PermissionFilter enum values can be converted (parameterized) |
| `Verify_ToBatchPracticeResult_ConvertsSuccessfully` | EntityAuthorizationCheckResult list converts to BatchPracticeAuthorizationResult |
| `Verify_ToBatchOrganizationResult_ConvertsSuccessfully` | EntityAuthorizationCheckResult list converts to BatchOrganizationAuthorizationResult |
| `Verify_ToBatchPracticeResult_WithEmptyResults_ConvertsSuccessfully` | Empty list converts to empty BatchPracticeAuthorizationResult |
| `Verify_ToBatchOrganizationResult_WithEmptyResults_ConvertsSuccessfully` | Empty list converts to empty BatchOrganizationAuthorizationResult |

### 3. API Tests - PracticeAuthorizationTests.cs

**File:** `tests/PracticeAuthorizationProxy.Web.ApiTests/PracticeAuthorizationTests.cs`  
**Test Class:** `PracticeAuthorizationTests`  
**Type:** API/Integration Test

| Test Method | What It Tests |
|-------------|---------------|
| `IsPracticeAuthorized_GivenNotLoggedIn_ReturnsUnauthorized` | Returns 401 when no authentication |
| `IsPracticeAuthorized_GivenNonPracticeUser_ReturnsForbidden` | Returns 403 for patient/CSR users (2 test cases) |
| `IsPracticeAuthorized_GivenPracticeUser_ReturnsResponse` | Returns 200 with correct is_authorized for practice users (4 test cases) |
| `BatchIsPracticeAuthorized_GivenMoreThan50Practices_ReturnsBadRequest` | Returns 400 when >50 practice IDs |
| `BatchIsPracticeAuthorized_GivenExactly50Practices_ReturnsOK` | Returns 200 when exactly 50 practice IDs |

### 4. API Tests - OrganizationAuthorizationTests.cs

**File:** `tests/PracticeAuthorizationProxy.Web.ApiTests/OrganizationAuthorizationTests.cs`  
**Test Class:** `OrganizationAuthorizationTests`  
**Type:** API/Integration Test

| Test Method | What It Tests |
|-------------|---------------|
| `IsOrganizationAuthorized_GivenNotLoggedIn_ReturnsUnauthorized` | Returns 401 when no authentication |
| `IsOrganizationAuthorized_GivenNonPracticeUser_ReturnsForbidden` | Returns 403 for patient/CSR users (2 test cases) |
| `IsOrganizationAuthorized_GivenPracticeUser_ReturnsResponse` | Returns 200 with correct is_authorized for practice users (4 test cases) |
| `BatchIsOrganizationAuthorized_GivenMoreThan50Organizations_ReturnsBadRequest` | Returns 400 when >50 organization IDs |
| `BatchIsOrganizationAuthorized_GivenExactly50Organizations_ReturnsOK` | Returns 200 when exactly 50 organization IDs |

---

## Gap Analysis

### 1. AuthorizationImpl (Controller Layer) - NO UNIT TESTS

**File:** `src/PracticeAuthorizationProxy.Web/AuthorizationImpl.cs`  
**Lines:** 184  
**Current Coverage:** API tests only (no unit tests)

**Missing Unit Tests:**

| Method | Missing Test Scenarios |
|--------|------------------------|
| `ParsePracticePermissionString` (private) | Invalid permission string handling |
| `ParseOrganizationPermissionString` (private) | Invalid permission string handling |
| `IsPracticeAuthorized` | Bad request (400) when invalid permission string passed |
| `IsOrganizationAuthorized` | Bad request (400) when invalid permission string passed |
| `BatchIsPracticeAuthorized` | Bad request (400) when invalid permission string passed |
| `BatchIsOrganizationAuthorized` | Bad request (400) when invalid permission string passed |

### 2. Missing API Test Scenarios

| Endpoint | Missing Test |
|----------|--------------|
| `GET /practice/{id}/is_authorized` | Empty permissions array handling |
| `GET /practice/{id}/is_authorized` | Invalid PermissionFilter value |
| `GET /practice/{id}/is_authorized` | Malformed practice_id format |
| `GET /organization/{id}/is_authorized` | Empty permissions array handling |
| `GET /organization/{id}/is_authorized` | Invalid PermissionFilter value |
| `PUT /practice/is_authorized~batchGet` | Empty practice_ids array |
| `PUT /practice/is_authorized~batchGet` | Empty practice_permissions array |
| `PUT /practice/is_authorized~batchGet` | Invalid permission string in request |
| `PUT /practice/is_authorized~batchGet` | FGA service error (500 response) |
| `PUT /organization/is_authorized~batchGet` | Empty organization_ids array |
| `PUT /organization/is_authorized~batchGet` | Empty organization_permissions array |
| `PUT /organization/is_authorized~batchGet` | Invalid permission string in request |
| `PUT /organization/is_authorized~batchGet` | FGA service error (500 response) |

### 3. Exception Classes - NO TESTS

**File:** `src/PracticeAuthorizationProxy/AuthorizationExceptions.cs`

| Class | Missing Tests |
|-------|---------------|
| `BatchPracticeAuthorizationException` | Constructor parameter validation, message format, property getters |
| `BatchOrganizationAuthorizationException` | Constructor parameter validation, message format, property getters |

### 4. ConversionExtensions - Partial Coverage

**File:** `src/PracticeAuthorizationProxy.Web/ConversionExtensions.cs`

| Method | Missing Tests |
|--------|---------------|
| `WebToCore` | Invalid/unknown PermissionFilter value throws ArgumentOutOfRangeException |
| `ToBatchPracticeResult` | Null input handling |
| `ToBatchOrganizationResult` | Null input handling |

### 5. SetupExtensions - NO TESTS

**File:** `src/PracticeAuthorizationProxy/SetupExtensions.cs`

| Method | Missing Tests |
|--------|---------------|
| `AddCommonAwsServices` | AWS service registration, LocalStack configuration |

### 6. FakeAuthorizationService - NO TESTS

**File:** `src/PracticeAuthorizationProxy.Web.Fake/Services/FakeAuthorizationService.cs`

The fake service is used in integration tests but has no unit tests to verify its behavior is consistent with the real implementation.

### 7. Startup Configuration - NO TESTS

**File:** `src/PracticeAuthorizationProxy.Web/Startup.cs`

| Missing Tests |
|---------------|
| Authorization policy configuration |
| Service registration |
| Middleware configuration |

### 8. Missing Edge Case Tests

| Scenario | Impact |
|----------|--------|
| Concurrent authorization requests | Potential race conditions |
| Very long permission lists | Performance degradation |
| Special characters in practice_id/organization_id | Input validation |
| Case sensitivity of permission strings | Inconsistent behavior |
| Null/empty authorization header | 401 vs 400 response |

---

## Obsolete/Potentially Problematic Tests

### 1. Token Placeholder Tests (3 instances)

```csharp
[Test]
public void TokenEmptyTest()
{
    (1 + 1).Should().Be(2);
}
```

**Locations:**
- `PracticeAuthorizationProxy.UnitTests/ExampleTests.cs`
- `PracticeAuthorizationProxy.IntegrationTests/ExampleTests.cs`
- `PracticeAuthorizationProxy.Web.IntegrationTests/ExampleTests.cs`

**Issue:** These are trivial placeholder tests that provide no value. They exist only to satisfy build requirements that at least one test exists in each test project.

**Recommendation:** Remove these files and add real tests, or document why these test projects exist without real tests.

### 2. Duplicate Test Cases in AllowedTestCases

Both `PracticeAuthorizationTests` and `OrganizationAuthorizationTests` have test case sources that appear to have duplicates - calling the same method with the same parameters using different syntax.

---

## Recommendations

### High Priority

1. **Add unit tests for `AuthorizationImpl`** - The controller layer has significant logic for permission string parsing and error handling that is only tested through API tests. Unit tests would provide faster feedback and more targeted coverage.

2. **Add tests for invalid permission strings** - The `ParsePracticePermissionString` and `ParseOrganizationPermissionString` methods handle invalid input by throwing `ArgumentException`, but this path has no dedicated tests.

3. **Test batch endpoint error scenarios** - The batch endpoints can return 500 errors when FGA fails, but this is only tested at the unit level, not at the API level.

### Medium Priority

4. **Remove placeholder tests** - Delete the three `TokenEmptyTest` instances and either add real tests or remove the empty test projects.

5. **Add null input handling tests** - The conversion extensions don't have tests for null inputs which could cause `NullReferenceException`.

6. **Test exception classes** - While simple, having tests for the custom exception classes ensures the error messages and properties are correct.

### Low Priority

7. **Add integration tests for SetupExtensions** - Verify AWS services are properly registered.

8. **Document or remove duplicate test cases** - Review the `AllowedTestCases` in both API test files for potential duplication.

9. **Add performance/load tests** - No tests exist for concurrent request handling or large batch sizes (near the 50 item limit).

---

*Generated: 2026-04-09*
