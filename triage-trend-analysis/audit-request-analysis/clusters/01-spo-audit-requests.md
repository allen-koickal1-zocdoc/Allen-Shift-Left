# Cluster 1: SPO (Sponsored Results) Audit Requests

**Tickets:** 9  
**Percentage:** 20%  
**Product Area:** SPO(Provider)

---

## Root Cause

Providers dispute SPO activation/changes and request logs to identify who enabled the feature. CX lacks visibility into change history, requiring QA triage to pull logs.

**Resolution Pattern:** Most resolved as "Working as Intended" — providers activated SPO themselves but forgot or didn't realize the implications.

---

## Tickets

| Ticket | Summary | Resolution |
|--------|---------|------------|
| TRIAG-22952 | SPO logs request - practice requests exact date/time SPO was activated and IP address | Working as Intended |
| TRIAG-22941 | Request for SPO activation logs - Provider claims she never activated this | Working as Intended |
| TRIAG-22797 | SPO booking when SPO was off - PR received SPO booking when she said SPO was off | Done |
| TRIAG-22784 | SPO activation dispute - practice denies enabling | Working as Intended |
| TRIAG-22599 | Unexpected SPO charges - request for activation history | Working as Intended |
| TRIAG-22587 | SPO charge dispute - when was this turned on | Done |
| TRIAG-22528 | Request for who enabled SPO and when | Working as Intended |
| TRIAG-22251 | SPO activation audit - provider says never enabled | Working as Intended |
| TRIAG-22165 | SPO logs needed - practice disputing charges | Done |

---

## Common Symptoms

- Provider denies enabling SPO
- Provider charged for SPO unexpectedly
- Request for activation logs/timestamps
- Request for IP address of user who made changes
- "I would never have turned this on"

---

## The Story

**Typical scenario:**

1. Provider receives unexpected SPO charges on their account
2. Provider calls CX: "I never turned on Sponsored Results! Someone else did this!"
3. CX has no visibility into SPO change history
4. CX files TRIAG ticket requesting activation logs
5. QA pulls logs from backend, finds:
   - Provider activated SPO themselves
   - Often 2-4 months ago
   - From their own IP address
   - Using their own login
6. Resolved as "Working as Intended"

**Why this happens:**
- SPO activation may happen during onboarding without full understanding
- Providers forget they enabled it
- Multiple users on practice account — one enables, another disputes
- No confirmation email sent when SPO is activated
- No activity log visible to provider

---

## Recommendations

### Short-term (Operational)
- Create CX runbook for SPO audit queries
- Provide CX read access to SPO activation logs
- Standard response template for WAI results

### Long-term (Product)
- Send email confirmation when SPO is activated
- Add "SPO History" section to practice dashboard
- Show who activated, when, from what IP
- Consider activation confirmation modal

---

## Related Product Areas

- SPO(Billing) — for charge disputes
- Practice-Settings-Page — where SPO is enabled
