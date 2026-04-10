# Audit Request Analysis Report

**Analysis Period:** January - April 2026  
**Total Tickets Analyzed:** 45  
**Report Generated:** April 10, 2026

## Executive Summary

This analysis examined 45 triage tickets that represent **audit/log requests** — a distinct category from bug reports. These tickets occur when providers dispute changes to their accounts and CX needs to verify who made what change and when.

### Key Finding

**91% of these triage tickets (41/45) share a single meta-root-cause: CX lacks self-service access to audit logs.**

| Metric | Value |
|--------|-------|
| **Total Tickets** | 45 |
| **Distinct Clusters** | 7 |
| **Resolution: Working as Intended** | 22 (49%) |
| **Resolution: Done (logs provided)** | 17 (38%) |
| **True bugs** | 4 (9%) |

### The Real Story

These aren't bugs — they're **trust gaps**. The pattern:
1. Provider calls CX upset about unexpected charge/booking/setting
2. Provider claims "I never made that change!"
3. CX has no way to verify who made the change
4. CX files TRIAG ticket requesting audit logs
5. QA pulls logs, finds provider made the change themselves
6. Resolved as "Working as Intended"

---

## Root Cause Clusters

| Cluster | Count | % | Product Areas |
|---------|-------|---|---------------|
| [SPO Audit Requests](clusters/01-spo-audit-requests.md) | 9 | 20% | SPO(Provider) |
| [Visit Reason Audits](clusters/02-visit-reason-audits.md) | 9 | 20% | VR-Management |
| [Insurance Settings Audits](clusters/03-insurance-settings-audits.md) | 8 | 18% | Insurance-Settings-Page, Provider-Insurance |
| [Calendar/Availability Audits](clusters/04-calendar-availability-audits.md) | 7 | 16% | Manual-Availability, Calendar |
| [Spend/Budget Audits](clusters/05-spend-budget-audits.md) | 5 | 11% | Spend-Management |
| [Working Hours Disputes](clusters/06-working-hours-disputes.md) | 2 | 4% | Working-Hours |
| [Google Settings Audits](clusters/07-google-settings-audits.md) | 2 | 4% | Google-Reserve |
| [Unclustered](clusters/08-unclustered.md) | 4 | 9% | Various |

---

## Cluster Narratives

### 1. SPO (Sponsored Results) Audit Requests — 9 tickets

**The Story:** Provider calls upset about SPO charges. Claims "I never turned that on!" CX has no way to check, files TRIAG ticket. QA pulls logs, finds provider enabled SPO themselves 3 months ago. Resolved as WAI.

**Tickets:** TRIAG-22952, 22941, 22797, 22784, 22599, 22587, 22528, 22251, 22165

**Common Symptoms:**
- Provider denies enabling SPO
- Unexpected SPO charges
- Request for activation timestamps and IP addresses

---

### 2. Visit Reason (VR) Change Audits — 9 tickets

**The Story:** Provider gets booking for "ADHD evaluation" they say they don't do. Claims "I removed that VR!" or "VRs repopulated on their own." CX can't verify, files TRIAG. Logs show VR was correctly configured at booking time.

**Tickets:** TRIAG-22867, 22862, 22747, 22710, 22429, 22409, 22282, 22198, 22197

**Common Symptoms:**
- Bookings for VRs provider claims not to support
- VRs "repopulating on their own"
- Request for add/remove timestamps

---

### 3. Insurance Settings Audits — 8 tickets

**The Story:** Provider gets booking for insurance they don't accept. Claims "I never added that insurance!" or "Someone changed my OON setting." CX can't verify who made the change, files TRIAG.

**Tickets:** TRIAG-22946, 22533, 22517, 22496, 22276, 22242, 22207, 22197

**Common Symptoms:**
- Bookings for unaccepted insurances
- Accept OON setting "changed without authorization"
- Request for insurance change logs

---

### 4. Calendar/Availability Audits — 7 tickets

**The Story:** Provider's OOO block disappeared, booking came through during vacation. Claims "Someone removed my block!" Or mysterious busy blocks appeared. CX can't see calendar change history, files TRIAG.

**Tickets:** TRIAG-22987, 22850, 22778, 22643, 22443, 22416, 22183

**Common Symptoms:**
- OOO blocks removed "without authorization"
- Busy blocks added mysteriously
- Availability slots "created without authorization"

---

### 5. Spend/Budget Management Audits — 5 tickets

**The Story:** Provider says "I set my budget to $50K but it's showing $80K" or "I turned spend off but got a booking." CX can't see spend setting history, files TRIAG.

**Tickets:** TRIAG-22986, 22723, 22574, 22427, 22389

**Common Symptoms:**
- Unexpected spend caps
- Budget reverting to old values
- Bookings when spend was "off"

---

### 6. Working Hours Disputes — 2 tickets

**The Story:** Provider removed working hours for certain days but still got bookings. Claims "I removed all WH but appointments were still booked!"

**Tickets:** TRIAG-22481, 22412

---

### 7. Google/Partner Settings Audits — 2 tickets

**The Story:** Provider turns off "Bookings from Google and others" but it keeps reverting to enabled. Files complaint about unauthorized changes.

**Tickets:** TRIAG-22966, 22803

---

## Resolution Breakdown

| Resolution | Count | % | Meaning |
|------------|-------|---|---------|
| Working as Intended | 22 | 49% | Provider made the change themselves |
| Done | 17 | 38% | Logs provided, no further action |
| Closed | 3 | 7% | Closed without action |
| Incomplete | 2 | 4% | Missing information |
| Won't Do | 1 | 2% | Not actionable |

**Key Insight:** 87% resolved with no code changes required. These are operational overhead, not engineering work.

---

## Files in This Analysis

- `README.md` - This summary report
- `clusters/` - Detailed analysis per cluster
- `recommendations.md` - Operational and product improvement recommendations
- `tickets.json` - Structured ticket data
- `propagation-delay-tickets.md` - Separate category: data sync/propagation delays (8 tickets)

---

## Related Analyses

- [Outage-Related Triage Analysis](../README.md) - 32 tickets traced to production incidents
