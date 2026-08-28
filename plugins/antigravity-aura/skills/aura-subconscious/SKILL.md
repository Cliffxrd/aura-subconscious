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

## 2. Calculating HSL

- **Hue (H):** 0° (Defect), 45° (Investigation), 90° (Warning), 120° (Milestone), 180° (Blueprint), 240° (Fact), 300° (UX/UI).
- **Saturation (S):** Intensity of the lesson (0-100).
- **Lightness (L):** Positive/negative valence (30 for failure, 80 for success).

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
