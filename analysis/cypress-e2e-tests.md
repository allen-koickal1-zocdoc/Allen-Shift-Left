# Cypress E2E Tests - Pterodactyl Team Features

## Summary

| Category | Test Count | File Location |
|----------|------------|---------------|
| User Management | 9 | `cypress/e2e/rbac/user-management-smoke.spec.js` |
| RBAC (Role-Based Access) | 10 | `cypress/e2e/rbac/rbac-smoke.spec.js` |
| Practice Management | 26 | `cypress/e2e/rbac/practicemgmt-smoke.spec.js` |
| SPO Management | 5 | `cypress/e2e/rbac/spomgmt-smoke.spec.js` |
| Billing Management | 1 | `cypress/e2e/rbac/billingmgmt-smoke.spec.js` |
| Appointment Management | 6+ | `cypress/e2e/rbac/appointmentmgmt-smoke.spec.js` |
| Providers Page | 9 | `cypress/e2e/provider/provider-providerspage-regression.spec.js` |
| Auth (shared) | 7 | `cypress/e2e/BU/Infrastructure/Auth/` |
| **Total** | **~70+** | |

---

## Test Inventory

### 1. User Management Tests

**File:** `cypress/e2e/rbac/user-management-smoke.spec.js`  
**Suite:** `/provider/settings/users`  
**Type:** Smoke

| Test Case | What It Tests |
|-----------|---------------|
| `Create User - should create a user with API response verification` | Creates a new staff user via Add User flow, verifies 201 response, confirms user appears in table |
| `User Management Page - should display user management page with users table` | Verifies users page loads with practice-users-page-container-v2 |
| `User Management Page - should display add user button when practice is self sign up complete` | Verifies add-another-user button visibility |
| `User Management Page - should navigate to add user page when add button is clicked` | Verifies navigation to add user form |
| `User Management Page - should display account settings link` | Verifies users-page-account-link presence and href |
| `User Management Page - should display pagination when there are multiple pages of users` | Verifies pagination on users table |
| `User Management Page - should allow clicking on user row to view user details` | Verifies user detail navigation |
| `Edit and Delete User Flow - should edit a user with API response verification` | Edits user permissions (Full Access to Custom), verifies 204 response on practice-user-permissions API |
| `Edit and Delete User Flow - should delete a user with API response verification` | Deletes user, verifies 204 response, confirms user removed from table |

---

### 2. RBAC Tests (Role-Based Access Control)

**File:** `cypress/e2e/rbac/rbac-smoke.spec.js`  
**Type:** Smoke

#### Suite: RBAC SMOKE - Appointments User

| Test Case | What It Tests |
|-----------|---------------|
| `Appts user - Verify landing page is Inbox and all other pages are accessible` | Appointments user lands on inbox, can access calendar, dashboard, appointment report, settings |
| `Verify certain pages are inaccessible for Appts user` | Verifies SPO and Providers pages are blocked, API returns 403 |

#### Suite: RBAC SMOKE - Practice Settings + Appointments

| Test Case | What It Tests |
|-----------|---------------|
| `Appts+PS user - Verify landing page is Inbox and all other pages are accessible` | Practice Settings + Appts user can access inbox, calendar, providers page, dashboard, settings |
| `Verify certain pages are inaccessible for Appts+PS user` | Users page shows error, website settings redirect to inbox |

#### Suite: RBAC SMOKE - Billing User

| Test Case | What It Tests |
|-----------|---------------|
| `Verify Billing user lands on Performance dashboard page` | Billing user default landing page, accessible pages |
| `Verify that Billing user is unable to access certain pages` | Calendar, providers page, COVID vaccine settings, video visit blocked |

#### Suite: RBAC SMOKE - Practice Settings User

| Test Case | What It Tests |
|-----------|---------------|
| `Verify Practice settings user lands on Provider's page` | Practice Settings user homepage, accessible settings tabs |
| `Verify non-visibility of certain pages for Practice user` | Calendar, inbox, home tabs not visible; settings-users/billing/alerter not visible |

