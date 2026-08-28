---
id: "MEM_004"
title: "Roborazzi JVM Snapshot Testing & Cross-Platform UI Verification"
classification: "Type.BestPractice"
timestamp: "2026-08-12T16:45:00"
sourceChat: "AG088"
access:
  - "All"
emotional_vector:
  hsl: [120, 85, 50]
indexing:
  topics:
    - "#Compose"
    - "#Testing"
    - "#Roborazzi"
  keywords:
    - "Roborazzi"
    - "JVM Screenshot Test"
    - "Robolectric"
    - "Pixel Parity"
---

# Operational Summary
Fast, deterministic JVM-based screenshot regression testing for Jetpack Compose using Roborazzi and Robolectric, eliminating the need for slow Android emulator boots during PR verification.

# Interaction Context & Behavioral Log
- **Goal**: Automate pixel-parity UI validation across Light/Dark themes and multiple screen densities directly inside Gradle CI.
- **Workflow**:
  - Run `./gradlew verifyRoborazziDebug` on pull requests.
  - Run `./gradlew recordRoborazziDebug` to update baseline screenshots upon approved UI changes.

# Core Engineering Lessons & Mandates
1. Keep screenshot test suites fast and hermetic by running on JVM via Robolectric native graphics.
2. Store verified screenshot baselines under source control with Git LFS.
3. Automatically fail builds if visual diff thresholds exceed 0.5%.
