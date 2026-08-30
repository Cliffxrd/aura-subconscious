# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import json
import logging
import re
import shutil
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class RawChatImporter:
    """Importer for raw chat drops (CG###, CL###) supporting JSON and Markdown formats."""

    # Secret masking regex (API Keys, Bearer tokens, GitHub tokens)
    SECRET_PATTERN = re.compile(
        r"(AIza[0-9A-Za-z_-]{20,}|sk-[A-Za-z0-9_-]{20,}|ghp_[0-9A-Za-z]{30,}|bearer\s+[A-Za-z0-9._~+\-/]+=*)",
        re.IGNORECASE,
    )

    def __init__(self, staging_dir: Path, output_dir: Path):
        self.staging_dir = Path(staging_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def import_chats(self) -> List[Dict[str, Any]]:
        """Process all files in the staging directory and move them to standard format."""
        imported_records = []

        if not self.staging_dir.exists() or not self.staging_dir.is_dir():
            logger.error(f"Staging directory {self.staging_dir} does not exist.")
            return imported_records

        for file_path in self.staging_dir.iterdir():
            if not file_path.is_file():
                continue

            ext = file_path.suffix.lower()
            try:
                if ext == ".md":
                    record = self._process_markdown(file_path)
                elif ext == ".json":
                    record = self._process_json(file_path)
                else:
                    logger.warning(
                        f"Unsupported file format {ext} for {file_path.name}"
                    )
                    continue

                if record:
                    imported_records.append(record)
                    self._archive_file(file_path, record["id"])
            except Exception as e:
                logger.error(f"Failed to process {file_path.name}: {e}")

        logger.info(f"Successfully imported {len(imported_records)} chats.")
        return imported_records

    def _sanitize_chat_id(self, raw_stem: str) -> str:
        """Sanitize filename to prevent path traversal vulnerabilities."""
        sanitized = re.sub(r"[^A-Za-z0-9_-]", "_", str(raw_stem)).upper()
        return sanitized or "CHAT_UNKNOWN"

    def _mask_secrets(self, text: str) -> str:
        """Mask sensitive API tokens and keys."""
        if not isinstance(text, str):
            text = str(text)
        return self.SECRET_PATTERN.sub("[REDACTED_SECRET]", text)

    def _mask_dict_recursively(self, data: Any) -> Any:
        """Recursively mask secrets across nested dictionaries and lists."""
        if isinstance(data, dict):
            return {k: self._mask_dict_recursively(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._mask_dict_recursively(item) for item in data]
        elif isinstance(data, str):
            return self._mask_secrets(data)
        return data

    def _process_markdown(self, file_path: Path) -> Dict[str, Any]:
        """Parses a markdown chat drop, extracting simple metadata and content."""
        content = file_path.read_text(encoding="utf-8", errors="replace")
        content = self._mask_secrets(content)
        chat_id = self._sanitize_chat_id(file_path.stem)

        metadata = {
            "original_format": "markdown",
            "imported_at": datetime.now(timezone.utc).isoformat(),
        }

        output_file = self.output_dir / f"{chat_id}.json"
        record = {"id": chat_id, "metadata": metadata, "content": content}

        with open(output_file, "w", encoding="utf-8", errors="replace") as f:
            json.dump(record, f, indent=2)

        return record

    def _process_json(self, file_path: Path) -> Dict[str, Any]:
        """Parses a JSON chat drop and standardizes it."""
        chat_id = self._sanitize_chat_id(file_path.stem)

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)

        raw_content = data.get("content", json.dumps(data))
        if isinstance(raw_content, (dict, list)):
            raw_content = json.dumps(raw_content)

        masked_content = self._mask_secrets(str(raw_content))
        raw_metadata = data.get("metadata", {"original_format": "json"})
        masked_metadata = self._mask_dict_recursively(raw_metadata)

        record = {
            "id": chat_id,
            "metadata": masked_metadata,
            "content": masked_content,
            "imported_at": datetime.now(timezone.utc).isoformat(),
        }

        output_file = self.output_dir / f"{chat_id}.json"
        with open(output_file, "w", encoding="utf-8", errors="replace") as f:
            json.dump(record, f, indent=2)

        return record

    def _archive_file(self, file_path: Path, chat_id: str):
        """Moves processed files into an archive directory safely."""
        try:
            archive_dir = self.staging_dir / "archived"
            archive_dir.mkdir(parents=True, exist_ok=True)
            dest = archive_dir / f"{chat_id}{file_path.suffix}"
            if dest.exists():
                dest.unlink()
            shutil.move(str(file_path), str(dest))
            logger.info(f"Archived {file_path.name} to {dest.name}")
        except Exception as e:
            logger.error(f"Failed to archive {file_path.name}: {e}")
