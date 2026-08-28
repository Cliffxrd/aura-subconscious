---
name: ARCH-1
description: Pure Composable Interface Mandate (Stateless Leaf Rule)
type: rule
author: Mike
hooks:
  - pre-commit
  - lint
---
# ARCH-1: Pure Composable Interface Mandate (Stateless Leaf Rule)

**Description:** No Composable function below top-level Screen Containers (*ScreenRoute / *ScreenContainer) may accept a ViewModel, NavController, CoroutineScope, or platform framework dependency as a parameter.

**Enforcement Mechanism:** ArchUnit static analysis rules and Detekt custom linter rules will check parameter types. Build compilation fails instantly if any Composable below a Screen container imports `androidx.lifecycle.ViewModel` or `androidx.navigation.NavController`.

## Verification Checklist:
- [ ] Are all child/leaf composable parameters read-only data classes or explicit state interfaces?
- [ ] Are user actions emitted strictly via `(UiEvent) -> Unit` lambda callbacks?
- [ ] Does ArchUnit linter pass with 0 ViewModel parameter violations?
