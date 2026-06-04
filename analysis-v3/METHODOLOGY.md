# Methodology (v3)

## Fetching current remote data

The analysis sandbox blocks plain `git clone` (HTTP 567, network policy), but the authenticated `gh` CLI reaches `api.github.com`. Each repo was fetched at its current-HEAD SHA via the tarball endpoint, then extracted:

```bash
gh api repos/Zocdoc/<repo>/tarball/<sha> > t.tar.gz
tar xzf t.tar.gz
```

For the two large repos this is impractical, so they were read through the git-tree + contents API instead:

- **zocdoc_web** (monolith): too large to tar. Navigated `SeleniumTests/SeleniumTests/Tests/` via `gh api .../git/trees/<sha>?recursive=1` (tree was not truncated) and fetched each candidate file with `gh api .../contents/<path>?ref=<sha> --jq .content | base64 -d`.
- **provider-fe-monorepo**: recursive tree fetched once (7,611 entries, not truncated), then the three CODEOWNERS-owned areas filtered locally.

This is genuinely current remote data — the stale local checkouts of the source repos were deliberately **not** used.

## Counting tests

### NUnit (C# backend repos)

```bash
grep -cE "^\s*\[Test\]|^\s*\[TestCase\(" <file>
```

Each `[Test]` and each `[TestCase(...)]` counts as one. `[TestCaseSource]`, `[SetUp]`, `[OneTimeSetUp]`, `[TearDown]` are not matched. Per-project totals were summed with `awk` (macOS `paste -sd+` mishandles the multi-line `grep -hc` output).

### Monolith (zocdoc_web) — the `[CiTest]` fix

The monolith marks tests with Zocdoc's custom **`[CiTest]`** attribute, not NUnit's `[Test]`. v2 missed this entirely. v3 counts:

```bash
grep -cE "^\s*\[CiTest\]|^\s*\[Test\]" <file>     # test methods
grep -cE "^\s*\[TestCase\("            <file>     # parameterized rows (reported separately)
```

Headline = `[CiTest]` + `[Test]` (method count). An alternate total adds `[TestCase]` rows to match how v2 counts NUnit cases. `[TestCaseSource]` rows expand at runtime and are not counted.

### Cypress / Jest / Vitest / Playwright

```bash
grep -cE "^\s*it\("            # Cypress specs
grep -cE "^\s*(it|test)\("     # Jest/Vitest unit, Playwright
```

`it.only`, `it.skip`, `xit(` are not matched. Note: provider-fe-monorepo unit tests use **both** `*-tests.tsx` (settings app) and `*.test.tsx` (provider-home-webapp) conventions — both are searched. v2's miss came from globbing only the hyphen form.

## Mapping source → tests (gap detection)

For a class `Foo`, a gap is recorded only when there is no `FooTests.cs`/`FooTest.cs` **and** `grep -rln "Foo" tests/` returns nothing, or only `Mock<IFoo>` interface references (never the concrete class). Conservative: indirect coverage via API/integration tests does not count as a gap-filler but also is not claimed as direct coverage.

## LOC

```bash
find <root> -name "*.cs" -not -path "*/obj/*" -not -path "*/bin/*" -exec cat {} + | wc -l
```

Physical lines (blanks + comments included) — sufficient for a test/source ratio.

## Out of scope (unchanged from v2)

- Per-test runtime / flakiness.
- Line/branch coverage % (would require `coverlet`/`dotnet test`).
- Whether each test is meaningful — only obvious no-ops (`1+1`, echo-back, `[Ignore]`) were flagged.
- Datadog UI-side synthetic monitors (only synthetics-as-code in-repo were checked — none found).
