---
name: UI-2
description: Mandatory @PreviewParameterProvider Suite Rule
type: rule
author: Diana
hooks:
  - static-analysis
---
# UI-2: Mandatory @PreviewParameterProvider Suite Rule

**Description:** Every stateful screen or component MUST be accompanied by a dedicated `PreviewParameterProvider<T>` implementation supplying at least 6 canonical UI state variations across multi-device preview annotations.

**Enforcement Mechanism:** Static analysis verification. Providers must supply: 1. Idle, 2. Loading, 3. Success/Populated, 4. EmptyState, 5. ErrorState, 6. EdgeCase/Overflow (max text lengths, extreme values). Annotations must cover Light/Dark mode, Compact Phone, Foldable, and Landscape Tablet (`@Preview(device = Devices.TABLET)`).

## Verification Checklist:
- [ ] Are all 6 canonical UI state variations defined in the parameter provider?
- [ ] Are `@Preview` annotations configured for Compact Phone, Foldable, and Tablet Landscape modes?
- [ ] Are edge-case long strings and latency spikes visually verified in previews?
