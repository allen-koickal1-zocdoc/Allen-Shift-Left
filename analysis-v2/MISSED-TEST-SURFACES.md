# Test Surfaces Originally Missed (v2 supplement)

Added after the user asked: "did we miss any test like api, cron, datadog synthetic anything at all".

This file lists test types/surfaces beyond NUnit unit + Cypress E2E that we either confirmed are absent or found to be severely under-resourced.

## ⚠️ Frontend correction (most important)

The original v2 incorrectly reported **0 frontend unit tests** for the Users Page. After the user pointed out that `apps/settings/cypress/e2e/PracticeUsersPage/` exists, a full re-audit found:

- **5 Jest unit tests** for the Users Page (file naming uses `*-tests.tsx` with a hyphen, which the v2 grep missed)
- **68 in-app Cypress E2E tests** for `PracticeUsersPage/` (incorrectly excluded as "out of scope")
- **55 in-app Cypress E2E tests** for `signUpPortal/` in a different webapp (`apps/provider-home-webapp`)
- **13 Storybook stories** under Chromatic visual regression for Pterodactyl-owned components

Per [CODEOWNERS](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/.github/CODEOWNERS) Pterodactyl owns **3 UI areas**, not just one. See [frontend-users-page.md](frontend-users-page.md) for the corrected report.

**Total Pterodactyl frontend tests: 128 (5 unit + 123 in-app Cypress) + 13 Chromatic stories.** Not zero.

---

## 1. Per-test-project breakdown — what we'd missed in v2 main reports

The v2 totals are correct, but we hadn't broken them out by project. Several of these projects are critical (Cron, Lambda, Worker integration) and have near-zero coverage.

### practice-user-permissions @ `0fc641daa80e827bf13a5b95edbf2574f0fd6d42` — 1,043 total

| Test Project | Files | Tests | Notes |
|--------------|------:|------:|-------|
| [PracticeUserPermissions.UnitTests](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.UnitTests) | 35 | 380 | Core service unit tests |
| [PracticeUserPermissions.Lambda.UnitTests](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Lambda.UnitTests) | 31 | 269 | Lambda unit tests |
| [PracticeUserPermissions.Web.ApiTests](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Web.ApiTests) | 8 | 209 | HTTP API tests |
| [PracticeUserPermissions.IntegrationTests](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.IntegrationTests) | 8 | 117 | Service integration |
| [PracticeUserPermissions.Web.UnitTests](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Web.UnitTests) | 9 | 64 | Web layer unit tests |
| [PracticeUserPermissions.Worker.IntegrationTests](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Worker.IntegrationTests) | 1 | **2** | ⚠️ Worker has 2 integration tests |
| [PracticeUserPermissions.Lambda.IntegrationTests](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Lambda.IntegrationTests) | 1 | **1** | ⚠️ 12 Lambdas, 1 integration test |
| [PracticeUserPermissions.Cron.IntegrationTests](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Cron.IntegrationTests) | 1 | **1** | ⚠️ Cron runs 4x/day, 1 integration test |
| [PracticeUserPermissions.Worker.UnitTests](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Worker.UnitTests) | 0 | **0** | ❌ Project exists but empty |
| [TestCommon](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/TestCommon) | — | 0 | Test helper library |
| **Total** | **94** | **1,043** | |

### provider-grouping @ `d0bea39cc248a677df3e27faef314f1d3201b412` — 471 total

