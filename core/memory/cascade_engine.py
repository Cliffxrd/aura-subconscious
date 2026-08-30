# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

"""
AURA 6-4-8-8 harmonic signature Memory Matrix & Cascade Engine
Governs the multi-tier cognitive memory array:
- Tier 1: Requested Directives (Max 4 slots)
- Tier 2: Recent Episodic Memories (Top 6 slots)
- Tier 3: Subconscious Vector Proximity Memories (Top 8 slots)
- Tier 4: Rolling Conscious Working Stack (Max 8 slots)

Total context allocation: 26 maximum synchronized working slots with zero token duplication.
"""

import re
from typing import List, Dict, Any, Optional, Set, Tuple
from core.memory.hsl_vector import HSLVector


class CascadeEngine:
    """4-6-8-8 Memory Matrix cascade deduplication, slot borrowing, and multi-tenant isolation."""

    TIER_1_MAX = 4  # Requested Directives
    TIER_2_MAX = 6  # Recent Episodic
    TIER_3_MAX = 8  # Subconscious Vector
    TIER_4_MAX = 8  # Rolling Conscious

    @staticmethod
    def _parse_hsl(mem_hsl: Any) -> Tuple[float, float, float]:
        """Safely parse various HSL coordinate formats into a 3-tuple of floats."""
        default_hsl = (240.0, 70.0, 50.0)
        if isinstance(mem_hsl, (list, tuple)):
            if len(mem_hsl) == 3:
                try:
                    return (
                        float(str(mem_hsl[0]).replace("°", "")),
                        float(str(mem_hsl[1]).replace("%", "")),
                        float(str(mem_hsl[2]).replace("%", "")),
                    )
                except (ValueError, TypeError):
                    return default_hsl
            return default_hsl
        elif isinstance(mem_hsl, str):
            cleaned = (
                mem_hsl.replace("[", "")
                .replace("]", "")
                .replace("'", "")
                .replace('"', "")
            )
            parts = [
                p.strip().replace("°", "").replace("%", "")
                for p in cleaned.split(",")
                if p.strip()
            ]
            if len(parts) == 3:
                try:
                    return (float(parts[0]), float(parts[1]), float(parts[2]))
                except ValueError:
                    return default_hsl
        return default_hsl

    @staticmethod
    def is_accessible(memory: Dict[str, Any], agent_name: str = "Aura") -> bool:
        """
        Multi-tenant access control:
        - Access: All / Aura -> Accessible by Aura and all subagents
        - Access: Aura, <AgentName> -> Accessible only by Aura and that specific subagent
        """
        access_list = memory.get("access", ["All"])
        if access_list is None:
            access_list = ["All"]
        elif isinstance(access_list, str):
            access_list = [a.strip() for a in access_list.split(",") if a.strip()]

        if "All" in access_list or agent_name == "Aura":
            return True

        return agent_name in access_list

    @classmethod
    def assemble_active_context(
        cls,
        all_memories: List[Dict[str, Any]],
        requested_ids: List[str],
        session_hsl: Optional[Tuple[float, float, float]] = None,
        agent_name: str = "Aura",
        conscious_stack: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Assembles the complete 6-4-8-8 memory array for active session hydration.
        Guarantees 100% cascade deduplication and waterfall slot-borrowing.
        """
        if conscious_stack is None:
            conscious_stack = []

        if session_hsl is None:
            session_hsl = (240.0, 70.0, 50.0)

        # Filter memories accessible to this agent
        accessible_memories = [
            m for m in all_memories if cls.is_accessible(m, agent_name)
        ]

        used_ids: Set[str] = set()
        memory_map = {
            str(m.get("id")): m for m in accessible_memories if m.get("id") is not None
        }

        # 1. Tier 1: Explicit Requested Directives (Max 4 slots)
        tier_1: List[Dict[str, Any]] = []
        for req_id in requested_ids:
            s_req_id = str(req_id)
            if s_req_id in memory_map and s_req_id not in used_ids:
                if len(tier_1) < cls.TIER_1_MAX:
                    tier_1.append(memory_map[s_req_id])
                    used_ids.add(s_req_id)

        tier_1_deficit = cls.TIER_1_MAX - len(tier_1)
        tier_2_capacity = cls.TIER_2_MAX + max(0, tier_1_deficit)  # Waterfall down

        # 2. Tier 2: Recent Episodic Memories (Sorted by timestamp descending)
        tier_2: List[Dict[str, Any]] = []

        def safe_timestamp(x: Dict[str, Any]) -> str:
            return str(x.get("timestamp", ""))

        sorted_by_date = sorted(
            accessible_memories,
            key=safe_timestamp,
            reverse=True,
        )

        for mem in sorted_by_date:
            m_id = str(mem.get("id", ""))
            if m_id and m_id not in used_ids:
                if len(tier_2) < tier_2_capacity:
                    tier_2.append(mem)
                    used_ids.add(m_id)

        tier_2_deficit = tier_2_capacity - len(tier_2)
        tier_3_capacity = cls.TIER_3_MAX + max(0, tier_2_deficit)  # Waterfall down

        # 3. Tier 3: Subconscious Vector Proximity Memories (Ranked by HSL weight)
        tier_3: List[Dict[str, Any]] = []
        scored_memories = []
        for mem in accessible_memories:
            m_id = str(mem.get("id", ""))
            if m_id and m_id not in used_ids:
                mem_hsl = cls._parse_hsl(mem.get("hsl"))
                weight = HSLVector.calculate_weight(mem_hsl, session_hsl)
                scored_memories.append((weight, mem))

        # Sort by weight descending
        scored_memories.sort(key=lambda x: x[0], reverse=True)

        for weight, mem in scored_memories:
            if len(tier_3) < tier_3_capacity:
                mem_copy = dict(mem)
                mem_copy["proximity_weight"] = round(weight, 3)
                tier_3.append(mem_copy)
                used_ids.add(str(mem.get("id", "")))

        # 4. Tier 4: Conscious Rolling Memories (FIFO stack up to 8 slots)
        tier_4 = conscious_stack[-cls.TIER_4_MAX :]

        return {
            "tier_1_requested": tier_1,
            "tier_2_recent": tier_2,
            "tier_3_subconscious": tier_3,
            "tier_4_conscious": tier_4,
            "total_active_memories": len(tier_1) + len(tier_2) + len(tier_3),
            "allocated_slots": {
                "tier_1": len(tier_1),
                "tier_2": len(tier_2),
                "tier_3": len(tier_3),
                "tier_4": len(tier_4),
            },
        }
