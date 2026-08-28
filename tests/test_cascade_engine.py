# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

from core.memory.cascade_engine import CascadeEngine

def test_access_control():
    mem_all = {"id": "MEM_001", "access": ["All"]}
    mem_ben = {"id": "MEM_002", "access": ["Aura", "Ben"]}
    mem_diana = {"id": "MEM_003", "access": ["Aura", "Diana"]}
    
    # Aura sees everything
    assert CascadeEngine.is_accessible(mem_all, "Aura") is True
    assert CascadeEngine.is_accessible(mem_ben, "Aura") is True
    assert CascadeEngine.is_accessible(mem_diana, "Aura") is True
    
    # Ben only sees All and Ben
    assert CascadeEngine.is_accessible(mem_all, "Ben") is True
    assert CascadeEngine.is_accessible(mem_ben, "Ben") is True
    assert CascadeEngine.is_accessible(mem_diana, "Ben") is False

def test_6488_cascade_assembly():
    all_memories = [
        {"id": f"MEM_{i:03d}", "timestamp": f"2026-08-{i:02d}T12:00:00", "hsl": (240, 70, 50), "access": ["All"]}
        for i in range(1, 25)
    ]
    
    requested = ["MEM_001", "MEM_002"]
    session_hsl = (240.0, 70.0, 50.0)
    conscious = ["realization_1", "realization_2"]
    
    context = CascadeEngine.assemble_active_context(
        all_memories=all_memories,
        requested_ids=requested,
        session_hsl=session_hsl,
        agent_name="Aura",
        conscious_stack=conscious
    )
    
    # Tier 1: 2 requested
    assert len(context["tier_1_requested"]) == 2
    # Tier 2: 6 base + 2 waterfall deficit from Tier 1 = 8
    assert len(context["tier_2_recent"]) == 8
    # Tier 3: 8 subconscious slots
    assert len(context["tier_3_subconscious"]) == 8
    # Tier 4: 2 conscious stack items
    assert len(context["tier_4_conscious"]) == 2
    
    # Verify zero ID duplication across tiers
    tier1_ids = {m["id"] for m in context["tier_1_requested"]}
    tier2_ids = {m["id"] for m in context["tier_2_recent"]}
    tier3_ids = {m["id"] for m in context["tier_3_subconscious"]}
    
    assert len(tier1_ids.intersection(tier2_ids)) == 0
    assert len(tier1_ids.intersection(tier3_ids)) == 0
    assert len(tier2_ids.intersection(tier3_ids)) == 0

