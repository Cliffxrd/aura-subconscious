---
id: "MEM_002"
title: "Strict Unidirectional Data Flow (UDF) & Stateless Compose Previews"
classification: "Type.BestPractice"
timestamp: "2026-08-05T14:30:00"
sourceChat: "AG015"
access:
  - "All"
emotional_vector:
  hsl: [300, 90, 50]
indexing:
  topics:
    - "#Compose"
    - "#Android"
    - "#UI"
  keywords:
    - "UDF"
    - "Unidirectional Data Flow"
    - "Stateless Composable"
    - "PreviewParameter"
---

# Operational Summary
Enforcing strict Unidirectional Data Flow (UDF) in Jetpack Compose: prohibiting passing `ViewModel` instances into child presentation composables, hoisting all state downwards as immutable data classes and events upwards via lambda callbacks.

# Interaction Context & Behavioral Log
- **Goal**: Prevent UI coupling, enable instant Compose Previews without mock frameworks, and guarantee deterministic state transitions.
- **Pattern**:
  - `*Screen` (Stateful / ViewModel holder) -> passes state to `*Content` (Stateless UI).
  - `*Content` consumes `PreviewParameterProvider` for multi-theme and multi-device preview validation.

# Core Engineering Lessons & Mandates
1. Never pass `ViewModel` into child presentational composables.
2. Structure state models as immutable `data class` with `@Immutable` annotations where applicable.
3. Every screen must provide clean `@Preview` coverage for Light, Dark, and dynamic window size classes.
