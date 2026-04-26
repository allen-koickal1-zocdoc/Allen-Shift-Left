# Pterodactyl Test Coverage — In Plain English

For non-engineers (or engineers who just want the gist before diving in).

## What is this?

Pterodactyl (officially: **Provider Account & User Setup**) is the team that builds the parts of Zocdoc that decide *who can log in to a practice account, what they can see, and what they can do*. Think: when an office manager invites a receptionist, when a provider signs up for the first time, when an admin grants someone access to billing — that's Pterodactyl.

Like any team, we have automated tests that run before code ships. This audit asks: **how good is our safety net? Where could a bug slip through?**

## What does Pterodactyl own?

Six pieces of code (called "repos"):

| Repo | What it does | Think of it as... |
|------|--------------|-------------------|
| `practice-user-permissions` | The main brain for "who has what permission" | The lock-and-key system |
| `practice-authorization-proxy` | A thin layer that other services call to ask "is this user allowed?" | The bouncer at the door |
| `provider-grouping` | Groups practices into bigger organizations | The HR org chart |
| `provider-join-service` | The flow when a new provider signs up | The application form for joining Zocdoc |
| `zocdoc_web` (parts of) | The older monolith server-side authorization | The legacy filing cabinet |
| `provider-fe-monorepo` (parts of) | The actual screens users see (Users Page, Sign-Up Portal) | The buttons users click |

## How do we test today, in plain words?

There are several "kinds" of tests, each catching different bugs:

| Kind | What it does | Plain analogy |
|------|--------------|--------------|
| **Unit tests** | Tests one tiny piece of code in isolation | Checking each LEGO brick is the right shape |
| **Integration tests** | Tests several pieces talking to each other | Checking two LEGO bricks click together |
| **API/HTTP tests** | Tests a server endpoint end-to-end | Pressing a doorbell and checking the bell rings |
| **End-to-end (E2E) tests / Cypress** | Tests by driving a real browser through real screens | Pretending to be a user and clicking through |
| **Storybook + Chromatic** | Snapshots of UI components for visual diff | Yearbook photos: catches "did the button move?" |
| **CDK tests** | Tests our cloud infrastructure config | Checking the blueprints before we pour concrete |
| **Datadog Synthetics** | Real-traffic checks running 24/7 in production | Smoke detectors that beep when something's wrong |

## Current state — the headline

We counted **2,629 tests across 218 files** that protect Pterodactyl-owned code. That sounds like a lot, but **the protection is uneven**.

### Where we're strong ✓

- **practice-user-permissions** is heavily tested — 1,043 backend tests covering the core permission engine.
- **provider-grouping** has solid unit + API coverage — 471 tests.
- **provider-join-service** has comprehensive coverage of the sign-up logic — 634 tests.
- **The Users Page screen** has 68 in-app Cypress browser tests — clicking through real flows.
- **The Sign-Up Portal screen** has 55 in-app Cypress browser tests.

### Where we're shaky ⚠️

| Gap | Why it matters | What's there today |
|-----|----------------|--------------------|
| **CDK infrastructure tests = 0 across all 4 backend repos** | When we change Lambda configs, IAM policies, S3 bucket settings, autoscaling — nothing automatically verifies it. | The Jest config files exist but the `test/` folders are empty. |
| **PUP Cron has 1 integration test** | The cron runs **4x a day** to backfill org permissions. If it breaks, permissions go stale silently. | One integration test. |
| **PUP Lambda has 1 integration test for 12 Lambdas** | Lambdas handle real-time permission updates from DynamoDB streams. | One integration test for the entire fleet. |
| **PUP Worker.UnitTests project is literally empty** | The worker auto-audits FGA permission tuples. | Zero tests. |
| **SelfSignup.Tests.Unit is empty** | Top-level test project exists, has no content. | Zero tests. |
| **AuthorizationImpl in proxy = 0 unit tests** | A 183-line C# class that's the "bouncer at the door" — covered only by API tests, not isolated unit tests. | Only HTTP tests. |
| **StepFunctionService = 0 tests** | Drives the multi-step provider sign-up workflow. | Zero direct tests, mocked elsewhere. |
| **CreatePracticeDtoFactory = 0 tests** | Maps user inputs into the practice creation request — includes phone-number formatting logic. | Zero tests. |
| **MonolithSyncLambda untested in v1, modestly covered now** | Syncs grouping data into the legacy monolith. | 23 tests (good: v1 was wrong about this). |
| **Provider-grouping Cron has no dedicated test project** | The salesforce sync cron runs every 5 minutes. | Covered only via Unit tests. |
| **Frontend Jest unit tests = 5 total for Pterodactyl** | Critical "create user", "delete user", "change role" UI flows have one shallow test each. | 5 tests (was wrongly reported as 0). |
| **createProviderOrStaffPage UI = 0 unit tests** | Where admins create new staff/providers. Only Storybook stories exist. | 0 unit tests, 2 Chromatic stories. |
| **Datadog Synthetics in code = none** | Synthetics catch production breakage *before* a user complains. They might exist in the Datadog UI directly — needs human verification. | Cannot verify without logging into Datadog. |
| **No load tests, no contract tests, no mutation tests, no accessibility tests** | These would catch performance regressions, cross-service breakage, "is the test even meaningful?" gaps, and a11y issues. | None exist anywhere. |

