# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import logging
from pathlib import Path
from core.utils.config_resolver import ConfigResolver
from core.memory.parser import MemoryParser
from core.memory.validator import MemoryValidator
from core.ingestion.registry import PlatformRegistry
from core import __version__, __author__, __license__

logger = logging.getLogger(__name__)


class AuraDoctor:
    """Diagnostic health check suite for AURA."""

    def __init__(self, aura_home: Path = None):
        self.aura_home = aura_home or ConfigResolver.resolve_aura_home()

    def run_diagnostics(self) -> bool:
        """Run all system checks and return overall health status."""
        print("[AURA] Running Neuro-Architecture Diagnostics...\n")
        engine_healthy = True

        # 1. Path Resolution
        print(f"[PASS] 1. AURA_HOME Path Resolved: {self.aura_home}")

        # 2. Check Cognitive Directories (Scaffolded state vs Uninitialized)
        print("\n[CHECK] 2. Checking Cognitive Brain Regions:")
        required_dirs = [
            "Cortex",
            "Hippocampus",
            "Amygdala",
            "Circadian",
            "Chronicle",
            "Context",
            "Personas",
        ]
        present_dirs = 0
        for d in required_dirs:
            dp = self.aura_home / d
            if dp.exists():
                print(f"  [PASS] /{d}")
                present_dirs += 1
            else:
                print(f"  [INFO] /{d} (Pending `aura init`)")

        # 3. Check Subconscious Memories Frontmatter
        print("\n[CHECK] 3. Checking Subconscious Memory Frontmatter & HSL Integrity:")
        hippocampus = self.aura_home / "Hippocampus"
        if hippocampus.exists():
            memories = list(hippocampus.glob("*.md"))
            valid_mems = 0
            for mem_file in memories:
                parsed = MemoryParser.parse(mem_file)
                if parsed and "error" not in parsed:
                    validation = MemoryValidator.validate_memory(
                        parsed, parsed.get("content", "")
                    )
                    if validation.is_valid:
                        valid_mems += 1
                    else:
                        print(
                            f"  [WARN] Memory {mem_file.name} validation failed: {validation.errors}"
                        )
                        engine_healthy = False
                else:
                    print(
                        f"  [WARN] Corrupted memory {mem_file.name}: {parsed.get('error')}"
                    )
                    engine_healthy = False

            print(
                f"  [INFO] Valid Memories in Hippocampus: {valid_mems}/{len(memories)}"
            )
        else:
            print("  [INFO] No local Hippocampus found. Fresh install state.")

        # 4. Ingestion Platform Registry
        print("\n[CHECK] 4. Universal Platform Registry: ", end="")
        platforms = PlatformRegistry.list_platforms()
        if len(platforms) >= 50:
            print(f"[PASS] {len(platforms)} AI Platforms Loaded.")
        else:
            print(f"[WARN] Only {len(platforms)} platforms registered.")
            engine_healthy = False

        # 5. Versioning & SSOT
        print(
            f"\n[CHECK] 5. Framework Telemetry & SSOT: [PASS] v{__version__} ({__license__}) by {__author__}"
        )

        print("\n" + "=" * 50)
        if engine_healthy:
            if present_dirs == len(required_dirs):
                print(
                    "[SUCCESS] AURA Diagnostics Status: ALL SYSTEMS HEALTHY & SYNCHRONIZED"
                )
            else:
                print(
                    f"[SUCCESS] AURA Diagnostics Status: ENGINE READY ({present_dirs}/{len(required_dirs)} regions active - Run `aura init` to scaffold user brain)"
                )
        else:
            print("[ERROR] AURA Diagnostics Status: INTEGRITY ERRORS DETECTED")
        print("=" * 50 + "\n")

        return engine_healthy
