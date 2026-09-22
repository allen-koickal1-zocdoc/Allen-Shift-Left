# Test Mappings

**What this is:** a written inventory of every automated test the Infrastructure / Auth team owns — 2,268 tests across 11 repos. One table row per test, saying what it checks and what it deliberately leaves out.

**Who it's for:** anyone who needs to answer "is this already tested?" without reading the test code. Each row links straight to the test's source line.

**How to read a row:**

| Column | Means |
|--------|-------|
| **Test / Test Class** | The test's real name, so you can search for it in the repo |
| **What It Verifies** | The behavior the test proves, in one sentence |
| **Steps** | What the test actually does, in order |
| **Not Covered** | Behavior a reader might assume this test checks, but it doesn't |
| **Type** | Unit, Integration, API, or E2E — how much of the stack runs |
| **Source** | Link to the exact line, pinned to a commit so it never rots |

The **Not Covered** column is the point of the whole exercise: a row that looks covered often isn't covered the way you'd assume.

## The mappings

Slack `#auth` · Jira `AUTH` · `technology-auth@zocdoc.com` · QA owner Allen K.

| Mapping | Source | Tests | Granularity | Status |
|---------|--------|-------|-------------|--------|
| [sandbox-test-mapping.md](auth/sandbox-test-mapping.md) | `Zocdoc/sandbox` · `playwright/BU/Infrastructure/Auth` | 6 files / 24 tests | per test | Done |
| [legal-agreement-test-mapping.md](auth/legal-agreement-test-mapping.md) | `Zocdoc/legal-agreement` | 8 files / 52 tests | per method | Done |
| [audit-logging-service-test-mapping.md](auth/audit-logging-service-test-mapping.md) | `Zocdoc/audit-logging-service` | 17 files / 56 tests | per method | Done |
| [auth0-infrastructure](auth/auth0-infrastructure-test-mapping.md) | `Zocdoc/auth0-infrastructure` @ `cac1149` | 57 C# + 143 JS tests | per method | Done |
| [user-locking-test-mapping.md](auth/user-locking-test-mapping.md) | `Zocdoc/user-locking` | 8 files / 80 tests | per method | Done |
| [user-accounts](auth/user-accounts-test-mapping.md) | `Zocdoc/user-accounts` @ `0271f52` | 85 tests | per method | Done |
| [ServiceMockEndpoints](auth/service-mock-endpoints-test-mapping.md) | `Zocdoc/ServiceMockEndpoints` @ `90eacfb` | 99 tests | per method | Done |
| [consumer-privacy-service](auth/consumer-privacy-service-test-mapping.md) | `Zocdoc/consumer-privacy-service` @ `91dad97` | 308 tests | per method | Done |
| [auth-service](auth/auth-service-test-mapping.md) | `Zocdoc/auth-service` @ `fa9a039` | 1172 tests | per method | Done |
| [external-developer-api-auth-test-mapping.md](auth/external-developer-api-auth-test-mapping.md) | `Zocdoc/external-developer-api-auth` | 1 file / 4 tests | per test | Done |
| [zocdoc_web (auth-owned paths)](auth/zocdoc-web-test-mapping.md) | `Zocdoc/zocdoc_web` @ `eed912c` · `ZocDoc.Security`, `PracticeAuthorization`, `Apis/PracticeUserRolesPrivate` | 188 test classes / 2,180 methods | per class | Done |

**Coverage gaps:** [auth/GAPS.md](auth/GAPS.md) — 220 proposed tests derived by diffing these mappings against each repo's production surface at HEAD. Includes verified corrections to the mapping rows themselves.

Repo ownership was resolved by code search for `team: auth` / `technology-auth@zocdoc.com` in `plinth.yaml`, cross-checked against the org `team-directory.yaml`. The GitHub teams API is not reachable with the available token, so this list is targeted rather than exhaustively enumerated.

Version history: [CHANGELOG.md](CHANGELOG.md).
