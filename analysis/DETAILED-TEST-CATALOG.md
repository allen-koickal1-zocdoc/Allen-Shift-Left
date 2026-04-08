# Detailed Test Catalog - Pterodactyl Team

Every test and what it does.

---

# practice-authorization-proxy (30 tests)

## AuthorizationServiceTests.cs (12 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `Verify_IsPracticeAuthorized_ReturnsExpectedResult_SendsMetricsCorrectly` | Parameterized test verifying `IsPracticeAuthorized` returns `true` only when FGA returns `Success`, `false` for all other results |
| `Verify_IsPracticeAuthorized_FgaAuthzServiceThrows_ReturnsExpectedResult_SendsMetricsCorrectly` | When FGA throws exception, service catches it and returns `false` (fail-safe behavior) |
| `Verify_IsOrganizationAuthorized_ReturnsExpectedResult_SendsMetricsCorrectly` | Parameterized test verifying `IsOrganizationAuthorized` returns `true` only when FGA returns `Success` |
| `Verify_IsOrganizationAuthorized_FgaAuthzServiceThrows_ReturnsExpectedResult_SendsMetricsCorrectly` | When FGA throws exception, service catches it and returns `false` (fail-safe) |
| `Verify_BatchIsPracticeAuthorized_ReturnsSuccess` | Verifies batch practice auth returns correct `EntityAuthorizationCheckResult` for multiple practices (pt_123, pt_456) |
| `Verify_BatchIsPracticeAuthorized_FgaAuthzServiceThrows_ThrowsGenericException` | When FGA throws during batch, exception propagates up (not caught) |
| `Verify_BatchIsPracticeAuthorized_FgaReturnsError_ThrowsCustomExceptionWithMessage` | When FGA returns error, throws `BatchPracticeAuthorizationException` with specific message |
| `Verify_BatchIsPracticeAuthorized_FgaReturnsError_ThrowsCustomExceptionWithCorrectProperties` | Thrown exception contains correct properties: practice IDs, error object, null results |
| `Verify_BatchIsOrganizationAuthorized_ReturnsSuccess` | Verifies batch org auth returns correct results for multiple orgs (org_123, org_456) |
| `Verify_BatchIsOrganizationAuthorized_FgaAuthzServiceThrows_ThrowsException` | When FGA throws during batch org auth, exception propagates up |
| `Verify_BatchIsOrganizationAuthorized_FgaReturnsError_ThrowsCustomExceptionWithMessage` | When FGA returns error, throws `BatchOrganizationAuthorizationException` |
| `Verify_BatchIsOrganizationAuthorized_FgaReturnsError_ThrowsCustomExceptionWithCorrectProperties` | Thrown exception contains correct organization IDs, error object, null results |

## ConversionExtensionsTests.cs (5 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `VerifyAllPermissionsFiltersRepresentedInPracticeAuthorizationProxy` | Verifies `WebToCore()` can convert every `PermissionFilter` enum value without throwing |
| `Verify_ToBatchPracticeResult_ConvertsSuccessfully` | Converts `EntityAuthorizationCheckResult` list to `BatchSinglePracticeAuthorizationResult`, mapping Success→true |
| `Verify_ToBatchOrganizationResult_ConvertsSuccessfully` | Converts results to `BatchSingleOrganizationAuthorizationResult`, mapping Success→true |
| `Verify_ToBatchPracticeResult_WithEmptyResults_ConvertsSuccessfully` | Empty input returns non-null result with empty `Results` collection |
| `Verify_ToBatchOrganizationResult_WithEmptyResults_ConvertsSuccessfully` | Empty input returns non-null result with empty `Results` collection |

## PracticeAuthorizationTests.cs (5 tests) - API

| Test Name | What It Tests |
|-----------|---------------|
| `IsPracticeAuthorized_GivenNotLoggedIn_ReturnsUnauthorized` | `/practice/{id}/is_authorized` returns HTTP 401 when no auth headers |
| `IsPracticeAuthorized_GivenNonPracticeUser_ReturnsForbidden` | Returns HTTP 403 when authenticated as patient or CSR |
| `IsPracticeAuthorized_GivenPracticeUser_ReturnsResponse` | Returns HTTP 200 with correct `IsAuthorized` for practice users (tests authorized pt_100→true, unauthorized→false) |
| `BatchIsPracticeAuthorized_GivenMoreThan50Practices_ReturnsBadRequest` | Returns HTTP 400 when >50 practice IDs provided |
| `BatchIsPracticeAuthorized_GivenExactly50Practices_ReturnsOK` | Returns HTTP 200 when exactly 50 practice IDs (boundary test) |

## OrganizationAuthorizationTests.cs (5 tests) - API

| Test Name | What It Tests |
|-----------|---------------|
| `IsOrganizationAuthorized_GivenNotLoggedIn_ReturnsUnauthorized` | `/organization/{id}/is_authorized` returns HTTP 401 when no auth headers |
| `IsOrganizationAuthorized_GivenNonPracticeUser_ReturnsForbidden` | Returns HTTP 403 when authenticated as patient or CSR |
| `IsOrganizationAuthorized_GivenPracticeUser_ReturnsResponse` | Returns HTTP 200 with correct `IsAuthorized` for practice users |
| `BatchIsOrganizationAuthorized_GivenMoreThan50Organizations_ReturnsBadRequest` | Returns HTTP 400 when >50 org IDs provided |
| `BatchIsOrganizationAuthorized_GivenExactly50Organizations_ReturnsOK` | Returns HTTP 200 when exactly 50 org IDs (boundary test) |

## Placeholder Tests (3 tests) - TO REMOVE

| Test Name | What It Tests |
|-----------|---------------|
| `TokenEmptyTest` (UnitTests) | Placeholder: verifies 1+1=2 - NO REAL VALUE |
| `TokenEmptyTest` (IntegrationTests) | Placeholder: verifies 1+1=2 - NO REAL VALUE |
| `TokenEmptyTest` (Web.IntegrationTests) | Placeholder: verifies 1+1=2 - NO REAL VALUE |

---

# practice-user-permissions (~870 tests)

## Lambda Integration Tests

### FgaLambdaTests.cs (5 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToLambda_WithEmptyEventList_Success` | Verifies Lambda returns 200 OK when invoked with empty SQS event list |
| `SendMultipleEventsToLambda_TestParsingSqsEvents` | Tests parsing of mixed valid/invalid SQS messages, returns batch failures for malformed messages while processing valid UserRole inserts correctly |
| `FgaUpdates_HandlesDeletesProperly` | Verifies FGA tuple is created on insert and removed when soft-deleted |
| `FgaUpdates_RepeatedWritesAndDelete` | Tests idempotency: repeated inserts followed by delete correctly removes tuple |
| `FgaUpdates_MultipleDtoTypes` | End-to-end test processing UserRole, PracticeMember, OrganizationMember, Appointment, PracticeBlocked, and ScopedOrganizationMember DTOs with both inserts and deletes |

### StreamConsumerLambdaTests.cs (22 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToLambda_WithEmptyEventList_Success` | Verifies DDB stream consumer Lambda handles empty event list |
| `SendEventToLambda_InsertUserVersion_PropagatesMessagesToSqs` | Verifies INSERT of UserVersion record propagates correct SNS message to SQS |
| `SendEventToLambda_ModifyUserVersion_PropagatesMessagesToSqs` | Verifies MODIFY of UserVersion record propagates old and new values to SQS |
| `SendEventToLambda_DeleteUserVersion_DoesntPropagateMessagesToSqs` | Verifies REMOVE of UserVersion still propagates message to SQS (for completeness) |
| `SendEventToLambda_InsertUserRoles_PropagatesMessagesToSqs` | Verifies INSERT of UserRole record propagates to SQS |
| `SendEventToLambda_ModifyUserRoles_PropagatesMessagesToSqs` | Verifies MODIFY of UserRole (soft delete) propagates to SQS |
| `SendEventToLambda_DeleteUserRoles_PropagateMessagesToSqs` | Verifies REMOVE of UserRole propagates to SQS |
| `SendEventToLambda_InsertPracticeMember_PropagatesMessagesToSqs` | Verifies INSERT of PracticeMember record propagates to SQS |
| `SendEventToLambda_ModifyPracticeMember_PropagatesMessagesToSqs` | Verifies MODIFY of PracticeMember propagates to SQS |
| `SendEventToLambda_DeletePracticeMember_PropagateMessagesToSqs` | Verifies REMOVE of PracticeMember propagates to SQS |
| `SendEventToLambda_InsertOrganizationMember_PropagatesMessagesToSqs` | Verifies INSERT of OrganizationMember propagates to SQS |
| `SendEventToLambda_ModifyOrganizationMember_PropagatesMessagesToSqs` | Verifies MODIFY of OrganizationMember propagates to SQS |
| `SendEventToLambda_DeleteOrganizationMember_PropagateMessagesToSqs` | Verifies REMOVE of OrganizationMember propagates to SQS |
| `SendEventToLambda_InsertAppointment_PropagatesMessagesToSqs` | Verifies INSERT of Appointment propagates to SQS |
| `SendEventToLambda_ModifyAppointment_PropagatesMessagesToSqs` | Verifies MODIFY of Appointment propagates to SQS |
| `SendEventToLambda_DeleteAppointment_PropagateMessagesToSqs` | Verifies REMOVE of Appointment propagates to SQS |
| `SendEventToLambda_InsertPracticeBlockedDto_PropagatesMessagesToSqs` | Verifies INSERT of PracticeBlocked (churn) propagates to SQS |
| `SendEventToLambda_ModifyPracticeBlockedDto_PropagatesMessagesToSqs` | Verifies MODIFY of PracticeBlocked propagates to SQS |
| `SendEventToLambda_DeletePracticeBlockedDto_PropagateMessagesToSqs` | Verifies REMOVE of PracticeBlocked propagates to SQS |
| `SendEventToLambda_InsertScopedOrganizationMember_PropagatesMessagesToSqs` | Verifies INSERT of ScopedOrganizationMember propagates to SQS |
| `SendEventToLambda_ModifyScopedOrganizationMember_PropagatesMessagesToSqs` | Verifies MODIFY of ScopedOrganizationMember propagates to SQS |
| `SendEventToLambda_DeleteScopedOrganizationMember_PropagateMessagesToSqs` | Verifies REMOVE of ScopedOrganizationMember propagates to SQS |

### MonolithBackfillLambdaTests.cs (4 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToLambda_WithEmptyEventList_Success` | Verifies monolith backfill Lambda handles empty event list |
| `SendMultipleEventsToLambda_TestParsingSqsEvents` | Tests mixed valid/invalid messages, verifies user roles are backfilled to monolith for valid messages |
| `SendEventToLambda_WithSampleAuth0User_Succeeds` | Verifies backfill handles Auth0 SSO users with invalid practice IDs gracefully |
| `SendEventToLambda_WithOrgLevelPermissions_ProcessesCorrectly` | Verifies organization-level permissions are expanded to practice-level for backfill |

### AuditLoggingLambdaTests.cs (3 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToLambda_WithEmptyEventList_Success` | Verifies audit logging Lambda handles empty event list |
| `SendMultipleEventsToLambda_TestParsingSqsEvents` | Tests parsing of mixed valid/invalid messages with batch failure handling |
| `ProcessesEventsAndSendsToFirehose` | End-to-end test verifying audit logs are written to S3 for UserRole, PracticeMember, PracticeBlocked, and ScopedOrganizationMember events |

### HandleOrgMembershipRefreshSqsEventsTests.cs (3 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToLambda_WithEmptyEventList_Success` | Verifies org membership refresh Lambda handles empty event list |
| `SendMultipleEventsToLambda_TestParsingSqsEvents` | Tests parsing with batch failures; verifies user version is incremented after org member insert |
| `SendEventToLambda_WithComplexOrgHierarchy_UpdatesOnlyAffectedUsers` | Verifies only users with roles in affected organizations have their versions incremented |

