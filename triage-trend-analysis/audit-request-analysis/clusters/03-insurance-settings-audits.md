# Cluster 3: Insurance Settings Audit Requests

**Tickets:** 8  
**Percentage:** 18%  
**Product Areas:** Insurance-Settings-Page, Provider-Insurance

---

## Root Cause

Providers receive bookings for insurances they claim not to accept, or dispute Out-of-Network (OON) settings. CX cannot see insurance change history to verify who made changes.

**Resolution Pattern:** Mix of "Working as Intended" (provider changed settings themselves) and "Done" (logs provided showing legitimate configuration at booking time).

---

## Tickets

| Ticket | Summary | Resolution |
|--------|---------|------------|
| TRIAG-22946 | Insurance settings log - request for log of changes to Accept OON setting | Done |
| TRIAG-22533 | Provider got booking for insurance he doesn't have listed | Working as Intended |
| TRIAG-22517 | Insurance change audit request | Done |
| TRIAG-22496 | Insurances Changes - Practice claiming unauthorized changes | Working as Intended |
| TRIAG-22276 | Insurance allegedly removed but booking still came | Working as Intended |
| TRIAG-22242 | OON setting changed without authorization | Done |
| TRIAG-22207 | Request for insurance change history | Done |
| TRIAG-22197 | Who added this insurance to my profile | Working as Intended |

---

## Common Symptoms

- Provider received booking for insurance they claim not to accept
- "Accept Out of Network" setting allegedly changed
- Request for insurance change logs
- Insurance plan "removed" but bookings continue
- "I never added that insurance"

---

## The Story

**Typical scenario:**

1. Provider gets booking with insurance they don't want to accept
2. Provider: "I don't take that insurance! Who added it?"
3. CX cannot see insurance change history
4. TRIAG ticket for audit
5. Investigation reveals:
   - Insurance was present at time of booking
   - OON setting was "Accept" when booking was made
   - Changes often made by practice admin, not the provider themselves
   - Or changes during bulk operations by PDO
6. Resolved accordingly

**Special cases:**
- **OON disputes** — particularly contentious because it affects whether provider sees OON patients
- **Insurance inheritance** — some insurances inherited at practice level
- **Timing issues** — insurance removed after booking but provider thinks it was before

---

## Recommendations

### Short-term (Operational)
- CX runbook for insurance change queries
- Clear documentation on OON logic
- Template for explaining insurance inheritance

### Long-term (Product)
- Insurance change history in dashboard
- Show "as of booking date" configuration for disputes
- Email notification when insurance settings change
- Distinguish practice-level vs provider-level insurance settings

---

## Technical Notes

Insurance configuration is complex:
1. **Provider-level** — specific to individual provider
2. **Practice-level** — applies to all providers at practice
3. **OON setting** — separate toggle from insurance list
4. **Insurance ID matching** — sometimes fuzzy matching causes unexpected accepts

Audit logs need to capture all these dimensions.