#### Suite: RBAC SMOKE - SPO User

| Test Case | What It Tests |
|-----------|---------------|
| `Verify visibility of pages for SPO user access` | SPO user dashboard landing, Account/Legal settings only |
| `Verify certain pages not accessible for SPO user` | Home, calendar, inbox, performance, providers pages blocked |

---

### 3. Practice Management Smoke Tests

**File:** `cypress/e2e/rbac/practicemgmt-smoke.spec.js`  
**Type:** Smoke

| Suite | Test Case | What It Tests |
|-------|-----------|---------------|
| Instant Add-on Flow | `Verifying auto-population when user enters valid NPI` | NPI lookup auto-fills provider info |
| Insurance Management | `Verify Practice Settings User can add and remove insurance carriers` | Full insurance add/remove flow |
| Insurance Management | `Verify Practice Settings User can access insurance settings from Settings menu` | Settings navigation |
| Providers Page | `Verify Practice Settings User can access and interact with Providers page` | Filters, search, provider listing |
| Providers Page | `Verify Practice Settings User can access provider profile from Providers page` | Provider profile navigation |
| Providers Page | `Verify Practice Settings User can navigate to Providers page via header icon` | Header navigation |
| Visit Reasons | `Verify Practice Settings User can access Visit Reasons settings` | VR settings access |
| Visit Reasons | `Verify Practice Settings User can access VR Presets page` | VR presets functionality |
| Visit Reasons | `Verify Practice Settings User can interact with VR length inputs` | VR search and interaction |
| Dashboard | `Verify Practice Settings User can access Performance Dashboard` | Dashboard access |
| Dashboard | `Verify Practice Settings User can navigate to Performance Dashboard from navbar` | Navbar navigation |
| Dashboard | `Verify Practice Settings User Homepage is Providers page after login` | Login redirect validation |
| Practice Settings | `Verify Practice Settings User can access Practice settings via dropdown` | Dropdown navigation |
| Practice Settings | `Verify Practice Settings User can access available settings tabs` | Settings tab visibility |
| Practice Settings | `Verify Practice Settings User cannot access restricted pages` | Calendar, inbox, home blocked |
| Dropdown Menu | Multiple tests for Invite, Add Provider, Settings, Features, Help Center, Contact Us, Sign Out | Dropdown menu items |
| Provider Profile | `Verify Practice Settings User can access provider profile settings` | COVID-19 settings access |
| Provider Profile | `Verify Practice Settings User can view provider specialties section` | Provider specialties/VR sections |

---

### 4. SPO Management Smoke Tests

**File:** `cypress/e2e/rbac/spomgmt-smoke.spec.js`  
**Type:** Smoke

| Test Case | What It Tests |
|-----------|---------------|
| `should display provider groups tab with table and controls` | SPO dashboard provider groups tab |
| `should display trends tab with filters` | Trends tab, date range, provider group dropdown |
| `should navigate between tabs` | Tab navigation |
| `should navigate back to dashboard from campaign page` | Back navigation |
| `should complete full campaign lifecycle: create, edit, pause, and delete` | Full CRUD for SPO campaigns |

---

### 5. Billing Management Smoke Tests

**File:** `cypress/e2e/rbac/billingmgmt-smoke.spec.js`  
**Type:** Smoke

| Test Case | What It Tests |
|-----------|---------------|
| `Viewing and Checking Billing and Account Related functionality` | View billing page, replace/add/edit/delete ACH accounts, edit rollovers, view invoice details |

---

### 6. Appointment Management Smoke Tests

**File:** `cypress/e2e/rbac/appointmentmgmt-smoke.spec.js`  
**Type:** Smoke

