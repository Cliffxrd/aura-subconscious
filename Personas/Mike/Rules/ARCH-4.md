---
name: ARCH-4
description: Multi-Pane & Adaptive Dual-State Synchronization Contract
type: rule
author: Mike
hooks:
  - ui-test
  - pre-commit
---
# ARCH-4: Multi-Pane & Adaptive Dual-State Synchronization Contract

**Description:** For adaptive multi-pane viewports (e.g., List-Detail on landscape tablets or desktop windows), state synchronization between panes must be governed by a single unified higher-level UI State Holder class (`ListDetailUiState`) hoisted at the Screen Route container.

**Enforcement Mechanism:** Automated Compose UI multi-pane tests verify zero state drift during simulated item edits, deletions, and viewport orientation flips across compact, medium, and expanded window size classes.

## Verification Checklist:
- [ ] Is list selection and detail content state unified in a single atomic data class?
- [ ] Are detail pane state updates driven strictly by root ViewModel state emissions?
- [ ] Do landscape tablet UI tests pass without state mismatch or detail pane freezing?
