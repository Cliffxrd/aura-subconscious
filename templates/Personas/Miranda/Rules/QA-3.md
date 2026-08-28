---
name: QA-3
description: Automated ADB Real-Device Visual Inspection Harness
type: rule
author: Miranda
hooks:
  - post-build-adb
---
# QA-3: Automated ADB Real-Device Visual Inspection Harness

**Description:** QA maintains an automated ADB-driven test execution harness to validate real runtime behavior on physical/emulator target devices after APK compilation.

**Enforcement Mechanism:** Post-build ADB test suite. Harness executes `adb shell am start` for deep links (`networkpulse.web.app`), permissions (`ACCESS_NETWORK_STATE`), and launch assets (`ic_launcher_foreground.png`), grabbing screen bitmaps (`adb exec-out screencap`) and accessibility trees for automated visual validation.

## Verification Checklist:
- [ ] Does automated ADB harness trigger deep link invocation on emulator target?
- [ ] Are splash screen foreground assets verified via bitmap capture?
- [ ] Is dynamic ISP string detection verified on device runtime?
