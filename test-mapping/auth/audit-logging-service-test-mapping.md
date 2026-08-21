# audit-logging-service - Unit/Integration/API Test Mapping

<!-- test-mapping-meta
repo: Zocdoc/audit-logging-service
branch: main
commit: 2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242
generated: 2026-08-21
test-type: unit
scope: whole repo (owner team `auth` per plinth.yaml)
granularity: one row per test method
-->
> Source: Zocdoc/audit-logging-service @ `2d5e6ad` · branch `main` · generated 2026-08-21

**Team:** Infrastructure / Auth · **Coverage:** 17 files · 56 test methods (11 declared `TestCase`/`TestCaseSource` cases across 6 of them).
**Service:** accepts authorization- and permission-change audit logs over HTTP, flattens them, and writes them to Kinesis Firehose → S3; a lambda then parses those S3 files into a DynamoDB legal-reporting table of unique patients, which a worker keeps refreshed.

---

## tests/ApiTests/AuthorizationLogApiTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 1 | AuthorizationLogApiTests.VerifyPostAuthorizationLogs | `POST /audit-logging/v1/authorization-log` accepts a valid batch and echoes a per-record response. | POST the request with the service header -> Assert the `LogResponseDto` is equivalent to expected, with strict ordering on `Records` | Verifies the authorization-log endpoint's happy path and response ordering. | In: response shape and record order. Out: what actually lands in Firehose (covered by the integration test). | [L31](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/ApiTests/AuthorizationLogApiTests.cs#L31) |
| 2 | AuthorizationLogApiTests.VerifyPostAuthorizationLogsGeneratesIds | Every accepted record comes back with a generated `LogEventGuid` and no error. | POST a two-log batch -> Assert `FailedPutCount` is 0 -> Assert `Records.Count` is 2 -> For each record assert `ErrorMessage` is null and `LogEventGuid` is not null | Verifies server-side id generation per log record. | In: id presence per record. Out: id uniqueness/format. | [L71](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/ApiTests/AuthorizationLogApiTests.cs#L71) |
| 3 | AuthorizationLogApiTests.VerifyPostAuthorizationRejectsLogsWithOffsets | Timestamps carrying a non-zero UTC offset are rejected with a specific validation body. | POST a log whose datetime has a non-zero offset -> Assert 400 -> Assert body is `{"message":"Datetimes should have only zero offsets", ...}` | Verifies the zero-offset timestamp contract at the API boundary. | In: 400 body text. Out: which field paths appear in `errors`. | [L96](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/ApiTests/AuthorizationLogApiTests.cs#L96) |
| 4 | AuthorizationLogApiTests.VerifyPostAuthorizationRejectsMissingServiceHeader | A request without the calling-service header is rejected. | POST without the service header -> Assert 400 | Verifies the service header is mandatory on authorization logs. | In: presence check. Out: header name assertion / 401-vs-400 semantics. | [L113](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/ApiTests/AuthorizationLogApiTests.cs#L113) |
| 5 | AuthorizationLogApiTests.PermissionChangeLogs_Success | `POST /audit-logging/v1/permission-change-log` accepts a valid batch. | POST the permission-change request with the service header -> Assert the response is equivalent to expected, strict ordering on `Records` | Verifies the permission-change endpoint's happy path. | In: response shape and order. Out: downstream Firehose stream selection. | [L126](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/ApiTests/AuthorizationLogApiTests.cs#L126) |
| 6 | AuthorizationLogApiTests.PermissionChangeLog_RejectsLogsWithOffsets | The zero-offset rule applies to permission-change logs too. | POST a permission-change log with a non-zero offset -> Assert 400 -> Assert the same zero-offset message body | Verifies validation parity between the two endpoints. | In: 400 body text. Out: per-field error detail. | [L166](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/ApiTests/AuthorizationLogApiTests.cs#L166) |
| 7 | AuthorizationLogApiTests.PermissionChangeLog_RejectsMissingServiceHeader | The service header is mandatory on permission-change logs too. | POST without the service header -> Assert 400 | Verifies header parity between the two endpoints. | In: presence check. Out: header name assertion. | [L183](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/ApiTests/AuthorizationLogApiTests.cs#L183) |

---

## tests/IntegrationTests/FirehoseClientWrapperIntegrationTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 8 | FirehoseClientWrapperIntegrationTests.SaveLogsTest | Logs written through the Firehose wrapper actually land in S3 with the expected serialized content. | Call `SaveLogs(logs, "serviceName")` against the local Firehose/S3 stack -> Assert the response matches expected with strict record ordering -> Read the S3 object -> Assert its content equals the expected payload | Verifies the real Firehose → S3 delivery path end to end. | In: serialized S3 content and response. Out: partition/prefix scheme, retry on partial failure. | [L62](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/IntegrationTests/FirehoseClientWrapperIntegrationTests.cs#L62) |

---

## tests/IntegrationTests/PatientWorkerIntegrationTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 9 | PatientWorkerIntegrationTests.TestWorker | The patient-refresh worker runs a full scan-and-update cycle against real DynamoDB. | Seed patients -> `await _worker.StartAsync(CancellationToken)` -> assert the resulting Dynamo state | Verifies the worker's baseline single-pass execution. | In: happy-path worker run. Out: scheduling/host lifecycle. | [L46](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/IntegrationTests/PatientWorkerIntegrationTests.cs#L46) |
| 10 | PatientWorkerIntegrationTests.TestWorkerMultipleScansToComplete | A run too large for one scan checkpoints a scan key, and a second run resumes and finishes it. | Start the worker -> Assert the persisted scan key is not null -> Start the worker again -> `BatchGetPatientsAsync(urnPairs)` -> Assert all expected patients present with UTC subjects -> Assert the final scan key is null | Verifies scan checkpoint/resume across worker runs. | In: checkpoint persistence and clearing. Out: behavior if the checkpoint is corrupt. | [L142](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/IntegrationTests/PatientWorkerIntegrationTests.cs#L142) |
| 11 | PatientWorkerIntegrationTests.TestWorkerWithErrorInOneNamespace | A failure in one patient namespace does not block updates in the others. | Arrange ZVS, Insurance, and External-API patients with the external API failing -> Start the worker -> Assert ZVS and Insurance patients advanced to `v00001` with correct ids -> Assert the External-API patient is still at `v00000` | Verifies per-namespace fault isolation in the refresh worker. | In: partial-failure containment. Out: alerting/retry of the failed namespace. | [L233](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/IntegrationTests/PatientWorkerIntegrationTests.cs#L233) |

---

## tests/UnitTests/AuthorizationLogImplTest.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 12 | AuthorizationLogImplTest.Test_AuthorizationLog_WithSingleRecord | The service flattens one log and hands it to Firehose under the calling service's name. | Stub `HttpContext` with headers -> stub `FlattenAuthorizationLog(dto, "ServiceName", "1.2.3")` -> stub `SaveLogs(logList, "ServiceName")` -> call `AuthorizationLog` -> Assert the response matches expected | Verifies the single-record orchestration path. | In: convert-then-save wiring. Out: multi-record batching. | [L24](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/AuthorizationLogImplTest.cs#L24) |
| 13 | AuthorizationLogImplTest.Test_AuthorizationLog_ReturnErrorWhenDateHasNonZeroOffset | A non-zero offset is caught in the service layer, not just at the API boundary. | Stub `HttpContext` -> call `AuthorizationLog` with an offset datetime -> Assert the error response matches expected | Verifies the service-level source of the 400 in row 3. | In: error DTO. Out: HTTP status mapping. | [L56](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/AuthorizationLogImplTest.cs#L56) |
| 14 | AuthorizationLogImplTest.Test_AuthorizationLog_ReturnErrorWhenServiceHeaderIsMissing | A context with no service header produces the missing-header error response. | Stub `HttpContext` as a bare `DefaultHttpContext` -> call `AuthorizationLog` -> Assert the error response matches expected | Verifies the service-level source of the 400 in row 4. | In: error DTO. Out: HTTP mapping. | [L72](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/AuthorizationLogImplTest.cs#L72) |
| 15 | AuthorizationLogImplTest.Test_AuthorizationLog_ReturnErrorWhenRequestDtoIsEmpty | An empty log list is rejected rather than written as a zero-record batch. | Stub `HttpContext` with headers -> call `AuthorizationLog` with an empty body -> Assert the empty-request error response | Verifies the empty-payload guard. | In: empty-body rejection. Out: whether Firehose is called (not asserted). | [L88](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/AuthorizationLogImplTest.cs#L88) |
| 16 | AuthorizationLogImplTest.Test_AuthorizationLog_EmitsIdentityMetric | The `AuthorizationLogIdentityAudit` metric is emitted with tags describing the caller's identity, across 4 identity shapes. | `[TestCaseSource(AuthorizationLogIdentityMetricCases)]` — cases `UserAndServiceLoggedIn` (AspnetCloudId), `UserNotLoggedIn_ServiceLoggedIn`, `NullIdentities`, `IdentityServiceThrows` -> set up identity mocks -> call `AuthorizationLog` -> Verify `Increment("AuthorizationLogIdentityAudit", 1, 1.0, expectedTags)` once | Verifies identity-audit tagging, including that a throwing identity service degrades to "not logged in" rather than failing the request. | In: tag values `isUserLoggedIn`, `userIdNamespace`, `isServiceLoggedIn`. Out: metric backend. | [L117](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/AuthorizationLogImplTest.cs#L117) |
| 17 | AuthorizationLogImplTest.Test_PermissionChangeLog_EmitsIdentityMetric | The same identity-audit metric is emitted on the permission-change path, across 3 identity shapes. | `[TestCaseSource(PermissionChangeLogIdentityMetricCases)]` — cases `UserAndServiceLoggedIn` (Auth0PatientId), `NeitherLoggedIn`, `IdentityServiceThrows` -> set up identity mocks -> call `PermissionChangeLog` -> Verify the metric increment with the expected tags | Verifies identity-audit parity on the permission-change endpoint. | In: tag values. Out: metric backend. | [L154](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/AuthorizationLogImplTest.cs#L154) |

---

## tests/UnitTests/LogConverterTest.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 18 | LogConverterTest.Test_LogConverterWithSingleLog | A log DTO flattens correctly whether the incoming event guid is present, empty, or null. | `[TestCase("someGuid")]`, `[TestCase("")]`, `[TestCase(null)]` -> stub `NewGuid()` -> `FlattenAuthorizationLog(logDto, serviceName, libraryVersion)` -> Assert equivalent to expected | Verifies the core flatten mapping across guid-presence variants. | In: field mapping + guid fallback. Out: which guid wins when one is supplied (asserted only via expected). | [L17](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/LogConverterTest.cs#L17) |
| 19 | LogConverterTest.Test_LogConverterNullAdditionalField | A null `AdditionalFieldsAccessed` flattens without throwing. | Build a log DTO with the additional-fields collection null -> stub `NewGuid()` -> flatten -> Assert equivalent to expected | Verifies null-collection tolerance in the converter. | In: null handling. Out: null vs empty-list distinction downstream. | [L34](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/LogConverterTest.cs#L34) |
| 20 | LogConverterTest.Test_LogConverter_StripsQueryStrings | Query strings are removed from the logged URL so parameters are never persisted. | 6 `[TestCase]`s: `.../?blah=3`→`.../`, `.../`→unchanged, no-trailing-slash→unchanged, `""`→`""`, `null`→`null`, `/search?foo=3&blah=5`→`/search` -> flatten -> Assert equivalent to expected | Verifies query-string scrubbing, the converter's main data-minimization guard. | In: 6 URL shapes incl. empty and null. Out: fragments (`#...`), matrix params. | [L52](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/LogConverterTest.cs#L52) |
| 21 | LogConverterTest.Test_LogConverter_StripsHttpRoute | A very long real-world Pulse export URL is reduced to its path with the entire query removed. | 1 `[TestCase]` with a ~4KB `pulse.zocdoc.com/csr/bookingdataexport/downloadreport?...` URL carrying hundreds of provider ids -> flatten -> Assert the route is the bare path | Verifies scrubbing holds on the pathological long-URL case that motivated it. | In: long-URL scrubbing. Out: any length cap on the stored route. | [L65](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/LogConverterTest.cs#L65) |
| 22 | LogConverterTest.Test_LogConverterRemoveDuplicateEnums | Repeated field entries collapse to one, for both the enum list and the free-text list. | 1 `[TestCase()]` -> flatten a DTO with duplicate entries -> Assert `AuthorizationFieldsAccessed` equals `[PatientDob]` -> Assert `AuthorizationAdditionalFieldsAccessed` equals `["duplicate"]` | Verifies de-duplication of accessed-field lists. | In: dedupe of both lists. Out: ordering guarantees. | [L78](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/LogConverterTest.cs#L78) |

---

## tests/UnitTests/FirehoseClientWrapperTest.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 23 | FirehoseClientWrapperTest.Test_GetFireHoseResponse | Each flattened log is serialized individually and the Firehose response is mapped back to a `LogResponseDto`. | Stub `IAmazonKinesisFirehose` -> stub `SerializeObject` for three logs -> `SaveLogs(flattenedLogs, "ServiceName")` -> Assert the result matches expected | Verifies serialization-per-record and response mapping. | In: mapping of the AWS response. Out: real AWS behavior (row 8). | [L24](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/FirehoseClientWrapperTest.cs#L24) |

---

## tests/UnitTests/GuidGeneratorTest.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 24 | GuidGeneratorTest.Test_GuidGenerator_MatchingGuidLengths | `NewGuid()` returns a string of standard GUID length. | Call `_service.NewGuid()` -> Assert its length equals that of a canonical GUID string | Verifies the generated id's shape. | In: length only. Out: format validity and uniqueness — length alone would pass on any 36-char string. | [L11](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/GuidGeneratorTest.cs#L11) |

---

## tests/UnitTests/DynamoKeyServiceTest.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 25 | DynamoKeyServiceTest.CreateDynamoPartitionKey_ValidIdAndNamespace | The patient partition key is built as `patient#<namespace>#<id>`. | `CreateDynamoPartitionKey("someId", PatientNamespace.MonolithPatient)` -> Assert it equals `patient#MonolithPatient#someId` | Pins the Dynamo partition-key format. | In: exact key string. Out: key length limits / id escaping. | [L10](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/DynamoKeyServiceTest.cs#L10) |
| 26 | DynamoKeyServiceTest.VersionKeyToNumerical_FirstVersionTo0 | The first version sort key maps to numeric 0. | `VersionKeyToNumerical(DynamoKeyService.FirstVersionSortKey)` -> Assert 0 | Pins the version-key ↔ integer mapping at its base case. | In: first version only. Out: higher versions and malformed keys. | [L18](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/DynamoKeyServiceTest.cs#L18) |

---

## tests/UnitTests/LegalReportingPatientDynamoPersistenceTest.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 27 | LegalReportingPatientDynamoPersistenceTest.ScanOnce | A scan that consumes the whole table returns all items and no continuation key. | `ScanForUniquePatients(null, 100)` -> Assert `LastScannedKey` is null -> Assert `ScannedItems` equals the expected patient list | Verifies the terminal-scan result shape. | In: full-scan case. Out: filter-expression correctness. | [L90](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/LegalReportingPatientDynamoPersistenceTest.cs#L90) |
| 28 | LegalReportingPatientDynamoPersistenceTest.ScanOnce_2DdbItemsButMaxOneScan_LastEvaluatedKeyPatient1 | A size-capped scan returns the first item plus a continuation key pointing at it. | `ScanForUniquePatients(null, 1)` over 2 items -> Assert `LastScannedKey` equals `(patientUrn1, versionNumber)` -> Assert only the first item is returned | Verifies pagination checkpointing. | In: continuation-key value. Out: resuming from that key (row 10). | [L116](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/LegalReportingPatientDynamoPersistenceTest.cs#L116) |
| 29 | LegalReportingPatientDynamoPersistenceTest.GetLatestPatients_ChunkAndQuery | A large URN list is chunked into multiple Dynamo queries and reassembled in order. | Stub `QueryAsync` to echo per-request results -> `BatchGetLatestPatientsAsync(patientUrns)` -> Assert the result matches one DTO per input URN, index-aligned | Verifies chunked batch-get and result reassembly. | In: chunking + ordering. Out: the chunk size itself. | [L135](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/LegalReportingPatientDynamoPersistenceTest.cs#L135) |

---

## tests/UnitTests/PatientNamespaceContractTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 30 | PatientNamespaceContractTests.PatientNamespace_MatchesPlinthPatientNamespaceForReporting | The hand-written `PatientNamespace` enum stays in lockstep with the generated `PatientNamespaceForReporting`. | Collect `[EnumMember]` serialized names from both enums -> Assert the two sets are equivalent | Guards a cross-repo contract: per the test's own comment, drift makes the lambda throw on a whole S3 object and silently drop those patients from legal reporting. | In: serialized-name parity. Out: value ordering and numeric values. | [L21](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientNamespaceContractTests.cs#L21) |

---

## tests/UnitTests/PatientIdEnqueue.Lambda/S3LogParserTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 31 | S3LogParserTests.RetrieveUnzippedS3FileAsString_ValidFile_ParsingSucceeds | A well-formed gzipped S3 log file parses into the expected patient models. | Stage the S3 response -> `ParsePatientsFromS3File("bucketName", "objectKey")` -> Assert equivalent to the expected models | Verifies the lambda's core S3 parse path. | In: unzip + line parse + model mapping. Out: S3 listing/triggering. | [L25](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientIdEnqueue.Lambda/S3LogParserTests.cs#L25) |
| 32 | S3LogParserTests.RetrieveUnzippedS3FileAsString_LogsWithMissingProperties | Log lines missing optional properties still parse. | Stage logs with absent fields -> parse -> Assert equivalent to the expected models | Verifies tolerance to schema-optional fields. | In: missing optional properties. Out: missing required properties. | [L69](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientIdEnqueue.Lambda/S3LogParserTests.cs#L69) |
| 33 | S3LogParserTests.RetrieveUnzippedS3FileAsString_UnknownPatientNamespace_SkipsOnlyThatLine | An unrecognized patient namespace drops that one line instead of failing the whole file. | Stage a file mixing a valid line with an unknown-namespace line -> parse -> Assert only the valid model is returned | Verifies line-level fault isolation — the mitigation for the drift risk in row 30. | In: single-line skip. Out: whether the skip is logged/alerted. | [L107](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientIdEnqueue.Lambda/S3LogParserTests.cs#L107) |
| 34 | S3LogParserTests.RetrieveUnzippedS3FileAsString_OutboundSchedulingPatient_ParsingSucceeds | The Outbound Scheduling patient namespace parses correctly. | Stage an outbound-scheduling log -> parse -> Assert the expected model list | Verifies namespace-specific coverage for outbound scheduling. | In: one namespace. Out: the other namespaces individually. | [L138](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientIdEnqueue.Lambda/S3LogParserTests.cs#L138) |

---

## tests/UnitTests/PatientIdEnqueue.Lambda/ReportingModelToDdbDtoServiceTest.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 35 | ReportingModelToDdbDtoServiceTest.CreateDtosForFirstVersionInsertion_SingleModel_SingleDto | One reporting model becomes one first-version DTO. | `CreateDtosForFirstVersionInsertion([model("someId")])` -> Assert it equals `[dto("someId")]` | Verifies the base-case model→DTO conversion. | In: single-item mapping. Out: field-level detail beyond the id. | [L53](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientIdEnqueue.Lambda/ReportingModelToDdbDtoServiceTest.cs#L53) |
| 36 | ReportingModelToDdbDtoServiceTest.CreateDtosForFirstVersionInsertion_10Models_10Dtos | Ten distinct models produce ten DTOs. | Convert 10 models -> Assert equivalent to the 10 expected DTOs | Verifies conversion scales without loss. | In: 1:1 fan-out. Out: ordering. | [L60](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientIdEnqueue.Lambda/ReportingModelToDdbDtoServiceTest.cs#L60) |
| 37 | ReportingModelToDdbDtoServiceTest.CreateDtosForFirstVersionInsertion_10ModelsBut5Exist_OnlyCreate5 | Patients already in Dynamo are not re-inserted at version 0. | Arrange 5 of 10 as already existing -> convert -> Assert only the 5 new DTOs come back | Verifies existence filtering before insertion. | In: existing-record suppression. Out: what happens to the existing 5 (handled by the refresh worker). | [L68](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientIdEnqueue.Lambda/ReportingModelToDdbDtoServiceTest.cs#L68) |
| 38 | ReportingModelToDdbDtoServiceTest.CreateDtosForFirstVersionInsertion_10Models0Exist5Duplicates_OnlyCreate5 | Duplicates within one input batch collapse to unique DTOs. | Supply 10 models containing 5 duplicate pairs, none existing -> convert -> Assert 5 DTOs | Verifies intra-batch de-duplication, preventing duplicate-key writes. | In: dedupe within the batch. Out: dedupe across batches. | [L76](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientIdEnqueue.Lambda/ReportingModelToDdbDtoServiceTest.cs#L76) |

---

## tests/UnitTests/PatientRefresh.Worker/PatientResponseToDdbDtoServiceTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 39 | PatientResponseToDdbDtoServiceTests.CalculatePatientsToUpdateOrCreate_CreatesNewVersion | Changed patient data produces a new version row. | `CalculatePatientsToUpdateOrCreate(oldPatients, newPatients)` with differing data -> Assert the expected new-version DTOs | Verifies version increment on change. | In: change detection → new version. Out: which fields count as a change. | [L31](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/PatientResponseToDdbDtoServiceTests.cs#L31) |
| 40 | PatientResponseToDdbDtoServiceTests.CalculatePatientsToUpdateOrCreate_KeepSameVersion | Unchanged patient data does not bump the version. | Call with identical old and new data -> Assert the expected same-version DTOs | Verifies no-op writes don't inflate version history. | In: no-change path. Out: whether a write is skipped entirely. | [L83](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/PatientResponseToDdbDtoServiceTests.cs#L83) |
| 41 | PatientResponseToDdbDtoServiceTests.CalculatePatientsToUpdateOrCreate_NotFoundVersion | A patient the upstream API no longer returns is versioned as not-found rather than dropped. | Call with a new set missing a patient -> Assert the expected not-found DTO | Verifies deletion/absence is recorded, not silently lost. | In: not-found marking. Out: downstream consumption of that marker. | [L117](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/PatientResponseToDdbDtoServiceTests.cs#L117) |
| 42 | PatientResponseToDdbDtoServiceTests.CalculatePatientsToUpdateOrCreate_RandomMix | A mixed batch of changed, unchanged, and missing patients resolves correctly for all three. | Call with a mixed old/new set -> order by `PatientId` -> Assert the full expected DTO list | Verifies the three branches interact correctly in one batch. | In: combined-branch correctness. Out: batch-size effects. | [L171](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/PatientResponseToDdbDtoServiceTests.cs#L171) |

---

## tests/UnitTests/PatientRefresh.Worker/PatientServiceTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 43 | PatientServiceTests.GetLatestPatientInfo_CallsDifferentApis | Patients are routed to the correct upstream API by namespace. | Stub the intake, payment, and external-API callers -> stub `CalculatePatientsToUpdateOrCreate` -> `GetLatestPatientInfo(shuffledList, ct)` -> Assert each caller received only its own patients | Verifies namespace-based API routing on a shuffled input. | In: routing correctness. Out: per-API response mapping. | [L26](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/PatientServiceTests.cs#L26) |
| 44 | PatientServiceTests.GetLatestPatientInfo_CallsDifferentApisOnce | Each upstream API is called exactly once with the full id set for its namespace, not once per patient. | Stub each caller with `It.Is` matchers on the exact id sets -> call `GetLatestPatientInfo` -> Assert the matched single call per API | Verifies request batching per namespace. | In: one-call-per-API batching. Out: chunking above the API's own limit. | [L104](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/PatientServiceTests.cs#L104) |
| 45 | PatientServiceTests.GetLatestPatientInfo_DoesNotCallApiCallersIfNoPatients | Namespaces with no patients trigger no upstream calls. | Call with monolith-only patients -> Verify the intake, payment, external-API, and calculate collaborators were never invoked -> Assert the result is empty | Verifies empty-namespace short-circuiting. | In: no wasted upstream calls. Out: monolith-namespace handling itself. | [L183](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/PatientServiceTests.cs#L183) |

---

## tests/UnitTests/PatientRefresh.Worker/ScanServiceTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 46 | ScanServiceTests.GetUniqueFirstVersionPatients_ReturnsFilteredResults | Only patients still at first version are returned, and the per-scan gauge is emitted. | Stub `ScanForUniquePatients` -> `GetUniqueFirstVersionPatients(...)` -> Assert 1 patient returned and it is the expected one -> Assert `lastScanned` is null -> Verify `Gauge("patientToUpdateCountPerScan", 1, ...)` once | Verifies filtering plus scan-level instrumentation. | In: filter + gauge. Out: the filter predicate's own definition. | [L23](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/ScanServiceTests.cs#L23) |
| 47 | ScanServiceTests.GetUniqueFirstVersionPatients_HandlesMultipleScans | Results accumulate across successive Dynamo scans. | Stub two scan pages -> call -> Assert both patients returned -> Assert `lastScanned` null -> Verify the gauge emitted twice | Verifies multi-page accumulation. | In: aggregation across pages. Out: page-size selection. | [L60](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/ScanServiceTests.cs#L60) |
| 48 | ScanServiceTests.GetUniqueFirstVersionPatients_StopsAtScanSize | Scanning halts once the configured scan size is reached and returns a resume key. | Stub scans exceeding the size -> call -> Assert 2 patients -> Assert `lastScanned` equals the last evaluated PK/SK -> Verify the scan call count | Verifies the scan-size cap. | In: cap enforcement + resume key. Out: the cap value. | [L112](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/ScanServiceTests.cs#L112) |
| 49 | ScanServiceTests.GetUniqueFirstVersionPatients_StopsAtScanSizeAndIgnoresSubsequentScans | Once the cap is hit, later scan pages are neither issued nor included. | Stub 4 available patients with a cap of 2 -> call -> Assert patients 1 and 2 returned and 3 and 4 absent -> Assert `lastScanned` is the first scan's key -> Verify the scan and gauge call counts | Verifies no over-read past the cap. | In: strict truncation. Out: fairness/starvation of later items. | [L154](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/ScanServiceTests.cs#L154) |
| 50 | ScanServiceTests.GetUniqueFirstVersionPatients_StopsWhenLastEvaluatedKeyIsNull_EvenIfScanSizeNotReached | A null `LastEvaluatedKey` ends the scan even below the cap, and the resume key is cleared. | Stub a table exhausted before the cap -> call -> Assert 2 patients, 3 and 4 absent -> Assert `lastScanned` is null -> Verify scan and gauge counts | Verifies end-of-table termination. | In: exhaustion path. Out: interaction with concurrent writes. | [L214](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/ScanServiceTests.cs#L214) |
| 51 | ScanServiceTests.GetUniqueFirstVersionPatients_StopsAfterMaxIterations_AndReturnsLastKey | A runaway scan is bounded at 1000 iterations and still returns a usable resume key. | Stub scans that never exhaust -> call -> Assert the collected patients -> Assert `lastScanned` equals the last evaluated key -> Verify the gauge emitted exactly 1000 times | Verifies the infinite-loop backstop. | In: 1000-iteration cap. Out: whether hitting the cap is alerted. | [L268](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/ScanServiceTests.cs#L268) |

---

## tests/UnitTests/PatientRefresh.Worker/WorkerTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 52 | WorkerTests.ExecuteAsync_NoPriorScansAllItemsScanned_DeleteLastScannedKey | A run that scans everything writes the updates and clears the checkpoint. | Stub the scan, batch-get, and `GetLatestPatientInfo` collaborators -> `StartAsync` -> Verify `BatchWritePatientsAsync(updated, ct)` once -> Verify `DeleteLastScannedKey` once | Verifies checkpoint cleanup on a complete run. | In: write + delete-checkpoint. Out: failure mid-write. | [L69](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/WorkerTests.cs#L69) |
| 53 | WorkerTests.ExecuteAsync_NoPriorScansPatientOneScanned_PutPatient1LastEval | A partial run writes its updates and persists the resume key. | Stub a scan returning only patient 1 -> `StartAsync` -> Verify `BatchWritePatientsAsync(updatedPatient1, ct)` once -> Verify `PutLastScannedKey(lastScannedKey, ct)` once | Verifies checkpoint persistence on an incomplete run. | In: write + put-checkpoint. Out: resume correctness (row 10). | [L121](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/WorkerTests.cs#L121) |
| 54 | WorkerTests.ExecuteAsync_MultipleBatchesInScan | With `ProcessingBatchSize = 1`, one scan's results are processed as multiple sequential batches. | Set `ProcessingBatchSize = 1` -> stub two batches with distinct `GetLatestPatientInfo` results -> `StartAsync` -> Assert each batch was fetched and written separately | Verifies intra-scan batching. | In: batch splitting. Out: the production batch size. | [L167](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/WorkerTests.cs#L167) |
| 55 | WorkerTests.ExecuteAsync_ErrorInOneNamespaceDoesNotAffectOthers | Namespaces are processed as separate batches so one failing does not block the rest — the unit-level counterpart of row 11. | Set `ProcessingBatchSize = 2` (enough for both patients in one batch if same-namespace) -> stub ZVS and External-API patients in separate namespaces with one failing -> `StartAsync` -> Assert the healthy namespace still wrote | Verifies per-namespace batching is what provides the fault isolation. | In: isolation mechanism. Out: retry of the failed namespace. | [L237](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/tests/UnitTests/PatientRefresh.Worker/WorkerTests.cs#L237) |

---

## monolithInvestigationScripts/BitmaskDecode.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 56 | RunBitMask | Nothing — an `[Test]`-annotated developer script that decodes hex field-access bitmasks into readable field names for manual monolith investigation. | Iterate a hard-coded list of hex bitmasks -> decode each into the fields it represents | Investigation tool, not coverage. No assertions. | Out of scope for coverage accounting; it runs under the test runner only as a convenient entry point. | [L3](https://github.com/Zocdoc/audit-logging-service/blob/2d5e6ad6c605368f5fe3f2709ceb44e0fdebc242/monolithInvestigationScripts/BitmaskDecode.cs#L3) |

---

## Observations

- **One test has no assertion and one asserts almost nothing.** `RunBitMask` (row 56) is a developer script wearing a `[Test]` attribute, and `Test_GuidGenerator_MatchingGuidLengths` (row 24) only compares string *length*, so any 36-character return value passes.
- **Data minimization is well covered.** Rows 20–22 pin query-string stripping, long-URL stripping, and accessed-field de-duplication — the converter behaviors that keep request parameters out of the audit store.
- **The cross-repo enum contract (row 30) is the highest-leverage test here.** Its own comment documents the failure mode: enum drift makes the lambda throw on an entire S3 object, silently dropping those patients from legal reporting.
- **Fault isolation is tested at two levels** — per-namespace batching in the worker unit test (row 55) and end-to-end against DynamoDB (row 11) — plus per-line skipping in the S3 parser (row 33).
- **No authorization tests.** Both endpoints validate a service *header* (rows 4, 7) but nothing asserts authentication or authorization on this service's API surface.