| Test Case | What It Tests |
|-----------|---------------|
| `Book an appointment for Inbox Testing` | Patient booking flow |
| `Verify that an appointment management user can confirm an appointment` | Appointment confirmation, status change |
| `Verify that an appointment management user can reschedule an appointment` | Appointment modification |
| `Verify that an appointment management user can delete an appointment` | Appointment cancellation flow |
| `Verify that an appointment management user can send a manual intake request` | Manual intake request to patients |
| `Verify that an appointment management user can use filters in the Inbox` | Provider/Location filters |
| Additional calendar, busy block, and scheduling tests | Calendar interactions, availability management |

---

### 7. Providers Page Regression Tests

**File:** `cypress/e2e/provider/provider-providerspage-regression.spec.js`  
**Type:** Regression

| Test Case | What It Tests |
|-----------|---------------|
| `Verify the presence of Filters in the new Providers page` | Role filter (Providers, Resources, Facilities), clear filters |
| `Verify the presence & behaviour of Search bar in the providers page` | Search functionality |
| `Verify the columns present in the providers page of Local & enterprise(LPG) practice` | Column visibility (name, status, searchability score, date added) |
| `Verify the different Status Categories` | Missing information, Pending approval, Setup incomplete, Deactivated, No availability, Can't receive bookings, Can receive bookings |
| `Verify the Date added column` | Date format |
| `Verify the empty States when there are no providers found on search` | Empty search state |
| `Verify the empty States when there are no providers present in the practice` | Empty practice state |
| `Verify the presence of practice control feature` | Practice filter for enterprise users |
| `Verify the functional behaviour of the practice control feature modal` | Practice filter modal |

---

### 8. Authentication Tests (Shared with Auth Team)

**File:** `cypress/e2e/BU/Infrastructure/Auth/Flows/provider-signin-flow.spec.js`  
**Type:** Flow

| Test Case | What It Tests |
|-----------|---------------|
| `Provider can login and log out to log back in` | Provider login, default landing page |

**File:** `cypress/e2e/BU/Infrastructure/Auth/Pages/signin-page.spec.js`  
**Type:** Page

| Test Case | What It Tests |
|-----------|---------------|
| `Locked Provider should see error message when trying to log in` | Locked account error message |
| `MFA enabled user can get error message for incorrect verification` | MFA verification error |
| `Form Validation Checks - Missing Email and Invalid email` | Email validation |
| `Form Validation Checks - Missing Password` | Password validation |
| `Form Validation Checks - Non-existent user` | Invalid credentials error |
| `Form Validation Checks - Incorrect Password` | Wrong password error |

---

## Directory Structure

```
cypress/e2e/
├── rbac/
│   ├── user-management-smoke.spec.js      (Primary - Users Page)
│   ├── rbac-smoke.spec.js                 (Primary - Role Management)
│   ├── practicemgmt-smoke.spec.js         (Primary - Practice Settings)
│   ├── spomgmt-smoke.spec.js              (SPO user role testing)
│   ├── billingmgmt-smoke.spec.js          (Billing user role testing)
│   └── appointmentmgmt-smoke.spec.js      (Appointments user role testing)
├── provider/
│   └── provider-providerspage-regression.spec.js  (Providers & Staff page)
└── BU/Provider/Acquisition/Account-User-Setup/
    └── OWNERSHIP.md                       (Pterodactyl ownership declaration)
```

---

## Gap Analysis

### Missing E2E Tests

| Feature | Gap |
|---------|-----|
| **Organization-level permissions** | No tests for org-level role management |
| **Permission inheritance** | No tests for inherited permissions from org to practice |
| **Batch user operations** | No tests for bulk user management |
| **User invitation flow** | No tests for invitation acceptance/rejection |
| **Permission change notifications** | No tests for notification triggers |
| **Edge cases** | Concurrent user edits, permission conflicts |

### Recommendations

1. **Add organization permission tests** - Test org-level role assignment
2. **Add permission inheritance tests** - Test parent org → child practice inheritance
3. **Add batch operations tests** - Test bulk user invite/remove
4. **Add negative test cases** - Test permission denial scenarios more thoroughly

---

*Generated: 2026-04-09*
