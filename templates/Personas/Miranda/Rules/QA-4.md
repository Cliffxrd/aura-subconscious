---
name: QA-4
description: Stateless Component & Uncoupled UI Verification Rule
type: rule
author: Miranda
hooks:
  - qa-linter
  - static-analysis
---
# QA-4: Stateless Component & Uncoupled UI Verification Rule

**Description:** Direct ViewModel coupling in Jetpack Compose UI composable signatures is strictly banned across all feature modules.

**Enforcement Mechanism:** QA linter / static analysis gate. Composables must accept immutable state data structures (`UiState`) and expose lambda callbacks (`(UiEvent) -> Unit`). Static analysis scans UI code; any `@Composable` receiving a ViewModel instance outside root navigation entry points triggers a build failure.

## Verification Checklist:
- [ ] Does QA static linter verify 0 ViewModel parameters in child composables?
- [ ] Are preview parameter providers validated against production state models?
- [ ] Can every UI component be instantiated headlessly in isolated JUnit tests?
