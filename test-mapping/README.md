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

| Repo | What it does | Tests |
|------|--------------|-------|
| [auth-service](auth/auth-service-test-mapping.md) | Patient + provider login, OTP, Auth0, refresh tokens, service-to-service auth | 1,172 |
| [zocdoc_web](auth/zocdoc-web-test-mapping.md) *(auth-owned paths only)* | Monolith security, practice authorization, user roles | 188 classes / 2,180 methods |
| [consumer-privacy-service](auth/consumer-privacy-service-test-mapping.md) | CCPA/CPA — access, delete, and opt-out requests | 308 |
| [auth0-infrastructure](auth/auth0-infrastructure-test-mapping.md) | Auth0 Actions that run on every live login, plus the log-stream lambda | 200 |
| [ServiceMockEndpoints](auth/service-mock-endpoints-test-mapping.md) | Mock endpoints other services test against | 99 |
| [user-accounts](auth/user-accounts-test-mapping.md) | Account records and identity lookup | 85 |
| [user-locking](auth/user-locking-test-mapping.md) | Locking accounts out of login and booking | 80 |
| [audit-logging-service](auth/audit-logging-service-test-mapping.md) | Authorization + permission-change audit logs → S3 → legal reporting | 56 |
| [legal-agreement](auth/legal-agreement-test-mapping.md) | Practice User Agreement signatures | 52 |
| [sandbox](auth/sandbox-test-mapping.md) | Browser (Playwright) tests for sign-in, password reset, sign-up | 24 |
| [external-developer-api-auth](auth/external-developer-api-auth-test-mapping.md) | Partner Auth0 app-client roster | 4 |

Two things to know about the numbers. Counts are **distinct test methods**, not `[TestCase]` attributes — a parametrized test counts once, and that's why some figures are lower than a naive grep suggests. And `zocdoc_web` is mapped one row per **class** rather than per method: at 2,180 methods a per-method table would be unreadable.

## How scope was decided

Mappings cover whole repos, except `zocdoc_web` (only the auth-owned paths) and `sandbox` (only `playwright/BU/Infrastructure/Auth`). Ownership came from each repo's `plinth.yaml`, from `CODEOWNERS` for monolith paths, and from `OWNERSHIP.md` for the browser tests.

This repo list is targeted, not exhaustive — it was built by searching for the Auth team in config files, because the GitHub teams API isn't reachable with the token available here. A repo the team owns but never labelled could be missing.

## Dashboard

[dashboard.html](dashboard.html) — per-repo and per-file breakdowns, a treemap of where tests live, and a searchable index of all 2,268 rows. Clone the repo and open it in a browser; GitHub won't render it inline.

Version history: [CHANGELOG.md](CHANGELOG.md).
