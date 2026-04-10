# Cluster 1: VR Propagation Delays

**Tickets:** 3  
**Percentage:** 37.5%  
**Product Areas:** VR-Management, Provider-Profile-Page(Patient)

---

## Root Cause

VR updates made by providers are not propagating to patient-facing pages, search results, or FAQ sections in a timely manner.

---

## Tickets

| Ticket | Summary | Product Area | Labels | Resolution |
|--------|---------|--------------|--------|------------|
| TRIAG-22938 | Incorrect VR showing up on PFS | VR-Management | `Updation-Delay-Required-Action`, `issue-type-functional` | Fixed |
| TRIAG-22433 | VRs not updating on patient side | VR-Management | `Updation-Delay-Required-Action`, `issue-type-functional` | Closed |
| TRIAG-22596 | FAQs still showing removed VRs | Provider-Profile-Page(Patient) | `Updation-Delay-Required-Action`, `issue-type-data` | Fixed |

---

## Symptoms

- VR changes not reflecting on patient search after 1+ hour
- Removed VRs still appearing in FAQ section
- Unmapped VRs showing on provider profile

---

## Technical Investigation Areas

1. **Search index refresh timing** — How often does search re-index VR data?
2. **FAQ generation** — Is FAQ cached separately from VR data?
3. **Cache invalidation** — Are all caches being invalidated on VR change?

---

## Recommendations

- Add monitoring for VR propagation latency
- Set SLA: VR changes visible within 15 minutes
- Implement cache busting on VR updates
