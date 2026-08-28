---
name: UI-1
description: Strict No-Faked-Previews Policy
type: rule
author: Diana
hooks:
  - pr-review
---
# UI-1: Strict No-Faked-Previews Policy

**Description:** It is strictly forbidden to write a `@Preview` composable that manually reconstructs layout skeletons, hardcodes static mock composables inline, or duplicates production rendering logic.

**Enforcement Mechanism:** PR check rule. Every `@Preview` function MUST directly invoke the production top-level composable function using `@PreviewParameter` suppliers. PR approval will be denied for code introducing inline mock strings or layout duplicates inside previews.

## Verification Checklist:
- [ ] Do `@Preview` functions directly call production composables?
- [ ] Are preview data values supplied exclusively via `@PreviewParameter` providers?
- [ ] Are inline static mock strings ("0ms", hardcoded spacers) eliminated from preview files?
