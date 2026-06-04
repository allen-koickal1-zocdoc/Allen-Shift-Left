# Overall Assessment — Strength & Coverage of the Tests

**Verdict: quantitatively strong, qualitatively good-but-uneven — a solid core with a few sharp edges that sit exactly where the risk is highest. Grade: B (strong-with-sharp-edges).**

> Caveat: counts and test/source LOC ratios are *proxies*. This audit did not run line/branch coverage (`coverlet`/`dotnet test`), so "2,981 tests" reflects effort and breadth, not how many code paths actually execute. Read the assessment below with that framing. See [METHODOLOGY.md](METHODOLOGY.md).

## What's genuinely strong

- **The core authz service is well-tested.** practice-user-permissions: 1,075 tests at a **2.38× test/source LOC ratio**, layered unit → integration → API. A properly invested codebase.
- **The highest-risk domain — FGA/RBAC permission checks — has the heaviest net under it.** 433 HTTP-API tests across 27 monolith files exercise the actual authorization endpoints. For a team whose product *is* the security boundary, concentrating coverage there is the right instinct.
- **Real test pyramids exist** in most repos (unit + integration + API + E2E), not just a single layer.

## Where it's weak — and why it matters

1. **The single most security-critical class is untested.** `AuthorizationImpl` (the primary `IAuthorization` implementation, 183 LOC) has **zero direct unit tests** — exercised only indirectly through API tests. The worst gap by risk-to-effort: coarse, slow coverage on the one component you'd most want branch-pinned. See [GAPS.md](GAPS.md).
2. **Volume masks unevenness.** provider-grouping sits at **1.03×** (barely more test than source) vs PUP's 2.38× — yet POGS feeds the org/group membership that authz decisions depend on. The thin repo is *upstream* of the well-tested one.
3. **A visible tail of scaffolding-never-filled.** 3 `(1+1)` placeholders, an echo-back lambda test, an `[Ignore]`d StrategicLambda, an empty `SelfSignup.Tests.Unit`, `SalesforceAccountBackfillCron` at 0, `createProviderOrStaffPage` at 0 unit tests, and `Lambda.IntegrationTests` = **1 test for 12+ handlers**. Individually minor; collectively a pattern of "harness wired up, tests not written."
4. **Infrastructure is completely unguarded.** **0 CDK tests in all 4 backend repos** despite each shipping a `cdk/jest.config.js`. For this team the infra (IAM, SQS/DLQ, audit-logging stacks, membership-processing lambdas) *is* part of the trust boundary — an untested CDK change can silently widen access.
5. **E2E debt is accruing.** Account-User-Setup is **0% migrated to Playwright** while the org moves off Cypress.

## Bottom line

The breadth is real and the team clearly invests in testing — but the gaps aren't random. They cluster on the highest-consequence surfaces: the core authz implementation, the upstream grouping repo, and infrastructure.

## Prioritized remediation

| # | Action | Effort | Risk guarded |
|---|--------|--------|--------------|
| 1 | Unit-test `AuthorizationImpl` (4 public methods) directly | Low | **High** — core authorization decisions |
| 2 | Add CDK tests across all 4 backend repos (harness already configured) | Low–Med | **High** — IAM/SQS/audit-logging trust boundary |
| 3 | Backfill empty/placeholder projects (`SelfSignup.Tests.Unit`, the 3 `(1+1)` examples, `AbandonmentLambda` echo-back, `StrategicLambda`, `SalesforceAccountBackfillCron`) | Med | Med — removes false confidence |
| 4 | Deepen provider-grouping toward parity with PUP; cover `DynamicGroupingUpdateExecutor` | Med | Med–High — upstream of authz |
| 5 | Add unit tests for `createProviderOrStaffPage`; expand PUP `Lambda.IntegrationTests` beyond 1 test | Med | Med |
| 6 | Finish the Account-User-Setup Cypress → Playwright migration | Med | Low–Med — tech debt |

Items 1 and 2 are small efforts guarding disproportionately large risk — do them first.
