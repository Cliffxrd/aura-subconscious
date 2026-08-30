# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import json
from pathlib import Path
from core.ingestion.raw_chat_importer import RawChatImporter


def test_raw_chat_importer_markdown(tmp_path):
    staging = tmp_path / "staging"
    output = tmp_path / "output"
    staging.mkdir()
    output.mkdir()

    # Create dummy chat drop with a secret token
    drop_file = staging / "CG001.md"
    drop_file.write_text(
        "# Chat Session\nHere is my api key: AIzaSyD9876543210123456789012345678901\nLet's discuss architecture.",
        encoding="utf-8",
    )

    importer = RawChatImporter(staging_dir=staging, output_dir=output)
    records = importer.import_chats()

    assert len(records) == 1
    assert records[0]["id"] == "CG001"
    assert "[REDACTED_SECRET]" in records[0]["content"]
    assert "AIzaSyD" not in records[0]["content"]

    # Verify output JSON created
    out_json = output / "CG001.json"
    assert out_json.exists()


def test_raw_chat_importer_json(tmp_path):
    staging = tmp_path / "staging"
    output = tmp_path / "output"
    staging.mkdir()
    output.mkdir()

    drop_file = staging / "CL042.json"
    drop_file.write_text(
        json.dumps(
            {
                "metadata": {"model": "claude-3-opus"},
                "content": "Bearer sk-1234567890abcdef1234567890",
            }
        ),
        encoding="utf-8",
    )

    importer = RawChatImporter(staging_dir=staging, output_dir=output)
    records = importer.import_chats()

    assert len(records) == 1
    assert records[0]["id"] == "CL042"
    assert "[REDACTED_SECRET]" in records[0]["content"]

def test_boundary_states_scrapers():
    import pytest
    with pytest.raises(Exception):
        RawChatImporter(staging_dir=None, output_dir=None)
