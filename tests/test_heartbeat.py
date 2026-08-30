# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

from pathlib import Path
from core.circadian.heartbeat import CircadianHeartbeat


def test_circadian_heartbeat_run(tmp_path):
    # Setup dummy AURA_HOME
    aura_home = tmp_path / ".aura"
    triage_dir = aura_home / "Hippocampus" / "triage"
    triage_dir.mkdir(parents=True)

    # Place a valid memory in triage to test auto-promotion
    valid_mem = triage_dir / "memory_fixed.md"
    body_55_words = " ".join(["word"] * 55)
    valid_mem.write_text(
        f"---\ntitle: 'Resolved Issue'\nhsl: [120, 70, 50]\ntags: ['#Fix']\n---\n{body_55_words}",
        encoding="utf-8",
    )

    heartbeat = CircadianHeartbeat(aura_home=aura_home)
    report = heartbeat.run_heartbeat()

    assert report["triage_scanned"] == 1
    assert report["triage_fixed"] == 1
    assert (aura_home / "Hippocampus" / "memory_fixed.md").exists()
    assert (aura_home / "Circadian" / "HEARTBEAT.md").exists()