| Test Project | Files | Tests | Notes |
|--------------|------:|------:|-------|
| [UnitTests](https://github.com/Zocdoc/provider-grouping/tree/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests) | 18 | 176 | Core service unit tests |
| [ApiTests](https://github.com/Zocdoc/provider-grouping/tree/d0bea39cc248a677df3e27faef314f1d3201b412/tests/ApiTests) | 3 | 176 | HTTP API tests |
| [IntegrationTests](https://github.com/Zocdoc/provider-grouping/tree/d0bea39cc248a677df3e27faef314f1d3201b412/tests/IntegrationTests) | 7 | 60 | Service integration |
| [LambdaTests](https://github.com/Zocdoc/provider-grouping/tree/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests) | 7 | 58 | Lambda tests (8 Lambda projects) |
| [Tests.Common](https://github.com/Zocdoc/provider-grouping/tree/d0bea39cc248a677df3e27faef314f1d3201b412/tests/Tests.Common) | 1 | 1 | Helper |

**No Cron-specific test project** even though `ProviderGrouping.Cron` runs every 5 minutes. Cron is tested only via UnitTests.

### practice-authorization-proxy @ `e8c72baef19e1031dd0c753eb019d67a2d36aaf2` — 26 total

| Test Project | Files | Tests |
|--------------|------:|------:|
| [PracticeAuthorizationProxy.UnitTests](https://github.com/Zocdoc/practice-authorization-proxy/tree/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.UnitTests) | 2 | 13 |
| [PracticeAuthorizationProxy.Web.ApiTests](https://github.com/Zocdoc/practice-authorization-proxy/tree/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.Web.ApiTests) | 2 | 6 |
| [PracticeAuthorizationProxy.Web.UnitTests](https://github.com/Zocdoc/practice-authorization-proxy/tree/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.Web.UnitTests) | 1 | 5 |
| [PracticeAuthorizationProxy.Web.IntegrationTests](https://github.com/Zocdoc/practice-authorization-proxy/tree/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.Web.IntegrationTests) | 1 | 1 |
| [PracticeAuthorizationProxy.IntegrationTests](https://github.com/Zocdoc/practice-authorization-proxy/tree/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/tests/PracticeAuthorizationProxy.IntegrationTests) | 1 | 1 |

### provider-join-service @ `cec322f4fe6d69011b6ba74ae097cbaea59ea030` — 634 total

Already broken out in [provider-join-service.md](provider-join-service.md). One empty project: `SelfSignup.Tests.Unit`.

---

## 2. CDK Infrastructure Tests — **0 tests in all 4 repos**

Every repo has a `cdk/` directory configured for Jest tests:

```js
// cdk/jest.config.js (identical in all 4 repos)
module.exports = {
  testEnvironment: 'node',
  roots: ['<rootDir>/test'],
  testMatch: ['**/*.test.ts'],
  transform: { '^.+\\.tsx?$': 'ts-jest' }
};
```

But the `test/` directory **does not exist** in any of them. Verified via:

```bash
find cdk -name "*.test.ts" -o -name "*.spec.ts" | grep -v node_modules
# Returns nothing in all 4 repos
```

**What's untested:**

| Repo | Untested CDK code |
|------|------|
| practice-user-permissions | [AuditLogS3.ts](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/cdk/src/AuditLogS3.ts), [createLambdaFunction.ts](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/cdk/src/createLambdaFunction.ts), [createSqsWithDlq.ts](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/cdk/src/createSqsWithDlq.ts), [PracticeUserPermissionsCronStack.ts](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/cdk/src/PracticeUserPermissionsCronStack.ts), [PracticeUserPermissionsLambdaStack.ts](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/cdk/src/PracticeUserPermissionsLambdaStack.ts), [PracticeUserPermissionsWorkerStack.ts](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/cdk/src/PracticeUserPermissionsWorkerStack.ts) |
| practice-authorization-proxy | [cdk.ts](https://github.com/Zocdoc/practice-authorization-proxy/blob/e8c72baef19e1031dd0c753eb019d67a2d36aaf2/cdk/src/cdk.ts) |
| provider-grouping | [cdk.ts](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/cdk/src/cdk.ts), [monolithSyncLambdaStack.ts](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/cdk/src/monolithSyncLambdaStack.ts) |
| provider-join-service | [cdk.ts](https://github.com/Zocdoc/provider-join-service/blob/cec322f4fe6d69011b6ba74ae097cbaea59ea030/cdk/src/cdk.ts) |

**Risk:** Infrastructure changes (IAM policies, Lambda configs, S3 bucket policies, SQS DLQ wiring, autoscaling) deploy without any automated verification. Per [Zocdoc OPS-009 standard](~/.claude/skills/zd-base/standards/devops/OPS-009.md), CDK changes are subject to security review — but there's no test asset to back that review.

---

## 3. Datadog Synthetic Tests — None as code

Searched all 4 repos for synthetic test config:

```bash
grep -rE "synthetic|Synthetic" --include="*.json" --include="*.yaml" --include="*.yml" --include="*.tf"
# No results in any repo
```

**Datadog dashboards exist** for both PUP and POGS (referenced in original v1 README), but no synthetic browser/API tests defined as code in these repos.

⚠️ **Cannot verify whether synthetics exist out-of-band in Datadog UI.** They could be configured directly in Datadog without being checked into the repo. To confirm, log into Datadog → Synthetics → filter by team `@Zocdoc/user-permissions`.

---

## 4. Other Test Surfaces — Confirmed Absent

| Surface | Status | Search performed |
|---------|--------|------------------|
| **Pact / contract tests** | None | `find . -iname "*pact*"` and `find . -iname "*contract*test*"` |
| **Postman collections** | None | `find . -iname "*.postman*"` |
| **k6 / JMeter / load tests** | None | `find . -iname "*k6*" -o -iname "*loadtest*"` |
| **Verify snapshot tests (CS-006)** | None | `grep -r "Verify\." --include="*.cs" -l` returned only one app-code reference |
| **Stryker mutation tests** | None | No `stryker-config.json` in any repo |
| **xUnit `[Fact]` / `[Theory]`** | None | All 4 repos use NUnit exclusively |
| **Smoke tests** | None as files | `find . -iname "*smoke*"` (deploy hooks would live in zd-cdk, not here) |
| **Accessibility / axe tests** | None | No `axe-core` or `@axe-core/cypress` in any package.json |
| **Storybook visual tests** | N/A | Backend repos don't ship Storybook |
| **Percy visual regression** | N/A | Backend repos don't ship Percy |

---

## 5. Things we cannot verify from these clones

| Item | Why | How to verify |
|------|-----|---------------|
| Datadog Synthetic UI tests | Configured in Datadog UI, not in code | Datadog → Synthetics, filter `team:user-permissions` |
| Datadog monitor coverage | zd-cdk-bound, may live in `zd-cdk` repo | Search `zd-cdk` for `team: user-permissions` |
| Smoke tests in deployment | Live in deploy pipeline (Octopus/zd-deploy) | Octopus Deploy → projects matching repo names |
| Cypress component tests | Cypress component runner lives in apps that ship UI | Check `provider-fe-monorepo/apps/settings/cypress.config.*` |
| OpenAPI contract validation | Could run via Plinth swagger checks at CI time | Check Plinth CI config |

---

## 6. Updated headline summary

If we add the missed surfaces, **Pterodactyl owns 6 layers of tests**, of which only 3 are healthy:

| Layer | Status | Tests |
|-------|--------|------:|
| Backend unit tests (NUnit) | ✓ Healthy | ~1,500 |
| Backend integration tests (LocalStack/DDB local) | ✓ Healthy | ~270 |
| Backend HTTP/API tests | ✓ Healthy | ~390 |
| Selenium browser tests | ❌ **None exist** despite directory naming | 0 |
| Cypress E2E tests | ⚠️ Adequate but no org-level FGA coverage | ~72 |
| Frontend unit tests (Users Page) | ❌ **None exist** | 0 |
| **Cron integration tests (PUP)** | ⚠️ **1 test for a 4x/day cron** | 1 |
| **Lambda integration tests (PUP)** | ⚠️ **1 test for 12 Lambdas** | 1 |
| **Worker unit tests (PUP)** | ❌ **Empty project** | 0 |
| **CDK infrastructure tests** | ❌ **None exist in any repo** | 0 |
| Datadog Synthetics | ❓ **Not in code; may exist in DD UI** | unknown |
| Contract tests / Pact / Postman / k6 / Verify / mutation | ❌ Absent | 0 |

---

*Generated 2026-04-27. SHA-pinned per repo.*
