---
name: UI-4
description: Mandatory Multi-Device & Motion Verification Guardrail
type: rule
author: Diana
hooks:
  - pre-qa-check
---
# UI-4: Mandatory Multi-Device & Motion Verification Guardrail

**Description:** No UI feature or layout change may be certified as ready for testing without explicit multi-device layout validation and motion specification audits.

**Enforcement Mechanism:** Pre-QA check. Layouts must be verified across 3 Window Size Classes. Any dynamic state change involving element reordering (chip lane movements) or visibility toggling must include explicit Compose animation primitives (`AnimatedVisibility`, `animateItemPlacement()`, `transitionSpec`).

## Verification Checklist:
- [ ] Have layouts been visually inspected across Compact, Medium, and Expanded window widths?
- [ ] Are chip lane enabling/disabling transitions animated via `animateItemPlacement()`?
- [ ] Are motion specs verified for 60fps fluidity without visual pop or layout jank?
