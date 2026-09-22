# Infrastructure / Auth — Test Gap Analysis

<!-- test-mapping-gaps-meta
team: Infrastructure / Auth
scope: every repo in test-mapping/auth/README.md
generated: 2026-08-27
verified: 2026-08-27 (second pass; every claim re-checked against source)
method: mapped tests diffed against each repo's production surface at HEAD
-->
> Companion to the [Auth test mappings](README.md). The mappings answer *what is tested*; this answers *what is not*.

## Method and confidence

For every repo in the Auth mapping index the production surface at current `HEAD` was enumerated (API operation
impls, controllers, lambda handlers, workers, Auth0 action scripts, CDK stacks, service classes) and diffed
against the test surface.

Every "untested" claim below was verified three ways, because a name-based scan alone produces false positives:

1. **Word-boundary scan** — the type name never appears in any test file.
2. **Substring scan** — catches `FooTests.cs` naming and `IFoo` interface mentions. Where the only hits are
   `Mock<IFoo>()`, the row says so: the interface is mocked by consumers, the concrete class is untested, and
   nothing asserts the two agree.
3. **Source read** — the class was opened to confirm it exists, is concrete (not abstract or an extension-method
   holder invoked without its name), and carries the behaviour claimed.

Candidates that failed step 2 or 3 were dropped rather than reported. Rows marked **⚠** are corrections to the
first pass of this document.

Priorities: **P1** = security or correctness boundary with no coverage at any level, **P2** = real behaviour
reachable only through a deployed environment, **P3** = hygiene.

## Summary

