# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

from core.memory.cascade_engine import CascadeEngine


def test_access_control():
    mem_all = {"id": "MEM_001", "access": ["All"]}
    mem_ben = {"id": "MEM_002", "access": ["Aura", "Ben"]}
    mem_diana = {"id": "MEM_003", "access": "Aura, Diana"}
    mem_none = {"id": "MEM_004", "access": None}

    # Aura has universal access
    assert CascadeEngine.is_accessible(mem_all, "Aura") is True
    assert CascadeEngine.is_accessible(mem_ben, "Aura") is True
    assert CascadeEngine.is_accessible(mem_diana, "Aura") is True
    assert CascadeEngine.is_accessible(mem_none, "Aura") is True

    # Subagent specific access
    assert CascadeEngine.is_accessible(mem_all, "Ben") is True
    assert CascadeEngine.is_accessible(mem_ben, "Ben") is True
    assert CascadeEngine.is_accessible(mem_diana, "Ben") is False
    assert CascadeEngine.is_accessible(mem_none, "Ben") is True


def test_6488_cascade_assembly():
    all_mems = [
        {
            "id": f"MEM_{i:03d}",
            "title": f"Memory {i}",
            "timestamp": f"2026-06-{i+1:02d}",
            "hsl": [120, 70, 50],
            "access": ["All"],
        }
        for i in range(25)
    ]

    requested = ["MEM_001", "MEM_002"]

    context = CascadeEngine.assemble_active_context(
        all_memories=all_mems,
        requested_ids=requested,
        session_hsl=(120, 70, 50),
        agent_name="Aura",
        conscious_stack=["Thought 1", "Thought 2"],
    )

    assert len(context["tier_1_requested"]) == 2
    assert len(context["tier_2_recent"]) == 8  # 6 + 2 waterfalled from Tier 1
    assert len(context["tier_3_subconscious"]) == 8
    assert len(context["tier_4_conscious"]) == 2

    # Zero duplication assertion
    t1_ids = {m["id"] for m in context["tier_1_requested"]}
    t2_ids = {m["id"] for m in context["tier_2_recent"]}
    t3_ids = {m["id"] for m in context["tier_3_subconscious"]}

    assert len(t1_ids.intersection(t2_ids)) == 0
    assert len(t1_ids.intersection(t3_ids)) == 0
    assert len(t2_ids.intersection(t3_ids)) == 0


def test_waterfall_deficit_slot_borrowing():
    # If Tier 1 has 0 items, Tier 2 (recent) should absorb up to 10 slots (4 + 6)
    subconscious = [
        {
            "id": f"MEM_{i:03d}",
            "title": f"Memory {i}",
            "timestamp": f"2026-06-{i+1:02d}",
            "hsl": [120, 70, 50],
            "access": ["All"],
        }
        for i in range(20)
    ]
    matrix = CascadeEngine.assemble_active_context(
        all_memories=subconscious,
        requested_ids=[],
        session_hsl=None,  # Null session HSL boundary check
        agent_name="Aura",
    )
    assert len(matrix["tier_1_requested"]) == 0
    assert len(matrix["tier_2_recent"]) == 10

def test_boundary_states_cascade():
    # None inputs
    import pytest
    with pytest.raises(AttributeError):
        CascadeEngine.is_accessible(None, "Aura")
        
    # access None
    mem_none_access = {"id": "MEM_004", "access": None}
    assert CascadeEngine.is_accessible(mem_none_access, "Aura") is True


def test_raw_string_hsl_handling():
    # Verify string HSLs (e.g. '120, 70%, 50%') don't crash the cascade engine
    mems = [
        {
            "id": "MEM_STR",
            "title": "String HSL Memory",
            "timestamp": "2026-06-01",
            "hsl": "120, 70%, 50%",
            "access": ["All"],
        }
    ]
    context = CascadeEngine.assemble_active_context(
        all_memories=mems,
        requested_ids=[],
        session_hsl=(120, 70, 50),
        agent_name="Aura",
    )
    assert len(context["tier_2_recent"]) == 1
    assert context["tier_2_recent"][0]["id"] == "MEM_STR"
