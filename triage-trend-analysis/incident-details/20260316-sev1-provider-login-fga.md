# 20260316-[SEV1] Provider Login Not Working (FGA Misconfiguration)

**Incident:** [OUT-6517](https://zocdoc.atlassian.net/browse/OUT-6517)  
**Postmortem:** [Confluence](https://zocdoc.atlassian.net/wiki/spaces/INFRA/pages/2784657434)  
**Commander:** Elli Rappaport

## Timeline

| Milestone | Timestamp |
|-----------|-----------|
| Started | Mar 16, 2026 9:48 AM EDT |
| Detected | Mar 16, 2026 9:39 AM EDT |
| Mitigated | Mar 16, 2026 10:02 AM EDT |
| Resolved | Mar 16, 2026 10:24 AM EDT |
| **TTM** | 14 minutes |
| **TTR** | 36 minutes |

## Summary

Providers unable to log in due to FGA (Fine-Grained Authorization) errors resulting from a chain of PRs in `client-side-webapp-host`. The navbar component depended on FGA, so every provider-facing page (login, calendar, inbox, intake settings, etc.) failed to load.

## Root Cause

Chain of three PRs created the failure:

### PR #206: Initial FGA SDK Configuration
- Set up FGA SDK in `client-side-webapp-host`
- **But:** Repo was missing a spec config provider that other services have
- Without this, the service didn't get the default FGA configuration from `zd-dotnet` shared library

### PR #213: Enabled Audit Mode
- Audit mode appeared to pass
- **But:** Silently not catching the misconfiguration — audit exceptions weren't being surfaced properly
- Local dev and integration test environments had appsettings that masked the issue

### PR #226: Moved to Production Usage
- Exposed the broken configuration
- Caused 500 errors on provider navbar loads
- Since navbar is everywhere, this broke nearly every provider-facing page

## Business Impact

| Category | Impact |
|----------|--------|
| Appointments | No patient appointments disrupted — exclusively practice-side |
| Revenue | $0 — patient booking unaffected |
| UX | Providers unable to access any page with navbar for ~36 minutes |
| Dev-Cycles | ~10 people involved for ~30 minutes (~5 person-hours) |

## Detection

- **9:36 AM:** Auth synthetic fired (earliest automated signal)
- **9:40 AM:** PagerDuty alert for intake settings fired
- Manual reports came via #scheduling-alerts and #auth channels
- David Kaminsky identified it as SEV within 3 minutes of first report

## Recovery

1. Carlos Deleon re-ran previous known-good TeamCity build
2. Nico Rojo created revert PR #227
3. James Collins merged and redeployed the revert PR
4. Team self-organized and started reverting before commander was online

## What Went Smoothly

- Fast escalation (SEV identified within 3 minutes)
- Quick mitigation (14 minutes by reverting deploy)
- Carlos Deleon quickly found Honeycomb traces confirming FGA failure
- Team self-organized effectively

## What Created Friction

1. **Only 1 of 4 DataDog provider login synthetic tests fired** — monitoring gaps
2. **FGA SDK misconfiguration wasn't caught before merge/deploy** — audit mode gave false confidence
3. **Local dev and integration test environments masked the issue**
4. **Sentry was missing some errors** — CloudWatch had them but they weren't appearing in Sentry

## Key Lessons

### For Future Engineers

1. **Ensure exceptions are logged properly in audits** — in any audit mode, exceptions need to be surfaced visibly (e.g., in DataDog metrics), not silently swallowed
2. **Don't assume services are configured correctly** — when using shared libraries like `zd-dotnet` that depend on spec config provider, verify the configuration before enabling new features
3. **Other teams should verify their services have the spec config provider set up correctly**, especially older repos that may predate the current defaults

## Action Items

### Immediate Actions

| Action | Ticket | Status |
|--------|--------|--------|
| Fix CSWH FGA Connection — set up spec config provider, match local/integration env to prod, add audit mode metrics visibility in DataDog | [PTERODACTL-1749](https://zocdoc.atlassian.net/browse/PTERODACTL-1749) | **Closed** |

### Preventative Actions

| Action | Status |
|--------|--------|
| Investigate Sentry gap — CloudWatch errors not appearing in Sentry during audit mode | TBD (unassigned, tag SRE) |
| Verify spec config provider setup across older repos | TBD (All teams using zd-dotnet) |

## Fixes Applied

| Fix | PR | Status |
|-----|-----|--------|
| Revert PR | [PR #227](https://github.com/Zocdoc/client-side-webapp-host/pull/227) | Merged |
| Metrics fix | [zd-dotnet PR #1155](https://github.com/Zocdoc/zd-dotnet/pull/1155) | Merged |
| Config fix | [PR #234](https://github.com/Zocdoc/client-side-webapp-host/pull/234) | Merged |
| Config fix | [PR #229](https://github.com/Zocdoc/client-side-webapp-host/pull/229) | Merged |

## Related Triage Tickets

- TRIAG-22914: Provider Login Error Loop
- TRIAG-22913: Error message when logging into Zocdoc
- TRIAG-22190: Unable to verify phone number (2FA)
