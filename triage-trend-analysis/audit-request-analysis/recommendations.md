# Improvement Recommendations

Based on the analysis of 45 audit request tickets, here are prioritized recommendations to reduce triage volume and improve CX efficiency.

---

## Operational Improvements (Quick Wins)

| # | Recommendation | Impact | Effort | Owner |
|---|----------------|--------|--------|-------|
| 1 | **Train CX on Pulse cache dump queries** for SPO, VR, Insurance settings | Could eliminate TRIAG tickets if CX can self-serve | Low | CX Training |
| 2 | **Create runbooks with exact queries** for each audit type | Faster triage resolution | Low | QA |
| 3 | **Add "Audit-Request" label** to TRIAG tickets to distinguish from actual bugs | Better reporting, prevents false bug counts | Low | QA |
| 4 | **Pre-written response templates** for WAI audit results | Faster resolution, consistent messaging | Low | CX |

### Runbook Examples

**SPO Activation Audit:**
```sql
-- Check SPO activation history
SELECT * FROM SPOActivationLog 
WHERE PracticeId = {practice_id}
ORDER BY ActivatedAt DESC;
```

**VR Change Audit:**
```sql
-- Check visit reason change history
SELECT * FROM VisitReasonChangeLog
WHERE ProviderId = {provider_id}
ORDER BY ChangedAt DESC;
```

---

## Product Improvements (Strategic)

| # | Recommendation | Impact | Affected Clusters | Effort |
|---|----------------|--------|-------------------|--------|
| 1 | **Build CX-facing audit log dashboard** | Eliminates 91% of these TRIAG tickets | All | High |
| 2 | **Add "Change History" tab to Practice Dashboard** visible to CX | Self-service for SPO, VR, Insurance, Spend | 1, 2, 3, 5 | Medium |
| 3 | **Implement change confirmations with email receipts** to providers | Providers can reference their own actions | All | Medium |
| 4 | **Add "View my activity log" for providers** in dashboard | Providers can self-verify before calling CX | All | Medium |
| 5 | **Calendar change attribution** showing who removed OOO/availability | Resolves calendar dispute tickets | 4 | Medium |
| 6 | **Google settings sticky/confirmation** - require explicit save | Fixes "keeps reverting" complaints | 7 | Low |

---

## Priority Matrix

```
                    HIGH IMPACT
                        |
   +--------------------+--------------------+
   |                    |                    |
   |  CX Audit          |  Provider          |
   |  Dashboard         |  Activity Log      |
   |  (91% reduction)   |                    |
LOW+--------------------+--------------------+HIGH
EFFORT                  |                    EFFORT
   |  CX Runbooks &     |  Email             |
   |  Templates         |  Confirmations     |
   |                    |                    |
   +--------------------+--------------------+
                        |
                    LOW IMPACT
```

---

## Detailed Product Recommendations

### 1. CX-Facing Audit Log Dashboard

**Problem:** CX agents cannot see when/who changed provider settings, forcing them to file TRIAG tickets for every dispute.

**Solution:** Single dashboard showing change history across all provider settings:
- SPO activation/deactivation
- Visit reason adds/removes
- Insurance settings changes
- Spend/budget changes
- Calendar/availability changes
- Google settings changes

**Fields to display:**
| Field | Description |
|-------|-------------|
| Timestamp | When the change was made |
| User | Who made the change (email/name) |
| IP Address | For additional verification |
| Setting | What was changed |
| Old Value | Previous value |
| New Value | New value |
| Source | Dashboard, API, Integration, etc. |

**ROI Calculation:**
- Current: ~40 audit tickets/month × 10 min triage = 6.7 hours/month
- With dashboard: ~0 tickets (CX self-serves)
- Annual savings: 80 hours QA time + faster CX resolution

---

### 2. Provider Activity Log (Provider-Facing)

**Problem:** Providers call CX claiming they didn't make changes because they have no way to review their own history.

**Solution:** "Activity Log" section in provider dashboard showing their own recent actions.

**Benefits:**
- Providers can self-verify before calling CX
- Reduces inbound CX volume
- Increases provider trust in the platform

---

### 3. Change Confirmation Emails

**Problem:** Providers forget they made changes, especially for consequential settings like SPO.

**Solution:** Send email confirmation when providers change:
- SPO on/off
- Spend cap changes
- Insurance settings
- Availability blocks

**Email template:**
```
Subject: Zocdoc Setting Changed: SPO Activated

Hi Dr. [Name],

You activated Sponsored Results (SPO) on [Date] at [Time].

If you didn't make this change, please contact support immediately.

- Zocdoc
```

---

## Implementation Phases

### Phase 1: Quick Wins (1-2 weeks)
- [ ] Create "Audit-Request" label in TRIAG
- [ ] Write CX runbooks for each audit type
- [ ] Create response templates for WAI results
- [ ] Train CX on Pulse queries (if feasible)

### Phase 2: CX Dashboard MVP (4-6 weeks)
- [ ] Design CX audit dashboard
- [ ] Implement SPO change history endpoint
- [ ] Implement VR change history endpoint
- [ ] Deploy to internal tools

### Phase 3: Full Rollout (8-12 weeks)
- [ ] Add remaining change types to dashboard
- [ ] Implement provider activity log
- [ ] Implement change confirmation emails
- [ ] Monitor ticket reduction

---

## Success Metrics

| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| Monthly audit TRIAG tickets | ~40 | <5 | 3 months post-launch |
| Time to resolve audit requests | ~10 min | <2 min | Immediate with dashboard |
| CX escalation rate for audits | 100% | <10% | 3 months post-launch |
| Provider satisfaction (audit disputes) | Unknown | Measure baseline | Ongoing |

---

## Stakeholders

| Area | Team | Contact |
|------|------|---------|
| SPO | SPO Team | TBD |
| Visit Reasons | VR Management | TBD |
| Insurance | Insurance Team | TBD |
| Calendar/Availability | Calendar Team | TBD |
| Spend Management | Billing | TBD |
| CX Tools | Internal Tools | TBD |
| CX Training | CX Ops | TBD |
