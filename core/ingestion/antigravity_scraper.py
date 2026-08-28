# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class AntigravityScraper:
    """Parses Google Antigravity transcripts (JSONL) extracting steps and generating markdown."""
    
    def __init__(self, brain_dir: Path):
        self.brain_dir = Path(brain_dir)
        
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape transcript.jsonl files from the brain directory."""
        transcripts = []
        if not self.brain_dir.exists() or not self.brain_dir.is_dir():
            logger.warning(f"Brain directory {self.brain_dir} does not exist.")
            return transcripts
            
        for path in self.brain_dir.rglob("transcript.jsonl"):
            try:
                parsed_data = self.parse_transcript_file(path)
                if parsed_data:
                    transcripts.append(parsed_data)
            except Exception as e:
                logger.error(f"Failed to parse transcript {path}: {e}")
                
        return transcripts

    def parse_transcript_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parses a single jsonl transcript file."""
        steps = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        step_data = json.loads(line)
                        steps.append(self.extract_step_info(step_data))
                    except json.JSONDecodeError as e:
                        logger.warning(f"Malformed JSON on line in {file_path}: {e}")
                        
            if not steps:
                return None
                
            return {
                "source": "Antigravity",
                "path": str(file_path),
                "conversation_id": file_path.parent.parent.name if len(file_path.parts) > 2 else "unknown",
                "steps": steps,
                "markdown": self.generate_markdown(steps)
            }
        except IOError as e:
            logger.error(f"IOError reading {file_path}: {e}")
            return None

    def extract_step_info(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts relevant fields from a step."""
        return {
            "step_index": step.get("step_index", -1),
            "source": step.get("source", "UNKNOWN"),
            "type": step.get("type", "UNKNOWN"),
            "status": step.get("status", "UNKNOWN"),
            "created_at": step.get("created_at", ""),
            "content": step.get("content", ""),
            "thinking": step.get("thinking", ""),
            "tool_calls": step.get("tool_calls", [])
        }

    def generate_markdown(self, steps: List[Dict[str, Any]]) -> str:
        """Converts extracted steps into a readable markdown format."""
        lines = ["# Antigravity Transcript\n"]
        for step in sorted(steps, key=lambda x: x["step_index"]):
            source = step["source"]
            content = step["content"]
            lines.append(f"## Step {step['step_index']} - {source} ({step['type']})")
            lines.append(f"**Status**: {step['status']} | **Time**: {step['created_at']}\n")
            
            if step["thinking"]:
                lines.append("### Thinking\n```text")
                lines.append(step["thinking"])
                lines.append("```\n")
                
            if content:
                lines.append("### Content\n")
                lines.append(content)
                lines.append("\n")
                
            if step["tool_calls"]:
                lines.append("### Tool Calls\n")
                for tc in step["tool_calls"]:
                    lines.append(f"- `{tc}`")
                lines.append("\n")
                
            lines.append("---\n")
            
        return "\n".join(lines)
