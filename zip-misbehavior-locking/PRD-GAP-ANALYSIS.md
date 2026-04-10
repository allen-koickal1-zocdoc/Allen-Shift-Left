# ZIP - Misbehavior Lock Revamp - Gap Analysis

**Jira Epic:** [AUTH-3025](https://zocdoc.atlassian.net/browse/AUTH-3025)  
**Tech Spec Author:** Ben Lee  
**Analysis Date:** 2026-04-10  
**Status:** In Progress

---

## Executive Summary

This initiative proposes separating login blocking from booking blocking, granting amnesty to ~8K previously locked users, and building new tooling for T&S to manually manage blocks. The goal is to decouple business logic from authentication while increasing booking conversion.

**Key Decision:** ~12K users will remain booking-locked (from CISTERN list), while ~8K users get amnesty. All users will be able to login; blocking moves to booking time.

---

## 1. Architecture & Design Gaps

| Gap | Impact | Question to Ask |
|-----|--------|-----------------|
| No microservice API contract defined | Engineering can't integrate | What endpoints will the new locking microservice expose? |
| Data model incomplete | Can't build tooling | What's the full schema for lock records (userId, patientId, phoneNumber, reason, timestamp, lockedBy)? |
| No event/audit trail spec | Compliance risk | How are lock/unlock events logged? What's the retention policy? |
| Phone number blocking logic unclear | Edge cases will fail | If user A is blocked on phone X, and user B adds phone X, is B blocked? |
| Device fingerprint mentioned but not specified | Future-proofing unclear | Is device-based blocking in scope or deferred? |

---

## 2. Requirement Ambiguities

| Requirement | Ambiguity | Clarifying Question |
|-------------|-----------|---------------------|
| "Booking blocked but can login" | When is block surfaced? | At booking start, slot selection, or confirmation? Different UX implications. |
| "T&S can lock/unlock via Retool" | No workflow defined | What's the review/approval process? Can one person lock without oversight? |
| "Bulk upload CSV" | No validation rules | What happens if CSV has invalid userIds? Partial success or full rollback? |
| "Login lock for compromised accounts" | Overlap with MFA work | How does this interact with AUTH-3195 MFA enforcement? |
| "Amnesty for locked users" | No notification plan | Do amnestied users get notified? How do they know they can book again? |

---

## 3. Missing Requirements

| Category | Missing Item | Why It Matters |
|----------|--------------|----------------|
| **User communication** | What message do booking-blocked users see? | UX critical - vague messages cause support calls |
| **Appeal process** | How do users contest a block? | Legal/compliance requirement |
| **Expiration** | Do blocks expire automatically? | ~12K permanent blocks seems excessive |
| **Escalation** | Who handles edge cases T&S can't resolve? | Need clear ownership |
| **Metrics** | No success criteria defined | How do we know this is working? |
| **Rollback plan** | What if amnesty causes booking quality crash? | Need ability to re-lock users |
| **Provider notification** | Do providers know a patient was previously blocked? | May affect trust |

---

## 4. Data Migration Concerns

| Issue | Risk | Question |
|-------|------|----------|
| CISTERN list accuracy | Blocking wrong users | How was this list curated? What's the false positive rate? |
| One-way migration | Can't undo easily | If we discover CISTERN missed bad actors, how do we catch up? |
| Historical context loss | T&S loses investigation history | Where is the reasoning for original blocks stored? |
| Phone number orphans | Blocks may not apply | If phone moved to new account, is old block still valid? |
| Patient vs User confusion | Wrong entity blocked | Spec mentions both - which is source of truth? |

---

## 5. Tooling Gaps (Retool)

| Feature Mentioned | Gap | Question |
|-------------------|-----|----------|
| "Bulk upload CSV" | No format spec | What columns? What validation? |
| "Lock with reason/notes" | No reason taxonomy | Free text or predefined reasons? |
| "List blocked users (nice to have)" | Pagination/search? | 12K users - how do they find specific ones? |
| "View lock status" | No history | Can they see who locked and when? |
| "Link from PSP to Retool" | No mockup | What's the user flow for service agents? |

---

## 6. Security & Compliance Gaps

| Gap | Risk | Question |
|-----|------|----------|
| No permission model details | Unauthorized locks | Who exactly can lock? What's the RBAC? |
| No audit requirements | Legal exposure | What audit trail is legally required? |
| "Drug seeking behavior" mentioned | HIPAA concern | Is this PHI? How is it stored/accessed? |
| No legal review confirmation | Contractual breach | Has legal confirmed amnesty doesn't violate agreements? |

---

## 7. Edge Cases Not Addressed

| Scenario | Gap |
|----------|-----|
| User with multiple patient profiles | If one profile misbehaves, are all blocked? |
| Shared phone number (family) | If parent blocked, can child's profile book? |
| User changes phone after block | Is block tied to user or phone? Both? |
| Blocked user creates new account | How is this detected/prevented? |
| Provider-initiated block | Can providers request patient blocks? Process? |
| Temporary vs permanent blocks | Is there a distinction? Auto-expiry? |
| Block during active booking | What happens if user is mid-booking when blocked? |
| Booking on behalf (caregiver) | If caregiver is blocked, can they book for patient? |

---

## 8. Integration Points Not Specified

| System | Question |
|--------|----------|
| Monolith | How does new service communicate? API? Events? |
| Booking service | What contract does booking expect? |
| PSP (Provider Support Portal) | How is lock status surfaced? |
| Service agent tools | What do agents see/do? |
| DataDog/monitoring | What alerts exist for unusual lock activity? |
| CISTERN | Is this a one-time export or ongoing sync? |

---

## 9. Metrics & Success Criteria (Missing)

The spec optimizes for "dev speed and increase in bookings" but doesn't define:

| Metric Needed | Why |
|---------------|-----|
| Booking conversion lift | Measure amnesty impact |
| Bad booking rate | Ensure quality doesn't crash |
| Support ticket volume | Measure user confusion |
| T&S workload | Are they overwhelmed with manual reviews? |
| Re-block rate | How many amnestied users get blocked again? |
| Appeal volume | Are blocks being contested? |

---

## 10. Risk Matrix

| Risk | Likelihood | Impact | Mitigation Needed |
|------|------------|--------|-------------------|
| Amnesty releases actual bad actors | Medium | High | Monitor booking quality, quick re-block capability |
| T&S overwhelmed with manual work | High | Medium | Clear escalation paths, possible automation later |
| CISTERN list has false positives | Medium | Medium | Appeal process, regular audits |
| Users confused by new block messages | High | Low | Clear UX copy, support training |
| Legal challenge to historical blocks | Low | High | Legal review before launch |
| Booking quality tanks | Medium | High | Monitoring, rollback plan |

---

## 11. Critical Questions by Stakeholder

### For Product/Engineering (Ben Lee):
1. **What's the API contract for the new locking microservice?** Endpoints, request/response schemas.
2. **What's the data model?** Full schema for lock records including audit fields.
3. **How does this interact with AUTH-3195 MFA?** If someone is login-locked, does MFA matter?
4. **What's the blocking UX in booking flow?** At what step? What message?

### For T&S:
5. **What's your current daily review volume?** Will you need more staff?
6. **What reason taxonomy do you need?** Free text or predefined categories?
7. **What's the appeal process?** Who reviews contested blocks?
8. **How do you handle "drug seeking" flags?** HIPAA implications?

### For Legal/Compliance:
9. **Has legal reviewed the amnesty plan?** Any contractual issues?
10. **What audit trail is required?** Retention period?
11. **Can we store "drug seeking" as a block reason?** PHI considerations?

### For Booking Team:
12. **Where in the booking flow should blocks surface?** Start, slot selection, confirmation?
13. **Can you commit to implementing auto-lock logic later this year?**
14. **What booking quality metrics should we monitor post-amnesty?**

### For QA/Testing:
15. **How do we test blocking in E2E?** Need test accounts that can be locked/unlocked.
16. **How do we verify amnesty worked?** Previously locked test accounts should book.
17. **How do we test Retool workflows?** Staging environment?

---

## 12. Recommendations

1. **Define success metrics before launch** - You can't optimize without measurement
2. **Build appeal process from day 1** - Users will contest blocks
3. **Create reason taxonomy** - Don't let T&S use free text; you'll never analyze it
4. **Audit CISTERN list** - Sample 100 users, verify they should be blocked
5. **Plan amnesty communication** - Users should know they can book again
6. **Add block expiration** - 17-year blocks are excessive; consider auto-expiry after N years
7. **Monitor re-block rate** - If >10% of amnestied users get re-blocked, amnesty was too broad
