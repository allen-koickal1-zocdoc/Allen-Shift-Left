# Cluster 4: Calendar/Availability Audit Requests

**Tickets:** 7  
**Percentage:** 16%  
**Product Areas:** Manual-Availability, Integrated-Availability, Calendar, Appointment-Experience(Provider)

---

## Root Cause

Providers claim OOO blocks, busy blocks, or availability were added/removed without their knowledge. Bookings occur during times providers thought were blocked. CX cannot see calendar change history.

**Resolution Pattern:** Mix of outcomes — some "Working as Intended" (provider forgot they removed block), some reveal legitimate sync issues with integrated calendars.

---

## Tickets

| Ticket | Summary | Resolution |
|--------|---------|------------|
| TRIAG-22987 | Incorrect Appointment Time Slots Created - manual calendar showed slots they didn't add | Working as Intended |
| TRIAG-22850 | OOO Blocked Removed - practice asking when and by whom | Done |
| TRIAG-22778 | Availability created without authorization | Working as Intended |
| TRIAG-22643 | Calendar change audit - who removed the block | Done |
| TRIAG-22443 | busy blocks added, poc unsure by who | Done |
| TRIAG-22416 | Booking during blocked time | Working as Intended |
| TRIAG-22183 | OOO block disappeared mysteriously | Done |

---

## Common Symptoms

- OOO block removed "without authorization"
- Busy blocks added without provider knowledge
- Availability/time slots created unexpectedly
- Booking during time provider thought was blocked
- "My calendar changed and I didn't touch it"

---

## The Story

**Typical scenario:**

1. Provider returns from vacation to find they had bookings
2. Provider: "I had OOO blocked! Who removed it?"
3. Or: "Busy blocks appeared on my calendar that I didn't add"
4. CX has no visibility into calendar change history
5. TRIAG ticket filed
6. Investigation reveals:
   - Another practice user edited the calendar
   - EHR sync overwrote manual changes
   - OOO block had an end date that passed
   - Provider removed block themselves while on mobile

**Calendar-specific complexities:**
- **Manual vs Integrated** — different rules for each
- **EHR sync** — can overwrite manual changes
- **Multi-user practices** — front desk often manages calendars
- **Mobile vs desktop** — accidental changes on mobile app

---

## Recommendations

### Short-term (Operational)
- CX runbook for calendar change queries
- Document sync behavior for integrated calendars
- Template explaining common scenarios

### Long-term (Product)
- Calendar change history with user attribution
- Show who made each change, from what device
- Warning when EHR sync might overwrite manual changes
- Confirmation before removing OOO blocks

---

## Technical Notes

Calendar changes can come from:
1. **Provider dashboard** — manual changes
2. **Mobile app** — touch-based changes (more accidental)
3. **EHR sync** — automated from integrated calendar
4. **Practice admin** — on behalf of provider
5. **CX/PDO** — support-initiated changes

Each source should be logged distinctly.
