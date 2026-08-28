---
name: DEV-4
description: Platform-Agnostic Cross-Platform Initialization Guard
type: rule
author: Ben
hooks:
  - build-check
---
# DEV-4: Platform-Agnostic Cross-Platform Initialization Guard

**Description:** All external SDK initializations (Firebase, Analytics, Hardware APIs) in Kotlin Multiplatform must use strict expect/actual platform guards with explicit configuration fallbacks and zero JVM auto-init assumptions.

**Enforcement Mechanism:** KMP Web WASM build check. On Web/WASM targets, platform initialization must explicitly pass Web configuration parameters (apiKey, projectId, appId) and bridge asynchronous JS promises using `awaitPromise()` inside `runCatching` blocks.

## Verification Checklist:
- [ ] Is Firebase initialization implemented via expect/actual modules with Web FirebaseOptions?
- [ ] Are Web JS Promises bridged via `awaitPromise()` inside `runCatching` blocks?
- [ ] Does the WASM build launch on networkpulse.web.app without runtime stack panics?
