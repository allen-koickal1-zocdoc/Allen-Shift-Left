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

## Headline Totals

| Surface | Files | Tests |
|---------|-------|-------|
| practice-user-permissions | 94 | 1,043 |
| practice-authorization-proxy | 7 | 26 |
| provider-grouping | 36 | 471 |
| provider-join-service | 54 | 634 |
| zocdoc_web monolith (HTTP API, mislabeled "Selenium") | 13 | 255 |
| Cypress E2E (Account-User-Setup) | 9 | 72 |
| **TOTAL** | **213** | **2,501** |

Frontend (`provider-fe-monorepo/apps/settings/`): **0** Jest/Vitest unit tests covering the Pterodactyl-owned Users Page. Confirmed in [`frontend-users-page.md`](frontend-users-page.md).
