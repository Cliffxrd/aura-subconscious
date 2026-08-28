---
name: QA-2
description: Mandatory Roborazzi/Paparazzi JVM Screenshot Test Pipeline
type: rule
author: Miranda
hooks:
  - ci-visual-regression
---
# QA-2: Mandatory Roborazzi/Paparazzi JVM Screenshot Test Pipeline

**Description:** Every single @Composable UI component created or modified in NetworkPulse must be accompanied by co-located JVM screenshot tests using Roborazzi/Paparazzi.

**Enforcement Mechanism:** CI visual regression gate. Screenshots are captured for all UI state permutations (Default, Loading, Success, Error, Disabled, custom states) and compared against golden baselines in `.github/snapshots/`. Any pixel delta exceeding 0.05% fails the build.

## Verification Checklist:
- [ ] Are Roborazzi/Paparazzi tests co-located with every UI composable?
- [ ] Are golden screenshot baselines committed in `.github/snapshots/`?
- [ ] Does CI screenshot diffing pass with < 0.05% perceptual pixel variance?
