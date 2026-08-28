---
id: "MEM_003"
title: "Deterministic Coroutine Mutex Concurrency & Virtual Test Dispatchers"
classification: "Type.DefectFix"
timestamp: "2026-08-10T09:15:00"
sourceChat: "AG042"
access:
  - "All"
emotional_vector:
  hsl: [0, 95, 50]
indexing:
  topics:
    - "#Kotlin"
    - "#Coroutines"
    - "#Testing"
  keywords:
    - "Mutex"
    - "StandardTestDispatcher"
    - "race condition"
    - "flaky test"
---

# Operational Summary
Root-cause resolution of asynchronous race conditions and flaky concurrency unit tests in Kotlin Coroutines by utilizing `Mutex.withLock` alongside dependency-injected `CoroutineDispatcher` instances.

# Interaction Context & Behavioral Log
- **Problem**: Concurrent background tasks mutating shared state simultaneously, throwing `ConcurrentModificationException` and causing flaky test suites.
- **Solution**: Inject `ioDispatcher: CoroutineDispatcher = Dispatchers.IO` into ViewModels, allowing unit test suites to supply `StandardTestDispatcher(testScheduler)`.

# Core Engineering Lessons & Mandates
1. Always protect shared mutable state in Coroutines with `kotlinx.coroutines.sync.Mutex`.
2. Never hardcode `Dispatchers.IO` or `Dispatchers.Default` inside ViewModels; inject them via constructor parameters.
3. Use `runTest` with virtual time control for 100% deterministic test execution.
