# Exhaustive 5-Surface Sweep

Date: 2026-04-27. SHAs from [README.md](README.md).

This pass closes the residual gaps after the question "did we cover every unit, integration test etc." The previous v2 walked the obvious surfaces; this one re-checks five surfaces that could have hidden tests.

## Summary

| # | Surface | Result | New tests | New files |
|---|---------|--------|----------:|----------:|
| 1 | Other Pterodactyl-owned UI in provider-fe-monorepo | **Confirmed clean** — only the 3 paths in root CODEOWNERS are Pterodactyl-owned; nested CODEOWNERS files belong to other teams | 0 | 0 |
| 2 | Cypress component tests (`cypress/component/`) | **Confirmed clean** — zero `cypress/component/` dirs and zero `component:` blocks in any cypress.config | 0 | 0 |
| 3 | Pterodactyl-relevant Cypress in sandbox repo outside Account-User-Setup | **Confirmed clean** — keyword matches outside the folder are unrelated (patient sign-in, marketplace, WL, etc.) | 0 | 0 |
| 4 | Vitest configurations | **Confirmed clean** — zero `vitest.config.*` files and zero `vitest` deps in any of the 5 repos | 0 | 0 |
| 5 | Plinth / OpenAPI contract validation at build time | **Confirmed clean** — no `PlinthContract`/`VerifySwagger`/`VerifyApi` markers; the only swagger refs are UI asset bundling | 0 | 0 |
| Bonus | `create-staff-page-v2-tests.ts` (was "unverified" in frontend-users-page.md) | **NEW finding** — 26 in-app Cypress `it()` blocks for `createProviderOrStaffPage` | **+26** | **+1** |

**Net change to grand total: 2,629 -> 2,655.**

---

## Surface 1 — Other Pterodactyl-owned UI in provider-fe-monorepo

### CODEOWNERS sweep

```
$ find . -name "CODEOWNERS" -not -path "*/node_modules/*"
./.github/CODEOWNERS
./shared/mini-front-end/.github/CODEOWNERS         # @Zocdoc/cal-inbox-pod (NOT Pterodactyl)
./shared/core/.github/CODEOWNERS                   # @Zocdoc/provider-peacock-team (NOT Pterodactyl)

$ grep -n "user-permissions\|pterodactyl" .github/CODEOWNERS
21: /apps/settings/src/pages/settingsPages/practiceSettings/createProviderOrStaffPage/   @Zocdoc/user-permissions
22: /apps/settings/src/pages/settingsPages/practiceUsersPage/                            @Zocdoc/user-permissions
47: apps/provider-home-webapp/src/pages/signUpPortal/                                    @Zocdoc/user-permissions
```

Only three Pterodactyl-owned UI paths exist. All three were already covered in [`frontend-users-page.md`](frontend-users-page.md). No `OWNERSHIP*` files exist in the monorepo.

**Verdict:** Confirmed clean. The previous v2 was complete on UI ownership.

---

## Surface 2 — Cypress component tests

```
$ find . -path "*/cypress/component/*" -not -path "*/node_modules/*"
(empty)

$ for f in apps/*/cypress.config.ts shared/*/cypress.config.ts; do
    grep -c "component" "$f"
  done
apps/dashboard/cypress.config.ts: 0
apps/enterprise-tools/cypress.config.ts: 0
apps/phi-safe/cypress.config.ts: 0
apps/provider-home-webapp/cypress.config.ts: 0
apps/settings/cypress.config.ts: 0
apps/spo-webapp/cypress.config.ts: 0
apps/synchronizer-webapp/cypress.config.ts: 0
shared/core/cypress.config.ts: 0
shared/mini-front-end/cypress.config.ts: 0
```

Every cypress.config.ts has only an `e2e:` block. specPattern is uniformly `cypress/e2e/**/*-tests.@(js|ts)`. Zero component testing infrastructure exists.

**Verdict:** Confirmed clean.

---

## Surface 3 — Pterodactyl-relevant Cypress outside Account-User-Setup (sandbox repo)

```
$ find cypress/e2e -name "*.spec.js" | xargs grep -lE "user-management|user-role|userRole|practice-user|RBAC|self-signup" \
   | grep -v Account-User-Setup
(empty)

$ find cypress/e2e -name "*.spec.js" | xargs grep -lE "permission|FGA|invite|signup|sign-up" \
   | grep -v Account-User-Setup
cypress/e2e/BU/Marketplace/Patient-Acquisition/Flows/sem-page-flow.spec.js
cypress/e2e/BU/Marketplace/Patient-Acquisition/Flows/homepage-flow.spec.js
cypress/e2e/BU/Provider/Retention/Provider-Success/Flows/provider-dashboard-flow.spec.js
cypress/e2e/BU/Infrastructure/Auth/Flows/patient-signin-flow.spec.js
cypress/e2e/BU/Practice-Solutions/Branded-Directory/Flows/wl-flow.spec.js
cypress/e2e/BU/Practice-Solutions/Appointment-Management/Pages/inbox-page.spec.js
cypress/e2e/BU/Practice-Solutions/Appointment-Management/Flows/appointment-management-flow.spec.js
cypress/e2e/BU/NoMansLand/Wordpress/Pages/about-page.spec.js
cypress/e2e/BU/NoMansLand/Wordpress/Pages/cms-page.spec.js
cypress/e2e/BU/Provider/Adoption/Provider-Onboarding/Flows/features-flow.spec.js
```

These match because of unrelated keywords: patient sign-in, marketplace SEM/homepage, WL/Branded-Directory, Practice-Solutions appt mgmt, etc. None touch Pterodactyl-owned features.

