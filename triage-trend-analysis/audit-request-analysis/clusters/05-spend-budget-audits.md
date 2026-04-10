# Cluster 5: Spend/Budget Management Audit Requests

**Tickets:** 5  
**Percentage:** 11%  
**Product Area:** Spend-Management

---

## Root Cause

Providers dispute spend caps, budget changes, or claim bookings came through when spend was turned off. CX cannot verify the timing of spend setting changes.

**Resolution Pattern:** Mix of "Working as Intended" (timing confusion) and some legitimate technical issues with budget tool.

---

## Tickets

| Ticket | Summary | Resolution |
|--------|---------|------------|
| TRIAG-22986 | Unexpected $50,000 spend cap on enterprise account | Done |
| TRIAG-22723 | Logs Of Provider Turning Off Spend - received appointment after | Working as Intended |
| TRIAG-22574 | Budget Tool - Confirmed budget saved as 50K but reverted back to 80K | Incomplete |
| TRIAG-22427 | Booking came through when spend was supposedly off | Working as Intended |
| TRIAG-22389 | Spend change history request | Done |

---

## Common Symptoms

- Unexpected spend cap on account
- Budget reverted to previous value
- Booking came through when spend was "off"
- "Who set this spend cap?"
- Budget tool showing wrong value

---

## The Story

**Typical scenario:**

1. Provider notices unexpected spend cap or booking
2. Provider: "I turned off spend yesterday but got a booking today!"
3. CX cannot see spend change history
4. TRIAG ticket filed
5. Investigation reveals:
   - Booking was made BEFORE spend was turned off
   - Or spend cap was set by practice admin
   - Or there's latency between setting change and effect
   - Occasionally: legitimate bug in budget tool

**Spend-specific nuances:**
- **Timing** — changes don't take effect immediately for in-flight bookings
- **Practice vs provider** — spend caps can be set at different levels
- **Budget reversion** — some reports of budgets reverting (potential bug)

---

## Recommendations

### Short-term (Operational)
- CX runbook for spend change queries
- Document spend change timing/latency
- Template explaining when bookings are "locked in"

### Long-term (Product)
- Spend change history dashboard
- Clear messaging on when changes take effect
- Investigate budget reversion reports (TRIAG-22574)
- Email notification when spend settings change

---

## Technical Notes

Spend management complexity:
1. **Effective timing** — when does a spend cap take effect?
2. **In-flight bookings** — bookings started before cap may complete after
3. **Practice vs provider caps** — hierarchy of limits
4. **Budget tool reliability** — investigate reversion reports
