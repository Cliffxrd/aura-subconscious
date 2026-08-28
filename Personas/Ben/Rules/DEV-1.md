---
name: DEV-1
description: Strict Unidirectional Data Flow (UDF) & State Hoisting Rule
type: rule
author: Ben
hooks:
  - ci-gate
---
# DEV-1: Strict Unidirectional Data Flow (UDF) & State Hoisting Rule

**Description:** No composable function below the top-level Screen Composable may accept a ViewModel, Presenter, or state-holder instance as a parameter. State flows down via immutable parameters; events flow up via explicit event lambdas `(Event) -> Unit`.

**Enforcement Mechanism:** CI static analysis gate. Any PR containing ViewModel parameter propagation to child composables will be automatically flagged and rejected.

## Verification Checklist:
- [ ] Are child composables 100% free of ViewModel parameter declarations?
- [ ] Do child composables receive pure data inputs and emit lambda event callbacks?
- [ ] Is UDF strictly preserved across all component trees?