### HandleScopedOrganizationChangesSqsEventsTests.cs (9 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToLambda_WithEmptyEventList_Success` | Verifies scoped org changes Lambda handles empty event list |
| `SendEventToLambda_WhenPracticeAddedWithUser_SetsScopedOrganization` | Verifies user's scoped org is set to ultimate parent when practice is added to org hierarchy |
| `SendEventToLambda_WhenUserAlreadyHasScopedOrgAndIsOnOrgLevelExperience_DoesNotUpdate` | Verifies V2 users' existing scoped org is preserved |
| `SendEventToLambda_WhenUserAlreadyHasScopedOrgButNotOnOrgLevelExperience_UpdatesScopedOrg` | Verifies V1 users' scoped org is updated to new ultimate parent |
| `SendEventToLambda_WhenMultipleUsersAtPractice_SetsAllUsersScopedOrganizations` | Verifies all users at a practice are scoped when practice joins org |
| `SendEventToLambda_WhenOrganizationMemberIsNotPractice_DoesNotProcess` | Verifies org-to-org relationships don't trigger scoped org updates |
| `SendEventToLambda_WhenMalformedMessages_ReturnsFailures` | Tests malformed message handling alongside valid messages |
| `SendEventToLambda_WhenPracticeHasNoUsers_CompletesSuccessfully` | Verifies Lambda succeeds when practice has no associated users |
| `SendEventToLambda_WhenV1UserHasConflictingOrganizationsAndExistingScopedOrg_DeletesScopedOrg` | Verifies V1 users with conflicting orgs have scoped org deleted; V2 users are preserved |

### HandleOrgHierarchyRoleFixesSqsEventsTests.cs (14 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToLambda_WithEmptyEventList_Success` | Verifies org hierarchy role fixes Lambda handles empty event list |
| `SendEventToLambda_WithMalformedMessages_ReturnsPartialFailures` | Tests batch failure handling for malformed messages |
| `SendEventToLambda_WithUltimateParentOrganization_NoConversionPerformed` | Verifies users at ultimate parent org level have roles unchanged |
| `SendEventToLambda_WithComplexHierarchyAndMultipleUsers_ConvertsChildOrgUsersWithRoleExpansion` | Verifies child org users have org-level roles converted to practice-level with role expansion |
| `SendEventToLambda_WhenPracticeMovesToDifferentOrganization_RemovesMisScopedUserRoles` | Verifies users scoped to old org lose practice roles when practice moves |
| `SendEventToLambda_WhenUserHasNoScopedOrganization_ProcessingFails` | Verifies processing fails (DLQ) when user has no scoped organization |

### ProviderGroupMembershipSqsEventsLambdaTests.cs (4 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToLambda_WithEmptyEventList_Success` | Verifies provider group membership Lambda handles empty event list |
| `SendEventToLambda_Success` | Tests org membership sync from provider-grouping service, verifying org hierarchy is correctly populated in DDB |
| `SendEventToLambda_RemovesChildrenWhenOrgNotFound` | Verifies org children are removed when org returns 404 from provider-grouping |
| `SendEventToLambda_RemovesChildrenWhenOrgNotFound_AndRemoves404FromParentWhenExists` | Verifies 404 org is removed from parent's children list |

### ProviderGroupSiblingPracticeSqsEventsLambdaTests.cs (3 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToLambda_WithEmptyEventList_Success` | Verifies sibling practices Lambda handles empty event list |
| `UserIsMappedToPracticeAndOrg` | Complex test verifying sibling practice SettingsManagement roles are added/removed based on user's practice access across orgs |
| `UltimateParentChange_RemovesOldOrgRolesAndPreservesUserSet` | Verifies system-set org roles are removed when ultimate parent changes; user-set roles preserved |

### ProviderProfileChurnSqsEventsTests.cs (2 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToLambda_WithEmptyEventList_Success` | Verifies provider profile churn Lambda handles empty event list |
| `SendEventToLambda_WithBothValidAndInvalidEvents_UpdatesChurnStatusInDdbForValidEventsOnly` | Verifies practice churn status is updated for valid events; invalid events return batch failures |

### ProviderMappingSqsEventsTests.cs (5 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToLambda_WithEmptyEventList_ReturnsSuccess` | Verifies provider mapping Lambda handles empty event list |
| `SendEventToLambda_WhenProviderExistsInProviderProfile_UpsertsPracticeMemberInDdb` | Verifies provider-practice relationship is created when provider exists in Provider Profile |
| `SendEventToLambda_WhenProviderNotInProviderProfile_SoftDeletesPracticeMemberInDdb` | Verifies provider-practice relationship is soft-deleted when provider not found |
| `SendEventToLambda_WhenNotificationIsIdempotent_UpsertIsIdempotent` | Verifies duplicate notifications don't create duplicate records |
| `SendEventToLambda_WithInvalidNotification_SkipsAndReturnsParsingFailure` | Verifies invalid notifications return batch failures |

### UserRoleChangeNotificationLambdaTests.cs (21 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SendEventToNotificationLambda_WithEmptyEventList_Success` | Verifies notification Lambda handles empty event list |
| `SendEventToNotificationLambda_GivenUltimateOrgIdNotFound_SkipsNotificationAndDoesNotFail` | Verifies orphan practices skip notification without failure |
| `UserCreatedEvent_GivenOrgHasOrgLevelUser_SinglePracticeUser_SendNotificationToOrgLevelUser` | Verifies org-level admin receives notification for new single-practice user |
| `UserCreatedEvent_GivenOrgHasOrgLevelUser_MultiplePracticeUser_SendNotificationToOrgLevelUser` | Verifies org-level admin receives notification for new multi-practice user |
| `UserCreatedEvent_GivenOrgHasOrgLevelUser_OrganizationUser_SendsNotificationToOrgLevelUser` | Verifies org-level admin receives notification for new org-level user |
| `UserCreatedEvent_GivenOrgDoesNotHaveOrgLevelUser_SinglePracticeUser_SendNotificationToPracticeUsers` | Verifies practice-level full-access users receive notification when no org admin exists |
| `UserCreatedEvent_GivenOrgDoesNotHaveOrgLevelUser_MultiplePracticeUser_SendNotificationToPracticeUsers` | Verifies multiple practice full-access users receive notifications |
| `UserCreatedEvent_GivenOrgDoesNotHaveOrgLevelUser_OrganizationUser_SendNotificationToPracticeUsers` | Verifies no notification for new org user when no org admin exists |
| `UserDeletedEvent_GivenOrgHasOrgLevelUser_SinglePracticeUser_SendNotificationToOrgLevelUser` | Verifies org admin receives notification for deleted single-practice user |
| `UserDeletedEvent_GivenOrgHasOrgLevelUser_MultiplePracticeUser_SendNotificationToOrgLevelUser` | Verifies org admin receives notification for deleted multi-practice user |
| `UserDeletedEvent_GivenOrgHasOrgLevelUser_OrganizationUser_SendsNotificationToOrgLevelUser` | Verifies org admin receives notification for deleted org user |
| `UserDeletedEvent_GivenOrgDoesNotHaveOrgLevelUser_SinglePracticeUser_SendNotificationToPracticeUsers` | Verifies practice full-access users receive deletion notification |
| `UserDeletedEvent_GivenOrgDoesNotHaveOrgLevelUser_MultiplePracticeUser_SendNotificationToPracticeUsers` | Verifies multiple practice users receive deletion notification |
| `UserDeletedEvent_GivenOrgDoesNotHaveOrgLevelUser_OrganizationUser_DoesNotSendNotification` | Verifies no notification for deleted org user when no org admin |
| `UserRolesUpdatedEvent_GivenOrgHasOrgLevelUser_SinglePracticeUser_SendsNotificationToOrgLevelUserAndImpactedUser` | Verifies both org admin and impacted user receive role update notification |
| `UserRolesUpdatedEvent_GivenOrgHasOrgLevelUser_MultiplePracticeUser_SendsNotificationToOrgLevelUserAndImpactedUser` | Verifies notifications for multi-practice role updates |
| `UserRolesUpdatedEvent_GivenOrgHasOrgLevelUser_OrganizationUser_SendsNotificationToOrgLevelUserAndImpactedUser` | Verifies notifications for org-level role updates |
| `UserRolesUpdatedEvent_GivenOrgDoesNotHaveOrgLevelUser_SinglePracticeUser_SendsNotificationToPracticeUsersAndImpactedUser` | Verifies practice users and impacted user receive notifications |
| `UserRolesUpdatedEvent_GivenOrgDoesNotHaveOrgLevelUser_MultiplePracticeUser_SendsNotificationToPracticeUsersAndImpactedUser` | Verifies multi-practice notification routing |
| `UserRolesUpdatedEvent_GivenOrgDoesNotHaveOrgLevelUser_OrganizationUser_SendsNotificationOnlyToImpactedUser` | Verifies only impacted user notified for org role changes |
| `UserRolesUpdatedEvent_GivenNoFullAccessUsers_SendsNotificationOnlyToImpactedUser` | Verifies fallback to impacted user when no full-access users exist |

## Lambda Unit Tests

### FgaTupleCreatorTests.cs (9 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `ConvertSqsUpdateToFgaTuple_WhenRelationshipAdded_ReturnsWriteTuple` | Verifies INSERT UserRole creates FGA Write tuple |
| `ConvertSqsUpdateToFgaTuple_WhenAppointmentRelationshipAdded_ReturnsWriteTuple` | Verifies INSERT Appointment creates FGA Write tuple with provider relation |
| `ConvertSqsUpdateToFgaTuple_WhenRelationshipDeleted_ReturnsDeleteTuple` | Verifies soft-deleted UserRole creates FGA Delete tuple |
| `ConvertSqsUpdateToFgaTuple_WhenAppointmentRelationshipDeleted_ReturnsDeleteTuple` | Verifies soft-deleted Appointment creates FGA Delete tuple |
| `ConvertSqsUpdateToFgaTuple_WhenRelationshipHardDeleted_ReturnsDeleteTuple` | Verifies REMOVE operation creates FGA Delete tuple |
| `ConvertSqsUpdateToFgaTuple_WhenAppointmentRelationshipHardDeleted_ReturnsDeleteTuple` | Verifies Appointment REMOVE creates FGA Delete tuple |
| `ConvertSqsUpdateToFgaTuple_WhenRelationshipUpdated_ReturnsWriteTuple` | Verifies MODIFY without deletion creates FGA Write tuple |
| `ConvertSqsUpdateToFgaTuple_WhenAppointmentRelationshipUpdated_ReturnsWriteTuple` | Verifies Appointment MODIFY creates FGA Write tuple |
| `ConvertSqsUpdateToFgaTuple_WhenUnexpectedActionType_ThrowsException` | Verifies exception thrown when both old and new DTOs are null |

### FgaUpdateServiceTests.cs (8 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `ProcessRecords_WhenParsingFails_ReturnsFailedMessageIds` | Verifies all messages returned as failures when parsing throws |
| `ProcessRecords_WhenUserVersionType_SkipsProcessing` | Verifies UserVersion model type is skipped (no FGA update needed) |
| `ProcessRecords_WhenProcessingSucceeds_ReturnsNoFailures` | Verifies successful processing returns empty failure list |
| `ProcessRecords_WhenFgaUpdateFails_ReturnsAllMessageIdsInGroup` | Verifies all messages in group fail when FGA update throws |
| `ProcessRecords_WhenMultipleModelTypes_ProcessesEachGroupSeparately` | Verifies different model types are batched and processed separately |
| `ProcessRecords_WhenMultipleModelTypesAndFirstFails_ProcessesSecondGroupSuccessfully` | Verifies failure in one group doesn't affect other groups |
| `ProcessRecords_HandlesAllModelTypesCorrectly` | Comprehensive test for all model types: UserRole, PracticeMember, OrganizationMember, Appointment, PracticeChurn, ScopedOrganizationMember |
| `ProcessRecords_WhenSomeFgaUpdatesFailInBatch_ReturnsCorrespondingMessageIds` | Verifies partial failure returns only failed message IDs |

