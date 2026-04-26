# provider-join-service

SHA: `cec322f4fe6d69011b6ba74ae097cbaea59ea030`
Repo: [Zocdoc/provider-join-service](https://github.com/Zocdoc/provider-join-service/tree/cec322f4fe6d69011b6ba74ae097cbaea59ea030)

## Headline

| | |
|--|--|
| Test files (with at least one `[Test]` or `[TestCase(`) | **54** |
| Total tests | **634** |
| Source LOC | 8,115 |
| Test LOC | 11,563 |
| Test/Source ratio | 1.42x |

## Tests by project

| Project | Tests |
|---------|-----:|
| `SelfSignup.Api.Tests.Unit` | 342 |
| `SelfSignup.Infrastructure.Tests.Unit` | 196 |
| `SelfSignup.Integration.Tests` | 93 |
| `ProviderJoinService.AbandonmentLambda.Tests` | 3 |
| `SelfSignup.Tests.Unit` | **0 (empty)** |
| **Total** | **634** |

## Per-file inventory

### SelfSignup.Api.Tests.Unit (342)
| File | Tests |
|------|-----:|
| [tests/SelfSignup.Api.Tests.Unit/SelfSignupLeadStatusBuilderTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/SelfSignupLeadStatusBuilderTest.cs) | 73 |
| [tests/SelfSignup.Api.Tests.Unit/LeadRetrievalImplTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/LeadRetrievalImplTest.cs) | 42 |
| [tests/SelfSignup.Api.Tests.Unit/LeadHelperTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/LeadHelperTests.cs) | 30 |
| [tests/SelfSignup.Api.Tests.Unit/AccountCreationImplTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/AccountCreationImplTest.cs) | 27 |
| [tests/SelfSignup.Api.Tests.Unit/InsuranceWizardImplTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/InsuranceWizardImplTest.cs) | 26 |
| [tests/SelfSignup.Api.Tests.Unit/ValidationExtensionsTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/ValidationExtensionsTests.cs) | 24 |
| [tests/SelfSignup.Api.Tests.Unit/LeadGenerationImplTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/LeadGenerationImplTest.cs) | 21 |
| [tests/SelfSignup.Api.Tests.Unit/LeadSubmissionImplTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/LeadSubmissionImplTest.cs) | 15 |
| [tests/SelfSignup.Api.Tests.Unit/ExtensionHelperTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/ExtensionHelperTests.cs) | 15 |
| [tests/SelfSignup.Api.Tests.Unit/ProviderJoinServiceReadWriteDataRequirementHandlerTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/ProviderJoinServiceReadWriteDataRequirementHandlerTests.cs) | 13 |
| [tests/SelfSignup.Api.Tests.Unit/UpdateLeadStatusPostSubmissionImplTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/UpdateLeadStatusPostSubmissionImplTest.cs) | 11 |
| [tests/SelfSignup.Api.Tests.Unit/RequestValidatorTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/RequestValidatorTest.cs) | 9 |
| [tests/SelfSignup.Api.Tests.Unit/Auth/SelfSignUpPracticeAuthorizationHandlerTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/Auth/SelfSignUpPracticeAuthorizationHandlerTests.cs) | 7 |
| [tests/SelfSignup.Api.Tests.Unit/Auth/PracticeAuthorizationHandlerTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/Auth/PracticeAuthorizationHandlerTests.cs) | 7 |
| [tests/SelfSignup.Api.Tests.Unit/RequestDemoImplTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/RequestDemoImplTest.cs) | 6 |
| [tests/SelfSignup.Api.Tests.Unit/IdentityHelperTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/IdentityHelperTests.cs) | 6 |
| [tests/SelfSignup.Api.Tests.Unit/UserAgreementControllerTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/UserAgreementControllerTest.cs) | 3 |
| [tests/SelfSignup.Api.Tests.Unit/PricingImplTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/PricingImplTest.cs) | 2 |
| [tests/SelfSignup.Api.Tests.Unit/Auth/CsrAuthorizationHandlerTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/Auth/CsrAuthorizationHandlerTests.cs) | 2 |
| [tests/SelfSignup.Api.Tests.Unit/ClaimProfileImplTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/ClaimProfileImplTest.cs) | 2 |
| [tests/SelfSignup.Api.Tests.Unit/CcpaImplTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Api.Tests.Unit/CcpaImplTest.cs) | 1 |

### SelfSignup.Infrastructure.Tests.Unit (196)
| File | Tests |
|------|-----:|
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/AccountCreation/AccountCreationServiceTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/AccountCreation/AccountCreationServiceTest.cs) | 53 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/InsuranceOnboarding/InsuranceOnboardingServiceTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/InsuranceOnboarding/InsuranceOnboardingServiceTest.cs) | 23 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/SignUpServiceTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/SignUpServiceTest.cs) | 19 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/LeadsServiceTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/LeadsServiceTests.cs) | 15 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/LeadSalesforceServiceTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/LeadSalesforceServiceTests.cs) | 14 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/SignupPortalServiceTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/SignupPortalServiceTest.cs) | 10 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/PartnerReferrerOverridesTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/PartnerReferrerOverridesTest.cs) | 9 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/ProviderSetup/ProviderOnboardTaskFrameworkApiTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/ProviderSetup/ProviderOnboardTaskFrameworkApiTests.cs) | 8 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/Pricing/PricingServiceTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/Pricing/PricingServiceTests.cs) | 6 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Extensions/EnumExtensionsTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Extensions/EnumExtensionsTests.cs) | 6 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Utils/LocationHelperTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Utils/LocationHelperTests.cs) | 5 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Repositories/DdbRepositoryTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Repositories/DdbRepositoryTests.cs) | 4 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/SalesforceRepositoryTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/Leads/SalesforceRepositoryTest.cs) | 4 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/FoundationalSupplementalMapping/FoundationalSupplementalMappingServiceTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/FoundationalSupplementalMapping/FoundationalSupplementalMappingServiceTests.cs) | 4 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/ProviderSetup/SvcToSvcAuthOnboardTaskFrameworkApiTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/ProviderSetup/SvcToSvcAuthOnboardTaskFrameworkApiTests.cs) | 4 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Extensions/CollectionExtensionsTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Extensions/CollectionExtensionsTests.cs) | 3 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Factories/LeadDdbDtoFactoryTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Factories/LeadDdbDtoFactoryTest.cs) | 3 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/Monolith/UserAgreementApiTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/Monolith/UserAgreementApiTests.cs) | 3 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/ClaimProfile/ClaimProfileServiceTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/ClaimProfile/ClaimProfileServiceTests.cs) | 2 |
| [tests/SelfSignup.Infrastructure.Tests.Unit/Services/Ccpa/CcpaServiceTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Infrastructure.Tests.Unit/Services/Ccpa/CcpaServiceTests.cs) | 1 |

