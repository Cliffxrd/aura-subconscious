---
name: UI-3
description: Zero-Hex & Material Design 3 State Token Enforcement
type: rule
author: Diana
hooks:
  - lint
---
# UI-3: Zero-Hex & Material Design 3 State Token Enforcement

**Description:** No inline hex color literals (0xFF...) or hardcoded pixel/dp magic numbers are permitted in UI composables. All visual values must resolve through MaterialTheme tokens.

**Enforcement Mechanism:** Linter check rule (Detekt color literal rule). Interactive states (disabled, active, pressed) MUST consume official MD3 state tokens (e.g., `MaterialTheme.colorScheme.onSurface.copy(alpha = 0.38f)` for disabled containers). Semantic action colors (Stop button red) must be defined as theme tokens.

## Verification Checklist:
- [ ] Are all color values resolved through `MaterialTheme.colorScheme` (Zero raw hex literals)?
- [ ] Does disabled "LOG" chip use 38% MD3 alpha state layer tokens?
- [ ] Is Stop capture button red configured as a semantic theme token (`colorScheme.error`)?
