---
id: "MEM_001"
title: "Kotlin Multiplatform Clean Architecture & Expect/Actual Bridges"
classification: "Type.ArchitecturalMilestone"
timestamp: "2026-08-01T12:00:00"
sourceChat: "AG001"
access:
  - "All"
emotional_vector:
  hsl: [180, 85, 50]
indexing:
  topics:
    - "#Kotlin"
    - "#KMP"
    - "#Architecture"
  keywords:
    - "expect/actual"
    - "Clean Architecture"
    - "commonMain"
    - "platform bridge"
---

# Operational Summary
Standard multi-module Kotlin Multiplatform (KMP) architecture enforcing clean separation of concerns, domain isolation in `commonMain`, and resilient `expect/actual` bridges for platform-specific capabilities (Android, iOS, WASM, Desktop).

# Interaction Context & Behavioral Log
- **Goal**: Establish deterministic dependency injection and platform bridges across shared Kotlin codebases.
- **Rules Enforced**:
  - Keep domain entities and business logic 100% pure Kotlin in `commonMain`.
  - Use `expect/actual` declarations exclusively for platform hardware/OS hooks (storage, audio, permissions).

# Core Engineering Lessons & Mandates
1. Never import Android SDK classes directly into `commonMain`.
2. Encapsulate third-party SDK differences behind interface adapters with deterministic test mocks.
3. Validate compilation across all declared targets before merging architectural refactors.

