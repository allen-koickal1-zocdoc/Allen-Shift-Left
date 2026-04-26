# Frontend — Pterodactyl-Owned UI (CORRECTED)

Repo: [Zocdoc/provider-fe-monorepo](https://github.com/Zocdoc/provider-fe-monorepo/tree/37d7eff62d9096c1b59ca494697b3ac5068a3234)
SHA: `37d7eff62d9096c1b59ca494697b3ac5068a3234`

## ⚠️ Correction notice (2026-04-27)

The original v2 frontend report claimed **0 frontend unit tests** for the Users Page. **That was wrong.** It was caused by a grep pattern mismatch — the monorepo uses `*-tests.tsx` naming (hyphen, not dot), so `find -name "*.test.tsx"` returned nothing. It also incorrectly excluded in-app Cypress tests as "out of scope" — but those tests are owned by the same team and exercise the same UI.

This file replaces that incorrect report.

## Pterodactyl-owned UI per CODEOWNERS

Authoritative ownership lives in [.github/CODEOWNERS](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/.github/CODEOWNERS):

```
/apps/settings/src/pages/settingsPages/practiceSettings/createProviderOrStaffPage/   @Zocdoc/user-permissions
/apps/settings/src/pages/settingsPages/practiceUsersPage/                            @Zocdoc/user-permissions
apps/provider-home-webapp/src/pages/signUpPortal/                                    @Zocdoc/user-permissions
```

Three owned UI areas, in two different webapps.

## Verified test inventory

### 1. Users Page — `apps/settings/src/pages/settingsPages/practiceUsersPage/`

| Layer | File | Tests | Link |
|-------|------|------:|------|
| Jest unit | `__tests__/PracticeUsersPageViewV2-tests.tsx` | **2** | [link](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/src/pages/settingsPages/practiceUsersPage/__tests__/PracticeUsersPageViewV2-tests.tsx) |
| Jest unit | `hooks/__tests__/useSelfSignUpData-tests.ts` | **3** | [link](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/src/pages/settingsPages/practiceUsersPage/hooks/__tests__/useSelfSignUpData-tests.ts) |
| In-app Cypress E2E | `apps/settings/cypress/e2e/PracticeUsersPage/practice-users-page-v2-tests.ts` | **35** | [link](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/cypress/e2e/PracticeUsersPage/practice-users-page-v2-tests.ts) |
| In-app Cypress E2E | `apps/settings/cypress/e2e/PracticeUsersPage/users-details-page-v2-tests.ts` | **33** | [link](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/cypress/e2e/PracticeUsersPage/users-details-page-v2-tests.ts) |
| Storybook + Chromatic | `apps/settings/src/pages/settingsPages/__stories__/PracticeUsersPageV2-stories.tsx` | 1 story file | [link](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/src/pages/settingsPages/__stories__/PracticeUsersPageV2-stories.tsx) |
| Storybook + Chromatic | `apps/settings/src/pages/settingsPages/__stories__/PracticeUsersPageDialogsV2-stories.tsx` | 1 story file | [link](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/src/pages/settingsPages/__stories__/PracticeUsersPageDialogsV2-stories.tsx) |

**Subtotal:** 5 unit tests, 68 in-app Cypress, 2 Chromatic stories.

### 2. Create Provider/Staff — `apps/settings/src/pages/settingsPages/practiceSettings/createProviderOrStaffPage/`

| Layer | File | Tests |
|-------|------|------:|
| Jest unit | (none — no `__tests__` dir) | **0** |
| In-app Cypress E2E | (none located under PracticeUsersPage scope; if any exist they live under `apps/settings/cypress/e2e/SettingsPages/` and are not directly named) | unverified |
| Storybook + Chromatic | [`CreateUserViewV2-stories.tsx`](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/src/pages/settingsPages/practiceSettings/createProviderOrStaffPage/__stories__/CreateUserViewV2-stories.tsx) | 1 story |
| Storybook + Chromatic | [`PracticeSelectionSection-stories.tsx`](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/src/pages/settingsPages/practiceSettings/createProviderOrStaffPage/__stories__/PracticeSelectionSection-stories.tsx) | 1 story |

**Subtotal:** 0 unit tests, 2 Chromatic stories.

### 3. Provider Sign-Up Portal — `apps/provider-home-webapp/src/pages/signUpPortal/`

| Layer | File | Tests | Link |
|-------|------|------:|------|
| Jest unit | (none) | **0** | — |
| In-app Cypress E2E | `apps/provider-home-webapp/cypress/e2e/signUpPortal/sign-up-portal-tests.ts` | **55** | [link](https://github.com/Zocdoc/provider-fe-monorepo/blob/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/provider-home-webapp/cypress/e2e/signUpPortal/sign-up-portal-tests.ts) |
| Storybook + Chromatic | 9 story files under `__stories__/` | 9 story files | [`signUpPortal/`](https://github.com/Zocdoc/provider-fe-monorepo/tree/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/provider-home-webapp/src/pages/signUpPortal) |

**Subtotal:** 0 unit tests, 55 in-app Cypress, 9 Chromatic stories.

## Roll-up across the 3 Pterodactyl-owned UI areas

| Layer | Tests/Stories |
|-------|--------------:|
| **Jest unit tests** | **5** (was claimed 0) |
| **In-app Cypress E2E** | **123** (was claimed 0 / out of scope) |
| **Storybook stories under Chromatic visual regression** | **13** files |
| **External Cypress E2E** (this sandbox repo, `cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/`) | 72 |

**Total Pterodactyl frontend test surface: 200 tests + 13 visual stories** — not zero.

## Real gaps (still meaningful)

Even with the corrections, the picture is thin in places:

| Gap | Detail |
|-----|--------|
| `practiceUsersPageV2` container/view has very shallow unit coverage | 2 tests for `PracticeUsersPageViewV2-tests.tsx` despite `PracticeUsersPageContainerV2.tsx`, `UserDetailContainerV2.tsx`, `UserDetailViewV2.tsx`, `ConfirmOrgLevelUserModal.tsx` all being non-trivial. |
| `createProviderOrStaffPage` has no unit tests at all | Only Storybook stories. Critical "create staff/user" flow has zero Jest coverage. [Source dir](https://github.com/Zocdoc/provider-fe-monorepo/tree/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/src/pages/settingsPages/practiceSettings/createProviderOrStaffPage). |
| `signUpPortal` has no unit tests | 0 Jest tests for the entire sign-up portal flow. All coverage is via in-app Cypress (55 tests) and Chromatic stories. |
| Hook unit coverage is sparse | Only `useSelfSignUpData` has tests. `useCurrentUserRoles`, `useOrganizationUserData`, and others are untested. [Hooks dir](https://github.com/Zocdoc/provider-fe-monorepo/tree/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/src/pages/settingsPages/practiceUsersPage/hooks). |
| No Datadog Synthetic for these UIs as code | `apps/settings/datadog/` only contains a `VaccineHub` legacy json file. |

## Methodology fix for v3

The grep that produced the wrong "0 unit tests" answer was:

```bash
find apps/settings -type f \( -name "*.test.tsx" -o -name "*.test.ts" \
                            -o -name "*.spec.tsx" -o -name "*.spec.ts" \)
```

The correct grep for this monorepo is:

```bash
find apps/settings apps/provider-home-webapp -type f \
  \( -name "*-tests.tsx" -o -name "*-tests.ts" \
     -o -name "*.test.tsx" -o -name "*.test.ts" \
     -o -name "*.spec.tsx" -o -name "*.spec.ts" \) \
  -not -path "*/node_modules/*"
```

In-app Cypress test files match `cypress/e2e/**/*-tests.ts`, NOT `*.spec.js`. Cypress in this sandbox repo (a separate repo) uses `*.spec.js`.

---

*Generated 2026-04-27. Supersedes the original v2 frontend-users-page.md from earlier the same day.*
