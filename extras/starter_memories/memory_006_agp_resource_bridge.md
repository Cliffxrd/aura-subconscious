---
id: "MEM_006"
title: "AGP 9.0+ KMP Module Migration & Compose Resources Packaging"
classification: "Type.LearnByFailing"
timestamp: "2026-08-16T18:00:00"
sourceChat: "AG205"
access:
  - "All"
emotional_vector:
  hsl: [0, 95, 50]
indexing:
  topics:
    - "#Android"
    - "#AGP"
    - "#Gradle"
    - "#Compose"
  keywords:
    - "AGP 9.0"
    - "com.android.kotlin.multiplatform.library"
    - "composeResources"
    - "MissingResourceException"
---

# Operational Summary
Workaround for a critical breaking change in Android Gradle Plugin (AGP) 9.0+ when bundling JetBrains Compose Multiplatform resources: AGP 9.0+ strictly bans `com.android.library` in KMP modules, enforcing `com.android.kotlin.multiplatform.library`, which fails to automatically bundle `composeResources` into Android assets, throwing runtime `MissingResourceException`.

# Interaction Context & Behavioral Log
- **Problem**: Runtime crash `MissingResourceException` when attempting to load images/strings via `Res.readBytes()` or `painterResource()`.
- **Solution**: Implement a custom `copyKmpComposeResources` Gradle task in `androidApp/build.gradle.kts` that evaluates Providers to absolute Files and appends to `sourceSets.main.assets.srcDirs`.

# Core Engineering Lessons & Mandates
1. In AGP 9.0+, never apply `com.android.library` to multiplatform modules.
2. Wire custom resource copy tasks before `preBuild` to ensure assets are packaged into the APK.
