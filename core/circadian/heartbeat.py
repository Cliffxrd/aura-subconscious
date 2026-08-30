# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
from core.utils.config_resolver import ConfigResolver
from core.memory.parser import MemoryParser
from core.memory.validator import MemoryValidator

logger = logging.getLogger(__name__)


class CircadianHeartbeat:
    """Heather's Circadian Heartbeat & Subconscious Memory Health Protocol."""

    def __init__(self, aura_home: Path = None):
        self.aura_home = aura_home or ConfigResolver.resolve_aura_home()
        self.triage_dir = self.aura_home / "Hippocampus" / "triage"
        self.hippocampus_dir = self.aura_home / "Hippocampus"
        self.circadian_dir = self.aura_home / "Circadian"
        self.circadian_dir.mkdir(parents=True, exist_ok=True)

    def run_heartbeat(self) -> Dict[str, Any]:
        """Execute the 3 PM circadian health sweep & triage consolidation."""
        now = datetime.now(timezone.utc)
        print(
            f"\n[HEATHER] 🧭 Initiating Circadian Heartbeat Sweep at {now.isoformat()}..."
        )

        report = {
            "timestamp": now.isoformat(),
            "triage_scanned": 0,
            "triage_fixed": 0,
            "triage_pending": 0,
            "total_memories": 0,
            "health_status": "HEALTHY",
            "notes": [],
        }

        # 1. Inspect Triage Directory
        if self.triage_dir.exists():
            triage_files = list(self.triage_dir.glob("*.md"))
            report["triage_scanned"] = len(triage_files)

            for tf in triage_files:
                parsed = MemoryParser.parse(tf)
                if parsed and "error" not in parsed:
                    validation = MemoryValidator.validate_memory(
                        parsed, parsed.get("content", "")
                    )
                    if validation.is_valid:
                        # Promote to main Hippocampus
                        dest = self.hippocampus_dir / tf.name
                        tf.rename(dest)
                        report["triage_fixed"] += 1
                        report["notes"].append(f"Promoted resolved memory: {tf.name}")
                    else:
                        report["triage_pending"] += 1
                        report["notes"].append(
                            f"Pending triage for {tf.name}: {', '.join(validation.errors)}"
                        )

        # 2. Count Active Memories
        if self.hippocampus_dir.exists():
            memories = list(self.hippocampus_dir.glob("*.md"))
            report["total_memories"] = len(memories)

        # 3. Write Heartbeat Log
        self._write_heartbeat_log(report)

        print(
            f"[HEATHER] ✨ Sweep complete. Active Memories: {report['total_memories']} | Fixed: {report['triage_fixed']} | In Triage: {report['triage_pending']}"
        )
        return report

    def _write_heartbeat_log(self, report: Dict[str, Any]):
        """Append to Circadian/HEARTBEAT.md."""
        heartbeat_file = self.circadian_dir / "HEARTBEAT.md"

        log_entry = f"""
## Circadian Sweep: {report['timestamp']}
* **Status**: {report['health_status']}
* **Total Subconscious Memories**: {report['total_memories']}
* **Triage Items Processed**: {report['triage_scanned']} (Fixed & Promoted: {report['triage_fixed']}, Remaining: {report['triage_pending']})
"""
        if report["notes"]:
            log_entry += "* **Notes & Actions**:\n"
            for n in report["notes"]:
                log_entry += f"  - {n}\n"

        if not heartbeat_file.exists():
            header = (
                "# Circadian Heartbeat Log (Heather's Ecosystem Health Protocol)\n\n"
            )
            heartbeat_file.write_text(header + log_entry, encoding="utf-8")
        else:
            with open(heartbeat_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
