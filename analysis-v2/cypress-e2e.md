# Cypress E2E — Pterodactyl (Account-User-Setup)

Repo: [Zocdoc/sandbox](https://github.com/Zocdoc/sandbox)
SHA: `e6c476cd294f9d80cf1bead34fc16c786fedc7b3` (current SHA of `main` at audit time; the user's pin table did not include this repo)

## Method

`grep -cE "^\s*it\(" <spec>` for each `*.spec.js` under
`cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/{Flows,Pages}/`.

`it(` is counted whether wrapped in `describe(` or not. `it.only`, `it.skip`, etc. are not counted because they don't match the pattern.

## Headline

| | |
|--|--|
| Spec files | **9** |
| Total `it(` blocks | **72** |

## Per-file inventory

### Flows (61)
| Spec | `it(` count |
|------|-----:|
| [Flows/practice-settings-user-flow.spec.js](https://github.com/Zocdoc/sandbox/blob/e6c476cd294f9d80cf1bead34fc16c786fedc7b3/cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/Flows/practice-settings-user-flow.spec.js) | 24 |
| [Flows/appointment-mgmt-user-flow.spec.js](https://github.com/Zocdoc/sandbox/blob/e6c476cd294f9d80cf1bead34fc16c786fedc7b3/cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/Flows/appointment-mgmt-user-flow.spec.js) | 18 |
| [Flows/rbac-user-roles-flow.spec.js](https://github.com/Zocdoc/sandbox/blob/e6c476cd294f9d80cf1bead34fc16c786fedc7b3/cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/Flows/rbac-user-roles-flow.spec.js) | 10 |
| [Flows/spo-user-flow.spec.js](https://github.com/Zocdoc/sandbox/blob/e6c476cd294f9d80cf1bead34fc16c786fedc7b3/cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/Flows/spo-user-flow.spec.js) | 5 |
| [Flows/list-practice-flow.spec.js](https://github.com/Zocdoc/sandbox/blob/e6c476cd294f9d80cf1bead34fc16c786fedc7b3/cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/Flows/list-practice-flow.spec.js) | 2 |
| [Flows/billing-user-flow.spec.js](https://github.com/Zocdoc/sandbox/blob/e6c476cd294f9d80cf1bead34fc16c786fedc7b3/cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/Flows/billing-user-flow.spec.js) | 1 |
| [Flows/org-level-user-flow.spec.js](https://github.com/Zocdoc/sandbox/blob/e6c476cd294f9d80cf1bead34fc16c786fedc7b3/cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/Flows/org-level-user-flow.spec.js) | 1 |
| **Subtotal Flows** | **61** |

### Pages (11)
| Spec | `it(` count |
|------|-----:|
| [Pages/user-management-page.spec.js](https://github.com/Zocdoc/sandbox/blob/e6c476cd294f9d80cf1bead34fc16c786fedc7b3/cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/Pages/user-management-page.spec.js) | 9 |
| [Pages/legal-settings-page.spec.js](https://github.com/Zocdoc/sandbox/blob/e6c476cd294f9d80cf1bead34fc16c786fedc7b3/cypress/e2e/BU/Provider/Acquisition/Account-User-Setup/Pages/legal-settings-page.spec.js) | 2 |
| **Subtotal Pages** | **11** |

| **Total** | **72** |

## v1 corrections

| v1 said | v2 verified |
|---------|-------------|
| ~70 tests across 4 files | **72 tests across 9 files** (rbac/*.spec.js + provider-providerspage-regression.spec.js was the v1 search; the actual Pterodactyl-relevant Cypress lives under `Account-User-Setup/Flows` and `Account-User-Setup/Pages`) |
