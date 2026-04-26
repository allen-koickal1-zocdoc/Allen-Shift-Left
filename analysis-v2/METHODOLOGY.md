# Methodology

## Why SHA pinning

`main`/`master` move. Two engineers reading the same audit a month apart will see different code if links resolve to a moving ref. Every link in v2 resolves to a fixed SHA so the report stays internally consistent forever.

The SHA pin table lives in [README.md](README.md).

## Counting tests

### NUnit (C#)

Per-file count:

```bash
grep -cE "^\s*\[Test\]|^\s*\[TestCase\(" <file>
```

Each `[Test]` and each `[TestCase(...)]` attribute occurrence is counted as **one test**, mirroring how NUnit's runner reports them in CI dashboards.

Edge cases not separately accounted for (counted once per occurrence as the leading attribute):

- `[TestCaseSource(...)]` — counted as 1 (the source-driven row count is unknown without runtime info).
- `[Theory]` / `[Combinatorial]` — none in scope.
- `[OneTimeSetUp]`, `[SetUp]`, `[TearDown]` — explicitly **not** matched (regex requires `[Test]` or `[TestCase(`).

Repo total:

```bash
find tests -name "*.cs" -type f -exec grep -hcE "^\s*\[Test\]|^\s*\[TestCase\(" {} +
```

### Cypress

```bash
grep -cE "^\s*it\(" <spec>
```

`it.only`, `it.skip`, `xit(` are not matched and not counted.

## Mapping source → tests

For each `<class>.cs` file in a service's `src/` tree, the audit looked for a sibling test file named `<class>Tests.cs` or `<class>Test.cs` anywhere under `tests/`. If no such file exists **and** `grep -rln "<class>" tests/` returns no hits (or only `Mock<I<class>>` references), the class is recorded as untested in [GAPS.md](GAPS.md).

This rule is conservative — a class can be exercised indirectly through API or integration tests without a dedicated `<class>Tests.cs`. v2 only records a gap when **direct** unit-test coverage is absent.

## Selenium classification (monolith)

A test was classified as Selenium iff:

- the file imports `using OpenQA.Selenium...`, **or**
- the file inherits from a known Selenium fixture (e.g. `BaseSeleniumTest`).

In `zocdoc_web/SeleniumTests/SeleniumTests/Tests/`, none of the 13 in-scope files met either criterion. All inherit from `BaseZocHttpApiTestFixture`. Therefore none are Selenium tests, despite the directory name.

(Note: the monolith was not cloned locally for v2. The classification was performed by a deep-audit subagent inspecting `using` directives and base classes file-by-file. The per-file counts in [selenium-monolith.md](selenium-monolith.md) come from that subagent run.)

## LOC counts

```bash
find <root> -name "*.cs" -type f \
  -not -path "*/obj/*" -not -path "*/bin/*" \
  -exec cat {} + | wc -l
```

Counts physical lines (including blanks and comments), which is sufficient for a test-vs-source ratio.

## What v2 deliberately does **not** claim

- Per-test execution time or flakiness — out of scope.
- Coverage % (line/branch) — would require `coverlet`/`dotnet test` runs.
- Whether each test is meaningful vs a no-op — sampled, not exhaustive. v2 only flagged tests that are obviously trivial (`1 + 1 == 2`, echo-back, `[Ignore]`).
