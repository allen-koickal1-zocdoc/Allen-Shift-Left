# auth-service - Unit / Integration / API Test Mapping

<!-- test-mapping-meta
repo: Zocdoc/auth-service
branch: main
commit: fa9a039b0709e34f520baa1323897360b6719603
generated: 2026-08-21
test-type: unit, integration, api
scope: whole repo
granularity: one row per test method
-->

> Source: [`Zocdoc/auth-service`](https://github.com/Zocdoc/auth-service/tree/fa9a039b0709e34f520baa1323897360b6719603) @ `fa9a039` (branch `main`)

The Auth team's largest service: patient and provider login, OTP and passwordless flows, Auth0 orchestration across three tenants, refresh tokens, service-to-service auth, phone ownership, and the event stream that feeds login analytics. **1,172 tests across 101 files.**

Three test projects:

- **`tests/ApiTests/`** — run against a deployed instance (or the mock, for `[Category("FakeOnly")]`); these are the ones that actually prove authorization.
- **`tests/IntegrationTests/`** — real DynamoDB persistence.
- **`tests/UnitTests/`** — the bulk of the suite.

## `tests/ApiTests/PatientApi/PatientApiTests.cs`

The patient-facing API surface: OTP send and verify, passwordless start, phone lookup, and the CSR-only block/unblock and user-account-id endpoints.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1 | PatientSendOtpToPhone_Success | OTP send happy path (2 cases) | Send an OTP to a phone as an authenticated patient | Succeeds. | API | [L42](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L42) |
| 2 | PatientSendOtpToPhone_FailureBecauseNotPatient | Role gate | Send an OTP with a non-patient token | Rejected. | API | [L56](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L56) |
| 3 | PatientSendOtpToPhone_FailureBecauseNoAuth | Auth gate | Send an OTP with no token | Rejected. | API | [L70](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L70) |
| 4 | PatientSendOtpToPhone_FailureBecausePhoneNotE164_BackwardsCompatible | Legacy phone format | Send with a non-E.164 number on the legacy contract | Rejected, but through the backwards-compatible error shape. | API | [L84](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L84) |
| 5 | PatientSendOtpToPhone_FailureBecausePhoneNotE164 | Phone format validation | Send with a non-E.164 number | Rejected. | API | [L99](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L99) |
| 6 | PatientSendOtpToPhone_Failure | OTP send failures (3 cases) | Three failure conditions | Each rejected. | API | [L117](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L117) |
| 7 | PatientSendOtpToPhone_Failure_PhoneBelongsToLockedPatient | Locked-owner guard | Send an OTP to a phone owned by a locked patient | Rejected — otherwise OTP-to-phone would be a way around an account lock. | API | [L133](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L133) |
| 8 | SendOtp_AddsSuccessEvent | Event emission, success (`RealOnly`) | Send an OTP against the real deployment | A success event lands on the stream. | API | [L154](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L154) |
| 9 | SendOtp_AddsFailureEvent | Event emission, failure (`RealOnly`) | Fail an OTP send | A failure event lands. | API | [L178](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L178) |
| 10 | PatientSendOtpToPhone_PhoneOwnerLockedInUserLocking_ReturnsLocked | Cross-service lock check | The phone's owner is locked in the user-locking service | Returns locked — auth-service defers to user-locking, it does not keep its own copy. | API | [L203](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L203) |
| 11 | PatientSendOtpToPhone_PhoneOwnerNotLocked_Success | Lock check, negative | Owner is not locked | Succeeds. | API | [L240](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L240) |
| 12 | PasswordlessStart_Login_SendEmailIfUserExists | Passwordless email | Start passwordless for an existing user | The email is sent. | API | [L276](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L276) |
| 13 | PasswordlessStart_WithEmail_AddsEvent | Event emission (`RealOnly`) | Start passwordless by email | An event lands. | API | [L290](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L290) |
| 14 | PasswordlessStart_Login_ProviderEmail | Provider email | Start passwordless with a provider's email | Handled as a provider, not a patient. | API | [L322](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L322) |
| 15 | PasswordlessStart_Login_DualPatientAndProvider_FlagOff_ReturnsIsProvider | Dual identity, flag off | Start for an email that is both a patient and a provider | Reported as a provider. | API | [L365](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L365) |
| 16 | PasswordlessStart_Login_DualPatientAndProvider_FlagOn_ReturnsPatient | Dual identity, flag on | Same with the flag on | Reported as a patient — the flag flips which identity wins for a dual-role email. | API | [L417](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L417) |
| 17 | PasswordlessStart_Login_PracticeSsoEmailDomain_ReturnsBadRequest | SSO domain block | Start passwordless with an email on an SSO-managed domain | 400 — those users must go through their IdP. | API | [L465](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L465) |
| 18 | PasswordlessStart_Login_PracticeSsoEmailDomain_ButIsExistingPatient_StillWorks | SSO domain carve-out (6 cases) | Same, but the email is also an existing patient | Still works across all six cases — an employee of an SSO practice can still be a Zocdoc patient. | API | [L502](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L502) |
| 19 | PasswordlessStart_Login_InvalidEmail | Email validation | Start with a malformed email | Rejected. | API | [L551](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L551) |
| 20 | PasswordlessStart_Phone_AddsEvent | Event emission (`RealOnly`) | Start passwordless by phone | An event lands. | API | [L577](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L577) |
| 21 | PasswordlessStart_Login_SendPhone | Passwordless by phone | Start by phone | The code is sent. | API | [L608](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L608) |
| 22 | VerifyPhone_NotLoggedIn_Unauthorized | Auth gate | Verify a phone with no session | 401. | API | [L627](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L627) |
| 23 | VerifyPhone_Success | Verification happy path | Verify with the right code | Succeeds and the phone is linked. | API | [L644](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L644) |
| 24 | VerifyPhone_SuccessWithUnlinkingUserWithPhone | Phone transfer, unlink | Verify a phone currently linked to another user | The old link is removed and the new one created. | API | [L689](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L689) |
| 25 | VerifyPhone_TransferExistingPhoneInAuth0 | Phone transfer in Auth0 | Verify a phone that exists on another Auth0 user | Transferred — phone numbers are reused between people in the real world, and this is the path that handles it. | API | [L756](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L756) |
| 26 | VerifyPhone_BadRequest_DeserializationBackwardsCompatible | Legacy request shape (3 cases) | Send three malformed legacy bodies | 400 through the backwards-compatible shape. | API | [L817](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L817) |
| 27 | VerifyPhone_BadRequest | Request validation (3 cases) | Three malformed bodies | 400. | API | [L835](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L835) |
| 28 | VerifyPhone_FailsBecauseNotPatient | Role gate | Verify with a non-patient token | Rejected. | API | [L852](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L852) |
| 29 | VerifyPhone_FailsBecauseWrongCode | Wrong code | Verify with an incorrect code | Rejected. | API | [L867](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L867) |
| 30 | VerifyPhone_FailsBecauseExpiredCode | Expired code | Verify with an expired code | Rejected. | API | [L884](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L884) |
| 31 | VerifyPhone_FailsBecauseMaxAttemptsReached | Attempt cap | Verify after too many attempts | Rejected — the brute-force bound on OTP. | API | [L901](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L901) |
| 32 | GetPhonesByPatient_UnauthorizedWithPatientRole | Cross-patient read | Read another patient's phones as a patient | Rejected. | API | [L920](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L920) |
| 33 | GetPhonesByPatient_AuthorizedWithPatientRoleIfPatientMatch | Self read | Read your own phones | Allowed. | API | [L944](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L944) |
| 34 | GetPhonesByPatient_BadRequestWhenRequestingTooMany | Batch bound | Request more patients than the cap | 400 — bounds the blast radius of the bulk endpoint. | API | [L974](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L974) |
| 35 | GetPhonesByPatient_AuthorizedWithAdminRole | Admin read | Read as an admin | Allowed. | API | [L988](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L988) |
| 36 | GetPhonesByPatient_EmptyPhone_AuthorizedWithAdminRole | Admin read, no phone | Read a patient with no phone as admin | Allowed, empty result. | API | [L1011](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1011) |
| 37 | GetPhonesByPatientAsLoggedInPractice_CanAccessSomePhoneButNotOthers | Partial authorization | Read a mixed batch as a practice user | Only the permitted phones come back — the batch is filtered per-item rather than all-or-nothing. | API | [L1042](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1042) |
| 38 | GetPhonesByPatient_WhenUserWasCreatedWithoutPhoneRecord_ReturnsProcessedPatientWithNullPhone | Missing phone record | Read a patient created with no phone record | Returned with a null phone rather than omitted, so the caller can tell "no phone" from "not found". | API | [L1074](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1074) |
| 39 | GetBruteforceBlockedUsers_Forbidden | CSR endpoint gate | List brute-force-blocked users without the role | 403. | API | [L1130](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1130) |
| 40 | GetBruteforceBlockedUsers_Success | CSR endpoint | List with the role | Succeeds. | API | [L1140](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1140) |
| 41 | UnblockedUsers_Forbidden | Unblock gate | Unblock without the role | 403. | API | [L1153](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1153) |
| 42 | UnblockedUsers_Success | Unblock | Unblock with the role | Succeeds. | API | [L1164](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1164) |
| 43 | ValidateUsername_VariousCases | Username validation (5 cases) | Validate five username shapes | Each classified correctly. | API | [L1179](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1179) |
| 44 | ValidateUsername_BehindExperiment | Validation under experiment (5 cases) | Same five with the experiment on | Behaviour under the variant is pinned. | API | [L1197](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1197) |
| 45 | ValidateUsername_Provider | Provider username | Validate a provider's email | Classified as a provider. | API | [L1215](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1215) |
| 46 | ValidateUsername_PracticeSsoDomain | SSO domain (3 cases) | Validate three SSO-domain emails | Flagged as SSO. | API | [L1246](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1246) |
| 47 | ValidateUsername_PracticeSsoDomain_ForExistingPatient_ReturnsExistingPatientUser | SSO domain carve-out | Validate an SSO-domain email that is an existing patient | Returned as an existing patient — mirrors row 18. | API | [L1262](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1262) |
| 48 | GetPatientIdByPhoneNumber_Success_WithDifferentFormats | Phone lookup formats (1 case) | Look up by phone in several formats | All resolve to the same patient. | API | [L1284](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1284) |
| 49 | GetPatientIdByPhoneNumber_Forbidden_WithProviderRole | Role gate | Look up as a provider | 403 — providers cannot reverse a phone number to a patient. | API | [L1336](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1336) |
| 50 | GetPatientIdByPhoneNumber_BadRequest_ForInvalidNumbers | Input validation (4 cases) | Four invalid numbers | 400. | API | [L1354](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1354) |
| 51 | GetPatientIdByPhoneNumber_Unauthorized_WithoutAuth | Auth gate | Look up with no token | 401. | API | [L1369](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1369) |
| 52 | GetPatientIdByPhoneNumber_NotFound_WhenPhoneDoesNotExist | Unknown phone | Look up an unknown number | 404. | API | [L1381](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1381) |
| 53 | SetUserAccountIdByPatientId_Success_GeneratesAndSetsUserAccountId | Account-id assignment | Assign a user-account id to a patient | Generated and set. | API | [L1400](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1400) |
| 54 | SetUserAccountIdByPatientId_ReturnsNotFound_WhenPatientDoesNotExist | Unknown patient | Assign for a missing patient | 404. | API | [L1431](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1431) |
| 55 | SetUserAccountIdByPatientId_ReturnsNotFound_WhenAuth0UserNotFound | Missing Auth0 user | Patient exists but has no Auth0 user | 404. | API | [L1447](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1447) |
| 56 | SetUserAccountIdByPatientId_WithoutAuth_ReturnsUnauthorized | Auth gate | No token | 401. | API | [L1468](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1468) |
| 57 | SetUserAccountIdByPatientId_WithoutPatientManagementRole_ReturnsForbidden | Role gate | Wrong role | 403. | API | [L1480](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1480) |
| 58 | SetUserAccountIdByPatientId_ReturnsForbidden_WithPatientReadRole | Read vs write scope | Call the write endpoint with the read role | 403 — read and management are distinct scopes. | API | [L1495](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1495) |
| 59 | SetUserAccountIdByPatientId_IsIdempotent_WhenUserAccountIdAlreadySet | Idempotency | Assign when one is already set | No change. | API | [L1510](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1510) |
| 60 | SetUserAccountIdByPatientId_IsIdempotent_OnSecondCall_ReturnsExistingId | Idempotency, repeat call | Call twice | The same id comes back — a retry cannot mint a second account id for one patient. | API | [L1541](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1541) |
| 61 | GetUserAccountIdByPatientId_ReturnsUserAccountId_WhenPatientExistsWithUserAccountId | Read happy path | Read an assigned id | Returned. | API | [L1588](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1588) |
| 62 | GetUserAccountIdByPatientId_ReturnsNotFound_WhenPatientDoesNotExist | Unknown patient | Read for a missing patient | 404. | API | [L1615](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1615) |
| 63 | GetUserAccountIdByPatientId_ReturnsNotFound_WhenUserAccountIdNotSet | Unassigned | Read when nothing is set | 404. | API | [L1629](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1629) |
| 64 | GetUserAccountIdByPatientId_ReturnsUnauthorized_WithoutAuth | Auth gate | No token | 401. | API | [L1652](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1652) |
| 65 | GetUserAccountIdByPatientId_ReturnsForbidden_WithoutPatientReadRole | Role gate | Missing read role | 403. | API | [L1663](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1663) |
| 66 | SetUserBlockedStatus_WithoutAuth_ReturnsUnauthorized | Auth gate | Block with no token | 401. | API | [L1681](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1681) |
| 67 | SetUserBlockedStatus_WithWrongRole_ReturnsForbidden | Role gate | Wrong role | 403. | API | [L1696](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1696) |
| 68 | SetUserBlockedStatus_WithPatientJwt_ReturnsForbidden | Patient cannot self-block | Call with a patient JWT | 403 — blocking is CSR-only. | API | [L1713](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1713) |
| 69 | SetUserBlockedStatus_WithPatientManagementRole_ReturnsOk | Correct role | Call with patient-management | 200. | API | [L1730](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1730) |
| 70 | SetUserBlockedStatus_InvalidUserAccountId_Returns400 | Input validation | Malformed account id | 400. | API | [L1760](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1760) |
| 71 | SetUserBlockedStatus_UserNotFound_Returns404 | Unknown user | Unknown account id | 404. | API | [L1777](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1777) |
| 72 | SetUserBlockedStatus_MultipleUsersWithSameUserAccountId_Returns500 | Ambiguous account id | Two Auth0 users share one account id | 500 rather than blocking an arbitrary one — the ambiguity is surfaced instead of guessed. | API | [L1794](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1794) |
| 73 | SetUserBlockedStatus_BlockUser_Success | Block | Block a user | Blocked in Auth0. | API | [L1823](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1823) |
| 74 | SetUserBlockedStatus_UnblockUser_Success | Unblock | Unblock a user | Unblocked. | API | [L1857](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1857) |
| 75 | SetUserBlockedStatus_BlockAlreadyBlockedUser_Success | Idempotent block | Block an already-blocked user | Succeeds. | API | [L1903](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1903) |
| 76 | SetUserBlockedStatus_UnblockAlreadyUnblockedUser_Success | Idempotent unblock | Unblock an already-unblocked user | Succeeds. | API | [L1946](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientApiTests.cs#L1946) |

---

## `tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs`

Builds the v1 login-analytics events. Every event family is checked the same six ways — wrapper fields, exactly one event-data element, the core payload, a GUID event id, logged-in user null, logged-in user set — plus family-specific type/description/booking-id assertions. The repetition is the point: a missing field on one family is what breaks a funnel dashboard.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 77 | GetPatientLoginSuccessEvent_SetsTheFieldsOnTheWrapper | Patient login success, wrapper | Build the event | Wrapper fields set. | Unit | [L62](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L62) |
| 78 | GetPatientLoginSuccessEvent_CreatesASingleEventData | Cardinality | Build the event | Exactly one event-data element — no duplicate counting downstream. | Unit | [L73](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L73) |
| 79 | GetPatientLoginSuccessEvent_EventData_SetsTheCoreFields | Core payload | Build the event | Core fields set. | Unit | [L79](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L79) |
| 80 | GetPatientLoginSuccessEvent_EventData_HasAGuidEventId | Event id | Build the event | The event id is a GUID. | Unit | [L100](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L100) |
| 81 | GetPatientLoginSuccessEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | Build with no logged-in user | The Auth0 user id is null. | Unit | [L108](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L108) |
| 82 | GetPatientLoginSuccessEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Build with a logged-in user | The Auth0 user id is carried. | Unit | [L117](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L117) |
| 83 | GetPatientLoginSuccessEvent_EventData_SetsTheSuccessType | Success type (2 cases) | Build for two success types | Each mapped. | Unit | [L133](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L133) |
| 84 | GetPatientLoginSuccessEvent_EventData_SetsTheDescription | Description (2 cases) | Build for two descriptions | Each carried. | Unit | [L146](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L146) |
| 85 | GetPatientLoginSuccessEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Build with four booking-id shapes | Each carried — this is what ties a login to the booking it unblocked. | Unit | [L161](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L161) |
| 86 | GetPatientLoginFailureEvent_SetsTheFieldsOnTheWrapper | Patient login failure, wrapper | Build the event | Wrapper fields set. | Unit | [L185](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L185) |
| 87 | GetPatientLoginFailureEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L196](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L196) |
| 88 | GetPatientLoginFailureEvent_EventData_SetsTheCoreFields | Core payload | Build the event | Core fields set. | Unit | [L202](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L202) |
| 89 | GetPatientLoginFailureEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L223](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L223) |
| 90 | GetPatientLoginFailureEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L231](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L231) |
| 91 | GetPatientLoginFailureEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L240](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L240) |
| 92 | GetPatientLoginFailureEvent_EventData_SetsTheFailureType | Failure type (3 cases) | Build for three failure types | Each mapped — the split that makes "why did logins fail" answerable. | Unit | [L257](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L257) |
| 93 | GetPatientLoginFailureEvent_EventData_SetsTheDescription | Description (4 cases) | Four descriptions | Each carried. | Unit | [L270](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L270) |
| 94 | GetPatientLoginFailureEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four booking-id shapes | Each carried. | Unit | [L286](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L286) |
| 95 | GetRefreshSuccessEvent_SetsTheFieldsOnTheWrapper | Refresh success, wrapper | Build the event | Wrapper fields set. | Unit | [L315](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L315) |
| 96 | GetRefreshSuccessEvent_EventData_SetsTheCoreFields | Core payload | Build the event | Core fields set. | Unit | [L326](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L326) |
| 97 | GetRefreshSuccessEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L349](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L349) |
| 98 | GetRefreshSuccessEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L355](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L355) |
| 99 | GetRefreshSuccessEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L363](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L363) |
| 100 | GetRefreshSuccessEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L372](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L372) |
| 101 | GetRefreshSuccessEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L390](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L390) |
| 102 | GetRefreshFailureEvent_SetsTheFieldsOnTheWrapper | Refresh failure, wrapper | Build the event | Wrapper fields set. | Unit | [L413](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L413) |
| 103 | GetRefreshFailureEvent_EventData_SetsTheCoreFields | Core payload | Build the event | Core fields set. | Unit | [L424](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L424) |
| 104 | GetRefreshFailureEvent_EventData_AddsAdditionalDescriptionIfProvided | Optional detail | Build with an extra description | Appended — the only place a free-form reason reaches the stream. | Unit | [L447](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L447) |
| 105 | GetRefreshFailureEvent_SetsFailureTypeForError | Error mapping (2 cases) | Two error kinds | Each mapped to a failure type. | Unit | [L455](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L455) |
| 106 | GetRefreshFailureEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L462](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L462) |
| 107 | GetRefreshFailureEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L468](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L468) |
| 108 | GetRefreshFailureEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L476](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L476) |
| 109 | GetRefreshFailureEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L485](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L485) |
| 110 | GetRefreshFailureEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L503](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L503) |
| 111 | GetSentOneTimePasscodeSuccessEvent_SetsTheFieldsOnTheWrapper | OTP sent, wrapper | Build the event | Wrapper fields set. | Unit | [L531](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L531) |
| 112 | GetSentOneTimePasscodeSuccessEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L542](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L542) |
| 113 | GetSentOneTimePasscodeSuccessEvent_EventData_SetsTheCoreFields | Core payload | Build the event | Core fields set. | Unit | [L548](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L548) |
| 114 | GetSentOneTimePasscodeSuccessEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L570](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L570) |
| 115 | GetSentOneTimePasscodeSuccessEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L578](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L578) |
| 116 | GetSentOneTimePasscodeSuccessEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L587](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L587) |
| 117 | GetSentOneTimePasscodeSuccessEvent_EventData_SetsTheDescription | Description (2 cases) | Two descriptions | Each carried. | Unit | [L603](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L603) |
| 118 | GetSentOneTimePasscodeSuccessEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L618](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L618) |
| 119 | GetSentOneTimePasscodeSuccessFailureEvent_SetsTheFieldsOnTheWrapper | OTP send failure, wrapper | Build the event | Wrapper fields set. | Unit | [L643](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L643) |
| 120 | GetSentOneTimePasscodeSuccessFailureEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L654](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L654) |
| 121 | GetSentOneTimePasscodeSuccessFailureEvent_EventData_SetsTheCoreFields | Core payload | Build the event | Core fields set. | Unit | [L660](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L660) |
| 122 | GetSentOneTimePasscodeSuccessFailureEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L681](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L681) |
| 123 | GetSentOneTimePasscodeSuccessFailureEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L689](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L689) |
| 124 | GetSentOneTimePasscodeSuccessFailureEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L698](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L698) |
| 125 | GetSentOneTimePasscodeSuccessFailureEvent_EventData_SetsTheDescription | Description (4 cases) | Four descriptions | Each carried. | Unit | [L716](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L716) |
| 126 | GetSentOneTimePasscodeSuccessFailureEvent_EventData_SetsTheFailureType | Failure type (3 cases) | Three failure types | Each mapped. | Unit | [L731](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L731) |
| 127 | GetSentOneTimePasscodeSuccessFailureEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L743](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L743) |
| 128 | GetCreatePasswordlessPatientUserSuccessEvent_EventData_SetsTheCoreFields | Account creation success (2 cases) | Build for two variants | Core fields set. | Unit | [L773](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L773) |
| 129 | GetCreatePasswordlessPatientUserSuccessEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L819](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L819) |
| 130 | GetCreatePasswordlessPatientUserFailureEvent_EventData_SetsTheCoreFields | Account creation failure | Build the event | Core fields set. | Unit | [L845](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L845) |
| 131 | GetProviderLoginSuccessEvent | Provider login (6 cases) | Build for six provider login shapes | Each produces the right event — the provider side has one combined test where the patient side has six separate ones. | Unit | [L897](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L897) |
| 132 | GetProviderSsoLoginFailureEvent | Provider SSO failure | Build an SSO failure event | Correct. | Unit | [L953](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryTests.cs#L953) |

---

## `tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs`

The v2 factory, tested with the same six-way shape as v1 (rows 77–132) over a renamed and slightly reorganised set of event families: refresh, patient login, a single generic login-failure event replacing v1's separate failure events, send-OTP, and create-account. Both factories are live; v2 is not a replacement that retired v1.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 133 | GetRefreshSuccessEvent_SetsTheFieldsOnTheWrapper | Refresh success, wrapper | Build the event | Wrapper fields set. | Unit | [L54](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L54) |
| 134 | GetRefreshSuccessEvent_EventData_SetsTheCoreFields | Core payload (2 cases) | Build for two variants | Core fields set. | Unit | [L66](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L66) |
| 135 | GetRefreshSuccessEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L92](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L92) |
| 136 | GetRefreshSuccessEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L98](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L98) |
| 137 | GetRefreshSuccessEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L106](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L106) |
| 138 | GetRefreshSuccessEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L115](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L115) |
| 139 | GetRefreshSuccessEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L133](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L133) |
| 140 | GetRefreshFailureEvent_SetsTheFieldsOnTheWrapper | Refresh failure, wrapper | Build the event | Wrapper fields set. | Unit | [L145](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L145) |
| 141 | GetRefreshFailureEvent_EventData_SetsTheCoreFields | Core payload (2 cases) | Two variants | Core fields set. | Unit | [L157](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L157) |
| 142 | GetRefreshFailureEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L183](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L183) |
| 143 | GetRefreshFailureEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L189](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L189) |
| 144 | GetRefreshFailureEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L197](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L197) |
| 145 | GetRefreshFailureEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L206](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L206) |
| 146 | GetRefreshFailureEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L224](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L224) |
| 147 | GetPatientLoginSuccessEvent_SetsTheFieldsOnTheWrapper | Patient login success, wrapper | Build the event | Wrapper fields set. | Unit | [L240](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L240) |
| 148 | GetPatientLoginSuccessEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L251](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L251) |
| 149 | GetPatientLoginSuccessEvent_EventData_SetsTheCoreFields | Core payload (2 cases) | Two variants | Core fields set. | Unit | [L258](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L258) |
| 150 | GetPatientLoginSuccessEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L284](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L284) |
| 151 | GetPatientLoginSuccessEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L292](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L292) |
| 152 | GetPatientLoginSuccessEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L301](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L301) |
| 153 | GetPatientLoginSuccessEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L319](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L319) |
| 154 | GetLoginFailureEvent_SetsTheFieldsOnTheWrapper | Generic login failure, wrapper | Build the event | Wrapper fields set — v2 collapses v1's per-surface failure events into one. | Unit | [L331](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L331) |
| 155 | GetLoginFailureEvent_EventData_SetsTheCoreFields | Core payload (2 cases) | Two variants | Core fields set. | Unit | [L343](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L343) |
| 156 | GetLoginFailureEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L369](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L369) |
| 157 | GetLoginFailureEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L375](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L375) |
| 158 | GetLoginFailureEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L383](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L383) |
| 159 | GetLoginFailureEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L392](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L392) |
| 160 | GetLoginFailureEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L410](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L410) |
| 161 | GetSendOtpSuccessEvent_SetsTheFieldsOnTheWrapper | OTP sent, wrapper | Build the event | Wrapper fields set. | Unit | [L426](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L426) |
| 162 | GetSendOtpSuccessEvent_EventData_SetsTheCoreFields | Core payload (2 cases) | Two variants | Core fields set. | Unit | [L438](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L438) |
| 163 | GetSendOtpSuccessEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L464](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L464) |
| 164 | GetSendOtpSuccessEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L470](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L470) |
| 165 | GetSendOtpSuccessEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L478](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L478) |
| 166 | GetSendOtpSuccessEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L487](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L487) |
| 167 | GetSendOtpSuccessEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L505](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L505) |
| 168 | GetSendOtpFailureEvent_SetsTheFieldsOnTheWrapper | OTP send failure, wrapper | Build the event | Wrapper fields set. | Unit | [L521](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L521) |
| 169 | GetSendOtpFailureEvent_EventData_SetsTheCoreFields | Core payload (2 cases) | Two variants | Core fields set. | Unit | [L533](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L533) |
| 170 | GetSendOtpFailureEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L559](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L559) |
| 171 | GetSendOtpFailureEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L565](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L565) |
| 172 | GetSendOtpFailureEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L573](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L573) |
| 173 | GetSendOtpFailureEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L582](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L582) |
| 174 | GetSendOtpFailureEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L600](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L600) |
| 175 | GetCreateAccountSuccessEvent_SetsTheFieldsOnTheWrapper | Account creation success, wrapper | Build the event | Wrapper fields set. | Unit | [L616](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L616) |
| 176 | GetCreateAccountSuccessEvent_EventData_SetsTheCoreFields | Core payload (2 cases) | Two variants | Core fields set. | Unit | [L628](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L628) |
| 177 | GetCreateAccountSuccessEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L654](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L654) |
| 178 | GetCreateAccountSuccessEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L660](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L660) |
| 179 | GetCreateAccountSuccessEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L668](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L668) |
| 180 | GetCreateAccountSuccessEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L677](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L677) |
| 181 | GetCreateAccountSuccessEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L695](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L695) |
| 182 | GetCreateAccountFailureEvent_SetsTheFieldsOnTheWrapper | Account creation failure, wrapper | Build the event | Wrapper fields set. | Unit | [L711](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L711) |
| 183 | GetCreateAccountFailureEvent_EventData_SetsTheCoreFields | Core payload (2 cases) | Two variants | Core fields set. | Unit | [L723](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L723) |
| 184 | GetCreateAccountFailureEvent_CreatesASingleEventData | Cardinality | Build the event | One element. | Unit | [L749](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L749) |
| 185 | GetCreateAccountFailureEvent_EventData_HasAGuidEventId | Event id | Build the event | GUID. | Unit | [L755](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L755) |
| 186 | GetCreateAccountFailureEvent_EventData_GivenNoLoggedInUser_SetsTheLoggedInAuth0UserIdToNull | Anonymous case | No logged-in user | Null. | Unit | [L763](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L763) |
| 187 | GetCreateAccountFailureEvent_EventData_GivenALoggedInUser_SetsTheLoggedInAuth0UserId | Identified case | Logged-in user | Carried. | Unit | [L772](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L772) |
| 188 | GetCreateAccountFailureEvent_EventData_SetsTheBookingId | Booking attribution (4 cases) | Four shapes | Each carried. | Unit | [L790](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/LoggingEventFactoryV2Tests.cs#L790) |

---

## `tests/UnitTests/PostLoginMetricsServiceTests.cs`

Turns an Auth0 post-login payload into Datadog tags and histograms. Two things dominate: every field has an explicit unknown/null fallback so a missing attribute never drops the metric, and the provider tenant deliberately omits high-cardinality tags the patient tenant keeps.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 189 | Platform_UsesParserTag | Platform tag | Emit with a parsed platform | The parser's value is used. | Unit | [L93](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L93) |
| 190 | Platform_NullOrEmpty_ReturnsUnknown | Platform fallback (2 cases) | Null and empty | `unknown`. | Unit | [L105](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L105) |
| 191 | OsFamily_UsesParserTag | OS tag | Emit with a parsed OS | The parser's value is used. | Unit | [L116](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L116) |
| 192 | OsFamily_NullOrEmpty_ReturnsUnknown | OS fallback (2 cases) | Null and empty | `unknown`. | Unit | [L128](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L128) |
| 193 | BrowserType_UsesParserTag | Browser tag | Emit with a parsed browser | The parser's value is used. | Unit | [L139](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L139) |
| 194 | BrowserType_NullOrEmpty_ReturnsUnknown | Browser fallback (2 cases) | Null and empty | `unknown`. | Unit | [L151](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L151) |
| 195 | LoginCount_BucketedCorrectly | Login-count buckets (7 cases) | Seven login counts | Each falls in the right bucket — raw counts would blow up tag cardinality. | Unit | [L168](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L168) |
| 196 | ConnectionStrategy_PassedThrough | Strategy tag (4 cases) | Four strategies | Passed through unchanged. | Unit | [L184](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L184) |
| 197 | RiskConfidence_EmittedCorrectly | Risk confidence (3 cases) | Three confidence levels | Each emitted. | Unit | [L197](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L197) |
| 198 | NewDeviceCode_PassedThrough | New-device signal (3 cases) | Three codes | Passed through. | Unit | [L206](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L206) |
| 199 | NewDeviceCode_NullAssessment_EmitsUnknown | Missing risk assessment | No assessment object | `unknown` — the metric still lands. | Unit | [L214](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L214) |
| 200 | IsRefresh_DetectedFromProtocol | Refresh detection (4 cases) | Four protocols | Refresh correctly inferred. | Unit | [L228](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L228) |
| 201 | IsRefresh_NullTransaction_EmitsFalse | Missing transaction | No transaction | `false`, not unknown. | Unit | [L235](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L235) |
| 202 | Tenant_EmittedCorrectly | Tenant tag (2 cases) | Both tenants | Each emitted. | Unit | [L249](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L249) |
| 203 | ClientId_EmittedCorrectly | Client id (3 cases) | Three clients | Each emitted. | Unit | [L262](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L262) |
| 204 | ClientId_NullClient_EmitsUnknown | Missing client | No client | `unknown`. | Unit | [L269](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L269) |
| 205 | ClientName_Sanitized | Client-name sanitising (4 cases) | Four raw names | Sanitised before becoming a tag. | Unit | [L283](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L283) |
| 206 | NullAuthentication_HandlesGracefully | Missing auth block | No authentication object | Handled without throwing. | Unit | [L294](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L294) |
| 207 | OnException_IncrementsWithErrorTag_AndDoesNotThrow | Failure isolation | Force an exception inside the service | An error-tagged metric is emitted and nothing propagates — metrics never break a login. | Unit | [L308](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L308) |
| 208 | OnException_WithNullUser_IncrementsWithErrorTag_AndDoesNotThrow | Failure isolation, null user | Same with no user | Same. | Unit | [L321](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L321) |
| 209 | ProviderTenant_OmitsHighCardinalityTags | Provider cardinality guard | Emit for the provider tenant | High-cardinality tags are omitted. | Unit | [L339](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L339) |
| 210 | ProviderTenant_KeepsSharedTags | Provider tag floor | Emit for the provider tenant | The shared tags survive the omission. | Unit | [L350](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L350) |
| 211 | PatientTenant_IncludesAllTags | Patient tenant | Emit for the patient tenant | All tags present. | Unit | [L362](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L362) |
| 212 | AuthFactors_PwdOnly | Single factor | Password only | Emitted as `pwd`. | Unit | [L379](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L379) |
| 213 | AuthFactors_PwdThenMfaKnownType_JoinedInOrder | Factor ordering (2 cases) | Password then MFA | Joined in order — order carries the meaning. | Unit | [L388](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L388) |
| 214 | AuthFactors_MissingType_UsesNameOnly | Missing type | Factor with a name but no type | Name used alone. | Unit | [L400](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L400) |
| 215 | AuthFactors_EmptyMethods_EmitsNone | Empty list | No methods | `none`. | Unit | [L412](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L412) |
| 216 | AuthFactors_NullMethodsList_EmitsNone | Null list | Null methods | `none`. | Unit | [L419](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L419) |
| 217 | AuthFactors_NullName_Skipped | Null name | One factor has a null name | Skipped. | Unit | [L426](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L426) |
| 218 | AuthFactors_AllNamesNull_EmitsNone | All null names | Every name null | `none`. | Unit | [L438](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L438) |
| 219 | AuthFactors_UnrecognizedName_MappedToOther | Unknown name | An unrecognised factor name | `other` — new Auth0 factor types do not create unbounded tags. | Unit | [L446](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L446) |
| 220 | AuthFactors_UnrecognizedType_MappedToOther | Unknown type | An unrecognised type | `other`. | Unit | [L454](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L454) |
| 221 | AuthFactors_NullElement_Skipped_AndDoesNotThrow | Null element | A null entry in the list | Skipped, no throw. | Unit | [L462](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L462) |
| 222 | AuthFactors_MoreThanMax_KeepsFirstThreeInOrder | Truncation | More than three factors | The first three in order — the cardinality bound. | Unit | [L476](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L476) |
| 223 | AuthFactors_EmittedForBothTenants | Tenant coverage (2 cases) | Both tenants | Auth factors are emitted for both, unlike the high-cardinality tags in row 209. | Unit | [L491](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L491) |
| 224 | Latency_PwdAndMfa_EmitsHistogramWithTenantTag | MFA latency | Password and MFA timestamps present | A histogram is emitted with the tenant tag. | Unit | [L510](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L510) |
| 225 | Latency_EmittedForBothTenants | Tenant coverage (2 cases) | Both tenants | Emitted for both. | Unit | [L527](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L527) |
| 226 | Latency_SingleMethod_NoHistogram | One factor | Only one method | No histogram — there is no interval to measure. | Unit | [L543](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L543) |
| 227 | Latency_GarbageTimestamp_NoHistogram_EmitsUnparseableDrop_AndDoesNotThrow | Unparseable timestamp | A malformed timestamp | No histogram, an `unparseable` drop counter instead, no throw. | Unit | [L558](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L558) |
| 228 | Latency_MissingPwdTimestamp_NoHistogram_EmitsMissingPwdDrop | Missing password time | Password timestamp absent | `missing_pwd` drop. | Unit | [L580](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L580) |
| 229 | Latency_MissingMfaTimestamp_NoHistogram_EmitsMissingMfaDrop | Missing MFA time | MFA timestamp absent | `missing_mfa` drop. | Unit | [L600](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L600) |
| 230 | Latency_BothPwdAndMfaAbsent_NoHistogram_NoDrop | Neither present | Both absent | No histogram and no drop counter — an MFA-less login is not a measurement failure. | Unit | [L620](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L620) |
| 231 | Latency_NullElementInMethods_DoesNotThrow | Null element | Null entry in the method list | No throw. | Unit | [L640](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L640) |
| 232 | Latency_NegativeDelta_NoHistogram_EmitsNegativeDeltaDrop | Negative interval | MFA timestamp before the password one | `negative_delta` drop rather than a negative sample poisoning the histogram. | Unit | [L659](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L659) |
| 233 | ManyAuthFactors_ThreeOrMore_EmitsMetric | Many-factor signal | Three or more factors | The metric is emitted. | Unit | [L685](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L685) |
| 234 | ManyAuthFactors_FewerThanThree_DoesNotEmit | Threshold | Fewer than three | Not emitted. | Unit | [L702](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L702) |
| 235 | UnknownAuthFactors_UnrecognizedName_LogsRawNameAndType | Unknown-factor logging | An unrecognised name | The raw name and type are logged — how row 219's `other` bucket gets investigated. | Unit | [L723](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L723) |
| 236 | UnknownAuthFactors_UnrecognizedType_LogsRawNameAndType | Unknown-factor logging | An unrecognised type | Logged. | Unit | [L736](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L736) |
| 237 | UnknownAuthFactors_UnrecognizedNameWithoutType_LogsTypeAsNone | Missing type in the log | Unrecognised name, no type | Type logged as `none`. | Unit | [L749](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L749) |
| 238 | UnknownAuthFactors_MultipleUnknown_LogsAllJoined | Multiple unknowns | Several unrecognised factors | All joined into one log line. | Unit | [L762](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L762) |
| 239 | UnknownAuthFactors_AllWhitelisted_DoesNotLog | No-op case | All factors recognised | Nothing logged. | Unit | [L780](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L780) |
| 240 | UnknownAuthFactors_WhitelistedName_DoesNotLog | Whitelist (3 cases) | Three whitelisted names | Nothing logged. | Unit | [L806](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PostLoginMetricsServiceTests.cs#L806) |

---

## `tests/UnitTests/PatientLoginServiceTests.cs`

The patient login orchestrator: passwordless start by SMS and email, token exchange, refresh, and the OAuth authorize/callback pair. Roughly half the file exists to prove that every failure branch still emits an analytics event — a silent failure is treated as a defect in its own right.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 241 | Login_RequestsOfflineAccessScope_ToGetBackARefreshToken | Scope request | Log in | `offline_access` is requested — without it there is no refresh token and every session dies at access-token expiry. | Unit | [L244](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L244) |
| 242 | Login_WhenTokenIsSms_LookupPhoneNumber | SMS login | Log in with an SMS token | The phone number is looked up. | Unit | [L260](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L260) |
| 243 | Login_WhenTokenIsSmsAndLookupFails_ReturnNullToken | Lookup failure | The lookup fails | No token is returned. | Unit | [L268](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L268) |
| 244 | Login_WhenTokenIsSmsAndLookupFails_ReturnsError | Lookup failure, error | Same | An error is returned. | Unit | [L276](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L276) |
| 245 | SmsPasswordlessStart_ReturnsCorrectResult | SMS start (6 cases) | Six starting conditions | Each returns the right result. | Unit | [L290](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L290) |
| 246 | SmsPasswordlessStart_DualPatientAndProvider_FlagOn_ReturnsSuccess | Dual identity | Start for a dual patient/provider with the flag on | Succeeds as a patient. | Unit | [L316](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L316) |
| 247 | SmsPasswordlessStart_WhenNull_ReturnsNoPhone | No phone | The user has no phone | `NoPhone`. | Unit | [L338](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L338) |
| 248 | EmailPasswordlessStart_ReturnsCorrectResult | Email start (4 cases) | Four starting conditions | Each returns the right result. | Unit | [L354](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L354) |
| 249 | Login_WhenMfa_ShouldNotLogin | MFA gate | The user requires MFA | Login is not completed here — MFA must run through Auth0's flow. | Unit | [L371](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L371) |
| 250 | Login_WhenTokenIsSmsAndLookupFails_LogsFailureEvent | Event on failure | Lookup fails | A failure event is logged. | Unit | [L385](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L385) |
| 251 | Login_WhenIsMfa_LogsFailureEvent | Event on MFA | MFA required | A failure event is logged. | Unit | [L401](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L401) |
| 252 | Login_WhenSmsAndNullPhone_LogsFailureEvent | Event on no phone | Null phone | A failure event is logged. | Unit | [L432](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L432) |
| 253 | Login_WhenLoginFails_LogsFailureEvent | Event on generic failure | Login fails | A failure event is logged. | Unit | [L463](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L463) |
| 254 | Login_Success_LogsEvent | Event on success (2 cases) | Two successful logins | A success event is logged. | Unit | [L497](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L497) |
| 255 | Refresh_OnRefresh_LogsSuccessEvent | Refresh event | Refresh a token | A success event is logged. | Unit | [L528](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L528) |
| 256 | Refresh_OnNullTokenAndNoErrorFromAuth0_LogsFailureEvent | Silent Auth0 failure | Auth0 returns no token and no error | A failure event is still logged — the case that would otherwise vanish. | Unit | [L551](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L551) |
| 257 | Refresh_OnInvalidToken_LogsFailureEvent | Invalid token | Refresh with an invalid token | A failure event is logged. | Unit | [L581](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L581) |
| 258 | Refresh_OnNoPatientIdentifiers_LogsFailureEvent | Missing identifiers | The token carries no patient identifiers | A failure event is logged. | Unit | [L610](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L610) |
| 259 | Refresh_OnGeneralFailure_LogsFailureEvent | Generic failure | Refresh fails | A failure event is logged. | Unit | [L639](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L639) |
| 260 | SmsPasswordlessStart_OnSuccessfulSend_LogsSuccessEvent | SMS start event | Send succeeds | Success event. | Unit | [L790](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L790) |
| 261 | SmsPasswordlessStart_ForMfaUser_LogsFailureEvent | SMS start, MFA user | MFA user | Failure event. | Unit | [L815](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L815) |
| 262 | SmsPasswordlessStart_ForProviderUser_LogsFailureEvent | SMS start, provider | Provider user | Failure event. | Unit | [L843](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L843) |
| 263 | SmsPasswordlessStart_ForPracticeSsoDomain_LogsFailureEvent | SMS start, SSO domain | SSO-domain user | Failure event. | Unit | [L871](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L871) |
| 264 | SmsPasswordlessStart_ForUnknownUserName_LogsFailureEvent | SMS start, unknown user | Unknown username | Failure event. | Unit | [L899](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L899) |
| 265 | SmsPasswordlessStart_ForUserWithNoPhone_LogsFailureEvent | SMS start, no phone | No phone on file | Failure event. | Unit | [L914](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L914) |
| 266 | SmsPasswordlessStart_ForPhoneIsNotTextable_LogsFailureEvent | SMS start, landline | The phone cannot receive texts | Failure event. | Unit | [L942](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L942) |
| 267 | SmsPasswordlessStart_ForPUnexpectedException_LogsFailureEvent | SMS start, exception | An unexpected exception | Failure event — even the unhandled path reports. | Unit | [L970](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L970) |
| 268 | EmailPasswordlessStart_OnSuccessfulSend_LogsSuccessEvent | Email start event | Send succeeds | Success event. | Unit | [L1025](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1025) |
| 269 | EmailPasswordlessStart_ForMfaUser_LogsFailureEvent | Email start, MFA user | MFA user | Failure event. | Unit | [L1050](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1050) |
| 270 | EmailPasswordlessStart_ForUnknownUserName_LogsFailureEvent | Email start, unknown user | Unknown username | Failure event. | Unit | [L1078](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1078) |
| 271 | EmailPasswordlessStart_ForBadEmail_LogsFailureEvent | Email start, bad email | Malformed email | Failure event. | Unit | [L1093](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1093) |
| 272 | EmailPasswordlessStart_ForPUnexpectedException_LogsFailureEvent | Email start, exception | Unexpected exception | Failure event. | Unit | [L1121](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1121) |
| 273 | ExchangeForToken_WithValidAuthorizationCode_ReturnsToken | Code exchange | Exchange a valid code | A token comes back. | Unit | [L1175](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1175) |
| 274 | ExchangeForToken_WithError_ReturnsExpectedError | Exchange errors (2 cases) | Two error conditions | Each surfaces the expected error. | Unit | [L1207](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1207) |
| 275 | ExchangeForToken_UsesCorrectCallbackUrl | Callback URL | Exchange a code | The registered callback URL is sent — a mismatch is rejected by Auth0. | Unit | [L1232](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1232) |
| 276 | InitiateOAuthFlow_BuildsCorrectAuthorizeUrl | Authorize URL | Start the flow | The authorize URL is built correctly. | Unit | [L1333](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1333) |
| 277 | InitiateOAuthFlow_WithInvalidReturnTo_ReturnsError | Open-redirect guard | Start with an off-site `returnTo` | Error — the redirect allowlist. | Unit | [L1355](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1355) |
| 278 | InitiateOAuthFlow_WithNullTrackingId_OmitsExtTrackingIdFromUrl | Optional tracking | Null tracking id | Omitted from the URL rather than sent empty. | Unit | [L1380](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1380) |
| 279 | InitiateOAuthFlow_WithNullSessionId_OmitsExtSessionIdFromUrl | Optional session | Null session id | Omitted. | Unit | [L1391](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1391) |
| 280 | InitiateOAuthFlow_WithBothTrackingIdAndSessionIdNull_OmitsBothFromUrl | Both optional | Both null | Both omitted. | Unit | [L1402](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1402) |
| 281 | InitiateOAuthFlow_WithExistingTransactionId_ReusesItWithFreshState | Transaction continuity | Start with an existing transaction | The id is reused with a fresh state — one transaction can span several authorize attempts. | Unit | [L1416](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1416) |
| 282 | InitiateOAuthFlow_WithoutExistingTransactionId_GeneratesNewTransactionId | New transaction | No existing transaction | A new id is generated. | Unit | [L1439](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1439) |
| 283 | CompleteOAuthFlow_WithValidStateAndCode_ReturnsTokenAndPath | Callback happy path | Complete with a valid state and code | Token and return path. | Unit | [L1581](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1581) |
| 284 | CompleteOAuthFlow_WithStateNotFoundInDynamoDB_ReturnsStateNotFoundError | Unknown state | State missing from Dynamo | `StateNotFound` — a forged state cannot complete a flow. | Unit | [L1632](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1632) |
| 285 | CompleteOAuthFlow_WithNullOrEmptyState_ReturnsStateNotFoundWithoutLookup | Empty state (2 cases) | Null and empty state | `StateNotFound` without even hitting Dynamo. | Unit | [L1657](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1657) |
| 286 | CompleteOAuthFlow_WithMismatchedTransactionId_ReturnsTransactionIdMismatchError | Transaction binding | The transaction id does not match | Rejected — binds the callback to the browser that started it. | Unit | [L1676](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1676) |
| 287 | CompleteOAuthFlow_WithWrongTenantType_ReturnsTenantMismatchError | Tenant binding | A provider-tenant state on the patient flow | Rejected — the cross-tenant guard. | Unit | [L1711](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1711) |
| 288 | CompleteOAuthFlow_WhenTokenExchangeFails_ReturnsTokenExchangeFailedError | Exchange failure | The exchange fails | `TokenExchangeFailed`. | Unit | [L1744](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1744) |
| 289 | CompleteOAuthFlow_WithInvalidReturnToOnReverification_ReturnsInvalidReturnToError | Redirect guard on callback | An invalid `returnTo` at callback time | Rejected — the allowlist is re-checked on the way out, not just on the way in. | Unit | [L1780](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientLoginServiceTests.cs#L1780) |

---

## `tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs`

Patient account creation over the API, run three times over: phone start, email start, and the completion call — each with the same rejection matrix (bad email, Zocdoc-internal email, disposable domain, existing provider email, existing patient email, practice-SSO domain). Web and mobile are exercised separately because the realm differs.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 290 | CreatePasswordlessPatientUserStart_BlocksInternational_ThenBlocksUser | Abuse response | Attempt with an international number | Blocked, and the user is then blocked — the escalation, not just the rejection. | API | [L47](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L47) |
| 291 | CreatePasswordlessPatientUserStart_BadEmail_ReturnsBadRequest | Email validation (2 cases) | Two malformed emails | 400. | API | [L80](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L80) |
| 292 | CreatePasswordlessPatientUserStart_ZocdocEmail_ReturnsBadRequest | Internal-domain block | A `@zocdoc.com` email | 400 — staff cannot self-create patient accounts on their work email. | API | [L100](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L100) |
| 293 | CreatePasswordlessPatientUserStart_DisposableEmail_ReturnsBadRequest | Disposable domains | A throwaway-mail domain | 400. | API | [L120](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L120) |
| 294 | CreatePasswordlessPatientUserStart_ProviderEmailExists_ReturnsBadRequest | Provider collision | The email is a provider's | 400. | API | [L140](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L140) |
| 295 | CreatePasswordlessPatientUserStart_EmailHasPracticeSsoDomain_ReturnsBadRequest | SSO-domain block (3 cases) | Three SSO domains | 400. | API | [L176](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L176) |
| 296 | CreatePasswordlessPatientUserStart_ExistingPatient_AndEmailHasPracticeSsoDomain_ReturnsBadRequest | SSO domain, existing patient | An SSO-domain email that is already a patient | Still 400 on *creation* — the carve-out in the login path (row 18) does not extend to creating a second account. | API | [L199](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L199) |
| 297 | CreatePasswordlessPatientUserStart_PatientEmailExists_ReturnsBadRequest | Duplicate patient | The email is already a patient | 400. | API | [L241](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L241) |
| 298 | CreatePasswordlessPatientUserStart_NonTransferablePhoneNumber_ReturnsBadRequest | Phone transferability | A phone that cannot be transferred | 400. | API | [L277](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L277) |
| 299 | CreatePasswordlessPatientUserStart_PhoneBelongsToLockedPatient_ReturnsBadRequest | Locked-owner guard | The phone belongs to a locked patient | 400 — creating a new account is not a way around a lock. | API | [L317](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L317) |
| 300 | CreatePasswordlessPatientUserStart_ValidPhoneAndUsername_Success | Happy path | Valid phone and username | Succeeds. | API | [L346](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L346) |
| 301 | EmailCreatePasswordlessPatientUserStart_BadEmail_ReturnsBadRequest | Email start, validation (2 cases) | Two malformed emails | 400. | API | [L362](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L362) |
| 302 | EmailCreatePasswordlessPatientUserStart_ZocdocEmail_ReturnsBadRequest | Email start, internal domain | Zocdoc email | 400. | API | [L382](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L382) |
| 303 | EmailCreatePasswordlessPatientUserStart_DisposableEmail_ReturnsBadRequest | Email start, disposable | Disposable domain | 400. | API | [L402](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L402) |
| 304 | EmailCreatePasswordlessPatientUserStart_ProviderEmailExists_ReturnsBadRequest | Email start, provider collision | Provider email | 400. | API | [L422](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L422) |
| 305 | CreateEmailPasswordlessPatientUserStart_EmailHasPractieSsoDomain_ReturnsBadRequest | Email start, SSO domain | SSO domain | 400. | API | [L456](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L456) |
| 306 | EmailCreatePasswordlessPatientUserStart_PatientEmailExists_ReturnsBadRequest | Email start, duplicate | Existing patient email | 400. | API | [L480](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L480) |
| 307 | EmailCreatePasswordlessPatientUserStart_ValidUsername_Success | Email start, happy path | Valid email | Succeeds. | API | [L516](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L516) |
| 308 | CreatePasswordlessPatientUser_InvalidEmail | Completion, email validation (4 cases) | Four invalid emails | Rejected. | API | [L538](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L538) |
| 309 | CreatePasswordlessPatientUser_InvalidName | Name validation | An invalid name | Rejected. | API | [L564](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L564) |
| 310 | CreatePasswordlessPatientUser_ZocdocEmail_ReturnsBadRequest | Completion, internal domain | Zocdoc email | 400. | API | [L597](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L597) |
| 311 | CreatePasswordlessPatientUser_DisposableEmail_ReturnsBadRequest | Completion, disposable | Disposable domain | 400. | API | [L623](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L623) |
| 312 | CreatePasswordlessPatientUser_ProviderEmailExists_ReturnsBadRequest | Completion, provider collision | Provider email | 400. | API | [L649](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L649) |
| 313 | CreatePasswordlessPatientUser_InvalidEmail_ReturnsBadRequest | Completion, invalid email | Invalid email | 400. | API | [L689](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L689) |
| 314 | CreatePasswordlessPatientUser_PatientEmailExists_ReturnsBadRequest | Completion, duplicate | Existing patient email | 400 — the duplicate check runs again at completion, not just at start. | API | [L716](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L716) |
| 315 | CreatePasswordlessPatientUser_EmailHasPracticeSsoDomain_ReturnBadRequest | Completion, SSO domain | SSO domain | 400. | API | [L760](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L760) |
| 316 | CreatePasswordlessPatientUser_Web_MonolithCreateUserFails_UserCreationSuccess | Monolith decoupling, web | The monolith user creation fails | The auth-service account is still created — Auth0 is the source of truth and the monolith record is reconciled later. | API | [L790](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L790) |
| 317 | CreatePasswordlessPatientUser_Mobile_MonolithCreateUserFails_UserCreationSuccess | Monolith decoupling, mobile | Same on mobile | Same. | API | [L809](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L809) |
| 318 | CreatePasswordlessPatientUser_Web_NewUnlinkedPhone_Success | Web, fresh phone | Create with an unlinked phone | Succeeds. | API | [L827](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L827) |
| 319 | CreatePasswordlessPatientUser_Web_StealLinkedPhone_Success | Web, phone takeover | Create with a phone linked to someone else, verified | Succeeds and the phone moves — recycled numbers are handled deliberately. | API | [L852](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L852) |
| 320 | CreatePasswordlessPatientUser_Mobile_NewUnlinkedPhone_Success | Mobile, fresh phone | Same on mobile | Succeeds. | API | [L897](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L897) |
| 321 | CreatePasswordlessPatientUser_Mobile_StealLinkedPhone_Success | Mobile, phone takeover | Same on mobile | Succeeds. | API | [L918](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L918) |
| 322 | CreateEmailPasswordlessPatientUser_InvalidEmail | Email completion, validation (4 cases) | Four invalid emails | Rejected. | API | [L961](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L961) |
| 323 | CreateEmailPasswordlessPatientUser_InvalidName | Email completion, name | Invalid name | Rejected. | API | [L986](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L986) |
| 324 | CreatePasswordlessEmailPatientUser_ZocdocEmail_ReturnsBadRequest | Email completion, internal domain | Zocdoc email | 400. | API | [L1019](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1019) |
| 325 | CreateEmailPasswordlessPatientUser_DisposableEmail_ReturnsBadRequest | Email completion, disposable | Disposable domain | 400. | API | [L1044](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1044) |
| 326 | CreateEmailPasswordlessPatientUser_ProviderEmailExists_ReturnsBadRequest | Email completion, provider | Provider email | 400. | API | [L1069](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1069) |
| 327 | CreateEmailPasswordlessPatientUser_EmailHasPracticeSsoDomain_ReturnBadRequest | Email completion, SSO domain | SSO domain | 400. | API | [L1108](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1108) |
| 328 | CreateEmailPasswordlessPatientUser_PatientEmailExists_ReturnsBadRequest | Email completion, duplicate | Existing patient email | 400. | API | [L1143](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1143) |
| 329 | CreateEmailPasswordlessPatientUser_Web_MonolithCreateUserFails_UserCreationSuccess | Monolith decoupling, web | Monolith failure | Account still created. | API | [L1186](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1186) |
| 330 | CreateEmailPasswordlessPatientUser_Mobile_MonolithCreateUserFails_UserCreationSuccess | Monolith decoupling, mobile | Monolith failure | Account still created. | API | [L1204](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1204) |
| 331 | CreateEmailPasswordlessPatientUser_Web_Success | Email completion, web | Valid input | Succeeds. | API | [L1221](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1221) |
| 332 | CreateEmailPasswordlessPatientUser_Mobile_Success | Email completion, mobile | Valid input | Succeeds. | API | [L1245](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1245) |
| 333 | CreatePasswordlessPatientUser_InvalidRealm_Mobile_ReturnsBadRequest | Realm validation, mobile | An invalid realm | 400 — a client cannot pick an arbitrary Auth0 connection. | API | [L1267](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1267) |
| 334 | CreatePasswordlessPatientUser_InvalidRealm_Web_ReturnsBadRequest | Realm validation, web | Invalid realm | 400. | API | [L1297](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1297) |
| 335 | CreatePasswordlessPatientUserStart_PhoneOwnerLockedInUserLocking_ReturnsLocked | Cross-service lock | The phone owner is locked in user-locking | Returns locked. | API | [L1331](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1331) |
| 336 | CreatePasswordlessPatientUserStart_PhoneOwnerNotLocked_Success | Lock check, negative | Not locked | Succeeds. | API | [L1357](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/CreatePatientAccountApiTests.cs#L1357) |

---

## `tests/UnitTests/Login/PracticeLoginServiceTests.cs`

The provider-side mirror of `PatientLoginServiceTests`: password vs SSO routing, the identity-provider login, and the OAuth authorize/callback pair. Two things are unique to this file — a large `login_hint` sanitising block (rows 357–363), and the monolith JWT exchange that only database-connection users go through (373–375).

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 337 | PracticeLoginStart_BadEmail | Email validation | Start with a malformed email | Rejected. | Unit | [L120](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L120) |
| 338 | PracticeLoginStart_PasswordLogin | Password routing (4 cases) | Four password-login emails | Routed to the password flow. | Unit | [L132](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L132) |
| 339 | PracticeLoginStart_SSOLogin | SSO routing (4 cases) | Four SSO-domain emails | Routed to the IdP — the fork that decides whether a provider ever sees a password box. | Unit | [L147](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L147) |
| 340 | PracticeLoginStart_SSOLogin_IncludesTrackingParams | Tracking on SSO | Start an SSO login | Tracking params ride along. | Unit | [L171](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L171) |
| 341 | PracticeLoginStart_SSOLogin_IncludesCorrelationIdFromFactory | Correlation id | Start an SSO login | The factory's correlation id is used — how a login is traced across services. | Unit | [L199](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L199) |
| 342 | PracticeLoginStart_SSOLogin_WithBothTrackingIdAndSessionIdNull_OmitsBothFromUrl | Optional tracking | Both ids null | Both omitted. | Unit | [L228](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L228) |
| 343 | PracticeIdentityProviderLogin_Success | IdP login | Complete an IdP login | Succeeds. | Unit | [L256](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L256) |
| 344 | PracticeIdentityProviderLoginV2_Success | IdP login v2 | Complete on v2 | Succeeds. | Unit | [L313](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L313) |
| 345 | PracticeIdentityProviderLogin_UserHasPracticeStaffId_Success | Staff linkage | The user already has a practice-staff id | Succeeds. | Unit | [L361](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L361) |
| 346 | PracticeIdentityProviderLogin_MonolithLoginError | Monolith failure (1 case) | The monolith login errors | Surfaced — unlike patient creation (row 316), provider login does *not* proceed without the monolith. | Unit | [L432](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L432) |
| 347 | PracticeIdentityProviderLogin_PracticeStaffLinkFailed | Staff link failure | Linking the staff record fails | Error. | Unit | [L489](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L489) |
| 348 | PracticeIdentityProviderLogin_NoPracticeId | Missing practice | No practice id | Error. | Unit | [L541](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L541) |
| 349 | PracticeIdentityProviderLogin_Auth0AuthorizationCodeError | Code error (1 case) | Auth0 returns a code error | Surfaced. | Unit | [L590](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L590) |
| 350 | PracticeIdentityProviderLoginV2_Auth0AuthorizationCodeError | Code error, v2 (1 case) | Same on v2 | Surfaced. | Unit | [L618](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L618) |
| 351 | InitiateOAuthFlow_InvalidReturnTo_ReturnsError | Open-redirect guard | Off-site `returnTo` | Error. | Unit | [L646](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L646) |
| 352 | InitiateOAuthFlow_ValidReturnTo_StoresStateInDynamo | State persistence | Start the flow | The state is written to Dynamo. | Unit | [L659](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L659) |
| 353 | InitiateOAuthFlow_ValidReturnTo_ReturnsAuthorizeUrl | Authorize URL | Start the flow | The URL is returned. | Unit | [L683](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L683) |
| 354 | InitiateOAuthFlow_ValidReturnTo_IncludesTrackingParams | Tracking | Start the flow | Tracking params included. | Unit | [L710](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L710) |
| 355 | InitiateOAuthFlow_ValidReturnTo_IncludesCorrelationIdFromFactory | Correlation id | Start the flow | Factory id used. | Unit | [L732](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L732) |
| 356 | InitiateOAuthFlow_WithBothTrackingIdAndSessionIdNull_OmitsBothFromUrl | Optional tracking | Both null | Both omitted. | Unit | [L755](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L755) |
| 357 | InitiateOAuthFlow_WithLoginHint_IncludesLoginHintInUrl | Login hint | Start with a hint | Included — pre-fills the IdP's username box. | Unit | [L779](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L779) |
| 358 | InitiateOAuthFlow_WithoutLoginHint_OmitsLoginHintFromUrl | No hint | No hint supplied | Omitted. | Unit | [L796](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L796) |
| 359 | InitiateOAuthFlow_WithEmptyOrWhitespaceLoginHint_OmitsLoginHintFromUrl | Blank hint (2 cases) | Empty and whitespace | Omitted. | Unit | [L812](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L812) |
| 360 | InitiateOAuthFlow_WithUnsanitizedLoginHint_SanitizesBeforeForwarding | Hint sanitising (3 cases) | Three unsanitised hints | Sanitised before reaching the IdP — the hint is user-controlled and lands in a URL. | Unit | [L829](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L829) |
| 361 | InitiateOAuthFlow_WithMalformedLoginHint_OmitsLoginHintFromUrl | Malformed hint (4 cases) | Four malformed hints | Dropped entirely. | Unit | [L850](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L850) |
| 362 | InitiateOAuthFlow_WithExcessivelyLongLoginHint_OmitsLoginHintFromUrl | Length bound | An overlong hint | Dropped. | Unit | [L865](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L865) |
| 363 | InitiateOAuthFlow_WithDisplayNameFormLoginHint_OmitsLoginHintFromUrl | Display-name form (4 cases) | `Name <email>` style hints | Dropped rather than partially parsed. | Unit | [L884](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L884) |
| 364 | InitiateOAuthFlow_WithExistingCookie_ReusesTransactionIdWithFreshState | Transaction continuity | An existing transaction cookie | Reused with a fresh state. | Unit | [L899](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L899) |
| 365 | InitiateOAuthFlow_WithoutExistingCookie_GeneratesNewTransactionId | New transaction | No cookie | New id generated. | Unit | [L931](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L931) |
| 366 | CompleteOAuthFlow_StateNotFound_ReturnsError | Unknown state | State not in Dynamo | Error. | Unit | [L950](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L950) |
| 367 | CompleteOAuthFlow_StateKeyedLookup_NullOrEmptyState_ReturnsStateNotFound | Empty state (2 cases) | Null and empty | `StateNotFound`. | Unit | [L980](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L980) |
| 368 | CompleteOAuthFlow_TenantMismatch_ReturnsError | Tenant binding | Wrong tenant | Error. | Unit | [L1005](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L1005) |
| 369 | CompleteOAuthFlow_TokenExchangeFailed_ReturnsError | Exchange failure | Exchange fails | Error. | Unit | [L1044](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L1044) |
| 370 | CompleteOAuthFlow_InvalidReturnToOnReverification_ReturnsError | Redirect guard on callback | Invalid `returnTo` at callback | Error. | Unit | [L1083](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L1083) |
| 371 | CompleteOAuthFlow_Success_ReturnsTokenAndPathAndIdentifiers | Callback happy path | Complete the flow | Token, path, and identifiers. | Unit | [L1137](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L1137) |
| 372 | CompleteOAuthFlow_Success_LogsProviderLoginSuccessEvent | Success event | Complete the flow | A provider login-success event is logged. | Unit | [L1217](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L1217) |
| 373 | CompleteOAuthFlow_DatabaseUser_Success_ReturnsMonolithJwt | Monolith exchange | Complete for a database-connection user | A monolith JWT is returned alongside the Auth0 one. | Unit | [L1282](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L1282) |
| 374 | CompleteOAuthFlow_DatabaseUser_NoAspnetCloudId_DoesNotCallMonolithExchange | Exchange precondition | The user has no aspnet cloud id | The monolith exchange is skipped rather than attempted and failed. | Unit | [L1361](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L1361) |
| 375 | CompleteOAuthFlow_DatabaseUser_MonolithExchangeFailed_ReturnsError | Exchange failure | The monolith exchange fails | Error — provider login is hard-coupled to the monolith here. | Unit | [L1430](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L1430) |
| 376 | CompleteOAuthFlow_TokenExchangeFailed_LogsFailureEvent | Failure event | Exchange fails | A failure event is logged. | Unit | [L1506](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L1506) |
| 377 | CompleteOAuthFlow_StateKeyedLookup_TransactionIdMismatch_ReturnsError | Transaction binding | Transaction id mismatch on the state-keyed lookup | Error. | Unit | [L1548](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeLoginServiceTests.cs#L1548) |

---

## `tests/UnitTests/Auth0/Auth0ServiceTests.cs`

The Auth0 Management/Authentication API wrapper. The largest block is passwordless account creation across three starting states — the phone is unlinked, already linked to another passwordless user, or linked to an email user — each with a correct-OTP and a wrong-OTP variant.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 378 | CreateEmailUser_Success | Email user creation | Create an email user | Succeeds. | Unit | [L41](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L41) |
| 379 | UpdatePhone_NoOneOwnsPhone | Phone update, free number | Update to an unowned phone | Succeeds. | Unit | [L52](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L52) |
| 380 | UpdatePhone_TransfererHasPhone | Phone update, self | The caller already owns it | Handled. | Unit | [L66](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L66) |
| 381 | UpdatePhone_TargetPhoneIsLinked | Phone update, linked | The target is linked elsewhere | Handled. | Unit | [L81](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L81) |
| 382 | UpdatePhone_UserInUnexpectedState | Unexpected state (2 cases) | Two inconsistent user states | Rejected rather than silently repaired. | Unit | [L97](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L97) |
| 383 | UpdatePhone_UserHasUnexpectedPatientId | Patient-id mismatch | The user carries an unexpected patient id | Rejected — prevents attaching a phone to the wrong patient. | Unit | [L110](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L110) |
| 384 | VerifyOneTimePassword_Success | OTP verify | Verify a correct OTP | Succeeds. | Unit | [L119](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L119) |
| 385 | VerifyOneTimePassword_ThrowsException | OTP verify errors (6 cases) | Six Auth0 error conditions | Each throws the mapped exception. | Unit | [L136](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L136) |
| 386 | RefreshAccessToken_GivenNoError_ReturnsToken | Refresh | Refresh cleanly | A token comes back. | Unit | [L152](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L152) |
| 387 | RefreshAccessToken_GivenAuth0Error_ReturnsError | Refresh, Auth0 error | Auth0 errors | Error returned. | Unit | [L165](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L165) |
| 388 | RefreshAccessToken_GivenGeneralError_Returns | Refresh, general error | A general error | Returned. | Unit | [L178](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L178) |
| 389 | RefreshAccessToken_GivenNullRefreshToken_ReturnsError | Missing token | Null refresh token | Error without calling Auth0. | Unit | [L191](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L191) |
| 390 | DeleteUserByAuth0UserId_Success | User deletion | Delete by Auth0 id | Succeeds. | Unit | [L201](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L201) |
| 391 | UpdateMfaStatus_Success | MFA toggle | Update MFA status | Succeeds. | Unit | [L210](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L210) |
| 392 | PatientSendOtpToPhone_Auth0ClientException | SMS OTP errors (2 cases) | Two Auth0 client exceptions | Handled. | Unit | [L222](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L222) |
| 393 | PatientSendOtpToEmail_Auth0ClientException | Email OTP error (1 case) | An Auth0 client exception | Handled. | Unit | [L234](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L234) |
| 394 | UpdatePatientIdTest | Patient id update | Set the patient id on the Auth0 user | Succeeds. | Unit | [L246](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L246) |
| 395 | UpdateUserAccountId_Success | Account id update | Set the user-account id | Succeeds. | Unit | [L256](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L256) |
| 396 | UpdateUserAccountId_ClientThrows_ShouldThrowException | Account id failure | The client throws | The exception propagates rather than being swallowed. | Unit | [L272](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L272) |
| 397 | GetBlockedUsers_FiltersBasedOnUserBlocks | Blocked-user listing | List blocked users | Filtered on the user-block records. | Unit | [L285](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L285) |
| 398 | CreateSmsPasswordlessAccount_UnlinkedPhone_CorrectOtp | SMS create, free phone | Correct OTP, unlinked phone | Account created. | Unit | [L316](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L316) |
| 399 | CreateSmsPasswordlessAccount_AlreadyLinkedPhone_CorrectOtp | SMS create, linked phone | Correct OTP, phone linked elsewhere | Account created and the phone moves. | Unit | [L348](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L348) |
| 400 | CreateSmsPasswordlessAccount_PhoneLinkedToEmailUserAlready_CorrectOtp | SMS create, email user owns it | Correct OTP, phone on an email user | Handled — the trickiest of the three states. | Unit | [L384](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L384) |
| 401 | CreateSmsPasswordlessAccount_UnlinkedPhone_IncorrectOtp | Wrong OTP, free phone (5 cases) | Five wrong-OTP conditions | Rejected. | Unit | [L420](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L420) |
| 402 | CreateSmsPasswordlessAccount_AlreadyLinkedPhone_IncorrectOtp | Wrong OTP, linked phone (5 cases) | Five wrong-OTP conditions | Rejected — a wrong OTP never moves a phone. | Unit | [L457](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L457) |
| 403 | CreateSmsPasswordlessAccount_PhoneLinkedToEmailUserAlready_IncorrectOtp | Wrong OTP, email user owns it (5 cases) | Five wrong-OTP conditions | Rejected. | Unit | [L498](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L498) |
| 404 | CreateSmsPasswordlessAccount_EmailUserHasPatientId_ThrowsException | Existing patient collision | The email user already has a patient id | Throws rather than merging two patients. | Unit | [L534](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L534) |
| 405 | CreateEmailPasswordlessAccount_CorrectOtp | Email create | Correct OTP | Account created. | Unit | [L553](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L553) |
| 406 | CreateEmailPasswordlessAccount_WrongOtp | Email create, wrong OTP (5 cases) | Five wrong-OTP conditions | Rejected. | Unit | [L585](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L585) |
| 407 | CreateEmailPasswordlessAccount_UserHasPatientId_ThrowsException | Existing patient collision | The user already has a patient id | Throws. | Unit | [L604](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0ServiceTests.cs#L604) |

---

## `tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs`

Real DynamoDB. Phone ownership is the hardest piece of state in the service — a phone number is unique across patients, gets recycled by carriers, and its transferability is tied to whether the owner has MFA. Most of this file is the transfer state machine.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 408 | PatientPhoneDynamoDto_SatisfiesNullConstraints | Schema contract | Inspect the DTO | Null constraints hold. | Integration | [L37](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L37) |
| 409 | GetPhoneAsync_CreatesNewPhoneForPatient | Read-through create | Get a phone for a new patient | A record is created. | Integration | [L56](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L56) |
| 410 | GetByPatientAsync_WhenRecordDoesNotExist_ReturnsNull | Missing record | Read a nonexistent record | Null. | Integration | [L83](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L83) |
| 411 | SetPhoneAsync_ChangesOwnPhone | Self change | Change your own phone | Updated. | Integration | [L90](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L90) |
| 412 | SetPhoneAsync_DoesNotRepeatDynamoUpdates | Write economy | Set the same phone twice | No redundant write. | Integration | [L127](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L127) |
| 413 | SetPhoneAsync_TransfersPhoneFromOtherPatient | Transfer | Take a phone from another patient | Transferred. | Integration | [L153](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L153) |
| 414 | SetPhoneAsync_HasPhoneAndTransfersPhoneFromOtherPatient | Transfer while owning | Already have a phone, take another patient's | Both sides updated. | Integration | [L182](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L182) |
| 415 | SetPhoneAsync_TakeAPhoneThatWasPreviouslyAssignedToUser | Re-take | Take back a previously held phone | Works. | Integration | [L221](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L221) |
| 416 | SetPhoneAsync_LosesPhoneThenTakesNewPhone | Lose then take | Lose a phone, then take a new one | Consistent. | Integration | [L267](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L267) |
| 417 | SetPhoneAsync_TakesPhoneThatWasOnceOwned | Historic ownership | Take a phone once owned | Works — history does not block reassignment. | Integration | [L305](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L305) |
| 418 | SetPhoneAsync_RemovesPhoneFromSelf | Removal | Remove your own phone | Removed. | Integration | [L342](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L342) |
| 419 | SetPhoneAsync_ThrowsForFailedConstraint_Auth0UserIdDiffers | Conditional write | The Auth0 user id has changed underneath | Throws — the optimistic-concurrency guard. | Integration | [L374](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L374) |
| 420 | SetPhoneAsync_ThrowsForFailedConstraint_PhoneNotUnique | Uniqueness | Two patients race for one number | Throws; the uniqueness constraint is enforced by Dynamo, not by a read-then-write. | Integration | [L402](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L402) |
| 421 | SetPhoneAsync_ThrowsForIfSelfHasNonTransferablePhone | Non-transferable, self | Your current phone is non-transferable | Throws — an MFA-protected phone cannot be silently dropped. | Integration | [L419](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L419) |
| 422 | SetPhoneAsync_ThrowsForIfPhoneIsNotTransferable | Non-transferable, target | The target phone is non-transferable | Throws. | Integration | [L447](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L447) |
| 423 | SetPhoneAsync_DefaultsToTransferable_IfIsTransferablIsNull | Default | The flag is null on an old record | Treated as transferable — the back-compat default for records predating the field. | Integration | [L475](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L475) |
| 424 | BatchSetPhoneAsync_WorksWithManyParallelRequests | Concurrency | Many parallel batch sets | All consistent. | Integration | [L504](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L504) |
| 425 | DeletePatientPhoneAsync_DeletesPatientPhone | Deletion | Delete a phone | Deleted. | Integration | [L527](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L527) |
| 426 | DeletePatientPhoneAsync_NoExistingPhone_DoesNothing | Idempotent delete | Delete a nonexistent phone | No-op. | Integration | [L550](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L550) |
| 427 | UpdateMfaStatusAsync_UpdatesPhoneTransferabilityStatus | MFA drives transferability (6 cases) | Six MFA transitions | Transferability follows MFA — the coupling that rows 421/422 enforce. | Integration | [L594](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L594) |
| 428 | UpdateMfaStatusAsync_WhenPhoneRecordDoesNotExistForPatient_ThrowsException | Missing record | Update MFA with no phone record | Throws. | Integration | [L616](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L616) |
| 429 | UpdateMfaStatusAsync_WhenPhoneHasBeenDeleted_ThrowsException | Deleted record | Update MFA on a deleted phone | Throws. | Integration | [L626](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L626) |
| 430 | BatchTouchPhonesAsync_WorksWithBatch | Batch touch | Touch a batch | Works. | Integration | [L642](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L642) |
| 431 | BatchTouchPhonesAsync_WorksOnTouchingPhoneRecordAgain | Repeat touch | Touch again | Works. | Integration | [L667](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L667) |
| 432 | BatchTouchPhonesAsync_WorksWithNullPhone | Null phone | Touch a record with a null phone | Works. | Integration | [L698](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L698) |
| 433 | BatchTouchPhonesAsync_DoesNothingWithNonExistentPatient | Unknown patient | Touch an unknown patient | No-op. | Integration | [L720](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientPhoneDynamoPersistenceTests.cs#L720) |

---

## `tests/UnitTests/User/UserCreationServiceTests.cs`

Account creation orchestration, symmetric across SMS and email. The recurring theme is that monolith failures do not fail creation (rows 444, 445, 452, 453) while Auth0 or profile failures do. Rows 447 and 455 are large tables pinning which inputs are recognised as test patients.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 434 | SmsPasswordlessAccountCreationStart_ValidUsername_ValidSendOtpResult_Success | SMS start | Valid username, OTP sent | Succeeds. | Unit | [L97](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L97) |
| 435 | SmsPasswordlessAccountCreationStart_InvalidUsername | SMS start, bad username (6 cases) | Six invalid usernames | Rejected. | Unit | [L124](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L124) |
| 436 | SmsPasswordlessAccountCreationStart_ValidUsername_BadOtpResult | SMS start, OTP failure (5 cases) | Five OTP failures | Rejected. | Unit | [L160](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L160) |
| 437 | EmailPasswordlessAccountCreationStart_ValidUsername_ValidSendOtpResult_Success | Email start | Valid email, OTP sent | Succeeds. | Unit | [L186](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L186) |
| 438 | EmailPasswordlessAccountCreationStart_InvalidUsername | Email start, bad username (6 cases) | Six invalid emails | Rejected. | Unit | [L212](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L212) |
| 439 | EmailPasswordlessAccountCreationStart_ValidUsername_BadOtpResult | Email start, OTP failure (2 cases) | Two OTP failures | Rejected. | Unit | [L237](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L237) |
| 440 | CreateSmsPasswordlessAccount_FailedUsernameValidation | SMS create, username (6 cases) | Six invalid usernames | Rejected at completion too. | Unit | [L269](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L269) |
| 441 | CreateSmsPasswordlessAccount_FailedProfileValidation | SMS create, profile (5 cases) | Five invalid profiles | Rejected. | Unit | [L291](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L291) |
| 442 | CreateSmsPasswordlessAccount_BadOtp | SMS create, bad OTP (5 cases) | Five OTP failures | Rejected. | Unit | [L319](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L319) |
| 443 | CreateSmsPasswordlessAccount_CreateProfileFails | Profile creation failure (4 cases) | Four failure modes | Creation fails — unlike the monolith, the profile is a hard dependency. | Unit | [L349](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L349) |
| 444 | CreateSmsPasswordlessAccount_CreateMonolithUserFails_UserCreationSuccess | Monolith decoupling | The monolith user creation fails | Creation still succeeds. | Unit | [L378](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L378) |
| 445 | CreateSmsPasswordlessAccount_LinkMonolithUserToPatientFails_UserCreationSuccess | Monolith link failure | Linking fails | Creation still succeeds. | Unit | [L436](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L436) |
| 446 | CreateSmsPasswordlessAccount_Success | SMS create | Everything valid | Succeeds. | Unit | [L494](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L494) |
| 447 | CreateSmsPasswordlessAccount_TestPatient | Test-patient detection (21 cases) | Twenty-one inputs | Each classified as test or real — a wrong entry either leaks synthetic accounts into production metrics or marks a real patient as a test. | Unit | [L562](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L562) |
| 448 | CreateEmailPasswordlessAccount_FailedUsernameValidation | Email create, username (6 cases) | Six invalid emails | Rejected. | Unit | [L609](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L609) |
| 449 | CreateEmailPasswordlessAccount_FailedProfileValidation | Email create, profile (5 cases) | Five invalid profiles | Rejected. | Unit | [L631](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L631) |
| 450 | CreateEmailPasswordlessAccount_BadOtp | Email create, bad OTP (5 cases) | Five OTP failures | Rejected. | Unit | [L658](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L658) |
| 451 | CreateEmailPasswordlessAccount_CreateProfileFails | Profile failure (4 cases) | Four failure modes | Creation fails. | Unit | [L688](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L688) |
| 452 | CreateEmailPasswordlessAccount_CreateMonolithUserFails_UserCreationSuccess | Monolith decoupling | Monolith creation fails | Creation succeeds. | Unit | [L717](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L717) |
| 453 | CreateEmailPasswordlessAccount_LinkMonolithUserToPatientFails_UserCreationSuccess | Monolith link failure | Linking fails | Creation succeeds. | Unit | [L772](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L772) |
| 454 | CreateEmailPasswordlessAccount_Success | Email create | Everything valid | Succeeds. | Unit | [L828](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L828) |
| 455 | CreateEmailPasswordlessAccount_TestPatient | Test-patient detection (13 cases) | Thirteen inputs | Each classified — the email counterpart to row 447. | Unit | [L886](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserCreationServiceTests.cs#L886) |

---

## `tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs`

The browser login and refresh endpoints — cookie issuance, expiry, and the Auth0 parameter pass-through. Four tests are `RealOnly` because they assert on events that only the deployed stack produces.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 456 | OauthToken_ReturnsErrorMessages | Error messages (3 cases) | Three failing token requests | The expected messages come back. | API | [L26](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L26) |
| 457 | OauthToken_ReturnsErrorCodes | Error codes (3 cases) | Three failing requests | The expected codes come back. | API | [L48](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L48) |
| 458 | OauthToken_PassesThroughParametersToAuth0 | Parameter forwarding (9 cases) | Nine parameters | Each reaches Auth0 unchanged. | API | [L76](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L76) |
| 459 | ReturnsCookiesForEmail | Cookie issuance, email | Log in by email | Cookies are set. | API | [L96](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L96) |
| 460 | Login_LogsEventOnSuccess | Success event (`RealOnly`) | Log in against the deployment | An event lands. | API | [L141](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L141) |
| 461 | Login_LogsEventOnFailure | Failure event (`RealOnly`) | Fail a login | An event lands. | API | [L169](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L169) |
| 462 | Login_ReturnsExpiresInSeconds | Expiry contract | Log in | `expires_in` is returned — clients depend on it to schedule refresh. | API | [L202](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L202) |
| 463 | ReturnsCookiesForSms | Cookie issuance, SMS | Log in by SMS | Cookies are set. | API | [L218](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L218) |
| 464 | RefreshToken_ReturnsForbiddenForBadRequestToken | Bad refresh token | Refresh with a bad token | 403. | API | [L262](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L262) |
| 465 | RefreshToken_ReturnsExpiresInSeconds | Expiry on refresh | Refresh | `expires_in` returned. | API | [L276](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L276) |
| 466 | RefreshToken_LogsEventOnSuccess | Refresh event (`RealOnly`) | Refresh | An event lands. | API | [L303](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L303) |
| 467 | RefreshToken_LogsEventOnFailure | Refresh failure event (`RealOnly`) | Fail a refresh | An event lands. | API | [L340](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L340) |
| 468 | RefreshToken_ReturnsNewAccessTokenForValidRefreshToken | Refresh happy path | Refresh with a valid token | A new access token. | API | [L378](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L378) |
| 469 | Login_FailsOnUnknownUserNameMapping | Unknown user (`RealOnly`) | Log in as an unmapped username | Fails. | API | [L423](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L423) |
| 470 | Login_FailsOnMissingAccessTokenFromAuth0 | Missing access token | Auth0 returns no access token | Login fails. | API | [L438](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L438) |
| 471 | Login_SucceedsOnMissingRefreshTokensFromAuth0 | Missing refresh token | Auth0 returns no refresh token | Login still succeeds — degraded rather than blocked, the session just cannot be extended. | API | [L455](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L455) |
| 472 | Refresh_FailsOnMissingTokensFromAuth0 | Missing tokens on refresh (2 cases) | Two missing-token shapes | Refresh fails. | API | [L495](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L495) |
| 473 | Login_FailsOnMissingUsername_ReturnsBadRequest | Required field | No username | 400. | API | [L526](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L526) |
| 474 | Login_FailsOnEmptyUsername_ReturnsBadRequest | Required field | Empty username | 400. | API | [L551](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L551) |
| 475 | Login_FailsOnMissingOtp_ReturnsBadRequest | Required field | No OTP | 400. | API | [L577](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L577) |
| 476 | Login_FailsOnMissingRealm_ReturnsBadRequest | Required field | No realm | 400. | API | [L602](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/WebSiteLoginAndRefreshTests.cs#L602) |

---

## `tests/ApiTests/ReconciliatorApiTests.cs`

The reconciliation endpoints that back-office jobs use to sync patients, provider usernames, MFA status, and phone records. Every endpoint has its unauthorized and forbidden case pinned before its success case — these are privileged bulk-mutation routes.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 477 | ReconcilePatients_TestResponseStatus | Response codes (4 cases) | Four request shapes | Correct statuses. | API | [L27](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L27) |
| 478 | ReconcilePatients_Success | Patient reconciliation | Reconcile patients | Succeeds. | API | [L51](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L51) |
| 479 | UpdateMfaStatus_WithNoMatchingUser_ReturnsUnauthorized | Unknown user | No matching user | 401. | API | [L170](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L170) |
| 480 | UpdateMfaStatus_UserMissingRole_ReturnsForbidden | Role gate | Missing role | 403. | API | [L184](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L184) |
| 481 | UpdateMfaStatus_UserChangingMfaStatus_Works | MFA update (3 cases) | Three transitions | Applied. | API | [L202](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L202) |
| 482 | ReconcileProviderUsername_Unauthorized | Auth gate | No token | 401. | API | [L239](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L239) |
| 483 | ReconcileProviderUsername_Forbidden | Role gate | Wrong role | 403. | API | [L252](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L252) |
| 484 | ReconcileProviderUsername_Success | Username reconciliation (`RealOnly`) | Reconcile | Succeeds. | API | [L266](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L266) |
| 485 | BatchDeleteProviderUsernames_Unauthorized | Auth gate | No token | 401. | API | [L299](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L299) |
| 486 | BatchDeleteProviderUsernames_Forbidden | Role gate | Wrong role | 403. | API | [L312](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L312) |
| 487 | BatchDeleteProviderUsernames_Success | Bulk delete (`RealOnly`) | Delete a batch | Succeeds. | API | [L326](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L326) |
| 488 | BatchDeleteProviderUsernames_DeletesDdbRowsAndAuth0Users | Two-system delete (`RealOnly`) | Delete a batch | Both the Dynamo rows and the Auth0 users go — a half-delete would leave a login that resolves to nothing. | API | [L394](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L394) |
| 489 | BatchTouchPhonesByPatientIds_Unauthorized | Auth gate | No token | 401. | API | [L455](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L455) |
| 490 | BatchTouchPhonesByPatientIds_Forbidden | Role gate | Wrong role | 403. | API | [L465](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L465) |
| 491 | BatchTouchPhonesByPatientIds_ValidPhoneRecord_Success | Phone touch (`RealOnly`) | Touch valid records | Succeeds. | API | [L476](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L476) |
| 492 | BatchTouchPhonesByPatientIds_NonExistentPatient_DoesNothing | Unknown patient (`RealOnly`) | Touch an unknown patient | No-op rather than an error — the batch job tolerates stale ids. | API | [L506](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L506) |
| 493 | BatchTouchUsersByPatientIds_Unauthorized | Auth gate | No token | 401. | API | [L531](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L531) |
| 494 | BatchTouchUsersByPatientIds_Forbidden | Role gate | Wrong role | 403. | API | [L541](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L541) |
| 495 | BatchTouchUsersByPatientIds_ValidUserRecord_Success | User touch | Touch valid records | Succeeds. | API | [L552](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ReconciliatorApiTests.cs#L552) |

---

## `tests/ApiTests/UserApi/UserApiTests.cs`

The user-lookup and user-deletion API. `GetCurrentUser` is patient-only — a practice or CSR token is explicitly rejected rather than resolved to whatever the token happens to identify.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 496 | BatchGetUsers_TestNotFound | Missing users (2 cases) | Two not-found shapes | Handled. | API | [L23](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L23) |
| 497 | BatchGetUsersByPatientId_TestUnhappyPaths | Unhappy paths (2 cases) | Two bad requests | Rejected. | API | [L47](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L47) |
| 498 | BatchGetUsersByPatientId_WhenTooManyPatientIdsArePassedIn_BadRequest | Batch bound | Over the cap | 400. | API | [L70](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L70) |
| 499 | BatchGetUsersByPatientId_WorksWithCorrectRoleWhenPatientExists | Batch read | Correct role, existing patient | Succeeds. | API | [L88](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L88) |
| 500 | GetCurrentUser_ReturnsLoggedInPatient | Self lookup | Read as a patient | The patient comes back. | API | [L132](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L132) |
| 501 | GetCurrentUser_NotLoggedIn | Auth gate | No session | Rejected. | API | [L151](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L151) |
| 502 | GetCurrentUser_ReturnsUnauthorized_WhenLoggedInAsPractice | Wrong identity type | Practice token | 401 — not silently resolved to a practice user. | API | [L161](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L161) |
| 503 | GetCurrentUser_ReturnsUnauthorized_WhenLoggedInAsCsr | Wrong identity type | CSR token | 401. | API | [L172](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L172) |
| 504 | GetCurrentUser_ReturnsUnauthorized_WhenPatientNotFound | Missing patient | The patient does not exist | 401 rather than 404 — the endpoint does not confirm which patient ids exist. | API | [L182](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L182) |
| 505 | DeletePatientUser_NoUser_ReturnsUnauthorized | Auth gate | No user | 401. | API | [L192](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L192) |
| 506 | DeletePatientUser_UserNoRole_ReturnsForbidden | Role gate | No role | 403. | API | [L202](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L202) |
| 507 | DeletePatientUser_AuthReconciliatorWriteRole_DeletesPatientData | Patient deletion | Delete with the reconciliator write role | The patient data is deleted. | API | [L214](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L214) |
| 508 | DeletePracticeUser_Unauthorized | Auth gate | No token | 401. | API | [L255](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L255) |
| 509 | DeletePracticeUser_Forbidden | Role gate | Wrong role | 403. | API | [L267](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L267) |
| 510 | DeletePracticeUser_Works | Practice deletion | Delete a practice user | Succeeds. | API | [L280](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L280) |
| 511 | UpdatePracticeUserRoles_Unauthorized | Auth gate | No token | 401. | API | [L296](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L296) |
| 512 | UpdatePracticeUserRoles_Forbidden | Role gate | Wrong role | 403 — the endpoint that grants roles is itself role-gated. | API | [L310](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L310) |
| 513 | UpdatePracticeUserRoles_UserDoesNotExist_ReturnsNotFound | Unknown user | Update a missing user | 404. | API | [L324](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L324) |
| 514 | UpdatePracticeUserRoles_UserExists_UpdatesRoles | Role update | Update an existing user | Roles applied. | API | [L335](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/UserApiTests.cs#L335) |

---

## `tests/UnitTests/Phone/PhoneRepositoryTests.cs`

The authorization layer over phone reads. Note rows 519–521: a patient may read only their own, a practice may read only patients it has a relationship with, and a mixed batch is filtered per item rather than refused outright.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 515 | GetPatientPhones_Works | Read | Read phones | Returned. | Unit | [L27](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L27) |
| 516 | GetPatientPhones_ReturnsNullPhoneWhenUserExistsWithoutPhoneRecord | No phone record | The user exists with no phone | A null phone, not an omission. | Unit | [L69](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L69) |
| 517 | GetPatientPhones_WhenPhoneAndUserMappingRecordDoNotExist_ReturnsPatientNotFound | Missing patient | Neither record exists | `PatientNotFound`. | Unit | [L95](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L95) |
| 518 | GetPatientPhones_Unauthorized | Auth gate | Unauthenticated | Rejected. | Unit | [L115](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L115) |
| 519 | GetPatientPhones_LoggedInAsPatient | Patient scope (2 cases) | Own and another patient | Own allowed, other denied. | Unit | [L137](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L137) |
| 520 | GetPatientPhones_LoggedInAsPractice | Practice scope (3 cases) | Three practice/patient combinations | Only related patients are readable. | Unit | [L182](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L182) |
| 521 | GetPatientPhones_LoggedInAsPractice_CanAccessSome | Partial batch | A mixed batch as a practice | Filtered per item. | Unit | [L229](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L229) |
| 522 | Reconcile_Unauthorized | Auth gate | Reconcile unauthenticated | Rejected. | Unit | [L267](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L267) |
| 523 | Reconcile_Success | Reconcile | Authorized reconcile | Succeeds. | Unit | [L284](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L284) |
| 524 | DeletePatientPhone_UnauthorizedRole | Role gate | Wrong role | Rejected. | Unit | [L323](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L323) |
| 525 | DeletePatientPhone_AuthorizedRole | Delete | Correct role | Succeeds. | Unit | [L335](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L335) |
| 526 | UpdateMfaStatusAsync_UnauthorizedRole | Role gate | Wrong role | Rejected. | Unit | [L345](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L345) |
| 527 | UpdateMfaStatusAsync_AuthorizedRole | MFA update | Correct role | Succeeds. | Unit | [L357](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L357) |
| 528 | IsPhoneNumberTransferable_NonDeletedPhone_ReturnsTransferableStatus | Transferability | A live phone | The stored status is returned. | Unit | [L367](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L367) |
| 529 | IsPhoneNumberTransferable_DeletedPhone_ReturnsTrue | Deleted phone | A deleted phone | Always transferable — deletion releases the number. | Unit | [L389](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L389) |
| 530 | GetPatientIdByPhone_WhenPhoneExists_ReturnsPatientId | Reverse lookup | Known phone | The patient id. | Unit | [L411](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L411) |
| 531 | GetPatientIdByPhone_WhenPhoneDoesNotExist_ReturnsNullPatientId | Unknown phone | Unknown number | Null. | Unit | [L449](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L449) |
| 532 | GetPatientIdByPhone_WhenPhoneRecordHasNoPatientId_ReturnsNullPatientId | Orphan record | A phone record with no patient id | Null. | Unit | [L467](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L467) |
| 533 | GetPatientIdByPhone_Unauthorized | Auth gate | Unauthenticated | Rejected. | Unit | [L500](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneRepositoryTests.cs#L500) |

---

## `tests/UnitTests/InternalUserLoginServiceTests.cs`

Staff login through the internal-services Auth0 tenant (workforce connection). The distinguishing behaviour is how `returnTo` failures are handled: unlike the patient and practice flows, an invalid `returnTo` here falls back to a default rather than failing the login (rows 537, 551).

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 534 | InitiateOAuthFlow_StoresStateInDynamoUnderTheInternalServicesTenant | Tenant tagging | Start the flow | The state is stored under the internal-services tenant. | Unit | [L67](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L67) |
| 535 | InitiateOAuthFlow_ValidReturnTo_StoresTheValidatedFormOfIt | Normalisation | Valid `returnTo` | The validated form is stored, not the raw input. | Unit | [L85](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L85) |
| 536 | InitiateOAuthFlow_ReturnToIsAbsent_StoresTheDefaultAndTagsItAbsent | Absent `returnTo` | No `returnTo` | The default is stored and tagged absent. | Unit | [L100](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L100) |
| 537 | InitiateOAuthFlow_ReturnToFailsValidation_StoresTheDefaultRatherThanFailingTheLogin | Soft failure | Invalid `returnTo` | Falls back to the default — staff are not locked out by a bad deep link. | Unit | [L112](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L112) |
| 538 | InitiateOAuthFlow_ReturnsTheTransactionIdItStored | Transaction id | Start the flow | The returned id matches the stored one. | Unit | [L125](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L125) |
| 539 | InitiateOAuthFlow_BuildsAnAuthorizeUrlCarryingTheAudienceAndWorkforceConnection | Authorize URL | Start the flow | Audience and workforce connection are carried. | Unit | [L156](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L156) |
| 540 | InitiateOAuthFlow_NoScopeRequested_OmitsScopeFromTheAuthorizeUrlEntirely | Scope omission | No scope requested | `scope` is absent rather than empty. | Unit | [L201](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L201) |
| 541 | InitiateOAuthFlow_ScopeRequested_PassesItThroughToTheAuthorizeUrl | Scope pass-through | A scope requested | Passed through. | Unit | [L215](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L215) |
| 542 | CompleteOAuthFlow_NoState_ReturnsStateNotFound | Missing state | No state | `StateNotFound`. | Unit | [L233](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L233) |
| 543 | CompleteOAuthFlow_NoStoredFlowState_ReturnsStateNotFound | Unknown state | Nothing stored | `StateNotFound`. | Unit | [L249](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L249) |
| 544 | CompleteOAuthFlow_PreauthCookieDoesNotMatchStoredState_ReturnsTransactionIdMismatch | Cookie binding | The pre-auth cookie does not match | `TransactionIdMismatch`. | Unit | [L265](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L265) |
| 545 | CompleteOAuthFlow_StoredStateBelongsToAnotherTenant_ReturnsTenantMismatch | Tenant binding | A state from another tenant | `TenantMismatch`. | Unit | [L283](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L283) |
| 546 | CompleteOAuthFlow_Auth0ReturnedAnErrorInsteadOfACode_ReturnsTokenExchangeFailed | Auth0 error | An error in place of a code | `TokenExchangeFailed`. | Unit | [L304](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L304) |
| 547 | CompleteOAuthFlow_ExchangesAgainstTheInternalServicesTenantCallbackUrl | Callback URL | Complete the flow | The internal-services callback URL is used. | Unit | [L333](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L333) |
| 548 | CompleteOAuthFlow_Auth0RejectsTheCode_ReturnsTokenExchangeFailed | Rejected code | Auth0 rejects the code | `TokenExchangeFailed`. | Unit | [L361](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L361) |
| 549 | CompleteOAuthFlow_Auth0ReturnsNoToken_ReturnsTokenExchangeFailed | No token | Auth0 returns nothing | `TokenExchangeFailed`. | Unit | [L390](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L390) |
| 550 | CompleteOAuthFlow_StoredReturnToStillValidates_ReturnsIt | Re-validation | The stored `returnTo` still validates | Returned. | Unit | [L417](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L417) |
| 551 | CompleteOAuthFlow_StoredReturnToNoLongerValidates_FallsBackToTheDefault | Re-validation failure | The allowlist changed between start and callback | Falls back to the default — the value is re-checked on the way out. | Unit | [L437](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginServiceTests.cs#L437) |

---

## `tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs`

The provider browser login end to end: redirect, pre-auth cookie, callback, role assignment. Rows 564–566 and 568 pin the role side-effect per user kind — a Zo SSO user and a database user get no roles set, while a practice SSO user is granted full admin on every practice they map to.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 552 | PracticeLoginStart_InvalidReturnTo_Returns400 | Open-redirect guard | Off-site `returnTo` | 400. | API | [L29](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L29) |
| 553 | PracticeLoginStart_MissingReturnTo_Returns400 | Required parameter | No `returnTo` | 400 — unlike the internal flow (row 536), the provider flow requires it. | API | [L40](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L40) |
| 554 | PracticeLoginStart_ValidReturnTo_Returns302AndSetsCookie | Redirect and cookie | Valid `returnTo` | 302 with the pre-auth cookie set. | API | [L55](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L55) |
| 555 | PracticeLoginStart_ValidReturnTo_StoresStateInDynamo | State persistence (`RealOnly`) | Start the flow | The state lands in Dynamo. | API | [L97](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L97) |
| 556 | PracticeLoginCallback_NoPreauthCookie_RedirectsToError | Missing cookie | Callback with no pre-auth cookie | Redirected to the error page. | API | [L139](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L139) |
| 557 | PracticeLoginCallback_StateMismatch_RedirectsToError | State binding (3 cases) | Three mismatch shapes | Error redirect. | API | [L163](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L163) |
| 558 | PracticeLoginCallback_InvalidCode_RedirectsToError | Invalid code (3 cases) | Three bad codes | Error redirect. | API | [L213](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L213) |
| 559 | PracticeLoginCallback_Success_SetsCookiesAndRedirects | Happy path | Valid callback | Cookies set, redirected. | API | [L261](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L261) |
| 560 | PracticeLoginCallback_ZoSsoUser_Success_SetsCookiesAndRedirects | Zo SSO user | Callback as a Zo SSO user | Cookies set, redirected. | API | [L356](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L356) |
| 561 | PracticeLoginStart_ExistingCookie_ReusesPreauthTokenWithFreshState | Transaction continuity | Start with an existing cookie | The pre-auth token is reused with a fresh state. | API | [L425](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L425) |
| 562 | PracticeLoginCallback_Success_PreservesPreauthCookie | Cookie survival | Complete the flow | The pre-auth cookie is preserved — this is what makes row 563 work. | API | [L456](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L456) |
| 563 | PracticeLogin_MultiTab_BothTabsComplete | Multi-tab login | Start in two tabs, complete both | Both succeed — a second tab does not invalidate the first. | API | [L507](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L507) |
| 564 | PracticeLoginCallback_ZoSsoUser_DoesNotSetRoles | Role side-effect (`RealOnly`) | Zo SSO callback | No roles are set. | API | [L570](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L570) |
| 565 | PracticeLoginCallback_SsoSinglePractice_SetsFullAdminRole | Role grant (`RealOnly`) | SSO user mapping to one practice | Full admin on that practice. | API | [L610](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L610) |
| 566 | PracticeLoginCallback_SsoMultiplePractices_SetsFullAdminRoleForAll | Role grant, multi (`RealOnly`) | SSO user mapping to several practices | Full admin on all of them — the blast radius of a practice-SSO login. | API | [L675](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L675) |
| 567 | PracticeLoginCallback_DBUser_Success_SetsCookiesAndRedirects | Database user | Callback as a database-connection user | Cookies set, redirected. | API | [L739](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L739) |
| 568 | PracticeLoginCallback_DBUser_Success_DoesNotSetUserRoles | Role side-effect (`RealOnly`) | Database-user callback | No roles set — only SSO logins grant roles. | API | [L811](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeOAuthLoginApiTests.cs#L811) |

---

## `tests/UnitTests/Auth0WebhookControllerTests.cs`

The webhook Auth0 calls after a login. Authentication is a shared secret, and there is one secret per tenant — row 581 pins that an unconfigured provider secret rejects provider calls while row 580 pins that it does not break patient calls.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 569 | MissingSecret_ReturnsUnauthorized | Auth gate | No secret | 401. | Unit | [L82](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L82) |
| 570 | InvalidSecret_ReturnsUnauthorized | Wrong secret | An invalid secret | 401. | Unit | [L89](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L89) |
| 571 | PatientSecret_ReturnsNoContent | Patient secret | The patient secret | 204. | Unit | [L96](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L96) |
| 572 | ProviderSecret_ReturnsNoContent | Provider secret | The provider secret | 204. | Unit | [L103](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L103) |
| 573 | PatientSecret_LogsUserActivity | Activity logging | Patient call | Activity is logged. | Unit | [L114](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L114) |
| 574 | ProviderSecret_LogsUserActivity | Activity logging | Provider call | Activity is logged. | Unit | [L121](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L121) |
| 575 | PatientSecret_PassesPatientTenantToFactory | Tenant routing | Patient call | The patient tenant reaches the factory. | Unit | [L132](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L132) |
| 576 | ProviderSecret_PassesProviderTenantToFactory | Tenant routing | Provider call | The provider tenant reaches the factory. | Unit | [L148](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L148) |
| 577 | PatientSecret_RecordsMetricsWithPatientTenantType | Metrics | Patient call | Tagged with the patient tenant. | Unit | [L168](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L168) |
| 578 | ProviderSecret_RecordsMetricsWithProviderTenantType | Metrics | Provider call | Tagged with the provider tenant. | Unit | [L175](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L175) |
| 579 | CorrelationId_PassesTransactionCorrelationIdToFactory | Correlation | A call carrying a correlation id | Passed through — links the webhook to the login that triggered it. | Unit | [L186](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L186) |
| 580 | UnconfiguredProviderSecret_PatientStillWorks | Partial config | No provider secret configured | Patient calls still work. | Unit | [L210](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L210) |
| 581 | UnconfiguredProviderSecret_ProviderSecretReturnsUnauthorized | Fail closed | No provider secret configured | Provider calls are rejected, not accepted by default. | Unit | [L221](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L221) |
| 582 | RefreshProtocol_LogsRefreshIntent | Intent mapping | A refresh protocol | Logged as a refresh. | Unit | [L236](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L236) |
| 583 | KnownLoginProtocol_LogsLoginIntent | Intent mapping | A known login protocol | Logged as a login. | Unit | [L246](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L246) |
| 584 | NullTransaction_LogsLoginIntent | Missing transaction | No transaction | Defaults to login intent. | Unit | [L256](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L256) |
| 585 | UnknownProtocol_LogsLoginIntent_AndStillLogsActivity | Unknown protocol | An unrecognised protocol | Login intent, and the activity is still logged — a new Auth0 protocol does not silently drop the record. | Unit | [L266](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0WebhookControllerTests.cs#L266) |

---

## `tests/UnitTests/PatientAccountServiceTests.cs`

Account deletion, MFA status, and the user-account-id lifecycle behind the API tests in rows 53–65.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 586 | DeletePatientAccount_UserExists | Deletion | Delete an existing account | Deleted. | Unit | [L28](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L28) |
| 587 | DeletePatientAccount_UserHasAnonTokenData_ThrowsException | Anonymous-token guard | The user carries anon token data | Throws rather than deleting — a guard against destroying a partially-migrated record. | Unit | [L39](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L39) |
| 588 | DeletePatientAccount_NoUser_DoesNothing | Idempotent delete | No such user | No-op. | Unit | [L52](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L52) |
| 589 | UpdateMfaStatus_WorksWhenUserExists | MFA update | Existing user | Updated. | Unit | [L60](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L60) |
| 590 | UpdateMfaStatus_Works_WhenOriginalMfaStatusIsNull | Null prior state | The prior status is null | Updated. | Unit | [L71](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L71) |
| 591 | UpdateMfaStatus_NoMatchingUserInAuth0_ThrowsException | Missing Auth0 user | No Auth0 user | Throws. | Unit | [L82](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L82) |
| 592 | UpdateMfaStatus_WhenMfaStatusIsAlreadySet_StillMakesCall | No short-circuit | The status already matches | The Auth0 call is still made — auth-service does not trust its local copy as authoritative. | Unit | [L97](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L97) |
| 593 | UpdateMfaStatus_WhenUserIdentityIsMissingAPhone_ThrowsException | Missing phone | The identity has no phone | Throws — MFA without a phone is not a valid state. | Unit | [L108](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L108) |
| 594 | GetUserAccountIdByPatientId_ReturnsUserAccountId_WhenPatientExistsAndHasUserAccountId | Read | Assigned id | Returned. | Unit | [L129](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L129) |
| 595 | GetUserAccountIdByPatientId_ReturnsPatientNotFound_WhenNoUserMappingExists | Missing mapping | No user mapping | `PatientNotFound`. | Unit | [L146](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L146) |
| 596 | GetUserAccountIdByPatientId_ReturnsUserAccountIdNotSet_WhenPatientExistsButNoUserAccountId | Unassigned | No id set | `UserAccountIdNotSet` — distinct from patient-not-found. | Unit | [L158](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L158) |
| 597 | GetUserAccountIdByPatientId_ReturnsUserAccountIdNotSet_WhenAuth0UserNotFound | Missing Auth0 user | No Auth0 user | `UserAccountIdNotSet`. | Unit | [L174](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L174) |
| 598 | SetUserAccountId_Success_GeneratesAndSetsUserAccountId | Assignment | Assign an id | Generated and set. | Unit | [L188](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L188) |
| 599 | SetUserAccountId_ReturnsPatientNotFound_WhenNoUserMappingExists | Missing mapping | No mapping | `PatientNotFound`. | Unit | [L205](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L205) |
| 600 | SetUserAccountId_ReturnsAuth0UserNotFound_WhenAuth0UserDoesNotExist | Missing Auth0 user | No Auth0 user | `Auth0UserNotFound`. | Unit | [L218](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L218) |
| 601 | SetUserAccountId_ReturnsExistingUserAccountId_WhenUserAccountIdAlreadyExists | Idempotency | Already assigned | The existing id is returned. | Unit | [L233](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L233) |
| 602 | SetUserAccountId_GeneratesIdWithCorrectPrefix | Id format | Generate an id | The prefix is correct — the shape other services parse. | Unit | [L251](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientAccountServiceTests.cs#L251) |

---

## `tests/UnitTests/RequestContext/RequestContextServiceTests.cs`

Assembles the per-request context that every event and metric is tagged with. Each field is read from a header first and a cookie second, and every one has an explicit "absent" case — a missing header must produce null, not an empty string that pollutes analytics.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 603 | Context_GivenNoTrackingHeadersOrCookies_ReturnsNullValue | Tracking absent | Neither header nor cookie | Null. | Unit | [L42](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L42) |
| 604 | Context_GivenTrackingIdInHeader_SetsIt | Tracking from header (2 cases) | Two header forms | Set. | Unit | [L51](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L51) |
| 605 | Context_GivenTrackingIdInCookie_SetsIt | Tracking from cookie | Cookie only | Set. | Unit | [L61](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L61) |
| 606 | Context_GivenNoSessionHeadersOrCookies_ReturnsNullValue | Session absent | Neither | Null. | Unit | [L72](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L72) |
| 607 | Context_GivenSessionId_SetsIt | Session from header (2 cases) | Two header forms | Set. | Unit | [L81](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L81) |
| 608 | Context_GivenSessionIdInCookie_SetsIt | Session from cookie | Cookie only | Set. | Unit | [L91](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L91) |
| 609 | Context_GivenBsidCookie_StripsTimestampSuffixViaCorrelationIdFactory | Cookie normalisation | A `bsid` cookie | The timestamp suffix is stripped — otherwise every request looks like a new session. | Unit | [L102](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L102) |
| 610 | Context_GivenZdSessionIdHeader_DoesNotInvokeStripHelper | Header pass-through | The `ZD-Session-Id` header | Used as-is; the strip helper is cookie-only. | Unit | [L116](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L116) |
| 611 | Context_GivenNoUserAgent_ReturnsNullValue | UA absent | No user agent | Null. | Unit | [L131](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L131) |
| 612 | Context_GivenUserAgent_SetsIt | UA present (4 cases) | Four user agents | Set. | Unit | [L142](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L142) |
| 613 | Context_GivenNoReferer_ReturnsNullValue | Referer absent | No referer | Null. | Unit | [L152](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L152) |
| 614 | Context_GivenReferer_SetsIt | Referer present (2 cases) | Two referers | Set. | Unit | [L161](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L161) |
| 615 | Context_GivenNoApplicationName_ReturnsNullValue | App name absent | None supplied | Null. | Unit | [L171](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L171) |
| 616 | Context_GivenApplicationName_SetsIt | App name present (2 cases) | Two names | Set. | Unit | [L180](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L180) |
| 617 | Context_Url_SetsThePath | URL path (2 cases) | Two request paths | The path is captured. | Unit | [L191](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L191) |
| 618 | Context_GivenNoIp_ReturnsNullValue | IP absent | No IP | Null. | Unit | [L201](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L201) |
| 619 | Context_GivenIp_ReturnsNullValue | IP handling | An IP is present | Still null — the IP is deliberately not carried into the context. | Unit | [L211](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/RequestContext/RequestContextServiceTests.cs#L211) |

---

## `tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs`

The provider-tenant Auth0 client. Rows 625–629 are the practice-staff-id write rules: setting it when absent or null is fine, setting it to the same value is a no-op, and overwriting a different value throws.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 620 | GetUserByAuth0UserId_Success | User read | Read by Auth0 id | Returned. | Unit | [L38](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L38) |
| 621 | GetUserByAuth0UserId_UserNotFoundDoesNotLog | Expected miss | User not found | No exception logged — a miss is normal, not an incident. | Unit | [L50](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L50) |
| 622 | GetUserByAuth0UserId_UserNotFoundLogsException | Unexpected miss | A not-found that is an error | Logged. | Unit | [L64](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L64) |
| 623 | VerifyAuthorizationCodeLogin_Success | Code verification | Verify a valid code | Succeeds. | Unit | [L78](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L78) |
| 624 | VerifyAuthorizationCodeLogin_Error | Code verification errors (2 cases) | Two error conditions | Surfaced. | Unit | [L99](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L99) |
| 625 | UpdatePracticeStaffId_NoAppMetadata_UpdatesPracticeStaffId | First write | No app metadata yet | Set. | Unit | [L114](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L114) |
| 626 | UpdatePracticeStaffId_NullPracticeStaffId_UpdatesPracticeStaffId | Null prior value | The field is null | Set. | Unit | [L127](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L127) |
| 627 | UpdatePracticeStaffId_UpdateSameStaffId_Noop | Same value | Write the value it already has | No-op. | Unit | [L144](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L144) |
| 628 | UpdatePracticeStaffId_OverwriteStaffId_ThrowsException | Overwrite guard | Write a different value | Throws — a staff id is write-once, so one Auth0 user cannot be re-pointed at another practice staff record. | Unit | [L159](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L159) |
| 629 | UpdatePracticeStaffId_UpdatesPracticeStaffId | Write | A valid write | Applied. | Unit | [L174](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L174) |
| 630 | DeletePracticeUserByAuth0UserId_Success | Deletion | Delete a practice user | Succeeds. | Unit | [L187](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L187) |
| 631 | UpdatePracticeUserRoles_Success | Role update | Update roles | Succeeds. | Unit | [L196](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L196) |
| 632 | RefreshAccessToken_FlagOn_UsesZipCredentials | Credential switch | Refresh with the flag on | The ZIP credentials are used. | Unit | [L206](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L206) |
| 633 | RefreshAccessToken_FlagOff_UsesDefaultCredentials | Credential switch | Flag off | The default credentials are used — both sides of the migration flag are pinned. | Unit | [L235](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L235) |
| 634 | RefreshAccessToken_FlagOn_NullToken_ReturnsNullRefreshTokenError | Null token | No refresh token | `NullRefreshToken`. | Unit | [L264](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L264) |
| 635 | RefreshAccessToken_FlagOn_InvalidToken_ReturnsInvalidRefreshTokenError | Invalid token | A bad refresh token | `InvalidRefreshToken`. | Unit | [L277](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ServiceTests.cs#L277) |

---

## `tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs`

The staff login flow over HTTP. Note rows 646–647: an allowlisted `returnTo` deep-links, an off-allowlist one silently lands on the default page rather than erroring.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 636 | InternalUserLoginStart_Returns302ToTheInternalServicesTenantAuthorizeUrl | Redirect | Start the flow | 302 to the internal-services authorize URL. | API | [L28](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L28) |
| 637 | InternalUserLoginStart_ScopeSupplied_ForwardsItToTheAuthorizeUrl | Scope | Supply a scope | Forwarded. | API | [L65](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L65) |
| 638 | InternalUserLoginStart_SetsThePreauthCookie | Pre-auth cookie | Start the flow | The cookie is set. | API | [L84](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L84) |
| 639 | InternalUserLoginStart_StoresStateInDynamoUnderTheInternalServicesTenant | State persistence (`RealOnly`) | Start the flow | Stored under the right tenant. | API | [L106](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L106) |
| 640 | InternalUserLoginCallback_NoPreauthCookie_RedirectsToError | Missing cookie | No pre-auth cookie | Error redirect. | API | [L138](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L138) |
| 641 | InternalUserLoginCallback_UnknownState_RedirectsToError | Unknown state | A state that was never stored | Error redirect. | API | [L154](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L154) |
| 642 | InternalUserLoginCallback_PreauthCookieFromADifferentFlow_RedirectsToError | Cross-flow cookie | A cookie from another flow | Error redirect — the cookie is bound to its own transaction. | API | [L172](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L172) |
| 643 | InternalUserLoginCallback_Auth0RejectsTheCode_RedirectsToError | Rejected code | Auth0 rejects the code | Error redirect. | API | [L191](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L191) |
| 644 | InternalUserLoginCallback_Auth0ReturnedAnErrorInsteadOfACode_RedirectsToError | Auth0 error | An error in place of a code | Error redirect. | API | [L208](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L208) |
| 645 | InternalUserLoginCallback_NoReturnTo_RedirectsToTheDefaultLandingPage | No deep link | No `returnTo` | The default landing page. | API | [L225](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L225) |
| 646 | InternalUserLoginCallback_AllowlistedReturnTo_RedirectsToTheDeepLink | Allowlisted deep link | An allowlisted `returnTo` | Redirected there. | API | [L243](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L243) |
| 647 | InternalUserLoginCallback_OffAllowlistReturnTo_RedirectsToTheDefaultLandingPage | Off-allowlist | A non-allowlisted `returnTo` | Falls back to the default rather than erroring — no open redirect, no lockout. | API | [L262](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L262) |
| 648 | InternalUserLoginCallback_ValidCode_SetsTheAuthCookies | Cookie issuance | A valid code | Auth cookies set. | API | [L284](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L284) |
| 649 | InternalUserLoginCallback_ValidCode_SetsAPlaceholderXsrfCookie | XSRF cookie | A valid code | A placeholder XSRF cookie is set — the internal flow does not parse a real one out of the token. | API | [L318](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L318) |
| 650 | InternalUserLoginCallback_ValidCode_ClearsThePreauthCookie | Cookie cleanup | A valid code | The pre-auth cookie is cleared, so it cannot be replayed. | API | [L341](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalUserOauthLoginApiTests.cs#L341) |

---

## `tests/UnitTests/InternalUserLoginControllerTests.cs`

The controller half of the staff flow — cookie planting, metric recording, and the division of labour with the service. Row 652 is the notable one: the controller deliberately does not validate `returnTo`, leaving that entirely to the service.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 651 | InternalUserLoginStart_RedirectsToTheAuthorizeUrlTheServiceBuilt | Redirect | Start | The service's URL is used verbatim. | Unit | [L44](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L44) |
| 652 | InternalUserLoginStart_PassesTheCallerSuppliedReturnToThroughUnvalidated | Layer boundary | Start with any `returnTo` | Passed through unvalidated — validation lives in one place, the service. | Unit | [L55](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L55) |
| 653 | InternalUserLoginStart_PassesTheCallerSuppliedScopeThroughToTheFlow | Scope | Start with a scope | Passed through. | Unit | [L69](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L69) |
| 654 | InternalUserLoginStart_PlantsThePreauthCookieWithTheTransactionIdFromTheFlow | Cookie | Start | The cookie carries the flow's transaction id. | Unit | [L86](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L86) |
| 655 | InternalUserLoginStart_RecordsAStartMetricForTheInternalServicesTenant | Metrics | Start | A start metric tagged with the tenant. | Unit | [L97](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L97) |
| 656 | InternalUserLoginCallback_NoPreauthCookie_RedirectsToErrorWithoutRedeemingTheCode | Early exit | Callback with no cookie | Error redirect and the code is never redeemed — the code stays unspent. | Unit | [L115](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L115) |
| 657 | InternalUserLoginCallback_NoPreauthCookie_RecordsTheMissingPreauthCookieMetric | Metrics | Same | A specific missing-cookie metric. | Unit | [L145](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L145) |
| 658 | InternalUserLoginCallback_PassesTheCookieTransactionIdAndEveryQueryParameterToTheService | Parameter forwarding | Callback | Everything reaches the service. | Unit | [L168](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L168) |
| 659 | InternalUserLoginCallback_ServiceReturnsAnError_RedirectsToErrorAndSetsNoAuthCookies | Error path | The service errors | Error redirect and no auth cookies — a failed login never leaves a partial session. | Unit | [L194](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L194) |
| 660 | InternalUserLoginCallback_ServiceReturnsAnError_RecordsThatErrorOnTheCallbackMetric | Metrics | The service errors | The error is tagged on the callback metric. | Unit | [L215](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L215) |
| 661 | InternalUserLoginCallback_Success_RedirectsToTheReturnToTheFlowResolved | Redirect | Success | Redirected to the resolved `returnTo`. | Unit | [L237](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L237) |
| 662 | InternalUserLoginCallback_Success_SetsTheAuth0TokenCookiesWithoutParsingXsrf | Cookie issuance | Success | Token cookies set without XSRF parsing. | Unit | [L254](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L254) |
| 663 | InternalUserLoginCallback_Success_ClearsThePreauthAndStaleAuthCookiesBeforeSettingNewOnes | Cookie hygiene | Success | Stale cookies are cleared first — prevents a stale token surviving a fresh login. | Unit | [L274](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L274) |
| 664 | InternalUserLoginCallback_Success_RecordsAnErrorlessCallbackMetric | Metrics | Success | An error-free callback metric. | Unit | [L305](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/InternalUserLoginControllerTests.cs#L305) |

---

## `tests/UnitTests/User/UserRepositoryTests.cs`

The user-mapping repository and its authorization checks. Rows 668 and 670 pin that an unauthorized batch read returns the ids as *forbidden* entries rather than failing the whole call.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 665 | ReconcilePatientUserMappings_Success | Reconciliation | Reconcile mappings | Succeeds. | Unit | [L26](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L26) |
| 666 | ReconcilePatientUserMappings_Unauthorized | Auth gate | Unauthorized reconcile | Rejected. | Unit | [L71](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L71) |
| 667 | GetUsers_WithRightRole_Success | Batch read | Correct role | Succeeds. | Unit | [L99](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L99) |
| 668 | GetUsers_Unauthorized_ReturnsForbiddenUsers | Partial authorization | Wrong role | The users come back marked forbidden rather than the call failing. | Unit | [L173](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L173) |
| 669 | GetUsersByPatientIds_WithRightRole_Success | Batch read by patient | Correct role | Succeeds. | Unit | [L222](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L222) |
| 670 | GetUsersByPatientIds_Unauthorized_ReturnsForbiddenUsers | Partial authorization | Wrong role | Marked forbidden. | Unit | [L296](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L296) |
| 671 | DeletePatientUserMapping | Mapping deletion | Delete a mapping | Deleted. | Unit | [L345](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L345) |
| 672 | GetUserByAuth0UserId_ReturnsObject | Read | Read by Auth0 id | Returned. | Unit | [L371](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L371) |
| 673 | GetUserByAuth0UserId_WhenDeleted_ReturnsNull | Soft delete | The record is deleted | Null — deleted rows are not resurrected by a read. | Unit | [L384](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L384) |
| 674 | GetUserByAuth0UserId_WhenNull_ReturnsNull | Missing | No record | Null. | Unit | [L397](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L397) |
| 675 | CreateUserMapping_CreatesMapping | Creation | Create a mapping | Created. | Unit | [L409](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L409) |
| 676 | GetCurrentUser_ReturnsNull_WhenNotLoggedIn | No session | Not logged in | Null. | Unit | [L421](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L421) |
| 677 | GetCurrentUser_ReturnsNull_WhenNotLoggedInAsPatient | Wrong identity type | Logged in as something else | Null. | Unit | [L430](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L430) |
| 678 | GetCurrentUser_ReturnsCurrentUser | Self read | Logged in as a patient | The current user. | Unit | [L441](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserRepositoryTests.cs#L441) |

---

## `tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs`

CRUD on a practice's identity provider — the record that decides whether that practice's users log in with a password or through SSO. Row 689's 11-case table is the domain restriction list: an IdP claiming a public mail domain would let anyone with such an address into the practice.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 679 | GetIdentityProviderByPracticeId_NoJwt_Unauthorized | Auth gate | No token | 401. | API | [L26](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L26) |
| 680 | GetIdentityProviderByPracticeId_WrongRole_Forbidden | Role gate | Wrong role | 403. | API | [L35](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L35) |
| 681 | GetIdentityProviderByPracticeId_PatientJwt_Forbidden | Cross-audience | A patient token | 403. | API | [L47](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L47) |
| 682 | GetIdentityProviderByPracticeId_CsrUser_Success | CSR access | A CSR token | Allowed. | API | [L59](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L59) |
| 683 | GetIdentityProviderByPracticeId_ServiceUser_Success | Service access | A service token | Allowed. | API | [L69](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L69) |
| 684 | GetIdentityProviderByPracticeId_PracticeUserWithFgaPermission_Success | FGA grant | A practice user with the FGA permission | Allowed. | API | [L79](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L79) |
| 685 | GetIdentityProviderByPracticeId_RbacPracticeIdOnlyMatch_Success | RBAC fallback | A user matching only on practice id | Allowed — the legacy path still grants alongside FGA. | API | [L101](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L101) |
| 686 | GetIdentityProviderByPracticeId_PracticeUserWithoutFgaPermission_Forbidden | FGA deny | A practice user without the permission | 403. | API | [L125](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L125) |
| 687 | AddIdentityProvider_RequiresIdpWriteRole | Write gate | Add without the write role | Rejected. | API | [L147](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L147) |
| 688 | AddIdentityProvider_Success | Create | Add with the role | Created. | API | [L166](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L166) |
| 689 | AddIdentityProvider_RestrictedDomain | Domain restrictions (11 cases) | Eleven domains | The restricted ones are refused — a practice cannot claim `gmail.com` and inherit every Gmail user. | API | [L231](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L231) |
| 690 | DeleteIdentityProvider_RequiresIdpWriteRole | Delete gate | Delete without the role | Rejected. | API | [L260](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L260) |
| 691 | DeleteIdentityProvider_Success | Delete | Delete with the role | Deleted. | API | [L271](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeIdentityProviderApiTests.cs#L271) |

---

## `tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs`

Provider login over HTTP: the password-vs-SSO fork, the IdP callback, and refresh. Row 696 verifies the full-admin role is granted only on the SSO path — its comment notes the assertion runs through the user-permissions fake, which is why it is `RealOnly`.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 692 | PracticeLoginStart_BadEmail_ReturnsBadRequest | Email validation | Malformed email | 400. | API | [L35](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L35) |
| 693 | PracticeLoginStart_NoIdPForDomain_ReturnsPasswordLogin | Password fork (3 cases) | Three domains with no IdP | Password login. | API | [L59](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L59) |
| 694 | PracticeLoginStart_IdPForDomain_ReturnsSsoLogin | SSO fork (3 cases) | Three domains with an IdP | SSO login. | API | [L76](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L76) |
| 695 | PracticeIdentityProviderLogin_Success | IdP callback (4 cases) | Four successful callbacks | Each succeeds. | API | [L146](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L146) |
| 696 | PracticeIdentityProviderLogin_SetsFullAdminRoleInUserPermission_OnlyWhenSso | Role grant (3 cases, `RealOnly`) | Three login kinds | Full admin is set only for SSO. | API | [L201](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L201) |
| 697 | PracticeIdentityProviderLogin_ExistingStaffId_Success | Existing staff link | The user already has a staff id | Succeeds. | API | [L278](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L278) |
| 698 | PracticeIdentityProviderLogin_InvalidCode | Invalid code (2 cases) | Two bad codes | Rejected. | API | [L312](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L312) |
| 699 | PracticeIdentityProviderLogin_NoPracticeId | Missing practice | No practice id | Rejected. | API | [L325](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L325) |
| 700 | PracticeIdentityProviderLogin_ChurnedPractice | Churned practice | The practice has churned | Rejected — an ex-customer's IdP does not keep working. | API | [L338](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L338) |
| 701 | PracticeUserRefreshToken_ReturnsNewAccessTokenForValidRefreshToken | Refresh (`RealOnly`) | Refresh with a valid token | A new access token. | API | [L366](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L366) |
| 702 | PracticeUserRefreshToken_BsidCookieWithTimestampSuffix_StripsSuffixInLoggedSessionId | Session id hygiene (`RealOnly`) | Refresh with a suffixed `bsid` cookie | The suffix is stripped in the logged session id — the end-to-end version of row 609. | API | [L421](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L421) |
| 703 | PracticeUserRefreshToken_LogsEventOnFailure | Failure event (`RealOnly`) | Fail a refresh | An event lands. | API | [L456](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L456) |
| 704 | PracticeUserRefreshToken_InvalidRefreshToken_ReturnsForbidden | Invalid token | A bad refresh token | 403. | API | [L487](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLoginApiTests.cs#L487) |

---

## `tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs`

Service-auth client registration. Most of the file is the key-ARN credential rules — how many credentials a client ends up with after repeated create/update calls, and when an ambiguous ARN must throw rather than guess which credential to rotate.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 705 | CreateUpdateClient_LegacyWithoutKeyArn_Success | Legacy client | Create/update without a key ARN | Succeeds. | API | [L28](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L28) |
| 706 | CreateClient_ThrowsException | Failure path | A failing create | Throws. | API | [L68](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L68) |
| 707 | CreateUpdateClient_Unauthorized | Auth gate | No authorization | Rejected. | API | [L85](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L85) |
| 708 | GetServiceAuthClient_Success | Read | Read a client | Returned. | API | [L114](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L114) |
| 709 | GetServiceAuthClient_NoClient | Missing client | Read a nonexistent client | Handled. | API | [L148](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L148) |
| 710 | GetServiceAuthClient_Unauthorized | Auth gate | No token | 401. | API | [L163](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L163) |
| 711 | GetServiceAuthClient_Forbidden | Role gate | Wrong role | 403. | API | [L177](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L177) |
| 712 | CreateLegacyClient_UpdateWithKeyArn_ShouldResultInOneCredential | Legacy upgrade | Legacy client, then update with an ARN | One credential — the upgrade does not duplicate. | API | [L278](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L278) |
| 713 | CreateClientWithKeyArn_UpdateWithSameKeyArn_ShouldResultInOneCredential | Idempotent update | Same ARN twice | One credential. | API | [L317](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L317) |
| 714 | CreateClientWithKeyArn_UpdateWithNewKeyArn_ShouldResultInTwoCredentials | Key rotation | A new ARN | Two credentials — both live, which is what makes a zero-downtime rotation possible. | API | [L353](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L353) |
| 715 | CreateThreeClientsWithDifferentKeyArn_ShouldThrow | Credential cap | A third distinct ARN | Throws — the rotation window holds at most two. | API | [L386](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L386) |
| 716 | CreateClientWithTwoKeyArn_UpdateWithSameKeyArn_ShouldThrowForAmbiguousKeyArn | Ambiguity | Two credentials, update with a shared ARN | Throws rather than picking one. | API | [L418](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L418) |
| 717 | CreateClientWithTwoKeyArn_UpdateWithSameSecondKeyArn_ShouldUpdateRole | Disambiguated update | Update matching the second ARN | The role updates. | API | [L451](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/InternalServicesApiTests.cs#L451) |

---

## `tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs`

Which practices a provider user may switch between, and the switch itself. The allowed set comes from SAML connection metadata; rows 720–723 pin that every way of not having that metadata yields an empty list, never an unrestricted one.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 718 | GetMultiPracticeAccess_WithSamlConnection_ReturnsPracticeIdsFromMetadata | Allowed set | A SAML connection with practice ids | The ids from the metadata. | API | [L27](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L27) |
| 719 | GetMultiPracticeAccess_WithSamlConnection_SinglePracticeId_ReturnsSinglePracticeId | Single practice | One id in the metadata | One id. | API | [L63](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L63) |
| 720 | GetMultiPracticeAccess_WithSamlConnection_EmptyAllowedPracticeIds_ReturnsEmptyList | Empty allowlist | An empty allowed list | Empty — an empty allowlist denies rather than permitting all. | API | [L99](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L99) |
| 721 | GetMultiPracticeAccess_WithAuth0ConnectionStrategy_ReturnsEmptyList | Non-SAML connection | An Auth0-strategy connection | Empty. | API | [L133](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L133) |
| 722 | GetMultiPracticeAccess_WithSamlConnection_NullMetadata_ReturnsEmptyList | Missing metadata | Null metadata | Empty. | API | [L161](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L161) |
| 723 | GetMultiPracticeAccess_NonPracticeUser_ReturnsEmptyList | Wrong user type | A non-practice user | Empty. | API | [L190](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L190) |
| 724 | GetMultiPracticeAccess_WithoutJwt_ReturnsUnauthorized | Auth gate | No token | 401. | API | [L215](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L215) |
| 725 | SwitchPractice_NoUser_Returns401 | Auth gate | No user | 401. | API | [L228](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L228) |
| 726 | SwitchPractice_NoRefreshToken_Returns400 | Required token | No refresh token | 400 — the switch re-mints a token, so it needs one to start from. | API | [L239](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L239) |
| 727 | SwitchPractice_MonolithPracticeUser_Returns400 | Unsupported user | A monolith practice user | 400. | API | [L288](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L288) |
| 728 | SwitchPractice_Success | Switch | A valid switch | Succeeds. | API | [L309](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L309) |
| 729 | SwitchPractice_InvalidRefreshToken_ReturnsBadRequest | Invalid token | A bad refresh token | 400. | API | [L374](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L374) |
| 730 | SwitchPractice_UnauthorizedPractice_ReturnsForbidden | Allowlist enforcement | Switch to a practice outside the allowed set | 403 — the set from rows 718–723 is enforced, not just reported. | API | [L426](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/MultiPractice/MultiPracticeApiTests.cs#L426) |

---

## `tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs`

The endpoint the Auth0 Universal Login page posts interaction events to. It is called from an unauthenticated login page, so the contract is strict validation plus tenant routing to the right Firehose stream.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 731 | LogPageEvent_WithValidPageView_ReturnsNoContent | Page view | Post a page view | 204. | API | [L21](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L21) |
| 732 | LogPageEvent_WithButtonClick_ReturnsNoContent | Button click | Post a click | 204. | API | [L38](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L38) |
| 733 | LogPageEvent_WithCheckboxChange_ReturnsNoContent | Checkbox change | Post a change | 204. | API | [L56](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L56) |
| 734 | LogPageEvent_WithLinkClick_ReturnsNoContent | Link click | Post a link click | 204. | API | [L75](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L75) |
| 735 | LogPageEvent_WithMissingPageName_ReturnsBadRequest | Required field | No page name | 400. | API | [L93](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L93) |
| 736 | LogPageEvent_WithMissingTargetType_ReturnsBadRequest | Required field | No target type | 400. | API | [L104](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L104) |
| 737 | LogPageEvent_WithMissingTargetTrigger_ReturnsBadRequest | Required field | No target trigger | 400. | API | [L115](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L115) |
| 738 | LogPageEvent_WithEmptyBody_ReturnsBadRequest | Empty body | Post nothing | 400. | API | [L126](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L126) |
| 739 | LogPageEvent_WithPatientTenantType_ReturnsNoContent | Patient tenant | Post with the patient tenant | 204. | API | [L135](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L135) |
| 740 | LogPageEvent_WithProviderTenantType_ReturnsNoContent | Provider tenant | Post with the provider tenant | 204. | API | [L153](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L153) |
| 741 | LogPageEvent_WithNullTenantType_ReturnsNoContent | Missing tenant | No tenant | 204 — the event is not dropped for lack of a tenant. | API | [L171](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L171) |
| 742 | LogPageEvent_WithNullTenantType_LogsPatientEventToFirehose | Default routing (2 cases, `RealOnly`) | Post with no tenant | It lands on the patient stream — patient is the default. | API | [L189](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L189) |
| 743 | LogPageEvent_WithProviderTenantType_LogsProviderEventToFirehose | Provider routing (`RealOnly`) | Post with the provider tenant | It lands on the provider stream. | API | [L232](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UniversalLoginEvent/UniversalLoginEventApiTests.cs#L232) |

---

## `tests/UnitTests/UniversalLoginMetricsServiceTests.cs`

The metric side of the same endpoint. Every event field has an enumerated case table because these become Datadog tag values — an unbounded value here is a cardinality incident.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 744 | Tenant_Patient_EmitsPatient | Tenant tag | Patient tenant | `patient`. | Unit | [L58](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L58) |
| 745 | Tenant_Provider_EmitsProvider | Tenant tag | Provider tenant | `provider`. | Unit | [L65](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L65) |
| 746 | ClientId_EmittedCorrectly | Client id (3 cases) | Three clients | Emitted. | Unit | [L78](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L78) |
| 747 | ClientName_Sanitized | Client name (5 cases) | Five raw names | Sanitised. | Unit | [L93](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L93) |
| 748 | Platform_UsesParserTag | Platform | A parsed platform | The parser's value. | Unit | [L104](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L104) |
| 749 | Platform_NullOrEmpty_ReturnsUnknown | Platform fallback (2 cases) | Null and empty | `unknown`. | Unit | [L116](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L116) |
| 750 | PageName_EmittedCorrectly | Page name (6 cases) | Six pages | Emitted. | Unit | [L132](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L132) |
| 751 | TargetType_EmittedCorrectly | Target type (7 cases) | Seven types | Emitted. | Unit | [L149](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L149) |
| 752 | TargetTrigger_EmittedCorrectly | Target trigger (6 cases) | Six triggers | Emitted. | Unit | [L165](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L165) |
| 753 | TargetName_EmittedCorrectly | Target name (5 cases) | Five names | Emitted. | Unit | [L180](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L180) |
| 754 | NewState_EmittedCorrectly | New state (6 cases) | Six states | Emitted. | Unit | [L196](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L196) |
| 755 | RecordPageEvent_EmitsAllExpectedTags | Full tag set | Record an event | Every expected tag is present. | Unit | [L207](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L207) |
| 756 | MetricName_IsCorrect | Metric name | Record an event | The name is correct — renaming it silently orphans every dashboard. | Unit | [L229](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/UniversalLoginMetricsServiceTests.cs#L229) |

---

## `tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs`

Credential rotation and retrieval for external API clients. Three independent conditions must all hold beyond the role check: the management client id must match, the client must be owned by the external API, and the metadata must exist — any one missing is a 403, not a 404.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 757 | RotateCredential_ReturnsUnauthorized_WithNoToken | Auth gate | No token | 401. | API | [L30](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L30) |
| 758 | RotateCredential_ReturnsForbidden_WithoutCorrectRole | Role gate | Wrong role | 403. | API | [L39](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L39) |
| 759 | RotateCredential_ReturnsOk_WithCorrectRole | Rotation | Correct role | 200. | API | [L49](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L49) |
| 760 | RotateCredential_ReturnsForbidden_WhenManagementClientIdMismatch | Client binding | The management client id does not match | 403 — one management client cannot rotate another's credentials. | API | [L62](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L62) |
| 761 | RotateCredential_ReturnsForbidden_WhenOwnerIsNotExternalApi | Ownership | The owner is not the external API | 403. | API | [L74](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L74) |
| 762 | RotateCredential_ReturnsForbidden_WhenClientMetadataIsMissing | Missing metadata | No client metadata | 403 — fails closed rather than treating absent metadata as unowned. | API | [L86](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L86) |
| 763 | GetCredential_ReturnsUnauthorized_WithNoToken | Auth gate | No token | 401. | API | [L102](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L102) |
| 764 | GetCredential_ReturnsForbidden_WithoutCorrectRole | Role gate | Wrong role | 403. | API | [L110](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L110) |
| 765 | GetCredential_ReturnsNotFound_WhenClientDoesNotExist | Unknown client | No such client | 404. | API | [L119](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L119) |
| 766 | GetCredential_ReturnsForbidden_WhenOwnerIsNotExternalApi | Ownership | Wrong owner | 403. | API | [L129](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L129) |
| 767 | GetCredential_ReturnsForbidden_WhenClientMetadataIsMissing | Missing metadata | No metadata | 403. | API | [L139](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L139) |
| 768 | GetCredential_ReturnsOk_WithCorrectRole | Read | Correct role | 200. | API | [L149](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/ExternalClient/ExternalClientCredentialTests.cs#L149) |

---

## `tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs`

The native-app counterpart to `WebSiteLoginAndRefreshTests` (rows 456–476) — same flows, tokens in the body instead of cookies. The iOS and Android cases assert a one-year `expires_in`, much longer than the web session.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 769 | OauthToken_ReturnsErrorMessages | Error messages (3 cases) | Three failing requests | The expected messages. | API | [L24](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L24) |
| 770 | OauthToken_ReturnsErrorCodes | Error codes (3 cases) | Three failing requests | The expected codes. | API | [L47](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L47) |
| 771 | OauthToken_PassesThroughParametersToAuth0 | Parameter forwarding (9 cases) | Nine parameters | Each reaches Auth0. | API | [L76](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L76) |
| 772 | ReturnsTokensForEmail | Email login | Log in by email | Tokens returned. | API | [L97](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L97) |
| 773 | ReturnsTokensForSms | SMS login (4 cases, 2 `RealOnly`) | Four clients including iOS and Android | Tokens returned with the per-client expiry. | API | [L122](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L122) |
| 774 | Login_FailsOnUnknownUserNameMapping | Unknown user (`RealOnly`) | An unmapped username | Fails. | API | [L148](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L148) |
| 775 | Login_FailsOnMissingAccessTokenFromAuth0 | Missing access token | Auth0 returns none | Login fails. | API | [L164](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L164) |
| 776 | Login_SucceedsOnMissingRefreshTokenFromAuth0 | Missing refresh token | Auth0 returns none | Login still succeeds — same degradation as row 471. | API | [L181](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L181) |
| 777 | RefreshToken_ReturnsForbiddenForBadRequestToken | Bad token | A bad refresh token | 403. | API | [L204](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L204) |
| 778 | RefreshToken_ReturnsExpiresInSeconds | Refresh expiry (4 cases, 2 `RealOnly`) | Four clients | The per-client `expires_in` is returned. | API | [L222](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L222) |
| 779 | RefreshToken_LogsEventOnSuccess | Refresh event (`RealOnly`) | Refresh | An event lands. | API | [L258](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L258) |
| 780 | RefreshToken_LogsEventOnFailure | Refresh failure event (`RealOnly`) | Fail a refresh | An event lands. | API | [L301](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/OauthTokenLoginAndRefreshTests.cs#L301) |

---

## `tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs`

Builds the events sourced from Auth0 itself (the webhook and Universal Login page), as distinct from the service-sourced events in rows 77–188. Patient is the default user type when no tenant is supplied.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 781 | GetLoginSuccessEvent_SetsAllFieldsCorrectly | Login success | Build the event | All fields set. | Unit | [L33](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L33) |
| 782 | GetLoginSuccessEvent_GivenNullOptionalFields_SetsThemToNull | Optional fields | Omit the optional fields | Null, not empty strings. | Unit | [L88](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L88) |
| 783 | GetLoginSuccessEvent_GivenV3Fields_SetsAllV3FieldsCorrectly | V3 payload | Build with v3 fields | All carried. | Unit | [L98](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L98) |
| 784 | GetULPageEvent_SetsAllFieldsCorrectly | Universal Login page event | Build the event | All fields set. | Unit | [L128](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L128) |
| 785 | GetULPageEvent_GivenCorrelationId_SetsItCorrectly | Correlation | Build with a correlation id | Carried. | Unit | [L169](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L169) |
| 786 | GetULPageEvent_GivenDefaultTenantType_SetsUserTypeToPatient | Default tenant | No tenant supplied | User type is patient. | Unit | [L191](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L191) |
| 787 | GetULPageEvent_GivenProviderTenant_SetsUserTypeToProvider | Provider tenant | Provider tenant | User type is provider. | Unit | [L211](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L211) |
| 788 | GetULPageEvent_GivenClientIdAndClientName_SetsThemCorrectly | Client fields | Build with client id and name | Both carried. | Unit | [L230](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L230) |
| 789 | GetLoginSuccessEvent_GivenDefaultTenantType_SetsUserTypeToPatient | Default tenant | No tenant | Patient. | Unit | [L252](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L252) |
| 790 | GetLoginSuccessEvent_GivenPatientTenant_SetsUserTypeToPatient | Patient tenant | Patient tenant | Patient. | Unit | [L259](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L259) |
| 791 | GetLoginSuccessEvent_GivenProviderTenant_SetsUserTypeToProvider | Provider tenant | Provider tenant | Provider. | Unit | [L266](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L266) |
| 792 | GetLoginSuccessEvent_GivenCorrelationId_SetsItCorrectly | Correlation | A correlation id | Carried. | Unit | [L273](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/Auth0LoggingEventFactoryTests.cs#L273) |

---

## `tests/UnitTests/ExternalClientCredentialServiceTests.cs`

The service behind rows 757–768. Same three ownership conditions, asserted here as validation exceptions rather than HTTP codes, plus the propagate-vs-translate rule for Auth0 failures (rows 803, 804).

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 793 | RotateClientSecret_ReturnsNewSecret_WhenMetadataIsValid | Rotation | Valid metadata | A new secret. | Unit | [L30](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L30) |
| 794 | RotateClientSecret_ThrowsValidationException_WhenManagementClientIdMismatch | Client binding | Mismatched management client id | Validation exception. | Unit | [L45](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L45) |
| 795 | RotateClientSecret_ThrowsValidationException_WhenOwnerMetadataMissing | Missing owner | No owner metadata | Validation exception. | Unit | [L67](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L67) |
| 796 | RotateClientSecret_ThrowsValidationException_WhenOwnerIsNotExternalApi | Wrong owner | Owner is not the external API | Validation exception. | Unit | [L89](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L89) |
| 797 | RotateClientSecret_ThrowsValidationException_WhenClientMetadataIsNull | Null metadata | No metadata at all | Validation exception. | Unit | [L111](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L111) |
| 798 | RotateClientSecret_PropagatesException_WhenAuth0Fails | Upstream failure | Auth0 fails | The exception propagates rather than being converted to a validation error. | Unit | [L129](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L129) |
| 799 | GetClientCredential_ReturnsCredential_WhenClientIsExternalApi | Read | A valid external-API client | The credential. | Unit | [L142](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L142) |
| 800 | GetClientCredential_ThrowsValidationException_WhenClientMetadataIsNull | Null metadata | No metadata | Validation exception. | Unit | [L170](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L170) |
| 801 | GetClientCredential_ThrowsValidationException_WhenOwnerIsNotExternalApi | Wrong owner | Wrong owner | Validation exception. | Unit | [L188](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L188) |
| 802 | GetClientCredential_ThrowsValidationException_WhenOwnerIsNull | Null owner | Null owner | Validation exception. | Unit | [L209](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L209) |
| 803 | GetClientCredential_ThrowsNotFoundException_WhenAuth0Returns404 | 404 translation | Auth0 returns 404 | Translated to not-found. | Unit | [L230](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L230) |
| 804 | GetClientCredential_PropagatesException_WhenAuth0FailsWithNon404 | Other failures | A non-404 Auth0 failure | Propagated — only 404 is translated. | Unit | [L247](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ExternalClientCredentialServiceTests.cs#L247) |

---

## `tests/UnitTests/Login/CorrelationIdFactoryTests.cs`

Packs the tracking and session GUIDs into a single Auth0-safe correlation string so a login can be traced end to end. The constraints are tight: Auth0 caps the length and the character set, and the value must round-trip back to the original GUIDs.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 805 | Build_ValidInputs_ProducesCompositeOfMaxAllowedLength | Length bound | Build from valid inputs | The composite is exactly at Auth0's maximum. | Unit | [L20](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L20) |
| 806 | Build_ValidInputs_OnlyContainsAuth0AllowedCharacters | Character set | Build | Only allowed characters — anything else is rejected by Auth0 at request time. | Unit | [L31](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L31) |
| 807 | Build_RoundTrip_RecoversOriginalGuids | Round trip | Build then unpack | The original GUIDs come back. | Unit | [L39](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L39) |
| 808 | Build_BsidCookieWithTimestampSuffix_RoundTripsToUnderlyingGuid | Cookie normalisation | Build from a suffixed `bsid` | Round-trips to the underlying GUID. | Unit | [L50](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L50) |
| 809 | Build_TwoCallsWithSameInputs_ProduceDifferentCorrelationIds | Per-attempt uniqueness | Build twice from identical inputs | Different ids — each login attempt is distinguishable even for the same session. | Unit | [L61](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L61) |
| 810 | Build_MissingOrUnparseableInputs_FallsBackToStandaloneGuidAndEmitsMetric | Fallback (4 cases) | Four bad-input shapes | A standalone GUID plus a metric — tracing degrades rather than the login failing. | Unit | [L82](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L82) |
| 811 | Build_ValidInputs_DoesNotEmitFallbackMetric | Metric hygiene | Valid inputs | No fallback metric, so the metric means what it says. | Unit | [L101](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L101) |
| 812 | Build_FallbackPath_LogsWarning | Fallback logging | Trigger the fallback | A warning is logged. | Unit | [L111](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L111) |
| 813 | Unpack_StandaloneGuid_ReturnsNull | Unpack, standalone | Unpack a fallback id | Null. | Unit | [L126](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L126) |
| 814 | Unpack_Decodable63CharNonComposite_ReturnsNull | Unpack, look-alike | A decodable but non-composite string of the right length | Null — length alone does not make it a composite. | Unit | [L132](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L132) |
| 815 | Unpack_MalformedComposite_ReturnsNullAndLogsError | Unpack, malformed | A malformed composite | Null and an error logged. | Unit | [L140](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L140) |
| 816 | Unpack_Null_ReturnsNull | Unpack, null | Null input | Null. | Unit | [L156](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/CorrelationIdFactoryTests.cs#L156) |

---

## `tests/UnitTests/Login/RefreshTokenServiceTests.cs`

Refresh across the three user types. Row 819 is the key boundary: a monolith token carrying an identity is rejected with `InvalidUserType` rather than refreshed down the normal path.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 817 | RefreshAccessToken_PatientTokenSuccessfulRefresh_ReturnsTokenAndLogsV2Events | Patient refresh | Refresh a patient token | Token returned and v2 events logged. | Unit | [L41](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L41) |
| 818 | RefreshAccessToken_PracticeUserTokenSuccessfulRefresh_ReturnsTokenAndLogsV2Events | Practice refresh | Refresh a practice token | Token returned and events logged. | Unit | [L85](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L85) |
| 819 | RefreshAccessToken_MonolithTokenWithIdentity_ReturnsInvalidUserTypeError | User-type boundary | A monolith token with an identity | `InvalidUserType` — it must go through the monolith refresh path instead. | Unit | [L129](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L129) |
| 820 | RefreshAccessToken_PatientTokenWithNoIdentifiersParsed_ReturnsInvalidRefreshTokenError | Unparseable patient token | No identifiers parsed | `InvalidRefreshToken`. | Unit | [L146](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L146) |
| 821 | RefreshAccessToken_PracticeUserTokenWithNoIdentifiersParsed_ReturnsInvalidRefreshTokenError | Unparseable practice token | No identifiers parsed | `InvalidRefreshToken`. | Unit | [L189](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L189) |
| 822 | RefreshAccessToken_NullRefreshToken_ReturnsMissingRefreshTokenError | Missing token | Null token | `MissingRefreshToken` — distinct from invalid. | Unit | [L231](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L231) |
| 823 | RefreshAccessToken_InvalidRefreshToken_ReturnsInvalidRefreshTokenError | Invalid token | A bad token | `InvalidRefreshToken`. | Unit | [L252](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L252) |
| 824 | RefreshMonolithAccessToken_SuccessfulRefresh_ReturnsJwtAndLogsEvent | Monolith refresh | Refresh a monolith token | A JWT and an event. | Unit | [L286](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L286) |
| 825 | RefreshMonolithAccessToken_ApiReturnsNull_ReturnsError | Monolith null | The API returns null | Error. | Unit | [L321](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L321) |
| 826 | RefreshMonolithAccessToken_FailsToParseIdentifiers_ReturnsError | Monolith parse failure | Identifiers unparseable | Error. | Unit | [L346](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L346) |
| 827 | DetermineUserTypeFromRefreshToken_WithMonolithIdentity_ReturnsMonolithPracticeUser | Type detection | A monolith identity | `MonolithPracticeUser`. | Unit | [L376](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L376) |
| 828 | DetermineUserTypeFromRefreshToken_NonMonolithUser_ParsesExpectedUserType | Type detection (3 cases) | Three non-monolith tokens | Each parsed to the expected type. | Unit | [L391](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenServiceTests.cs#L391) |

---

## `tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs`

Real DynamoDB coverage for the patient-id ↔ user-name mapping. Row 833 is the notable one: a duplicate patient mapping throws rather than picking one, because silently choosing would attach a login to the wrong patient record.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 829 | InsertPatientUserMapping_Success | Insert | Insert a mapping | Persisted. | Integration | [L34](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs#L34) |
| 830 | BatchWritePatientUserMappings_Success | Batch insert | Batch-write mappings | All persisted. | Integration | [L57](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs#L57) |
| 831 | GetPatientUserMappingByPatientId_Success | Read by patient | Read back by patient id | The mapping. | Integration | [L82](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs#L82) |
| 832 | GetPatientUserMappingByPatientId_WhenPatientIdDoesNotExist_ReturnsNull | Missing patient | Unknown patient id | Null. | Integration | [L106](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs#L106) |
| 833 | GetPatientUserMappingByPatientId_MultipleRecordsForPatientThrowsException | Ambiguity | Two records for one patient | Throws rather than picking one. | Integration | [L114](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs#L114) |
| 834 | DeletePatientUserMapping_Success | Delete | Delete a mapping | Removed. | Integration | [L141](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs#L141) |
| 835 | DeletePatientUserMapping_NoExistingRecord_DoesNothing | Idempotent delete | Delete a nonexistent mapping | No-op, no throw. | Integration | [L175](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs#L175) |
| 836 | GetByUserName_ReturnsUserIfItExists | Read by user name | Read by user name | The mapping. | Integration | [L187](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs#L187) |
| 837 | GetByUserName_ReturnsNullIfNoUser | Missing user | Unknown user name | Null. | Integration | [L197](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs#L197) |
| 838 | BatchTouchPatientUserMappings_WorksWithBatch | Batch touch | Touch a batch | Timestamps updated. | Integration | [L231](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs#L231) |
| 839 | BatchTouchPatientUserMappings_WorksOnTouchingUserMappingAgain | Repeat touch | Touch the same batch again | Still succeeds — touching is idempotent. | Integration | [L262](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PatientUserMappingDynamoPersistenceTests.cs#L262) |

---

## `tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs`

The batching processor that ships login events to Firehose. Its whole job is not to lose events, so most of the file is failure handling: partial batch failures requeue only the failed items (row 844), retries are capped (847), and shutdown drops rather than requeues (849, 850).

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 840 | MissingEnvironmentVariable_LogsErrorAndRequeuesItems | Misconfiguration | No stream name configured | Error logged and items requeued, not dropped. | Unit | [L104](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs#L104) |
| 841 | SuccessPath_SendsBatchToFirehoseAndLogsMetrics | Happy path | Process a batch | Sent to Firehose with metrics. | Unit | [L131](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs#L131) |
| 842 | EventsWithoutEventData_LogAsUnknownType | Untyped events | An event with no data | Logged as unknown type rather than dropped. | Unit | [L171](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs#L171) |
| 843 | BatchException_RequeuesAllItemsForRetry | Whole-batch failure | The batch call throws | Every item requeued. | Unit | [L198](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs#L198) |
| 844 | PartialFailure_RequeuesOnlyFailedItemsAndLogsSeparateMetrics | Partial failure | Some records fail | Only the failures requeue; separate metrics. | Unit | [L222](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs#L222) |
| 845 | MemoryStreamsAreDisposed_AfterProcessing | Resource hygiene | Process a batch | Streams disposed. | Unit | [L265](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs#L265) |
| 846 | FailedItems_RequeuesItemsWithinRetryLimit | Retry budget | Failures below the limit | Requeued. | Unit | [L295](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs#L295) |
| 847 | FailedItems_DropsItemsAtRetryLimit | Retry cap | Failures at the limit | Dropped — the queue cannot grow without bound. | Unit | [L338](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs#L338) |
| 848 | BatchException_MixOfItemsAtAndBelowRetryLimit | Mixed retries | A batch straddling the limit | Each item judged on its own retry count. | Unit | [L388](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs#L388) |
| 849 | Shutdown_DropsAllFailedItemsWithoutRequeue | Shutdown | Fail during shutdown | Dropped, not requeued — nothing will drain the queue. | Unit | [L415](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs#L415) |
| 850 | Shutdown_WithPartialFailure_DropsFailedItemsOnly | Shutdown, partial | Partial failure during shutdown | Only the failures are dropped. | Unit | [L459](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/AuthServiceEventProcessorTests.cs#L459) |

---

## `tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs`

The DynamoDB-stream lambda that mirrors phone and user-mapping changes downstream. A record with no recognisable type throws (rows 852, 853) rather than being skipped, so a schema change fails loudly.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 851 | Verify_EntryPoint_Sets_Up_Correctly | Wiring | Construct the lambda | Dependencies resolve. | Unit | [L38](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs#L38) |
| 852 | Verify_Handler_ThrowsExceptionWhenRecordTypeIsMissingFromPhoneRecord | Unknown phone record | No record type | Throws. | Unit | [L82](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs#L82) |
| 853 | Verify_Handler_ThrowsExceptionWhenRecordTypeIsMissingFromUserMappingRecord | Unknown mapping record | No record type | Throws. | Unit | [L93](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs#L93) |
| 854 | Verify_Handler_Processes_Correctly_ForPhoneRecordInsert | Phone insert | An insert record | Processed. | Unit | [L104](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs#L104) |
| 855 | Verify_Handler_Processes_Correctly_ForPhoneRecordDelete | Phone delete | A delete record | Processed. | Unit | [L127](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs#L127) |
| 856 | Verify_Handler_Processes_Correctly_ForPhoneRecordUpdate | Phone update | An update record | Processed. | Unit | [L153](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs#L153) |
| 857 | Verify_Handler_Processes_Correctly_ForUserMappingInsert | Mapping insert | An insert record | Processed. | Unit | [L182](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs#L182) |
| 858 | Verify_Handler_FailsWhenIdValidationFailsForUserMapping | Bad mapping id | An invalid id | The record fails validation. | Unit | [L205](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs#L205) |
| 859 | Verify_Handler_FailsWhenIdValidationFailsForPhone | Bad phone id | An invalid id | The record fails validation. | Unit | [L303](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs#L303) |
| 860 | Verify_Handler_Processes_Correctly_ForUserMappingDelete | Mapping delete | A delete record | Processed. | Unit | [L406](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs#L406) |
| 861 | Verify_Handler_Batch_Item_Failures | Partial batch | A batch with some bad records | Only the failures are reported back, so good records are not reprocessed. | Unit | [L429](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/StreamProcessorLambdaTests.cs#L429) |

---

## `tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs`

Logs a hashed fingerprint of a refresh token so failures can be correlated without the token itself ever reaching a log. Half the file asserts that no logging path can throw — diagnostics must never break a login (rows 867–872).

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 862 | Fingerprint_NullToken_ReturnsEmpty | Null token | Fingerprint null | Empty. | Unit | [L17](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs#L17) |
| 863 | Fingerprint_EmptyString_ReturnsEmpty | Empty token | Fingerprint an empty string | Empty. | Unit | [L23](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs#L23) |
| 864 | Fingerprint_ValidToken_ReturnsSha256PrefixAndLength | Format | Fingerprint a token | A SHA-256 prefix plus length — never the token. | Unit | [L29](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs#L29) |
| 865 | Fingerprint_DifferentTokens_ProduceDifferentFingerprints | Discrimination | Two tokens | Different fingerprints. | Unit | [L39](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs#L39) |
| 866 | Fingerprint_SameToken_ProducesSameFingerprint | Stability | The same token twice | The same fingerprint, so occurrences correlate. | Unit | [L48](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs#L48) |
| 867 | LogIssued_NullToken_DoesNotThrow | Safety | Log issue with null | No throw. | Unit | [L59](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs#L59) |
| 868 | LogAttempt_NullToken_DoesNotThrow | Safety | Log attempt with null | No throw. | Unit | [L66](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs#L66) |
| 869 | LogSuccess_NullTokens_DoesNotThrow | Safety | Log success with nulls | No throw. | Unit | [L73](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs#L73) |
| 870 | LogAuth0Error_NullToken_DoesNotThrow | Safety | Log an Auth0 error with null | No throw. | Unit | [L82](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs#L82) |
| 871 | LogAuth0Error_WithException_DoesNotThrow | Safety | Log an Auth0 error with an exception | No throw. | Unit | [L89](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs#L89) |
| 872 | LogAttempt_WhenRequestContextThrows_DoesNotThrow | Safety | The request context itself throws | Swallowed — diagnostics never break the login. | Unit | [L102](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RefreshTokenDiagnosticLoggerTests.cs#L102) |

---

## `tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs`

Which practices an SSO user may act on. The allow-list comes from the SAML connection's metadata, and every non-SAML shape returns an empty list rather than a permissive default (rows 876–880).

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 873 | GetAllowedPracticeIdsForUser_WithSamlConnection_ReturnsPracticeIdsFromMetadata | Allow-list | A SAML connection with metadata | The practice ids. | Unit | [L24](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs#L24) |
| 874 | GetAllowedPracticeIdsForUser_WithSamlConnection_SinglePracticeId_ReturnsSinglePracticeId | Single entry | One practice id | Returned. | Unit | [L39](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs#L39) |
| 875 | GetAllowedPracticeIdsForUser_WithSamlConnection_EmptyAllowedPracticeIds_ReturnsEmptyList | Empty list | Empty metadata list | Empty. | Unit | [L53](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs#L53) |
| 876 | GetAllowedPracticeIdsForUser_WithAuth0ConnectionStrategy_ReturnsEmptyList | Non-SAML | An Auth0 database connection | Empty — multi-practice is SSO-only. | Unit | [L66](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs#L66) |
| 877 | GetAllowedPracticeIdsForUser_WithNullConnectionStrategy_ReturnsEmptyList | Null strategy | No connection strategy | Empty. | Unit | [L78](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs#L78) |
| 878 | GetAllowedPracticeIdsForUser_WithSamlConnection_NullMetadata_ReturnsEmptyList | Null metadata | No metadata | Empty. | Unit | [L90](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs#L90) |
| 879 | GetAllowedPracticeIdsForUser_WithSamlConnection_ConnectionIdIsNull_ReturnsEmptyList | Null connection id | No connection id | Empty. | Unit | [L103](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs#L103) |
| 880 | GetAllowedPracticeIdsForUser_WithNonAuth0PracticeUserNamespace_ReturnsEmptyList | Wrong namespace | A non-Auth0 practice-user namespace | Empty. | Unit | [L113](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs#L113) |
| 881 | UpdatePracticeIdForCurrentUser_SsoUser_ValidPracticeId_Success | Switch practice (3 cases) | An SSO user picks an allowed practice | Success. | Unit | [L133](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs#L133) |
| 882 | UpdatePracticeIdForCurrentUser_SsoUser_InvalidPracticeId_ReturnsError | Not allowed | A practice outside the allow-list | Error. | Unit | [L149](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs#L149) |
| 883 | UpdatePracticeIdForCurrentUser_NonSsoUser_ReturnsError | Non-SSO (5 cases) | Five non-SSO user shapes | Error — only SSO users can switch. | Unit | [L170](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MultiPractice/MultiPracticeServiceTests.cs#L170) |

---

## `tests/ApiTests/Lambdas/Auth.Lambdas.StreamProcessor/StreamProcessorLambdaTests.cs`

The deployed counterpart to rows 851–861: the same lambda, but asserted through real SNS/SQS side effects. Every test is `[Category("RealOnly")]` with `Retry(4)`, because the assertions poll a real queue. Row 887 is the phone-stealing case — one patient claiming a number another patient holds must emit events for both.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 884 | SendEventToLambda_WithEmptyEventList_DoesNotPropagateMessagesToSns | Empty batch | Send no events | Nothing published. | API (RealOnly) | [L47](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/Auth.Lambdas.StreamProcessor/StreamProcessorLambdaTests.cs#L47) |
| 885 | SendEventToLambda_WithValidEventListForPhone_PropagatesMessagesToSns | Publish (2 cases) | A phone record and a user-mapping record | Each publishes its own update type. | API (RealOnly) | [L74](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/Auth.Lambdas.StreamProcessor/StreamProcessorLambdaTests.cs#L74) |
| 886 | ReconcilePatientAndSetPhone_PropagatesMessagesToSns | Reconciliation | Reconcile a patient and set a phone | Events published. | API (RealOnly) | [L100](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/Auth.Lambdas.StreamProcessor/StreamProcessorLambdaTests.cs#L100) |
| 887 | PatientGetsPhoneNumberStolen_PropagatesMessagesToSns | Phone transfer | One patient takes another's number | Events published for the transfer. | API (RealOnly) | [L118](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/Auth.Lambdas.StreamProcessor/StreamProcessorLambdaTests.cs#L118) |
| 888 | PatientDeletesTheirAccount_PropagatesMessagesToSns | Deletion | Delete an account | Events published. | API (RealOnly) | [L159](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/Auth.Lambdas.StreamProcessor/StreamProcessorLambdaTests.cs#L159) |
| 889 | InsertThenUpdatePhoneNumber_ShouldRecordEventsToSqs | Insert then update | Two writes | Both recorded. | API (RealOnly) | [L200](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/Auth.Lambdas.StreamProcessor/StreamProcessorLambdaTests.cs#L200) |
| 890 | InsertThenDeletePhoneNumber_ShouldRecordEventsToSqs | Insert then delete | Write then delete | Both recorded. | API (RealOnly) | [L223](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/Auth.Lambdas.StreamProcessor/StreamProcessorLambdaTests.cs#L223) |
| 891 | InsertBorkedRecord_DoesNotRecordEventsToSqs | Malformed record | Write an unusable record | No events — bad data does not reach downstream consumers. | API (RealOnly) | [L246](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/Auth.Lambdas.StreamProcessor/StreamProcessorLambdaTests.cs#L246) |
| 892 | TouchingPhoneRecordAgain_ShouldRecordEventsToSqs | Repeat touch | Touch a phone record twice | Events recorded each time. | API (RealOnly) | [L261](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/Auth.Lambdas.StreamProcessor/StreamProcessorLambdaTests.cs#L261) |
| 893 | TouchingUserRecordAgain_ShouldRecordEventsToSqs | Repeat touch | Touch a user record twice | Events recorded each time. | API (RealOnly) | [L315](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/Auth.Lambdas.StreamProcessor/StreamProcessorLambdaTests.cs#L315) |

---

## `tests/UnitTests/Auth0/PatientTenantAuth0ServiceSetBlockedTests.cs`

Blocking a patient in Auth0. The file's theme is refusing to report success it cannot confirm: Auth0 accepting the patch is not enough, the returned user must actually show the new blocked state (rows 901, 903), and an ambiguous multi-user search throws (898).

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 894 | SetUserBlockedStatus_SingleUserFound_BlocksSuccessfully | Block | One matching user | Blocked. | Unit | [L20](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/PatientTenantAuth0ServiceSetBlockedTests.cs#L20) |
| 895 | SetUserBlockedStatus_SingleUserFound_UnblocksSuccessfully | Unblock | One matching user | Unblocked. | Unit | [L53](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/PatientTenantAuth0ServiceSetBlockedTests.cs#L53) |
| 896 | SetUserBlockedStatus_NoUserFound_ReturnsUserNotFound | Missing user | No match | User-not-found. | Unit | [L86](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/PatientTenantAuth0ServiceSetBlockedTests.cs#L86) |
| 897 | SetUserBlockedStatus_NullResultFromSearch_ReturnsUserNotFound | Null search | Search returns null | User-not-found. | Unit | [L103](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/PatientTenantAuth0ServiceSetBlockedTests.cs#L103) |
| 898 | SetUserBlockedStatus_MultipleUsersFound_ThrowsAndRecordsMetric | Ambiguity | Two matching users | Throws and records a metric rather than blocking an arbitrary one. | Unit | [L118](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/PatientTenantAuth0ServiceSetBlockedTests.cs#L118) |
| 899 | SetUserBlockedStatus_SearchThrows_RethrowsAfterMetric | Search failure | The search throws | Metric then rethrow. | Unit | [L142](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/PatientTenantAuth0ServiceSetBlockedTests.cs#L142) |
| 900 | SetUserBlockedStatus_PatchThrows_RethrowsAfterMetric | Patch failure | The patch throws | Metric then rethrow. | Unit | [L158](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/PatientTenantAuth0ServiceSetBlockedTests.cs#L158) |
| 901 | SetUserBlockedStatus_BlockRequestedButNotConfirmed_ThrowsAndRecordsMetric | Unconfirmed block | Auth0 accepts but does not report blocked | Throws — a silent no-op would leave the account usable. | Unit | [L179](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/PatientTenantAuth0ServiceSetBlockedTests.cs#L179) |
| 902 | SetUserBlockedStatus_UnblockWithNullResponse_SucceedsWithFalse | Null unblock response | Unblock, null response | Treated as unblocked. | Unit | [L207](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/PatientTenantAuth0ServiceSetBlockedTests.cs#L207) |
| 903 | SetUserBlockedStatus_UnblockRequestedButNotConfirmed_ThrowsAndRecordsMetric | Unconfirmed unblock | Auth0 does not report unblocked | Throws. | Unit | [L232](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/PatientTenantAuth0ServiceSetBlockedTests.cs#L232) |

---

## `tests/UnitTests/EventLogging/UserActivityLoggingServiceTests.cs`

The write path for the events built in rows 77–188 and 781–792. V2 hands off to a background queue (row 905) so logging never sits on the login's critical path, and retries are narrowed to service-unavailable only (911, 912).

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 904 | LogActivity_UsesLegacyImplementation | V1 path | Call `LogActivity` | Routes to the legacy implementation. | Unit | [L93](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/UserActivityLoggingServiceTests.cs#L93) |
| 905 | LogActivityV2_EnqueuesToBackgroundQueue | V2 path | Call `LogActivityV2` | Enqueued, not sent inline. | Unit | [L106](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/UserActivityLoggingServiceTests.cs#L106) |
| 906 | InternalLogEventAsync_SavesEventToStreamInEnvironmentVariables | Stream target | Log an event | Written to the configured stream. | Unit | [L132](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/UserActivityLoggingServiceTests.cs#L132) |
| 907 | InternalLogEventAsync_SavesSerializedEventToFirehose | Serialization | Log an event | The serialized form reaches Firehose. | Unit | [L142](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/UserActivityLoggingServiceTests.cs#L142) |
| 908 | InternalLogEventAsync_OnSuccess_LogsUnknownToDataDogIfItCantFindTheEventName | Unknown name | An unrecognised event name | Tagged unknown rather than dropped. | Unit | [L152](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/UserActivityLoggingServiceTests.cs#L152) |
| 909 | InternalLogEventAsync_SerializesUserTypeAsString | User type | Log an event | User type serialized as a string, not an enum ordinal. | Unit | [L175](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/UserActivityLoggingServiceTests.cs#L175) |
| 910 | InternalLogEventAsync_OnSuccess_LogsToDataDog | Success metric | Log successfully | A Datadog metric. | Unit | [L185](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/UserActivityLoggingServiceTests.cs#L185) |
| 911 | InternalLogEventAsync_RetriesOnServiceUnavailable | Retry | Firehose returns service-unavailable | Retried. | Unit | [L215](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/UserActivityLoggingServiceTests.cs#L215) |
| 912 | InternalLogEventAsync_DoesNotRetryOnOtherExceptionTypes | Retry scope | Any other exception | Not retried. | Unit | [L230](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/UserActivityLoggingServiceTests.cs#L230) |
| 913 | InternalLogEventAsync_OnFailure_LogsToDataDog | Failure metric | Logging fails | A Datadog metric. | Unit | [L245](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/EventLogging/UserActivityLoggingServiceTests.cs#L245) |

---

## `tests/UnitTests/Phone/PhoneServiceTests.cs`

OTP send and verify for patient phone numbers. Row 923 is the anti-abuse test and the most interesting in the file: it drives 500 usernames × 5 attempts against an international number to fill the reputation cache, then proves a fresh username is still blocked on that international number while a US number succeeds.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 914 | PatientSendOtpToPhone_SendCodeIfTransferable | Send OTP (5 cases) | Five transferability states | A code is sent only when the number is transferable. | Unit | [L48](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneServiceTests.cs#L48) |
| 915 | PatientSendOtpToPhone_Auth0ClientException | Auth0 failure (2 cases) | Two Auth0 client exceptions | Surfaced as errors. | Unit | [L89](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneServiceTests.cs#L89) |
| 916 | PatientVerifyPhone_VerifyCodeIfTransferable | Verify (5 cases) | Five transferability states | Verification only where allowed. | Unit | [L104](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneServiceTests.cs#L104) |
| 917 | PatientVerifyPhone_FailedToVerifyCode | Bad code (4 cases) | Four failure shapes | Error. | Unit | [L118](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneServiceTests.cs#L118) |
| 918 | PatientVerifyPhone_FailureToUpdatePhone | Persistence failure | The phone write fails after verification | Error. | Unit | [L130](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneServiceTests.cs#L130) |
| 919 | PatientVerifyPhone_Success | Happy path | Verify a valid code | The phone is updated. | Unit | [L144](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneServiceTests.cs#L144) |
| 920 | PatientSendOtpToPhoneForAccountCreation_PhoneExists | Signup OTP (6 cases) | Six existing-phone states | The signup path's own rules, distinct from the update path. | Unit | [L164](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneServiceTests.cs#L164) |
| 921 | PatientSendOtpToPhoneForAccountCreation_Auth0Exception | Auth0 failure (2 cases) | Two exceptions | Errors. | Unit | [L177](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneServiceTests.cs#L177) |
| 922 | PatientSendOtpToPhoneForAccountCreation_RecordCountryCode | Country metric (4 cases) | Four country codes | Each recorded — this is what feeds the abuse signal. | Unit | [L192](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneServiceTests.cs#L192) |
| 923 | ValidateUsernamePhone_BlockMaliciousUsers_UntilCacheFills | Abuse throttle | Drive 500 usernames × 5 attempts at an international number, then try a fresh username | The fresh username is still blocked internationally but allowed on a US number — the block is per-destination reputation, not per-user. | Unit | [L214](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneServiceTests.cs#L214) |

---

## `tests/UnitTests/User/UsernameEmailServiceTests.cs`

Whether an email may become a new account. Row 930 is the precedence rule that matters: a practice-SSO domain normally means "existing provider", but if that email is already a patient, the patient answer wins.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 924 | GetUsernameValidationAndLogResults_IsValid | Valid emails (8 cases) | Eight acceptable emails | Valid for account creation. | Unit | [L30](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UsernameEmailServiceTests.cs#L30) |
| 925 | IsValidNewUsername_IsInvalidFormat | Format (5 cases) | Five malformed emails | Invalid format. | Unit | [L42](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UsernameEmailServiceTests.cs#L42) |
| 926 | IsValidNewUsername_IsDisposableEmail | Disposable (3 cases) | Three throwaway domains | Rejected. | Unit | [L52](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UsernameEmailServiceTests.cs#L52) |
| 927 | IsValidNewUsername_IsZocdocEmail | Internal domain (3 cases) | Three zocdoc.com addresses | Rejected. | Unit | [L63](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UsernameEmailServiceTests.cs#L63) |
| 928 | IsValidNewUsername_IsExistingProviderEmail | Existing provider (4 cases) | Four provider emails | Existing provider. | Unit | [L75](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UsernameEmailServiceTests.cs#L75) |
| 929 | IsValidNewUsername_HasPracticeSsoDomain_ReturnExistingProvider | SSO domain | An email on a practice SSO domain | Treated as an existing provider. | Unit | [L85](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UsernameEmailServiceTests.cs#L85) |
| 930 | IsValidNewUsername_HasPracticeSsoDomain_ButIsExistingPatient_ReturnExistingPatient | Precedence | An SSO-domain email that is already a patient | Existing patient wins over the SSO-domain rule. | Unit | [L102](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UsernameEmailServiceTests.cs#L102) |
| 931 | IsValidNewUsername_IsExistingPatientEmail | Existing patient (4 cases) | Four patient emails | Existing patient. | Unit | [L123](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UsernameEmailServiceTests.cs#L123) |
| 932 | GetLoggingOutcomesForUserLogin_ForAllValidationResults_ReturnsCorrectOutcomes | Outcome mapping | Every `UsernameValidationResult` value via `[Values]` | Each maps to its expected outcome detail and description. | Unit | [L134](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UsernameEmailServiceTests.cs#L134) |
| 933 | GetLoggingOutcomesForUserLogin_ForAllValidationResults_ReturnsNonNull | Total mapping | Every enum value | None returns null, so a new enum member cannot silently produce a blank outcome. | Unit | [L155](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UsernameEmailServiceTests.cs#L155) |

---

## `tests/ApiTests/PatientApi/PatientOauthLoginApiTests.cs`

The patient OAuth authorize/callback pair end to end. Row 941 covers the case that breaks naive preauth-cookie designs: two tabs starting a login in the same browser, where the second overwrites the first's cookie — both must still complete.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 934 | PatientLoginStart_WithValidReturnTo_Returns302AndSetsCookie | Authorize | Start with a valid `return_to` | 302 plus the preauth cookie. | API | [L24](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientOauthLoginApiTests.cs#L24) |
| 935 | PatientLoginStart_WithInvalidReturnTo_Returns400 | Open redirect | An off-site `return_to` | 400. | API | [L69](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientOauthLoginApiTests.cs#L69) |
| 936 | PatientLoginStart_WithAllowedPaths_Returns302 | Allow-list (2 cases) | Two permitted paths | 302. | API | [L82](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientOauthLoginApiTests.cs#L82) |
| 937 | PatientLoginCallback_WithoutPreauthCookie_ReturnsRedirectToError | Missing cookie | Callback with no preauth cookie | Redirect to error. | API | [L101](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientOauthLoginApiTests.cs#L101) |
| 938 | PatientLoginCallback_WithValidCode_RedirectsAndSetsCookies | Happy path | Callback with a valid code | Redirect plus session cookies. | API | [L123](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientOauthLoginApiTests.cs#L123) |
| 939 | PatientLoginCallback_WithInvalidCode_ReturnsRedirectToError | Bad code | An invalid code | Redirect to error. | API | [L193](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientOauthLoginApiTests.cs#L193) |
| 940 | PatientLoginCallback_WithInvalidState_ReturnsRedirectToError | CSRF | A tampered `state` | Redirect to error. | API | [L237](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientOauthLoginApiTests.cs#L237) |
| 941 | PatientLogin_MultiTab_BothTabsComplete | Concurrent tabs | Tab A starts, tab B starts in the same browser, both call back | Both complete — the second tab reuses the shared preauth cookie instead of invalidating the first. | API | [L284](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientOauthLoginApiTests.cs#L284) |
| 942 | PatientLoginCallback_MismatchedPreauthCookie_RedirectsToError | Cookie binding | A preauth cookie that does not match the state | Redirect to error. | API | [L338](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/PatientOauthLoginApiTests.cs#L338) |

---

## `tests/UnitTests/ApiCallers/MonolithAuthBackdoorApiCallerTests.cs`

The client for the monolith's privileged auth endpoints — creating practice staff users and minting monolith cookies from an Auth0 JWT. Every HTTP status the monolith can return is mapped to a distinct result so a 401 is never mistaken for a 403 (rows 948, 949).

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 943 | CreatePracticeStaffUser_Success | Create user | The monolith returns success | Success. | Unit | [L50](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthBackdoorApiCallerTests.cs#L50) |
| 944 | CreatePracticeStaffUser_BadRequest | 400 | The monolith returns 400 | Mapped to a bad-request result. | Unit | [L80](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthBackdoorApiCallerTests.cs#L80) |
| 945 | CreatePracticeStaffUser_Unauthorized | 401 | The monolith returns 401 | Mapped to unauthorized. | Unit | [L117](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthBackdoorApiCallerTests.cs#L117) |
| 946 | CreatePracticeStaffUser_Unknown | Other status | An unexpected status | Mapped to unknown. | Unit | [L149](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthBackdoorApiCallerTests.cs#L149) |
| 947 | SetMonolithAuthCookiesFromAuth0Jwt_Success | Cookie exchange | A valid JWT | Cookies returned. | Unit | [L181](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthBackdoorApiCallerTests.cs#L181) |
| 948 | SetMonolithAuthCookiesFromAuth0Jwt_Unauthorized | 401 | The monolith returns 401 | Unauthorized. | Unit | [L208](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthBackdoorApiCallerTests.cs#L208) |
| 949 | SetMonolithAuthCookiesFromAuth0Jwt_Forbidden | 403 | The monolith returns 403 | Forbidden — distinct from 401. | Unit | [L226](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthBackdoorApiCallerTests.cs#L226) |
| 950 | SetMonolithAuthCookiesFromAuth0Jwt_UnknownResponse | Other status | An unexpected status | Unknown. | Unit | [L251](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthBackdoorApiCallerTests.cs#L251) |
| 951 | SetMonolithAuthCookiesFromAuth0Jwt_UnexpectedException | Transport failure | The call throws | Handled, not propagated raw. | Unit | [L276](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthBackdoorApiCallerTests.cs#L276) |

---

## `tests/UnitTests/PatientImpllTests.cs`

The patient API implementation layer. Rows 956–958 are the audit-trail tests: reading phone numbers in bulk must record a read action with the right object ids, and must not emit an audit entry when no phones were returned.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 952 | PatientSendOtpToPhone_Success | Send OTP | A valid request | Success. | Unit | [L30](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImpllTests.cs#L30) |
| 953 | PatientSendOtpToPhone_TransferFailure | Transfer blocked (6 cases) | Six blocked-transfer shapes | Each returns its own error. | Unit | [L51](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImpllTests.cs#L51) |
| 954 | VerifyPatientPhone_Success | Verify | A valid code | Success. | Unit | [L67](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImpllTests.cs#L67) |
| 955 | VerifyPatientPhone_ErrorCase | Verify errors (9 cases) | Nine failure shapes | Each mapped to its own error. | Unit | [L86](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImpllTests.cs#L86) |
| 956 | BatchGetPhonesByPatientIds_SuccessUpdatesAuditActionToRead | Audit action | Batch-read phones | The audit action is set to read. | Unit | [L119](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImpllTests.cs#L119) |
| 957 | BatchGetPhonesByPatientIds_AddsAuditObjectId | Audit ids | Batch-read phones | The object ids are recorded. | Unit | [L144](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImpllTests.cs#L144) |
| 958 | BatchGetPhonesByPatientIds_DoesNotAuditEmptyPhones | Audit noise | No phones returned | No audit entry. | Unit | [L173](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImpllTests.cs#L173) |
| 959 | CreatePasswordlessPatientUserStart_FlagOn_Success | Passwordless signup | The flag on, a valid request | Success. | Unit | [L194](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImpllTests.cs#L194) |
| 960 | CreatePasswordlessPatientUserStart_FlagOn_BadRequest | Passwordless signup | The flag on, an invalid request | Bad request. | Unit | [L209](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImpllTests.cs#L209) |

---

## `tests/UnitTests/Auth0/BaseAuth0AdministrationTokenCacheTests.cs`

The management-API token cache. Three of eight tests (963–965) exist purely for the thundering-herd case: many parallel callers on a missing or expired token must produce exactly one fetch. Row 966 pins the proactive refresh at 83% of lifetime, and 967–968 keep serving a still-valid token when a refresh fails.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 961 | GetManagementApiToken_FirstTime_ReturnsToken | Cold cache | First call | A token. | Unit | [L44](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/BaseAuth0AdministrationTokenCacheTests.cs#L44) |
| 962 | GetManagementApiToken_MultipleSequentialCalls_UsesCachedToken | Warm cache | Sequential calls | One fetch, cached thereafter. | Unit | [L57](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/BaseAuth0AdministrationTokenCacheTests.cs#L57) |
| 963 | GetAccessTokenAsync_NullToken_MultipleParallelCalls_OnlyOneDoesWorkAndOthersWaitUntilTokenCached | Herd, cold | Parallel calls with no token | One fetch; the rest wait. | Unit | [L72](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/BaseAuth0AdministrationTokenCacheTests.cs#L72) |
| 964 | GetAccessTokenAsync_ExpiredToken_MultipleParallelCalls_OnlyOneDoesWorkAndOthersWaitUntilTokenCached | Herd, expired | Parallel calls on an expired token | One fetch; the rest wait. | Unit | [L92](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/BaseAuth0AdministrationTokenCacheTests.cs#L92) |
| 965 | GetAccessTokenAsync_TokenShouldBeRefreshed_MultipleParallelCalls_OnlyOneDoesWorkAndOthersReturnCachedToken | Herd, refreshing | Parallel calls during a proactive refresh | One fetch; the rest get the still-valid cached token rather than blocking. | Unit | [L119](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/BaseAuth0AdministrationTokenCacheTests.cs#L119) |
| 966 | GetManagementApiToken_RenewsToken_After83PercentToExpiration | Refresh threshold | Advance past 83% of lifetime | Renewed before expiry. | Unit | [L147](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/BaseAuth0AdministrationTokenCacheTests.cs#L147) |
| 967 | GetManagementApiToken_ThrowsOnFailure_ButCurrentTokenIsStillValid | Failure tolerance | A refresh fails while the token is valid | The valid token is still served. | Unit | [L175](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/BaseAuth0AdministrationTokenCacheTests.cs#L175) |
| 968 | GetManagementApiToken_ReturnsExistingGoodJwtOnFailure_ThrowsIfNoGoodToken | Failure escalation | A refresh fails with no good token | Throws only then. | Unit | [L201](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/BaseAuth0AdministrationTokenCacheTests.cs#L201) |

---

## `tests/UnitTests/Login/AccessTokenParsingServiceTests.cs`

Pulls identifiers out of an access token. Half the file (rows 970, 971, 973, 974) asserts the parser never throws on a malformed or claim-less token — a parse failure must degrade to null, not 500 a request.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 969 | ParseXsrfIdentifier | XSRF claim (2 cases) | Two tokens | The identifier parsed. | Unit | [L22](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/AccessTokenParsingServiceTests.cs#L22) |
| 970 | ParseXsrfIdentifier_DoesNotThrow_BadAccessToken | Malformed | A bad token | No throw. | Unit | [L29](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/AccessTokenParsingServiceTests.cs#L29) |
| 971 | ParseXsrfIdentifier_DoesNotThrow_OnNoZti | Missing claim | No `zti` claim | No throw. | Unit | [L35](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/AccessTokenParsingServiceTests.cs#L35) |
| 972 | ParseAuth0UserId_ParsesOutSubToken | Subject (2 cases) | Two tokens | The `sub` parsed. | Unit | [L42](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/AccessTokenParsingServiceTests.cs#L42) |
| 973 | ParseAuth0UserId_DoesNotThrowOnBadAccessToken | Malformed | A bad token | No throw. | Unit | [L57](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/AccessTokenParsingServiceTests.cs#L57) |
| 974 | DoesNotThrow_DoesNotThrowThrowOnNoSub | Missing claim | No `sub` | No throw. | Unit | [L63](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/AccessTokenParsingServiceTests.cs#L63) |
| 975 | ParseUserId_ParsesSub | User id (2 cases) | Two tokens | The user id parsed. | Unit | [L70](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/AccessTokenParsingServiceTests.cs#L70) |
| 976 | ParseProviderIdentifiers_ParsesSubAndPracticeClaims | Provider claims (3 cases) | Three provider tokens | Subject and practice claims parsed together. | Unit | [L89](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/AccessTokenParsingServiceTests.cs#L89) |

---

## `tests/UnitTests/Login/WebCookieServiceTests.cs`

The cookie writer. Row 980 pins an easily-missed detail — when XSRF parsing is off the cookie is set to a literal dash rather than omitted, so downstream code always sees the cookie. Row 982 is the logout guarantee: clearing removes pre-existing cookies as well as the JWT and refresh token.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 977 | SetCookies_SetsJwtCookie | JWT cookie | Set cookies | The JWT cookie is set. | Unit | [L42](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/WebCookieServiceTests.cs#L42) |
| 978 | SetCookies_SetsRefreshToken | Refresh cookie | Set cookies | The refresh token is set. | Unit | [L60](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/WebCookieServiceTests.cs#L60) |
| 979 | SetCookies_SetsXsrfToken | XSRF cookie | Set cookies | The XSRF token is set. | Unit | [L78](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/WebCookieServiceTests.cs#L78) |
| 980 | SetCookies_SetsXsrfTokenToDash_WhenShouldParseXsrfIsFalse | XSRF off | Parsing disabled | The cookie is set to a dash, not omitted. | Unit | [L96](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/WebCookieServiceTests.cs#L96) |
| 981 | RemoveCookies_Works | Removal | Remove cookies | Cleared. | Unit | [L118](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/WebCookieServiceTests.cs#L118) |
| 982 | ClearAllAuthCookies_ClearsExistingCookiesPlusJwtAndRefreshToken | Logout | Clear all | Pre-existing cookies plus the JWT and refresh token are cleared. | Unit | [L149](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/WebCookieServiceTests.cs#L149) |
| 983 | ClearAllAuthCookies_ClearsCurrentPracticeIdCookie | Practice context | Clear all | The current-practice cookie is cleared too, so a logout drops the practice selection from rows 881–883. | Unit | [L172](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/WebCookieServiceTests.cs#L172) |
| 984 | SetCookies_SetsRefreshTokenForPracticeUser | Practice refresh | Set cookies for a practice user | The refresh token is set. | Unit | [L183](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/WebCookieServiceTests.cs#L183) |

---

## `tests/ApiTests/PhoneVerification/PhoneVerificationApiTests.cs`

The deployed phone-verification endpoints. Rows 985 and 989 are the authorization tests — no user, no verification. Row 988 maps Twilio's own error codes to distinct API errors so a carrier rejection is not reported as a Zocdoc bug.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 985 | SendVerificationCode_WithNoUser_ReturnsUnauthorized | Authorization (3 cases) | Three unauthenticated shapes | 401. | API | [L22](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PhoneVerification/PhoneVerificationApiTests.cs#L22) |
| 986 | SendVerificationCode_Success | Send (3 cases) | Three valid requests | Code sent. | API | [L38](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PhoneVerification/PhoneVerificationApiTests.cs#L38) |
| 987 | SendVerificationCode_BadRequest_InvalidPhoneFormat | Validation (4 cases) | Four malformed numbers | 400. | API | [L59](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PhoneVerification/PhoneVerificationApiTests.cs#L59) |
| 988 | SendVerificationCode_TwilioErrorCodes_ReturnsAppropriateError | Carrier errors (4 cases) | Four Twilio error codes | Each mapped to its own API error. | API | [L81](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PhoneVerification/PhoneVerificationApiTests.cs#L81) |
| 989 | VerifyPhoneCode_WithNoUser_ReturnsUnauthorized | Authorization | Unauthenticated | 401. | API | [L108](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PhoneVerification/PhoneVerificationApiTests.cs#L108) |
| 990 | VerifyPhoneCode_Success | Verify | A valid code | Verified. | API | [L122](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PhoneVerification/PhoneVerificationApiTests.cs#L122) |
| 991 | VerifyPhoneCode_ErrorCases_ReturnsAppropriateError | Verify errors (9 cases) | Nine failure shapes | Each mapped to its own API error. | API | [L148](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PhoneVerification/PhoneVerificationApiTests.cs#L148) |

---

## `tests/UnitTests/ApiCallers/MonolithAuthNonEssentialBackdoorApiCallerTests.cs`

The non-essential half of the monolith backdoor — user creation and patient linking that a login can survive without. Compare rows 943–951: same status-mapping discipline, but these calls are the ones whose failures do not block account creation (rows 316, 317).

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 992 | CreateUser_Success | Create | Success from the monolith | Success. | Unit | [L70](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthNonEssentialBackdoorApiCallerTests.cs#L70) |
| 993 | CreateUser_BadRequest | 400 | The monolith returns 400 | Bad request. | Unit | [L84](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthNonEssentialBackdoorApiCallerTests.cs#L84) |
| 994 | CreateUser_Unauthorized | 401 | The monolith returns 401 | Unauthorized. | Unit | [L105](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthNonEssentialBackdoorApiCallerTests.cs#L105) |
| 995 | CreateUser_UnknownError | Other status | An unexpected status | Unknown. | Unit | [L122](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthNonEssentialBackdoorApiCallerTests.cs#L122) |
| 996 | LinkUserToPatient_Success | Link | Success | Linked. | Unit | [L139](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthNonEssentialBackdoorApiCallerTests.cs#L139) |
| 997 | LinkUserToPatient_Unauthorized | 401 | The monolith returns 401 | Unauthorized. | Unit | [L150](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthNonEssentialBackdoorApiCallerTests.cs#L150) |
| 998 | LinkUserToPatient_UnknownError | Other status | An unexpected status | Unknown. | Unit | [L167](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/MonolithAuthNonEssentialBackdoorApiCallerTests.cs#L167) |

---

## `tests/UnitTests/ApiCallers/PatientVaultApiCallerTests.cs`

The client for the patient vault, called during account creation. Row 1005 is the privacy hook: the SPI opt-out cookie must be forwarded on, so a patient's opt-out choice reaches the vault at the moment the profile is created rather than later.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 999 | CreatePatientProfile_Success | Create (4 cases) | Four valid requests | Profile created. | Unit | [L29](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PatientVaultApiCallerTests.cs#L29) |
| 1000 | CreatePatientProfile_BadRequest | 400 | The vault returns 400 | Bad request. | Unit | [L64](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PatientVaultApiCallerTests.cs#L64) |
| 1001 | CreatePatientProfile_UnknownError | Other status | An unexpected status | Unknown. | Unit | [L107](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PatientVaultApiCallerTests.cs#L107) |
| 1002 | ValidatePatientProfile_Success | Validate | A valid profile | Success. | Unit | [L141](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PatientVaultApiCallerTests.cs#L141) |
| 1003 | ValidatePatientProfile_BadRequest | 400 | The vault returns 400 | Bad request. | Unit | [L177](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PatientVaultApiCallerTests.cs#L177) |
| 1004 | ValidatePatientProfile_UnknownError | Other status | An unexpected status | Unknown. | Unit | [L219](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PatientVaultApiCallerTests.cs#L219) |
| 1005 | CreatePatientProfile_PassesSpiOptOutCookieSet | Privacy forwarding (2 cases) | With and without the SPI opt-out cookie | The cookie state is forwarded to the vault. | Unit | [L252](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PatientVaultApiCallerTests.cs#L252) |

---

## `tests/UnitTests/IdentityProvider/PracticeIdentityProviderServiceTests.cs`

Maps an email domain to a practice's SSO connection — the lookup that decides whether a provider login is redirected to a customer IdP. Rows 1008 and 1009 block the two domains that would be catastrophic to register: a public mail domain (which would hijack every gmail user) and zocdoc.com itself.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1006 | GetIdentityProviderByEmailDomainTest | Lookup (4 cases) | Four domains | The matching provider. | Unit | [L26](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/IdentityProvider/PracticeIdentityProviderServiceTests.cs#L26) |
| 1007 | InsertIdentityProviderConfigTest | Insert (4 cases) | Four valid configs | Stored. | Unit | [L48](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/IdentityProvider/PracticeIdentityProviderServiceTests.cs#L48) |
| 1008 | InsertIdentityProviderConfigPublicEmailDomain | Public domain | Register a public mail domain | Rejected. | Unit | [L76](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/IdentityProvider/PracticeIdentityProviderServiceTests.cs#L76) |
| 1009 | InsertIdentityProviderConfigZocdocEmailDomain | Internal domain | Register zocdoc.com | Rejected. | Unit | [L101](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/IdentityProvider/PracticeIdentityProviderServiceTests.cs#L101) |
| 1010 | DeleteIdentityProviderByEmailDomainTest | Delete | Delete by domain | Removed. | Unit | [L126](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/IdentityProvider/PracticeIdentityProviderServiceTests.cs#L126) |
| 1011 | GetIdentityProviderByOrganizationIdTest | Lookup by org | An organization id | The provider. | Unit | [L135](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/IdentityProvider/PracticeIdentityProviderServiceTests.cs#L135) |
| 1012 | GetIdentityProviderByOrganizationId_NoOrganizationUsesPracticeId | Fallback | No organization id | Falls back to the practice id. | Unit | [L174](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/IdentityProvider/PracticeIdentityProviderServiceTests.cs#L174) |

---

## `tests/UnitTests/ProviderUsername/ProviderUsernameServiceTests.cs`

Bulk deletion of provider usernames, with a flag that extends the delete into Auth0. Rows 1017 and 1018 are the important pair: under the flag the Auth0 user is deleted from a constructed id for every requested id, so a missing Dynamo row does not leave an orphaned Auth0 account behind. Row 1019 makes an Auth0 delete failure loud rather than partial.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1013 | BatchDelete_HappyPath_DeletesEachInParallel | Bulk delete | Several usernames | Each deleted in parallel. | Unit | [L25](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameServiceTests.cs#L25) |
| 1014 | BatchDelete_SomeRowsMissing_DeletesFoundOnes | Partial | Some rows absent | The found ones are deleted. | Unit | [L70](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameServiceTests.cs#L70) |
| 1015 | BatchDelete_AllRowsMissing_DoesNothing | All missing | No rows found | No-op. | Unit | [L105](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameServiceTests.cs#L105) |
| 1016 | BatchDelete_DuplicateInputs_DedupesBeforeLookup | Dedupe | Duplicate ids | Deduped before the lookup. | Unit | [L122](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameServiceTests.cs#L122) |
| 1017 | BatchDelete_FlagOn_DeletesAuth0UsersByConstructedIdForAllRequestedIds | Auth0 delete | The flag on | Auth0 users deleted by constructed id for every requested id. | Unit | [L151](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameServiceTests.cs#L151) |
| 1018 | BatchDelete_FlagOn_NoDynamoRows_StillDeletesAuth0Users | Orphan cleanup | The flag on, no Dynamo rows | Auth0 users are still deleted, so no orphan remains. | Unit | [L186](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameServiceTests.cs#L186) |
| 1019 | BatchDelete_FlagOn_Auth0DeleteFails_IncrementsMetricAndThrows | Failure | The Auth0 delete fails | Metric plus throw. | Unit | [L207](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameServiceTests.cs#L207) |

---

## `tests/ApiTests/Auth0Webhook/Auth0WebhookApiTests.cs`

The endpoint Auth0 itself calls. Row 1023 is the one that matters for exposure: the webhook is a public URL, so a missing or wrong shared secret must return 401 rather than accepting forged login events into the analytics stream.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1020 | LogUserActivityEvent_LogsLoginSuccessEvent | Login event | Post a login-success payload | The event is logged. | API (RealOnly) | [L29](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Auth0Webhook/Auth0WebhookApiTests.cs#L29) |
| 1021 | LogUserActivityEvent_WithRefreshProtocol_LogsRefreshIntent | Refresh intent | Post a refresh-protocol payload | Logged with refresh intent. | API (RealOnly) | [L119](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Auth0Webhook/Auth0WebhookApiTests.cs#L119) |
| 1022 | LogUserActivityEvent_WithProviderSecret_ReturnsNoContent | Provider tenant | Post with the provider secret | 204. | API | [L161](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Auth0Webhook/Auth0WebhookApiTests.cs#L161) |
| 1023 | LogUserActivityEvent_WithMissingOrInvalidAuthorizationHeader_ReturnsUnauthorized | Webhook auth | Missing or wrong secret | 401 — the endpoint is public, so the secret is the only gate. | API | [L173](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Auth0Webhook/Auth0WebhookApiTests.cs#L173) |
| 1024 | LogUserActivityEvent_WithEmptyBody_ReturnsBadRequest | Empty body | Post nothing | 400. | API | [L197](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Auth0Webhook/Auth0WebhookApiTests.cs#L197) |
| 1025 | LogUserActivityEvent_WithMissingUserId_ReturnsBadRequest | Missing user | No user id | 400. | API | [L207](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Auth0Webhook/Auth0WebhookApiTests.cs#L207) |

---

## `tests/IntegrationTests/AuthFlowStateDynamoPersistenceTests.cs`

The persisted OAuth state that ties an authorize call to its callback. Row 1027 is deliberate: the state is readable more than once, which is what makes the multi-tab case in row 941 work. Rows 1028 and 1031 bound the exposure with a ten-minute TTL.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1026 | InsertAuthFlowState_Success | Insert | Store a flow state | Persisted. | Integration | [L32](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/AuthFlowStateDynamoPersistenceTests.cs#L32) |
| 1027 | GetAuthFlowStateByOAuthState_CanBeReadMultipleTimes | Repeat read | Read the same state twice | Both succeed — not single-use, which is what allows concurrent tabs. | Integration | [L71](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/AuthFlowStateDynamoPersistenceTests.cs#L71) |
| 1028 | TtlIsSetCorrectly_TenMinutesInFuture | TTL | Store a state | The TTL is ten minutes out. | Integration | [L99](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/AuthFlowStateDynamoPersistenceTests.cs#L99) |
| 1029 | GetAuthFlowStateByOAuthState_Success | Read | Read by state | The record. | Integration | [L125](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/AuthFlowStateDynamoPersistenceTests.cs#L125) |
| 1030 | GetAuthFlowStateByOAuthState_ReturnsNull_WhenNotExists | Missing | Unknown state | Null. | Integration | [L164](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/AuthFlowStateDynamoPersistenceTests.cs#L164) |
| 1031 | GetAuthFlowStateByOAuthState_ReturnsNull_WhenExpired | Expiry | An expired state | Null. | Integration | [L174](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/AuthFlowStateDynamoPersistenceTests.cs#L174) |

---

## `tests/IntegrationTests/PracticeUserAuthIdentityDynamoPersistenceTests.cs`

The Auth0-to-ASP.NET identity mapping for provider users, over real DynamoDB. Row 1037 mirrors row 833 — a duplicate cloud id throws rather than resolving to one of the two, since guessing here would log a user into the wrong provider identity.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1032 | GetPracticeUserAuthIdentityByAuth0UserId_WhenAuth0UserIdIsNotInTable_ReturnsNull | Missing Auth0 id | Unknown id | Null. | Integration | [L32](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PracticeUserAuthIdentityDynamoPersistenceTests.cs#L32) |
| 1033 | GetPracticeUserAuthIdentityByAspnetUserId_WhenAspnetUserIdIsNotInTable_ReturnsNull | Missing ASP.NET id | Unknown id | Null. | Integration | [L42](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PracticeUserAuthIdentityDynamoPersistenceTests.cs#L42) |
| 1034 | InsertPracticeUserAuthIdentityRecord_Success | Insert | Store a record | Persisted. | Integration | [L52](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PracticeUserAuthIdentityDynamoPersistenceTests.cs#L52) |
| 1035 | DeletePracticeUserAuthIdentity_Success | Delete | Delete a record | Removed. | Integration | [L74](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PracticeUserAuthIdentityDynamoPersistenceTests.cs#L74) |
| 1036 | GetPracticeUserAuthIdentityByAspnetCloudId_Success | Read by cloud id | Read by cloud id | The record. | Integration | [L101](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PracticeUserAuthIdentityDynamoPersistenceTests.cs#L101) |
| 1037 | GetPracticeUserAuthIdentityByAspnetCloudId_ThrowsWhenMultipleMatchingRecordsFound | Ambiguity | Two records for one cloud id | Throws rather than choosing. | Integration | [L124](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PracticeUserAuthIdentityDynamoPersistenceTests.cs#L124) |

---

## `tests/UnitTests/Login/RedirectStateValidatorTests.cs`

The post-login redirect decision. Every degenerate input — no state, a null return path, an invalid path — resolves to a safe default rather than an error page, so a broken redirect never blocks a completed login.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1038 | ValidateAndGetRedirectPath_NoState_ReturnsAppropriateDefault | No state (4 cases) | Four state-less shapes | The default path. | Unit | [L26](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RedirectStateValidatorTests.cs#L26) |
| 1039 | ValidateAndGetRedirectPath_NullReturnPath_ReturnsAppropriateDefault | Null path (2 cases) | Two null return paths | The default. | Unit | [L36](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RedirectStateValidatorTests.cs#L36) |
| 1040 | ValidateAndGetRedirectPath_NullReturnPath_OtherField_ReturnsAppropriateDefault | Null path, alternate field (2 cases) | The other carrier field is null | The default. | Unit | [L46](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RedirectStateValidatorTests.cs#L46) |
| 1041 | ValidateAndGetRedirectPath_InvalidPath_ReturnsAppropriateDefault | Open redirect (2 cases) | Two disallowed paths | The default, not the requested target. | Unit | [L84](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RedirectStateValidatorTests.cs#L84) |
| 1042 | ValidateAndGetRedirectPath_ValidPath_ReturnsFullUrl | Allowed path (6 cases) | Six permitted paths | A full URL. | Unit | [L118](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RedirectStateValidatorTests.cs#L118) |
| 1043 | ValidateAndGetRedirectPath_ValidPath_OtherField_ReturnsFullUrl | Alternate field | The path in the other field | A full URL. | Unit | [L127](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/RedirectStateValidatorTests.cs#L127) |

---

## `tests/UnitTests/ProviderUsername/ProviderUsernameRepositoryTests.cs`

Pure authorization coverage: each of the three repository operations is run once with the `AuthServiceReconciliatorApiWrite` JWT role and once with no roles. The negative cases assert both the `UnauthorizedAccessException` and that the persistence layer was never called — a caller without the role cannot reach Dynamo at all.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1044 | InsertProviderUsername_WithCorrectRole_Success | Insert, authorized | The reconciliator write role | Inserted. | Unit | [L19](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameRepositoryTests.cs#L19) |
| 1045 | InsertProviderUsername_WithWrongRole_Failure | Insert, denied | No roles | `UnauthorizedAccessException` and no persistence call. | Unit | [L34](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameRepositoryTests.cs#L34) |
| 1046 | BatchDeleteProviderUsernames_WithCorrectRole_Success | Delete, authorized | The role | Deleted. | Unit | [L51](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameRepositoryTests.cs#L51) |
| 1047 | BatchDeleteProviderUsernames_WithWrongRole_Failure | Delete, denied | No roles | Unauthorized, no persistence call. | Unit | [L71](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameRepositoryTests.cs#L71) |
| 1048 | GetProviderUsernameByAspnetCloudId_WithCorrectRole_Success | Read, authorized | The role | The record. | Unit | [L85](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameRepositoryTests.cs#L85) |
| 1049 | GetProviderUsernameByAspnetCloudId_WithWrongRole_Failure | Read, denied | No roles | Unauthorized — reads are gated too, not just writes. | Unit | [L105](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ProviderUsername/ProviderUsernameRepositoryTests.cs#L105) |

---

## `tests/UnitTests/ServiceAuthV2/SimpleServiceAuthTokenProviderTests.cs`

The service-to-service token cache. Same six-shape contract as the Auth0 management cache (rows 961–968), but the refresh threshold is halfway to expiry rather than 83% (row 1053).

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1050 | GetAccessTokenAsync_FirstTime_ReturnsToken | Cold cache | First call | A token. | Unit | [L36](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/SimpleServiceAuthTokenProviderTests.cs#L36) |
| 1051 | GetAccessTokenAsync_MultipleSequentialCalls_UsesCachedToken | Warm cache | Sequential calls | One fetch. | Unit | [L49](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/SimpleServiceAuthTokenProviderTests.cs#L49) |
| 1052 | GetAccessTokenAsync_MultipleParallelCalls_OnlyOneDoesWork | Herd | Parallel calls | One fetch. | Unit | [L64](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/SimpleServiceAuthTokenProviderTests.cs#L64) |
| 1053 | GetAccessTokenAsync_RenewsToken_AfterHalfwayToExpiration | Refresh threshold | Advance past half the lifetime | Renewed. | Unit | [L83](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/SimpleServiceAuthTokenProviderTests.cs#L83) |
| 1054 | GetAccessTokenAsync_ThrowsOnFailure_ButMightWorkLater | Transient failure | A fetch fails | Throws but leaves the provider usable. | Unit | [L111](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/SimpleServiceAuthTokenProviderTests.cs#L111) |
| 1055 | GetAccessTokenAsync_ReturnsExistingGoodJwtOnFailure_ThrowsIfNoGoodToken | Failure tolerance | A fetch fails with a good token cached | The cached token is served; throws only when there is none. | Unit | [L137](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/SimpleServiceAuthTokenProviderTests.cs#L137) |

---

## `tests/ApiTests/Lambdas/ServiceAuthRelease.Lambda/ServiceAuthReleaseLambdaTests.cs`

The deploy-time lambda that writes a service's roles into the service-auth config. Rows 1058 and 1059 cover the fallback path — a failed write retries against a secondary target, and the test that both fail exists so a release does not silently ship a service with no roles.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1056 | InvokeLambda_Success_ChangeRoles_Success | Role change | Invoke with new roles | Applied. | API (RealOnly) | [L33](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/ServiceAuthRelease.Lambda/ServiceAuthReleaseLambdaTests.cs#L33) |
| 1057 | InvokeLambda_Success_NullRoles_Success | Null roles | Invoke with no roles | Succeeds. | API (RealOnly) | [L59](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/ServiceAuthRelease.Lambda/ServiceAuthReleaseLambdaTests.cs#L59) |
| 1058 | InvokeLambda_PutExceptionWillFallBack | Fallback | The put throws | Falls back. | API (RealOnly) | [L85](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/ServiceAuthRelease.Lambda/ServiceAuthReleaseLambdaTests.cs#L85) |
| 1059 | InvokeLambda_PutException_FallBackAlsoFails | Fallback fails | Both paths throw | Fails loudly. | API (RealOnly) | [L107](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/ServiceAuthRelease.Lambda/ServiceAuthReleaseLambdaTests.cs#L107) |
| 1060 | InvokeLambda_BadRole_WillFail | Validation | An unrecognised role | Fails rather than writing it. | API (RealOnly) | [L122](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/Lambdas/ServiceAuthRelease.Lambda/ServiceAuthReleaseLambdaTests.cs#L122) |

---

## `tests/ApiTests/PatientApi/UserAgentForwardingTests.cs`

Forwards the caller's `ZD-User-Agent` to Auth0 so Auth0's own anomaly detection sees the real client rather than the service. Row 1064 is the defensive one: a non-RFC-compliant header is sanitised and still forwarded instead of failing the token call.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1061 | OauthToken_WithZdUserAgent_ForwardsItToAuth0AsUserAgent | Forwarding | Send the header | Forwarded to Auth0. | API | [L20](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/UserAgentForwardingTests.cs#L20) |
| 1062 | OauthToken_WithoutZdUserAgent_DoesNotOverrideUserAgent | Absent header | No header | The default is left alone. | API | [L45](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/UserAgentForwardingTests.cs#L45) |
| 1063 | OauthToken_WithEmptyZdUserAgent_DoesNotOverrideUserAgent | Empty header | An empty value | The default is left alone. | API | [L66](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/UserAgentForwardingTests.cs#L66) |
| 1064 | OauthToken_WithNonRfcCompliantZdUserAgent_SanitizesAndForwards | Malformed header | An illegal header value | Sanitised and forwarded — it does not break the token call. | API | [L91](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/UserAgentForwardingTests.cs#L91) |
| 1065 | RefreshToken_WithZdUserAgent_ForwardsItToAuth0AsUserAgent | Refresh path | Send the header on refresh | Forwarded. | API | [L122](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/PatientApi/UserAgentForwardingTests.cs#L122) |

---

## `tests/UnitTests/ApiCallers/PracticeUserPermissionsApiCallerTests.cs`

The call that grants roles on SSO login (the behaviour asserted end to end at rows 565, 566, 696). Rows 1066 and 1067 are the guards: a non-SAML connection or a user with no practice id is an `ArgumentException`, not a silent no-grant.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1066 | SetSsoUserRoles_ThrowsArgumentException_ForNonSamlpConnections | Connection guard | A non-SAML connection | `ArgumentException`. | Unit | [L25](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PracticeUserPermissionsApiCallerTests.cs#L25) |
| 1067 | SetSsoUserRoles_ThrowsArgumentException_ForUserWithoutPracticeId | Practice guard | No practice id | `ArgumentException`. | Unit | [L38](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PracticeUserPermissionsApiCallerTests.cs#L38) |
| 1068 | SetSsoUserRoles_CallsPracticeUserPermissionsWithExpectedParameters_Success | Grant | A valid SSO user | Called with the expected parameters. | Unit | [L51](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PracticeUserPermissionsApiCallerTests.cs#L51) |
| 1069 | SetSsoUserRoles_WithAdditionalPractices_CallsPracticeUserPermissionsWithExpectedParameters_Success | Multi-practice | A user with additional practices | Roles granted across them. | Unit | [L81](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PracticeUserPermissionsApiCallerTests.cs#L81) |
| 1070 | SetSsoUserRoles_CallsPracticeUserPermissionsWithExpectedParameters_Failure | Downstream failure | The permissions service fails | Surfaced. | Unit | [L114](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ApiCallers/PracticeUserPermissionsApiCallerTests.cs#L114) |

---

## `tests/UnitTests/Auth0ProtocolIntentMapperTests.cs`

Classifies the Auth0 `protocol` field as a login or a refresh, which is what keeps refreshes out of the login funnel. Row 1073 is the choice worth noting: a null or blank protocol is classified as a *login*, so an unlabelled event inflates logins rather than disappearing.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1071 | Classify_RefreshProtocol_ReturnsRefreshIntentRecognized | Refresh (3 cases) | Three refresh protocols | Refresh intent, recognised. | Unit | [L17](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0ProtocolIntentMapperTests.cs#L17) |
| 1072 | Classify_KnownLoginProtocol_ReturnsLoginIntentRecognized | Login (15 cases) | Fifteen known login protocols | Login intent, recognised. | Unit | [L41](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0ProtocolIntentMapperTests.cs#L41) |
| 1073 | Classify_NullOrWhitespaceProtocol_ReturnsLoginIntentRecognized | Blank (3 cases) | Null and whitespace | Login intent — the default is login, not unknown. | Unit | [L53](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0ProtocolIntentMapperTests.cs#L53) |
| 1074 | Classify_UnknownProtocol_ReturnsLoginIntentNotRecognized | Unknown | An unrecognised protocol | Login intent, flagged unrecognised so new Auth0 protocols are visible. | Unit | [L63](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0ProtocolIntentMapperTests.cs#L63) |
| 1075 | IsRefresh_MatchesRefreshSubstring | Substring match (6 cases) | Six protocol strings | Matched on the refresh substring. | Unit | [L82](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0ProtocolIntentMapperTests.cs#L82) |

---

## `tests/UnitTests/OAuth/InternalUserReturnToUrlValidatorTests.cs`

The internal-services variant of the redirect allow-list, which accepts absolute HTTPS URLs rather than paths. Row 1078 is the subtle one — percent-encoding inside a nested return URL must survive validation untouched, or the inner redirect breaks.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1076 | TryValidate_AcceptsAllowlistedHttpsUrls | Allow-list (4 cases) | Four allow-listed URLs | Accepted. | Unit | [L24](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuth/InternalUserReturnToUrlValidatorTests.cs#L24) |
| 1077 | TryValidate_AcceptsADeepLinkAndKeepsItsQueryString | Query string | A deep link with a query | Accepted with the query intact. | Unit | [L33](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuth/InternalUserReturnToUrlValidatorTests.cs#L33) |
| 1078 | TryValidate_PreservesPercentEncodingInsideANestedReturnUrl | Encoding | A nested, percent-encoded return URL | The encoding survives. | Unit | [L45](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuth/InternalUserReturnToUrlValidatorTests.cs#L45) |
| 1079 | TryValidate_RejectsNullOrEmptyUrls | Empty (3 cases) | Null and empty | Rejected. | Unit | [L63](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuth/InternalUserReturnToUrlValidatorTests.cs#L63) |
| 1080 | TryValidate_RejectsUrlsThatAreNotAbsoluteAllowlistedHttps | Open redirect | A relative or non-allow-listed URL | Rejected. | Unit | [L96](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuth/InternalUserReturnToUrlValidatorTests.cs#L96) |

---

## `tests/UnitTests/Phone/PhoneNumberUpdaterServiceTests.cs`

The three-way write of a phone number to Auth0, DynamoDB and the monolith. Rows 1082, 1083 and 1085 each fail one leg — the point is that a partial write is reported as a failure rather than a success.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1081 | UpdatePhone_Success | Happy path | Update everywhere | Success. | Unit | [L35](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneNumberUpdaterServiceTests.cs#L35) |
| 1082 | UpdatePhone_FailedAuth0 | Auth0 leg | Auth0 fails | Failure. | Unit | [L45](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneNumberUpdaterServiceTests.cs#L45) |
| 1083 | UpdatePhone_FailedDynamoDB | Dynamo leg | Dynamo fails | Failure. | Unit | [L56](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneNumberUpdaterServiceTests.cs#L56) |
| 1084 | UpdatePhoneDdb_Success | Dynamo-only | Update Dynamo only | Success. | Unit | [L69](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneNumberUpdaterServiceTests.cs#L69) |
| 1085 | UpdatePhoneMonolithAndDdb_FailedDynamoDB | Monolith + Dynamo | Dynamo fails | Failure, monolith write not treated as sufficient. | Unit | [L79](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneNumberUpdaterServiceTests.cs#L79) |

---

## `tests/UnitTests/ServiceAuthV2/JwtFetcherTests.cs`

Fetching a service-auth JWT. Rows 1088 and 1089 are diagnostics tests — the error must name the URL on a 404 and include the response body otherwise, because this failure surfaces at service startup with no other context.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1086 | Ctor_ThrowsIfMissingSettings | Configuration | Construct without settings | Throws. | Unit | [L54](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/JwtFetcherTests.cs#L54) |
| 1087 | Ctor_ThrowsIfBadEndpoint | Configuration | A malformed endpoint | Throws. | Unit | [L66](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/JwtFetcherTests.cs#L66) |
| 1088 | FetchJwt_Http404_ErrorMessageIncludesUrl | Diagnostics | A 404 | The error names the URL. | Unit | [L79](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/JwtFetcherTests.cs#L79) |
| 1089 | FetchJwt_OtherHttpError_ErrorMessageIncludesResponseBody | Diagnostics | Another HTTP error | The error includes the response body. | Unit | [L92](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/JwtFetcherTests.cs#L92) |
| 1090 | FetchJwt_Success | Happy path | A successful fetch | A JWT. | Unit | [L108](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/JwtFetcherTests.cs#L108) |

---

## `tests/ApiTests/IdentityProvider/PracticeLogoutApiTests.cs`

Provider logout. Row 1094 is the deliberate design point: logout requires no authentication, so an expired or broken session can still be cleared. Row 1093 is the guarantee that pairs with it — every auth cookie expires, not just the JWT.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1091 | PracticeLogout_RedirectsToAuth0V2Logout | Redirect | Call logout | Redirects to Auth0's v2 logout. | API | [L29](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLogoutApiTests.cs#L29) |
| 1092 | PracticeLogout_LocationHeaderIsUrlEncoded | Encoding | Call logout | The location header is correctly encoded. | API | [L48](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLogoutApiTests.cs#L48) |
| 1093 | PracticeLogout_ExpiresAllAuthCookies | Cookie clearing | Call logout | Every auth cookie is expired. | API | [L66](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLogoutApiTests.cs#L66) |
| 1094 | PracticeLogout_RequiresNoAuthentication | Access | Call logout unauthenticated | Allowed — a broken session can still be cleared. | API | [L88](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/IdentityProvider/PracticeLogoutApiTests.cs#L88) |

---

## `tests/IntegrationTests/ProviderUsernameDynamoPersistenceTests.cs`

The Dynamo layer beneath rows 1044–1049, over real storage.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1095 | BatchInsertProviderUsernames_Single_Success | Single insert | Insert one | Persisted. | Integration | [L34](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/ProviderUsernameDynamoPersistenceTests.cs#L34) |
| 1096 | BatchInsertProviderUsernames_Multiple_Success | Batch insert (3 cases) | Three batch sizes | All persisted. | Integration | [L62](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/ProviderUsernameDynamoPersistenceTests.cs#L62) |
| 1097 | BatchDeleteProviderUsernames_Success | Batch delete | Delete a batch | Removed. | Integration | [L102](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/ProviderUsernameDynamoPersistenceTests.cs#L102) |
| 1098 | GetProviderUsernameByAspnetCloudId_Success | Read | Read by cloud id | The record. | Integration | [L148](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/ProviderUsernameDynamoPersistenceTests.cs#L148) |

---

## `tests/UnitTests/Auth0/ProviderTenantAuth0ClientSearchTests.cs`

Email search in the provider tenant. Unlike the patient path (row 898), a multi-match here returns all of them (row 1101) — provider emails legitimately span practices. Row 1102 guards the search query itself against special characters.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1099 | SearchUserByEmail_SingleMatch_ReturnsIt | Single match | One user | Returned. | Unit | [L49](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ClientSearchTests.cs#L49) |
| 1100 | SearchUserByEmail_NoMatches_ReturnsEmpty | No match | No users | Empty. | Unit | [L63](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ClientSearchTests.cs#L63) |
| 1101 | SearchUserByEmail_MultipleMatches_ReturnsAll | Multiple | Several users | All returned — not an error, unlike the patient tenant. | Unit | [L73](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ClientSearchTests.cs#L73) |
| 1102 | SearchUserByEmail_UrlEncodesSpecialCharacters | Query injection | An email with special characters | URL-encoded before the search. | Unit | [L89](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/ProviderTenantAuth0ClientSearchTests.cs#L89) |

---

## `tests/UnitTests/PatientImplSetBlockedTests.cs`

The API surface over the blocking service in rows 894–903, asserting status codes rather than exceptions.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1103 | SetUserBlockedStatus_InvalidUserAccountId_Returns400 | Validation (5 cases) | Five malformed account ids | 400. | Unit | [L23](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImplSetBlockedTests.cs#L23) |
| 1104 | SetUserBlockedStatus_Success_ReturnsOkWithUserDetails | Block | A valid block | 200 with the user details. | Unit | [L40](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImplSetBlockedTests.cs#L40) |
| 1105 | SetUserBlockedStatus_UserNotFound_Returns404 | Missing user | No such user | 404. | Unit | [L65](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImplSetBlockedTests.cs#L65) |
| 1106 | SetUserBlockedStatus_Unblock_ReturnsOk | Unblock | A valid unblock | 200. | Unit | [L84](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PatientImplSetBlockedTests.cs#L84) |

---

## `tests/UnitTests/Phone/PhoneTransferabilityCheckerTests.cs`

The rule that decides whether a phone number can move to a new patient — the check driven end to end at rows 914, 916, 953. Row 1109 is the anti-abuse link: a locked patient's number cannot be transferred away, so locking an account also protects its phone.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1107 | IsTransferable_GeneralCases | Transfer rules (4 cases) | Four ownership states | Transferable or not per the rule. | Unit | [L23](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneTransferabilityCheckerTests.cs#L23) |
| 1108 | IsTransferable_CanNotTransferPhoneToSelf | Self-transfer | The same patient | Not transferable. | Unit | [L45](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneTransferabilityCheckerTests.cs#L45) |
| 1109 | IsTransferable_CanNotTransferPhoneFromLockedPatient | Locked owner | The current owner is locked | Not transferable. | Unit | [L68](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneTransferabilityCheckerTests.cs#L68) |
| 1110 | IsTransferablePhone_Test | Number-level check (4 cases) | Four numbers | Per-number transferability. | Unit | [L98](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PhoneTransferabilityCheckerTests.cs#L98) |

---

## `tests/UnitTests/ServiceAuthClientServiceTests.cs`

Creating and updating the Auth0 client that backs a service-auth identity. Row 1112 pins the detail that makes rotation work — an update saves the KMS key ARN alongside the client.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1111 | PutAuth0Client_CreatesClient | Create | A new client | Created. | Unit | [L19](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthClientServiceTests.cs#L19) |
| 1112 | PutAuth0Client_UpdatesClient_SavesKeyArn | Update | An existing client | Updated and the key ARN saved. | Unit | [L45](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthClientServiceTests.cs#L45) |
| 1113 | GetServiceAuthClient_Success | Read | An existing client | Returned. | Unit | [L85](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthClientServiceTests.cs#L85) |
| 1114 | GetServiceAuthClient_NoClient | Missing | No client | Handled. | Unit | [L107](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthClientServiceTests.cs#L107) |

---

## `tests/UnitTests/ServiceAuthLambdaTests/ServiceAuthLambdaTests.cs`

The unit-level counterpart to rows 1056–1060. Row 1117 keeps null and empty role entries from being written as roles.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1115 | TestValidRoles | Valid roles (2 cases) | Two valid role sets | Applied. | Unit | [L22](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthLambdaTests/ServiceAuthLambdaTests.cs#L22) |
| 1116 | TestInvalidRole | Invalid role (2 cases) | Two unrecognised roles | Rejected. | Unit | [L58](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthLambdaTests/ServiceAuthLambdaTests.cs#L58) |
| 1117 | TestSkipNullAndEmpty | Blank entries (2 cases) | Null and empty entries | Skipped rather than written. | Unit | [L82](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthLambdaTests/ServiceAuthLambdaTests.cs#L82) |
| 1118 | TestDeleteReturnsSuccess | Delete | Delete a config | Success. | Unit | [L124](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthLambdaTests/ServiceAuthLambdaTests.cs#L124) |

---

## `tests/UnitTests/ServiceAuthV2/AssertionJwtCreatorTests.cs`

Builds the signed assertion a service presents to get a token. Row 1122 covers the local-development escape hatch — with the fake-signature setting on, KMS is never called, which is what lets the suite run without AWS credentials.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1119 | CreateNewJwtAssertion_Jwt_Has_Correct_Claims | Claims | Create an assertion | The expected claims. | Unit | [L64](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/AssertionJwtCreatorTests.cs#L64) |
| 1120 | CreateNewJwtAssertion_Jwt_Claims_Includes_ExpectedRoles | Roles | Create an assertion | The roles are present. | Unit | [L97](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/AssertionJwtCreatorTests.cs#L97) |
| 1121 | CreateNewJwtAssertion_HasGoodSignature | Signature | Create an assertion | The signature verifies. | Unit | [L127](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/AssertionJwtCreatorTests.cs#L127) |
| 1122 | CreateNewJwtAssertion_WithFakeSignatureSetting_DoesNotCallKms | Local mode | The fake-signature setting on | KMS is not called. | Unit | [L147](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/AssertionJwtCreatorTests.cs#L147) |

---

## `tests/ApiTests/InternalServicesApi/KafkaProduceTestApiTests.cs`

A diagnostic endpoint that produces a Kafka message. Rows 1123 and 1124 are the authorization pair — unauthenticated is rejected, and so is an authenticated non-CSR user, so the tool is gated on role rather than merely on login.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1123 | ProduceTestMessage_FailureBecauseNoAuth | Authentication | No credentials | Rejected. | API | [L20](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/KafkaProduceTestApiTests.cs#L20) |
| 1124 | ProduceTestMessage_FailureBecauseNotCsr | Authorization | An authenticated non-CSR user | Rejected. | API | [L31](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/KafkaProduceTestApiTests.cs#L31) |
| 1125 | ProduceTestMessage_CsrUser_Success | Authorized | A CSR user | Success. | API | [L42](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/InternalServicesApi/KafkaProduceTestApiTests.cs#L42) |

---

## `tests/ApiTests/UserApi/MonolithUserRefreshApiTests.cs`

The monolith refresh endpoint. Row 1128 is the one that matters — an expired JWT returns 403 rather than being refreshed, so an expired session cannot be extended indefinitely.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1126 | MonolithUserRefreshToken_Success_ReturnsCookiesWithCorrectClaims | Refresh | A valid token | Cookies with the expected claims. | API | [L25](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/MonolithUserRefreshApiTests.cs#L25) |
| 1127 | MonolithUserRefreshToken_LogsEventOnSuccess | Event | A successful refresh | The event is logged. | API (RealOnly) | [L70](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/MonolithUserRefreshApiTests.cs#L70) |
| 1128 | MonolithUserRefreshToken_WithExpiredJwt_ReturnsForbidden | Expiry | An expired JWT | 403 — expiry is not refreshable. | API | [L102](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/ApiTests/UserApi/MonolithUserRefreshApiTests.cs#L102) |

---

## `tests/IntegrationTests/PracticeIdentityProviderDynamoPersistenceTests.cs`

Real-storage coverage for the SSO domain mapping validated at rows 1006–1012.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1129 | InsertIdentityProviderConfig_Success | Insert | Store a config | Persisted. | Integration | [L33](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PracticeIdentityProviderDynamoPersistenceTests.cs#L33) |
| 1130 | DeleteIdentityProviderByEmailDomain_Success | Delete | Delete by domain | Removed. | Integration | [L62](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PracticeIdentityProviderDynamoPersistenceTests.cs#L62) |
| 1131 | GetIdentityProviderByOrganizationId_Success | Read | Read by organization | The config. | Integration | [L95](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/PracticeIdentityProviderDynamoPersistenceTests.cs#L95) |

---

## `tests/UnitTests/Login/PracticeAuth0LogoutUrlFactoryTests.cs`

The URL built by the logout in rows 1091–1094: the provider tenant's v2 logout, carrying the client id and a URL-encoded final redirect.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1132 | BuildLogoutUrl_TargetsProviderTenantV2Logout | Target | Build the URL | Points at the provider tenant's v2 logout. | Unit | [L36](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeAuth0LogoutUrlFactoryTests.cs#L36) |
| 1133 | BuildLogoutUrl_IncludesClientId | Client id | Build the URL | The client id is present. | Unit | [L44](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeAuth0LogoutUrlFactoryTests.cs#L44) |
| 1134 | BuildLogoutUrl_IncludesUrlEncodedFinalRedirect | Redirect | Build the URL | The final redirect is URL-encoded. | Unit | [L53](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/PracticeAuth0LogoutUrlFactoryTests.cs#L53) |

---

## `tests/UnitTests/OAuth/PatientReturnToPathValidatorTests.cs`

The patient allow-list behind rows 934–936: relative paths only, with seven rejection cases (row 1137) covering the open-redirect shapes.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1135 | TryValidate_AcceptsValidRelativePaths | Accept (2 cases) | Two relative paths | Accepted. | Unit | [L16](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuth/PatientReturnToPathValidatorTests.cs#L16) |
| 1136 | TryValidate_RejectsNullOrEmptyPaths | Empty (3 cases) | Null and empty | Rejected. | Unit | [L27](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuth/PatientReturnToPathValidatorTests.cs#L27) |
| 1137 | TryValidate_RejectsInvalidPaths | Open redirect (7 cases) | Seven disallowed paths | Rejected. | Unit | [L42](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuth/PatientReturnToPathValidatorTests.cs#L42) |

---

## `tests/UnitTests/OAuth/PracticeReturnToPathValidatorTests.cs`

The provider equivalent, with a much wider accept list (20 cases at row 1138) because the provider app has many valid landing pages.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1138 | TryValidate_AcceptsValidRelativePaths | Accept (20 cases) | Twenty provider paths | Accepted. | Unit | [L37](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuth/PracticeReturnToPathValidatorTests.cs#L37) |
| 1139 | TryValidate_RejectsNullOrEmptyPaths | Empty (3 cases) | Null and empty | Rejected. | Unit | [L52](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuth/PracticeReturnToPathValidatorTests.cs#L52) |
| 1140 | TryValidate_RejectsNonRelativePaths | Open redirect (6 cases) | Six absolute or off-site URLs | Rejected. | Unit | [L70](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuth/PracticeReturnToPathValidatorTests.cs#L70) |

---

## `tests/UnitTests/PracticeLogoutControllerTests.cs`

The controller behind rows 1091–1094. Row 1143 pins that the Auth0 logout URL is built exactly once — building it twice would produce a second state and break the redirect.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1141 | Logout_RedirectsToAuth0LogoutUrl | Redirect | Call logout | Redirects to the Auth0 logout URL. | Unit | [L34](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PracticeLogoutControllerTests.cs#L34) |
| 1142 | Logout_ClearsCookies | Cookies | Call logout | Cookies cleared. | Unit | [L43](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PracticeLogoutControllerTests.cs#L43) |
| 1143 | Logout_BuildsAuth0LogoutUrlExactlyOnce | Idempotence | Call logout | The URL is built once. | Unit | [L52](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PracticeLogoutControllerTests.cs#L52) |

---

## `tests/UnitTests/PracticeUserAccountServiceTests.cs`

Row 1145 is the notable one: deleting a user that does not exist locally still calls through to delete the practice user, so a half-created account can be cleaned up rather than becoming undeletable.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1144 | DeletePracticeUserAccount_UserExists | Delete | An existing user | Deleted. | Unit | [L25](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PracticeUserAccountServiceTests.cs#L25) |
| 1145 | DeletePracticeUserAccount_UserDoesNotExist_StillCallsDeletePracticeUser_Succeeds | Orphan cleanup | No local user | The downstream delete still runs and succeeds. | Unit | [L35](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PracticeUserAccountServiceTests.cs#L35) |
| 1146 | UpdatePracticeUserRoles_Success | Roles | Update roles | Applied. | Unit | [L42](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/PracticeUserAccountServiceTests.cs#L42) |

---

## `tests/UnitTests/User/UserEmailValidationServiceTests.cs`

The three domain classifiers behind rows 926, 927 and 1008: disposable, public, and protected-Zocdoc.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1147 | IsDisposableEmailDomain_IsCorrect | Disposable | A table of domains | Classified. | Unit | [L30](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserEmailValidationServiceTests.cs#L30) |
| 1148 | IsPublicEmailDomain_IsCorrect | Public (9 cases) | Nine domains | Classified. | Unit | [L45](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserEmailValidationServiceTests.cs#L45) |
| 1149 | IsProtectedZocdocEmailDomain_IsCorrect | Protected (7 cases) | Seven domains | Classified. | Unit | [L57](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/User/UserEmailValidationServiceTests.cs#L57) |

---

## `tests/UnitTests/Auth0/Auth0AdministrationTokenFetcherTests.cs`

The fetch beneath the cache in rows 961–968.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1150 | FetchToken_Success | Fetch | A successful call | A token. | Unit | [L48](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0AdministrationTokenFetcherTests.cs#L48) |
| 1151 | FetchToken_Failure | Failure | A failed call | Handled. | Unit | [L71](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/Auth0AdministrationTokenFetcherTests.cs#L71) |

---

## `tests/UnitTests/Auth0/InternalServicesTenantAuth0ServiceTests.cs`

The third Auth0 tenant — internal services. Only the two write operations are covered.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1152 | CreateAuth0Client_Success | Create client | Create a client | Created. | Unit | [L26](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/InternalServicesTenantAuth0ServiceTests.cs#L26) |
| 1153 | UpdateAuth0ClientRoles_Success | Update roles | Update client roles | Applied. | Unit | [L82](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/InternalServicesTenantAuth0ServiceTests.cs#L82) |

---

## `tests/UnitTests/Auth0/UserAgentForwardingUnitTests.cs`

The sanitiser behind rows 1061–1065.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1154 | GetValidUserAgent_ReturnsRfcCompliantValue | Sanitising (5 cases) | Five header values | An RFC-compliant value. | Unit | [L27](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/UserAgentForwardingUnitTests.cs#L27) |
| 1155 | GetValidUserAgent_ReturnsNull_WhenNullOrWhitespace | Blank (3 cases) | Null and whitespace | Null, so the default is kept. | Unit | [L45](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Auth0/UserAgentForwardingUnitTests.cs#L45) |

---

## `tests/UnitTests/KafkaProduceTestControllerTests.cs`

The controller behind rows 1123–1125. Row 1157 records a failure metric and rethrows, so a broken Kafka path is visible on a dashboard rather than only in a caller's response.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1156 | ProduceTestMessage_ProducesHardcodedMessageAndReturnsOk | Produce | Call the endpoint | The fixed message is produced, 200. | Unit | [L27](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/KafkaProduceTestControllerTests.cs#L27) |
| 1157 | ProduceTestMessage_ProduceThrows_RecordsFailureMetricAndRethrows | Failure | The produce throws | Metric then rethrow. | Unit | [L73](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/KafkaProduceTestControllerTests.cs#L73) |

---

## `tests/UnitTests/MetricFunnelServiceTests.cs`

The two funnel metrics — OAuth flow start and callback — that make an authorize-without-callback drop-off measurable.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1158 | RecordOAuthFlowStartResult_EmitsCorrectTags | Start metric | Record a flow start | The expected tags. | Unit | [L15](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MetricFunnelServiceTests.cs#L15) |
| 1159 | RecordOAuthFlowCallbackResult_EmitsCorrectTags | Callback metric | Record a callback | The expected tags. | Unit | [L31](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/MetricFunnelServiceTests.cs#L31) |

---

## `tests/UnitTests/OAuthFlowTenantTypeTests.cs`

Persists the tenant type by member name rather than ordinal, so reordering the enum cannot silently reinterpret stored flow states.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1160 | TenantType_PersistsAsMemberName | Serialization (3 cases) | Three tenant types | Stored as the member name, not an ordinal. | Unit | [L17](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuthFlowTenantTypeTests.cs#L17) |
| 1161 | TenantType_RoundTripsThroughDynamoConverter | Round trip | Write then read | The same value. | Unit | [L26](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/OAuthFlowTenantTypeTests.cs#L26) |

---

## `tests/UnitTests/Phone/MaskedPhoneNumberTests.cs`

The masked-phone value type — the form a phone number takes in logs and responses.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1162 | MaskedPhoneNumber_InstantiatesFine | Construction (3 cases) | Three valid numbers | Constructed. | Unit | [L14](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/MaskedPhoneNumberTests.cs#L14) |
| 1163 | MaskedPhoneNumber_FailsToInstantiates | Validation | An invalid number | Rejected. | Unit | [L21](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/MaskedPhoneNumberTests.cs#L21) |

---

## `tests/UnitTests/Service/FeatureFlagServiceTests.cs`

The two flags that gate behaviour elsewhere in the suite — the internal-user response shape and practice Universal Login.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1164 | ShouldReturnInternalUserResponse_ReturnsBasedOnAssignment | Internal-user flag (4 cases) | Four assignments | Follows the assignment. | Unit | [L27](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Service/FeatureFlagServiceTests.cs#L27) |
| 1165 | IsPracticeUniversalLoginEnabled_ReturnsBasedOnAssignment | Universal Login flag (4 cases) | Four assignments | Follows the assignment. | Unit | [L44](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Service/FeatureFlagServiceTests.cs#L44) |

---

## Single-test files

Seven files hold one test each. Two of them (rows 1166, 1168) are scaffolds for the practice-user Auth0 synchroniser lambda that assert only that the handler logs and emits a test metric — the synchroniser's actual behaviour is untested. Row 1171 is not a test at all but a developer script for generating an assertion JWT from a locally-created key pair.

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1166 | VerifyLambda | Synchroniser lambda | Invoke the deployed lambda | It runs — a smoke check, not a behaviour assertion. | Integration | [L44](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/Auth.Lambdas.PracticeUserAuth0Synchronizer.IntegrationTests/LambdaTests.cs#L44) |
| 1167 | InsertServiceAuthClient_Success | Service-auth config (2 cases) | Insert two client configs | Persisted. | Integration | [L28](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/IntegrationTests/ServiceAuthConfigDynamoPersistenceTests.cs#L28) |
| 1168 | Verify_Handler_RecordsTestLog_AndFiresTestMetric | Synchroniser handler | Invoke the handler with an empty SQS event | A "Test log" entry and a `test_metric` — placeholder coverage only. | Unit | [L30](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/LambdaTests/PracticeUserAuth0SynchronizerLambdaHandlerTests.cs#L30) |
| 1169 | Validates_TokesShouldNotBeNullrEmpty | Token validation (5 cases) | Five null/empty token shapes | Rejected. | Unit | [L28](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Login/LoginValidationServiceTests.cs#L28) |
| 1170 | IsPatientLocked_DelegatesToUserLocking | Lock check (2 cases) | Locked and unlocked | Delegates to the user-locking service (the repo mapped separately), which is what row 1109 relies on. | Unit | [L17](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/Phone/PatientLockCheckerTests.cs#L17) |
| 1171 | GenerateAssertionJwt | Developer script | Generate an assertion JWT from a pasted key pair | A `[Test]`-annotated utility with setup instructions in a comment; not product coverage. | Unit (script) | [L15](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthProofOfConcept.cs#L15) |
| 1172 | GetSignatureTest | KMS signing | Sign a payload | A signature. | Unit | [L18](https://github.com/Zocdoc/auth-service/blob/fa9a039b0709e34f520baa1323897360b6719603/tests/UnitTests/ServiceAuthV2/JwtSignerTests.cs#L18) |

---

## Observations

**The suite is large but unevenly distributed.** 1,172 tests across 101 files, and the top ten files hold roughly a third of them. `PatientApiTests.cs` alone is 76 tests. The long tail is thin: 24 files have three or fewer, and seven have exactly one.

**Authorization is proven in `tests/ApiTests/`, not in the unit tests.** The unit projects mock the identity, so they assert that a service *asks* the right question. Only the API tests exercise the real gate. Two files are pure authorization coverage — `ProviderUsernameRepositoryTests.cs` (rows 1044–1049), which runs every operation once with the `AuthServiceReconciliatorApiWrite` role and once with none, and `KafkaProduceTestApiTests.cs` (1123–1125), which separates unauthenticated from authenticated-but-not-CSR.

**`[Category("RealOnly")]` marks the tests that cannot run against the mock.** They assert on Firehose, SNS and SQS side effects the deployed stack produces — the stream-processor API tests (884–893), the Auth0 webhook events (1020, 1021), the service-auth release lambda (1056–1060), and the monolith refresh event (1127). A green local run does not cover any of them. Several also carry `Retry(4)` because they poll real queues.

**Monolith coupling is deliberately asymmetric.** Patient account *creation* survives a monolith failure (rows 316, 317, 329, 330, 444, 445, 452, 453) but provider login does not (346, 375). The split runs through the api-caller layer too: the "non-essential" backdoor (992–998) is the one whose failures are tolerated.

**Ambiguity is an error everywhere identity is involved.** Two patient mappings for one patient id throws (833), two auth identities for one cloud id throws (1037), two Auth0 patients for one email throws (898), and two service-auth credentials past the rotation window throws (714–717). The one place multiplicity is allowed is provider-tenant email search (1101), where an email legitimately spans practices.

**Redirect validation is layered and repeated.** There are four validators — patient paths (1135–1137), practice paths (1138–1140), internal-services absolute URLs (1076–1080), and the state-carried redirect (1038–1043) — and every `returnTo` is re-validated at callback time as well as at authorize time (289, 370, 550, 551). The failure modes differ by surface: internal services falls back to a default (537, 551, 647) while the provider flow 400s on a missing `returnTo` (553).

**Logging and metrics are treated as a product surface.** Two near-identical 56-test event-factory files (77–132 and 133–188) cover V1 and V2 side by side — V2 did not retire V1. Every tag has an explicit unknown/null fallback so a missing attribute never drops a metric, `MetricName_IsCorrect` (756) exists because a rename silently orphans dashboards, and the diagnostic logger's entire second half (867–872) asserts that no logging path can throw.

**Caching has one shape, applied twice, with different thresholds.** The Auth0 management token cache (961–968) and the service-auth token provider (1050–1055) share a six-test contract — cold, warm, parallel-herd, proactive renewal, failure-with-valid-token, failure-without. The renewal thresholds differ: 83% of lifetime for Auth0, halfway for service auth.

**Known thin spots.** The practice-user Auth0 synchroniser lambda has only placeholder coverage — rows 1166 and 1168 assert a test log and a test metric, nothing about synchronisation. `ServiceAuthProofOfConcept.cs` (1171) is a developer script carrying a `[Test]` attribute rather than a test. And the phone abuse throttle (923) is covered by exactly one test, which builds its cache from 2,500 in-process calls.
