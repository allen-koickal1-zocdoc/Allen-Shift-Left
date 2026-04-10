# Provider MFA - Current Test Coverage Analysis

**Repository:** zocdoc/sandbox (Cypress E2E)  
**Analysis Date:** 2026-04-10  
**Auth Team Slack:** #auth  
**Auth Jira:** AUTH

---

## Test Structure

```
cypress/e2e/BU/Infrastructure/Auth/
├── Pages/
│   ├── signin-page.spec.js
│   ├── forgot-password-page.spec.js
│   └── create-user-page.spec.js
├── Flows/
│   ├── provider-signin-flow.spec.js
│   ├── patient-signin-flow.spec.js
│   └── password-recovery-flow.spec.js
└── OWNERSHIP.md
```

---

## Currently Tested Scenarios

### 1. Basic Login/Logout Flows ✅
- Provider login with password
- Patient login with password
- Logout functionality
- Redirect to appropriate dashboards (home/calendar/performance)

**Files:**
- `provider-signin-flow.spec.js`
- `patient-signin-flow.spec.js`

### 2. MFA Error Case ✅ (Partial)
- MFA enabled user verification flow exists
- Test for incorrect MFA code entry with error message
- Test user: `qa+automfa@test.zocdoc.com`

**File:** `signin-page.spec.js` (Lines 27-47)

```javascript
it("MFA enabled user can get an error message to realize incorrect verification attempt", () => {
    cy.visit("https://www.zocdoc.com/signin")
    cy.get('[data-test="email-form-textbox-input"]').type("qa+automfa@test.zocdoc.com")
    cy.get('[data-test="email-form-continue-button"]').click()
    cy.get('[data-test="password-input"]').type("zocdoc@123")
    cy.get('[data-test="sign-in-form-submit"]').click()
    cy.get('[data-test="verification-form-text-input"]').type("123456")
    cy.get('[data-test="verification-form-continue-button"]').click()
    cy.get('[data-test="verification-form-text-error"]').should(
        "contain.text",
        "Please double-check the code and try again."
    )
})
```

### 3. Form Validation & Error Handling ✅
- Email validation (required, format)
- Password validation (required)
- Non-existent user handling
- Incorrect password handling
- Locked account detection

### 4. Account Lockout ✅
- Provider lockout after too many attempts
- Patient locked account detection
- Error messaging and redirect to `/lockedaccount`

**Test Credentials:**
- Locked Provider: `qatestdocR@test.zocdoc.com`
- Locked Patient: `qa+lockedautomationpt@test.zocdoc.com`

### 5. Password Reset Flow ✅
- Forgot password page accessible
- Email validation during reset
- Confirmation message display

**File:** `forgot-password-page.spec.js`

### 6. Social Login Buttons ✅ (Visibility Only)
- Google login link visibility
- Apple login link visibility
- No actual OAuth flow tests

---

## Critical Gaps for MFA Rollout

### HIGH PRIORITY - Must Have Before Launch

| Gap | Description | Blocking? |
|-----|-------------|-----------|
| **MFA Success Flow** | No test for valid MFA code completion | Yes |
| **MFA Enrollment** | No test for initial MFA setup | Yes |
| **Email OTP Delivery** | No validation of OTP email receipt | Yes |
| **SMS OTP Flow** | No tests for phone-based MFA | Yes |
| **Session Post-MFA** | No validation of authenticated state after MFA | Yes |

### MEDIUM PRIORITY - Needed for Full Coverage

| Gap | Description |
|-----|-------------|
| Recovery codes usage | Backup authentication method |
| MFA code expiration | Time-based validation |
| MFA retry limits | Brute-force protection |
| Device trust/remember | Skip MFA for trusted devices |
| Step-up MFA for sensitive actions | Re-authentication flows |

### LOWER PRIORITY - Edge Cases

| Gap | Description |
|-----|-------------|
| MFA with network issues | Offline/degraded handling |
| Cross-device MFA | Session sync |
| MFA resend functionality | Code re-delivery |
| Concurrent login handling | Race conditions |

---

## SSO Test Gaps

| Scenario | Status | Notes |
|----------|--------|-------|
| Google OAuth complete flow | ❌ Not tested | Only button visibility |
| Apple OAuth complete flow | ❌ Not tested | Only button visibility |
| SAML SSO integration | ❌ Not tested | Enterprise feature |
| OIDC SSO integration | ❌ Not tested | Enterprise feature |
| SSO session management | ❌ Not tested | - |
| SSO logout/SAML SLO | ❌ Not tested | - |

---

## Test Infrastructure Available

### Custom Commands
- `cy.loginByAPI(email, password)` - API-based authentication
- `cy.stubNetworkCalls()` - Stub analytics/tracking
- `cy.EnterTestDirByCookie()` - Test directory setup
- `cy.setCookie()` / `cy.getCookie('JWTv2')` - Token management

### Test Accounts
| Purpose | Email | Notes |
|---------|-------|-------|
| MFA-enabled | `qa+automfa@test.zocdoc.com` | Has MFA configured |
| Locked provider | `qatestdocR@test.zocdoc.com` | Triggers lockout |
| Locked patient | `qa+lockedautomationpt@test.zocdoc.com` | Triggers lockout |

### Configuration
- Base URL: `https://www.zocdoc.com/`
- API Endpoint: `/accounts/v2/authentication/authenticate-password`
- Project ID: `wgw1u4`
- Retries: 2 (both modes)
- Timeout: 36000ms

---

## Recommended Test Plan for MFA

### Phase 1: Core MFA Tests (P0)
1. Valid MFA code completes authentication
2. MFA enrollment flow for new users
3. Email OTP delivery and entry
4. MFA code expiration handling
5. MFA retry limit enforcement

### Phase 2: Recovery & Edge Cases (P1)
6. Backup/recovery code usage
7. MFA resend functionality
8. Device trust ("remember this device")
9. Step-up MFA for sensitive operations

### Phase 3: SSO Tests (P1)
10. SSO redirect to IdP
11. SSO return and session creation
12. SSO logout handling

---

## Test Account Requirements for MFA Automation

To properly automate MFA tests, we need:

1. **Known OTP seed accounts** - Test accounts with TOTP seeds we control
2. **Bypass tokens** - Test-only tokens that skip MFA for automation
3. **Email interception** - Mailinator or similar for OTP email capture
4. **Phone number interception** - Twilio test numbers for SMS OTP

**Action Required:** Work with Auth team to provision these before enforcement rollout.
