---
name: DEV-2
description: Immutable UI State Class & Compose Stability Requirement
type: rule
author: Ben
hooks:
  - compile-metrics
---
# DEV-2: Immutable UI State Class & Compose Stability Requirement

**Description:** All UI state models passed into composable functions must be declared as explicit `@Immutable` or `@Stable` Kotlin data classes containing read-only properties (`val`) and persistent/immutable collections.

**Enforcement Mechanism:** Compose Compiler Metrics report check. All composable screens must pass Compose Compiler metrics reporting (`skippable = true`) during release build compilation.

## Verification Checklist:
- [ ] Are all UI state models annotated with `@Immutable` or `@Stable`?
- [ ] Are collections represented as read-only or ImmutableList primitives?
- [ ] Does Compose Compiler report confirm `skippable = true` for all UI composables?
