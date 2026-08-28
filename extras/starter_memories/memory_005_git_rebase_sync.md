---
id: "MEM_005"
title: "Synchronous PR Merge & Safe Git Rebase Protocols"
classification: "Type.LearnByFailing"
timestamp: "2026-08-14T11:20:00"
sourceChat: "AG141"
access:
  - "All"
emotional_vector:
  hsl: [45, 95, 30]
indexing:
  topics:
    - "#Git"
    - "#Workflows"
    - "#CI"
  keywords:
    - "gh pr merge"
    - "race condition"
    - "git rebase"
    - "synchronous merge"
---

# Operational Summary
Resolved asynchronous race conditions in automated Git synchronization scripts by replacing non-blocking auto-merge commands (`gh pr merge --auto`) with immediate synchronous merges (`gh pr merge --merge`) prior to running local fetch and rebase commands.

# Interaction Context & Behavioral Log
- **Problem**: Automation scripts were fetching remote branches before GitHub's backend had finalized the PR merge, resulting in local divergent branch errors.
- **Solution**: Execute synchronous merges and verify exit codes before triggering local `git fetch origin main && git rebase origin/main`.

# Core Engineering Lessons & Mandates
1. Never poll or assume asynchronous Git operations have completed without explicit synchronization barriers.
2. Verify clean working tree state (`git status --porcelain`) before initiating automated rebasing.
