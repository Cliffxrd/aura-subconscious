# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

from core.memory.validator import MemoryValidator


def test_validate_memory_valid():
    metadata = {
        "title": "State Hoisting in Compose",
        "hsl": "120, 70%, 50%",
        "tags": ["#Compose", "#Architecture"],
    }
    # 55 words body
    content = " ".join(["word"] * 55)
    res = MemoryValidator.validate_memory(metadata, content)
    assert res.is_valid is True
    assert len(res.errors) == 0


def test_validate_memory_todo_violation():
    metadata = {
        "title": "Unfinished Work",
        "hsl": [120, 70, 50],
        "tags": ["#Test"],
    }
    content = (
        "This is a long text with over fifty words to pass the length constraint. " * 5
    )
    content += "\n// TODO: Fix this later"
    res = MemoryValidator.validate_memory(metadata, content)
    assert res.is_valid is False
    assert any("Zero-TODO Mandate" in e for e in res.errors)


def test_validate_memory_word_count_short():
    metadata = {
        "title": "Short Note",
        "hsl": "120, 70, 50",
        "tags": ["#Test"],
    }
    content = "Too short"
    res = MemoryValidator.validate_memory(metadata, content)
    assert res.is_valid is False
    assert any("below minimum required" in e for e in res.errors)


def test_validate_hsl_formats():
    # String format
    assert len(MemoryValidator._validate_hsl("120, 70%, 50%")) == 0
    assert len(MemoryValidator._validate_hsl("[120, 70, 50]")) == 0
    # List format
    assert len(MemoryValidator._validate_hsl([120, "70%", "50%"])) == 0
    assert len(MemoryValidator._validate_hsl(["120", "70", "50"])) == 0
    # Out of bounds
    assert len(MemoryValidator._validate_hsl("400, 70%, 50%")) > 0
    assert len(MemoryValidator._validate_hsl("120, 150%, 50%")) > 0

def test_boundary_states_validator():
    # None metadata
    res = MemoryValidator.validate_memory(None, "content")
    assert res.is_valid is False
    assert "Invalid metadata format: must be a dictionary." in res.errors

    # Malformed types: metadata string
    res2 = MemoryValidator.validate_memory("not a dict", "content")
    assert res2.is_valid is False
    assert "Invalid metadata format: must be a dictionary." in res2.errors
    
    # String HSL invalid
    assert len(MemoryValidator._validate_hsl("invalid_hsl")) > 0
    assert len(MemoryValidator._validate_hsl(None)) > 0
    assert len(MemoryValidator._validate_hsl(123)) > 0
