---
name: ARCH-3
description: Enforced @PreviewParameterProvider Standard for All UI Components
type: rule
author: Mike
hooks:
  - pre-commit
  - ci-lint
---
# ARCH-3: Enforced @PreviewParameterProvider Standard for All UI Components

**Description:** Every presentation Composable function MUST be accompanied by an Android Studio @Preview function backed by a dedicated `@PreviewParameterProvider`. Nullable ViewModel hacks, dummy ViewModel subclasses, or inline layout mocks are forbidden.

**Enforcement Mechanism:** Pre-commit git hooks and CI linter scripts verify that every @Composable file contains a corresponding PreviewParameterProvider supplying at least 4 canonical states (Default, Loading, EmptyState, ErrorState).

## Verification Checklist:
- [ ] Does a dedicated `PreviewParameterProvider<T>` exist for the component?
- [ ] Are Default, Loading, EmptyState, and ErrorState variants supplied?
- [ ] Are previews free of nullable ViewModel parameters and inline mock layouts?
