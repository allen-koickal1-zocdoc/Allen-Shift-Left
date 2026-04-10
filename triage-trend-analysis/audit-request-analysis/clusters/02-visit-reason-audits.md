# Cluster 2: Visit Reason (VR) Change Audit Requests

**Tickets:** 9  
**Percentage:** 20%  
**Product Area:** VR-Management

---

## Root Cause

Providers receive bookings for visit reasons they claim not to support, and request logs to prove when VRs were added/removed. CX lacks visibility into VR change history.

**Resolution Pattern:** Most resolved as "Working as Intended" — VRs were correctly configured at the time of booking. Providers often forget they added VRs or don't realize how VR inheritance works.

---

## Tickets

| Ticket | Summary | Resolution |
|--------|---------|------------|
| TRIAG-22867 | Visit reason history needed - when added/removed + source of change | Done |
| TRIAG-22862 | Inaccurate Booking - Practice believes they removed ADHD VR and it repopulated | Working as Intended |
| TRIAG-22747 | VRs were removed from provider - Reports all VRs were removed | Done |
| TRIAG-22710 | VR audit - provider says VR was never added by them | Working as Intended |
| TRIAG-22429 | Booking for VR provider doesn't support | Working as Intended |
| TRIAG-22409 | VRs allegedly repopulated without action | Working as Intended |
| TRIAG-22282 | Visit reason change log request | Done |
| TRIAG-22198 | VR removed but bookings still coming | Working as Intended |
| TRIAG-22197 | Who added this visit reason to my profile | Done |

---

## Common Symptoms

- Provider received booking for VR they claim not to service
- Request for VR add/remove timestamps
- VRs "repopulated on their own"
- VRs allegedly removed but bookings still came
- "I never added that visit reason"

---

## The Story

**Typical scenario:**

1. Provider gets booking for "ADHD Evaluation" or similar specialized VR
2. Provider: "I don't do ADHD evals! I removed that visit reason!"
3. CX has no way to see VR change history
4. TRIAG ticket filed for audit
5. QA investigation reveals:
   - VR was present at time of booking
   - Provider may have removed it AFTER getting the booking
   - Or VR was inherited from specialty defaults
   - Or another practice user added the VR
6. Resolved as "Working as Intended"

**Common confusions:**
- VR inheritance from specialty → providers don't understand why VRs appear
- Timing confusion → VR removed after booking, not before
- Multi-user practices → one user adds, another disputes
- Batch operations → changes during onboarding forgotten

---

## Recommendations

### Short-term (Operational)
- CX runbook for VR change queries
- Document VR inheritance rules for CX
- Template explaining WAI scenarios

### Long-term (Product)
- VR change history visible in dashboard
- Distinguish inherited vs manually added VRs
- Email notification when VRs change
- Clear indication of when VR was present vs removed

---

## Technical Notes

VRs can come from multiple sources:
1. **Manual addition** — provider explicitly adds
2. **Specialty inheritance** — default VRs for specialty
3. **Practice-level** — applies to all providers at practice
4. **Bulk operations** — PDO/CX adding during onboarding

Audit logs should distinguish between these sources.
