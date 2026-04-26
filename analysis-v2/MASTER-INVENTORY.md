# Master Test Inventory (v2)

All counts produced by:

```
grep -cE "^\s*\[Test\]|^\s*\[TestCase\(" <file>     # NUnit
grep -cE "^\s*it\("                                   # Cypress
```

…run against each repo at the SHA pinned in [README.md](README.md).

## Per-repo summary

| Repo | Test Files | Tests (v2) | v1 Claim | Delta | Notes |
|------|-----------:|-----------:|---------:|------:|-------|
| [practice-user-permissions](practice-user-permissions.md) | 94 | **1,043** | ~870 | **+173** | v1 round-numbered and missed several files |
| [practice-authorization-proxy](practice-authorization-proxy.md) | 7 | **26** | 30 | -4 | 3 of the 26 are `1+1 == 2` placeholders |
| [provider-grouping](provider-grouping.md) | 36 | **471** | ~200 | **+271** | v1 was off by more than 2x |
| [provider-join-service](provider-join-service.md) | 54 | **634** | (broad) | n/a | v1 had no aggregate; 5 projects, one empty |
| [zocdoc_web monolith ("Selenium")](selenium-monolith.md) | 13 | **255** | 89+ | **+166** | None are actual Selenium tests |
| [Cypress E2E (Account-User-Setup)](cypress-e2e.md) | 9 | **72** | ~70 | +2 | Counts `it(` only, not `describe(` |
| [Frontend Pterodactyl UI (provider-fe-monorepo)](frontend-users-page.md) | 5 | **128** | 0 | **+128** | **CORRECTED 2026-04-27**: 5 Jest unit + 123 in-app Cypress (was missed by wrong grep) |
| **TOTAL** | **218** | **2,629** | — | — | |

## Per-project breakdown

### practice-user-permissions
| Project | Tests |
|---------|-----:|
| PracticeUserPermissions.UnitTests | 380 |
| PracticeUserPermissions.Lambda.UnitTests | 269 |
| PracticeUserPermissions.Web.ApiTests | 209 |
| PracticeUserPermissions.IntegrationTests | 117 |
| PracticeUserPermissions.Web.UnitTests | 64 |
| PracticeUserPermissions.Worker.IntegrationTests | 2 |
| PracticeUserPermissions.Cron.IntegrationTests | 1 |
| PracticeUserPermissions.Lambda.IntegrationTests | 1 |
| PracticeUserPermissions.Worker.UnitTests | **0 (empty)** |
| TestCommon | 0 |
| **Total** | **1,043** |

### practice-authorization-proxy
| Project | Tests |
|---------|-----:|
| PracticeAuthorizationProxy.UnitTests/Service/AuthorizationServiceTests | 12 |
| PracticeAuthorizationProxy.Web.UnitTests/ConversionExtensionsTests | 5 |
| PracticeAuthorizationProxy.Web.ApiTests/PracticeAuthorizationTests | 3 |
| PracticeAuthorizationProxy.Web.ApiTests/OrganizationAuthorizationTests | 3 |
| PracticeAuthorizationProxy.UnitTests/ExampleTests (placeholder `1+1==2`) | 1 |
| PracticeAuthorizationProxy.IntegrationTests/ExampleTests (placeholder `1+1==2`) | 1 |
| PracticeAuthorizationProxy.Web.IntegrationTests/ExampleTests (placeholder `1+1==2`) | 1 |
| **Total** | **26** |

### provider-grouping
| Project | Tests |
|---------|-----:|
| ApiTests | 176 |
| UnitTests | 176 |
| IntegrationTests | 60 |
| LambdaTests | 58 |
| Tests.Common | 1 |
| **Total** | **471** |

### provider-join-service
| Project | Tests |
|---------|-----:|
| SelfSignup.Api.Tests.Unit | 342 |
| SelfSignup.Infrastructure.Tests.Unit | 196 |
| SelfSignup.Integration.Tests | 93 |
| ProviderJoinService.AbandonmentLambda.Tests | 3 |
| SelfSignup.Tests.Unit | **0 (empty)** |
| **Total** | **634** |

### Frontend (provider-fe-monorepo) — Pterodactyl-owned UI per CODEOWNERS

| UI area | Jest unit | In-app Cypress | Chromatic stories |
|---------|----------:|---------------:|------------------:|
| `apps/settings/src/pages/settingsPages/practiceUsersPage/` | 5 | 68 | 2 |
| `apps/settings/src/pages/settingsPages/practiceSettings/createProviderOrStaffPage/` | 0 | 0 (or in shared `SettingsPages/` cypress folder, unverified) | 2 |
| `apps/provider-home-webapp/src/pages/signUpPortal/` | 0 | 55 | 9 |
| **Total** | **5** | **123** | **13** |

**Critical gaps absent from earlier v2:** CDK/infrastructure tests, Datadog Synthetics as code, contract/Pact, Verify snapshot, mutation tests, accessibility tests. See [MISSED-TEST-SURFACES.md](MISSED-TEST-SURFACES.md).

## Source-vs-test LOC

| Repo | Source LOC | Test LOC | Test/Source ratio |
|------|----------:|---------:|------------------:|
| practice-user-permissions | 17,958 | 43,603 | 2.43x |
| practice-authorization-proxy | 733 | 858 | 1.17x |
| provider-grouping | 15,016 | 14,282 | 0.95x |
| provider-join-service | 8,115 | 11,563 | 1.42x |

(Counts produced by `find … -name "*.cs" -not -path "*/obj/*" -not -path "*/bin/*" -exec cat {} + | wc -l`.)