### Where we're flat-out wrong about labeling

| Misnomer | Reality |
|----------|---------|
| The `SeleniumTests/SeleniumTests/Tests/` folder in the monolith | These are **NOT Selenium browser tests**. They're HTTP API tests. There are 255 of them, none drive a browser. The folder name has misled the team for years. |
| v1's "89+ Selenium tests" | Off by 3x: actual is 255 HTTP tests, 0 browser tests. |
| v1's "frontend-monorepo" | The actual repo is `provider-fe-monorepo`. |

## What we found that v1 missed entirely

- **3 FGA test files** in the monolith (43 tests).
- **In-app Cypress** in the frontend monorepo (123 tests).
- **Storybook stories under Chromatic** for our owned UI (13 files).
- **Per-project test breakdowns** that show Cron/Lambda/Worker integration coverage is near-zero.
- **CDK infrastructure tests are 0 in every backend repo.**

## What "good enough" looks like (a practical bar)

Not aiming for 100% coverage. Aiming for: **every code path that, if it broke in prod, would page someone — has at least one direct test.**

Here's a target by layer:

| Layer | Today | Pragmatic target | Why |
|-------|------:|-----------------:|-----|
| Unit (per service class) | mixed | every public method has ≥1 unit test | catches dumb regressions in seconds |
| Integration (LocalStack/DDB local) | sparse for Cron/Lambda/Worker | every Cron, every Lambda handler, every Worker has ≥1 integration test | catches AWS/wiring bugs |
| API/HTTP | strong | maintain | catches contract bugs |
| Frontend Jest | 5 tests | every Pterodactyl-owned `__tests__/` folder has ≥1 component test for each top-level screen | catches React render bugs |
| In-app Cypress | 123 | maintain | catches real-user flow regressions |
| CDK infrastructure | 0 | each Stack class has ≥1 snapshot test | catches IAM/policy mistakes before deploy |
| Datadog Synthetics | unknown | at least 1 sign-up portal flow + 1 user-management flow | catches prod breakage in minutes, not days |

## The 7 things to fix first (priority order)

1. **Add CDK snapshot tests in all 4 backend repos.** Each `*Stack.ts` file gets one snapshot test. Catches IAM/security misconfigurations before deploy. Probably ~1 day of work for the first repo, then templatable.
2. **Add 1 unit test per Pterodactyl-owned UI screen** (Users Page, Sign-Up Portal, Create Provider/Staff). At least bring each above zero with a smoke render test.
3. **Add `StepFunctionService` and `CreatePracticeDtoFactory` direct unit tests** in `provider-join-service`. These are the two "glue services" with no direct coverage today.
4. **Add `AuthorizationImpl` unit tests** in `practice-authorization-proxy`. The "bouncer" deserves more than just HTTP coverage.
5. **Verify or build Datadog Synthetics for the Sign-Up Portal and Users Page.** Log into Datadog → Synthetics → filter by `team:user-permissions`. If none exist, build one for each.
6. **Backfill PUP Cron/Lambda/Worker integration tests.** Today: 1 + 1 + 0 + 2 across these projects. Bring each above 5.
7. **Replace the 3 placeholder `1+1==2` tests in `practice-authorization-proxy`** with real coverage of the corresponding endpoints.

## What this audit does NOT cover

- **Whether the existing tests are well-written.** A test that always passes regardless of behavior is worse than no test. Coverage % doesn't measure quality. Mutation testing (Stryker.NET) would help here — and we have none.
- **Whether tests are flaky.** That's a Cypress Dashboard / TeamCity question. Different audit.
- **PR-level coverage gates.** Is the team requiring tests on new code? Out of scope here; would need to inspect CI configs in zd-cdk.

## Where to go next (concrete)

1. Read [MISSED-TEST-SURFACES.md](MISSED-TEST-SURFACES.md) — full per-project breakdown.
2. Read [GAPS.md](GAPS.md) — verified gaps with line links.
3. Pick one item from "The 7 things to fix first" above, file it as a Jira ticket, ship the fix.
4. After 30 days, re-run the audit (`grep -cE "^\s*\[Test\]|^\s*\[TestCase\("` is the basic primitive; SHAs change, methodology in [METHODOLOGY.md](METHODOLOGY.md) is reusable).

---

*Generated 2026-04-27 by Allen via Claude. Every number above is backed by a grep result against a SHA-pinned repo — see other v2 reports for the per-claim evidence.*
