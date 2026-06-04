# Pterodactyl Test Coverage Audit — v3 (Current-HEAD Re-verification)

This is the **v3** audit. It re-verifies every count from [`/analysis-v2/`](../analysis-v2/) against the **current HEAD** of each repo (v2 was pinned to SHAs from 2026-04-26 and is now ~6 weeks stale — every source repo has moved since). v1 ([`/analysis/`](../analysis/)) and v2 are preserved unchanged for diffing.

Every count here was produced by fetching each repo at the SHA pinned below via the authenticated `gh api .../tarball/<sha>` endpoint (plain `git clone` is blocked in the analysis sandbox) and running the documented `grep` counters against the extracted tree. The monolith and the frontend monorepo were read through the `gh api` git-tree + contents endpoints rather than a full tarball.

## What changed since v2 — the material corrections

| # | v2 Claim | Reality (v3) |
|---|----------|--------------|
| 1 | Monolith "Selenium" tests: **255 tests / 13 files** (counted by an unverified subagent, never grepped) | **433 test methods across 27 files** (414 `[CiTest]` + 19 `[Test]`; 535 if `[TestCase]` rows are counted v2-style). v2 was blind to Zocdoc's custom **`[CiTest]`** attribute — the real per-test marker in the monolith — and missed **14** Pterodactyl-relevant files. This is the single biggest correction in v3. See [selenium-monolith.md](selenium-monolith.md). |
| 2 | Frontend Pterodactyl UI unit tests: **5** (only `practiceUsersPage`) | **20 unit tests across 6 files.** v2 missed the **15 Jest unit tests in `signUpPortal`** (`Context`, `Footer`, `RepositionConfirmEmail`, `steps`). See [frontend.md](frontend.md). |
| 3 | "Zero real Selenium tests" classification | **CONFIRMED and strengthened** — all 27 monolith files have 0 `OpenQA.Selenium` references; all chain to `BaseZocHttpApiTestFixture` (an HTTP-API base, not WebDriver). |
| 4 | practice-user-permissions `Worker.UnitTests` is **empty** (a gap) | **GAP CLOSED** — now 8 tests. A new `Cron.UnitTests` project (13 tests) and `SmokeTests` (3) also appeared. PUP grew 1,043 → **1,075**. |
| 5 | provider-grouping ~471 tests | **558 tests / 45 files** (+87). New finding: **`SalesforceAccountBackfillCron` has 0 tests**; `StrategicLambda` still has only 1 active test (the other is `[Ignore]`d). |
| 6 | `createProviderOrStaffPage` UI counted only via Cypress | **NEW GAP**: it has **0 unit tests** (7 source files incl. `CreateUserViewV2`, `RbacRoleSetupSection`) — only 26 in-app Cypress + 2 stories. |
| 7 | practice-authorization-proxy 26 tests | **31 tests / 8 files** (+5, a new `SmokeTests` project). The **3 `(1+1).Should().Be(2)` placeholders still exist**, and `AuthorizationImpl` (183 LOC) is **still untested**. |

## SHA Pin Table (current HEAD as of 2026-06-04)

| Repo | Pinned SHA | HEAD date |
|------|-----------|-----------|
| `Zocdoc/practice-user-permissions` | `e484112be9b04a2c5b6b2d3cd0c36ad613e367c7` | 2026-06-03 |
| `Zocdoc/practice-authorization-proxy` | `88ed06931303fe57e1d3cb948e86d029037fe881` | 2026-05-28 |
| `Zocdoc/provider-grouping` | `b7e65e81484cb41823073398d28563b2d5f80b73` | 2026-06-02 |
| `Zocdoc/provider-join-service` | `a7635199696e49f35fdd1cf73f346e86a99cfdbd` | 2026-05-28 |
| `Zocdoc/zocdoc_web` (monolith) | `35bc2f17109578b3ba13dbd543a4300d2c20bf3c` | 2026-06-04 |
| `Zocdoc/provider-fe-monorepo` | `2e3f76bed111f8cc3aa568bc4c8dc197cbf274fc` | 2026-06-03 |
| `Zocdoc/sandbox` (E2E repo) | `80a6b099ac35978070edc5636d0eec106600bab8` | 2026-06-04 |