The narrower keyword set (`user-management|user-role|practice-user|RBAC|self-signup`) returned only files already inside `Account-User-Setup/`.

**Verdict:** Confirmed clean.

---

## Surface 4 — Vitest configurations

```
$ for d in practice-user-permissions practice-authorization-proxy provider-grouping provider-join-service provider-fe-monorepo; do
    cd "$d"
    find . -maxdepth 4 -name "vitest.config.*" -not -path "*/node_modules/*"
    find . -name "package.json" -not -path "*/node_modules/*" | xargs grep -l "vitest" 2>/dev/null
  done
(empty across all 5 repos)
```

Zero vitest configs and zero `vitest` package.json deps anywhere. The four backend repos are .NET (NUnit). The frontend monorepo uses Jest via react-scripts (`yarn test:react-scripts`), not Vitest.

**Verdict:** Confirmed clean.

---

## Surface 5 — Plinth / OpenAPI contract validation at build time

```
$ for d in practice-user-permissions practice-authorization-proxy provider-grouping provider-join-service; do
    cd "$d"
    find . -name "swagger.json" -o -name "swagger.yaml" -o -name "openapi.json" -o -name "openapi.yaml"
    grep -rE "PlinthContract|VerifySwagger|VerifyApi|VerifyOpenApi" --include="*.cs" -l
    ls .github/workflows/
  done
(no .github/workflows/ dirs — these repos use TeamCity + Pants)
(0 PlinthContract/VerifySwagger/VerifyApi/VerifyOpenApi matches)
(0 swagger/openapi spec files)

$ grep -E "swagger|openapi|api-spec" src/*.Web/BUILD
practice-user-permissions:  "swagger-ui/index.css",        # UI asset bundling only
provider-grouping:          "swagger-ui/index.css",        # UI asset bundling only
practice-authorization-proxy: "swagger-ui/index.css",      # UI asset bundling only
provider-join-service:      (no swagger refs)
```

The only swagger/openapi references are runtime UI asset bundling (Swagger UI for `/swagger/*`). No contract test, no Verify-based snapshot of the API spec, no build-time validator step.

**Verdict:** Confirmed clean — and this is itself a gap worth flagging.

---

## Bonus checks

### Cron-specific tests

```
$ find tests -type f -name "*.cs" | xargs grep -lE "Cron|cron"
practice-user-permissions:
  tests/PracticeUserPermissions.Cron.IntegrationTests/ScopedOrganizationBackfillServiceTests.cs   # already counted (1 test)
  tests/PracticeUserPermissions.Cron.IntegrationTests/IntegrationTestsBase.cs                      # not a test class
  tests/PracticeUserPermissions.Cron.IntegrationTests/FakeHostApplicationLifetime.cs               # helper
provider-grouping:
  tests/IntegrationTests/OrganizationSyncServiceTests.cs        # already counted (in IntegrationTests subtotal)
  tests/UnitTests/Services/OrganizationSyncServiceTests.cs      # already counted (in UnitTests subtotal)
  tests/UnitTests/Services/JitterbitServiceTests.cs             # already counted (in UnitTests subtotal)
```

All Cron-related tests already in the master inventory. No standalone `*CronTaskTests.cs` files.

### Lambda Functional test pattern

```
$ find tests -name "*Functional*" -type f
practice-user-permissions: (none)
practice-authorization-proxy: (none)
provider-grouping: (none)
provider-join-service: tests/ProviderJoinService.AbandonmentLambda.Tests/FunctionalTests   # already counted
```

PUP/PG/PAP have no Functional test pattern — only PJS has one and it was already counted (3 tests).

### package.json scripts in apps/settings and provider-home-webapp

```
apps/settings/package.json:
  "test": "yarn test:react-scripts",
  "test:react-scripts": "react-scripts test ..."
apps/provider-home-webapp/package.json:
  "test": "yarn test:react-scripts",
  "test:react-scripts": "react-scripts test ..."
```

No `test:component`, `test:integration`, or `test:e2e` scripts beyond the cypress entry points already known.

---

## NEW finding: `create-staff-page-v2-tests.ts` (26 it() tests)

This file was flagged in [`frontend-users-page.md`](frontend-users-page.md) as **"unverified"** — it was suspected but not opened or counted. It exists, it is owned by Pterodactyl, and it has 26 tests.

| File | it() count | Owner |
|------|-----------:|-------|
| [`apps/settings/cypress/e2e/PracticeSettingsPages/create-staff-page-v2-tests.ts`](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/cypress/e2e/PracticeSettingsPages/create-staff-page-v2-tests.ts) | **26** | `@Zocdoc/user-permissions` (covers `createProviderOrStaffPage`) |

Evidence the file targets `createProviderOrStaffPage`:
- Imports `createRbacUser`, `clickAddUserButton`, `verifyRoleCheckboxMetric` from `./create-staff-page-v2-commands`.
- Imports `setUpRoutesAndVisitUsersPage` from `../PracticeUsersPage/practice-users-page-v2-commands`.
- 8 distinct `createRbacUser({...})` calls covering RBAC role flows.

```
$ grep -cE "^\s*(it|test)\(" apps/settings/cypress/e2e/PracticeSettingsPages/create-staff-page-v2-tests.ts
26
```

**This adds 26 tests to the in-app Cypress subtotal**, raising it from 123 to **149**, and raises the grand total from **2,629 to 2,655**.

It also closes the "0 tests for createProviderOrStaffPage" claim in [`frontend-users-page.md`](frontend-users-page.md) — there are zero **Jest** tests, but **26 in-app Cypress tests** exist for that page.
