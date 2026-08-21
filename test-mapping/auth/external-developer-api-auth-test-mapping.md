# external-developer-api-auth - Jest Test Mapping

<!-- test-mapping-meta
repo: Zocdoc/external-developer-api-auth
branch: main
commit: 198ebb42192838214bdc2f5dd504935106471079
generated: 2026-08-21
test-type: jest
scope: whole repo (owner team `auth` per plinth.yaml)
granularity: one row per test
-->
> Source: Zocdoc/external-developer-api-auth @ `198ebb4` · branch `main` · generated 2026-08-21

**Team:** Infrastructure / Auth · **Coverage:** 1 file · 4 tests.
**Repo:** CDK infrastructure that loads the external-developer (partner) Auth0 app-client roster per AWS account and writes it into DynamoDB.

---

## cdk/test/auth0-app-clients.test.ts

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 1 | auth0AppClients > loads CI auth0 app clients | The CI account's app-client roster file loads and is non-empty. | `loadAuth0AppClients(Account.CI.name)` -> Assert defined -> Assert `length > 0` | Smoke-checks that the CI config file exists and parses. | In: file resolves and is non-empty. Out: the contents of any client. | [L5](https://github.com/Zocdoc/external-developer-api-auth/blob/198ebb42192838214bdc2f5dd504935106471079/cdk/test/auth0-app-clients.test.ts#L5) |
| 2 | auth0AppClients > loads PR201 auth0 app clients | The PR201 account's app-client roster file loads and is non-empty. | `loadAuth0AppClients(Account.PR201.name)` -> Assert defined -> Assert `length > 0` | Same smoke check for the PR201 account. | In: PR201 config resolves. Out: prod and other accounts are not covered. | [L11](https://github.com/Zocdoc/external-developer-api-auth/blob/198ebb42192838214bdc2f5dd504935106471079/cdk/test/auth0-app-clients.test.ts#L11) |
| 3 | auth0AppClients > maps booking requirement attributes when enabled on the client | Booking-requirement flags set to `true` on a client map to `{ BOOL: true }` Dynamo attributes. | Build an `Auth0AppClientUser` with `memberIdBookingRequirementEnabled: true` and `insuranceAcceptanceRequirementEnabled: true` -> `auth0AppClientsToDynamoRequests([client])[0].PutRequest.Item` -> Assert `MemberIdBookingRequirementEnabled` and `InsuranceAcceptanceRequirementEnabled` both equal `{ BOOL: true }` | Verifies the enabled case of the flag-to-Dynamo mapping. | In: 2 flags, true case. Out: the other ~10 fields on the client object. | [L17](https://github.com/Zocdoc/external-developer-api-auth/blob/198ebb42192838214bdc2f5dd504935106471079/cdk/test/auth0-app-clients.test.ts#L17) |
| 4 | auth0AppClients > defaults booking requirement attributes to false when omitted on the client | Omitting the booking-requirement flags defaults them to `{ BOOL: false }` rather than leaving them undefined. | Build the same client with both flags absent -> map to a Dynamo put item -> Assert both attributes equal `{ BOOL: false }` | Verifies the default, which keeps a partner from silently inheriting a permissive value. | In: 2 flags, omitted case. Out: explicit `false` vs omitted (behaviorally identical here). | [L40](https://github.com/Zocdoc/external-developer-api-auth/blob/198ebb42192838214bdc2f5dd504935106471079/cdk/test/auth0-app-clients.test.ts#L40) |

---

## Observations

- **This is the whole test suite for the repo** — 4 tests in one file. The Dynamo mapping is covered only for the two booking-requirement flags; the other client attributes (`hasAccessToReviews`, `patientTransactionalMessagingEnabled`, `developerRole`, `shouldExcludeActivityFromReporting`, etc.) have no assertions.
- **Only CI and PR201 rosters are load-tested.** Production and the remaining accounts have no equivalent smoke test, so a malformed prod roster would not be caught here.