### SelfSignup.Integration.Tests (93)
| File | Tests |
|------|-----:|
| [tests/SelfSignup.Integration.Tests/InsuranceWizardTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/InsuranceWizardTest.cs) | 34 |
| [tests/SelfSignup.Integration.Tests/AccountCreationTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/AccountCreationTests.cs) | 15 |
| [tests/SelfSignup.Integration.Tests/LeadRetrievalTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/LeadRetrievalTest.cs) | 13 |
| [tests/SelfSignup.Integration.Tests/SignUpFlowTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/SignUpFlowTest.cs) | 10 |
| [tests/SelfSignup.Integration.Tests/LocalStackDynamoDbTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/LocalStackDynamoDbTests.cs) | 6 |
| [tests/SelfSignup.Integration.Tests/LocalStackDemoRequestTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/LocalStackDemoRequestTests.cs) | 4 |
| [tests/SelfSignup.Integration.Tests/UserAgreementTests.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/UserAgreementTests.cs) | 3 |
| [tests/SelfSignup.Integration.Tests/CcpaTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/CcpaTest.cs) | 2 |
| [tests/SelfSignup.Integration.Tests/ClaimProfileTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/ClaimProfileTest.cs) | 2 |
| [tests/SelfSignup.Integration.Tests/PostSubmissionUpdatesTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/PostSubmissionUpdatesTest.cs) | 2 |
| [tests/SelfSignup.Integration.Tests/PricingTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/SelfSignup.Integration.Tests/PricingTest.cs) | 2 |

### ProviderJoinService.AbandonmentLambda.Tests (3)
| File | Tests |
|------|-----:|
| [tests/ProviderJoinService.AbandonmentLambda.Tests/FunctionalTests/FunctionTest.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/ProviderJoinService.AbandonmentLambda.Tests/FunctionalTests/FunctionTest.cs) | 2 |
| [tests/ProviderJoinService.AbandonmentLambda.Tests/FunctionTest.cs#L19](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/ProviderJoinService.AbandonmentLambda.Tests/FunctionTest.cs#L19) | 1 (echo-back placeholder: `Assert.AreEqual("hello", test.Result);`) |

### SelfSignup.Tests.Unit
Empty (no `*.cs` files matching `[Test]`/`[TestCase(`).

## Critical untested classes (verified)

| Class | Source | Notes |
|-------|--------|-------|
| `StepFunctionService` | [src/SelfSignup.Infrastructure/Services/StepFunctionService/StepFunctionService.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/src/SelfSignup.Infrastructure/Services/StepFunctionService/StepFunctionService.cs) | All test references are `Mock<IStepFunctionService>`. |
| `CreatePracticeDtoFactory` | [src/SelfSignup.Infrastructure/Services/PracticeAndProviderCreation/CreatePracticeDtoFactory.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/src/SelfSignup.Infrastructure/Services/PracticeAndProviderCreation/CreatePracticeDtoFactory.cs) | 0 references in `tests/`. |
| `UpdatesDefinitionFactory` | [src/SelfSignup.Infrastructure/Services/Factories/UpdatesDefinitionFactory.cs](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/src/SelfSignup.Infrastructure/Services/Factories/UpdatesDefinitionFactory.cs) | 0 references in `tests/`. |

## v1 corrections

| v1 said | v2 verified |
|---------|-------------|
| `InsuranceWizardTest` 26 tests | **34** |
| `SelfSignupLeadStatusBuilderTest` 70+ tests | **73** (CONFIRMED) |
| `AccountCreationTests` 15 tests | **15** (CONFIRMED) |
| `SignUpFlowTest` 10 tests | **10** (CONFIRMED) |
| `AbandonmentLambda` `FunctionTest` is trivial echo-back | **CONFIRMED** at [L19](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/tests/ProviderJoinService.AbandonmentLambda.Tests/FunctionTest.cs#L19) |
| `StepFunctionService`/`CreatePracticeDtoFactory`/`UpdatesDefinitionFactory` untested | **CONFIRMED** for all three |
