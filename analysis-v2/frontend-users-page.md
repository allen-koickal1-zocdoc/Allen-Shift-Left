# Frontend — Pterodactyl Users Page

Repo: [Zocdoc/provider-fe-monorepo](https://github.com/Zocdoc/provider-fe-monorepo/tree/37d7eff62d9096c1b59ca494697b3ac5068a3234)
SHA: `37d7eff62d9096c1b59ca494697b3ac5068a3234`

## Verification

The Pterodactyl-owned Users Page lives at:
[apps/settings/src/pages/settingsPages/practiceUsersPage/](https://github.com/Zocdoc/provider-fe-monorepo/tree/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/src/pages/settingsPages/practiceUsersPage)

(There is also a v2 sibling at [`practiceUsersPage/practiceUsersPageV2`](https://github.com/Zocdoc/provider-fe-monorepo/tree/37d7eff62d9096c1b59ca494697b3ac5068a3234/apps/settings/src/pages/settingsPages/practiceUsersPage/practiceUsersPageV2).)

## Search

```
find provider-fe-monorepo/apps/settings -type f \
  \( -name "*.test.tsx" -o -name "*.test.ts" \
     -o -name "*.spec.tsx" -o -name "*.spec.ts" \)
```

Result: **0 files**.

## Conclusion

| | |
|--|--|
| Jest/Vitest unit tests in `apps/settings/` | **0** |
| Jest/Vitest unit tests in `practiceUsersPage/` | **0** |
| Jest/Vitest unit tests in `practiceUsersPageV2/` | **0** |

This confirms v1's claim verbatim. The correction relative to v1 is the **repo name**: v1 implied a "frontend-monorepo" repo, but the Users Page UI actually lives in `provider-fe-monorepo` under `apps/settings/`.

## Notes

- `apps/settings/cypress/e2e/PracticeUsersPage/` exists for E2E coverage but those are not unit tests and are out of scope for this report.
- Other apps in the monorepo (e.g. `apps/dashboard`, `apps/spo-webapp`) may have their own test suites; only `apps/settings/` was audited for Pterodactyl scope.
