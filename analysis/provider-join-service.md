# Test Coverage Analysis: provider-join-service

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Source Files** | 121 C# files |
| **Total Test Files** | 55 test files |
| **Integration Tests** | 12 files |
| **Unit Tests (API)** | 21 files |
| **Unit Tests (Infrastructure)** | 19 files |
| **Lambda Tests** | 3 files |
| **Estimated Line Coverage** | ~60-70% |

**Assessment:** Decent coverage for core functionality but critical gaps in StepFunctionService, CreatePracticeDtoFactory, and concurrent access scenarios.

---

## Test Inventory

### Integration Tests (SelfSignup.Integration.Tests)

| File | Tests | What It Tests |
|------|-------|---------------|
| `InsuranceWizardTest.cs` | 26 | Insurance onboarding wizard GET/PUT endpoints, authorization, validation, status transitions |
| `LocalStackDemoRequestTests.cs` | 4 | Demo request lead creation, validation (phone, email, practice name length) |
| `LocalStackDynamoDbTests.cs` | 4 | DynamoDB operations: expiration date removal, lead status persistence, marketing channel |
| `PostSubmissionUpdatesTest.cs` | 2 | Step function trigger endpoint success/not found cases |
| `LeadRetrievalTest.cs` | 12 | Lead data retrieval by ID and practice ID, authorization (practice/selfsignup/csr) |
| `CcpaTest.cs` | 2 | Gong data deletion request auth and success |
| `ClaimProfileTest.cs` | 2 | Claim profile removal case creation |
| `UserAgreementTests.cs` | 3 | User agreement PDF retrieval from monolith |
| `PricingTest.cs` | 2 | Signup portal pricing retrieval |
| `SignUpFlowTest.cs` | 10 | Full signup flow, lead creation, Salesforce sync, status transitions |
| `AccountCreationTests.cs` | 15 | Account creation, email confirmation, onboarding practice upsert, rate limiting |

### Unit Tests - API Layer (SelfSignup.Api.Tests.Unit)

| File | Tests | What It Tests |
|------|-------|---------------|
| `ProviderJoinServiceReadWriteDataRequirementHandlerTests.cs` | 14 | PJS read/write data authorization handler |
| `RequestDemoImplTest.cs` | 5 | Demo request creation validation and success |
| `PricingImplTest.cs` | 2 | Pricing endpoint response handling |
| `AccountCreationImplTest.cs` | ~20 | Account creation endpoint error handling |
| `SelfSignUpPracticeAuthorizationHandlerTests.cs` | 8 | SelfSignUp practice auth handler |
| `CsrAuthorizationHandlerTests.cs` | 2 | CSR authorization handler |
| `PracticeAuthorizationHandlerTests.cs` | 8 | Practice authorization handler |
| `LeadHelperTests.cs` | 14 | Test lead detection (by email, last name, practice name) |
| `ValidationExtensionsTests.cs` | 22 | Email, phone, zip code validation |
| `SelfSignupLeadStatusBuilderTest.cs` | 70+ | Lead state/view validation combinations |
| `LeadSubmissionImplTest.cs` | ~15 | Lead submission to Salesforce |
| `InsuranceWizardImplTest.cs` | ~20 | Insurance wizard endpoint logic |
| `LeadRetrievalImplTest.cs` | ~25 | Lead retrieval endpoint logic |
| `LeadGenerationImplTest.cs` | ~15 | Lead generation/upsert logic |
| `UpdateLeadStatusPostSubmissionImplTest.cs` | ~15 | Post-submission lead status updates |
| `RequestValidatorTest.cs` | ~15 | Request validation logic |
| `CcpaImplTest.cs` | ~3 | CCPA endpoint implementation |
| `ClaimProfileImplTest.cs` | ~5 | Claim profile implementation |
| `UserAgreementControllerTest.cs` | ~4 | User agreement controller |
| `ExtensionHelperTests.cs` | ~6 | Extension helper methods |
| `IdentityHelperTests.cs` | ~5 | Identity helper methods |

### Unit Tests - Infrastructure Layer (SelfSignup.Infrastructure.Tests.Unit)

| File | Tests | What It Tests |
|------|-------|---------------|
| `LocationHelperTests.cs` | 5 | Zip code to state code mapping |
| `DdbRepositoryTests.cs` | 4 | DynamoDB CRUD operations |
| `EnumExtensionsTests.cs` | 3 | Case-insensitive enum conversion |
| `CollectionExtensionsTests.cs` | 3 | List to semicolon-delimited string |
| `LeadDdbDtoFactoryTest.cs` | 3 | Lead DTO creation from request |
| `UserAgreementApiTests.cs` | 3 | Monolith user agreement API calls |
| `FoundationalSupplementalMappingServiceTests.cs` | 4 | Foundational/supplemental specialty and location checks |
| `LeadsServiceTests.cs` | 14 | Lead service: get, submit status, Salesforce sync |
| `SignupPortalServiceTest.cs` | 10 | Signup portal lead upsert logic |
| `SalesforceRepositoryTest.cs` | 5 | Salesforce lead queries |
| `SignUpServiceTest.cs` | 15 | SignUp service: user agreement, execution ARN, status updates |
| `LeadSalesforceServiceTests.cs` | ~25 | Salesforce lead creation/update |
| `SvcToSvcAuthOnboardTaskFrameworkApiTests.cs` | 4 | Service-to-service onboarding API |
| `ProviderOnboardTaskFrameworkApiTests.cs` | 5 | Provider onboarding API calls |
| `ClaimProfileServiceTests.cs` | 2 | Claim profile Salesforce case creation |
| `CcpaServiceTests.cs` | 1 | Gong deletion request |
| `InsuranceOnboardingServiceTest.cs` | 13 | Insurance onboarding entry creation, eligibility, save/get |
| `PricingServiceTests.cs` | 6 | Pricing calculation and specialty lookup |
| `AccountCreationServiceTest.cs` | ~20 | Account creation service logic |

