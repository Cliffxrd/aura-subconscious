---
name: QA-1
description: Zero Self-Certification Policy (The Non-Bypassable QA Gate)
type: rule
author: Miranda
hooks:
  - pr-merge-blocker
---
# QA-1: Zero Self-Certification Policy (The Non-Bypassable QA Gate)

**Description:** Developer agents (Mike, Diana, Ben) are strictly prohibited from self-certifying UI tasks or marking them as ReadyForTesting or Completed. Task transition to Verified requires automated CI execution, visual snapshot artifacts, and formal sign-off from Miranda (QA Lead).

**Enforcement Mechanism:** Automated PR merge blocker. Any PR merged without explicit QA Lead approval and passing CI screenshot artifacts will be automatically reverted by the repository build system.

## Verification Checklist:
- [ ] Has developer self-certification been disabled in project workflow permissions?
- [ ] Are automated CI pipeline tests 100% green before QA review?
- [ ] Has Miranda (QA Lead) signed off on generated visual diff artifacts?