Link template: `https://github.com/Zocdoc/{repo}/blob/{SHA}/{path}#L{line}`.

## Headline Totals (v3, current HEAD)

| Surface | Files | Tests |
|---------|------:|------:|
| practice-user-permissions | 98 | 1,075 |
| practice-authorization-proxy | 8 | 31 |
| provider-grouping | 45 | 558 |
| provider-join-service | 55 | 642 |
| zocdoc_web monolith (HTTP API, mislabeled "Selenium") | 27 | 433¹ |
| sandbox Cypress E2E (Account-User-Setup) | 8 | 71 |
| Frontend Pterodactyl UI — Jest/Vitest unit | 6 | 20 |
| Frontend Pterodactyl UI — in-app Cypress E2E | 4 | 151 |
| **TOTAL** | **251** | **2,981** |

Plus **12 Chromatic/Storybook visual-regression stories** under Pterodactyl ownership (not assertion tests).

¹ Monolith headline counts each `[CiTest]`/`[Test]` *method* as one (433). Counting `[TestCase(...)]` parameterized rows the way v2 counts NUnit cases yields **535**; an additional 14 `[TestCaseSource]` attributes expand to an unknown number of rows at runtime. See [selenium-monolith.md](selenium-monolith.md).

**v2→v3 total delta:** 2,655 → 2,981 tests (+326), 219 → 251 files (+32). Roughly half the growth is genuinely new tests written in the last 6 weeks; the rest is the corrected monolith `[CiTest]` count and the 15 previously-missed `signUpPortal` unit tests.

## Reports

| Report | Scope |
|--------|-------|
| [MASTER-INVENTORY.md](MASTER-INVENTORY.md) | Per-repo + per-project counts and LOC, with v2→v3 deltas |
| [CORRECTIONS-VS-V2.md](CORRECTIONS-VS-V2.md) | Every v2 claim graded CONFIRMED / CHANGED / REFUTED |
| [GAPS.md](GAPS.md) | Verified coverage gaps at current HEAD |
| [selenium-monolith.md](selenium-monolith.md) | 27 HTTP-API files, per-file `[CiTest]` counts, classification evidence |
| [frontend.md](frontend.md) | Pterodactyl UI: unit / in-app Cypress / Storybook by owned area |
| [METHODOLOGY.md](METHODOLOGY.md) | Counters, the `[CiTest]` fix, the tarball-via-gh-api fetch method |

## Genuine empty / near-empty / placeholder surfaces (current HEAD)

- `practice-authorization-proxy` — 3 `(1+1).Should().Be(2)` placeholder `ExampleTests` still present (3 of 31 "tests" are no-ops).
- `practice-authorization-proxy` — `AuthorizationImpl.cs` (183 LOC, the primary `IAuthorization` impl) has **0 direct unit tests**.
- `provider-join-service` — `SelfSignup.Tests.Unit` project is **empty** (only `Usings.cs`).
- `provider-join-service` — `AbandonmentLambda` `FunctionTest.TestReturnsId` is an echo-back placeholder (`DynamoRowId="hello"` → asserts `"hello"`).
- `provider-grouping` — `StrategicLambdaTests` has `[Ignore("Test Not Completed")]` (1 of its 2 tests stubbed); `SalesforceAccountBackfillCron` has **0 tests**.
- **All four backend repos** — `0` CDK/infrastructure tests despite each shipping a `cdk/jest.config.js`.
- `provider-fe-monorepo` — `createProviderOrStaffPage` has **0 unit tests**.
- `sandbox` — Account-User-Setup is **0% migrated to Playwright** (folders scaffolded with `.gitkeep` only; still 100% Cypress).
