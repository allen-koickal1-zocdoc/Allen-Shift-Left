# Cluster 7: Google/Partner Settings Audit Requests

**Tickets:** 2  
**Percentage:** 4%  
**Product Areas:** Google-Reserve, Practice-Settings-Page

---

## Root Cause

Providers claim "Bookings from Google and others" setting keeps reverting to enabled, or was changed without their authorization.

---

## Tickets

| Ticket | Summary | Resolution |
|--------|---------|------------|
| TRIAG-22966 | Google Business Profile - POC turned off Bookings from Google multiple times but it keeps turning back on | Incomplete |
| TRIAG-22803 | PR requesting to see who changed Bookings from Google and others practice-level setting | Done |

---

## Common Symptoms

- Google booking setting keeps reverting to enabled
- Provider claims never enabled Google bookings
- "I keep turning this off but it comes back"

---

## The Story

**Typical scenario:**

1. Provider turns off "Bookings from Google and others"
2. Setting appears to revert to enabled later
3. Provider frustrated: "I've turned this off multiple times!"
4. Investigation needed to determine:
   - Is this a bug (setting not persisting)?
   - Is another user re-enabling?
   - Is there a sync issue?

**Note:** TRIAG-22966 marked as "Incomplete" suggests this may be a real technical issue, not just user confusion.

---

## Recommendations

### Short-term
- Investigate TRIAG-22966 for potential bug
- CX runbook for Google settings queries

### Long-term
- Ensure Google settings persist properly
- Add change history for this setting
- Consider confirmation on re-enable
