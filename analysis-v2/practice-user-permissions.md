# practice-user-permissions

SHA: `0fc641daa80e827bf13a5b95edbf2574f0fd6d42`
Repo: [Zocdoc/practice-user-permissions](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42)

## Headline

| | |
|--|--|
| Test files (with at least one `[Test]` or `[TestCase(`) | **94** |
| Total tests | **1,043** |
| Source LOC | 17,958 |
| Test LOC | 43,603 |
| Test/Source ratio | **2.43x** |
| `[Ignore]` / `[Explicit]` attributes | 0 |

## Tests by project

| Project | Tests |
|---------|-----:|
| `PracticeUserPermissions.UnitTests` | 380 |
| `PracticeUserPermissions.Lambda.UnitTests` | 269 |
| `PracticeUserPermissions.Web.ApiTests` | 209 |
| `PracticeUserPermissions.IntegrationTests` | 117 |
| `PracticeUserPermissions.Web.UnitTests` | 64 |
| `PracticeUserPermissions.Worker.IntegrationTests` | 2 |
| `PracticeUserPermissions.Cron.IntegrationTests` | 1 |
| `PracticeUserPermissions.Lambda.IntegrationTests` | 1 |
| `PracticeUserPermissions.Worker.UnitTests` | 0 (empty) |
| `TestCommon` | 0 |
| **Total** | **1,043** |

## Most-loaded test files

| File | Tests |
|------|-----:|
| [tests/PracticeUserPermissions.Web.ApiTests/UserRolesApiTests.cs](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Web.ApiTests/UserRolesApiTests.cs) | 122 |
| [tests/PracticeUserPermissions.UnitTests/Services/TupleAuditServiceTests.cs](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.UnitTests/Services/TupleAuditServiceTests.cs) | 70 |

(Per-file numbers for the other 92 files are produced verbatim by the same `grep -cE "^\s*\[Test\]\|^\s*\[TestCase\("` invocation; the totals reconcile to 1,043.)

## v1 corrections

| v1 said | v2 verified |
|---------|-------------|
| ~870 tests | **1,043** |
| `TupleAuditServiceTests` 61 tests | **70** |
| `UserRolesApiTests` 123 tests | **122** |
| `BatchGetEntityDirectUsersCount` has no API tests | **REFUTED** — 11 tests in [`UserRolesApiTests.cs#L4335`](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Web.ApiTests/UserRolesApiTests.cs#L4335) `#region BatchGetEntityDirectUsersCount` (lines 4361–4706) |
| 94 test files | **CONFIRMED** |

## Untested service classes (verified in v2)

| Class | Source link |
|-------|-------------|
| `PracticeBlockedService` | [src/PracticeUserPermissions/Service/PracticeBlockedService.cs](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/src/PracticeUserPermissions/Service/PracticeBlockedService.cs) |
| `AuditLoggingMetadataService` | [src/PracticeUserPermissions/Service/AuditLoggingMetadataService.cs](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/src/PracticeUserPermissions/Service/AuditLoggingMetadataService.cs) |
| `DlqRedriveSettings` (config-only class, no unit test) | [src/PracticeUserPermissions/Service/DlqRedriveSettings.cs](https://github.com/Zocdoc/practice-user-permissions/blob/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/src/PracticeUserPermissions/Service/DlqRedriveSettings.cs) |

Search method: for each `*.cs` in `src/PracticeUserPermissions/Service/`, looked for a matching `${name}Tests.cs` anywhere in `tests/`.

## Empty test project

[tests/PracticeUserPermissions.Worker.UnitTests/](https://github.com/Zocdoc/practice-user-permissions/tree/0fc641daa80e827bf13a5b95edbf2574f0fd6d42/tests/PracticeUserPermissions.Worker.UnitTests) — contains only `AssemblyInfo.cs`, `BUILD`, `PracticeUserPermissions.Worker.UnitTests.csproj`. Companion `Worker.IntegrationTests` project has 2 tests.
