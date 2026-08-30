# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

from core.memory.parser import MemoryParser


def test_parse_valid_yaml_frontmatter():
    content = """---
title: "Test Memory"
hsl: [120, 70%, 50%]
tags: ["#Kotlin", "#Compose"]
---
This is a test memory body containing the architectural explanation.
- Point one
- Point two
"""
    metadata, body = MemoryParser.parse_file(content)
    assert metadata["title"] == "Test Memory"
    assert metadata["hsl"] == ["120", "70%", "50%"]
    assert metadata["tags"] == ["#Kotlin", "#Compose"]
    assert "This is a test memory body" in body


def test_parse_bullets():
    body = """
Some narrative text.
- Bullet 1
* Bullet 2
- Bullet 3
"""
    bullets = MemoryParser.extract_bullets(body)
    assert len(bullets) == 3
    assert bullets[0] == "Bullet 1"
    assert bullets[1] == "Bullet 2"
    assert bullets[2] == "Bullet 3"
    # Null/type boundary check
    assert MemoryParser.extract_bullets(None) == []
    assert MemoryParser.extract_bullets(123) == []


def test_parse_empty_or_malformed_frontmatter():
    content = "Just pure markdown without YAML frontmatter."
    metadata, body = MemoryParser.parse_file(content)
    assert metadata == {}
    assert body == content

def test_boundary_states_parser():
    import pytest
    with pytest.raises(TypeError):
        MemoryParser.parse_file(None)
    
    assert MemoryParser.extract_bullets(None) == []
    
    # Empty string
    metadata, body = MemoryParser.parse_file("")
    assert metadata == {}
    assert body == ""
