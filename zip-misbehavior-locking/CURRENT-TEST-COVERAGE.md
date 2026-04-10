# ZIP Misbehavior Locking - Current Test Coverage Analysis

**Repository:** zocdoc/sandbox (Cypress E2E)  
**Analysis Date:** 2026-04-10  
**Auth Team Slack:** #auth  

---

## Test Structure

```
cypress/e2e/BU/
├── Infrastructure/Auth/
│   └── Pages/signin-page.spec.js       # Login lockout tests
│   └── Flows/patient-signin-flow.spec.js
├── Marketplace/Booking/
│   └── Flows/booking-flow.spec.js      # Appointment stacking blocks
│   └── Flows/profile-booking-flow.spec.js
```

---

## Currently Tested Scenarios

### 1. Login Lockout (Brute Force Protection) ✅

**File:** `signin-page.spec.js`

| Test | Description | Test Account |
|------|-------------|--------------|
| Locked Provider error | Provider sees "attempted too many times" | `qatestdocR@test.zocdoc.com` |
| Locked Patient redirect | Patient redirected to `/lockedaccount` | `qa+lockedautomationpt@test.zocdoc.com` |

**Note:** This tests brute-force lockout, NOT T&S misbehavior locks.

### 2. Password Reset Lockout ✅

**File:** `forgot-password-page.spec.js`

| Test | Description | Test Account |
|------|-------------|--------------|
| Locked account cannot reset | Error "password cannot be reset at this time" | `qa+lockedauto@test.zocdoc.com` |

### 3. Booking Appointment Stacking ✅

**File:** `booking-flow.spec.js`

| Test | Type | Validation Code |
|------|------|-----------------|
| Soft block modal | Warning, can proceed | `AppointmentStackingSoftBlock` |
| Hard block modal | Must replace existing | `AppointmentStackingHardBlock` |

**Support Commands:**
- `verifySoftBlockModal()` - checks for "replace-existing-appointment" and "continue-anyway"
- `verifyHardBlockModal()` - checks for "replace-existing-appointment" only

### 4. Insurance/Network Restrictions ✅

**File:** `profile-booking-flow.spec.js`

| Test | Description |
|------|-------------|
| OON block | Out-of-network patients blocked from in-network-only providers |
| Age restrictions | Pediatric/adult age mismatches blocked |

---

## Critical Gaps for ZIP Misbehavior Locking

### HIGH PRIORITY - Must Have

| Gap | Description | Why Critical |
|-----|-------------|--------------|
| **T&S Misbehavior Block** | No test for users blocked due to T&S violations | Core feature |
| **Booking Block Message** | No test for block message shown during booking | User-facing |
| **Login vs Booking Block** | No test verifying blocked user CAN login but CANNOT book | Key behavior change |
| **Amnesty Verification** | No test that previously blocked user can now book | Migration validation |
| **Phone Number Block** | No test for booking blocked by phone number | Mentioned in spec |

### MEDIUM PRIORITY - Important

| Gap | Description |
|-----|-------------|
| Block reason display | What message does user see? |
| Retool lock/unlock | Can't automate Retool, but can test API |
| Multi-patient profile | If one profile blocked, test others |
| Block persistence | Verify block survives session/logout |
| Appeal flow | User contesting a block |

### LOWER PRIORITY - Edge Cases

| Gap | Description |
|-----|-------------|
| Block during mid-booking | User blocked while in flow |
| Phone number transfer | New user gets blocked phone |
| Bulk lock behavior | Many locks at once |

---

## Test Account Needs

To properly test the new locking system, we need:

| Account Type | Purpose | Current Status |
|--------------|---------|----------------|
| Booking-blocked user | Can login, cannot book | ❌ Not available |
| Login-blocked user | Cannot login at all | ❌ Not available |
| Amnestied user | Previously blocked, now can book | ❌ Not available |
| Phone-blocked user | Phone number is blocked | ❌ Not available |
| Multi-profile user | One profile blocked | ❌ Not available |

**Action Required:** Work with Auth/T&S to provision test accounts before launch.

---

## Proposed Test Scenarios

### Phase 1: Core Lock/Unlock Behavior

```gherkin
Scenario: Booking-blocked user can login but cannot book
  Given a user is booking-blocked in the system
  When they attempt to login
  Then they should successfully authenticate
  When they attempt to book an appointment
  Then they should see the booking block message
  And the booking should be prevented

Scenario: Login-blocked user cannot authenticate
  Given a user is login-blocked in the system
  When they attempt to login
  Then they should see the login block message
  And authentication should fail

Scenario: Amnestied user can login and book
  Given a user was previously blocked
  And they have been granted amnesty
  When they attempt to login
  Then they should successfully authenticate
  When they attempt to book an appointment
  Then the booking should succeed
```

### Phase 2: Block Management

```gherkin
Scenario: T&S can block user from booking via API
  Given a T&S operator with appropriate permissions
  When they submit a booking block request for user X
  Then user X should be booking-blocked
  And an audit record should be created

Scenario: T&S can view block status
  Given a blocked user
  When T&S queries the lock status API
  Then they should see block type, reason, timestamp, and operator
```

### Phase 3: Edge Cases

```gherkin
Scenario: Phone number block prevents booking
  Given phone number 555-1234 is blocked
  And user A has phone 555-1234
  When user A attempts to book
  Then the booking should be prevented

Scenario: User with multiple patient profiles - partial block
  Given user has patient profiles Alice and Bob
  And Alice profile is booking-blocked
  When user attempts to book as Alice
  Then booking should be blocked
  When user attempts to book as Bob
  Then booking should succeed
```

---

## API Testing Requirements

If the new microservice exposes APIs, we should add API tests for:

| Endpoint | Test Cases |
|----------|------------|
| `GET /lock-status/{userId}` | Valid user, invalid user, no permission |
| `POST /lock` | Lock user, lock phone, invalid input, duplicate lock |
| `POST /unlock` | Unlock user, already unlocked, invalid input |
| `GET /locks` | Pagination, filtering, search |
| `POST /bulk-lock` | Valid CSV, partial failures, empty CSV |

---

## Integration Test Dependencies

| System | Dependency |
|--------|------------|
| New locking microservice | Need staging deployment |
| Retool app | Can't automate directly |
| CISTERN | Need test data subset |
| Booking service | Must respect new lock API |
| Monolith | UnifiedNotes update verification |

---

## Recommendations

1. **Create test accounts immediately** - Block testing without test accounts is impossible
2. **Add API layer tests** - Don't rely solely on E2E for locking logic
3. **Mock the lock service** - For booking E2E, mock lock responses to test UI behavior
4. **Add monitoring tests** - Verify DataDog alerts fire on unusual lock activity
5. **Test amnesty in staging** - Run amnesty migration in staging first, verify with E2E
