---
name: ARCH-2
description: Mandatory State Hoisting Boundary & Single Screen ViewModel Rule
type: rule
author: Mike
hooks:
  - pre-commit
  - pr-review
---
# ARCH-2: Mandatory State Hoisting Boundary & Single Screen ViewModel Rule

**Description:** ViewModel instantiation and state collection are strictly limited to the top-level Screen Container (*ScreenRoute). Screen routes collect state using `collectAsStateWithLifecycle()` and pass immutable snapshots down the tree.

**Enforcement Mechanism:** Code review gate verification. Exactly one ViewModel declaration is permitted per top-level navigation destination. Sub-composables attempting to acquire ViewModels via `hiltViewModel()` or `koinViewModel()` will trigger PR rejection.

## Verification Checklist:
- [ ] Is ViewModel collection restricted to *ScreenRoute entry points?
- [ ] Is state collected using `collectAsStateWithLifecycle()`?
- [ ] Do sub-composables receive read-only state objects without instantiating ViewModels?
