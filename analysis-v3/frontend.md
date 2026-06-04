# Frontend — Pterodactyl-Owned UI (provider-fe-monorepo)

**SHA:** `2e3f76bed111f8cc3aa568bc4c8dc197cbf274fc`
**Owner:** `@Zocdoc/user-permissions` per [`.github/CODEOWNERS`](https://github.com/Zocdoc/provider-fe-monorepo/blob/2e3f76bed111f8cc3aa568bc4c8dc197cbf274fc/.github/CODEOWNERS).

The recursive git tree was complete (`truncated: false`, 7,611 entries), so all three areas were covered in one fetch.

## Convention note

This monorepo names unit tests with a **hyphen** (`*-tests.tsx` / `*-tests.ts`) in the `settings` app, but `signUpPortal` (in `provider-home-webapp`) mixes in the dotted `*.test.tsx` / `*.test.ts` convention. **v2 counted only the hyphen form in `practiceUsersPage` and missed all 15 dotted unit tests in `signUpPortal`.** Both conventions are counted here.

## Owned areas (current — unchanged from v2)

1. `apps/settings/src/pages/settingsPages/practiceUsersPage/`
2. `apps/settings/src/pages/settingsPages/practiceSettings/createProviderOrStaffPage/`
3. `apps/provider-home-webapp/src/pages/signUpPortal/`

## Coverage

| Area | Jest/Vitest unit files | unit tests | in-app Cypress files | Cypress `it()` | stories |
|------|-----------------------:|-----------:|---------------------:|---------------:|--------:|
| practiceUsersPage | 2 | 5 | 2 | 68 | 0 |
| createProviderOrStaffPage | **0** | **0** | 1 | 26 | 2 |
| signUpPortal | 4 | 15 | 1 | 57 | 10 |
| **Total** | **6** | **20** | **4** | **151** | **12** |

## Files counted (auditable)

**Jest/Vitest unit (6 files, 20 tests):**
- `apps/settings/src/pages/settingsPages/practiceUsersPage/__tests__/PracticeUsersPageViewV2-tests.tsx` — 2
- `apps/settings/src/pages/settingsPages/practiceUsersPage/hooks/__tests__/useSelfSignUpData-tests.ts` — 3
- `apps/provider-home-webapp/src/pages/signUpPortal/__tests__/Context.test.tsx` — 3
- `apps/provider-home-webapp/src/pages/signUpPortal/components/__tests__/Footer.test.tsx` — 6
- `apps/provider-home-webapp/src/pages/signUpPortal/components/steps/__tests__/RepositionConfirmEmail.test.tsx` — 4
- `apps/provider-home-webapp/src/pages/signUpPortal/components/steps/__tests__/steps.test.ts` — 2

**In-app Cypress E2E (4 files, 151 tests):**
- `apps/settings/cypress/e2e/PracticeUsersPage/practice-users-page-v2-tests.ts` — 35
- `apps/settings/cypress/e2e/PracticeUsersPage/users-details-page-v2-tests.ts` — 33
- `apps/settings/cypress/e2e/PracticeSettingsPages/create-staff-page-v2-tests.ts` — 26
- `apps/provider-home-webapp/cypress/e2e/signUpPortal/sign-up-portal-tests.ts` — 57

**Storybook (12 files):** 2 under `createProviderOrStaffPage` (`CreateUserViewV2-stories`, `PracticeSelectionSection-stories`); 10 under `signUpPortal` (`HelpModal`, `BundleSelection`, `GoalTile`, `RecommendationStep`, `RecommendationTile`, `SkuModal`, `AccountSetup`, `ConfirmEmail`, `ProcessingLoader`, `RepositionConfirmEmail`).

## Gap

**`createProviderOrStaffPage` has 0 unit tests.** Its 7 source files (incl. `CreateUserViewV2.tsx`, `CreateUserSchema.tsx`, `RbacRoleSetupSection.tsx`, `getProfileCreationCommands.ts`) are exercised only by 26 in-app Cypress tests and 2 stories — no Jest/Vitest unit coverage.
