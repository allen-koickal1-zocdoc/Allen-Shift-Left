# provider-grouping

SHA: `d0bea39cc248a677df3e27faef314f1d3201b412`
Repo: [Zocdoc/provider-grouping](https://github.com/Zocdoc/provider-grouping/tree/d0bea39cc248a677df3e27faef314f1d3201b412)

## Headline

| | |
|--|--|
| Test files (with at least one `[Test]` or `[TestCase(`) | **36** |
| Total tests | **471** |
| Source LOC | 15,016 |
| Test LOC | 14,282 |
| Test/Source ratio | 0.95x |
| `[Ignore(...)]` attributes | 2 (one real test ignored; one `TestDataSeeding` utility) |

## Tests by project

| Project | Tests |
|---------|-----:|
| `ApiTests` | 176 |
| `UnitTests` | 176 |
| `IntegrationTests` | 60 |
| `LambdaTests` | 58 |
| `Tests.Common` | 1 |
| **Total** | **471** |

## Per-file inventory (all 36 files)

### ApiTests (176)
| File | Tests |
|------|-----:|
| [tests/ApiTests/OrganizationControllerTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/ApiTests/OrganizationControllerTests.cs) | 104 |
| [tests/ApiTests/GroupControllerTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/ApiTests/GroupControllerTests.cs) | 56 |
| [tests/ApiTests/GroupRuleControllerTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/ApiTests/GroupRuleControllerTests.cs) | 16 |

### UnitTests (176)
| File | Tests |
|------|-----:|
| [tests/UnitTests/Services/OrganizationServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/OrganizationServiceTests.cs) | 60 |
| [tests/UnitTests/Services/RuleServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/RuleServiceTests.cs) | 20 |
| [tests/UnitTests/Services/OrganizationGraphValidationServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/OrganizationGraphValidationServiceTests.cs) | 17 |
| [tests/UnitTests/Model/DtoTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Model/DtoTests.cs) | 16 |
| [tests/UnitTests/Services/StrategicBackfillWorkerTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/StrategicBackfillWorkerTests.cs) | 9 |
| [tests/UnitTests/Services/GroupSyncServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/GroupSyncServiceTests.cs) | 9 |
| [tests/UnitTests/Utils/EntityIdUtilsTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Utils/EntityIdUtilsTests.cs) | 7 |
| [tests/UnitTests/Services/GroupServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/GroupServiceTests.cs) | 6 |
| [tests/UnitTests/Controllers/DeleteOrganizationImplTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Controllers/DeleteOrganizationImplTests.cs) | 6 |
| [tests/UnitTests/Services/StrategicManagementApiClientTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/StrategicManagementApiClientTests.cs) | 4 |
| [tests/UnitTests/Services/OrganizationSyncServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/OrganizationSyncServiceTests.cs) | 4 |
| [tests/UnitTests/Services/SnsServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/SnsServiceTests.cs) | 4 |
| [tests/UnitTests/Services/OrganizationHierarchyServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/OrganizationHierarchyServiceTests.cs) | 4 |
| [tests/UnitTests/Model/WebDtoTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Model/WebDtoTests.cs) | 4 |
| [tests/UnitTests/Services/OrganizationEntityServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/OrganizationEntityServiceTests.cs) | 3 |
| [tests/UnitTests/Model/OrganizationTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Model/OrganizationTests.cs) | 1 |
| [tests/UnitTests/Services/JitterbitServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/JitterbitServiceTests.cs) | 1 |
| [tests/UnitTests/Services/KinesisNotificationServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/UnitTests/Services/KinesisNotificationServiceTests.cs) | 1 |

### IntegrationTests (60)
| File | Tests |
|------|-----:|
| [tests/IntegrationTests/OrganizationPersistenceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/IntegrationTests/OrganizationPersistenceTests.cs) | 23 |
| [tests/IntegrationTests/MonolithSyncLambdaHandlerTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/IntegrationTests/MonolithSyncLambdaHandlerTests.cs) | 14 |
| [tests/IntegrationTests/GroupPersistenceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/IntegrationTests/GroupPersistenceTests.cs) | 10 |
| [tests/IntegrationTests/OrganizationSyncServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/IntegrationTests/OrganizationSyncServiceTests.cs) | 9 |
| [tests/IntegrationTests/MembershipValidatorExecutorTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/IntegrationTests/MembershipValidatorExecutorTests.cs) | 2 |
| [tests/IntegrationTests/StrategicLambdaHandlerTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/IntegrationTests/StrategicLambdaHandlerTests.cs) | 1 |
| [tests/IntegrationTests/AuditLoggingMetadataServiceTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/IntegrationTests/AuditLoggingMetadataServiceTests.cs) | 1 |

### LambdaTests (58)
| File | Tests |
|------|-----:|
| [tests/LambdaTests/Lambdas/MetadataChangeProcessorTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests/Lambdas/MetadataChangeProcessorTests.cs) | 22 |
| [tests/LambdaTests/Lambdas/MembershipChangeProcessorTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests/Lambdas/MembershipChangeProcessorTests.cs) | 10 |
| [tests/LambdaTests/Lambdas/MonolithSyncLambdaHandlerTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests/Lambdas/MonolithSyncLambdaHandlerTests.cs) | 9 |
| [tests/LambdaTests/Lambdas/ChangeStreamLambdaTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests/Lambdas/ChangeStreamLambdaTests.cs) | 8 |
| [tests/LambdaTests/Lambdas/ReferenceDataChangeLambdaTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests/Lambdas/ReferenceDataChangeLambdaTests.cs) | 4 |
| [tests/LambdaTests/Lambdas/GroupUpdateLambdaTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests/Lambdas/GroupUpdateLambdaTests.cs) | 3 |
| [tests/LambdaTests/Lambdas/StrategicLambdaTests.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests/Lambdas/StrategicLambdaTests.cs) | 2 (1 of which is `[Ignore]` at [L56](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests/Lambdas/StrategicLambdaTests.cs#L56)) |

### Tests.Common (1)
| File | Tests |
|------|-----:|
| [tests/Tests.Common/TestDataSeeding.cs](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/Tests.Common/TestDataSeeding.cs) | 1 (utility, `[Ignore]` — only run manually) |

## v1 corrections

| v1 said | v2 verified |
|---------|-------------|
| ~200 total tests | **471** |
| `MonolithSyncLambda` has zero tests | **REFUTED** — 23 tests across 2 files |
| `StrategicLambdaTests` is `[Ignore("Test Not Completed")]` | CONFIRMED at [L56](https://github.com/Zocdoc/provider-grouping/blob/d0bea39cc248a677df3e27faef314f1d3201b412/tests/LambdaTests/Lambdas/StrategicLambdaTests.cs#L56) |
| `DynamicGroupingUpdateExecutor` no unit tests | CONFIRMED — see [GAPS.md](GAPS.md) |
