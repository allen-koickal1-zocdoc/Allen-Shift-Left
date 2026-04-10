# Cluster 4: Profile Media Updates

**Tickets:** 1  
**Percentage:** 12.5%  
**Product Areas:** Provider-Profile-Page(Patient)

---

## Root Cause

Profile media (headshots) not updating due to CDN caching or image processing delays.

---

## Tickets

| Ticket | Summary | Product Area | Labels | Resolution |
|--------|---------|--------------|--------|------------|
| TRIAG-22800 | Headshot Issue | Provider-Profile-Page(Patient) | `Updation-Delay-Required-Action`, `issue-type-performance` | Closed |

---

## Symptoms

- Headshot updated in system
- User cleared cache/cookies
- Still seeing old image

---

## Technical Investigation Areas

1. **CDN caching** — What's the TTL on profile images?
2. **Image processing queue** — Is there a backlog?
3. **Cache busting** — Does image URL change on update?

---

## Recommendations

- Implement cache busting for profile images (versioned URLs)
- Reduce CDN TTL for profile media
- Add "force refresh" option for CX
