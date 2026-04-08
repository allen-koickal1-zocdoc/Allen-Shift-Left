# Frontend Unit Tests - Pterodactyl Team

## Summary

**Critical Finding: No frontend unit tests exist for the Users Page owned by Pterodactyl.**

The `org-management` webapp (owned by @Zocdoc/user-permissions) contains only scaffold example tests - no actual user management tests.

---

## Team Ownership in frontend-monorepo

The `@Zocdoc/user-permissions` team owns:
- `/webapps/provider-join`
- `/webapps/org-management`

Both webapps have **minimal test coverage** - only example/scaffold tests exist.

---

## Important Note

**The `promo` and `fromo` packages do not exist in frontend-monorepo.** The Users Page UI may be:
1. In the **monolith** (legacy code)
2. In `org-management` webapp (new, under development)
3. Rendered by a different system

---

## Test Files Found

### org-management (Pterodactyl-owned)

| File | Tests | Status |
|------|-------|--------|
| `src/pages/Example/__tests__/ExamplePage-test.tsx` | `it('renders the example page with correct content')` | **SCAFFOLD ONLY** |
| `cypress/e2e/organization-management-tests.js` | `it('Visits the app')` - visits `/provider/organization-management` | **SMOKE ONLY** |
| `webpack/__tests__/bundles-tests.ts` | `it('has valid bundle names')` - validates webpack bundles | **INFRA ONLY** |

**Gap:** No actual user management, role management, or permissions tests. This appears to be a **new webapp in early development**.

---

### Related Tests (Other Teams)

The following tests exist but are owned by **other teams** (patient-booking):

#### Patient Permissions Page (`my-accounts-web-app`)

| File | What It Tests | Owner |
|------|---------------|-------|
| `pages/Permissions/__tests__/PermissionsContainer-tests.tsx` | User authentication, login state, data permission API | @Zocdoc/patient-booking |
| `pages/Permissions/__tests__/PermissionsView-tests.tsx` | Checkbox interactions, save functionality | @Zocdoc/patient-booking |
| `pages/Permissions/__tests__/utils-tests.ts` | Permission difference calculation | @Zocdoc/patient-booking |
| `components/PermissionSettings/__tests__/CheckBoxCard-tests.tsx` | Permission checkbox component | @Zocdoc/patient-booking |
| `api/permissionSettings/__tests__/getUserSavedData-tests.ts` | API calls for saved data | @Zocdoc/patient-booking |

**Note:** These are for **patient-side** data privacy permissions (GDPR/CCPA), not practice user management.

#### Role-Based Access Tests (`provider-dashboard-web-app`)

| File | What It Tests | Owner |
|------|---------------|-------|
| `features/appointment-report/utils/__tests__/accessChecks-test.ts` | `isFullAdminUser`, `isAppointmentManagementUser`, `isInternalUser` role checks | @Zocdoc/provider-dashboard |
| Same file | `canAccessAppointmentLinks`, `canAccessDisputeActions` permission checks | @Zocdoc/provider-dashboard |

**Note:** These test role-checking utility functions but are owned by another team.

---

## Gap Analysis

### Critical Gaps - No Tests Exist

| Component | Expected Location | Status |
|-----------|-------------------|--------|
| Users Page (list/table) | `org-management` or `promo` | **NO TESTS** |
| Add User Form | `org-management` or `promo` | **NO TESTS** |
| Edit User Form | `org-management` or `promo` | **NO TESTS** |
| Delete User Confirmation | `org-management` or `promo` | **NO TESTS** |
| Role Selection Component | `org-management` or `promo` | **NO TESTS** |
| Permission Matrix | `org-management` or `promo` | **NO TESTS** |
| User Invitation Flow | `org-management` or `promo` | **NO TESTS** |

### What Should Be Tested

1. **UsersPage Component**
   - Renders user table correctly
   - Pagination works
   - Search/filter functionality
   - Add user button visibility based on permissions

2. **AddUserForm Component**
   - Form validation (email, name)
   - Role selection
   - Permission assignment
   - Submit success/error handling

3. **EditUserForm Component**
   - Loads existing user data
   - Updates permissions correctly
   - Handles conflicts

4. **DeleteUser Component**
   - Confirmation dialog
   - Success/error handling

5. **RoleSelector Component**
   - Displays available roles
   - Handles selection
   - Shows permission preview

6. **API Hooks**
   - useGetUsers
   - useCreateUser
   - useUpdateUser
   - useDeleteUser
   - useGetRoles

---

## Recommendations

### P0 - Critical

1. **Add unit tests for Users Page components** - The entire Users Page frontend has zero test coverage

2. **Add unit tests for role/permission components** - Critical for RBAC functionality

### P1 - High

3. **Add integration tests for user management flows** - Add user, edit user, delete user flows

4. **Add API hook tests** - Test the frontend API layer

### P2 - Medium

5. **Add accessibility tests** - Ensure users page meets a11y standards

6. **Add error state tests** - Test loading, error, and empty states

---

## Comparison with E2E Coverage

| Feature | Frontend Unit Tests | Cypress E2E Tests |
|---------|---------------------|-------------------|
| Users Page Display | **NONE** | YES (9 tests) |
| Add User Flow | **NONE** | YES |
| Edit User Flow | **NONE** | YES |
| Delete User Flow | **NONE** | YES |
| Role Management | **NONE** | YES (10 tests) |

**Conclusion:** The Users Page relies entirely on E2E tests for coverage. There are no frontend unit tests, which means:
- Slow feedback loop (E2E tests are slow)
- Harder to test edge cases
- Component behavior not isolated

---

*Generated: 2026-04-09*