### Lambda Tests (ProviderJoinService.AbandonmentLambda.Tests)

| File | Tests | What It Tests |
|------|-------|---------------|
| `FunctionTest.cs` | 1 | Basic lambda handler returns ID |
| `FunctionalTests/FunctionTest.cs` | 2 | Lambda with fake client: success logging, error logging |

---

## Gap Analysis

### 1. Services Without Tests

| Service | File Path | Gap |
|---------|-----------|-----|
| **StepFunctionService** | `src/SelfSignup.Infrastructure/Services/StepFunctionService/StepFunctionService.cs` | **No unit tests. Critical for abandonment flow.** |
| **CreatePracticeDtoFactory** | `src/SelfSignup.Infrastructure/Services/PracticeAndProviderCreation/CreatePracticeDtoFactory.cs` | No unit tests |
| **MonolithApi (base class)** | `src/SelfSignup.Infrastructure/Services/Monolith/MonolithApi.cs` | Abstract class, only partial coverage via derived classes |

### 2. Missing Edge Case Coverage

| Area | Missing Tests |
|------|---------------|
| **DdbRepository** | Tests for `shouldIgnoreNullValues=false`, concurrent updates |
| **LeadSalesforceService** | Tests for duplicate lead handling, retry logic |
| **InsuranceWizardImpl** | Tests for partial data saves, concurrent updates |
| **AccountCreationService** | Tests for race conditions in email verification caching |
| **StepFunctionService** | All scenarios: stop execution failure, start execution timeout |

### 3. Missing Integration Tests

| Endpoint/Flow | Current Coverage | Gap |
|---------------|------------------|-----|
| Error recovery flows | Minimal | No tests for retry after transient failures |
| Concurrent request handling | None | No tests for race conditions |
| Salesforce API failures | Minimal | More edge cases needed |

### 4. API Endpoints Missing Test Coverage

| Endpoint | Controller/Impl | Gap |
|----------|-----------------|-----|
| Insurance wizard edge cases | InsuranceWizardImpl | Status transitions under load |
| Lead generation concurrent updates | LeadGenerationImpl | Same lead ID simultaneous updates |

---

## Potentially Obsolete Tests

### 1. Tests That May Be Outdated

| Test File | Test Name | Concern |
|-----------|-----------|---------|
| `SelfSignupLeadStatusBuilderTest.cs` | All 70+ test cases | Tests only validate state/view combinations are invalid - no positive test cases for valid combinations |
| `LocalStackDemoRequestTests.cs` | `CreateSignupPortalRequestDemoLead_Should_Return_BadRequest_When_PracticeName_CharCount_GreaterThan_50` | Hardcoded validation may have changed |

### 2. Tests with Trivial Assertions

| Test File | Test Name | Concern |
|-----------|-----------|---------|
| `FunctionTest.cs` (Lambda) | `TestReturnsId` | Simply checks handler returns input ID - minimal value |

### 3. Duplicate Test Coverage

| Area | Files | Overlap |
|------|-------|---------|
| Authorization handlers | CsrAuthorizationHandlerTests, PracticeAuthorizationHandlerTests, SelfSignUpPracticeAuthorizationHandlerTests | Similar patterns could be consolidated with shared base |
| Validation | ValidationExtensionsTests + RequestValidatorTest | Some email/phone validation overlap |

---

## Recommendations

### High Priority

1. **Add StepFunctionService unit tests** - Critical for abandonment flow reliability

2. **Add CreatePracticeDtoFactory tests** - Core business logic untested

3. **Add concurrent access tests** - No tests for race conditions in lead updates

4. **Add Salesforce failure recovery tests** - Ensure graceful degradation

### Medium Priority

5. **Consolidate authorization handler tests** - Reduce duplication with shared test base

6. **Add positive test cases to SelfSignupLeadStatusBuilderTest** - Currently only tests invalid combinations

7. **Add timeout and retry tests** - External service resilience

8. **Improve Lambda tests** - Current tests are minimal

### Low Priority

9. **Add enum serialization edge case tests** - For EnumExtensions

10. **Add collection extension edge case tests** - Empty/null list handling

11. **Remove or enhance trivial Lambda test** - TestReturnsId provides minimal value

---

*Generated: 2026-04-09*