| Repo | Proposed tests | Headline gap |
|---|---:|---|
| [auth-service](#auth-service) | 34 | All 9 API operation impls and 5 of 6 login controllers are unit-test-free |
| [zocdoc_web (auth-owned)](#zocdoc_web-auth-owned-paths) | 32 | 3 of the 4 authentication schemes, the password expiry/reuse checker, and both service API callers |
| [auth0-infrastructure](#auth0-infrastructure) | 29 | 3 of 13 Auth0 action scripts have zero tests — all three make access decisions |
| [audit-logging-service](#audit-logging-service) | 27 | The S3/SNS enqueue lambda handler and all 3 patient API callers |
| [legal-agreement](#legal-agreement) | 27 | No `PracticeUserAgreementImpl` unit tests; the 25-item backfill cap is unasserted at every level |
| [user-locking](#user-locking) | 23 | `AuthServiceApiCaller` — the whole auth-service edge — has zero tests |
| [consumer-privacy-service](#consumer-privacy-service) | 18 | `BasicAuthService` is untested and throws on 3 malformed headers; no CCPA request runs end to end |
| [sandbox (Playwright E2E)](#sandbox-playwright-e2e) | 12 | No test completes a sign-up, a password reset, or a successful MFA challenge |
| [external-developer-api-auth](#external-developer-api-auth) | 7 | `auth0AppClientFrontEndKeysToDynamoRequests` and every schema-rejection path |
| [ServiceMockEndpoints](#servicemockendpoints) | 8 | Nothing compares the mock's responses to the real auth-service contract |
| [user-accounts](#user-accounts) | 3 | Best covered in the set; the web integration project holds only a scaffold |

**220 numbered proposals**, plus 9 unnumbered hygiene items (delete-or-fix rows, marked `—`).

---

## auth-service

The mapped 1,172 tests are real, but they concentrate in services and event factories. Every class below is
**never named anywhere under `tests/`**. Where the behaviour is covered at all it is covered only by `ApiTests`
against a deployed instance — which is precisely the coverage that cannot shift left.

Verified: each of the nine impls has a matching `tests/ApiTests/**` file, so these are unit-test gaps, not
total blind spots. There is a strong in-repo precedent for controller unit tests — `InternalUserLoginControllerTests`,
`KafkaProduceTestControllerTests`, `Auth0WebhookControllerTests`, and `PracticeLogoutControllerTests` all exist.

| # | P | Proposed test file | Covers | Why |
|---|---|---|---|---|
| 1–9 | P2 | `PhoneVerificationImplTests`, `ReconciliatorImplTests`, `UserImplTests`, `UniversalLoginEventsImplTests`, `ExternalClientImplTests`, `PracticeIdentityProviderImplTests`, `PracticeLoginImplTests`, `ServiceAuthImplTests`, `MultiPracticeImplTests` | The nine API operation impls | `PhoneVerificationImpl` alone is 259 lines of branch logic; its response-code mapping is only ever observed over HTTP |
| 10–14 | P2 | `PatientLoginControllerTests`, `PracticeLoginControllerTests`, `UserLoginControllerTests`, `MultiPracticeLoginControllerTests`, `CreatePatientAccountControllerTests` (+ `CreateAccountUtils`) | Five untested login controllers | Note `UserLoginController` is a distinct class from the already-tested `InternalUserLoginController` |
| 15–17 | P1 | `MonolithAuthorizationApiCallerTests`, `ProviderGroupingApiCallerTests`, `UserLockingApiCallerTests` | Status mapping, timeouts, non-200 bodies | Each interface is mocked in exactly one consumer test; the concrete caller is untested, so nothing checks the mock matches reality. `MonolithAuthBackdoorApiCallerTests` is the precedent |
| 18 | P1 | `InternalServicesTenantManagementApiTokenCacheTests` | Cache hit, expiry, refresh, concurrent refresh, refresh failure | A stale or thundering-herd management token breaks every internal-services login |
| 19–20 | P2 | `InternalServicesTenantAuth0ClientTests`, `PatientTenantUniversalLoginWebClientTests` | Auth0 client wrappers | |
| 21–23 | P1 | `TwilioVerifyServiceTests`, `TwilioClientWrapperTests`, `FakeTwilioClientWrapperTests` | Send/check verification, Twilio error codes, fake-vs-real parity | Neither `ITwilioVerifyService` nor `ITwilioClientWrapper` is even mocked in a test; phone verification has no unit coverage of the Twilio edge at all |
| 24–27 | P1 | `EmailFormatValidatorTests`, `PhoneUtilityTests`, `SpiCookieServiceTests`, `GuidFactoryTests` | Pure helpers — `EmailFormatValidator` is a static class with `IsValidEmailFormat` / `IsBareEmailFormat` | Cheapest tests in the repo; the email-format rules currently rest on nothing |
| 28 | P2 | `RequestContextMiddlewareTests` | Context population, missing headers, exception pass-through | Runs on every request |
| 29–31 | P2 | `KmsServiceTests`, `ServiceAuthRelease.AuthServiceApiCallerTests`, `EndpointSettingsTests` | The service-auth release lambda | `IKmsService` is mocked in `ServiceAuthLambdaTests`; the concrete `KmsService` is untested and its 5 ApiTests are all `RealOnly` |
| 32 | P1 | Real `PracticeUserAuth0SynchronizerLambdaHandlerTests` | Actual synchronisation behaviour | Verified: the sole unit test is `Verify_Handler_RecordsTestLog_AndFiresTestMetric` — it asserts a log line and a `test_metric`. The integration test only asserts the lambda returns HTTP 200 with no `FunctionError` |
| 33 | P2 | `DateTimeConverterTests` (StreamProcessor) | The millisecond-epoch `Read` path | ⚠ Softened: `StreamProcessorLambdaTests` exercises the converter implicitly via `LambdaSerializer.Serialize`, so the **write** path runs. The millisecond-epoch **read** — the only reason this copy of the AWS converter exists — is never exercised |
| 34 | P2 | `TickerTests`, `BackgroundServiceAuthTokenProviderTests`, `AmazonKinesisFirehoseClientFactoryTests`, `ServiceAuthExtensions` DI-registration test | Remaining unnamed classes | `ServiceAuthExtensions` is extension-method-only; verified its methods (`AddZocdocServiceAuthForEcs`/`ForLambdas`) appear in no test |
| — | P3 | Delete or relabel `tests/UnitTests/ServiceAuthProofOfConcept.cs` | Verified: a `[Test]`-annotated developer script for minting an assertion JWT, with one assertion and no subject under test | |

---

## zocdoc_web (auth-owned paths)

188 test classes / 2,180 methods, and the classes below are still never named in `ZocDoc.Security.Tests`,
`PracticeAuthorization.Test`, or `Zocdoc.PracticeUserRolesPrivate.Tests`. Every substring hit was checked and is
a `Mock<IFoo>()` in a consumer's test.

| # | P | Proposed test | LOC | Why |
|---|---|---|---:|---|
| 35–37 | P1 | `AspxAuthCookieAuthenticationScheme`, `Auth0JwtAuthenticationScheme`, `OAuthAuthenticationScheme` | 34/34/31 | The schemes that decide *how* a monolith request authenticates. `JwtAuthenticationSchemeTests.cs` exists for the fourth; these three are mocked in `RequireAuthenticationServiceTest` and never executed |
| 38 | P1 | `PasswordExpirationReuseChecker` | 28 | Password expiry and reuse policy — a direct compliance surface, mocked in `PasswordUtilityTests`, never run |
| 39 | P1 | `SymmetricEncryptor` — round-trip, wrong key, tampered ciphertext, empty and oversized input | 197 | Zero references of any kind |
| 40–41 | P1 | `AuthIdentityReconciliatorSql`, `AuthIdentityAuditService` | 302 / 116 | Dual-identity reconciliation — the code path behind `aspnet_cloud_id_mismatch` token-exchange 403s |
| 42–43 | P1 | `AuthServiceApiCaller` + `FakeAuthServiceApiCaller` | 277 | Monolith → auth-service edge. The fake has no test either, so nothing pins the two together |
| 44–45 | P1 | `UserLockingServiceApiCaller` + `FakeUserLockingServiceApiCaller` | 114 | Monolith → user-locking edge; decides whether a locked patient is let in |
| 46 | P1 | `UsernameEmailChangeService` — collision, verification state, Auth0 propagation | 339 | |
| 47 | P2 | `PracticeUserRolesPrivateImpl` | 247 | The five API operations are untested; the project's test classes cover only the services behind them |
| 48–49 | P2 | `PracticeAuthorizationUtils`, `PracticeAuthorizationProxyApiClientFactory` | | The only untested files in the FGA proxy layer |
| 50–51 | P2 | `OAuth2AttributeService`, `AuthorizationServerWrapper` | 190 | ⚠ `OAuth2Client` was dropped from this list — verified `internal abstract class`, so it is not directly testable |
| 52–53 | P2 | `ResourceServerFactory`, `StandardAccessTokenAnalyzerFactory` | | Token validation and key plumbing |
| 54 | P2 | `ServiceAuthServiceAuthKmsClientWrapper` + `FakeServiceAuthKmsClientWrapper` | | Neither the real wrapper nor its fake is referenced by a test |
| 55–57 | P2 | `MultiProviderLoginMetricsService` and its two SQL persistences, `MultiProviderAuditor`, `MultiProviderMetricsService` | 79 | Multi-provider login metrics are entirely unverified |
| 58–59 | P2 | `CognitoClient`, `CognitoUserServiceBase` | | Cognito identity-provider path; `ICognitoClient` is mocked in three service tests |
| 60–62 | P2 | `FormsAuthenticationWrapper`, `AuthFormSqlProvider`, `ExtendedSessionSqlFactory` | | Session and cookie issuance |
| 63–66 | P3 | `ZDMembership` (96), `ZDRoles`, `Pbkdf2ConcurrencyLock`, `SecuritySensitiveCodeAttribute`, `ScopedDataAuthUserNameAttribute` | | `ZDMembershipSqlTests` covers `ZDMembershipSql`, a different class |
| — | P3 | Remove the stale `CODEOWNERS` entry for `/Zocdoc.AuditLogging/` | | Directory no longer exists; already noted in the mapping changelog |

---

## auth0-infrastructure

Verified: 13 action scripts under `actions/`, 10 with a matching file in `__tests__/unit/`. The three without
one are `add_patient_role.js`, `redirect.js`, and `require_zd_app_for_marketplace.js` — all three make access
decisions. The Jest harness already covers the other ten, so these are drop-in additions.

### `actions/patient/require_zd_app_for_marketplace.js` → `__tests__/unit/require-zd-app-for-marketplace-tests.js`

The whole action is three nested `if`s and one `api.access.deny`.

| # | P | Proposed test | Why |
|---|---|---|---|
| 67 | P1 | marketplace audience + `is_zocdoc_application !== "true"` → `api.access.deny("Invalid audience for application")` | The only thing stopping a third-party client from minting a marketplace token |
| 68 | P1 | marketplace audience + `"true"` → no deny | Guards against over-denying first-party apps |
| 69 | P1 | non-marketplace audience → no deny, whatever the client metadata | Confirms the rule is audience-scoped |
| 70 | P2 | `event.resource_server` undefined → no deny, no throw | Non-API logins must pass through |
| 71 | P1 | `event.client.metadata` undefined → currently throws `TypeError` | Verified: no optional chaining on `event.client.metadata`. Undefined metadata is a plausible client state; a test settles whether the action fails open or the login errors |
| 72 | P2 | `is_zocdoc_application` boolean `true` rather than the string → denies | The comparison is strict-equality against `"true"`; pin it or fix it |

### `actions/patient/redirect.js` → `__tests__/unit/redirect-tests.js`

| # | P | Proposed test | Why |
|---|---|---|---|
| 73 | P2 | `is_zocdoc_application === "true"` → returns before signing or fetching | First-party short-circuit |
| 74 | P1 | `event.client.metadata` undefined → throws | Verified: this dereference sits **before** the `try`, so it escapes the `api.access.deny` catch entirely and fails the login with an unhandled error |
| 75 | P2 | `externalApiBaseUrl` not `https://api-developer.zocdoc.com/` → returns without a fetch | Nothing tests that non-prod stays inert |
| 76 | P1 | terms fetch returns non-200 → `api.access.deny` | Fail-closed on a dependency error |
| 77 | P1 | terms fetch rejects → `api.access.deny` | Same, for a transport failure |
| 78 | P1 | `requires_terms_of_use && !has_signed_terms_of_use` → `PUT v1/user/terms-of-use`, then no redirect | Auto-accept branch |
| 79 | P2 | `requires_terms_of_use && has_signed_terms_of_use` → no PUT, no redirect | Idempotence |
| 80 | P1 | `!requires_terms_of_use && requires_active_consent_to_market && !has_active_consent_to_market` → redirect | The consent-page branch |
| 81 | P2 | same with consent already active → no redirect | |
| 82 | P2 | neither flag set → no redirect | Default pass-through |
| 83 | P1 | signed assertion carries `azp` = client id, `scope` and `permissions` = `external.consent.write`, issuer `Auth0ActionIssuer`, subject = `event.user.user_id`, audience `[secrets.audience]`, RS256, 1800s expiry | This JWT authenticates to the external developer API |
| 84 | P2 | `keyid` falls back to a generated uuid when `secrets.kid` is absent | Key-rotation path |
| 85 | P2 | redirect query carries `session_token` and `event.transaction.state` | State must survive the round trip |
| 86 | P2 | `onContinuePostLogin` on resume | Verified: it is an empty function, so nothing re-checks the consent outcome after the redirect returns. A test should pin whether that is intended |

### `actions/patient/add_patient_role.js` → `__tests__/unit/add-patient-role-tests.js`

| # | P | Proposed test | Why |
|---|---|---|---|
| 87 | P2 | user already holds `Patient` → no `ManagementClient` constructed, `assignUsers` not called | Avoids a Management API call on every login |
| 88 | P1 | no roles → `assignUsers({id: secrets.patientRoleId}, {users:[user_id]})` | Every new patient depends on this |
| 89 | P2 | `event.authorization` undefined → still assigns | The `?.` branch |
| 90 | P2 | roles present but not `Patient` → assigns | |
| 91 | P1 | `assignUsers` rejects → error swallowed, login proceeds | The catch is deliberate fail-open; pin it so nobody "fixes" it into a login outage |

### Rest of the repo

| # | P | Proposed test | Why |
|---|---|---|---|
| 92 | P2 | Any test for `cdk/src/auth0LambdaAndEventbridgeStack.ts` and `cdk/src/cdk.ts` | Verified: `cdk/jest.config.js` sets `roots: ['<rootDir>/test']` and `cdk/test/` does not exist — the config is dead and both stack files have zero tests |
| 93–94 | P2 | `CorrelationIdDecoder`, `Auth0LogErrorJsonConverter` (valid, malformed, absent error payloads) | Zero references of any kind |
| 95 | P3 | `KafkaSsmConfiguration` | Zero references of any kind |
| — | P3 | Extend the Cypress smoke beyond the single authorization-code login | One e2e test guards the whole tenant config |

---

## audit-logging-service

| # | P | Proposed test | Why |
|---|---|---|---|
| 96–101 | P1 | `PatientIdEnqueue.Lambda/HandlerTests`: S3 event with one record; with several; SNS-wrapped S3 event; malformed SNS body; parse failure surfacing; empty object → no DDB writes | Verified: `src/PatientIdEnqueue.Lambda/` holds `Handler.cs` and `Function.cs` with no test file, though `S3LogParser` and `ReportingModelToDdbDtoService` beneath them are covered |
| 102–105 | P2 | `LastScannedKeyDynamoPersistenceTests` (get / put / delete / missing key) and `LastScannedKeyDdbDtoAttributeServiceTests` | The worker's resume checkpoint. `WorkerTests` mocks both interfaces, so neither implementation ever runs |
| 106–113 | P1 | `ZvsApiCallerTests` (both `GetPatientDetails` and `GetPaymentPatientDetails`), `ExternalDeveloperApiCallerTests`, `PatientInsuranceLookupApiCallerTests` — id-set batching, non-200, partial results, `PatientCallerResponseStatus` mapping | Three concrete outbound callers with zero tests. `IPatientInsuranceLookupApiCaller` is not even mocked anywhere |
| 114 | P1 | **⚠ Corrected:** `FirehoseClientWrapper.SaveLogs` with `FailedPutCount == 0` | The first pass claimed the failure branch was untested. It is not — `Test_GetFireHoseResponse` asserts `FailedFirehosePutCount` is incremented by 3. The real gap is the inverse: the only unit test has **every** record failing, so the success path is never asserted |
| 115 | P1 | `FirehoseClientWrapper.SavePermissionLogs` | The whole method is untested; it duplicates `SaveLogs` against a different stream and tags the failure metric differently |
| 116 | P1 | `SaveLogs` with more than 500 records | Verified: no chunking anywhere in the wrapper, and `PutRecordBatch` caps at 500 records per call |
| 117 | P2 | `SaveLogs` where `RequestResponses.Count != logs.Count` | Both methods do `logs.ElementAt(index)` over the response list; a short response throws rather than degrading |
| 118–121 | P2 | `LogConverter.FlattenPermissionChangeLog` | All five existing converter tests are authorization-log; the permission-change flattener is only ever mocked, in `AuthorizationLogImplTest` |
| 122 | P2 | `AuthorizationLogImpl`: multi-record batch, and `xAuditLoggingLibraryVersion` propagated into the flattened log | |
| — | P3 | Rename `ExternalDeveloperDeveloperApiCaller` | Verified typo: the class in `ExternalDeveloperApiCaller.cs` is declared `ExternalDeveloperDeveloperApiCaller` |
| — | P3 | Delete or convert `monolithInvestigationScripts/BitmaskDecode.cs` | Verified: a `[Test]` with no assertion, counted in the mapping |

---

## legal-agreement

Verified: only 4 of the 8 mapped test files contain real tests. `LegalAgreement.UnitTests` and
`LegalAgreement.Web.IntegrationTests` hold nothing but a scaffold.

| # | P | Proposed test | Why |
|---|---|---|---|
| 123–131 | P2 | New `PracticeUserAgreementImplTests`: signature found → OK; not found + `OrganizationType == HealthSystem` → the synthesized `ENTERPRISE_PRACTICE_SIGNATORY_FULL_NAME` / `ENTERPRISE_PRACTICE_VERSION` response; not found + other org type → 404; not found + null org membership → 404; copy with >100 ids → 400; copy with exactly 100 → passes through; `KeyNotFoundException` → 404; backfill with >25 → 400; audit request with a non-`pt_` id → 400 | Five endpoints of branch logic with no unit tests at all. All four limits verified in source (`> 100`, `> 25`, `HealthSystem`, `StartsWith("pt_")`) |
| 132 | P1 | API test: backfill batch of 26 → 400 `"Max batch size is 25"` | The 25-item cap is asserted nowhere, at any level |
| 133 | P2 | API test: copy with exactly 100 ids → success | Only the 101 case is tested, so an off-by-one would pass |
| 134–137 | P1 | `ProviderGroupingApiCallerTests`: HealthSystem, other org type, null membership, caller throws | An exception here surfaces as a 500 on the agreement read |
| 138–141 | P1 | `SignUserAgreementPracticeUserAuthorizationHandlerTests`: FGA success → `context.Succeed`; FGA denial → requirement left unmet; parameter missing from route or body; FGA throws | Verified: the handler only ever calls `context.Succeed`, which is correct ASP.NET style — but nothing pins it |
| 142 | P1 | Policy-level test for `allow_practice_user_or_csr_signature_write` | ⚠ Reframed: `AllowPracticeUserOrCsrRolesRequirement` is *both* a `RolesAuthorizationRequirement` and an `ISignUserAgreementPracticeUserRequirement`, so the role handler and the FGA handler both evaluate it and **either** succeeding is enough. That OR is deliberate given the policy name, but a role holder passing despite an FGA denial is significant and untested |
| 143 | P2 | `AllowPracticeUserOrCsrRolesRequirementTests` | |
| 144–148 | P1 | Service helpers via the backfill path: identical ids → match; two differing `au_` ids → no match; mixed-type ids → match plus the `AuditAndBackfillUserAgreement.UserIdsAreDifferentTypes` metric; timestamps exactly 5s apart → match; 5.001s apart → no match | Verified in source: `UserIdsAreProbablyEqual` and `IsWithinFiveSeconds` (`<= 5`) decide whether a signature is backfilled or dropped, and the boundary is untested |
| 149 | P2 | API: sign twice with different versions, then read → newest wins | |
| — | P3 | Replace the four `ExampleTests` scaffolds | |

---

## user-locking

| # | P | Proposed test | Why |
|---|---|---|---|
| 150–158 | P1 | `AuthServiceApiCallerTests`: `GetUserAccountIdByPatientId` and `SetUserAccountIdByPatientId` with null or empty patient id → `ArgumentException`; happy path; 404 → `Auth0UserNotFoundException`; other non-2xx → `InvalidOperationException`; `SetUserBlockedStatus` with an empty account id; block and unblock happy paths | The entire auth-service edge — including the exception the lambda branches on — has zero tests. Only `IAuthServiceApiCaller` is mocked, in `HandlerTests` and `UserLockingImplTests` |
| 159–163 | P2 | `EnumListConverterTests`: string-list round-trip, legacy numeric read, unknown value, null, empty | Zero references of any kind; only indirectly exercised through one persistence test |
| 164 | P2 | `Handler`: unrecognised `UserLockAction` → `InvalidOperationException` | Verified at `Handler.cs:157`; the `_ => throw` branch is unreached |
| 165 | P2 | `Handler`: auth-service returns 5xx → the record lands in `BatchItemFailures` | Only a deserialization failure is tested today |
| 166–171 | P2 | `UserLockingImplTests` for `UnlockByPatientId`, `GetLockHistoryByPatientId`, and `LockByPatientId` beyond its metric | Verified: the impl exposes 12 operations; the 12 unit tests cover `GetLockReasonCodes`, `GetLockForCurrentUser`, `GetLockByPatientId`, `GetAllLocksByPatientId`, and one metric assertion on `LockByPatientId` |
| 172 | P3 | Pin the contract of the five published-but-unimplemented operations | Verified: `GetLockByUserAccount`, `LockByUserAccount`, `UnlockByUserAccount`, `LockByUserAccounts`, `DeleteLocksByUserAccounts` all `throw new NotImplementedException()` (`UserLockingImpl.cs:335–372`). A caller sees a 500 and no test records that this is intentional |
| — | P3 | Replace the three `ExampleTests` scaffolds | |

---

## consumer-privacy-service

| # | P | Proposed test | Why |
|---|---|---|---|
| 173–177 | P1 | `BasicAuthServiceTests`: header absent → null; `Authorization: Basic` with no parameter → today `Convert.FromBase64String(null)` throws; non-Base64 parameter → `FormatException`; decoded value with no `:` → `credentials[1]` throws `IndexOutOfRangeException`; valid header → username/password split on the **first** colon only | Verified against source. Every one of these is reachable by an unauthenticated caller and yields a 500 rather than a 401. Only `IBasicAuthService` is mocked; the concrete class has no test |
| 178–179 | P1 | `SalesforceAuthenticatorTests`, `CpaAuthHeaderProviderTests` | Outbound credential handling. `CpaAuthHeaderProvider` has zero references of any kind |
| 180–182 | P2 | `MessageSenderTests`, `FileRetrieverTests`, `DownloadControllerTests` | The delivery path for a subject-access request. `FileRetriever` and `DownloadController` have zero references |
| 183–184 | P2 | `FeatureFlagCheckerTests` / `Experiments` | Flag evaluation gates request behaviour |
| 185 | P3 | `GuidGeneratorTests` | |
| 186–190 | P1 | Replace `tests/FunctionalTests/ConsumerPrivacyTests.cs` with a real lifecycle: submit access request → generate PIN → verify PIN → download; plus the delete and opt-out equivalents | Verified: `PublicApiImpl` exposes 18 operations (37 paths across `service.yaml`) and the functional test is an empty `[Fact] Test1`. `tests/IntegrationTests/ConsumerPrivacyTests.cs` is the same empty scaffold |
| — | P3 | Replace `HomeControllerTests.Test1` (`Assert.True(true)`) | |

---

## sandbox (Playwright E2E)

24 tests across 6 files, all current — verified no commit has touched `playwright/BU/Infrastructure/Auth`
since the mapping was generated. Every test stops at a form-validation or error state; none completes an
account lifecycle.

| # | P | Proposed spec | Why |
|---|---|---|---|
| 191 | P1 | Complete a patient sign-up and land signed in | `create-user-page` covers only validation errors; the success path has no E2E |
| 192 | P1 | `password-recovery-flow`: follow the reset link, set a new password, sign in with it | Today the flow stops at "the email was accepted" |
| 193 | P1 | `signin-page`: successful MFA challenge | Only the wrong-code error is covered, though `challenge_mfa.js` carries 37 unit tests |
| 194 | P2 | Patient sign-out, then confirm protected pages redirect to `/signin` | Only the provider spec logs out |
| 195 | P2 | Deep-link → sign-in → returned to the original URL | Return-URL handling is unverified |
| 196 | P2 | Booking-locked patient can sign in but is blocked at booking | Both lock specs cover login locks only; the two lock types diverge here |
| 197 | P2 | Multi-practice provider login and practice switch | `MultiPracticeLoginController` has no E2E |
| 198 | P2 | First provider login gated on signing the practice user agreement | The legal-agreement gate is invisible to the E2E suite |
| 199 | P3 | Provider username/email change, then sign in with the new address | Pairs with `UsernameEmailChangeService` (row 46) |
| 200 | P3 | Passwordless (email/SMS) login start | Supported by auth-service, no E2E |
| 201 | P3 | Session expiry → re-authentication | |
| 202 | P3 | Rename one of the two duplicate tests in `password-recovery-flow.spec.ts` | Verified: lines 6 and 25 both read `"Accurate redirection to password reset page - Split Screen Expt ON"`. `-g` cannot select between them and Xray keys results on the title |

---

## external-developer-api-auth

| # | P | Proposed test | Why |
|---|---|---|---|
| 203–205 | P2 | `auth0AppClientFrontEndKeysToDynamoRequests`: keys present, none, deleted-key filtering | Verified: the module exports three functions and the Jest file imports only `loadAuth0AppClients` and `auth0AppClientsToDynamoRequests` |
| 206–208 | P1 | Schema validation: a client missing a required field is rejected; an out-of-enum `rateLimitingGroup` is rejected; a client with no `rateLimitingGroup` is rejected once the schema requires it | Per `docs/superpowers/specs/2026-07-15-require-rate-limiting-group-design.md`, a missing value writes an empty `ApiProduct` and silently drops the consumer to the `standard` Kong group |
| 209 | P2 | Synth test for `cdk/src/cdk.ts` | |
| — | P3 | Report `test-sync-clients-to-kong.sh` results in CI | Its 12 assertions exist but run as a standalone script, invisible to the mapping and easy to skip |

---

## ServiceMockEndpoints

⚠ **Corrected from the first pass.** That version rated "un-`[Ignore]` `ApiParityTests.TestingJwt`" as P1 and
called it the only test binding the mock to the real contract. Verified: `/testing/jwt` is already covered
extensively by `TestingControllerTests` (issuer, subject, audience, `kid`, expiry, RS256), so the ignored test
is a near-duplicate. Un-ignoring it adds almost nothing.

The real gap is what the class *name* promises and no test delivers: nothing anywhere compares this mock's
responses to the real auth-service contract. Downstream suites across the org trust it blindly.

Also verified and deliberately excluded from scope: `authentication/` is a Scala/Finatra service with ~31 of its
own tests, marked **deprecated** in `CLAUDE.md` ("do not add features or invest effort here"). No tests are
proposed for it. The mapping's line that "all 99 tests live in the single `Zocdoc.Auth.Mock.Tests` project"
should say the deprecated project was excluded.

| # | P | Proposed test | Why |
|---|---|---|---|
| 210 | P1 | A contract test validating mock responses against the same OpenAPI spec the real auth-service publishes | Turns parity from a manual promise into a build failure — and makes `ApiParityTests` mean what it says |
| 211–215 | P2 | `FgaServiceTests`, `PublicPrivateKeyPairsTests` (kid selection, rotation), `SerializationTests`, `ExamplesImplTests`, `CustomMetadataProviderTests` | Zero references of any kind. `FgaControllerTests` (34 tests) drives the controller over HTTP but never names `FgaService` |
| 216 | P3 | `AppSettings` binding test | |
| 217 | P3 | Either finish `ApiParityTests.TestingJwt` or delete it | An `[Ignore]`d test counted as coverage in the index |

---

## user-accounts

Best-covered repo in the set: both `UserAccountServiceTests` and `AccountsImplTests` end with
`AllPublicMethodsAreTested() => base.EnsureAllPublicMethodsAreTested()` — verified.

| # | P | Proposed test | Why |
|---|---|---|---|
| 218 | P2 | Give `UserAccounts.Web.IntegrationTests` real content | The project holds only an `ExampleTests` scaffold asserting `(1 + 1).Should().Be(2)`, so the web layer has no integration coverage |
| 219 | P3 | Direct `ConversionExtensions` cases for the enum tuples | Reached only implicitly, as extension methods |
| 220 | P3 | Remove the remaining `ExampleTests` scaffold in `UserAccounts.IntegrationTests` | |

---

## Cross-cutting

1. **Fakes have no parity tests.** `FakeAuthServiceApiCaller`, `FakeUserLockingServiceApiCaller`,
   `FakeServiceAuthKmsClientWrapper`, `FakeTwilioClientWrapper`, `FakeUserAccountDynamoPersistence`,
   `FakeUserLockDynamoPersistence`, `FakePracticeUserAgreementDynamoPersistence`, `FakeProviderGroupingApiCaller`.
   Where the fake is tested the real implementation usually is not, and nothing asserts the two behave alike.
   One shared parity fixture per interface would cover the set.
2. **Interfaces are mocked; implementations are not run.** This is the single most common shape in the whole
   analysis — verified for `IAuthServiceApiCaller`, `IUserLockingServiceApiCaller`, `IMonolithAuthorizationApiCaller`,
   `IProviderGroupingApiCaller`, `IKmsService`, `IBasicAuthService`, `IPasswordExpirationReuseChecker`,
   `IAuthIdentityReconciliatorSql`, `ILastScannedKeyDynamoPersistence`, `IZvsApiCaller`, and all three
   authentication schemes. Consumers are well tested against a contract nobody has checked.
3. **`[Category("RealOnly")]` is invisible coverage.** Verified: 56 RealOnly tests in auth-service across 13
   files, including *all 11* stream-processor ApiTests and *all 5* service-auth-release ApiTests. A green local
   or PR run implies coverage that never executed. Worth a CI line naming what was skipped.
4. **Scaffold tests are counted as coverage.** Verified 12 scaffold test methods — consumer-privacy-service (3),
   legal-agreement (4), user-locking (3), user-accounts (2) — plus `BitmaskDecode.cs`,
   `ServiceAuthProofOfConcept.cs`, and the `[Ignore]`d `ApiParityTests`. Fifteen entries in the index totals
   assert nothing.
5. **Every service edge between Auth repos is untested on both sides.** monolith→auth-service,
   monolith→user-locking, user-locking→auth-service, auth-service→provider-grouping,
   legal-agreement→provider-grouping. Contract tests on these five pairs are the highest-leverage single
   addition in the set.

## Corrections to the mappings

Found while diffing. These are mapping-accuracy issues, separate from the coverage gaps above.

| Mapping | Correction |
|---|---|
| `external-developer-api-auth` | Recorded as "1 file / 4 tests" with scope "whole repo". `test-sync-clients-to-kong.sh` — 12 `assert_json_eq` assertions covering deleted-client filtering, key filtering, `custom_id` dedupe, and Kong rate-limiting-group mapping — is missing entirely. Confirmed it existed at the pinned commit (the compare shows it *modified*, not added). The Jest file is also now 6 tests, not 4 |
| `user-accounts` | Materially stale, beyond a count bump. Pinned `0271f52` → HEAD `91af902` is 3 commits touching **8 test files**, including `AccountsImplTests.cs` (+110/−379), `FakeUserAccountDynamoPersistenceTests.cs` (+64/−278), and `ConversionExtensionsTests.cs` (+34/−98), plus two new files. `[Category("FakeOnly")]` no longer appears anywhere in the repo, so the 14 rows tagged FakeOnly are wrong. HEAD is ~90 test attributes. **Regenerate rather than patch** |
| `auth-service` | Pinned `fa9a039` → HEAD `bc14fb8` is 3 commits touching 6 test files, including `PracticeLoginServiceTests.cs` (+500/−2), `MonolithAuthBackdoorApiCallerTests.cs` (+56/−2), and a new `MonolithTokenExchangeEventFactoryTests.cs` (+268) |
| `auth-service` (changelog) | The 2026-08-21 entry describes `tests/ApiTests/` as "deployed instance, or the mock for `[Category("FakeOnly")]`". Verified there is no `FakeOnly` category anywhere in this repo — the real selector is 56 `[Category("RealOnly")]` tests that run only against a deployed stack |
| `auth0-infrastructure` | Pinned `cac1149` → HEAD `9e5531b` is 4 commits; `__tests__/unit/add-provider-claims-tests.js` grew +491/−32, a substantial expansion rather than a tweak |
| `ServiceMockEndpoints` | "All 99 tests live in the single `Zocdoc.Auth.Mock.Tests` project" — accurate for the live service (100 test methods counted), but should note that the deprecated Scala `authentication/` project with ~31 tests was excluded on purpose |
| `zocdoc_web` | 4 commits on `ZocDoc.Security` since the mapping; only `JwtV2ClaimsServiceTests.cs` changed, for new role ids. `PracticeAuthorization` and `Apis/PracticeUserRolesPrivate` are unchanged |
| `legal-agreement`, `audit-logging-service`, `user-locking`, `consumer-privacy-service`, `sandbox` | No test-file drift since the pinned commit. The sandbox repo has 21 new commits but none under `playwright/BU/Infrastructure/Auth` |
