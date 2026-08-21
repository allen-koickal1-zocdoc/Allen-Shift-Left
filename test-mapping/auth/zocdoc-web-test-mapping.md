# zocdoc_web (auth-owned paths) - Unit Test Mapping

<!-- test-mapping-meta
repo: Zocdoc/zocdoc_web
branch: master
commit: eed912c1362a8e6c62d11ed6b3245f01cc6e7530
generated: 2026-08-21
test-type: unit
scope: ZocDoc.Security, PracticeAuthorization, Apis/PracticeUserRolesPrivate
granularity: one row per test class
-->

> Source: [`Zocdoc/zocdoc_web`](https://github.com/Zocdoc/zocdoc_web/tree/eed912c1362a8e6c62d11ed6b3245f01cc6e7530) @ `eed912c` (branch `master`)

The Auth team's surface inside the monolith. Scope was taken from `CODEOWNERS`: three test projects covering the legacy ASP.NET membership stack, the OAuth2 authorization server the monolith still hosts, the Auth0/Cognito/Apple identity-provider adapters, and the practice-user permission model.

**188 test classes / 2,180 test methods.** Rows are one per test class, ordered by project and then by feature area; within an area, the largest class first.

Three projects:

- **`ZocDoc.Security/ZocDoc.Security.Tests/`** — 174 classes. Passwords, sessions, JWTs, identity providers, the membership provider, and provider/patient identity.
- **`PracticeAuthorization/PracticeAuthorization.Test/`** — 9 classes. Practice-level authorization including the FGA migration.
- **`Apis/PracticeUserRolesPrivate/Zocdoc.PracticeUserRolesPrivate.Tests/`** — 5 classes. The private roles API.

One scope note: `CODEOWNERS` still assigns `/Zocdoc.AuditLogging/` to the Auth team, but that directory no longer exists in the repo — it became the standalone `audit-logging-service`, mapped separately. The entry is stale and has no tests behind it.

---

## `ZocDoc.Security.Tests/` — root

The classes that answer "who is this user and what are they allowed to do to other users". The two largest are deletion-permission matrices: row 1 covers Zocdoc-internal admin roles and row 2 covers practice staff deleting each other, both enumerating every actor/target role pair rather than testing a rule in the abstract.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 1 | AdminUserManagementPermissionCheckerTests | Internal deletion rights (40 tests) | Every admin/management/CSR/CSR-marketing actor against every target user type | The full matrix of who may delete whom — CSR can delete a patient but not a Zocdoc employee, CSR-marketing only Answers users. | Unit | [L15](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/AdminUserManagementPermissionCheckerTests.cs#L15) |
| 2 | PracticeStaffUserManagementCheckerTests | Practice staff management (23 tests) | Delete and role-edit checks across MPL, full-admin, PUP-authorized and self-target cases | Staff cannot delete themselves, cannot act without PUP authorization, and the MPL target rule differs from the non-MPL one. | Unit | [L25](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/PracticeStaffUserManagementCheckerTests.cs#L25) |
| 3 | CurrentProviderDetectorTests | Current provider/practice resolution (17 tests) | Resolve for auth identities and RBAC practice users, with MPL on and off, plus cookie-based impersonation | Returns null rather than a default whenever the user is not in the provider role or has no provider. | Unit | [L20](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/CurrentProviderDetectorTests.cs#L20) |
| 4 | IdentityCreatorServiceTests | Identity construction (14 tests) | Each strategy type — aspxauth, public token, Auth0 token — including linked and unlinked ASP.NET users and cloud-id mismatches | Covers the `aspnet_cloud_id_mismatch` path directly; an unsupported strategy throws rather than producing a partial identity. | Unit | [L27](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityCreatorServiceTests.cs#L27) |
| 5 | CsrUserDetectorTests | CSR detection (10 tests) | CSR, CSR super-user, external CSR and Zocdoc-staff checks with and without a current user | Every check is false with no user; super-user requires that exact role, and staff detection also consults the trusted IP. | Unit | [L14](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/CsrUserDetectorTests.cs#L14) |
| 6 | ProviderAuthorizationTests | Inactive/blocked practice users (10 tests) | Churned, back-from-churn, missing, null and active practices | A churned practice makes its staff inactive; back-from-churn is treated as active again. | Unit | [L22](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/ProviderAuthorizationTests.cs#L22) |
| 7 | AuthCookieAuditorTests | Cookie consistency audit (4 tests) | Mismatched values, a null cookie, the flag off, and a throwing dependency | The auditor reports mismatches but swallows its own exceptions, so auditing cannot break a request. | Unit | [L17](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/AuthCookieAuditorTests.cs#L17) |
| 8 | AspxAuthRenewalServiceTests | Forced aspxauth renewal (3 tests) | No existing token, a ticket already reissued, and the renewal itself | Renewal is skipped when there is nothing to renew or a new ticket is already on the response. | Unit | [L15](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/AspxAuthRenewalServiceTests.cs#L15) |
| 9 | ConcealableTests | Concealed values (3 tests) | Reveal when allowed, reveal when not, and the thrown message | A concealed value throws on unauthorized reveal rather than returning a placeholder. | Unit | [L9](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/ConcealableTests.cs#L9) |
| 10 | SecureRandomGuidGeneratorTests | Secure GUID generation (3 tests) | Non-empty, unique across calls, and the random bits set | Guards the randomness that token identifiers depend on. | Unit | [L9](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/SecureRandomGuidGeneratorTests.cs#L9) |
| 11 | StringSanitizerTests | Name sanitising (3 tests) | Bad characters, numbers, and a mix | Filtering is applied to display names. | Unit | [L7](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/StringSanitizerTests.cs#L7) |
| 12 | AlerterAuthorizationTests | Churned-user check (2 tests) | With and without a user | No user is treated as churned — the safe default. | Unit | [L11](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/AlerterAuthorizationTests.cs#L11) |
| 13 | UserCategorizerTest | User categorisation (1 test) | Categorise a user | A single assertion over the category rule. | Unit | [L13](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/UserCategorizerTest.cs#L13) |

---

## `ZocDoc.Security.Tests/IdentityProvider/`

The largest area — 23 classes, 309 tests — covering three external identity providers (Auth0, Cognito, Apple) plus the social-login web flow. The four JWT validators (rows 17, 20, 24, 29) all run the same seven-way negative battery: no signing key, bad signature, unsigned, expired, wrong audience, wrong issuer, then the legitimate token.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 14 | SocialLoginHandlerTests | Social sign-in (43 tests) | Monolith id found/not found, no id, unapproved, locked, locked-then-unlocked, and the OOM lock flag with a throwing OOM check | The largest class in the mapping. Falls back to email login when no monolith id matches, and when the OOM lock check throws it falls back to the monolith result rather than failing the login. | Unit | [L30](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/WebFlow/SocialLoginHandlerTests.cs#L30) |
| 15 | Auth0ServiceTests | Auth0 operations (36 tests) | Delete user and secondary SMS users, refresh, user info, and passwordless start including phone-number stealing | Refresh is rejected when the token is not owned by the patient; passwordless start handles a number already held by another account. | Unit | [L28](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/Auth0/Auth0ServiceTests.cs#L28) |
| 16 | CognitoUserLoginServiceTests | Cognito login (35 tests) | Valid login, not-found, not-authorized, invalid password, bad JWT, throttling with retry, and email case | Distinguishes "user not found" from "bad credentials" internally without leaking it, lower-cases the email, and retries on too-many-requests. | Unit | [L27](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/CognitoUserLoginServiceTests.cs#L27) |
| 17 | Auth0JwtValidationServiceTests | Auth0 JWT validation (21 tests) | Each failure mode run twice, once per tenant — audience, issuer, subject, expiry, signature | Patient and provider tenants are validated independently, so a token from one tenant cannot satisfy the other. | Unit | [L22](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/Auth0/Auth0JwtValidationServiceTests.cs#L22) |
| 18 | CognitoUserWriteServiceTests | Cognito writes (18 tests) | Create, reset-password initiation and confirmation, and the failure-logging matrix | Which sink each failure goes to is asserted per exception type — throttling to the datalake only, limit-exceeded to Datadog only. Row 18 also pins that the real password is sent on CI only, never in prod. | Unit | [L30](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/CognitoUserWriteServiceTests.cs#L30) |
| 19 | WebFlowValueServiceTests | Social-flow session state (17 tests) | Nonce issue/consume, and id-token and return-url storage with late, null and missing expiry | Every read returns null once the stored time is too old, so a stale social flow cannot be resumed. | Unit | [L12](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/WebFlow/WebFlowValueServiceTests.cs#L12) |
| 20 | AppleJwtValidatorTests | Apple token validation (16 tests) | The seven-way negative battery plus a 60-minute freshness bound and the debug-only expired-token allowance | Apple tokens are accepted for at most 60 minutes; expired tokens pass only in debug with the flag on. | Unit | [L21](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/Apple/AppleJwtValidatorTests.cs#L21) |
| 21 | Auth0JwtRequestValidationServiceTests | Token extraction (15 tests) | Header present, header absent with a cookie and the flag on, malformed header — across patient, provider and internal-services tenants | When both a header and a cookie are present the header wins, so a stale cookie cannot override a fresh token. | Unit | [L15](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/Auth0/Auth0JwtRequestValidationServiceTests.cs#L15) |
| 22 | CognitoClientServiceTests | Cognito client (14 tests) | Create, list, delete, email update, user count, and both retry wrappers | Email is lower-cased on every entry point, which is the invariant the whole Cognito path depends on. | Unit | [L26](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/CognitoClientServiceTests.cs#L26) |
| 23 | Auth0SigningKeyServiceTests | Signing-key cache (13 tests) | Fetch, cache, and not-found — once per tenant | A miss returns an empty list and makes exactly one API call, so an unknown key id cannot stampede Auth0. | Unit | [L25](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/Auth0/Auth0SigningKeyServiceTests.cs#L25) |
| 24 | CognitoJwtValidatorTests | Cognito token validation (13 tests) | The seven-way battery, plus access and id tokens, a second key set, and principal extraction | A second set of signing keys is accepted, which is what makes key rotation non-breaking. | Unit | [L18](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/Cognito/CognitoJwtValidatorTests.cs#L18) |
| 25 | IdentityProviderUserStatusServiceTests | Social mappings (13 tests) | Add, read, delete and enumerate social mappings; password/passwordless status | A blank social name resolves to null rather than matching a row. | Unit | [L13](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/IdentityProviderUserStatusServiceTests.cs#L13) |
| 26 | CognitoUserReadServiceTests | Cognito reads (11 tests) | Existence, by-email, and native-user lookups with null, empty and social-only responses | Native-user lookup filters out social users, so a social account is never treated as a password user. | Unit | [L19](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/CognitoUserReadServiceTests.cs#L19) |
| 27 | CognitoIdentityProviderUserFactoryTests | Attribute mapping (9 tests) | From a user type and from a dictionary, including gender, a birthday edge case, and malformed identities fields | Malformed or missing identity fields are tolerated on the dictionary path but a null user type throws. | Unit | [L17](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/Cognito/CognitoIdentityProviderUserFactoryTests.cs#L17) |
| 28 | Auth0TokenOwnerCheckerTests | Token ownership (8 tests) | Email, patient id and Auth0 id mismatches, missing subject and patient claims, and case sensitivity | Every identifier must agree before a token is treated as the patient's; the username comparison is case-insensitive. | Unit | [L21](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/Auth0/Auth0TokenOwnerCheckerTests.cs#L21) |
| 29 | SocialLoginTokenValidatorTests | Validator dispatch (6 tests) | An unknown issuer, a delegate throwing a handled type, and one throwing an unhandled type | Handled exceptions become errors; unhandled ones propagate rather than being swallowed into a generic failure. | Unit | [L24](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/Common/SocialLoginTokenValidatorTests.cs#L24) |
| 30 | NonceMakerTests | Nonce generation (5 tests) | Round trip, bad input, and GUID parsing | A non-GUID source returns null rather than a fabricated nonce. | Unit | [L12](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/WebFlow/NonceMakerTests.cs#L12) |
| 31 | AppleSigningKeyServiceTests | Apple key cache (4 tests) | Matching id only, caching, not-found, and an HTTP failure | A missing key throws; an HTTP failure is logged and rethrown rather than cached as absent. | Unit | [L23](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/Apple/AppleSigningKeyServiceTests.cs#L23) |
| 32 | AppleValidationSettingsTests | Apple audiences (4 tests) | Prod, debug, the expired-token flag, and empty client ids | The test audience exists only in debug; empty client ids throw at configuration time. | Unit | [L16](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/Apple/AppleValidationSettingsTests.cs#L16) |
| 33 | ThirdPartyLoginUrlFactoryTests | Provider URLs (3 tests) | URL generation, state and nonce, and missing config | Missing core config throws rather than emitting a URL that would fail at the provider. | Unit | [L11](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/WebFlow/ThirdPartyLoginUrlFactoryTests.cs#L11) |
| 34 | CognitoOAuthClientTests | Token exchange (2 tests) | A good and a bad response | Minimal coverage of the Cognito OAuth client. | Unit | [L19](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/CognitoOauthClientTests.cs#L19) |
| 35 | CognitoUserAdminServiceTests | Admin operations (2 tests) | Delete and user count | Request shape only. | Unit | [L13](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/CognitoUserAdminServiceTests.cs#L13) |
| 36 | IdentityProviderUserTests | DTO mapping (1 test) | Map to the DTO | A single mapping assertion. | Unit | [L8](https://github.com/Zocdoc/zocdoc_web/blob/eed912c1362a8e6c62d11ed6b3245f01cc6e7530/ZocDoc.Security/ZocDoc.Security.Tests/IdentityProvider/IdentityProviderUserTests.cs#L8) |

---

## `ZocDoc.Security.Tests/OAuth2/`

The OAuth2 authorization server the monolith still hosts for the patient mobile app and the provider alerter. Four sub-areas: the token/validation services at the root, per-client resource-owner rules under `Clients/`, the RSA key handling under `Keys/`, and the newer JWT-assertion service-to-service flow under `ServiceAuth/`. The recurring theme is failure shape — most classes spend more tests on how a bad token is rejected than on the happy path.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 37 | OAuth2ServiceTest | Token requests and access-token validation (36 tests) | Both AB-flag states, then every validation failure: extraction error, null principal, invalid proxy, invalid client, revoked and expired tokens — each with `SetForbiddenResponseOnFailure` true and false | The 403 is opt-in: with the flag off a failed validation returns a false result and writes no response, so callers must check the result themselves. | Unit | [L32]($R/OAuth2ServiceTest.cs#L32) |
| 38 | OAuth2AuthorizationServiceTests | Authorization records and token state (21 tests) | Add authorization with expiring and non-expiring refresh tokens, then access- and refresh-token validity across missing, expired, revoked and mismatched-proxy cases | An invalid proxy throws rather than returning false, and a proxy/user mismatch alerts before returning false — it is treated as a possible attack, not a normal miss. | Unit | [L25]($R/Authorization/OAuth2AuthorizationServiceTests.cs#L25) |
| 39 | PatientMobileAppWithJwtClientTests | JWT-issuing mobile client (20 tests) | Token lifetimes under good, off and malformed AB config, then resource-owner validation with valid, invalid, flag-off and bad-token patients | The JWT variant fails closed twice — a valid patient still fails if the flags are off or the issued token does not validate. | Unit | [L22]($R/Clients/PatientMobileAppWithJwtClientTests.cs#L22) |
| 40 | OAuth2MultiFactorAuthServiceTests | MFA on the token endpoint (16 tests) | Parameter extraction across casing variants, the legacy alerter user-agent path, and missing authorization; then MFA validation with each of token, code and id absent | A missing verification piece silently falls back to the password flow rather than erroring — the fallback is the tested behaviour, not an edge case. | Unit | [L19]($R/OAuth2MultiFactorAuthServiceTests.cs#L19) |
| 41 | PatientMobileAppClientTests | Legacy mobile client (16 tests) | The same lifetime matrix, then resource-owner validation for patient, provider and unknown user types | An unknown user type throws; the provider path is exercised through the patient client because both share the resource-owner entry point. | Unit | [L21]($R/Clients/PatientMobileAppClientTests.cs#L21) |
| 42 | ProviderAlerterClientTests | Provider alerter client (15 tests) | Lifetimes, resource-owner validation for doctor and non-doctor users, scope checks, then the login side for valid, invalid-scope and non-existent users | Scope is enforced twice — once on validate and again on login — so a scope-less caller cannot validate then log in. | Unit | [L22]($R/Clients/ProviderAlerterClientTests.cs#L22) |
| 43 | ConstantsTests | Protocol constants (13 tests) | Assert each scope, protocol string, URL and the default expiration timespan still exists with its expected value | A change-detector on the wire contract: these strings are consumed by shipped mobile builds, so renaming one is a breaking change. | Unit | [L10]($R/ConstantsTests.cs#L10) |
| 44 | OAuth2AppSettingGetterTests | Key material from app settings (9 tests) | Unencrypted key, encrypted key, encrypted key with an uninitialised helper, empty setting, empty decrypt result, and keys with junk prefix/suffix | Empty inputs throw rather than yielding an empty key, but junk around a valid PEM is tolerated. | Unit | [L15]($R/Keys/OAuth2AppSettingGetterTests.cs#L15) |
| 45 | ServiceAuthAssertionValidationServiceTests | JWT assertion validation (8 tests) | A successful validation then each rejection: wrong audience, subject/issuer mismatch, missing subject, expired token, invalid lifetime, failed signature, and no client registration | Every field of the assertion is checked independently, so a single failure maps to a specific error type rather than a generic invalid-token. | Unit | [L24]($R/ServiceAuth/ServiceAuthAssertionValidationServiceTests.cs#L24) |
| 46 | OAuth2CryptoKeyStoreTests | Crypto key store (8 tests) | Lookup by handle, primary and secondary keys, an invalid value, listing all keys, and the two mutating methods | Store and remove throw `NotSupportedException` — the store is deliberately read-only at runtime. | Unit | [L15]($R/Keys/OAuth2CryptoKeyStoreTests.cs#L15) |
| 47 | ServiceAuthClientRegistrationServiceTests | Service-auth client registry (8 tests) | Get one, get all, insert and delete, each paired with a wrong-role case | Registration writes are role-gated and throw on insufficient roles; reads return null rather than throwing when nothing is registered. | Unit | [L16]($R/ServiceAuth/ServiceAuthClientRegistrationServiceTests.cs#L16) |
| 48 | AuthorizationServerHostTests | DotNetOpenAuth host adapter (7 tests) | Client lookup for valid and invalid ids, the resource-owner credential grant for invalid clients and valid credentials, access-token creation, and refresh-token validity | An unknown client returns null rather than throwing, and the grant check denies rather than erroring — the host is written to keep the protocol response well-formed. | Unit | [L27]($R/AuthorizationServerHostTests.cs#L27) |
| 49 | OAuth2AuthorizationRepositoryTests | Authorization persistence (6 tests) | Add, get one, get many, and the three revoke paths | Pure pass-through verification to the SQL layer; the logic lives in the service above it. | Unit | [L15]($R/Authorization/OAuth2AuthorizationRepositoryTests.cs#L15) |
| 50 | OAuth2PrincipalExtractorTests | Principal extraction from tokens (5 tests) | Success, primary-key throw with a null secondary, both keys null, both keys failing, and primary failure with secondary lookup disabled | The secondary key is a fallback only when explicitly enabled — with it disabled a primary failure returns null instead of trying the other key. | Unit | [L18]($R/Keys/OAuth2PrincipalExtractorTests.cs#L18) |
| 51 | OAuth2KeyRepositoryTests | Key-pair loading (4 tests) | Constructor population of the authorization- and resource-server primary pairs, then lazy loading of both secondary pairs | Primary pairs load eagerly and secondary pairs lazily — the rotation key is not touched unless needed. | Unit | [L13]($R/Keys/OAuth2KeyRepositoryTests.cs#L13) |
| 52 | OAuth2ResourceOwnerProxyRepositoryTests | Proxy persistence (4 tests) | Create with null/empty/whitespace client instance id, then the three read paths | Blank client instance ids are normalised to null before reaching SQL. | Unit | [L16]($R/Proxy/OAuth2ResourceOwnerProxyRepositoryTests.cs#L16) |
| 53 | ServiceAuthTokenServiceTests | Service-auth token endpoint (4 tests) | Invalid grant type, invalid assertion type, success and failure | The two shape checks run before any assertion validation, so a malformed request never reaches the validator. | Unit | [L13]($R/ServiceAuth/ServiceAuthTokenServiceTests.cs#L13) |
| 54 | OAuth2ClientRepositoryTests | Client lookup (2 tests) | An invalid and a valid client id | The repository throws on an unknown id — the null-returning behaviour tested in row 48 is added by the host above it. | Unit | [L13]($R/Clients/OAuth2ClientRepositoryTests.cs#L13) |

---

## `ZocDoc.Security.Tests/User/`

Login itself, plus the email-domain rules under `UserEmails/` that decide which addresses a practice may use. This is the densest area in the mapping: the top two classes alone hold 127 tests, and both are dominated by the Auth0 migration — the same login has to work through the legacy ASP.NET path and through Auth0's patient and provider tenants. Three classes here hit a real database rather than mocks.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 55 | UserLoginServiceTests | Every login entry point (77 tests) | Refresh-token, SMS and passwordless logins through Auth0; the legacy SMS path; newly created passwordless users; null inputs; and the password-expiration parameter | The largest class in the monolith mapping. Each Auth0 path is paired with its failure — bad user, bad token, failed validation — so the fallback behaviour is pinned as tightly as the success. | Unit | [L57]($R/UserLoginServiceTests.cs#L57) |
| 56 | LoginValidationServiceTests | Pre-login validation (50 tests) | Auth0 refresh-token validation across exception, user mismatch, invalid, blocked and MFA-blocked users; then SMS passwordless validation over null users, ASP.NET checks, scheme checks and bad tokens | Blocked and MFA-blocked are distinct outcomes from invalid, and a token/user mismatch is rejected even when both sides are individually valid. | Unit | [L38]($R/LoginValidationServiceTests.cs#L38) |
| 57 | UserRepoContextAdapterCachingFriendTests | Per-request user caching (33 tests) | Set, remove and re-set the context user including null users and null identities, then every read path over missing keys, present users and cached nulls | Reads return an option rather than null, so "not cached" and "cached as null" stay distinguishable — the distinction most of these tests exist to protect. | Unit | [L21]($R/UserRepoContextAdapterCachingFriendTests.cs#L21) |
| 58 | DomainRestrictionServiceTests | Reading practice domain restrictions (18 tests) | Standalone practices, strategic practices with restrictions one and two levels up, child practices with and without parent restrictions, then username matching | Circular strategic references throw instead of looping, and that guard is tested from both the child and the parent side. | Unit | [L22]($R/UserEmails/DomainRestrictionServiceTests.cs#L22) |
| 59 | AuthTokenValidationServiceTests | Cookie vs JWT identity selection (15 tests) | Auth0 patient and provider tenants, the cookie-promotion flag on and off, requests carrying both a cookie JWT and an aspxauth cookie, JWT-only requests, and the Plinth API case | When both credentials are present the service must pick the right one per tenant; Plinth API requests skip cookie auth entirely. | Unit | [L19]($R/AuthTokenValidationServiceTests.cs#L19) |
| 60 | DomainRestrictionWriteServiceTests | Writing domain restrictions (15 tests) | Delete at practice and strategic level with restrictions remaining or not and with mismatching domains; add for standalone, strategic and child practices | A write is refused when existing usernames would no longer match the resulting domain set — the check runs on both add and delete. | Unit | [L19]($R/UserEmails/DomainRestrictionWriteServiceTests.cs#L19) |
| 61 | PracticeEmailDomainValidationServiceTests | Existing usernames vs domains (13 tests) | Find non-matching usernames for practices and strategics across direct and MPL mismatches, then validate new usernames for MPL, non-MPL, unrestricted and non-provider users | MPL users must satisfy the overlap of every practice they belong to, so a username valid at one practice can still be rejected. | Unit | [L26]($R/UserEmails/PracticeEmailDomainValidationServiceTests.cs#L26) |
| 62 | UserPasswordServiceTests | Password change and reset (12 tests) | Change with a null user and a successful change, direct set, then reset via reset key, expired-password flow and IdP — each with validation passing and failing and the reset itself succeeding and failing | A successful password change deletes extended sessions, which is asserted rather than assumed. | Unit | [L21]($R/UserPasswordServiceTests.cs#L21) |
| 63 | UserValidationServiceTests | Who may log in (12 tests) | No role, patient, CSR with and without a Zocdoc email, practice staff, CSR holding the provider-login role, the flag-off case, back-from-churn users, unconfirmed emails, and RBAC users | CSR identity requires a Zocdoc email, not just the role; unconfirmed emails only block when both the feature and entity flags are on. | Unit | [L26]($R/UserValidationServiceTests.cs#L26) |
| 64 | LockingRedirectUtilityTests | Post-login lockout redirects (9 tests) | Null user, then the approved/locked matrix, then the OOM variant over unresolved patients and locked/unlocked results | Locked-out wins over unapproved, and an unresolvable patient throws rather than redirecting somewhere arbitrary. | Unit | [L15]($R/LockingRedirectUtilityTests.cs#L15) |
| 65 | UserEmailMappingServiceTests | Email history records (8 tests) | Record a new email and an email change, both with and without a logged-in user; mark confirmed for a normal user and a professional; read confirmed state and timestamp | Writes tolerate a null actor, which matters because self-service signup has no logged-in user. | Unit | [L17]($R/UserEmails/UserEmailMappingServiceTests.cs#L17) |
| 66 | Aspnet_Users_StoredProc_ServiceAccount_SqlTest | Service-account creation proc (5 tests) | Name validation failure, duplicate user, bogus role, then success with and without roles | Runs against a real database via `SqlTestFixture` — the stored procedure's own validation is what is under test, not the C# above it. | Integration (SQL) | [L12]($R/Aspnet_Users_StoredProc_ServiceAccount_SqlTest.cs#L12) |
| 67 | Aspnet_Users_PublicId_SqlTest | Public id column (4 tests) | New user gets a public id, ids are unique, comparison is case-sensitive, and the conversion DB function | Case sensitivity is asserted explicitly because a case-insensitive collation would silently merge distinct ids. | Integration (SQL) | [L11]($R/Aspnet_Users_PublicId_SqlTest.cs#L11) |
| 68 | UserEmailValidationServiceTests | Email domain classification (4 tests) | Disposable-domain detection and its throwing case, public-domain detection, and practice SSO domains | The three classifications are independent — an address can be public without being disposable. | Unit | [L9]($R/UserEmailValidationServiceTests.cs#L9) |
| 69 | CookieAuthRulesTests | When cookie auth is skipped (2 tests) | The flag off, and a static-content request | Thin coverage for a rule that gates authentication on every request. | Unit | [L13]($R/CookieAuthRulesTests.cs#L13) |
| 70 | DomainRestrictionSqlPersistenceTests | Domain restriction persistence (2 tests) | Delete an entity's domains, then delete the same domain twice | Re-deleting is a no-op rather than an error, verified against a real database. | Integration (SQL) | [L16]($R/UserEmails/DomainRestrictionSqlPersistenceTests.cs#L16) |
| 71 | UserCookieServiceTests | Insurance cookie on login (1 test) | Set cookies for a patient user | One test for cookie writing, all of it about the patient insurance cookie. | Unit | [L18]($R/UserCookieServiceTests.cs#L18) |

---

## `ZocDoc.Security.Tests/AspnetMembershipProvider/`

Zocdoc's replacement for the stock ASP.NET SQL membership provider, plus the password hashing under `Hashing/`. The hashing tree carries the SHA-1 → PBKDF2 migration: both algorithms are still implemented, and the interesting tests are about upgrading a hash in place during a successful login rather than about either algorithm on its own.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 72 | CustomBaseSqlMembershipProviderIntegrationTests | The membership provider end to end (72 tests) | Initialisation and connection-string failures, then create/get/validate/change-password/reset/unlock across uniqueness, trimming, unsupported parameters, hash type, missing users and lockout counters | Marked `[Category("SQL")]` through its fixture and wired with real salts, verifiers and SQL friend — the widest genuinely-integrated class in the mapping. Iteration count is lowered to 2 so it stays fast. | Integration (SQL) | [L28]($R/CustomBaseSqlMembershipProviderIntegrationTests.cs#L28) |
| 73 | Pbkdf2VerifierTests | PBKDF2 hashing and verification (23 tests) | Create a hash over null/whitespace and bad iteration counts, check embedded properties and the 16-byte salt request; then the SHA-1 backfill variant with its own salt validation; then verification | The backfill path reuses the existing SHA-1 salt instead of asking for a new one, which is asserted explicitly — regenerating it would invalidate every migrated password. | Unit | [L19]($R/Hashing/Pbkdf2/Pbkdf2VerifierTests.cs#L19) |
| 74 | CustomBaseSqlMembershipProviderUnitTests | Hash creation on write paths (6 tests) | Create user, reset password, change password with and without validation failing, validate user, and the expiration-flow idempotency check | Confirms a new hash is written on every successful credential change and none on a failed one. | Unit | [L18]($R/CustomBaseSqlMembershipProviderUnitTests.cs#L18) |
| 75 | MembershipProviderAccessorTests | Provider resolution (6 tests) | Membership and role providers, each over null, wrong type and correct type | A wrong provider type throws rather than being coerced — a misconfigured web.config fails loudly at startup. | Unit | [L12]($R/Proxies/MembershipProviderAccessorTests.cs#L12) |
| 76 | SecUtilityTests | System.Web helper shims (6 tests) | Default app name, connection string, parameter validation, the two check-parameter outcomes, and integer settings | Covers the copied-in framework helpers the provider depends on. | Unit | [L14]($R/SystemWebHelpers/SecUtilityTests.cs#L14) |
| 77 | PasswordUpgraderTests | In-place hash upgrade (4 tests) | No upgrade when rehash is not needed, no upgrade when the action is not validate-user, the upgrade itself, and a thrown exception | An upgrade failure is caught and logged, never surfaced — a login must not fail because the rehash did. | Unit | [L14]($R/Hashing/PasswordUpgraderTests.cs#L14) |
| 78 | PasswordVerifierTests | Verify-and-upgrade orchestration (4 tests) | Check password with upgrade, a throwing verify, hash creation, and logging on a create failure | Unlike the upgrader, a verify exception is logged and rethrown — verification failures must not be swallowed. | Unit | [L15]($R/Hashing/PasswordVerifierTests.cs#L15) |
| 79 | Pbkdf2HashedPasswordTests | PBKDF2 value object (3 tests) | Reject null/whitespace hashes, require a positive iteration count, and set properties | Constructor guards on the type that carries hash material. | Unit | [L10]($R/Hashing/Pbkdf2/Pbkdf2HashedPasswordTests.cs#L10) |
| 80 | SaltShakerTests | Salt generation (3 tests) | Salt is non-trivial, is not reused across calls, and the raw byte overload | Salt uniqueness is asserted rather than assumed. | Unit | [L12]($R/Hashing/SaltShakerTests.cs#L12) |
| 81 | Sha1HashedPasswordTests | Legacy SHA-1 value object (3 tests) | Reject null/whitespace hash and salt, then property assignment | Kept alive for accounts not yet migrated to PBKDF2. | Unit | [L9]($R/Hashing/Sha/Sha1HashedPasswordTests.cs#L9) |
| 82 | Sha1VerifierTests | Legacy SHA-1 verification (3 tests) | Check a password, create a hash, and a full encode/verify round trip | The round-trip test is what pins compatibility with hashes already in the database. | Unit | [L12]($R/Hashing/Sha/Sha1VerifierTests.cs#L12) |
| 83 | UserCredentialsTests | Credentials value object (3 tests) | Reject null/whitespace username and password, then property assignment | Guards the pair that flows into every verifier. | Unit | [L9]($R/Hashing/UserCredentialsTests.cs#L9) |
| 84 | MembershipInitializerTests | Provider initialisation (2 tests) | Throw with no context, and delegate to the accessor | Thin, but it is the entry point every request passes through. | Unit | [L12]($R/Proxies/MembershipInitializerTests.cs#L12) |
| 85 | Pbkdf2SettingsTests | Iteration count setting (1 test) | Read the desired iteration count | Single test on the value that determines hashing cost. | Unit | [L10]($R/Hashing/Pbkdf2/Pbkdf2SettingsTests.cs#L10) |
| 86 | ZDSqlMembershipProviderTests | Provider constructibility (1 test) | Assert a default constructor exists | ASP.NET instantiates the provider by name from config, so losing the parameterless constructor breaks startup — this is the only thing worth testing. | Unit | [L10]($R/ZDSqlMembershipProviderTests.cs#L10) |
| 87 | ZDSqlRoleProviderTests | Role provider constructibility (1 test) | Assert a default constructor exists | The role-provider counterpart of row 86. | Unit | [L8]($R/ZDSqlRoleProviderTests.cs#L8) |

---

## `ZocDoc.Security.Tests/Verification/`

Proving a user owns an email address or a phone number: Twilio-backed phone verification, email confirm keys, and the username-change requests those keys authorise. Two generations of the phone service coexist (`PhoneVerificationService` and `...V2`), and a debug-machine bypass runs through the Twilio adapter.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 88 | UserIdentityVerificationServiceTests | Password-then-phone step-up (19 tests) | Record valid and invalid password attempts, verify with validation passing and failing, then phone verification over not-found, deleted, already-verified, failed and succeeded records; then status reads | Each bad record state raises its own exception type rather than a shared failure, and inconsistent dates throw instead of being reconciled. | Unit | [L23]($R/UserIdentityVerification/UserIdentityVerificationServiceTests.cs#L23) |
| 89 | PhoneVerificationServiceTests | Sending a phone code (18 tests) | Happy path through Twilio, then Twilio and SQL throwing, a failed phone reveal, MFA without a scoped username, a locked number, a bad format, a missing provider phone, Android SMS vs call app-hash handling, and a home preferred phone | Rich failure surface for one send call. Notably a home preferred phone is overridden to the cell number, and the Android app hash is attached for SMS but not for voice. | Unit | [L30]($R/PhoneVerification/PhoneVerificationServiceTests.cs#L30) |
| 90 | TwilioVerifyPhoneVerificationServiceTests | The Twilio Verify adapter (16 tests) | Start a verification successfully, unsuccessfully and with a throw; custom parameters; the debug-machine bypass on send and verify; default vs supplied service sid; and the test-patient path | The debug-machine and test-patient bypasses are tested as first-class behaviour — they short-circuit Twilio entirely, including returning not-verified for a wrong code. | Unit | [L19]($R/TwilioVerifyPhoneVerificationServiceTests.cs#L19) |
| 91 | UsernameConfirmKeyServiceTests | Email confirm keys (13 tests) | Read mappings with and without a key, list change and verify requests, mark used, make a request, and build the password-reset and self-signup confirm URLs | URL construction is role-dependent and throws for anyone who is neither a provider nor a self-signed-up user. | Unit | [L27]($R/UsernameConfirmKeyServiceTests.cs#L27) |
| 92 | UsernameChangeRequestServiceTests | Initiating a username change (7 tests) | Provider and patient initiation each with a wrong-user-type throw, then resend over no existing key and a new username | Provider and patient flows are separate methods with separate type guards; a resend with no key returns false rather than creating one. | Unit | [L27]($R/UsernameChangeRequestServiceTests.cs#L27) |
| 93 | PatientEmailVerificationServiceTests | Patient email verification (6 tests) | Confirm key not found, patient mismatch, expired key, already verified, success, and the outbound email | Each outcome is a distinct result value rather than a boolean, so the caller can tell "expired" from "wrong patient". | Unit | [L25]($R/PatientEmailVerificationServiceTests.cs#L25) |
| 94 | PhoneVerificationServiceV2Tests | V2 anonymous-user send (5 tests) | Success, general failures, invalid number, number already in use, and a locked number | V2 exists for the anonymous pre-account flow; "phone number in use" is a V2-only outcome. | Unit | [L19]($R/PhoneVerification/PhoneVerificationServiceV2Tests.cs#L19) |
| 95 | PhoneNumberVerificationSqlPersistenceTests | Verification-attempt persistence (4 tests) | Register a verification with and without existing rows, then record an unverified and a verified attempt | Registering deletes prior rows for the entity, and only a verified result stamps the completion date. Runs against a real database. | Integration (SQL) | [L19]($R/PhoneVerification/PhoneNumberVerificationSqlPersistenceTests.cs#L19) |
| 96 | ProviderVerifyNudgeServiceTests | Verification nudge rollout (3 tests) | The redirect URL, whether to redirect, and the last-digit-of-user-id bucketing | Rollout is bucketed on the trailing digit of the user id rather than an AB framework. | Unit | [L16]($R/ProviderVerifyNudgeServiceTests.cs#L16) |
| 97 | E164FormatPhoneNumberTests | Phone number parsing (2 tests) | Well-formed numbers, then invalid ones | Invalid numbers throw at construction, so nothing downstream handles a malformed number. | Unit | [L8]($R/E164FormatPhoneNumberTests.cs#L8) |
| 98 | PhoneVerificationServiceV2WithPatientCreationFlowMetricsTests | V2 with creation-flow metrics (1 test) | One success case through the metrics-wrapped decorator | A single smoke test over the metrics wrapper; the behaviour itself is covered by row 94. | Unit | [L18]($R/PhoneVerification/PhoneVerificationServiceV2WithPatientCreationFlowMetricsTests.cs#L18) |

---

## `ZocDoc.Security.Tests/JWT/`

The monolith's own JWT, in two versions living side by side: v1 at the root and v2 under `v2/`. Validation accepts both; generation only produces v2. The claim set is the interesting part — roles are stored as an integer array and the subject is the user's public id, both of which are asserted precisely because they are a wire contract with every service that reads a Zocdoc JWT.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 99 | JwtV2ClaimsServiceTests | Claim assembly (40 tests) | New jti, timeout, then practice RBAC roles across no roles, bogus roles, non-practice roles and real practice roles — each for an explicit user and for the current user — plus the provider-can-login role behind its flag | Every role lookup is duplicated for the explicit-user and current-user entry points, which is where most of the 40 tests go. Bogus and non-practice roles return null rather than an empty list. | Unit | [L23]($R/v2/JwtV2ClaimsServiceTests.cs#L23) |
| 100 | JwtV2GenerationServiceTests | Token generation (35 tests) | Null-user throws on both entry points, DataDog claims, token format, functional claims, subject, roles with none/one/many, the integer-array encoding, and patient id present and absent | The subject is the public id, not the numeric user key, and role values are integers — these two assertions are the contract every consuming service depends on. | Unit | [L30]($R/v2/JwtV2GenerationServiceTests.cs#L30) |
| 101 | JwtValidationServiceTests | Token validation (10 tests) | Bad format, bad signature, missing public key, expiry, wrong issuer, wrong audience, missing user, missing subject, then valid v1 and valid v2 tokens | Both versions validate through the same service — the v1 case is what keeps already-issued tokens working. | Unit | [L16]($R/JwtValidationServiceTests.cs#L16) |
| 102 | JwtAuthenticationServiceTests | The authorization filter (7 tests) | Invalid request, no token, invalid token, a valid v2 token, missing sub, missing user, and a sanity check on the validation result | The filter's job is to set the right response and nothing else — a valid token must leave the response untouched, which is asserted directly. | Unit | [L25]($R/JwtAuthenticationServiceTests.cs#L25) |
| 103 | JwtV2CookieServiceTests | JWT cookie lifecycle (7 tests) | Delete for logged-out users, set for authenticated users, then the aspxauth-derived path over a null ticket, null user, logged out, expired ticket and success | The cookie is derived from the existing aspxauth ticket during the migration; a null ticket logs an error rather than throwing. | Unit | [L16]($R/v2/JwtV2CookieServiceTests.cs#L16) |
| 104 | JwtRequestValidationServiceTests | Where the token comes from (6 tests) | Missing authorization, cookie-only with the flag on, both header and cookie present, malformed header, header token, and a missing subject | The header wins when both a header and a cookie are present — the precedence rule for the cookie-promotion rollout. | Unit | [L15]($R/JwtRequestValidationServiceTests.cs#L15) |
| 105 | JwtUserMapperTests | User → claim data lookups (4 tests) | Patient lookup by user key with a throwing case, then practice lookup including a null provider | A failed patient lookup logs and returns rather than throwing, so a data gap does not block token issuance. | Unit | [L18]($R/v2/JwtUserMapperTests.cs#L18) |
| 106 | CookieWriterTests | Cookie write/delete (2 tests) | Write cookies, then delete them | Thin wrapper coverage under the service in row 103. | Unit | [L17]($R/v2/CookieWriterTests.cs#L17) |
| 107 | JwtProviderDetectorTests | Practice resolution for JWTs (1 test) | A multi-provider user who is not eligible | One test, covering only the ineligible multi-provider case. | Unit | [L13]($R/JwtProviderDetectorTests.cs#L13) |
| 108 | JwtRoleIdsTests | Role id uniqueness (1 test) | Assert every role id is distinct | A one-line guard with outsized value: a duplicated id would silently grant the wrong role to every token holder. | Unit | [L10]($R/v2/JwtRoleIdsTests.cs#L10) |

---

## `ZocDoc.Security.Tests/AuthOOM/`

The reconciliation layer that keeps the monolith's user tables in step with the out-of-monolith identity stores — Auth0, `auth-service`, and the OOM user APIs. Every class here is a background sync rather than a request path, so the recurring assertion is that a failure is logged and the batch continues instead of aborting.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 109 | AuthIdentityReconciliatorServiceTests | Identity reconciliation driver (12 tests) | Reconcile end to end, chunking, skipping bad emails, iterator get/set, the two id-selection queries, then user-data and provider-username sync including a missing monolith identity and an unexpected exception | Bad emails are skipped rather than failing the run, and both sync failures log instead of throwing — the loop is designed to make partial progress. | Unit | [L24]($R/AuthIdentityReconciliatorServiceTests.cs#L24) |
| 110 | ProviderUserReconcilatorServiceTests | Provider-user deletion queue (10 tests) | Queue for deletion with a success and an exception, batch insert and delete usernames, queue reads with zero and non-zero batch sizes, item removal, and OOM delete over failure, single-item and multi-item queues | A zero batch size skips SQL entirely, and a multi-item queue only calls delete for the valid users while still recording the metric. Deletion failure records a metric and rethrows — unlike the other syncs here. | Unit | [L22]($R/ProviderUserReconcilatorServiceTests.cs#L22) |
| 111 | Auth0ReconciliatorServiceTests | Auth0 user creation (5 tests) | Create with and without a phone, create where the phone already exists, then set-phone with a value and with null | An existing phone triggers unlink-then-relink rather than an error — the collision case Auth0 forces on the migration. | Unit | [L15]($R/Auth0ReconciliatorServiceTests.cs#L15) |
| 112 | PracticeUserAuthProfileServiceTests | Auth profile assembly (5 tests) | Missing practice staff, a valid user, UA-free role mapping to JWT role ids, and boolean and nullable field variants | Missing practice staff throws `KeyNotFoundException`; the role-id mapping is the same contract asserted in row 108. | Unit | [L26]($R/PracticeUserAuthProfileServiceTests.cs#L26) |
| 113 | AuthServiceReconciliatorServiceTests | `auth-service` reconciliation (4 tests) | Reconcile, chunking, the update call, and provider usernames | The `auth-service` counterpart of row 109, sharing its chunked shape. | Unit | [L24]($R/AuthServiceReconciliatorServiceTests.cs#L24) |
| 114 | AuthServiceProviderUserQueueSqlTests | Queue persistence (3 tests) | Insert, remove and read queue items | Runs against a real database through `SqlPersistenceTestFixture`. | Integration (SQL) | [L13]($R/AuthServiceProviderUserQueueSqlTests.cs#L13) |
| 115 | PracticeUserAgreementReconciliatorServiceTests | User-agreement sync (3 tests) | Success, a logged exception returning an empty list, and chunked processing | On failure it returns an empty list rather than a partial one, so the caller cannot mistake an error for "nothing to sync" only by count. | Unit | [L22]($R/PracticeUserAgreementReconciliatorServiceTests.cs#L22) |
| 116 | MfaReconciliatorServiceTests | MFA state sync (2 tests) | Success, and a failure that logs | Minimal coverage for keeping MFA enrolment consistent across stores. | Unit | [L19]($R/MfaReconciliatorServiceTests.cs#L19) |
| 117 | MonolithIdentityUtilityTests | Deleted-identity predicate (1 test) | The considered-deleted check | One test on the rule that decides whether an identity is skipped by every reconciliator above. | Unit | [L10]($R/MonolithIdentityUtilityTests.cs#L10) |

---

## `ZocDoc.Security.Tests/Password/`

Password reset and expiry. The three largest classes are all facets of one flow — request a reset, validate the request, and audit what was decided — and each enumerates the same user states (unknown, locked patient, unapproved, inactive) so the three layers agree. The Cognito/IdP branch runs through the same request path, adding a create-user fallback when the account is missing from the identity provider.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 118 | PasswordResetServiceTests | Requesting a reset (51 tests) | Invalid email, unknown user, locked patient, valid patient with and without a redirect url, then the IdP-enabled branch over present-in-Cognito, missing-with-create-succeeding, missing-with-create-failing, create-then-reset-failing, and non-patient users | An unknown user still receives an email — a deliberate anti-enumeration choice, and one of the few places a "failure" produces outbound mail. The Cognito-missing branch has four distinct outcomes. | Unit | [L39]($R/PasswordResetServiceTests.cs#L39) |
| 119 | PasswordResetValidationServiceTests | Reset eligibility (40 tests) | User not found, not approved, invalid password, valid password with user validation succeeding and failing, and a locked patient — the whole set repeated for the reset and the request-reset entry points | The two entry points are validated separately against the same state matrix, which is where the count comes from. | Unit | [L17]($R/PasswordResetValidationServiceTests.cs#L17) |
| 120 | PasswordResetValidationAuditServiceTests | Auditing reset decisions (26 tests) | The flag off, then every username state — valid, locked patient, inactive account, unknown, unapproved — crossed with validation succeeding and failing, for both the request and the guid-based reset | The audit is behind its own flag and mirrors the row 119 matrix; the flag-off tests assert nothing is written at all. | Unit | [L15]($R/PasswordResetValidationAuditServiceTests.cs#L15) |
| 121 | PasswordExpiredServiceTest | Forced password expiry (10 tests) | Expire, expire by guid, unexpire, detect expired and unexpired, the page whitelist for expired users, the general page block, and the entity-flag-plus-past-expiration conditions | An expired user can reach only the whitelisted reset pages; expiry is gated on an entity flag and only applies to providers. | Unit | [L24]($R/PasswordExpired/PasswordExpiredServiceTest.cs#L24) |
| 122 | PasswordUtilityTests | Password rules (8 tests) | Regular validation without history, a null username under stricter requirements, previously-used passwords with the flag on and history checks requested or not, the blacklist, generation, character-class counting and scoring | History checking is opt-in per call even when the flag is on, so a caller can validate strength without a history lookup. | Unit | [L17]($R/PasswordUtilityTests.cs#L17) |
| 123 | PasswordResetKeyServiceTests | Reset keys and URLs (7 tests) | Look up the user for a key, mark used, build a URL on a normal host, a debug machine and a Pulse domain, then the validated variant with validation failing and succeeding | The URL host is environment-dependent — debug machines get localhost and Pulse keeps the current domain, so a reset link never points at the wrong environment. | Unit | [L21]($R/PasswordResetKeyServiceTests.cs#L21) |
| 124 | PasswordExpiredRepositoryTest | Expiry repository (4 tests) | Expire, unexpire, and the two detection cases | Pass-through verification under row 121. | Unit | [L9]($R/PasswordExpired/PasswordExpiredRepositoryTest.cs#L9) |
| 125 | PasswordExpiredPersistenceTest | Expiry persistence (2 tests) | Expire a password, then unexpire one that is not expired | Runs against a real database; unexpiring an already-active password is a no-op. | Integration (SQL) | [L9]($R/PasswordExpired/PasswordExpiredSqlPersistenceTest.cs#L9) |
| 126 | PasswordResetKeySqlPersistenceTests | Reset key persistence (1 test) | Insert and read back | Single database-backed check on the table behind row 123. | Integration (SQL) | [L14]($R/PasswordResetKeySqlPersistenceTests.cs#L14) |

---

## `ZocDoc.Security.Tests/Provider/`

Provider-side account security, dominated by the MFA rollout: enabling MFA on a practice or strategic, the grace period before it is enforced, the phone-registration redirect that grace period drives, and a nightly audit that re-derives the expected state and logs every discrepancy. The strategic hierarchy is the hard part — a child practice cannot be left disabled under an enabled parent.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 127 | PracticeMfaServiceTests | Enabling and disabling MFA (37 tests) | Set for a strategic over missing id, already set, enable and disable; set for an entity over invalid input and each practice/strategic on-off combination; already-enabled children during a strategic enable; and disable blocked by an enabled parent strategic | Enabling a strategic skips practices already enabled, and disabling one fails while its parent is still enabled — the hierarchy invariant is enforced on the write path, not just audited. | Unit | [L34]($R/PracticeMfaServiceTests.cs#L34) |
| 128 | PracticeUsersServiceTests | Listing practice users (18 tests) | Practice staff and all users, each over no users, no MPL users, no direct users, both kinds together, churned excluded, and deleted MPL users | Direct and MPL users come from different sources and must merge without duplication; churn and deletion filter differently. | Unit | [L22]($R/PracticeUsersServiceTests.cs#L22) |
| 129 | ProviderMfaReconciliatorServiceTests | Nightly MFA audit (10 tests) | No enabled entities, correct and incorrect auth schemes, grace-period users with correct and incorrect activation dates, a valid strategic hierarchy, entities added to a strategic later, a disabled strategic under an enabled parent, a disabled practice under an enabled strategic, and a provider activating after its practice | The audit logs exceptions rather than repairing state, and it checks the same hierarchy rules row 127 enforces — so drift introduced outside the service is still caught. | Unit | [L24]($R/ProviderMfaReconciliatorServiceTests.cs#L24) |
| 130 | ProviderMfaActivationRepositoryTests | Activation-date persistence (6 tests) | Insert, delete, and the four read paths | Pass-through verification for the dates the audit and grace period both read. | Unit | [L14]($R/ProviderMfaActivation/ProviderMfaActivationRepositoryTests.cs#L14) |
| 131 | ProviderPhoneRegistrationFlowServiceTests | Phone-registration redirect (6 tests) | CSR users, staff off the grace period, staff on it with and without a phone, then return-url handling for null/empty/non-slash and valid values | Only a grace-period user without a phone is redirected; return urls that do not start with a slash are dropped, which is an open-redirect guard. | Unit | [L18]($R/ProviderMfaActivation/ProviderPhoneRegistrationFlowServiceTests.cs#L18) |
| 132 | PracticeMfaNotificationServiceTests | MFA rollout emails (5 tests) | Enable notification to all users, the add-a-phone reminder to users without one, then missing user key, missing email and missing first name | Per-user data gaps do not stop the batch — the other emails still go out. | Unit | [L29]($R/PracticeMfaNotificationServiceTests.cs#L29) |
| 133 | PracticeUserRbacRolesServiceTests | RBAC role translation (5 tests) | ASP.NET roles from practice-staff roles for one and many items, roles for a given user and the current user, and the conversion helper | The bridge between the legacy ASP.NET role names and the RBAC model the JWT carries. | Unit | [L15]($R/Rbac/PracticeUserRbacRolesServiceTests.cs#L15) |
| 134 | PracticeUsersMfaServiceTests | Users holding MFA records (2 tests) | With existing users, and with none | Thin coverage of the query that feeds the notification batch in row 132. | Unit | [L16]($R/PracticeUsersMfaServiceTests.cs#L16) |

---

## `ZocDoc.Security.Tests/MultiProvider/`

Multi-practice login (MPL) — one user account mapped to several practices. Only seven classes, but the top two hold 106 tests between them because every mapping change has to satisfy four independent constraints at once: eligibility, the mapping limit, email-domain restrictions, and the MFA state of every practice involved.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 135 | MultiProviderServiceTests | Changing practice mappings (72 tests) | Actor cannot manage the account, target not enabled, target not eligible, adding mappings, MFA violations, MFA turned on for the user, a missing default provider, deletions, MFA kept on because another practice requires it, MFA turned off because none do, and combined add/remove | The MFA side-effect is the subtlety: removing a practice can turn a user's MFA off, but only if no remaining practice requires it — asserted from both directions. | Unit | [L39]($R/MultiProviderServiceTests.cs#L39) |
| 136 | MultiProviderSecurityServiceTests | Pre-validating mapping changes (34 tests) | Eligibility pass-through, then no mappings, duplicates, over the limit, a churned practice, a username violating domain restrictions, MFA violations, and the strategic-user cases — non-strategic providers, same strategic, different strategics under one top level, and different top-level strategics | A strategic user may span practices only within one top-level strategic; each rejection returns its own result type rather than a shared failure. | Unit | [L33]($R/MultiProviderSecurityServiceTests.cs#L33) |
| 137 | MultiProviderUserRulesServiceTest | Eligibility rules (7 tests) | Get-user throwing, get-user returning null, a non-professional, practice staff, then the can-log-in and can-view checks including a user who cannot manage | A thrown lookup and a null user both resolve to unknown-user rather than propagating. | Unit | [L18]($R/MultiProviderUserRulesServiceTest.cs#L18) |
| 138 | CurrentPracticeCookieServiceTests | Current-practice cookie (4 tests) | Null user, null practice, practice id zero, and a real practice id | Three separate "no practice" shapes all clear the cookie rather than writing an ambiguous value. | Unit | [L18]($R/CurrentPracticeCookieServiceTests.cs#L18) |
| 139 | MultiProviderAccountAuditResultTests | Audit result validity (4 tests) | Ineligible, not enabled, invalid mappings, and all three good | The result object only reports valid when every condition holds. | Unit | [L10]($R/MultiProviderAccountAuditResultTests.cs#L10) |
| 140 | MultiProviderAlerterServiceTests | Cross-practice alerter cleanup (3 tests) | No location preferences, valid ones, and invalid ones | Removing a practice mapping must also drop alerter locations the user can no longer see. | Unit | [L17]($R/MultiProviderAlerterServiceTests.cs#L17) |
| 141 | MultiProviderRepositoryTests | MPL enable/disable persistence (3 tests) | Enable, disable, and the reverse lookup by provider | Enabling also sets the current provider; disabling removes every mapping. | Unit | [L15]($R/MultiProviderRepositoryTests.cs#L15) |

---

## `ZocDoc.Security.Tests/Roles/`

Role bundles — named groups of ASP.NET roles assigned to internal users — and the change log that records every grant and revoke. The intersection tests are the reason this area exists as its own concern: removing a user from one bundle must not strip roles they still hold through another.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 142 | RoleChangeLoggingServiceTests | Role change audit log (14 tests) | Role added and removed for a user, roles added and removed from a bundle, users added and removed from a bundle, the non-internal-user and patient-role exclusions, no logged-in actor, and reading changes between dates | Patient-role changes are deliberately not logged — a signal-to-noise decision — and logging throws when there is no actor rather than recording an anonymous change. | Unit | [L24]($R/Roles/Logging/RoleChangeLoggingServiceTests.cs#L24) |
| 143 | RoleBundleRepositoryTests | Bundle persistence (10 tests) | Reject an invalid role name, create a bundle, then add and remove users and roles — each mutation paired with an assertion that it was logged | Every mutation is checked twice: that it reached SQL and that it produced an audit entry. | Unit | [L15]($R/Roles/RoleBundleRepositoryTests.cs#L15) |
| 144 | RoleBundleRepositoryIntersectionTests | Overlapping bundles (4 tests) | Remove a user from a bundle, remove a role from a bundle, remove several users, and delete a bundle — each with the roles also granted via another bundle | The whole class asserts one invariant from four angles: a removal never revokes a role the user still holds elsewhere. | Unit | [L17]($R/Roles/RoleBundleRepositoryIntersectionTests.cs#L17) |
| 145 | Roles_RenameRole_prc | Role rename stored proc (2 tests) | Rename a role, and confirm only one row changes | Database-backed; the single-row assertion is the guard against an unscoped UPDATE. | Integration (SQL) | [L12]($R/Roles/Roles_RenameRole_prc.cs#L12) |
| 146 | RoleNameTests | Role name constants (1 test) | Assert the organization-management role names have exact values with no leading space | A change detector for strings compared by exact match — a stray space would silently deny access. | Unit | [L7]($R/Roles/RoleNameTests.cs#L7) |

---

## `ZocDoc.Security.Tests/Auth0/`

The Auth0 management API client and the token that authorises it. Small area, but row 148 is the most concurrency-sensitive class in the mapping.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 147 | Auth0ApiClientTests | Auth0 management calls (30 tests) | Get user info with and without a JWT, then create passwordless email and SMS users, link and unlink SMS users, delete a user and the remaining management calls — each with a success and a failure case | Systematically paired success/failure coverage; the failure half is what pins how Auth0 errors surface to callers. | Unit | [L24]($R/Auth0/Auth0ApiClientTests.cs#L24) |
| 148 | Auth0AdministrationTokenCacheTests | Management token caching (8 tests) | First fetch, sequential cached calls, then parallel calls against a null token, an expired token and a refreshable token; renewal at 83% of lifetime; a fetch failure with a still-valid token; and a failure with no good token | Under parallel callers exactly one does the work while the others wait — asserted for three different token states. A fetch failure returns the existing good token and only throws when there is none. | Unit | [L17]($R/Auth0/Auth0AdministrationTokenCacheTests.cs#L17) |
| 149 | Auth0AdministrationTokenFetcherTests | Token fetch (2 tests) | Success and failure | The network call under row 148, kept deliberately thin. | Unit | [L23]($R/Auth0/Auth0AdministrationTokenFetcherTests.cs#L23) |
| 150 | Auth0ExceptionParserTests | Auth0 error parsing (2 tests) | An SMS provider error and a bad phone number | Only two Auth0 error shapes are recognised specifically; everything else falls through to generic handling. | Unit | [L10]($R/Auth0/Auth0ExceptionParserTests.cs#L10) |

---

## `ZocDoc.Security.Tests/Authentication/`

The request-time authentication pipeline: which scheme handles a request, whether the auth attribute can be short-circuited, and the MFA-aware password and phone authentication that sits behind the OAuth2 token endpoint.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 151 | MultiFactorAuthenticationServiceTests | MFA authentication (21 tests) | Password authentication over malformed username, malformed password, unknown account, locked and unapproved non-MFA users; then phone authentication over malformed username, verification id and code, unknown account, non-patient/provider users and non-MFA users | Every rejection is a distinct typed error rather than a boolean, so the caller can distinguish a malformed input from a locked account — the errors themselves are the contract. | Unit | [L29]($R/Authentication/MultiFactorAuthenticationServiceTests.cs#L29) |
| 152 | JwtAuthenticationSchemeTests | JWT scheme handler (8 tests) | Invalid request, no token, invalid token, an invalid token on a Plinth API route, a valid v2 token, missing sub, missing user, and a validation-result sanity check | Nearly a mirror of row 102 with one addition — Plinth API routes get a different response shape for the same failure. | Unit | [L27]($R/Authentication/AuthenticationScheme/JwtAuthenticationSchemeTests.cs#L27) |
| 153 | RequireAuthenticationServiceTest | Scheme selection (7 tests) | A single scheme, Auth0, OAuth failing while JWT passes, token plus cookie, the unauthorized result shape, the Plinth API unauthorized shape, and an anonymous request with no auth | Schemes are tried in order and any one succeeding is enough — the OAuth-fails-JWT-passes case is the one that proves it. | Unit | [L17]($R/Authentication/RequireAuthenticationServiceTest.cs#L17) |
| 154 | AuthAttributeShortCircuitServiceTests | Auth attribute bypass (5 tests) | No identity, no user, then Auth0, mobile OAuth and monolith JWT identities | No identity and no user both return false, so the bypass can only be reached by an already-authenticated caller. | Unit | [L11]($R/Authentication/AuthenticationScheme/AuthAttributeShortCircuitServiceTests.cs#L11) |

---

## `ZocDoc.Security.Tests/Auth/`

The legacy forms sign-in the provider site still uses. Small, but it holds the CSR trusted-IP rule and the churned-practice block — two checks that gate real access and appear nowhere else.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 155 | SignInTests | Sign-in outcomes (17 tests) | Patient sign-in with good credentials, a bad password and a bad email; CSR and CSR-sales from a trusted IP; an unsafe role on a debug machine; unapproved and locked-out users; then active doctors, active resources and new-application doctors | Enumerates the account states that may and may not sign in. CSR roles require a trusted IP, and the unsafe-role case is allowed only on a debug machine. | Unit | [L38]($R/Auth/SignInTests.cs#L38) |
| 156 | AuthFormUtilityTests | The sign-in form path (11 tests) | Valid and invalid credentials, invalid user, a CSR-domain email without the CSR role for a normal user and for a valid professional, CSR domain with the role, the same with a failing audit, a churned practice, and live doctor and practice-staff successes | A Zocdoc-domain email without the CSR role is explicitly not treated as CSR, and a failed audit blocks the sign-in even when credentials and role are correct. | Unit | [L21]($R/Auth/AuthFormUtilityTests.cs#L21) |
| 157 | AuthFormStateProviderTests | Request environment (3 tests) | Debug-machine detection, host address, and current url domain | Supplies the three environment values the trusted-IP and debug-machine rules above depend on. | Unit | [L19]($R/Auth/AuthFormStateProviderTests.cs#L19) |

---

## `ZocDoc.Security.Tests/Encryption/`

Hash helper wrappers. Four tests total — the thinnest area in the mapping, and the only justification is that these are pure functions over framework primitives.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 158 | SHA256HelperTests | SHA-256 formatting (2 tests) | Hex and base64 output | Only output formatting is covered, not the hash itself. | Unit | [L8]($R/Encryption/SHA256HelperTests.cs#L8) |
| 159 | MD5HelperTests | MD5 formatting (1 test) | Hex output | MD5 is still present in the codebase; the test says nothing about where it is used. | Unit | [L8]($R/Encryption/MD5HelperTests.cs#L8) |
| 160 | SHA512HelperTests | SHA-512 formatting (1 test) | Hex output | Counterpart to row 158 with no base64 case. | Unit | [L8]($R/Encryption/SHA512HelperTests.cs#L8) |

---

## `ZocDoc.Security.Tests/ExtendedSession/`

"Remember me" sessions that outlive the forms ticket. Sixty tests across three classes, most of them in the cookie/ticket plumbing rather than the session model — the ticket is read from either the request or the response depending on where in the pipeline the caller sits, and getting that wrong is the failure this area guards against.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 161 | ExtendedSessionServiceTests | Session lifecycle (37 tests) | Create, delete, delete-by, expiration lookup, the active-session check with and without a ticket parameter in both outcomes, then the implementation paths including using the response cookie and a null ticket | Creation reads the response cookie rather than the request cookie, because the ticket is written earlier in the same request; a null ticket inserts nothing instead of a partial row. | Unit | [L23]($R/ExtendedSession/ExtendedSessionServiceTests.cs#L23) |
| 162 | ExtendedSessionTicketHelperTests | Ticket and cookie handling (19 tests) | Add the identifier to user data, replace the existing forms cookie, persistent and non-persistent expiry, missing ticket and identifier cases, and reading the ticket from request, response, an invalid source and a context with no cookie | An invalid ticket source throws rather than defaulting to the request — the ambiguity is treated as a programming error. | Unit | [L21]($R/ExtendedSession/ExtendedSessionTicketHelperTests.cs#L21) |
| 163 | ExtendedSessionDtoTests | Instant conversions (4 tests) | Get and set for the created and expires instants | Covers the NodaTime conversion on the persisted session row. | Unit | [L9]($R/ExtendedSession/ExtendedSessionDtoTests.cs#L9) |

---

## `ZocDoc.Security.Tests/Monitoring/`

Metric recorders that emit account-state gauges on a schedule. Six tests across three classes — the coverage is proportional to the risk, since a wrong metric misleads rather than breaks.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 164 | ZdMembershipRecorderTests | Membership metrics (3 tests) | Record all statuses, then orphaned-provider-user detection with the flag off and with detection but no reconciliation | Detection and reconciliation are separately switchable, so the orphan sweep can run in observe-only mode. | Unit | [L19]($R/Monitoring/ZdMembershipRecorderTests.cs#L19) |
| 165 | ProfessionalStatusRecorderTests | Professional status metrics (2 tests) | All known statuses, then unaccounted-for ones | Unknown statuses are counted rather than dropped, so a new status value shows up in the metric instead of vanishing. | Unit | [L14]($R/Monitoring/ProfessionalStatusRecorderTests.cs#L14) |
| 166 | AuthEntityMonitoringTests | Auth entity metrics (1 test) | One end-to-end recording pass | Smoke coverage only. | Unit | [L11]($R/Monitoring/AuthEntityMonitoringTests.cs#L11) |

---

## `ZocDoc.Security.Tests/UserAccountActivityEvent/`

The account activity log — login successes and failures, password resets, MFA validation and logouts. Row 167 holds nearly all of it because each event type is asserted with and without metadata and in both outcomes.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 167 | UserAccountActivityLoggingServiceTests | Activity event shapes (38 tests) | Login success and failure with and without metadata, reset-password request and result in both outcomes, MFA password validation success and failure, logout, and the remaining event types | Each event's full payload is asserted, not just that something was logged — this log is what account-security investigations read. | Unit | [L31]($R/UserAccountActivityEvent/UserAccountActivityLoggingServiceTests.cs#L31) |
| 168 | UserAccountActivityEventServiceTests | Batch reads (2 tests) | An empty id list, and a populated one | An empty list short-circuits without a query. | Unit | [L12]($R/UserAccountActivityEvent/UserAccountActivityEventServiceTests.cs#L12) |
| 169 | UserAccountActivityEventWriteServiceTests | Event write (1 test) | Save one event | Thin coverage on the write path behind row 167. | Unit | [L9]($R/UserAccountActivityEvent/UserAccountActivityEventWriteServiceTests.cs#L9) |

---

## `ZocDoc.Security.Tests/AuthBackdoor/`

The test-account backdoor — the mechanism automated tests and internal tooling use to create and link patients without going through the real signup flow. Both classes spend most of their tests on the authorization around it rather than the creation itself, which is the right emphasis for a bypass.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 170 | AuthBackdoorServiceTests | Backdoor operations (6 tests) | Set an Auth0 user id and link, each with a success and an unauthorized case; then create a patient, including the booking-restriction bypass | Every operation has an explicit unauthorized test — the bypass is only reachable with the right caller. | Unit | [L24]($R/AuthBackdoor/AuthBackdoorServiceTests.cs#L24) |
| 171 | AuthBackdoorSyncSqlTests | Backdoor persistence (5 tests) | Create a new patient, create one with null optional fields, link a new patient, link an existing one, and link the same patient twice | Database-backed. Linking twice returns null rather than creating a duplicate mapping. | Integration (SQL) | [L17]($R/AuthBackdoor/AuthBackdoorSyncSqlTests.cs#L17) |

---

## `ZocDoc.Security.Tests/Patient/`

One class, covering scoped auth — the limited identity a patient gets from a booking confirmation link or a verification token instead of a full login.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 172 | ScopedAuthLoginServiceTests | Scoped identity precedence (13 tests) | Set each of provider-confirm-id, request-id and verification-token on its own, then each one after each of the other two; then read the identity with none set and with each source present | Nine of the thirteen tests are ordering permutations — which scope wins when two are set is the whole point of the class, and it is pinned exhaustively rather than by rule. | Unit | [L15]($R/Patient/ScopedAuthLoginServiceTests.cs#L15) |

---

## `ZocDoc.Security.Tests/SmsAuthentication/`

One class, but 35 tests: deciding whether a patient may use SMS as a login factor and what masked number to show them.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 173 | SmsAuthenticationServiceTests | SMS eligibility and masking (35 tests) | Null, unapproved and locked users; no patient; multiple, missing, badly formatted and fake phone numbers; one locked number among several; then Auth0 validation failing, throwing and passing | Fails closed on every ambiguity — multiple phone numbers on file makes a user ineligible rather than picking one, and an Auth0 exception is treated as a failed validation. | Unit | [L32]($R/SmsAuthentication/SmsAuthenticationServiceTests.cs#L32) |

---

## `ZocDoc.Security.Tests/UserAuthenticationScheme/`

One class over the table that records which authentication scheme each user is on, and when MFA was activated for them — the data the MFA audit in row 129 and the grace period in row 131 both read.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 174 | UserAuthenticationSchemeRepositoryTests | Scheme and MFA-date reads (9 tests) | Three no-op cases for record, batch record and current-scheme reads; activation-date lookups singly and batched; registration history for a missing user and one with scheme changes; batch MFA-enabled; and all practice users with MFA | Three methods are asserted to be no-ops, which is deliberate — the writes moved out of the monolith and the stubs remain so callers keep compiling. | Unit | [L17]($R/UserAuthenticationScheme/UserAuthenticationSchemeRepositoryTests.cs#L17) |

---

## `PracticeAuthorization.Test/` (root)

The second project: practice-level authorization. The root holds the pre-FGA model — RBAC role reads, CSR role spoofing, and primary-practice selection.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 175 | RbacSpoofableRolesServiceTests | CSR role spoofing (22 tests) | Spoofing on and possible, spoofed roles returned for a given user and the current user, then real roles returned when the feature is disabled, the actor is not CSR, the request is not on Pulse, or spoofing is off | Four independent conditions must all hold before a spoof takes effect, and each is tested through both the given-user and current-user entry points — that pairing is where the 22 tests come from. | Unit | [L26]($P/RbacSpoofableRolesServiceTests.cs#L26) |
| 176 | PracticeAuthorizationServiceTests | Primary-practice suggestion (13 tests) | Suggest from hierarchy and from an explicit list, each over no other practice, only the current one, all inactive, and several available; then the allowable-practices list over the same states plus a partially-inactive set | The oldest active practice wins, and inactive practices are excluded everywhere rather than ranked last. | Unit | [L18]($P/PracticeAuthorizationServiceTests.cs#L18) |
| 177 | PupClientRoleConverterTests | Role type conversion (4 tests) | Convert each direction, plus an exhaustive no-throw pass over every value of both enums | The exhaustive passes are the valuable part: adding a role to either enum without updating the converter fails here rather than at runtime. | Unit | [L9]($P/PupClientRoleConverterTests.cs#L9) |
| 178 | PracticeStaffPermissionServiceTests | Permission reads (3 tests) | Staff permissions, practice permissions, and practice permissions with FGA enabled | The FGA case is asserted to return the same permissions as the legacy path — the equivalence the migration depends on. | Unit | [L18]($P/PracticeStaffPermissionServiceTests.cs#L18) |
| 179 | PracticeStaffMappingServiceTests | Primary practice update (1 test) | Update and verify the calls | Thin pass-through coverage. | Unit | [L15]($P/PracticeStaffMappingServiceTests.cs#L15) |

---

## `PracticeAuthorization.Test/Fga/`

The FGA migration. Four classes, 77 tests, and the shape is a proxy to the external authorization service plus a per-endpoint config that decides whether each endpoint runs legacy, shadow or FGA. Row 182 is the most operationally important class in this project — it governs the rollout switch itself.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 180 | PracticeAuthorizationProxyServiceTests | The FGA proxy service (42 tests) | Practice checks over a null user, a non-practice user, a null practice, empty permissions and a real call; organization checks over empty permissions, an empty organization id, a null user and a non-practice user; then the batch variants over empty permissions and empty ids | The two entry points fail differently by design: practice checks return false on bad input while organization and batch checks throw. A caller that ignores the distinction gets an unexpected allow or an unexpected exception. | Unit | [L30]($P/Fga/PracticeAuthorizationProxyServiceTests.cs#L30) |
| 181 | PracticeAuthorizationProxyApiCallerTests | The HTTP caller (29 tests) | Practice and organization checks over success, 401, 403 and 400; then batching over a single batch, multiple batches, chunking with throttling, and an unauthorized batch | Each HTTP status maps to a specific exception type, and batching is both chunked and throttled — the throttle is asserted, not just the chunk boundary. | Unit | [L26]($P/Fga/PracticeAuthorizationProxyApiCallerTests.cs#L26) |
| 182 | FgaEndpointConfigProviderTests | Per-endpoint rollout config (5 tests) | Kill switch on, an unknown endpoint, a parseable variant, an unparseable variant, and an exhaustive pass over every mapped endpoint | Every failure path falls back to legacy — kill switch, unknown endpoint and unparseable variant all degrade to the old behaviour rather than to FGA, and the unknown-endpoint case also emits a metric. The exhaustive pass means a mis-typed variant string in config is caught here. | Unit | [L13]($P/Fga/FgaEndpointConfigProviderTests.cs#L13) |
| 183 | FakePracticeAuthorizationProxyApiCallerTests | The fake caller (1 test) | One authorization check through the fake | Guards the test double other suites depend on. | Unit | [L12]($P/Fga/FakePracticeAuthorizationProxyApiCallerTests.cs#L12) |

---

## `Zocdoc.PracticeUserRolesPrivate.Tests/`

The third project: the private API that other services call to read and write practice-user roles. Five classes, 54 tests, weighted toward request validation and the backfill that migrated existing users onto the new role model.

| # | Test Class | What It Tests | Steps | Summary | Scope | Source Code |
|---|---|---|---|---|---|---|
| 184 | RequestValidationServiceTests | Request validation (18 tests) | Deletion validation over non-existing and non-provider users; then role-set validation over duplicates, a stored role-set differing from an MPL request, non-existing users, churned users, non-existing practices, non-provider users, a valid MPL request, and churned-entry filtering including an empty list | Validation returns the offending id rather than a boolean, so the caller can report which user or practice failed. MPL requests are validated against the stored role set, not just the request body. | Unit | [L19]($A/RequestValidationServiceTests.cs#L19) |
| 185 | PracticeUsersServiceTests | User data reads (13 tests) | Valid ids, no authorized users, null authorized users, empty ids, duplicate ids, dependency wiring, permissions for one and several practices, no permissions, null ids, and names for deleted users | Duplicate ids are de-duplicated before the downstream API call, and with several practices the first non-empty permission set wins rather than a union. | Unit | [L23]($A/PracticeUsersServiceTests.cs#L23) |
| 186 | BackfillServiceTests | Role backfill and deletion (9 tests) | Delete users, delete an already-deleted user, delete an already-deleted but approved user, delete several; then backfill with the primary unmapped and one practice, already mapped, mapped with a different practice, unmapped with several practices, and unmapped with a single practice | Deleting an already-deleted user is tolerated unless the user is approved, in which case it throws. Backfill enables MPL login for multi-practice users and disables it for single-practice ones. | Unit | [L24]($A/BackfillServiceTests.cs#L24) |
| 187 | PrimaryPracticeUpdateServiceTests | Primary practice update (8 tests) | Valid requested practices, partial overlap with the allowed set, no overlap, an empty request, dependency wiring, a single allowed practice, a created-date tie, and the churn-service parameters | The oldest allowed practice wins, ties break by id, and no overlap throws instead of silently keeping the current primary. | Unit | [L21]($A/PrimaryPracticeUpdateServiceTests.cs#L21) |
| 188 | MapperHelperTests | Role and permission mapping (6 tests) | Every Plinth role accounted for, the Plinth-to-staff map, roles filtered out, and exhaustive conversion checks for staff and practice permissions | Three of the six tests are exhaustive enum sweeps — the same "no unmapped value" guard as row 177, applied to the public API contract. | Unit | [L10]($A/MapperHelperTests.cs#L10) |

---

## Observations

**Scale and shape.** 188 test classes holding 2,180 test methods, across three projects. The distribution is heavily skewed: the ten largest classes (rows 55, 135, 72, 118, 119, 99, 100, 127, 167, 161) hold 512 methods — just under a quarter of the total — while 26 classes have three tests or fewer. Grouping by feature area rather than by file was necessary; 78 of the 188 classes are the only class in their directory.

**Everything here is mid-migration, and the tests are the migration's contract.** Five separate migrations are visible in the coverage, and in each case the tests exist mainly to pin the equivalence between old and new:

- **Auth0** — rows 55 and 56 (127 tests between them) exist because every login must work through both the legacy ASP.NET path and Auth0's patient and provider tenants. Row 59 covers the cookie-vs-JWT precedence that follows from running both.
- **JWT v1 → v2** — row 101 validates both versions through one service while row 100 only generates v2.
- **SHA-1 → PBKDF2** — row 73's backfill tests assert the existing salt is reused, because regenerating it would invalidate every migrated password.
- **FGA** — rows 180–183, where row 182 governs the rollout switch itself.
- **Out-of-monolith identity** — the entire `AuthOOM/` area (rows 109–117) is reconciliation between the monolith's tables and Auth0 / `auth-service`.

**Fail-closed is the house rule, with two documented exceptions.** Ambiguity is almost always rejected: multiple phone numbers on file makes a user SMS-ineligible rather than picking one (row 173), an invalid ticket source throws rather than defaulting (row 162), three separate "no practice" shapes all clear the cookie rather than writing an ambiguous value (row 138), and an unknown identity is never coerced into a default (row 3). The two deliberate exceptions are both fail-open by design and both tested as such: a password-reset request for an unknown user still sends an email (row 118, anti-enumeration), and a failed hash upgrade is swallowed so a login cannot fail because the rehash did (row 77).

**The interesting asymmetries.** Several classes test the *same* operation with deliberately *different* failure behaviour, and those differences are the highest-value assertions in the mapping:
- Row 180 — practice checks return false on bad input, organization and batch checks throw.
- Rows 77 vs 78 — an upgrade exception is logged and swallowed; a verify exception is logged and rethrown.
- Row 110 — OOM deletion records a metric and rethrows, while every other reconciliator in the same directory logs and continues.
- Row 48 vs 54 — the client repository throws on an unknown id; the host above it converts that to null to keep the OAuth2 response well-formed.

**Three genuinely integrated areas.** Ten classes hit a real database rather than mocks: rows 66, 67, 70, 72, 95, 114, 125, 126, 145 and 171. Row 72 is the widest — the membership provider wired with real salts, verifiers and SQL friend, with the PBKDF2 iteration count lowered to 2 so it stays fast. Everything else in the mapping is mocked unit coverage, so the monolith has essentially no HTTP-level authorization tests of its own; those live in the Playwright suite and in `auth-service`'s `tests/ApiTests/`.

**Exhaustive enum sweeps as a pattern.** Rows 108, 146, 177 and 188 each assert that every value of an enum or constant set is accounted for, unique, or maps cleanly. These are one-line tests with outsized value — a duplicated JWT role id (row 108) would silently grant the wrong role to every token holder, and a stray leading space in a role name (row 146) would silently deny access, since both are compared by exact match.

**Thin spots.** Row 69 gives two tests to a rule that gates authentication on every request. Row 107 gives one test to practice resolution for JWTs, covering only the ineligible multi-provider case. Rows 158–160 cover only output formatting of the hash helpers, and MD5 is still present with no indication of where it is used. Row 166 is a single smoke test over auth entity monitoring. Row 98 is one test over a metrics decorator. None of these are wrong to be thin, but they are where the monolith's auth coverage is thinnest relative to what the code does.

**One stale ownership entry.** `CODEOWNERS` still assigns `/Zocdoc.AuditLogging/` to the Auth team, but that directory no longer exists — it became the standalone `audit-logging-service`, mapped separately. The entry has no tests behind it and should be removed.
