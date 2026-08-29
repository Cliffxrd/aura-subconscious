# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any
from core.utils.config_resolver import ConfigResolver
from core.memory.parser import MemoryParser
from core.memory.validator import MemoryValidator


class AuraDoctor:
    """Comprehensive diagnostic health check suite for AURA."""

    REQUIRED_DIRS = [
        "Cortex",
        "Hippocampus",
        "Amygdala",
        "Circadian",
        "Chronicle",
        "Context",
        "Personas",
    ]

    @classmethod
    def run_health_check(cls, cli_override: str = None) -> bool:
        """Run all diagnostic health checks."""
        print("[AURA] Running Neuro-Architecture Diagnostics...\n")
        all_passed = True

        # 1. Check Configuration Resolution
        aura_home = ConfigResolver.resolve_aura_home(cli_override)
        print(
            f"[{'PASS' if aura_home else 'FAIL'}] 1. AURA_HOME Path Resolved: {aura_home}"
        )
        if not aura_home:
            all_passed = False

        # 2. Check Biological Directory Structure
        print("\n[CHECK] 2. Checking Cognitive Brain Regions:")
        if aura_home and aura_home.exists():
            for d in cls.REQUIRED_DIRS:
                d_path = aura_home / d
                status = "PASS" if d_path.exists() else "WARN"
                print(f"  [{status}] /{d}")
        else:
            print("  [WARN] AURA_HOME directory not yet initialized (Run `aura init`).")

        # 3. Check Memory Frontmatter & HSL Integrity
        print("\n[CHECK] 3. Checking Subconscious Memory Frontmatter & HSL Integrity:")
        hippocampus = aura_home / "Hippocampus" if aura_home else None
        if hippocampus and hippocampus.exists():
            mem_files = list(hippocampus.glob("*.md"))
            valid_mems = 0
            for mem_file in mem_files:
                parsed = MemoryParser.parse(mem_file)
                if parsed and MemoryValidator.validate(parsed):
                    valid_mems += 1
                else:
                    print(f"  [WARN] Corrupted or non-standard memory: {mem_file.name}")
            print(
                f"  [PASS] Verified {valid_mems}/{len(mem_files)} subconscious memory artifacts."
            )
        else:
            print("  [INFO] No local Hippocampus found. Fresh install state.")

        # 4. Check Platform Registry
        from core.ingestion.registry import PlatformRegistry

        prefixes = PlatformRegistry.list_all_prefixes()
        print(
            f"\n[CHECK] 4. Universal Platform Registry: [PASS] {len(prefixes)} AI Platforms Loaded."
        )

        # 5. Check Framework Version & Telemetry SSOT
        from core.__version__ import __version__, __author__, __license__

        print(
            f"\n[CHECK] 5. Framework Telemetry & SSOT: [PASS] v{__version__} ({__license__}) by {__author__}"
        )

        print("\n" + "=" * 50)
        if all_passed:
            print(
                "[SUCCESS] AURA Diagnostics Status: ALL SYSTEMS HEALTHY & SYNCHRONIZED"
            )
        else:
            print("[WARNING] AURA Diagnostics Status: ATTENTION REQUIRED")
        print("=" * 50 + "\n")

        return all_passed
