# Provider MFA & Credential Compromise - PRD Gap Analysis

**Jira Epic:** [AUTH-3195](https://zocdoc.atlassian.net/browse/AUTH-3195)  
**PRD Author:** Ambreen Molitor  
**Analysis Date:** 2026-04-10  
**Status:** DRAFT

---

## Executive Summary

This analysis identifies gaps, ambiguities, and critical questions in the Provider MFA & Credential Compromise PRD. The PRD addresses a real security need (credential-stuffing attacks have cost >$100k and pose PHI exposure risk) but requires clarification in several areas before implementation.

---

## 1. Technical Architecture Gaps

| Gap | Impact | Question to Ask |
|-----|--------|-----------------|
| No Auth0 implementation details | Engineering can't estimate accurately | What Auth0 features are we leveraging? Universal Login, Actions, or custom flows? |
| MFA factor storage model undefined | Could affect user data migration | Where are MFA enrollments stored? Auth0 or Zocdoc DB? |
| Session token handling post-MFA unclear | Security vulnerability risk | Does MFA generate a new JWT or upgrade the existing one? |
| No API contract changes documented | Integration teams blocked | Will `/authenticate-password` endpoint change or will there be a new `/authenticate-mfa` endpoint? |

---

## 2. Requirement Ambiguities

| Requirement | Ambiguity | Clarifying Question |
|-------------|-----------|---------------------|
| "MFA required for designated provider segments" | What defines a segment? | Is segmentation by practice size, geography, specialty, or account age? Who maintains segment definitions? |
| "Smart capabilities - Skip MFA if logged in from trusted location" | No definition of "trusted" | How is trust established? IP whitelist? Device fingerprint? Cookie-based? What's the trust expiry? |
| "Phone number verification" | No verification flow described | Is this SMS OTP? Voice call? How do we handle international numbers? What's the cost per verification? |
| P0 vs P1 priority conflict | "Smart capabilities" marked P0/P1 | Is trusted location skip P0 (launch blocker) or P1 (fast-follow)? |

---

## 3. Missing Requirements

| Category | Missing Item | Why It Matters |
|----------|--------------|----------------|
| **Recovery flows** | What happens when email is compromised? | Attacker could intercept OTP if they have email access |
| **Shared inbox handling** | Many practices use shared admin emails | Email MFA fails for shared mailboxes |
| **Device management** | No "remember this device" spec | Users will be frustrated with MFA on every login |
| **Offline/degraded mode** | What if Auth0 is down? | No fallback = complete provider lockout |
| **Rate limiting on OTP** | How many OTP attempts before lockout? | Attackers could brute-force 6-digit codes |
| **OTP expiry** | How long is an OTP valid? | Too short = UX friction; too long = security risk |
| **Audit logging** | What auth events are logged? | Needed for incident forensics |

---

## 4. SSO Scope Concerns

| Constraint | Risk | Question |
|------------|------|----------|
| "Single-practice, all-admin, non-SPO" | Very narrow eligibility | What % of LPG/Enterprise actually qualifies? Could be <10% |
| SPO dependency unclear | Timeline risk | What SPO changes are needed? Is SPO work funded/prioritized? |
| "Vendor connection caps" | Could block rollout | How many SSO connections remain? What's the cost to add more? |
| FGA dependency for multi-practice | H2 2026 target | Is this acceptable for enterprise customers expecting SSO now? |

---

## 5. Metrics & Success Criteria Gaps

| Issue | Current State | What's Missing |
|-------|---------------|----------------|
| Login success rate baseline | "65-70%" | Is this pre- or post-MFA? What's acceptable degradation? |
| Support ticket threshold | "40/month" | What's the current baseline? Is 40 incremental or total? |
| No MFA completion rate target | - | What % of users must complete MFA challenge successfully? |
| No time-to-login metric | - | How much latency does MFA add? What's acceptable? |
| No rollback criteria | - | At what failure rate do we pause/rollback enforcement? |

---

## 6. Rollout & Operational Gaps

| Gap | Risk | Question |
|-----|------|----------|
| No grace period defined | Provider lockout on enforcement date | How long after enforcement before blocking non-compliant users? |
| No exception process | Sales escalations will flood in | Who approves MFA exemptions? For how long? |
| No support runbook | T&S can't help locked users | What's the identity verification process for manual resets? |
| No self-service recovery | High support burden | Can users recover via backup codes/alternative email? |
| Communication timeline vague | Providers surprised | When do announcements go out? 30 days? 60 days? |

---

## 7. Edge Cases Not Addressed

| Scenario | Gap |
|----------|-----|
| Provider changes email address | Is MFA re-enrollment required? |
| Practice merges/splits | How does MFA config transfer? |
| API-only integrations | Do service accounts need MFA? How? |
| Mobile app authentication | Same MFA flow or different? |
| Concurrent login attempts | Can attacker trigger lockout by spamming wrong OTPs? |
| Email delivery failures | What if OTP email goes to spam? Retry? Alternative? |

---

## 8. Risk Matrix

| Risk | Likelihood | Impact | Mitigation Needed |
|------|------------|--------|-------------------|
| Provider drop-off during MFA rollout | High | High | Phased rollout, clear comms, grace periods |
| Shared inbox users locked out | High | Medium | Alternative factor (SMS) or admin delegation |
| Auth0 outage = complete lockout | Low | Critical | Fallback authentication mechanism |
| Support ticket surge | High | Medium | Self-service recovery, clear error messages |
| SSO eligibility too narrow | High | Medium | Accelerate FGA work or expand criteria |
| Attackers shift to email compromise | Medium | High | Consider TOTP as primary, not email OTP |

---

## 9. Recommendations

1. **Add device trust ("Remember this device")** to Phase 1, not Phase 2 - otherwise MFA fatigue will crush adoption
2. **Define OTP parameters explicitly**: validity window (5 min?), retry limit (3?), resend cooldown (60s?)
3. **Create a test account bypass mechanism** for QA automation before enforcement
4. **Specify shared inbox solution** before rollout - this will affect many practices
5. **Add rollback criteria** to metrics section - what failure rate triggers pause?
6. **Consider TOTP/authenticator apps** as alternative to email - email is vulnerable if attacker has credentials + email access

---

## 10. Critical Questions by Stakeholder

### For Product/PM (Ambreen Molitor):
1. What's the enforcement timeline? The PRD says "~6 engineering weeks" but no target date for mandatory MFA.
2. What's the segmentation strategy? Which providers get MFA first? All at once or phased by size/risk?
3. What's the exception policy? Will there be a way to exempt specific providers? Who approves?
4. How do we handle shared inboxes? Email MFA won't work for `frontdesk@practice.com`.

### For Engineering (Ben Lee):
5. What's the Auth0 integration pattern? Are we using Auth0 Actions, Rules, or custom API?
6. What's the session upgrade flow? Does passing MFA issue a new token or add a claim?
7. What's the API contract? New endpoints or modifications to existing?
8. How do we handle the ~90% who've never changed passwords? Force password reset + MFA enrollment simultaneously?

### For Security/T&S:
9. What risk signals trigger step-up MFA in Phase 2? IP reputation? Impossible travel? Device fingerprint?
10. What's the OTP brute-force protection? Rate limits? Lockout after N failures?
11. What's the incident playbook for MFA bypass attempts?
12. Should compromised credential lists trigger forced password reset + MFA?

### For Sales/Commercial (Tyler Litke):
13. What's the commercial impact of blocking non-compliant providers? Revenue at risk?
14. Are there contractual obligations that prevent MFA enforcement for certain accounts?
15. Should MFA be a selling point or just table stakes? Pricing implications?

### For QA/Testing:
16. How do we test MFA in automation? Need test accounts with known OTP seeds or bypass tokens.
17. What's the test account strategy? The PRD mentions P1 for test accounts but no details.
18. How do we validate email/SMS delivery in E2E tests?