### FgaUpdatesGeneratorTests.cs (4 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `CreateUpdate_WhenMultipleUpdatesForSameUserAndObject_TakesLastUpdate` | Verifies deduplication takes last update for same user/object/relation |
| `CreateUpdate_WhenMultipleUpdatesForDifferentUsers_KeepsAllUpdates` | Verifies updates for different users are all kept |
| `CreateUpdate_WhenMultipleUpdatesForSameUserDifferentObjects_KeepsAllUpdates` | Verifies updates for same user but different objects are kept |
| `CreateUpdate_WhenMultipleUpdatesForSameUserObjectDifferentRelations_KeepsAllUpdates` | Verifies different relations for same user/object are kept |

### FgaWriteClientTests.cs (6 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `UpdateTuples_GivenNoUpdates_ShouldNotCallFga` | Verifies empty update list doesn't call FGA API |
| `UpdateTuples_GivenSuccessfulWritesAndDeletes_ShouldReturnNoFailures` | Verifies successful writes and deletes return empty failure list |
| `UpdateTuples_WhenWritesAlreadyExist_ShouldNotReturnAsFailures` | Verifies idempotent writes (tuple exists) don't count as failures |
| `UpdateTuples_WhenDeletesDoNotExist_ShouldNotReturnAsFailures` | Verifies idempotent deletes (tuple doesn't exist) don't count as failures |
| `UpdateTuples_WhenSomeUpdatesFailWithOtherErrors_ShouldReturnFailedTuples` | Verifies actual FGA errors are returned as failures |
| `UpdateTuples_WhenFgaClientThrows_ShouldThrowException` | Verifies client exceptions are propagated |

### ActiveUserBackfillHandlerTests.cs (5 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `BackfillActiveUsers_WhenBackfillEntriesIsEmpty_ReturnsEmptyFailures` | Verifies empty backfill list doesn't call API |
| `BackfillActiveUsers_WhenSuccessful_CallsApiAndReturnsNoFailures` | Verifies successful backfill returns no failures |
| `BackfillActiveUsers_WhenPartialFailure_ReturnsFailedMessageIds` | Verifies partial failures return corresponding message IDs |
| `BackfillActiveUsers_WhenMultipleUsersFailure_ReturnsAllFailedMessageIds` | Verifies multiple user failures return all message IDs |
| `BackfillActiveUsers_WhenMultipleEntries_GroupedByUserId` | Verifies entries are grouped by user for API call |

### RoleBackfillServiceTests.cs (8 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `BackfillUserRoles_CallsActiveUserHandlerWithCorrectArguments` | Verifies practice roles are backfilled, org roles excluded |
| `BackfillUserRoles_GivenHandlerReturnsFailures_ReturnsFailedItems` | Verifies handler failures are propagated |
| `BackfillUserRoles_GivenAllRolesForUserWereDeleted_CallsDeletedUserHandler` | Verifies users with no roles trigger deleted user handler |
| `BackfillUserRoles_GivenDeletedUserHandlerReturnsFailures_ReturnsFailedItems` | Verifies deleted user handler failures are propagated |
| `BackfillUserRoles_WithOrgLevelPermissions_BackfillsToAllPracticesInOrgOnly` | Verifies org-level roles expand to all practices in org for V2 users |
| `BackfillUserRoles_WithOrgLevelPermissions_ButNotOnOrgExperience_DoesNotBackfillOrgRoles` | Verifies V1 users don't have org roles expanded |
| `BackfillUserRoles_WithOrgLevelPermissions_MixedWithPracticeLevelRoles_BackfillsNone` | Verifies inconsistent role states skip backfill |
| `BackfillUserRoles_WithOrgLevelPermissions_WhenHandlerReturnsFailures_ReturnsFailedItems` | Verifies org-level backfill failures are propagated |

### SqsEventParserTests.cs (8 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `ParseInsertUserVersionDto_ValidEvent_Success` | Verifies INSERT UserVersion parsing |
| `ParseInsertUserRoleDto_ValidEvent_Success` | Verifies INSERT UserRole parsing with audit metadata |
| `ParseModifyUserVersionDto_ValidEvent_Success` | Verifies MODIFY UserVersion parsing with old/new values |
| `ParseDeleteUserVersionDto_ValidEvent_Success` | Verifies REMOVE UserVersion parsing |
| `ParseUserVersionDto_Malformed_Fails` | Verifies malformed JSON throws SqsEventParsingException |
| `ParseUserVersionDto_ValidSqsMessage_RequestedWrongType_Fails` | Verifies type mismatch throws exception |
| `ParseUserVersionDto_ValidSqsMessage_InvalidModelTypeInSnsAttributes_Fails` | Verifies missing ModelType attribute throws exception |
| `ParseUserVersionDto_ValidSqsMessage_MissingSnsMessageAttributes_Fails` | Verifies missing MessageAttributes throws exception |

### SqsEventClassifierTests.cs (7 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `DetermineActionType_WhenNewDtoOnlyExists_ReturnsRelationshipAdded` | Verifies INSERT maps to RelationshipAdded |
| `DetermineActionType_WhenNewDtoIsDeletedAndOldDtoExists_ReturnsRelationshipDeleted` | Verifies soft delete maps to RelationshipDeleted |
| `DetermineActionType_WhenNewDtoUndeleted_ReturnsRelationshipAdded` | Verifies un-deletion maps to RelationshipAdded |
| `DetermineActionType_WhenNewDtoUpdatedNotDeleted_ReturnsRelationshipUpdated` | Verifies non-delete MODIFY maps to RelationshipUpdated |
| `DetermineActionType_WhenOldDtoOnly_ReturnsRelationshipHardDeleted` | Verifies REMOVE maps to RelationshipHardDeleted |
| `DetermineActionType_WhenInvalidState_ThrowsArgumentException` | Verifies null old and new DTOs throw exception |

## Service/Business Logic Unit Tests

### UserRolesServiceTests.cs (17 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `SetUserRolesGivenUserVersion_WhenUpdateSucceeds_ReturnsSuccess` | Verifies roles are persisted with correct user version |
| `GetUserRoles_WhenUserHaveRoles_ReturnsUserRoles` | Verifies user roles are fetched and mapped correctly |
| `GetUserRoles_ExcludesChurnedPractices` | Verifies churned practice roles are filtered when requested |
| `GetUserRoles_WhenUserHaveNoRoles_ReturnsEmptyList` | Verifies empty role list is returned for user with no roles |
| `GetUserRoles_WhenFilterSiblingPracticesImplicitRolesIsTrue_FiltersOutImplicitOrganizationRoles` | Verifies implicit org roles (isUserSetPermission=false) are filtered |
| `GetUserRoles_WhenFilterSiblingPracticesImplicitRolesIsTrue_DoesNotFilterExplicitRoles` | Verifies explicit org roles (isUserSetPermission=true) are preserved |
| `GetUserVersion_WhenUserHaveVersion_ReturnsUserVersion` | Verifies existing user version is returned without creating new |
| `GetUserVersion_WhenVersionDoesNotExist_CreatesInitialVersionAndReturnsZero` | Verifies new user version is created when missing |
| `QueryUserRolesByEntity_WhenEntityHasRoles_ReturnsAllRolesRegardlessOfIsUserSetPermission` | Verifies all roles returned regardless of permission source |
| `QueryUserRolesByEntity_WhenEntityHasNoRoles_ReturnsEmptyList` | Verifies empty list for entity with no roles |
| `QueryUserRolesByEntity_WhenFilterImplicitOrgRolesIsTrue_ExcludesImplicitOrgRoles` | Verifies implicit roles filtered, explicit preserved |
| `QueryUserRolesByEntities_WhenEntityHasRoles_ReturnsUserRolesWithIds` | Verifies bulk query returns roles for multiple entities |
| `QueryUserRolesByEntities_WhenEntityHasNoRoles_ReturnsEmptyList` | Verifies empty list for entities with no roles |

*Additional ~700 tests in practice-user-permissions - see [full analysis](practice-user-permissions.md)*

---

# provider-grouping (~200 tests)

## Lambda Tests

### ChangeStreamLambdaTests.cs (8 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `Verify_EntryPoint_Sets_Up_Correctly` | Verifies the ChangeStream Lambda entry point initializes correctly with fake services |
| `FunctionHandler_GivenOrganizationCreatedWithoutParent_DoesNotNotify` | Verifies no Kinesis notification is sent when an organization is created without a parent |
| `FunctionHandler_GivenOrganizationCreatedWithParent_SendsNotification` | Verifies Kinesis notification sent for org created with parent |
| `FunctionHandler_GivenOrganizationMemberCreated_SendsNotification` | Verifies membership change triggers Kinesis notification |
| `FunctionHandler_GivenOrganizationUpdated_SendsNotification` | Verifies org metadata update triggers Kinesis notification |
| `FunctionHandler_GivenOrganizationDeleted_SendsNotification` | Verifies org deletion triggers Kinesis notification |
| `FunctionHandler_GivenOrganizationMemberDeleted_SendsNotification` | Verifies member deletion triggers Kinesis notification |
| `FunctionHandler_GivenGroupEvent_SendsNotification` | Verifies group changes trigger Kinesis notification |

### StrategicLambdaHandlerTests.cs (1 test) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `HandlePracticeEvent_WhenDummyPractice_RemovesFromHierarchy` | Verifies dummy practices are removed, valid practices added, and irrelevant events filtered |

## API Integration Tests

### OrganizationApiTests.cs (50+ tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `GetOrganizationByOrganizationId_InvalidId_BadRequest` | Verifies 400 for invalid organization ID format |
| `GetOrganizationByOrganizationId_NotFound` | Verifies 404 for non-existent organization |
| `GetOrganizationByOrganizationId_GivenOrganizationExists_ShouldReturn` | Verifies org details returned correctly |
| `GetPracticesByOrganizationId_InvalidOrganizationId_BadRequest` | Verifies 400 for invalid org ID when fetching practices |
| `GetPracticesByOrganizationId_GivenOrganizationDoesNotExist_ShouldReturnEmpty` | Verifies empty list for non-existent organization |
| `GetPracticesByOrganizationId_GivenEntitiesExist_ShouldReturnEntities` | Verifies practice IDs returned for organization |
| `GetLineageForOrganization_InvalidOrganizationId_BadRequest` | Verifies 400 for invalid org ID when fetching lineage |
| `GetLineageForOrganization_GivenOrganizationDoesNotExist_ShouldReturnNotFound` | Verifies 404 for non-existent organization |
| `GetLineageForOrganization_OrganizationHasNoParents_ShouldReturnEmpty` | Verifies empty ancestor list for root organization |
| `GetLineageForOrganization_OrganizationHasParents_ShouldReturnLineage` | Verifies correct ancestor chain for nested organization |
| `GetFullHierarchyForOrganization_InvalidOrganizationId_BadRequest` | Verifies 400 for invalid org ID when fetching hierarchy |
| `GetFullHierarchyForOrganization_Success` | Verifies full hierarchy tree returned from any node |
| `CreateOrganization_NoJwt_ShouldReturnUnauthorized` | Verifies 401 when creating org without JWT |
| `CreateOrganization_BadJwt_ShouldReturnForbidden` | Verifies 403 for JWT with wrong role |
| `CreateOrganization_NonCsrUser_ShouldReturnForbidden` | Verifies 403 for provider JWT |
| `CreateOrganization_MissingSalesforceAccountId_ShouldReturnBadRequest` | Verifies 400 when salesforce_account_id field is missing |
| `CreateOrganization_InvalidParentOrganizationId_ShouldReturnBadRequest` | Verifies 400 for malformed parent org ID |
| `CreateOrganization_NonExistentParentOrganizationId_ShouldReturnConflict` | Verifies 409 when parent org doesn't exist |
| `CreateOrganization_ValidRequestBody_ShouldReturnOk` | Verifies successful org creation with all required fields |
| `UpdateOrganization_NoJwt_ShouldReturnUnauthorized` | Verifies 401 when updating org without JWT |
| `UpdateOrganization_NonExistentOrganizationId_ShouldReturnNotFound` | Verifies 404 when updating non-existent org |
| `UpdateOrganization_ValidRequestBody_ShouldReturnOk` | Verifies successful org name and type update |
| `UpdateOrganizationParent_NewParentOrganizationIdCreatesCyclicGraph_ShouldReturnConflict` | Verifies 409 when reparenting would create circular hierarchy |
| `UpdateOrganizationParent_InvalidToReparentOrgWithActivePracticeMembers_ShouldReturnConflict` | Verifies 409 when moving org with active practices to different hierarchy |
| `UpdateOrganizationParent_ValidRequestBody_ShouldReturnOk` | Verifies successful parent org update |
| `UpdateOrganizationMembershipForPractice_*` (12 tests) | Tests for single practice membership updates including auth, validation, add/remove/move scenarios |
| `BatchUpdateOrganizationMembershipForPractice_*` (8 tests) | Tests for batch practice membership updates including validation, size limits, partial failures |
| `QueryOrganizationsByName_*` (4 tests) | Tests for org name search including empty query, case-insensitivity, multiple matches |
| `DeleteOrganization_*` (6 tests) | Tests for org deletion including auth, validation, conflict when has members, successful delete |

## Persistence/Repository Tests

### GroupPersistenceTests.cs (10 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `Test_CreateGroup_MultiLevelOrganization` | Verifies groups are stored at specific org level, not visible from parent org queries |
| `Test_CreateUpdateAndDeleteGroup` | Full lifecycle test with history tracking for create, update, and delete operations |
| `GetGroupsByOrganizationId_GetAllGroupsByOrganizationId_Test` | Verifies querying groups by org ID with and without group type filter |
| `Test_GetAllDynamicGroups` | Verifies retrieval of all groups with dynamic rulesets across organizations |
| `Test_BatchGetGroupsByGroupId` | Verifies batch retrieval of groups by their IDs |
| `Test_CreateAndDeleteGroupMember` | Full lifecycle test for group members with history tracking |
| `Test_BatchCreateAndDeleteGroupMembers` | Verifies batch operations for creating and deleting multiple members with history |
| `GetGroupMembersByMemberEntity_GetAllGroupMembersByMemberEntity_Test` | Verifies querying group memberships by member entity across group types |
| `GetGroupMembersByGroupId_Test` | Verifies retrieving all members of specific groups |
| `GetGroupMembersByGroupIds_Test` | Verifies batch retrieval of members across multiple groups |

### OrganizationPersistenceTests.cs (18 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `Test_CreateAndGetOrganization` | Verifies organization creation and retrieval with history tracking |
| `Test_CreateAndGetStrategicOrganization` | Verifies strategic (Health System) organization creation with strategic ID |
| `Test_CreateDeleteCreateOrganization_PreservesSalesforceIdIfNull_OverwritesOtherMetadata` | Verifies salesforce ID preservation/overwrite logic when recreating deleted org |
| `Test_BatchGetOrganizationsByOrganizationIds` | Verifies batch org retrieval excludes deleted orgs |
| `Test_GetAllOrganizationsUnderUltimateParent` | Verifies retrieval of all child orgs under ultimate parent |
| `Test_CreateAndGetOrganizationByMember` | Verifies practice membership creation and retrieval with history |
| `Test_UpdateAndGetOrganization` | Verifies org update with history tracking |
| `Test_CreateAndGetPracticeByOrganization` | Verifies practice members returned for org, excluding deleted |
| `Test_CreateAndBatchGetPracticeByOrganization_MultipleOrganizations` | Verifies batch member retrieval across multiple orgs |
| `Test_DeleteOrganization` | Verifies org deletion cascades to members with history |
| `Test_UpdateAndGetPractice` | Verifies practice member update with history |
| `Test_ReplaceOrganizationMember` | Verifies moving practice between orgs creates delete then create history |
| `Test_GetAllOrganizationsAndMembersPreviouslySyncedFromSalesforce` | Verifies Salesforce-synced orgs and members retrieval including soft-deleted |
| `Test_ObtainingAndRemovingOrganizationUpdateLocks` | Verifies lock acquisition, conflict, and release semantics |
| `Test_ObtainingAndRemovingOrganizationMemberUpdateLocks` | Verifies member-level lock semantics |
| `Test_OrganizationUpdateLockExpiration` | Verifies expired locks can be acquired by new holder |
| `Test_QueryOrganizationByName` | Verifies name search with various query strings |

### OrganizationSyncServiceTests.cs (5 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `UpdateSalesforceOrganizations_CreatesNewOrganizations` | Verifies new Salesforce orgs are created with practice members |
| `UpdateSalesforceOrganizations_UpdatesExistingOrganizations` | Verifies existing orgs are updated and new members added |
| `UpdateSalesforceOrganizations_DeletesMissingOrganizations` | Verifies orgs missing from Salesforce are deleted |
| `UpdateSalesforceOrganizations_DeletesMissingOrganizationsAndIgnoresDeletedOrgsWhenTheyExist` | Verifies already-deleted orgs aren't re-deleted |
| `UpdateSalesforceOrganizations_DeleteAndRecreateOrganizationPreservesOrganizationIds` | Verifies org ID preserved when deleted and recreated from Salesforce |

## Unit Tests

### DeleteOrganizationImplTests.cs (6 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `DeleteOrganization_InvalidId_ReturnsBadRequest` | Verifies 400 for invalid organization ID format |
| `DeleteOrganization_OrgNotFound_ReturnsNotFound` | Verifies 404 when organization doesn't exist |
| `DeleteOrganization_HasPracticeMember_ReturnsConflict` | Verifies 409 when org has practice members |
| `DeleteOrganization_HasChildOrgMember_ReturnsConflict` | Verifies 409 when org has child organization members |
| `DeleteOrganization_NoMembers_ReturnsOk` | Verifies successful deletion when org has no members |
| `DeleteOrganization_FailedToObtainLock_Throws` | Verifies exception propagated when lock cannot be obtained |

### DtoTests.cs (13 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `OrganizationDto_HasExpectedKeyFields` | Verifies DynamoDB partition and sort key generation for organizations |
| `OrganizationHistoryDto_HasExpectedKeyFields` | Verifies history partition/sort keys include timestamp and action |
| `OrganizationMemberDto_HasExpectedKeyFields` | Verifies member DTO keys include GSI keys for reverse lookups |
| `OrganizationMemberHistoryDto_HasExpectedKeyFields` | Verifies member history keys support both org-based and member-based queries |
| `GroupDto_HasExpectedKeyFields` | Verifies group DTO keys include GSI for org-based queries |
| `GroupDto_SerializeAndUnserialize_ShouldHaveSameRules` | Verifies ruleset survives JSON serialization round-trip |
| `GroupDto_DtoAndBack_HasExpectedInclusionsAndExclusions` | Verifies manual inclusion/exclusion lists preserved through DTO conversion |
| `GroupHistoryDto_HasExpectedKeyFields` | Verifies group history keys support org-based timeline queries |
| `GroupMemberDto_HasExpectedKeyFields` | Verifies member DTO GSI enables member-centric queries |
| `GroupMemberHistoryDto_HasExpectedKeyFields` | Verifies member history supports both group and member queries |
| `ArrayIntersectionRule_DtoConversionAndBackShouldBeEqual` | Verifies complex intersection ruleset survives DTO conversion |
| `ProviderBasicRule_DtoAndBackShouldBeEqual` | Verifies provider rule survives DTO conversion |
| `LocationBasicRule_DtoAndBackShouldBeEqual` | Verifies location rule survives DTO conversion |

### GroupServiceTests.cs (6 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `UpdateGroupMembers_NewMembersNotInsideOrganization_Throws` | Verifies exception thrown when adding members outside the organization |
| `UpdateGroupMembers_NewMembersInsideOrganization_ExpectedFlow` | Verifies members added and removed correctly when validation passes |
| `DeleteGroup_GroupNotEmpty_Throws` | Verifies exception when deleting group with existing members |
| `DeleteGroup_GroupEmpty_ExpectedFlow` | Verifies successful group deletion when empty |
| `GetAllGroupsByOrganizationId_NoExpandHierarchy_FetchesGroups` | Verifies groups fetched for single org without hierarchy expansion |
| `GetAllGroupsByOrganizationId_ExpandHierarchy_FetchesGroups` | Verifies groups fetched for org and all descendants with hierarchy expansion |

### GroupSyncServiceTests.cs (5 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `DeleteOrganizationGroups_LockDoesNotMatch_Throws` | Verifies exception when update lock doesn't match organization |
| `DeleteOrganizationGroups_GroupsToDeleteFound_ExpectedFlow` | Verifies all group members deleted before groups when deleting org groups |
| `DeleteGroupMembershipForDeletedPractice_LockDoesNotMatch_Throws` | Verifies exception for mismatched lock |
| `DeleteGroupMembershipForDeletedPractice_ValidIdsPassed_ExpectedFlow` | Verifies correct members removed across all group types when practice deleted |
| `DeleteGroupMembershipForDeletedPractice_MalformedProvLocId_GroupMemberDeleted` | Verifies malformed provider-location IDs are still cleaned up |

### OrganizationServiceTests.cs (16+ tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `GetOrganizationMembersByOrganizationId_NoExpandHierarchy_CorrectlyPassesThroughParameters` | Verifies parameters passed to persistence without hierarchy expansion |
| `GetOrganizationMembersByOrganizationId_ExpandHierarchy_Works` | Verifies batch fetch includes all descendant org IDs |
| `GetOrganizationByOrganizationId_CorrectlyPassesThroughParameters` | Verifies org ID passed to persistence |
| `GetOrganizationMembershipByPracticeId_CorrectlyPassesThroughParameters` | Verifies practice ID passed to persistence |
| `BatchGetOrganizationMembershipByPracticeIds_ReturnsProperDictionary` | Verifies dictionary includes null for not-found practices |
| `CreateOrganization_CorrectlyPassesThroughParameters` | Verifies org created with self-referencing parent/ultimate parent |
| `CreateOrganization_WithNonExistentParentOrgId_Throws` | Verifies exception for non-existent parent |
| `CreateOrganization_WithParentOrgId_CorrectlyPassesThroughParameters` | Verifies org inherits ultimate parent from parent org |
| `UpdateOrganization_CorrectlyPassesThroughParameters` | Verifies name and type updates persisted |
| `UpdateOrganization_WithNonExistentOrgId_Throws` | Verifies exception for non-existent org |
| `UpdateOrganizationParent_ChangesUltimateParentOrgOfActiveOrg_Throws` | Verifies exception when moving org with active practices to different hierarchy |
| `UpdateOrganizationParent_CorrectlyPassesThroughParametersAndNotifies` | Verifies parent update persisted correctly |

### OrganizationGraphValidationServiceTests.cs (2 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `IsNewParentCyclic_Test` | Parameterized test with 16 cases verifying cycle detection in org hierarchy |
| `IsNewParentCyclic_ThrowsWhenMaximumDepthExceeded` | Verifies exception when hierarchy depth exceeds maximum allowed |

### OrganizationHierarchyServiceTests.cs (4 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `GetAllDescendantOrganizations_RetrievesOrganizations` | Verifies all child and grandchild orgs retrieved |
| `GetAllAncestorOrganizations_RetrievesMultiLevelHierarchies` | Verifies ancestor chain retrieved for orgs at each hierarchy level |
| `GetFullOrganizationHierarchy_Test` | Verifies complete hierarchy tree structure built correctly |
| `GetUltimateParentOrganization_Test` | Verifies ultimate parent returned for orgs at any hierarchy level |

### RuleServiceTests.cs (17 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `ProviderBasicRule_CheckRule` | Verifies provider attribute matching logic |
| `LocationBasicRule_CheckRule` | Verifies location attribute matching logic |
| `ProviderLocationBasicRule_CheckRule` | Verifies provider-location mapping attribute matching |
| `ProviderLocationBasicRule_ProviderAttributeCheckRule` | Verifies provider attributes can be checked on provider-location entities |
| `IntersectionOnlyRule_CheckRuleTest` | Verifies AND logic for multiple rule intersection |
| `RulesEngine_ApplyRuleset_ReturnsValid` | Verifies ruleset application returns matching entity IDs |
| `RulesEngine_ApplyRuleset_EmptyRuleset` | Verifies empty ruleset returns all entities |
| `RulesEngine_ApplyManualInclusionsAndExclusions_ReturnsValid` | Verifies manual inclusion/exclusion override rules |
| `RulesEngine_FilterInactiveEntities_FiltersProviders` | Verifies disassociated providers filtered out |
| `RulesEngine_FilterInactiveEntities_FiltersLocations` | Verifies inactive locations filtered out |
| `RulesEngine_FilterInactiveEntities_FiltersProviderLocations` | Verifies inactive provider-location mappings filtered out |
| `GroupMembershipCalculator_GetFilteredMembers_RulesButNoManualIncExc_ReturnsValid` | Verifies rule-only membership calculation |
| `GroupMembershipCalculator_GetFilteredMembers_RulesAndManualIncExc_ReturnsValid` | Verifies combined rules and manual overrides |
| `GroupMembershipCalculator_GetFilteredMembers_NoChanges` | Verifies unchanged membership scenario |
| `GroupMembershipCalculator_GetFilteredMembers_RemovesInactive` | Verifies inactive entities excluded from membership |
| `MembershipDifferenceCalculator_CompareMembersToGroupMembers_ReturnsValid` | Verifies correct additions and removals calculated |

### StrategicBackfillWorkerTests.cs (9 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `ExecuteAsync_WithStrategicPractices_UpdatesStrategicMetadataAndPractices` | Verifies worker updates strategic metadata and practice mappings for each strategic ID |
| `ExecuteAsync_WithParentStrategic_UpdatesParentStrategicMetadata` | Verifies parent strategic metadata also updated when practice has parent strategic |
| `ExecuteAsync_WithNoStrategicPractices_DoesNotUpdateStrategicMetadata` | Verifies no updates when practices have no strategic IDs |
| `ExecuteAsync_WhenExceptionOccurs_LogsErrorAndContinues` | Verifies errors logged and processing continues |
| `ExecuteAsync_WithEmptyBatch_AdvancesIterator` | Verifies iterator advanced even when batch is empty |
| `ExecuteAsync_WithPracticeRemovedFromStrategicOrg_RemovesPracticeMapping` | Verifies practice removed from strategic hierarchy when no longer strategic |
| `ExecuteAsync_WithPracticeRemovedFromNonStrategicOrg_DoesNotRemoveMappings` | Verifies non-strategic org practices not affected |
| `ExecuteAsync_WithPracticeNotMappedToOrg_DoesNothing` | Verifies no action for practices without org membership |
| `ExecuteAsync_WithDummyPracticeInHierarchy_RemovesFromHierarchy` | Verifies dummy strategic parent practices removed from hierarchy |

### SnsServiceTests.cs (4 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `PublishEvent_OrgMetadataEvent_IncludesOrganizationTypeAttribute` | Verifies org metadata events include organization type in SNS attributes |
| `PublishEvent_OrgMetadataEvent_FallsBackToOldDataType_WhenNewDataIsNull` | Verifies org type from old data used when new data is null |
| `PublishEvent_OrgMembershipEvent_IncludesOrganizationTypeAttribute` | Verifies membership change events include org type attribute |
| `PublishEvent_GroupEvent_DoesNotIncludeOrganizationTypeAttribute` | Verifies group events don't include organization type attribute |

### WebDtoTests.cs (4 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `OrganizationType_ConvertsToWebEnumSuccessfully_ForAllValues` | Verifies all internal OrganizationType values map to web enum |
| `OrganizationType_ConvertsToDtoEnumSuccessfully_ForAllValues` | Verifies all web OrganizationType values map back to internal enum |
| `GroupMemberType_ConvertsToWebEnumSuccessfully_ForAllValues` | Verifies all internal GroupMemberType values map to web enum |
| `GroupMemberType_ConvertsToDtoEnumSuccessfully_ForAllValues` | Verifies all web GroupMemberType values map back to internal enum |

---

# provider-join-service (~300 tests)

## Lambda Tests

### FunctionTest.cs (1 test) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `TestReturnsId` | Verifies the Abandonment Lambda function handler returns the DynamoRowId from the payload |

### FunctionTest.cs (2 tests) - Functional

| Test Name | What It Tests |
|-----------|---------------|
| `FunctionHandler_GivenTestString_LogsLeadSuccessfullyCreated` | Verifies successful abandonment lambda processing with Salesforce lead creation |
| `FunctionHandler_GivenTestString_LogsLeadUpdateFailed` | Verifies error handling when Salesforce lead creation fails |

## Service Unit Tests

### SignUpServiceTest.cs (13 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `GetUserAgreementAsync_ThrowsSelfSignupNotFoundException_GivenLeadDoesntExist` | Verifies exception when getting agreement for non-existent lead |
| `GetUserAgreementAsync_CorrectlyReturnsUserAgreement_GivenLeadExists` | Verifies user agreement PDF returned for existing lead |
| `GetLeadAsync_ShouldThrow_WhenLeadNotFound` | Verifies SelfSignupNotFoundException for missing lead |
| `GetLeadAsync_ShouldNotThrow_WhenLeadFound` | Verifies no exception when lead exists |
| `UpdateExecutionArn_ShouldSave` | Verifies step function execution ARN saved to lead |
| `GetExecutionArn_ShouldReturnArn` | Verifies step function execution ARN retrieval |
| `UpdateSignUpPortalLeadStatusAsync_ShouldSubmitNewStatus` | Verifies lead status update by lead ID |
| `UpdateSignUpPortalLeadStatusAsync_ShouldThrowNotFound_WhenTheLeadNotExist` | Verifies exception for non-existent lead |
| `UpdateSignUpPortalLeadStatusWithPracticeAsync_ShouldSubmitNewStatus` | Verifies lead status update by practice ID for various statuses |
| `UpdateSignUpPortalLeadStatusWithPracticeAsync_SameStatus_ShouldNotUpdate` | Verifies no update when status unchanged |
| `UpdateSignUpPortalLeadStatusWithPracticeAsync_ShouldNotUpdateFromSpecificStatus` | Verifies SignupCompleted status not overwritten |
| `UpdateSignUpPortalLeadStatusWithPracticeAsync_ShouldThrowNotFound_WhenTheLeadNotExist` | Verifies exception for non-existent practice |

### SignupPortalServiceTest.cs (3 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `UpsertLeadAsync_Should_Create` | Verifies new lead creation with expiration date |
| `UpsertLeadAsync_Should_Update` | Verifies existing lead update clears expiration date |
| `UpsertLeadAsync_ShouldNoUpdate_WhenNotInEmailErrorAbandonState` | Verifies update blocked for leads not in EmailErrorAbandon state |

### InsuranceOnboardingServiceTest.cs (10 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `CreateInsuranceOnboardingEntryAsync_Should_CreateAnyOnboardingWith_PracticeId` | Verifies insurance entry creation with practice ID and eligibility flag |
| `CreateInsuranceOnboardingEntryAsync_Should_CreateAnyOnboardingWith_MainSpecialty` | Verifies insurance entry creation with main specialty |
| `GetOnboardEligibilityStatus_ReturnsExpectedResult_Given` | Verifies status mapping based on DDB status and eligibility flag |
| `GetOnboardEligibilityStatus_InsuranceEntityOverload_ReturnsExpectedResult_Given` | Verifies status mapping from InsuranceOnboardingInfo entity |
| `GetOnboardEligibilityStatus_ReturnsEntryNotFound_GivenEntryIsNull` | Verifies EntryNotFound when DDB returns null |
| `SaveOnboardingInfoAsync_SavesInsuranceOnboardingInfoOnDdbGivenNothingIsNull` | Verifies complete insurance info saved to DDB |
| `SaveOnboardingInfoAsync_SavesInsuranceOnboardingInfoOnDdbGivenPropsAreNull` | Verifies partial insurance info saved with null properties |
| `GetInsuranceOnboardingInfoAsync_ShouldRetrieveEntitySuccessfully` | Verifies insurance info retrieval and conversion |
| `GetInsuranceOnboardingInfoAsync_ShouldReturnNull_GivenEntityDoesNotExist` | Verifies null returned for non-existent entity |
| `UpdateInNetworkEligibilityAsync_ShouldUpdateInNetworkEligibilityInfo` | Verifies in-network eligibility update |

### SalesforceRepositoryTest.cs (4 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `GetLeads_Should_SearchByPhoneNumber` | Verifies lead search by phone number |
| `GetLeads_Should_SearchByEmail` | Verifies lead search by email |
| `GetLeads_Should_SearchByEmailAndPhone` | Verifies combined phone and email search |
| `GetLeads_Should_NotReturnDuplicates` | Verifies duplicate leads filtered from combined search |

### LeadDdbDtoFactoryTest.cs (3 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `CreateSupplementalSignUpRequest_GivenGoodRequestBody_ShouldCreateLead` | Verifies all lead properties correctly mapped from signup request |
| `CreateSupplementalSignUpRequest_GivenNullSpecialtyMapping_ShouldCreatedLead` | Verifies null specialty mapping handled |
| `CreateSupplementalSignUpRequest_GivenEmailWithWhitespaces_ShouldCreatedLead` | Verifies email whitespace trimming |

### LocationHelperTests.cs (1 test) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `GetStateCode_Should_Return_Expected_StateCode_When_ZipCode_Given` | Verifies state code lookup from zip code CSV (handles null, whitespace, trim) |

### ProviderSetupServiceClientTest.cs (2 tests) - Unit

| Test Name | What It Tests |
|-----------|---------------|
| `CreateOnboardingPractice_CallsHttpClient` | Verifies POST request to create onboarding practice |
| `CreateOnboardingPractice_Should_NotThrow_ProviderSetupServiceApiException_GivenStatusCodeIsNotASuccessStatusCode` | Verifies no exception for error status codes on create |

## Integration Tests

### AccountCreationTests.cs (13 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `CreateAccount_InternalServerError` | Verifies InternalServerError propagation from monolith |
| `CreateAccount_ShouldReturnCreated_If_HttpClientReturnsCreated` | Verifies account creation updates DDB with practice info |
| `CreateAccount_ShouldReturnUnauthorized_If_HttpClientReturnsUnauthorized` | Verifies Unauthorized propagation |
| `CreateAccount_ShouldReturnLocked_If_HttpClientReturnsLocked` | Verifies Locked status propagation |
| `CreateAccount_ShouldReturnNotFound_If_TheIdDoesNotExist` | Verifies NotFound for non-existent lead |
| `EmailConfirmation_ShouldReturnOk_If_HttpClientReturnsSuccess` | Verifies email confirmation status retrieval |
| `EmailConfirmation_ShouldReturnBadRequest_If_LeadIdIsNotPresent` | Verifies BadRequest for invalid lead ID |
| `EmailConfirmation_ShouldReturnInternalServerError_If_HttpClientReturnsFailure` | Verifies InternalServerError propagation |
| `ResendEmailConfirmation_ShouldLimitRequests` | Verifies rate limiting on email resend (max 5 per minute) |
| `UpsertOnboardingPractice_Should_Return_NoContent_If_PracticeExist` | Verifies NoContent for existing practice update |
| `UpsertOnboardingPractice_Should_Return_Created_If_Practice_DoesNot_Exist` | Verifies Created for new practice creation |
| `CreatePractice_ShouldReturnCreated_If_HttpClientReturnsCreated` | Verifies practice creation updates DDB |
| `CreatePractice_ShouldReturnNotFound_If_TheIdDoesNotExist` | Verifies NotFound for non-existent lead |

### InsuranceWizardTest.cs (24 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `GetInsuranceSetup_RespondsOkWithInsuranceData_GivenExistingPracticeCloudId_NotComplete` | Verifies GET returns minimal insurance data for NotComplete status |
| `GetInsuranceSetup_RespondsOkWithInsuranceData_GivenExistingPracticeCloudId_Complete` | Verifies GET returns full insurance data for Complete status |
| `GetInsuranceSetup_RespondsNotFound_GivenNoDataExistsForPracticeCloudId` | Verifies NotFound for non-existent practice |
| `GetInsuranceSetup_RespondsUnauthorized_GivenUserCannotEditPractice` | Verifies Unauthorized without JWT |
| `GetInsuranceSetup_RespondsForbidden_GivenUserCannotEditPractice` | Verifies Forbidden for different practice JWT |
| `CreateInsuranceSetup_Responds_Created` | Verifies Created for Complete, NotComplete, RequiresAdvancedMapping, NotEligible statuses |
| `CreateInsuranceSetup_Responds_Created_GivenUserIdentificationIsNotPassed` | Verifies Created without username/professional ID |
| `CreateInsuranceSetup_Responds_Created_WhenEntryNotFound_AndBodyHasMainSpecialty` | Verifies Created when no entry but body has specialty |
| `CreateInsuranceSetup_Responds_Conflict_Given` | Verifies Conflict for Complete/RequiresAdvancedMapping existing entries |
| `CreateInsuranceSetup_Responds_NotFound_GivenNoEntryMatchesId` | Verifies NotFound for non-existent entry |
| `CreateInsuranceSetup_Responds_BadRequest_OnAutomaticDtoValidation_GivenIsCompleteIstrue` | Verifies BadRequest with validation errors for complete status missing required fields |
| `CreateInsuranceSetup_Creates_GivenValuesAreNull_AndIsCompleteIsFalse` | Verifies creation with null values for not_complete |
| `CreateInsuranceSetup_Creates_DoesNot_Overwrite_States` | Verifies existing states not overwritten |
| `CreateInsuranceSetup_Creates_OverWrites_Empty_States` | Verifies empty states can be overwritten |
| `CreateInsuranceSetup_RespondsUnauthorized_GivenUserCannotEditPractice` | Verifies Unauthorized for PUT without JWT |
| `CreateInsuranceSetup_RespondsForbidden_GivenUserCannotEditPractice` | Verifies Forbidden for PUT with wrong practice JWT |
| `GetInsuranceOnboardingStatus_RespondsOkWithCorrespondingStatus_GivenIsEligibleIsTrue` | Verifies status mapping for eligible practices |
| `GetInsuranceOnboardingStatus_RespondsOkWithNotEligible_GivenIsEligibleIsFalse` | Verifies NotEligible for ineligible practices |
| `GetInsuranceOnboardingStatus_RespondsOkWithNotEligible_GivenNoMainSpecialty` | Verifies NotEligible when no main specialty |
| `GetInsuranceOnboardingStatus_RespondsWithNotFound_GivenNoEntryExists` | Verifies NotFound for non-existent entry |
| `PutIsInNetwork_RespondsNoContent_WhenInfoSaveSuccessfully` | Verifies NoContent for in-network update |

### LeadRetrievalTest.cs (10 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `GetSignUpData_ShouldReturnOK_IfLeadExists` | Verifies OK with lead data for existing lead |
| `GetSignUpData_ShouldReturnOK_WithIncomplete_IfSubmitted` | Verifies lead state after Salesforce submission |
| `GetSelfSignUpDataByPracticeId_ShouldReturnOK_IfLeadWithPractice_Exists` | Verifies retrieval by practice ID |
| `GetSelfSignUpDataByPracticeId_ShouldReturnNotFound_IfLeadWithPractice_DoesNotExists` | Verifies NotFound for missing practice lead |
| `GetSelfSignUpDataByPracticeIdBehindAuth_ShouldReturnOK_IfLeadWithPractice_Exists` | Verifies authenticated retrieval for practice, selfsignup, and CSR users |
| `GetSelfSignUpDataByPracticeIdBehindAuth_ShouldReturnNotFound_IfLeadWithPractice_DoesNotExists` | Verifies NotFound for authenticated missing lead |
| `GetSelfSignUpDataByPracticeIdBehindAuth_ShouldReturnForbidden_ForWrongRoles` | Verifies Forbidden for patient and wrong CSR roles |
| `GetSelfSignUpDataByPracticeIdBehindAuth_ShouldReturnForbidden_ForDifferentIds` | Verifies Forbidden when practice IDs don't match |
| `GetSelfSignUpDataByPracticeIdBehindAuth_ShouldReturnUnauthorized` | Verifies Unauthorized without JWT |

### SignUpFlowTest.cs (9 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `Should_CreateNewLead` | Verifies complete lead creation and Salesforce submission flow |
| `CreateNewLead_ShouldCreate_SpecialMappingCouldBeNull` | Verifies lead creation with null or populated specialty mapping |
| `Verify_DuplicateEnum_WritesDuplicate_In_DynamoDb` | Verifies Duplicate status persisted correctly |
| `Verify_SignUpCompleteLead_DoesNotReSubmit` | Verifies Locked returned for duplicate submission |
| `Verify_SubmittedNonCRM_ThrowsLeadLockedException` | Verifies Locked for abandoned then completed flow |
| `UpdateSignupPortalLeadStatus_Success` | Verifies lead status update with proper JWT |
| `UpdateSignupPortalLeadStatus_BadRequest` | Verifies BadRequest for null status |
| `UpdateSignupPortalLeadStatus_UnAuthorized` | Verifies Unauthorized without JWT |
| `UpdateSignupPortalLeadStatus_Forbidden` | Verifies Forbidden for wrong practice JWT |

### LocalStackDemoRequestTests.cs (4 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `CreateSignupPortalRequestDemoLead_ShouldCreateLead` | Verifies demo lead creation with Salesforce submission |
| `CreateSignupPortalRequestDemoLead_Should_Return_BadRequest_When_PhoneNumber_Is_Invalid` | Verifies phone validation error response |
| `CreateSignupPortalRequestDemoLead_Should_Return_BadRequest_When_Email_Is_Invalid` | Verifies email validation error response |
| `CreateSignupPortalRequestDemoLead_Should_Return_BadRequest_When_PracticeName_CharCount_GreaterThan_50` | Verifies practice name length validation |

### LocalStackDynamoDbTests.cs (3 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `UpdateLead_ShouldRemoveExpirationDate` | Verifies nullable field removal when set to null |
| `GetLead_SupplementalSignupLeadStatus_ShouldSetValue` | Verifies NewSignupLeadStatus enum persistence |
| `SurveyMarketingChannel_CreateAndGet_ShouldWorkAsExpected` | Verifies SurveyMarketingChannel enum persistence |

### UserAgreementTests.cs (3 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `GetUserAgreement_ReturnsNotFound_GivenLeadDoesNotExist` | Verifies NotFound for non-existent lead |
| `GetUserAgreement_RespondsInternalServer_GivenMonolithRespondsUnauthorized` | Verifies InternalServerError for monolith auth failure |
| `GetUserAgreement_GetsRespondsWithPdf_GivenMonolithRespondsWithPdf` | Verifies PDF response with correct content type |

### CcpaTest.cs (2 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `RequestGongDeletion_ShouldReturn_Unauthorized` | Verifies Unauthorized without CSR JWT |
| `RequestGongDeletion_ShouldReturn_Ok` | Verifies OK with CSR JWT and Gong response |

### ClaimProfileTest.cs (2 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `ShouldReturn_BadRequest_ForIncorrectBody` | Verifies BadRequest for empty required fields |
| `ShouldReturn_Created_ForCorrectBody` | Verifies Created for valid claim profile removal |

### PostSubmissionUpdatesTest.cs (2 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `TriggerStepFunction_ShouldReturnOK_WhenTriggerStepFunctionSuccessful` | Verifies OK when step function triggered |
| `TriggerStepFunction_ShouldReturnNotFound_WhenNoSuchLeadExist` | Verifies NotFound for non-existent lead |

### PricingTest.cs (2 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `SelfSignupPortal_ShouldReturn_Price_With_StatusCode_Ok` | Verifies pricing retrieval for known specialty |
| `SelfSignupPortal_ShouldReturn_Default_When_Specialty_NotFound_With_StatusCode_Ok` | Verifies default pricing for unknown specialty |

---

# Cypress E2E Tests (75 tests)

## user-management-smoke.spec.js (9 tests)

| Test Name | What It Tests |
|-----------|---------------|
| `should create a user with API response verification` | Fills add user form in iframe (first name, last name, email), verifies "Full access" pre-selected, clicks save, intercepts POST to `/api/provider/v1/organization-user/staff-user`, validates 201 response with `staff_id`, verifies user appears in table |
| `should display user management page with users table` | Navigates to `/provider/settings/users`, verifies iframe exists with `practice-users-page-container-v2` element |
| `should display add user button when practice is self sign up complete` | Verifies "Add another user" button is visible and enabled in settings iframe |
| `should navigate to add user page when add button is clicked` | Clicks "Add another user", verifies first name input appears |
| `should display account settings link` | Verifies account settings link exists with href containing `/provider/settings/password` |
| `should display pagination when there are multiple pages of users` | Checks if pagination element `users-page-bottom` is visible when multiple pages exist |
| `should allow clicking on user row to view user details` | Clicks first user row, verifies detail view loads |
| `should edit a user with API response verification` | Opens user, changes from full access to custom permissions, selects "Practice settings", intercepts PUT to `/practice-user-permissions/v1/user/*/roles`, validates 204 response, verifies toast |
| `should delete a user with API response verification` | Clicks Delete, confirms in modal, intercepts DELETE to `/api/provider/v1/organization-user/*`, validates 204, verifies user removed from table |

## rbac-smoke.spec.js (10 tests)

| Test Name | What It Tests |
|-----------|---------------|
| `Appts user - Verify landing page is Inbox` | Logs in as appointments-only user, verifies inbox landing, tests calendar/dashboard/report navigation, tests dropdown functionality, signs out |
| `Verify certain pages are inaccessible for Appts user` | Verifies SPO page redirects to inbox, providers page shows error, intercepts 403 on add provider API |
| `Appts+PS user - Verify landing page is Inbox` | Logs in as practice settings + appointments user, tests all accessible pages (calendar, providers, dashboard, settings tabs), signs out |
| `Verify certain pages are inaccessible for Appts+PS user` | Verifies SPO redirects, users page shows error, website settings redirects |
| `Verify Billing user lands on Performance dashboard` | Logs in as billing user, verifies dashboard landing, tests accessible pages, signs out |
| `Verify that Billing user is unable to access certain pages` | Verifies calendar redirects, providers error, COVID/video visit blocked |
| `Verify Practice settings user lands on Provider's page` | Logs in as practice settings user, verifies providers landing, tests accessible settings tabs |
| `Verify non-visibility of certain pages for Practice user` | Verifies home/calendar/inbox tabs don't exist, calendar URL redirects |
| `Verify visibility of pages for SPO user access` | Logs in as SPO user, verifies SPO dashboard landing, only password/legal tabs visible |
| `Verify certain pages not accessible for SPO user` | Verifies navbar tabs hidden, URLs redirect to SPO dashboard, providers shows error |

## practicemgmt-smoke.spec.js (24 tests)

| Test Name | What It Tests |
|-----------|---------------|
| `Verifying auto-population when user enters valid NPI` | Enters NPI (1477715670), verifies first name "Gabriella", last name "Gellrich", specialty, suffix "MD" auto-populate |
| `Verify Practice Settings User can add and remove insurance carriers` | Adds insurance via multi-step flow, verifies toast, edits to remove Aetna, verifies completion |
| `Verify can access insurance settings from Settings menu` | Clicks insurance tab, verifies URL contains `/provider/settings/insurance` |
| `Verify can access and interact with Providers page` | Tests Role/Status filters, applies filters, uses search, verifies filtered results |
| `Verify can access provider profile from Providers page` | Clicks provider row, verifies navigation to profile settings |
| `Verify can navigate to Providers page via header icon` | Clicks providers-and-staff header icon, verifies URL |
| `Verify can access Visit Reasons settings` | Clicks visit reasons tab with GQL intercept, verifies URL |
| `Verify can access VR Presets page` | Visits presets page, dismisses modal, clicks review/save, verifies error message |
| `Verify can interact with VR length inputs` | Searches "illness", verifies visit reason elements appear |
| `Verify can access Performance Dashboard` | Visits dashboard, verifies URL and navbar button |
| `Verify can navigate to Performance Dashboard from navbar` | Clicks performance dropdown, clicks dashboard link |
| `Verify Homepage is Providers page after login` | Fresh login flow, verifies landing URL is providers-and-staff |
| `Verify can access Practice settings via dropdown` | Clicks username, clicks settings, verifies URL |
| `Verify can access available settings tabs` | Tests password, practice, VR, insurance, user agreement tabs; verifies restricted tabs don't exist |
| `Verify cannot access restricted pages` | Verifies calendar/inbox/home icons don't exist, calendar URL redirects |
| `Verify Invite option in dropdown menu` | Tests invite navigates to `/provider/config/invite` |
| `Verify Add Provider option in dropdown menu` | Tests add provider navigates to `/provider/setup/add` |
| `Verify Settings option in dropdown menu` | Tests settings navigates to `/provider/settings/practice` |
| `Verify Features option in dropdown menu` | Tests features navigates to `/provider/features` |
| `Verify Help Center option in dropdown menu` | Tests help center navigates to `/provider-help/` |
| `Verify Contact Us option in dropdown menu` | Tests contact us navigates to `/provider/config/contact` |
| `Verify Sign Out functionality` | Clicks sign out, verifies URL contains `signin` |
| `Verify can access provider profile settings` | Clicks COVID-19 link, verifies screener settings navigation |
| `Verify can view provider specialties section` | Visits provider profile, checks specialties/visit-reasons edit buttons visible |

## spomgmt-smoke.spec.js (5 tests)

| Test Name | What It Tests |
|-----------|---------------|
| `should display provider groups tab with table and controls` | Verifies tabs, create button, table headers (Provider group, Off/On, Current Bid), toggle switches |
| `should display trends tab with filters` | Verifies date range dropdown ("Today"), provider group dropdown |
| `should navigate between tabs` | Clicks between provider-groups and trends tabs, verifies URL hashes |
| `should navigate back to dashboard from campaign page` | Clicks back button from campaign creation, verifies return to dashboard |
| `should complete full campaign lifecycle: create, edit, pause, delete` | Creates campaign with name/specialty/location/bid, edits bid level, toggles pause, deletes campaign, verifies removal |

## billingmgmt-smoke.spec.js (1 test)

| Test Name | What It Tests |
|-----------|---------------|
| `Viewing and Checking Billing and Account Related functionality` | Tests full billing flow: adds ACH payment (replace), adds second account, edits rollovers, adjusts position, deletes accounts, verifies invoice PDF download link, navigates to Understanding Your Bill |

## appointmentmgmt-smoke.spec.js (17 tests)

| Test Name | What It Tests |
|-----------|---------------|
| `Book an appointment for Inbox Testing` | Clicks available timeslot, handles modal if present, clicks book, verifies URL |
| `Verify can confirm an appointment` | Finds new booking, clicks confirm, intercepts API, validates 200, verifies toast, checks persistence |
| `Verify can reschedule an appointment` | Opens modify appointment, changes time/provider, intercepts API, validates 200, verifies provider changed |
| `Verify can delete an appointment` | Opens cancel appointment, steps through flow, verifies row removed |
| `Verify can send manual intake request` | Fills manual intake form, intercepts 201, verifies row appears with "Confirmed" status, deletes submission |
| `Verify can use filters in the Inbox` | Applies provider/location filters, verifies localStorage, tests across tabs, clears filters |
| `Verify tutorial works in Inbox` | Steps through 6-step tutorial (notifications, sidebar, pills, details, actions, tour) |
| `Verify can access all tabs in Inbox` | Clicks through new-bookings, reschedules, cancellations, intake-submissions tabs |
| `Verify can access patient record page and calendar` | Navigates to patient record, returns, views in calendar, verifies appointment card |
| `Verify header count equals sum of sidebar counts` | Extracts sidebar counts, calculates sum, asserts header badge matches |
| `Verify can access Dashboard` | Navigates to dashboard, verifies metrics visible, restricted sections hidden, tests date filter |
| `Verify can access Appointment Report` | Verifies 6 filter dropdowns, dashboard statistics labels, reset filters, date range, booking report modal |
| `Verify tutorial works in Calendar` | Completes 6-step calendar tutorial |
| `Verify can access Calendar from Inbox` | Clicks calendar icon, verifies API 200, tests view toggles, date navigation, filters |
| `Can add and view busy block` | Adds exclusion via GraphQL, verifies "Busy" text visible |
| `Can remove busy block` | Removes exclusion via GraphQL, verifies block removed |
| `Can add and view one time availability` | Adds availability template via GraphQL, verifies time range displayed |
| `Can remove availability` | Deletes template via GraphQL, verifies block removed |

## provider-providerspage-regression.spec.js (9 tests)

| Test Name | What It Tests |
|-----------|---------------|
| `Verify the presence of Filters` | Tests Role filter (Provider/Resources/Facilities), verifies filtered results, clears filters |
| `Verify Search bar behaviour` | Types "Nicholas", verifies 3 specific provider rows appear |
| `Verify columns present` | Checks local practice columns (name, status, score, date), LPG columns (name, status, practice, date) |
| `Verify different Status Categories` | Checks 7 statuses: Missing info, Pending approval, Setup incomplete, Deactivated, No availability, Can't receive bookings, Can receive bookings |
| `Verify Date added column` | Checks specific date format "05/08/2024" |
| `Verify empty state on search` | Types "provider", verifies "No providers found" message |
| `Verify empty state when no providers` | Logs into empty practice, verifies "You don't have any providers yet" |
| `Verify practice control feature presence` | Verifies LPG user sees practice filter, local user doesn't |
| `Verify practice control feature modal` | Tests modal validation ("Select at least one practice"), saves selection, verifies persistence |

---

# Selenium Tests (120+ tests)

## UserManagementApiTests.cs (8 tests) - API

| Test Name | What It Tests |
|-----------|---------------|
| `GetUser_BadAuth` | Verifies find-user endpoint returns Unauthorized when no user is logged in or user lacks correct roles |
| `GetEmployee_BadAuth` | Verifies find-employee endpoint returns Unauthorized when no user is logged in or user lacks correct roles |
| `GetUser_NotFound_404` | Verifies find-user endpoint returns 404 for non-existent user email |
| `GetEmployee_NotZocdoc_BadRequest` | Verifies find-employee endpoint returns BadRequest for non-zocdoc.com email address |
| `GetEmployee_NotFound_404` | Verifies find-employee endpoint returns 404 for non-existent Zocdoc employee email |
| `GetUser_Found_200` | Verifies find-user endpoint returns 200 OK when user exists and requester has proper authorization |
| `GetEmployee_Found_200` | Verifies find-employee endpoint returns 200 OK when Zocdoc employee exists |

## PracticeUserManagementApiTests.cs (17 tests) - API

| Test Name | What It Tests |
|-----------|---------------|
| `BulkDeletePracticeUsers_ReturnsUnauthorized_ForIncompleteCsrRoles` | Verifies bulk delete endpoint returns Unauthorized for CSR users with incomplete role combinations |
| `BulkDeletePracticeUsers_ReturnsOk_ForNonExistentUser` | Verifies bulk delete endpoint returns BadRequest when attempting to delete non-existent user |
| `BulkDeletePracticeUsers_ReturnsOk_ForExistingUser` | Verifies bulk delete endpoint successfully deletes existing practice user |
| `BulkRoleChangeEndpoint_NoUser_ReturnsUnauthorized` | Verifies bulk role change endpoint returns Unauthorized when no user is logged in |
| `BulkRoleChangeEndpoint_MissingRoles_ReturnsUnauthorized` | Verifies bulk role change endpoint returns Unauthorized for CSR users missing required roles |
| `BulkRoleChangeEndpoint_GivenPracticeUser_ReturnsUnauthorized` | Verifies bulk role change endpoint returns Unauthorized for practice users (CSR-only endpoint) |
| `BulkRoleChangeEndpoint_GivenCsrUserWithRoles_ChangesRole` | Verifies bulk role change endpoint successfully changes user roles when CSR has proper permissions |
| `BulkCreatePracticeUsers_GivenCsrMissingRequiredRole_ReturnsUnauthorized` | Verifies bulk create endpoint returns Unauthorized for CSR users missing required roles |
| `BulkCreatePracticeUsers_GivenPracticeUser_ReturnsUnauthorized` | Verifies bulk create endpoint returns Unauthorized for practice users (CSR-only endpoint) |
| `BulkCreatePracticeUsers_WithEmptyRequest_ReturnsEmptyResults` | Verifies bulk create endpoint returns empty results for empty staff users array |
| `BulkCreatePracticeUsers_GivenMissingRequiredFields_ReturnsBadRequest` | Verifies bulk create endpoint validates required fields (FirstName, LastName, Type, EmailAddress, Roles) |
| `BulkCreatePracticeUsers_WithDuplicateUsername_ReturnsError` | Verifies bulk create endpoint returns error when creating user with existing email |
| `BulkCreatePracticeUsers_WithMixedResults_ReturnsBothSuccessAndFailures` | Verifies bulk create endpoint returns both successful creations and failures in single response |
| `BulkCreatePracticeUsers_GivenTooManyUsers_ReturnsBadRequest` | Verifies bulk create endpoint enforces 30 user batch limit |
| `BulkCreatePracticeUsers_GivenInvalidTypeEnum_ReturnsBadRequest` | Verifies bulk create endpoint validates staff user type enum values |
| `BulkCreatePracticeUsers_GivenPhoneNumberWhenMfaIsOnForPractice_ReturnsSuccess` | Verifies bulk create endpoint handles phone number and MFA settings correctly |

## OrganizationUserApiTests.cs (19 tests) - API

| Test Name | What It Tests |
|-----------|---------------|
| `CreateStaffUser_GivenMissingRequiredFields_ReturnsBadRequest` | Verifies create staff user validates required fields (FirstName, LastName, EmailAddress, Roles) |
| `CreateStaffUser_GivenFirstOrLastNameAreTooLong_ReturnsBadRequest` | Verifies create staff user enforces 100 character limit on names |
| `CreateStaffUser_GivenPhoneNumberTooLong_ReturnsBadRequest` | Verifies create staff user validates phone number length |
| `CreateStaffUser_GivenInvalidPhoneNumberFormat_ReturnsBadRequest` | Verifies create staff user validates phone number format |
| `CreateStaffUser_GivenInvalidEmailFormat_ReturnsBadRequest` | Verifies create staff user validates email format |
| `CreateStaffUser_GivenEmptyRolesList_ReturnsBadRequest` | Verifies create staff user requires at least one role |
| `CreateStaffUser_GivenFullAdminWithOtherRoles_ReturnsBadRequest` | Verifies FullAdmin role cannot be combined with other roles on same practice |
| `CreateStaffUser_GivenBothPracticeAndOrganizationRoles_ReturnsBadRequest` | Verifies user cannot have both practice and organization level roles |
| `CreateStaffUser_GivenMultipleOrganizations_ReturnsBadRequest` | Verifies user can only have access to single organization |
| `CreateStaffUser_GivenInconsistentRolesAcrossPractices_ReturnsBadRequest` | Verifies multi-practice users must have identical role sets across practices |
| `CreateStaffUser_GivenUnsupportedEntityType_ReturnsBadRequest` | Verifies only Organization and Practice entity types are supported |
| `CreateStaffUser_GivenPracticeRequest_GivenDuplicateUsername_ReturnsBadRequest` | Verifies duplicate email address detection for practice-level users |
| `CreateStaffUser_GivenOrgRequest_GivenDuplicateUsername_ReturnsBadRequest` | Verifies duplicate email address detection for organization-level users |

## PermissionCheckerFgaTests.cs (9 tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `PermissionCheckerFga_FullAdminPracticeStaffWithFgaAuthorization_ReturnsOk` | Verifies FGA permission check passes for FullAdmin practice staff with proper authorization |
| `PermissionCheckerFga_FullAdminPracticeStaffWithFgaAuthorization_WithMultiplePractices_ReturnsOk` | Verifies FGA permission check passes when patient has appointments at multiple practices |
| `PermissionCheckerFga_BillingPracticeStaffWithFgaAuthorization_ReturnsOk` | Verifies FGA permission check passes for Billing role practice staff |
| `PermissionCheckerFga_FullAdminPracticeStaffWithoutFgaAuthorization_IsUnauthorized` | Verifies FGA permission check fails when practice ID indicates FGA should fail |
| `PermissionCheckerFga_FullAdminPracticeStaffWithoutFgaAuthorization_WithMultiplePractices_ReturnsUnauthorized` | Verifies FGA pre-filter correctly denies unauthorized practice in multi-practice scenario |
| `PermissionCheckerFga_CsrUserWithoutPatientDataAccess_IsUnauthorized` | Verifies CSR users without patient data access role are denied |
| `PermissionCheckerFga_CsrUserWithPatientDataAccess_ReturnsOk` | Verifies CSR users with patient data access role can access patient data |
| `PermissionCheckerFga_NoUserLoggedIn_IsUnauthorized` | Verifies unauthenticated requests are denied |

## PracticeUserPermissionsMultiProviderLoginLogic.cs (1 test) - API

| Test Name | What It Tests |
|-----------|---------------|
| `PracticeStaffChurnService_UpdatePrimaryPractice_Backdoor` | Verifies multi-provider login logic correctly updates primary practice when practice churns, including JWT roles and practice mappings |

## ProviderConfigApiFgaAuthTests.cs (7 tests) - API

| Test Name | What It Tests |
|-----------|---------------|
| `ListProviders_AuthorizedUser_ReturnsOk` | Verifies list-providers endpoint returns OK for authorized logged-in professional |
| `ListProviders_NotLoggedIn_ReturnsUnauthorized` | Verifies list-providers endpoint returns Unauthorized when not logged in |
| `ListProviders_FgaFailPractice_ReturnsBasedOnFlag` | Verifies list-providers endpoint respects FGA authorization flag (Forbidden when on, OK when off) |
| `ListProviders_CsrImpersonating_ReturnsOk` | Verifies CSR users bypass FGA when impersonating provider |
| `FindDuplicates_FgaFailPractice_ReturnsBasedOnFlag` | Verifies find-duplicates endpoint respects FGA authorization flag |
| `FindDuplicates_CsrImpersonating_FgaFailPractice_ReturnsOk` | Verifies CSR users bypass FGA for find-duplicates endpoint |

## PracticeUserRolesPrivateApiTest.cs (29 tests) - API

| Test Name | What It Tests |
|-----------|---------------|
| `GetPracticeUserData_NoUser_Unauthorized` | Verifies get-practice-user-data endpoint returns Unauthorized when no user logged in |
| `GetPracticeUserData_ForbiddenRoles_Unauthorized` | Verifies get-practice-user-data endpoint denies forbidden roles (CsrLogin, CsrDeveloper, Admin) |
| `GetPracticeUserData_AllowedRoles_Success` | Verifies get-practice-user-data endpoint allows specific roles (ProviderCanLogin, CsrCanEditProvider, PracticeUserRolesRead) |
| `GetPracticeUserData_EmptyUserIds_BadRequest` | Verifies get-practice-user-data endpoint rejects empty user IDs list |
| `GetPracticeUserData_TooManyUserIds_BadRequest` | Verifies get-practice-user-data endpoint enforces 50 user ID limit |
| `GetPracticeUserData_ValidRequest_ReturnsUserData` | Verifies get-practice-user-data endpoint returns correct user data including staff permissions |
| `GetPracticeUserData_MultipleUsers_ReturnsAllAuthorizedUsers` | Verifies get-practice-user-data endpoint returns data for multiple users with correct permissions |
| `GetPracticeUserData_MultipleUsers_WithOrgPermissionsUser_HasDeleteStaffPermissionForFullAdminUser` | Verifies organization-level users have correct delete permissions for FullAdmin users |
| `GetPracticeUserData_CsrUser_ReturnsAllData` | Verifies CSR users get all user data with appropriate permissions |
| `GetPracticeUserData_UnauthorizedUser_FilteredOut` | Verifies FGA-unauthorized users are filtered from results |
| `GetPracticeUserData_NonExistentUser_FilteredOut` | Verifies non-existent user IDs are filtered from results |
| `GetPracticeUserData_DuplicateUserIds_ReturnsDistinctUsers` | Verifies duplicate user IDs return only distinct users |
| `GetPracticeUserData_PatientUser_FilteredOut` | Verifies patient users are filtered from practice user data results |
| `GetPracticeUserData_DeletedUser_FilteredOut` | Verifies deleted practice users are filtered from results |
| `GetDeletedPracticeUserData_NoUser_Unauthorized` | Verifies get-staff-name-for-deleted-users endpoint returns Unauthorized when no user logged in |
| `GetDeletedPracticeUserData_ForbiddenRoles_Unauthorized` | Verifies get-deleted-user-data endpoint denies forbidden roles |
| `GetDeletedPracticeUserData_PracticeUser_Unauthorized` | Verifies practice users cannot access deleted user data endpoint |
| `GetDeletedPracticeUserData_EmptyUserIds_BadRequest` | Verifies get-deleted-user-data endpoint rejects empty user IDs |
| `GetDeletedPracticeUserData_TooManyUserIds_BadRequest` | Verifies get-deleted-user-data endpoint enforces 50 user ID limit |
| `GetDeletedPracticeUserData_MultipleUsers_ReturnsAllAuthorizedUsers` | Verifies get-deleted-user-data endpoint returns data for multiple deleted users |
| `GetDeletedPracticeUserData_UnauthorizedUser_FilteredOut` | Verifies non-deleted and unauthorized users are filtered from deleted user data |
| `GetDeletedPracticeUserData_DuplicateUserIds_ReturnsDistinctUsers` | Verifies duplicate user IDs return distinct results for deleted users |
| `ValidatePracticeMappings_NoUser_Unauthorized` | Verifies validate-practice-mappings endpoint returns Unauthorized when no user logged in |
| `ValidatePracticeMappings_ForbiddenRoles_Unauthorized` | Verifies validate-practice-mappings denies forbidden roles |
| `ValidatePracticeMappings_AllowedCsrRoles_Validated` | Verifies allowed roles can validate practice mappings |
| `ValidatePracticeMappings_PracticeUserForAnotherPractice_Forbidden` | Verifies practice users cannot validate mappings for other practices |
| `ValidatePracticeMappings_ForDeletedUser_Fails` | Verifies validate-practice-mappings handles deleted users based on flag |
| `ValidatePracticeMappings_PracticeUserForSamePractice_Validated` | Verifies practice users can validate mappings for their own practice |

## ProviderDashboardRbacControllerHttpTests.cs (31+ tests) - Integration

| Test Name | What It Tests |
|-----------|---------------|
| `CallEndpoints_GivenUserRole_ReturnsForbiddenIfRoleNotAllowed` | Data-driven test verifying RBAC enforcement across 14 dashboard endpoints for all practice staff role types |
| `GetAppointmentReportData_FutureApptCheck_InvalidDate_Throws` | Verifies appointment report rejects invalid future appointment check date |
| `GetAppointmentReportData_Success` | Verifies appointment report page data endpoint returns OK |
| `GetAppointmentReportCsv_Success` | Verifies appointment report CSV export endpoint returns OK |
| `GetAppointmentReportCsvStream_Success` | Verifies appointment report CSV stream endpoint returns OK |
| `GetAppointmentReportDataV2_Success` | Verifies multi-practice appointment report V2 endpoint returns OK |
| `GetAppointmentReportDataV2_FutureApptCheck_InvalidDate_Throws` | Verifies V2 appointment report rejects invalid future date |
| `GetAppointmentReportCsvV2_Success` | Verifies V2 CSV export with optional provider and location IDs |
| `GetAppointmentsV2_Success` | Verifies V2 appointments endpoint returns OK |
| `GetAppointmentsV2_MultipleProviders_Success` | Verifies V2 appointments works with multiple providers |
| `MultiPracticeAppointmentReport_FgaAuthorization_Success` | Verifies FGA authorization passes for authorized practices |
| `MultiPracticeAppointmentReport_FgaAuthorization_Unauthorized` | Verifies FGA authorization fails when unauthorized practice included |
| `GetPerformanceData_Success` | Verifies performance page data endpoint returns OK |
| `PutDispute_ExistingPatient_Success` | Verifies dispute endpoint accepts ExistingPatient dispute reason |
| `PutDispute_ExistingPatient_WithAdditionalDetails_Success` | Verifies dispute endpoint accepts additional details for ExistingPatient |
| `PutDispute_NoShow_WithAdditionalDetails_Success` | Verifies dispute endpoint accepts NoShow reason with details |
| `PutDispute_PatientCancellation_WithAdditionalDetails_Success` | Verifies dispute endpoint accepts PatientCancellation with cancellation reason |
| `GetPatientLoyaltyAwardsForPractice_ReturnsForbidden_TryingToAccessAnotherPractice` | Verifies awards endpoint denies access to other practices |
| `GetPatientLoyaltyAwardsForPractice_ReturnsUnauthorized_WhenNotLoggedIn` | Verifies awards endpoint returns Unauthorized when not logged in |
| `GetPatientLoyaltyAwardsForPractice_GivenCsrUser_ShouldAllow` | Verifies CSR users can access awards when impersonating provider |
| `UpdateSpendLock_GivenPracticeIdDoesNotMatch_ReturnsBadRequest` | Verifies spend lock update validates practice ID matches logged-in user |
| `UpdateSpendLock_GivenDoNotHaveCorrectRole_ReturnsUnauthorized` | Verifies spend lock update requires proper CSR roles |
| `UpdateSpendLock_GivenNotCurrentlyFeePerBooking_ReturnsForbidden` | Verifies spend lock is only available for fee-per-booking practices |
| `UpdateSpendLock` | Verifies spend lock update returns NoContent on success |
| `UpdateSpendLock_FgaIsOn_CsrUser` | Verifies FGA enforcement for CSR users on spend lock update |
| `UpdateSpendLock_FgaIsOn_PracticeUser` | Verifies FGA enforcement for practice users on spend lock update |
| `DeleteSpendLock_GivenPracticeIdDoesNotMatch_ReturnsBadRequest` | Verifies spend lock delete validates practice ID |
| `DeleteSpendLock_GivenDoNotHaveCorrectRole_ReturnsUnauthorized` | Verifies spend lock delete requires proper roles |
| `DeleteSpendLock` | Verifies spend lock delete returns NoContent on success |
| `UpdateBudget_GivenPracticeIdDoesNotMatch_ReturnsBadRequest` | Verifies budget update validates practice ID |
| `UpdateBudget_ReturnsNoContent` | Verifies budget update returns NoContent on success |

---

---

*Generated: 2026-04-09*
*Total tests catalogued: ~1,560*
