# Cluster 6: Working Hours Change Disputes

**Tickets:** 2  
**Percentage:** 4%  
**Product Area:** Working-Hours

---

## Root Cause

Provider working hours changed unexpectedly, leading to bookings during unavailable times. No audit trail visible to CX.

---

## Tickets

| Ticket | Summary | Resolution |
|--------|---------|------------|
| TRIAG-22481 | PR removed WH but times still booked - stated she removed all WH but appointments were still booked | Working as Intended |
| TRIAG-22412 | Provider Working Hours Incorrect - unexplained schedule changes causing major scheduling disruption | Done |

---

## Common Symptoms

- Working hours changed without authorization
- Bookings during times working hours were removed
- "I removed my hours but still got bookings"

---

## The Story

**Typical scenario:**

1. Provider removes working hours for certain days
2. Still receives bookings during those times
3. Provider: "I removed all my hours but appointments were still booked!"
4. Investigation reveals:
   - Bookings were made before hours were removed
   - Or working hours removal didn't sync immediately
   - Or EHR sync re-added working hours

---

## Recommendations

- Include in CX audit dashboard
- Document sync behavior for working hours
- Clear messaging on when hour changes take effect
