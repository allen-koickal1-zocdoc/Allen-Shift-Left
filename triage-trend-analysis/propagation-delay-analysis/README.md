# Propagation Delay Tickets Analysis

**Tickets Analyzed:** 8  
**Common Label:** `Updation-Delay-Required-Action` (100%)  
**Report Generated:** April 10, 2026

---

## Overview

This set of tickets represents a **different root cause category** from audit requests. These are **data propagation/sync issues** where updates in one system are not reflecting in another in a timely manner.

**Key Insight:** All 8 tickets share the `Updation-Delay-Required-Action` label, indicating a pattern of sync/propagation delays across systems.

---

## Ticket Details

### TRIAG-22938
| Field | Value |
|-------|-------|
| **Summary** | Incorrect VR showing up on PFS |
| **Product Area** | VR-Management |
| **Labels** | `Updation-Delay-Required-Action`, `issue-type-functional`, `triage-issue` |
| **Status/Resolution** | Closed / Fixed |
| **Description** | Provider profile showing "Allergy Shots" under popular VRs but this VR is not mapped to their profile. Request to remove unmapped VR from display. |
| **Cluster** | VR Propagation |

---

### TRIAG-22433
| Field | Value |
|-------|-------|
| **Summary** | The provider updated her VRs and they are not updating on pt side |
| **Product Area** | VR-Management |
| **Labels** | `Updation-Delay-Required-Action`, `issue-type-functional`, `triage-issue` |
| **Status/Resolution** | Closed / Closed |
| **Description** | Provider updated VRs to be limited, but patient search still shows her available for all visit reasons after 1+ hour. VR changes not propagating to patient-facing side. |
| **Cluster** | VR Propagation |

---

### TRIAG-22800
| Field | Value |
|-------|-------|
| **Summary** | Headshot Issue |
| **Product Area** | Provider-Profile-Page(Patient) |
| **Labels** | `Updation-Delay-Required-Action`, `issue-type-performance`, `triage-issue` |
| **Status/Resolution** | Closed / Closed |
| **Description** | POC unable to see updated headshot for provider. Image updated in system but not displaying for user despite cache/cookies cleared. |
| **Cluster** | Profile Media Updates |

---

### TRIAG-22596
| Field | Value |
|-------|-------|
| **Summary** | FAQ's |
| **Product Area** | Provider-Profile-Page(Patient) |
| **Labels** | `Updation-Delay-Required-Action`, `issue-type-data`, `triage-issue` |
| **Status/Resolution** | Closed / Fixed |
| **Description** | Provider FAQ still showing VRs (Psychotherapy Intake/Initial Visit, Weight Loss Consultation) that were removed. VR removal not reflected in FAQ section. |
| **Cluster** | VR Propagation |

---

### TRIAG-22869
| Field | Value |
|-------|-------|
| **Summary** | Marketplace Availability Bug |
| **Product Area** | Availability |
| **Labels** | `Required-operational-fix`, `Updation-Delay-Required-Action`, `issue-type-functional`, `triage-issue` |
| **Status/Resolution** | Closed / Closed |
| **Description** | Provider has CI complete, pulling availability, but Marketplace SKU not activated. Availability flashing on PFP. Provider not showing up on Marketplace despite expected active status. |
| **Cluster** | Availability Propagation |

---

### INTPLAT-3136
| Field | Value |
|-------|-------|
| **Summary** | DSP status showing inactive for active MD Mardiney opp |
| **Product Area** | Availability-Onboarding-Flow |
| **Labels** | `Updation-Delay-Required-Action`, `issue-type-functional`, `triage-issue` |
| **Status/Resolution** | Closed / Done |
| **Description** | Pulse shows professional as Active with two providers, but Salesforce DSP/professional status component shows Inactive. Provider confirmed live but SF status not updating. |
| **Cluster** | Salesforce Sync |

---

### TRIAG-22511
| Field | Value |
|-------|-------|
| **Summary** | Delay in Salesforce Case Creation – Parris and Associates |
| **Product Area** | Salesforce |
| **Labels** | `Redirected`, `Updation-Delay-Required-Action`, `Working-as-Intended`, `triage-issue` |
| **Status/Resolution** | Closed / Closed |
| **Description** | Three-day delay in Salesforce case creation for 3 providers submitted on same date. Cases eventually created manually by Systems team. |
| **Cluster** | Salesforce Sync |

---

### TRIAG-22160
| Field | Value |
|-------|-------|
| **Summary** | DEC invoice not able to load and DEC Appointment Report not loading |
| **Product Area** | Appointment-Report, Billing |
| **Labels** | `Updation-Delay-Required-Action`, `issue-type-functional`, `triage-issue` |
| **Status/Resolution** | Closed / Done |
| **Description** | December invoice grayed out/unloadable, DEC Appointment Report not loading since Dec 26th. Cannot view cancelled appointments or charges. |
| **Cluster** | Billing/Reports Loading |

---

## Cluster Summary

| Cluster | Count | Tickets | Product Areas |
|---------|-------|---------|---------------|
| **VR Propagation** | 3 | TRIAG-22938, TRIAG-22433, TRIAG-22596 | VR-Management, Provider-Profile-Page(Patient) |
| **Salesforce Sync** | 2 | INTPLAT-3136, TRIAG-22511 | Availability-Onboarding-Flow, Salesforce |
| **Availability Propagation** | 1 | TRIAG-22869 | Availability |
| **Profile Media Updates** | 1 | TRIAG-22800 | Provider-Profile-Page(Patient) |
| **Billing/Reports Loading** | 1 | TRIAG-22160 | Appointment-Report, Billing |

---

## Root Cause Analysis

### Pattern: Data Propagation Delays

Unlike audit requests (where providers dispute changes), these tickets are about **legitimate updates not propagating** across systems:

1. **VR updates** → Not reflecting on patient-facing pages/search
2. **Salesforce status** → Mismatch between Pulse and SF
3. **Profile media** → Images not updating due to caching
4. **Availability** → Marketplace activation status not syncing

### Technical Root Causes

| Issue Type | Likely Cause | Affected Systems |
|------------|--------------|------------------|
| VR not updating on patient side | Cache invalidation, search index delay | Search, PFP, FAQ |
| SF status mismatch | Sync job failure or delay | Pulse ↔ Salesforce |
| Headshot not updating | CDN caching, image processing queue | Media service, CDN |
| Reports not loading | Data aggregation failure | Billing, Reports |

---

## Recommendations

### Operational
1. **Create monitoring dashboard** for propagation delays by type
2. **Set SLAs** for data propagation (e.g., VR updates visible within 15 min)
3. **Runbook for CX** to manually trigger cache invalidation for urgent cases

### Product/Engineering
1. **VR propagation** — Investigate search index refresh timing
2. **Salesforce sync** — Add alerting on sync job failures
3. **Media caching** — Implement cache busting for profile updates
4. **Billing reports** — Add health check for report generation jobs

---

## Label Usage

All tickets consistently use:
- `Updation-Delay-Required-Action` — Indicates propagation delay
- `issue-type-functional` — Most common issue type
- `triage-issue` — Standard triage label

This labeling pattern is helpful for filtering and reporting.
