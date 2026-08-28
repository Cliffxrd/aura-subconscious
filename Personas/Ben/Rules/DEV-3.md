---
name: DEV-3
description: Controlled Coroutine Lifecycle & Effect Boundary Mandate
type: rule
author: Ben
hooks:
  - lint
  - static-analysis
---
# DEV-3: Controlled Coroutine Lifecycle & Effect Boundary Mandate

**Description:** Spawning coroutines or side-effects inside composable functions outside of explicit Compose effect handlers is strictly prohibited.

**Enforcement Mechanism:** Static analysis linter rule banning `rememberCoroutineScope().launch` directly in composable render bodies. All side-effects must use `LaunchedEffect` or `DisposableEffect`. Flow collection must use `collectAsStateWithLifecycle()`. ViewModel background jobs must run under `supervisorScope` with `CoroutineExceptionHandler`.

## Verification Checklist:
- [ ] Are coroutines launched exclusively inside `LaunchedEffect` or controlled handlers?
- [ ] Is flow collection bound to lifecycle via `collectAsStateWithLifecycle()`?
- [ ] Are async coroutines protected by `supervisorScope` and exception handlers?
