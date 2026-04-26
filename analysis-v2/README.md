# Pterodactyl Test Coverage Audit — v2 (Deep Evidence)

This is the **v2** audit. It supersedes [`/analysis/`](../analysis/) (v1), which contained material errors. The v1 reports are preserved unchanged for diff purposes.

Every count, claim, and gap in v2 is backed by a `grep` result actually run against the cloned repo at the SHA pinned below. Every link uses a permanent SHA-pinned URL so it cannot rot.

## What v1 got wrong (the material corrections)

| # | v1 Claim | Reality (v2) |
|---|----------|--------------|
| 1 | "89+ Selenium tests" for Pterodactyl in `zocdoc_web` | **Zero true Selenium tests.** All 255 tests under `SeleniumTests/SeleniumTests/Tests/` are HTTP API tests (extend `BaseZocHttpApiTestFixture`; no `using OpenQA.Selenium`). The directory name is misleading. |
| 2 | practice-user-permissions had "~870 tests" | **1,043 verified tests** (undercounted by ~173). |
| 3 | Selenium per-file undercounts of 100+ tests across 3 files (e.g. `OrganizationUserApiTests` v1=1 / actual=34) | Corrected per-file table in [`selenium-monolith.md`](selenium-monolith.md). |
| 4 | Three FGA test files missed entirely (`BulkProfileCompletionFgaAuthTests`, `PracticeLocationsSettingsFgaAuthTests`, `MultiPracticeProfileSettingsFgaAuthTests` — 43 tests total) | All three documented in [`selenium-monolith.md`](selenium-monolith.md). |
| 5 | Frontend Users Page has "ZERO frontend unit tests" | **REFUTED — v2 self-correction.** Pterodactyl owns 3 UI areas per CODEOWNERS, with **5 Jest unit tests + 123 in-app Cypress + 13 Chromatic stories**. The original v2 grep used `*.test.tsx` but the monorepo uses `*-tests.tsx`. See [`frontend-users-page.md`](frontend-users-page.md) and [`MISSED-TEST-SURFACES.md`](MISSED-TEST-SURFACES.md). |
| 6 | Per-project breakdown for backend (Cron, Lambda, Worker integration tests) | **PUP Cron has 1 integration test for a 4x/day cron, Lambda has 1 integration test for 12 Lambdas, Worker.UnitTests is empty.** See [`MISSED-TEST-SURFACES.md`](MISSED-TEST-SURFACES.md). |
| 7 | CDK / infrastructure tests | **0 CDK tests in any of the 4 backend repos** despite each having `jest.config.js` configured. Plus no Datadog Synthetics, Pact, k6, Verify, or mutation tests anywhere. See [`MISSED-TEST-SURFACES.md`](MISSED-TEST-SURFACES.md). |

## SHA Pin Table

Every link in this audit resolves to one of these SHAs.

| Repo | Pinned SHA |
|------|-----------|
| `Zocdoc/practice-user-permissions` | `0fc641daa80e827bf13a5b95edbf2574f0fd6d42` |
| `Zocdoc/practice-authorization-proxy` | `e8c72baef19e1031dd0c753eb019d67a2d36aaf2` |
| `Zocdoc/provider-grouping` | `d0bea39cc248a677df3e27faef314f1d3201b412` |
| `Zocdoc/provider-join-service` | `cec322f4fe6d69011b6ba74ae097cbaea59ea030` |
| `Zocdoc/zocdoc_web` (monolith) | `32cbab30f3919c0bddb684eeb01151e58793e13c` |
| `Zocdoc/provider-fe-monorepo` | `37d7eff62d9096c1b59ca494697b3ac5068a3234` |
| `Zocdoc/sandbox` (Cypress repo) | `e6c476cd294f9d80cf1bead34fc16c786fedc7b3` |

Link template: `https://github.com/Zocdoc/{repo}/blob/{SHA}/{path}#L{line}`.

## Reports

| Report | Scope |
|--------|-------|
| [MASTER-INVENTORY.md](MASTER-INVENTORY.md) | One-line per-repo inventory with v1 vs v2 deltas |
| [CORRECTIONS-VS-V1.md](CORRECTIONS-VS-V1.md) | Every v1 claim graded CONFIRMED / REFUTED / PARTIAL |
| [GAPS.md](GAPS.md) | Verified test gaps (no inflated/imaginary ones from v1) |
| [practice-user-permissions.md](practice-user-permissions.md) | 1,043 tests across 94 files |
| [practice-authorization-proxy.md](practice-authorization-proxy.md) | 26 tests across 7 files (incl. 3 placeholder `1+1==2`) |
| [provider-grouping.md](provider-grouping.md) | 471 tests across 36 files |
| [provider-join-service.md](provider-join-service.md) | 634 tests across 54 files |
| [selenium-monolith.md](selenium-monolith.md) | 255 HTTP API tests (NOT Selenium); 13 files |
| [cypress-e2e.md](cypress-e2e.md) | 72 `it(...)` blocks across 9 spec files |
| [frontend-users-page.md](frontend-users-page.md) | Zero unit tests in the Pterodactyl Users Page UI |
| [METHODOLOGY.md](METHODOLOGY.md) | grep patterns used, SHA-pinning rationale, source-vs-test mapping algorithm |
| [MISSED-TEST-SURFACES.md](MISSED-TEST-SURFACES.md) | Per-project breakdown, CDK tests, Datadog Synthetics, in-app Cypress, Storybook (added after first pass) |
| [EXHAUSTIVE-SWEEP.md](EXHAUSTIVE-SWEEP.md) | 5-surface residual sweep (cypress component / vitest / plinth contract / other Pterodactyl UI / cross-folder Cypress) — added 26 tests via `create-staff-page-v2-tests.ts` |
| [PLAIN-ENGLISH.md](PLAIN-ENGLISH.md) | Layman summary: where we stand and what's next |

## Headline Totals (corrected 2026-04-27 after exhaustive sweep)

| Surface | Files | Tests |
|---------|------:|------:|
| practice-user-permissions | 94 | 1,043 |
| practice-authorization-proxy | 7 | 26 |
| provider-grouping | 36 | 471 |
| provider-join-service | 54 | 634 |
| zocdoc_web monolith (HTTP API, mislabeled "Selenium") | 13 | 255 |
| Cypress E2E sandbox repo (Account-User-Setup) | 9 | 72 |
| Frontend Pterodactyl UI — Jest unit tests | 2 | 5 |
| Frontend Pterodactyl UI — in-app Cypress E2E | 4 | 149 |
| **TOTAL** | **219** | **2,655** |

The 5-surface sweep ([EXHAUSTIVE-SWEEP.md](EXHAUSTIVE-SWEEP.md)) added one in-app Cypress file (`create-staff-page-v2-tests.ts`, 26 tests) and confirmed the four other surfaces (cypress component tests, vitest, plinth/openapi contract, cross-folder Pterodactyl Cypress) are clean.

Plus 13 Chromatic visual regression stories under Pterodactyl ownership.

**Empty / near-empty test projects (genuine gaps):**
- `PracticeUserPermissions.Worker.UnitTests` — 0 tests (project exists)
- `PracticeUserPermissions.Cron.IntegrationTests` — 1 test for a 4x/day cron
- `PracticeUserPermissions.Lambda.IntegrationTests` — 1 test for 12 Lambdas
- `SelfSignup.Tests.Unit` — 0 tests (project exists)
- All four repos' `cdk/test/` directories — empty despite Jest configs
