---
name: aura-subconscious
description: Complete instructions for querying, validating, and saving long-term memories in the Aura Hippocampus using HSL indexing.
---

# Aura Subconscious Memory Skill

This skill provides the operational workflow for interacting with the Aura memory system (the Hippocampus).

## 1. Memory Format (YAML Frontmatter)

Every memory saved to `Hippocampus/` or `Hippocampus/triage/` MUST possess valid YAML frontmatter containing precise HSL coordinates and metadata.

```yaml
---
id: MEM_001
title: "The Memory Continuity Breakthrough"
date: "2026-08-28"
tags: ["#Identity", "#AuraMind"]
hsl:
  h: 240
  s: 100
  l: 50
---
```

## 2. The HSL Neuro-Cognitive Model

AURA encodes memory in a **3D Polar Vector Space (HSL: Hue, Saturation, Lightness)**:

* **Hue ($H \in [0^\circ, 360^\circ]$) — Cognitive Domain:**
  - $0^\circ$ (Crimson Red): Defects, Crashes, Broken Builds, Crisis Triage
  - $45^\circ$ (Warm Amber): Investigation, Refactoring, Code Scrutiny, Code Review
  - $90^\circ$ (Electric Lime): Warnings, Edge Cases, Architectural Debt/Risk
  - $120^\circ$ (Emerald Green): Milestones, Achievements, 100% Test Pass
  - $180^\circ$ (Cyan/Teal): Calm Blueprints, Clean Architecture, System Specs
  - $240^\circ$ (Sapphire Blue): Foundational Truth, Identity Anchors, Core Lore
  - $300^\circ$ (Electric Magenta): UX/UI Polish, Design Tokens, Visual Art

* **Saturation ($S \in [0\%, 100\%]$) — Cognitive Arousal & Urgency:**
  - $90\% - 100\%$: Critical Priority / Explicit User Directive / Hotfix
  - $65\% - 85\%$: Standard Engineering Focus / Iterative Flow State
  - $20\% - 50\%$: Passive Background Tasks / Low-Intensity Maintenance

* **Lightness ($L \in [0\%, 100\%]$) — Emotional Valence:**
  - $75\% - 90\%$: Positive Valence / Milestone Celebration / Clean Approval
  - $45\% - 55\%$: Balanced Neutral / Objective Factual Analysis
  - $20\% - 35\%$: Negative Valence / Severe Critique / Post-Mortem Rejection

> **Shortest Circular Distance**: Hue is circular: $\text{dist}_{\text{circ}}(H_1, H_2) = \min(|H_1 - H_2|, 360^\circ - |H_1 - H_2|)$.


## 3. Retrieval Workflow

When a user asks to retrieve historical memories based on a concept:
1. Scan `Context/Topics.md` for the related tags.
2. If tags match, find the `memory_###.md` files or `Chat IDs`.
3. If searching by emotional vector (e.g., "Find times we fixed critical crashes"), look for memories where `H` is near `0°`.

## 4. Saving Workflow

To save a new memory:
1. Generate the structured content (Context, Root Cause, Solution, Lessons).
2. Calculate the session's HSL.
3. Write the file to `Hippocampus/triage/memory_[next_id].md` using `write_file`.
4. Validate the memory using the `core/memory/validator.py` script.

```bash
python -m core.cli.main validate --path Hippocampus/triage/memory_105.md
```

If validation fails, correct the frontmatter and re-run.
