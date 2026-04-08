# Complete Test Inventory - All Pterodactyl Repositories

## Table of Contents

1. [practice-user-permissions](#practice-user-permissions)
2. [practice-authorization-proxy](#practice-authorization-proxy)
3. [provider-grouping](#provider-grouping)
4. [provider-join-service](#provider-join-service)

---

# practice-user-permissions

## Unit Tests

### Services/UserRolesServiceTests.cs (17 tests)

| Test Name | What It Tests |
|-----------|---------------|
| SetUserRolesGivenUserVersion_ValidInput_Success | Setting user roles with valid version succeeds |
| SetUserRolesGivenUserVersion_VersionMismatch_Throws | Version mismatch throws optimistic locking exception |
| GetUserRoles_ExistingUser_ReturnsRoles | Retrieving roles for existing user |
| GetUserRoles_NonExistentUser_ReturnsEmpty | Retrieving roles for non-existent user returns empty |
| GetUserVersion_ExistingUser_ReturnsVersion | Getting user version for existing user |
| GetUserVersion_NonExistentUser_ReturnsNull | Getting version for non-existent user |
| QueryUserRolesByEntity_Practice_ReturnsMatchingUsers | Querying users by practice entity |
| QueryUserRolesByEntity_Organization_ReturnsMatchingUsers | Querying users by organization entity |
| QueryUserRolesByEntity_WithFilters_AppliesFilters | Query with role filters applied |
| *Additional parameterized tests for filtering logic* | Various filtering scenarios |

### Services/UserServiceTests.cs (18 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GetUserPractices_ExistingUser_ReturnsPractices | Getting practices for a user |
| GetUserPractices_UserWithMultiplePractices_ReturnsAll | User with multiple practice memberships |
| GetUserPractices_UserWithOrganization_IncludesOrgPractices | Organization membership includes child practices |
| GetUserPractices_NonExistentUser_ReturnsEmpty | Non-existent user returns empty list |
| GetOverlappingUsers_PracticeA_PracticeB_ReturnsCommon | Finding users common to two practices |
| GetOverlappingUsers_NoOverlap_ReturnsEmpty | No common users between practices |
| *Additional tests for edge cases* | Various user lookup scenarios |

### Services/Auth0UserServiceTests.cs (3 tests)

| Test Name | What It Tests |
|-----------|---------------|
| ShouldSkipAuth0Users_SamlpPrefix_ReturnsTrue | Users with samlp| prefix should be skipped |
| ShouldSkipAuth0Users_NoPrefix_ReturnsFalse | Regular users should not be skipped |
| ShouldSkipAuth0Users_OtherPrefix_ReturnsFalse | Other prefixes don't trigger skip |

### Services/FgaModelServiceTests.cs (1 test)

| Test Name | What It Tests |
|-----------|---------------|
| GetLatestModelId_ReturnsCurrentModel | Retrieving the latest FGA model ID |

### Services/UserInvitationServiceTests.cs (9 tests)

| Test Name | What It Tests |
|-----------|---------------|
| CreateInvitation_ValidData_CreatesInvitation | Creating a new user invitation |
| CreateInvitation_DuplicateEmail_Throws | Duplicate invitation for same email |
| GetInvitation_ExistingId_ReturnsInvitation | Retrieving invitation by ID |
| GetInvitation_NonExistentId_ReturnsNull | Non-existent invitation returns null |
| GetInvitation_ExpiredInvitation_ReturnsExpired | Expired invitations are marked |
| InvalidateInvitation_ExistingId_Invalidates | Marking invitation as invalid |
| InvalidateInvitation_AlreadyInvalid_NoOp | Invalidating already invalid invitation |
| FilterInvitations_ByPractice_ReturnsMatching | Filtering invitations by practice |
| FilterInvitations_ByStatus_ReturnsMatching | Filtering invitations by status |

### Services/UserRolesHierarchyServiceTests.cs (10 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GetUserRolesFromEntityHierarchy_Practice_ReturnsDirectRoles | Getting roles from direct practice membership |
| GetUserRolesFromEntityHierarchy_Organization_ReturnsInheritedRoles | Getting inherited roles from organization |
| GetUserRolesFromEntityHierarchy_NestedOrg_TraversesHierarchy | Multi-level organization hierarchy traversal |
| BreakUserRolesFromOrganizationToPractices_SinglePractice_Creates | Breaking org roles to single practice |
| BreakUserRolesFromOrganizationToPractices_MultiplePractices_CreatesAll | Breaking org roles to multiple practices |
| BreakUserRolesFromOrganizationToPractices_EmptyPractices_NoOp | No practices to break roles to |
| *Additional hierarchy traversal tests* | Various hierarchy scenarios |

### Services/UserRolesServicePaginationTests.cs (9 tests)

| Test Name | What It Tests |
|-----------|---------------|
| QueryUserRolesByEntityPaginated_FirstPage_ReturnsWithToken | Paginated query returns continuation token |
| QueryUserRolesByEntityPaginated_LastPage_NoToken | Last page has no continuation token |
| QueryUserRolesByEntityPaginated_EmptyResult_ReturnsEmpty | Empty result set handling |
| V2UserFiltering_ExcludesV2Users_WhenFlagDisabled | V2 user filtering when flag is off |
| V2UserFiltering_IncludesV2Users_WhenFlagEnabled | V2 user filtering when flag is on |
| BatchGetUserVersions_MultipleUsers_ReturnsAll | Batch getting user versions |
| BatchGetUserVersions_SomeNotFound_ReturnsPartial | Partial results when some users not found |
| *Additional pagination tests* | Various pagination scenarios |

### Services/ScopedOrganizationMemberServiceTests.cs (8 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GetScopedOrgMembership_Existing_ReturnsMembership | Getting existing scoped org membership |
| GetScopedOrgMembership_NonExistent_ReturnsNull | Non-existent membership returns null |
| SetScopedOrgMembership_New_Creates | Creating new scoped org membership |
| SetScopedOrgMembership_Existing_Updates | Updating existing membership |
| SetScopedOrgMembership_VersionMismatch_Throws | Optimistic locking on update |
| DeleteScopedOrgMembership_Existing_Deletes | Deleting existing membership |
| DeleteScopedOrgMembership_NonExistent_NoOp | Deleting non-existent membership |
| DeleteScopedOrgMembership_VersionMismatch_Throws | Optimistic locking on delete |

### Services/DlqRedriveServiceTests.cs (7 tests)

| Test Name | What It Tests |
|-----------|---------------|
| StartRedriveAsync_ValidQueue_StartsRedrive | Starting DLQ redrive successfully |
| StartRedriveAsync_InvalidQueue_Throws | Invalid queue name throws exception |
| StartRedriveAsync_AlreadyInProgress_Throws | Redrive already in progress |
| StartRedriveAsync_EmptyDlq_ReturnsZero | Empty DLQ returns zero messages |
| ConfigurationValidation_MissingQueueUrl_Throws | Missing queue URL configuration |
| ConfigurationValidation_InvalidArn_Throws | Invalid ARN format |
| *Error handling tests* | Various error scenarios |

### Services/TupleAuditServiceTests.cs (61 tests)

| Test Name | What It Tests |
|-----------|---------------|
| AuditTuples_NewTuples_RecordsAll | Recording new FGA tuples |
| AuditTuples_RemovedTuples_RecordsRemoval | Recording tuple removals |
| AuditTuples_ModifiedTuples_RecordsBoth | Recording tuple modifications |
| CompareTuples_Identical_NoChanges | Identical tuple sets have no changes |
| CompareTuples_Added_DetectsAdditions | Detecting added tuples |
| CompareTuples_Removed_DetectsRemovals | Detecting removed tuples |
| *58 additional parameterized tests for tuple auditing scenarios* | Various FGA tuple audit scenarios |

### Services/OrganizationMembersServiceTests.cs (27 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GetOrgMembers_ExistingOrg_ReturnsMembers | Getting members of organization |
| GetOrgMembers_NonExistentOrg_ReturnsEmpty | Non-existent org returns empty |
| AddOrgMember_NewMember_Adds | Adding new organization member |
| AddOrgMember_ExistingMember_NoOp | Adding existing member is no-op |
| RemoveOrgMember_ExistingMember_Removes | Removing organization member |
| RemoveOrgMember_NonExistentMember_NoOp | Removing non-existent member is no-op |
| GetOrgMembersByHierarchy_TraversesUp | Getting members traversing up hierarchy |
| GetOrgMembersByHierarchy_TraversesDown | Getting members traversing down hierarchy |
| *19 additional organization membership tests* | Various org membership scenarios |

### Services/UserEditAuthorizationServiceTests.cs (7 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GetUserIdsAuthorizedForEditRoles_AdminUser_ReturnsAll | Admin can edit all users |
| GetUserIdsAuthorizedForEditRoles_RegularUser_ReturnsFiltered | Regular user sees filtered list |
| GetUserIdsAuthorizedForEditRoles_NoPermission_ReturnsEmpty | No permission returns empty |
| AuthorizeEditRoles_SameUser_Allowed | User can edit own roles |
| AuthorizeEditRoles_HigherPrivilege_Allowed | Higher privilege can edit lower |
| AuthorizeEditRoles_LowerPrivilege_Denied | Lower privilege cannot edit higher |
| AuthorizeEditRoles_DifferentOrg_Denied | Cross-org edit denied |

### Services/UserRoleChangeNotificationServiceTests.cs (4 tests)

| Test Name | What It Tests |
|-----------|---------------|
| QueueNotification_ValidChange_Queues | Queueing role change notification |
| QueueNotification_BatchChanges_QueuesBatch | Batching multiple notifications |
| ProcessNotifications_SingleMessage_Processes | Processing single notification |
| ProcessNotifications_BatchMessages_ProcessesAll | Processing batch of notifications |

### Services/PracticeChurnCalculatorTests.cs (11 tests)

| Test Name | What It Tests |
|-----------|---------------|
| ArePracticesChurned_ActiveProviders_NotChurned | Practices with active providers not churned |
| ArePracticesChurned_NoProviders_Churned | Practices without providers are churned |
| ArePracticesChurned_InactiveProviders_Churned | Practices with only inactive providers |
| ArePracticesChurned_MixedProviders_NotChurned | Mix of active/inactive not churned |
| *7 additional churn calculation tests* | Various churn scenarios |

### Services/UltimateParentOrganizationServiceTests.cs (16 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GetUltimateParent_RootOrg_ReturnsSelf | Root org is its own ultimate parent |
| GetUltimateParent_ChildOrg_ReturnsRoot | Child org returns root as ultimate parent |
| GetUltimateParent_DeeplyNested_TraversesAll | Deeply nested org traverses to root |
| ValidateUltimateParent_Valid_NoThrow | Valid ultimate parent validation |
| ValidateUltimateParent_Invalid_Throws | Invalid ultimate parent throws |
| *11 additional ultimate parent tests* | Various hierarchy scenarios |

### Services/NonceIdServiceTests.cs (4 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GenerateNonceId_ReturnsUniqueId | Generating unique nonce ID |
| GenerateNonceId_MultipleCalls_AllUnique | Multiple calls return unique IDs |
| ValidateNonceId_Valid_ReturnsTrue | Validating valid nonce ID |
| ValidateNonceId_Invalid_ReturnsFalse | Validating invalid nonce ID |

### Services/InternalMigrationServiceTests.cs (8 tests)

| Test Name | What It Tests |
|-----------|---------------|
| MigrateUser_ExistingUser_Migrates | Migrating existing user data |
| MigrateUser_NonExistentUser_NoOp | Non-existent user migration is no-op |
| MigratePractice_ExistingPractice_Migrates | Migrating practice data |
| MigratePractice_NonExistentPractice_NoOp | Non-existent practice migration is no-op |
| *4 additional migration tests* | Various migration scenarios |

### Clients/FgaRelationConverterTests.cs (59 tests)

| Test Name | What It Tests |
|-----------|---------------|
| ConvertRelation_PracticeAdmin_ReturnsCorrectTuple | Converting practice admin relation |
| ConvertRelation_PracticeUser_ReturnsCorrectTuple | Converting practice user relation |
| ConvertRelation_OrgAdmin_ReturnsCorrectTuple | Converting organization admin relation |
| ConvertRelation_OrgUser_ReturnsCorrectTuple | Converting organization user relation |
| *55 additional relation conversion tests for all role types* | All FGA relation type conversions |

### Clients/MessagingServiceClientTests.cs (7 tests)

| Test Name | What It Tests |
|-----------|---------------|
| SendMessage_ValidMessage_Sends | Sending valid message |
| SendMessage_InvalidRecipient_Throws | Invalid recipient throws exception |
| SendMessage_ServiceUnavailable_Retries | Retry on service unavailable |
| *4 additional messaging client tests* | Various messaging scenarios |

### Clients/PracticeUserRolesApiCallerTests.cs (11 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GetUserRoles_ValidRequest_ReturnsRoles | Getting user roles via API |
| GetUserRoles_NotFound_ReturnsNull | Not found returns null |
| SetUserRoles_ValidRequest_Sets | Setting user roles via API |
| SetUserRoles_Conflict_Throws | Conflict on concurrent update |
| *7 additional API caller tests* | Various API call scenarios |

### Clients/ProviderGroupingClientTests.cs (1 test)

| Test Name | What It Tests |
|-----------|---------------|
| GetOrganization_ValidId_ReturnsOrg | Getting organization from POGS |

### Helpers/FgaTupleParsingHelperTests.cs (17 tests)

| Test Name | What It Tests |
|-----------|---------------|
| ParseTuple_ValidPracticeTuple_ParsesCorrectly | Parsing valid practice tuple |
| ParseTuple_ValidOrgTuple_ParsesCorrectly | Parsing valid organization tuple |
| ParseTuple_InvalidFormat_Throws | Invalid tuple format throws |
| ParseTuple_MissingRelation_Throws | Missing relation in tuple |
| *13 additional tuple parsing tests* | Various parsing scenarios |

---

## Lambda Unit Tests

### FgaUpdates/FgaTupleCreatorTests.cs (11 tests)

| Test Name | What It Tests |
|-----------|---------------|
| CreateTuple_PracticeRole_CreatesCorrectTuple | Creating practice role tuple |
| CreateTuple_OrgRole_CreatesCorrectTuple | Creating organization role tuple |
| CreateTuple_WithCondition_IncludesCondition | Tuple with FGA condition |
| *8 additional tuple creation tests* | Various tuple creation scenarios |

### FgaUpdates/FgaUpdateServiceTests.cs (8 tests)

| Test Name | What It Tests |
|-----------|---------------|
| ProcessUpdate_AddTuple_CallsFgaWrite | Processing add tuple update |
| ProcessUpdate_RemoveTuple_CallsFgaDelete | Processing remove tuple update |
| ProcessUpdate_BatchUpdates_ProcessesAll | Batch update processing |
| ProcessUpdate_FgaError_Throws | FGA error handling |
| *4 additional update service tests* | Various update scenarios |

### FgaUpdates/FgaUpdatesGeneratorTests.cs (4 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GenerateUpdates_RoleAdded_GeneratesWrite | Generating write for added role |
| GenerateUpdates_RoleRemoved_GeneratesDelete | Generating delete for removed role |
| GenerateUpdates_RoleModified_GeneratesBoth | Generating both for modified role |
| GenerateUpdates_NoChanges_GeneratesEmpty | No changes generates empty |

### AuditLogging/AuditLogGeneratorTests.cs (7 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GenerateLog_RoleChange_IncludesAllFields | Role change audit log generation |
| GenerateLog_UserCreation_IncludesUserInfo | User creation audit log |
| GenerateLog_UserDeletion_IncludesReason | User deletion audit log |
| *4 additional audit log tests* | Various audit scenarios |

### AuditLogging/AuditLoggingServiceTests.cs (6 tests)

| Test Name | What It Tests |
|-----------|---------------|
| LogAuditEvent_ValidEvent_Logs | Logging valid audit event |
| LogAuditEvent_BatchEvents_LogsAll | Logging batch of events |
| LogAuditEvent_ServiceError_Retries | Retry on service error |
| *3 additional logging service tests* | Various logging scenarios |

### OrganizationMembershipUpdates/*.cs (~50 tests)

| Test Category | What It Tests |
|---------------|---------------|
| MemberAdded | Processing organization member added events |
| MemberRemoved | Processing organization member removed events |
| HierarchyChanged | Processing hierarchy change events |
| BatchUpdates | Processing batch membership updates |

### OrganizationHierarchyRoleFixes/*.cs (~54 tests)

| Test Category | What It Tests |
|---------------|---------------|
| RoleInheritance | Role inheritance when hierarchy changes |
| RoleBreaking | Breaking inherited roles to explicit |
| RoleMerging | Merging roles when orgs merge |
| RoleCleanup | Cleaning up orphaned roles |

### SqsEventParserTests.cs (8 tests)

| Test Name | What It Tests |
|-----------|---------------|
| Parse_ValidEvent_ReturnsEvent | Parsing valid SQS event |
| Parse_MalformedJson_Throws | Malformed JSON handling |
| Parse_MissingFields_Throws | Missing required fields |
| *5 additional parser tests* | Various parsing scenarios |

### SqsEventClassifierTests.cs (6 tests)

| Test Name | What It Tests |
|-----------|---------------|
| Classify_UserRoleChange_ReturnsUserRole | Classifying user role change events |
| Classify_OrgMemberChange_ReturnsOrgMember | Classifying org membership events |
| Classify_UnknownType_ReturnsUnknown | Unknown event type handling |
| *3 additional classifier tests* | Various classification scenarios |

---

## Integration Tests

### Persistence/UserRolesPersistenceTests.cs (38 tests)

| Test Name | What It Tests |
|-----------|---------------|
| CreateUserRoles_NewUser_Persists | Creating user roles in DynamoDB |
| CreateUserRoles_ExistingUser_Updates | Updating existing user roles |
| GetUserRoles_ExistingUser_Returns | Getting user roles from DynamoDB |
| GetUserRoles_NonExistent_ReturnsNull | Non-existent user returns null |
| QueryByPractice_ReturnsMatching | Querying users by practice |
| QueryByOrganization_ReturnsMatching | Querying users by organization |
| DeleteUserRoles_Existing_Deletes | Deleting user roles |
| *31 additional persistence tests* | Various DynamoDB operations |

### Persistence/OrganizationMembersPersistenceTests.cs (22 tests)

| Test Name | What It Tests |
|-----------|---------------|
| CreateOrgMember_NewMember_Persists | Creating org member in DynamoDB |
| GetOrgMembers_ExistingOrg_Returns | Getting org members |
| DeleteOrgMember_Existing_Deletes | Deleting org member |
| BatchGetOrgMembers_ReturnsAll | Batch getting org members |
| *18 additional persistence tests* | Various DynamoDB operations |

### Persistence/ScopedOrganizationMemberPersistenceTests.cs (15 tests)

| Test Name | What It Tests |
|-----------|---------------|
| Create_NewMember_Persists | Creating scoped org member |
| Get_ExistingMember_Returns | Getting scoped org member |
| Update_ExistingMember_Updates | Updating scoped org member |
| Delete_ExistingMember_Deletes | Deleting scoped org member |
| *11 additional persistence tests* | Various scoped org operations |

### Persistence/UserInvitationPersistenceTests.cs (12 tests)

| Test Name | What It Tests |
|-----------|---------------|
| Create_NewInvitation_Persists | Creating user invitation |
| Get_ExistingInvitation_Returns | Getting user invitation |
| Invalidate_ExistingInvitation_Updates | Invalidating invitation |
| Query_ByPractice_ReturnsMatching | Querying invitations by practice |
| *8 additional persistence tests* | Various invitation operations |

### Persistence/PracticeBlockedPersistenceTests.cs (10 tests)

| Test Name | What It Tests |
|-----------|---------------|
| MarkBlocked_NewPractice_Persists | Marking practice as blocked |
| IsBlocked_BlockedPractice_ReturnsTrue | Checking blocked practice |
| IsBlocked_UnblockedPractice_ReturnsFalse | Checking unblocked practice |
| BatchCheck_MultiPractices_ReturnsStatuses | Batch checking blocked status |
| *6 additional persistence tests* | Various blocked practice operations |

---

## API Tests

### UserRolesApiTests.cs (123 tests)

| Test Category | Count | What It Tests |
|---------------|-------|---------------|
| SetUserRoles | 25 | Setting user roles via API |
| GetEntityUsersRoles | 20 | Getting entity users via API |
| GetUserRoles | 15 | Getting specific user roles |
| QueryUserRoles | 18 | Querying user roles with filters |
| Authorization | 20 | Authorization requirements for each endpoint |
| Validation | 15 | Request validation |
| ErrorHandling | 10 | Error response handling |

### UserApiTests.cs (19 tests)

| Test Name | What It Tests |
|-----------|---------------|
| AuthorizeEditUserData_AdminUser_Returns200 | Admin can edit user data |
| AuthorizeEditUserData_RegularUser_Returns403 | Regular user cannot edit |
| AuthorizeViewUserData_SameUser_Returns200 | User can view own data |
| AuthorizeViewUserData_OtherUser_Returns403 | Cannot view other user data |
| *15 additional user API tests* | Various user API scenarios |

### InternalApiTests.cs (33 tests)

| Test Name | What It Tests |
|-----------|---------------|
| InternalMigration_ValidRequest_Returns200 | Internal migration endpoint |
| InternalMigration_Unauthorized_Returns401 | Unauthorized access |
| InternalBackfill_ValidRequest_Returns200 | Internal backfill endpoint |
| *30 additional internal API tests* | Various internal endpoints |

---

# practice-authorization-proxy

## Unit Tests

### Service/AuthorizationServiceTests.cs (12 tests)

| Test Name | What It Tests |
|-----------|---------------|
| Verify_IsPracticeAuthorized_ReturnsExpectedResult_SendsMetricsCorrectly | Practice authorization returns correct bool based on FGA result |
| Verify_IsPracticeAuthorized_FgaAuthzServiceThrows_ReturnsExpectedResult_SendsMetricsCorrectly | Practice authorization returns false when FGA throws |
| Verify_IsOrganizationAuthorized_ReturnsExpectedResult_SendsMetricsCorrectly | Organization authorization returns correct bool |
| Verify_IsOrganizationAuthorized_FgaAuthzServiceThrows_ReturnsExpectedResult_SendsMetricsCorrectly | Organization auth returns false when FGA throws |
| Verify_BatchIsPracticeAuthorized_ReturnsSuccess | Batch practice authorization success |
| Verify_BatchIsPracticeAuthorized_FgaAuthzServiceThrows_ThrowsGenericException | Batch practice auth propagates exceptions |
| Verify_BatchIsPracticeAuthorized_FgaReturnsError_ThrowsCustomExceptionWithMessage | Batch throws BatchPracticeAuthorizationException |
| Verify_BatchIsPracticeAuthorized_FgaReturnsError_ThrowsCustomExceptionWithCorrectProperties | Exception has correct properties |
| Verify_BatchIsOrganizationAuthorized_ReturnsSuccess | Batch organization auth success |
| Verify_BatchIsOrganizationAuthorized_FgaAuthzServiceThrows_ThrowsException | Batch org auth propagates exceptions |
| Verify_BatchIsOrganizationAuthorized_FgaReturnsError_ThrowsCustomExceptionWithMessage | Batch throws BatchOrganizationAuthorizationException |
| Verify_BatchIsOrganizationAuthorized_FgaReturnsError_ThrowsCustomExceptionWithCorrectProperties | Exception has correct properties |

### ConversionExtensionsTests.cs (5 tests)

| Test Name | What It Tests |
|-----------|---------------|
| VerifyAllPermissionsFiltersRepresentedInPracticeAuthorizationProxy | All PermissionFilter enum values can be converted |
| Verify_ToBatchPracticeResult_ConvertsSuccessfully | Converts to BatchPracticeAuthorizationResult |
| Verify_ToBatchOrganizationResult_ConvertsSuccessfully | Converts to BatchOrganizationAuthorizationResult |
| Verify_ToBatchPracticeResult_WithEmptyResults_ConvertsSuccessfully | Empty list conversion |
| Verify_ToBatchOrganizationResult_WithEmptyResults_ConvertsSuccessfully | Empty list conversion |

## API Tests

### PracticeAuthorizationTests.cs (5 tests)

| Test Name | What It Tests |
|-----------|---------------|
| IsPracticeAuthorized_GivenNotLoggedIn_ReturnsUnauthorized | Returns 401 when no authentication |
| IsPracticeAuthorized_GivenNonPracticeUser_ReturnsForbidden | Returns 403 for patient/CSR users |
| IsPracticeAuthorized_GivenPracticeUser_ReturnsResponse | Returns 200 with correct is_authorized |
| BatchIsPracticeAuthorized_GivenMoreThan50Practices_ReturnsBadRequest | Returns 400 when >50 practice IDs |
| BatchIsPracticeAuthorized_GivenExactly50Practices_ReturnsOK | Returns 200 when exactly 50 practice IDs |

### OrganizationAuthorizationTests.cs (5 tests)

| Test Name | What It Tests |
|-----------|---------------|
| IsOrganizationAuthorized_GivenNotLoggedIn_ReturnsUnauthorized | Returns 401 when no authentication |
| IsOrganizationAuthorized_GivenNonPracticeUser_ReturnsForbidden | Returns 403 for patient/CSR users |
| IsOrganizationAuthorized_GivenPracticeUser_ReturnsResponse | Returns 200 with correct is_authorized |
| BatchIsOrganizationAuthorized_GivenMoreThan50Organizations_ReturnsBadRequest | Returns 400 when >50 org IDs |
| BatchIsOrganizationAuthorized_GivenExactly50Organizations_ReturnsOK | Returns 200 when exactly 50 org IDs |

## Placeholder Tests (TO BE REMOVED)

| Test File | Test Name | What It Tests |
|-----------|-----------|---------------|
| UnitTests/ExampleTests.cs | TokenEmptyTest | `(1 + 1).Should().Be(2)` - PLACEHOLDER |
| IntegrationTests/ExampleTests.cs | TokenEmptyTest | `(1 + 1).Should().Be(2)` - PLACEHOLDER |
| Web.IntegrationTests/ExampleTests.cs | TokenEmptyTest | `(1 + 1).Should().Be(2)` - PLACEHOLDER |

---

# provider-grouping

## API Tests

### GroupControllerTests.cs (26 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GetGroupByGroupId_InvalidGroupId_BadRequest | Validates bad request for invalid group ID |
| GetGroupByGroupId_GivenGroupDoesNotExist_ShouldReturnNull | Null response for missing group |
| GetGroupByGroupId_GivenGroupExists_ShouldReturnGroup | Successful group retrieval |
| GetGroupsByOrganizationId_InvalidOrgId_BadRequest | Invalid org ID validation |
| GetGroupsByOrganizationId_OrgNotFound_ReturnsEmpty | Non-existent org returns empty |
| GetGroupsByOrganizationId_OrgExists_ReturnsGroups | Successful groups retrieval |
| GetGroupsByOrganizationId_IncludeHierarchy_ReturnsAll | Include child org groups |
| GetGroupsByTypeAndOrganizationId_ValidRequest_Returns | Filtered by type retrieval |
| GetGroupsByTypeAndOrganizationId_InvalidType_BadRequest | Invalid group type validation |
| GetGroupsByTypeAndOrganizationId_OrgNotFound_ReturnsEmpty | Non-existent org returns empty |
| GetGroupsByTypeAndMemberId_ValidRequest_Returns | Member-based lookup |
| GetGroupsByTypeAndMemberId_MemberNotFound_ReturnsEmpty | Non-existent member returns empty |
| GetGroupsByTypeAndMemberId_InvalidType_BadRequest | Invalid type validation |
| GetGroupMembersByGroupId_ValidRequest_Returns | Member retrieval success |
| GetGroupMembersByGroupId_GroupNotFound_ReturnsEmpty | Non-existent group returns empty |
| GetGroupMembersByGroupId_InvalidGroupId_BadRequest | Invalid group ID validation |
| GetGroupMembersByGroupId_Pagination_ReturnsPage | Paginated member retrieval |
| CreateGroup_ValidRequest_CreatesGroup | Group creation success |
| CreateGroup_DuplicateName_Conflict | Duplicate group name conflict |
| CreateGroup_InvalidOrgId_BadRequest | Invalid org ID validation |
| EditGroupMetadata_ValidRequest_Updates | Metadata update success |
| EditGroupMetadata_GroupNotFound_NotFound | Group not found error |
| DeleteGroup_ValidRequest_Deletes | Group deletion success |
| DeleteGroup_GroupNotEmpty_Conflict | Non-empty group conflict |
| EditGroupMembersForGroupId_AddMembers_Adds | Adding group members |
| EditGroupMembersForGroupId_RemoveMembers_Removes | Removing group members |

### GroupRuleControllerTests.cs (18 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GetAttributes_ExpectedResponse | Attributes endpoint success |
| PreviewUpdateGroupRules_ValidRules_ReturnsPreview | Rule preview success |
| PreviewUpdateGroupRules_InvalidRules_BadRequest | Invalid rules validation |
| PreviewUpdateGroupRules_GroupNotFound_NotFound | Group not found error |
| PreviewUpdateGroupRules_NoChanges_ReturnsEmpty | No changes preview |
| PreviewUpdateGroupRules_AddMembers_ShowsAdditions | Preview shows additions |
| PreviewUpdateGroupRules_RemoveMembers_ShowsRemovals | Preview shows removals |
| UpdateGroupRules_ValidRules_Updates | Rule update success |
| UpdateGroupRules_InvalidRules_BadRequest | Invalid rules validation |
| UpdateGroupRules_GroupNotFound_NotFound | Group not found error |
| UpdateGroupRules_ConcurrentUpdate_Conflict | Concurrent update conflict |
| RefreshAllDynamicGroups_ExpectedResponse | Refresh all success |
| RefreshGroupsByOrganizationIds_ValidRequest_Refreshes | Org-specific refresh |
| RefreshGroupsByOrganizationIds_InvalidOrgIds_BadRequest | Invalid org IDs validation |
| RefreshGroupsByOrganizationIds_SomeNotFound_PartialSuccess | Partial refresh success |
| RefreshGroupsByOrganizationIds_AllNotFound_NotFound | All orgs not found |
| RefreshGroupsByOrganizationIds_EmptyList_BadRequest | Empty list validation |

### OrganizationControllerTests.cs (60+ tests)

| Test Category | Count | What It Tests |
|---------------|-------|---------------|
| GetOrganizationMembershipByPracticeId | 6 | Practice membership lookup |
| BatchGetOrganizationMembershipByPracticeIds | 4 | Batch practice lookup |
| GetOrganizationByOrganizationId | 8 | Organization retrieval |
| GetPracticesByOrganizationId | 4 | Practice retrieval by org |
| GetLineageForOrganization | 4 | Hierarchy lineage |
| GetFullHierarchyForOrganization | 3 | Full hierarchy retrieval |
| CreateOrganization | 8 | Organization creation with auth |
| UpdateOrganization | 8 | Organization updates with auth |
| UpdateOrganizationParent | 10 | Parent relationship changes |
| UpdateOrganizationMembershipForPractice | 10 | Practice membership updates |
| BatchUpdateOrganizationMembershipForPractice | 6 | Batch membership updates |

## Integration Tests

### GroupPersistenceTests.cs (10 tests)

| Test Name | What It Tests |
|-----------|---------------|
| Test_CreateGroup_MultiLevelOrganization | Multi-level org group creation |
| Test_CreateUpdateAndDeleteGroup | Full CRUD + history |
| GetGroupsByOrganizationId_DirectOnly | Direct org groups only |
| GetGroupsByOrganizationId_IncludeHierarchy | Include hierarchy groups |
| Test_GetAllDynamicGroups | Dynamic group retrieval |
| Test_BatchGetGroupsByGroupId | Batch group retrieval |
| Test_CreateAndDeleteGroupMember | Member CRUD |
| Test_BatchCreateAndDeleteGroupMembers | Batch member CRUD |
| GetGroupMembersByMemberEntity_Practice | Member entity practice query |
| GetGroupMembersByMemberEntity_Provider | Member entity provider query |

### OrganizationPersistenceTests.cs (16 tests)

| Test Name | What It Tests |
|-----------|---------------|
| Test_CreateAndGetOrganization | Basic CRUD |
| Test_CreateAndGetStrategicOrganization | Strategic org handling |
| Test_CreateDeleteCreateOrganization_SameId | Recreate with same ID |
| Test_CreateDeleteCreateOrganization_NewId | Recreate with new ID |
| Test_BatchGetOrganizationsByOrganizationIds | Batch retrieval |
| Test_GetAllOrganizationsUnderUltimateParent | Hierarchy query |
| Test_CreateAndGetOrganizationByMember | Member-based query |
| Test_UpdateAndGetOrganization | Update operations |
| Test_DeleteOrganization | Deletion cascade |
| Test_ObtainingAndRemovingOrganizationUpdateLocks | Locking operations |
| Test_OrganizationUpdateLockExpiration | Lock expiry |
| Test_QueryOrganizationByName | Name search |
| *4 additional persistence tests* | Various DynamoDB operations |

### OrganizationSyncServiceTests.cs (6 tests)

| Test Name | What It Tests |
|-----------|---------------|
| UpdateSalesforceOrganizations_CreatesNewOrganizations | New org sync creation |
| UpdateSalesforceOrganizations_UpdatesExistingOrganizations | Existing org sync update |
| UpdateSalesforceOrganizations_DeletesMissingOrganizations | Missing org sync deletion |
| UpdateSalesforceOrganizations_DeleteAndRecreateOrganizationPreservesOrganizationIds | ID preservation |
| *2 additional sync tests* | Various sync scenarios |

## Lambda Tests

### ChangeStreamLambdaTests.cs (8 tests)

| Test Name | What It Tests |
|-----------|---------------|
| EntryPoint_Constructs | Lambda entry point construction |
| FunctionHandler_GivenOrganizationInsert_Notifies | Insert event notification |
| FunctionHandler_GivenOrganizationModify_Notifies | Modify event notification |
| FunctionHandler_GivenOrganizationRemove_Notifies | Remove event notification |
| FunctionHandler_GivenGroupInsert_Notifies | Group insert notification |
| FunctionHandler_GivenGroupModify_Notifies | Group modify notification |
| FunctionHandler_GivenGroupRemove_Notifies | Group remove notification |
| FunctionHandler_GivenUnknownType_NoOp | Unknown type handling |

### MonolithSyncLambdaHandlerTests.cs (7 tests)

| Test Name | What It Tests |
|-----------|---------------|
| EntryPoint_Constructs | Lambda entry point construction |
| HandleAsync_GivenMetadataEvent_RoutesToMetadataProcessor | Metadata event routing |
| HandleAsync_GivenMembershipEvent_RoutesToMembershipProcessor | Membership event routing |
| HandleAsync_GivenBatchWithOneFailure_ReturnsPartialBatchFailure | Partial failure handling |
| HandleAsync_GivenNonHealthSystemEvent_SkipsProcessing | Non-health system filtering |
| HandleAsync_GivenNullSqsEvent_ReturnsEmptyBatchResponse | Null event handling |
| HandleAsync_GivenAllRecordsFail_ReturnsAllBatchFailures | Total failure handling |

## Unit Tests

### OrganizationGraphValidationServiceTests.cs (17 tests)

| Test Name | What It Tests |
|-----------|---------------|
| IsNewParentCyclic_NoParent_NotCyclic | No parent is not cyclic |
| IsNewParentCyclic_SelfParent_Cyclic | Self as parent is cyclic |
| IsNewParentCyclic_DirectChild_Cyclic | Direct child as parent is cyclic |
| IsNewParentCyclic_IndirectChild_Cyclic | Indirect child as parent is cyclic |
| IsNewParentCyclic_Sibling_NotCyclic | Sibling as parent not cyclic |
| IsNewParentCyclic_ThrowsWhenMaximumDepthExceeded | Depth limit exceeded |
| *11 additional cycle detection tests* | Various cycle scenarios |

### RuleServiceTests.cs (18 tests)

| Test Name | What It Tests |
|-----------|---------------|
| EqualsRule_CheckRule_Matches | Equals rule matching |
| EqualsRule_CheckRule_NoMatch | Equals rule non-matching |
| ContainsRule_CheckRule_Matches | Contains rule matching |
| ContainsRule_CheckRule_NoMatch | Contains rule non-matching |
| IntersectionOnlyRule_CheckRuleTest | Intersection rule logic |
| RulesEngine_ApplyRuleset_MatchesAll | Ruleset with all matching |
| RulesEngine_ApplyRuleset_MatchesNone | Ruleset with no matching |
| RulesEngine_ApplyManualInclusionsAndExclusions_Includes | Manual inclusions |
| RulesEngine_ApplyManualInclusionsAndExclusions_Excludes | Manual exclusions |
| RulesEngine_ApplyManualInclusionsAndExclusions_Both | Both inclusions and exclusions |
| RulesEngine_ApplyManualInclusionsAndExclusions_Override | Override automatic rules |
| RulesEngine_FilterInactiveEntities_Filters | Filter inactive entities |
| RulesEngine_FilterInactiveEntities_KeepsActive | Keep active entities |
| RulesEngine_FilterInactiveEntities_Empty | Empty list filtering |
| GroupMembershipCalculator_GetFilteredMembers_Basic | Basic membership calculation |
| GroupMembershipCalculator_GetFilteredMembers_WithRules | Calculation with rules |
| GroupMembershipCalculator_GetFilteredMembers_WithExclusions | Calculation with exclusions |
| MembershipDifferenceCalculator_CalculatesDiff | Diff calculation |

---

# provider-join-service

## Integration Tests

### InsuranceWizardTest.cs (26 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GetInsuranceWizard_Unauthorized_Returns401 | Unauthorized access |
| GetInsuranceWizard_NotFound_Returns404 | Lead not found |
| GetInsuranceWizard_ValidLead_Returns200 | Successful retrieval |
| PutInsuranceWizard_Unauthorized_Returns401 | Unauthorized update |
| PutInsuranceWizard_InvalidData_Returns400 | Invalid data validation |
| PutInsuranceWizard_ValidData_Updates | Successful update |
| *20 additional insurance wizard tests* | Various wizard scenarios |

### SignUpFlowTest.cs (10 tests)

| Test Name | What It Tests |
|-----------|---------------|
| CreateLead_ValidData_CreatesLead | Lead creation |
| CreateLead_DuplicateEmail_ReturnsExisting | Duplicate email handling |
| SubmitLead_ValidLead_SubmitsToSalesforce | Salesforce submission |
| SubmitLead_InvalidLead_Returns400 | Invalid lead validation |
| GetLeadStatus_ValidLead_ReturnsStatus | Status retrieval |
| UpdateLeadStatus_ValidTransition_Updates | Status transition |
| UpdateLeadStatus_InvalidTransition_Returns400 | Invalid transition |
| *3 additional flow tests* | Various flow scenarios |

### AccountCreationTests.cs (15 tests)

| Test Name | What It Tests |
|-----------|---------------|
| CreateAccount_ValidData_CreatesAccount | Account creation |
| CreateAccount_DuplicateEmail_Returns409 | Duplicate email conflict |
| CreateAccount_InvalidEmail_Returns400 | Email validation |
| ConfirmEmail_ValidToken_Confirms | Email confirmation |
| ConfirmEmail_ExpiredToken_Returns400 | Expired token handling |
| ConfirmEmail_InvalidToken_Returns401 | Invalid token handling |
| UpsertOnboardingPractice_ValidData_Upserts | Practice upsert |
| RateLimiting_TooManyRequests_Returns429 | Rate limiting |
| *7 additional account tests* | Various account scenarios |

## Unit Tests - API Layer

### ValidationExtensionsTests.cs (22 tests)

| Test Name | What It Tests |
|-----------|---------------|
| IsValidEmail_ValidEmail_ReturnsTrue | Valid email validation |
| IsValidEmail_InvalidEmail_ReturnsFalse | Invalid email validation |
| IsValidEmail_Null_ReturnsFalse | Null email handling |
| IsValidEmail_Empty_ReturnsFalse | Empty email handling |
| IsValidPhone_ValidPhone_ReturnsTrue | Valid phone validation |
| IsValidPhone_InvalidPhone_ReturnsFalse | Invalid phone validation |
| IsValidPhone_WithExtension_ReturnsTrue | Phone with extension |
| IsValidZipCode_ValidZip_ReturnsTrue | Valid zip code |
| IsValidZipCode_InvalidZip_ReturnsFalse | Invalid zip code |
| IsValidZipCode_ZipPlus4_ReturnsTrue | Zip+4 format |
| *12 additional validation tests* | Various validation scenarios |

### SelfSignupLeadStatusBuilderTest.cs (70+ tests)

| Test Category | What It Tests |
|---------------|---------------|
| State/View combinations | All invalid state/view combinations throw |
| Status transitions | Valid and invalid status transitions |
| View permissions | View permissions by user type |

### LeadHelperTests.cs (14 tests)

| Test Name | What It Tests |
|-----------|---------------|
| IsTestLead_TestEmail_ReturnsTrue | Test lead detection by email |
| IsTestLead_ProductionEmail_ReturnsFalse | Non-test email detection |
| IsTestLead_TestLastName_ReturnsTrue | Test lead by last name |
| IsTestLead_TestPracticeName_ReturnsTrue | Test lead by practice name |
| IsTestLead_CombinedIndicators_ReturnsTrue | Multiple test indicators |
| *9 additional helper tests* | Various helper scenarios |

### Authorization Handler Tests (18 tests total)

| Test File | Tests | What It Tests |
|-----------|-------|---------------|
| ProviderJoinServiceReadWriteDataRequirementHandlerTests.cs | 14 | PJS read/write authorization |
| SelfSignUpPracticeAuthorizationHandlerTests.cs | 8 | SelfSignUp practice auth |
| CsrAuthorizationHandlerTests.cs | 2 | CSR authorization |
| PracticeAuthorizationHandlerTests.cs | 8 | Practice authorization |

## Unit Tests - Infrastructure Layer

### LeadsServiceTests.cs (14 tests)

| Test Name | What It Tests |
|-----------|---------------|
| GetLead_ExistingLead_ReturnsLead | Lead retrieval |
| GetLead_NonExistent_ReturnsNull | Non-existent lead |
| SubmitStatus_ValidLead_Updates | Status update |
| SyncToSalesforce_ValidLead_Syncs | Salesforce sync |
| SyncToSalesforce_SalesforceError_Throws | Salesforce error handling |
| *9 additional leads service tests* | Various service scenarios |

### LeadSalesforceServiceTests.cs (~25 tests)

| Test Name | What It Tests |
|-----------|---------------|
| CreateLead_ValidData_CreatesSalesforceLead | Salesforce lead creation |
| CreateLead_DuplicateEmail_ReturnsExisting | Duplicate handling |
| UpdateLead_ExistingLead_Updates | Lead update |
| UpdateLead_NonExistent_Throws | Non-existent lead error |
| QueryLeads_ValidCriteria_ReturnsMatching | Lead query |
| *20 additional Salesforce tests* | Various Salesforce scenarios |

### InsuranceOnboardingServiceTest.cs (13 tests)

| Test Name | What It Tests |
|-----------|---------------|
| CreateEntry_ValidData_Creates | Entry creation |
| GetEntry_ExistingEntry_Returns | Entry retrieval |
| CheckEligibility_Eligible_ReturnsTrue | Eligibility check |
| CheckEligibility_NotEligible_ReturnsFalse | Ineligibility check |
| SaveEntry_ValidData_Saves | Entry save |
| SaveEntry_InvalidData_Throws | Invalid data handling |
| *7 additional onboarding tests* | Various onboarding scenarios |

### AccountCreationServiceTest.cs (~20 tests)

| Test Name | What It Tests |
|-----------|---------------|
| CreateAccount_ValidData_Creates | Account creation |
| CreateAccount_RateLimited_Throws | Rate limiting |
| VerifyEmail_ValidToken_Verifies | Email verification |
| VerifyEmail_ExpiredToken_Throws | Expired token handling |
| *16 additional account tests* | Various account scenarios |

## Lambda Tests

### FunctionTest.cs (3 tests)

| Test Name | What It Tests |
|-----------|---------------|
| TestReturnsId | Lambda handler returns input ID (TRIVIAL) |
| FunctionalTest_Success_LogsSuccess | Success logging |
| FunctionalTest_Error_LogsError | Error logging |

---

*Generated: 2026-04-09*
*Total tests inventoried: ~1,400+*
