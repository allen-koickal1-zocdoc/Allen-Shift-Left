# Master Test Inventory (v3 — current HEAD)

Counters (run against each repo at the SHA in [README.md](README.md)):

```
grep -cE "^\s*\[Test\]|^\s*\[TestCase\("        # NUnit (C# backend repos)
grep -cE "^\s*\[CiTest\]|^\s*\[Test\]|^\s*\[TestCase\("   # monolith (adds Zocdoc [CiTest])
grep -cE "^\s*it\("                              # Cypress
grep -cE "^\s*(it|test)\("                       # Jest/Vitest / Playwright
```

## Per-repo summary

| Repo | Test Files | Tests (v3) | v2 | Delta | Notes |
|------|-----------:|-----------:|---:|------:|-------|
| [practice-user-permissions](#practice-user-permissions) | 98 | **1,075** | 1,043 | +32 | new `Cron.UnitTests` (13), `SmokeTests` (3); `Worker.UnitTests` no longer empty (8) |
| [practice-authorization-proxy](#practice-authorization-proxy) | 8 | **31** | 26 | +5 | new `SmokeTests` (5); 3 placeholder `1+1` tests remain |
| [provider-grouping](#provider-grouping) | 45 | **558** | 471 | +87 | growth across Unit/Api/Lambda; `SalesforceAccountBackfillCron` still 0 |
| [provider-join-service](#provider-join-service) | 55 | **642** | 634 | +8 | new `SmokeTests` (4); `SelfSignup.Tests.Unit` still empty |
| [zocdoc_web monolith](selenium-monolith.md) | 27 | **433** | 255 | +178 | `[CiTest]` correction + 14 new files; 535 counting `[TestCase]` rows |
| [sandbox Cypress (Account-User-Setup)](#sandbox-cypress-e2e) | 8 | **71** | 72 | −1 | recount; Playwright migration not started |
| [Frontend — Jest/Vitest unit](frontend.md) | 6 | **20** | 5 | +15 | v2 missed `signUpPortal` unit tests |
| [Frontend — in-app Cypress](frontend.md) | 4 | **151** | 149 | +2 | |
| **TOTAL** | **251** | **2,981** | 2,655 | **+326** | |

Plus 12 Chromatic/Storybook stories (visual regression, not assertions).

## Per-project breakdown

### practice-user-permissions
| Project | Tests |
|---------|-----:|
| PracticeUserPermissions.UnitTests | 380 |
| PracticeUserPermissions.Lambda.UnitTests | 252 |
| PracticeUserPermissions.Web.ApiTests | 207 |
| PracticeUserPermissions.IntegrationTests | 121 |
| PracticeUserPermissions.Web.UnitTests | 78 |
| PracticeUserPermissions.Cron.UnitTests | 13 |
| PracticeUserPermissions.Worker.UnitTests | 8 |
| PracticeUserPermissions.Cron.IntegrationTests | 6 |
| PracticeUserPermissions.Worker.IntegrationTests | 6 |
| PracticeUserPermissions.SmokeTests | 3 |
| PracticeUserPermissions.Lambda.IntegrationTests | 1 |
| TestCommon | 0 (shared helpers) |
| **Total** | **1,075** |

LOC: source 18,168 / test 43,420 → **2.38×**.
Watch items: `Lambda.IntegrationTests` = 1 test for the largest source surface; `PracticeBlockedService` & `AuditLoggingMetadataService` have no direct unit tests; 0 CDK tests.

### practice-authorization-proxy
| Project | Tests |
|---------|-----:|
| UnitTests/Service/AuthorizationServiceTests | 12 |
| Web.ApiTests (Practice 3 + Organization 3) | 6 |
| SmokeTests | 5 |
| Web.UnitTests/ConversionExtensionsTests | 5 |
| UnitTests/ExampleTests (placeholder `1+1`) | 1 |
| IntegrationTests/ExampleTests (placeholder `1+1`) | 1 |
| Web.IntegrationTests/ExampleTests (placeholder `1+1`) | 1 |
| **Total** | **31** |

LOC: source 733 / test 1,094 → **1.49×**. `AuthorizationImpl.cs` (183 LOC) untested; 3 of 31 tests are placeholders; 0 CDK tests.

### provider-grouping
| Project | Tests |
|---------|-----:|
| UnitTests | 217 |
| ApiTests | 184 |
| LambdaTests | 83 |
| IntegrationTests | 72 |
| SmokeTests | 1 |
| Tests.Common | 1 |
| **Total** | **558** |

LOC: source 16,579 / test 17,095 → **1.03×**.
Lambda coverage: MonolithSyncLambda well-covered (23 tests across integration+unit); `StrategicLambda` has 1 active test (1 `[Ignore]`d); `SalesforceAccountBackfillCron` **0 tests**; `DynamicGroupingUpdateExecutor` **0 direct tests**; 0 CDK tests.

### provider-join-service
| Project | Tests |
|---------|-----:|
| SelfSignup.Api.Tests.Unit | 342 |
| SelfSignup.Infrastructure.Tests.Unit | 200 |
| SelfSignup.Integration.Tests | 93 |
| SelfSignup.SmokeTests | 4 |
| ProviderJoinService.AbandonmentLambda.Tests | 3 |
| SelfSignup.Tests.Unit | **0 (empty)** |
| **Total** | **642** |

LOC: source 8,134 / test 11,840 → **1.46×**.
Untested: `StepFunctionService`, `CreatePracticeDtoFactory`, `UpdatesDefinitionFactory`. `AbandonmentLambda` echo-back placeholder. 0 CDK tests.

### Frontend (provider-fe-monorepo) — Pterodactyl-owned UI per CODEOWNERS (@Zocdoc/user-permissions)
| UI area | Jest/Vitest unit | In-app Cypress | Stories |
|---------|-----------------:|---------------:|--------:|
| `apps/settings/src/pages/settingsPages/practiceUsersPage/` | 5 | 68 | 0 |
| `apps/settings/src/pages/settingsPages/practiceSettings/createProviderOrStaffPage/` | **0** | 26 | 2 |
| `apps/provider-home-webapp/src/pages/signUpPortal/` | 15 | 57 | 10 |
| **Total** | **20** | **151** | **12** |

### sandbox Cypress E2E
| Area | Files | Tests |
|------|------:|------:|
| Flows | 6 | 60 |
| Pages | 2 | 11 |
| **Total** | **8** | **71** |

Playwright: **0 specs** (folders scaffolded with `.gitkeep` only). Owner per `OWNERSHIP.md`: Slack `#provider-user-permissions-vibes`, Jira `PTERODACTL`.

## Source-vs-test LOC (backend)

| Repo | Source LOC | Test LOC | Ratio |
|------|----------:|---------:|------:|
| practice-user-permissions | 18,168 | 43,420 | 2.38× |
| practice-authorization-proxy | 733 | 1,094 | 1.49× |
| provider-grouping | 16,579 | 17,095 | 1.03× |
| provider-join-service | 8,134 | 11,840 | 1.46× |
