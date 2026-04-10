# Cluster 2: Salesforce Sync Issues

**Tickets:** 2  
**Percentage:** 25%  
**Product Areas:** Availability-Onboarding-Flow, Salesforce

---

## Root Cause

Status and case sync between Pulse and Salesforce failing or experiencing significant delays.

---

## Tickets

| Ticket | Summary | Product Area | Labels | Resolution |
|--------|---------|--------------|--------|------------|
| INTPLAT-3136 | DSP status showing inactive for active provider | Availability-Onboarding-Flow | `Updation-Delay-Required-Action`, `issue-type-functional` | Done |
| TRIAG-22511 | Delay in Salesforce Case Creation | Salesforce | `Updation-Delay-Required-Action`, `Working-as-Intended` | Closed |

---

## Symptoms

- DSP/professional status mismatch between Pulse (Active) and Salesforce (Inactive)
- Multi-day delays in SF case creation
- Onboarding tasks stuck in pending state

---

## Technical Investigation Areas

1. **Sync job health** — Are sync jobs running successfully?
2. **Error handling** — What happens when sync fails?
3. **Retry logic** — Is there automatic retry for failed syncs?

---

## Recommendations

- Add alerting on SF sync job failures
- Dashboard showing Pulse ↔ SF sync status
- Implement sync health monitoring
