# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import re
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class MemoryValidator:
    """Robust quality gates and structural validation for AURA memory files."""

    MIN_WORD_COUNT = 50
    REQUIRED_TAGS = 1

    # HSL string format: "120, 70%, 50%" or "[120, 70, 50]" or "120, 70, 50"
    HSL_PATTERN = re.compile(
        r"\[?\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?%?)\s*,\s*(\d+(?:\.\d+)?%?)\s*\]?"
    )

    # Prohibited placeholder patterns (Zero-TODO Mandate)
    TODO_PATTERN = re.compile(
        r"(//\s*TODO|TODO:|//\s*Fix later|FIXME:|/\*\s*TODO|#\s*TODO)",
        re.IGNORECASE,
    )

    @staticmethod
    def validate_memory(
        metadata: Dict[str, Any], content: Optional[str]
    ) -> ValidationResult:
        """Validate a memory against AURA quality gates and constraints."""
        errors = []
        warnings = []

        if content is None:
            content = ""

        # 1. Zero-TODO Mandate Check
        if MemoryValidator.TODO_PATTERN.search(content):
            errors.append(
                "Zero-TODO Mandate Violation: Memory content contains placeholder comments (// TODO, FIXME, etc.)."
            )

        # 2. Check word count
        words = content.split()
        if len(words) < MemoryValidator.MIN_WORD_COUNT:
            errors.append(
                f"Content length ({len(words)} words) is below minimum required ({MemoryValidator.MIN_WORD_COUNT})."
            )

        # 3. Check required metadata fields
        if "title" not in metadata or not metadata["title"]:
            errors.append("Missing required metadata field: 'title'.")

        # 4. Check tags
        tags = metadata.get("tags", [])
        if isinstance(tags, str):
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        elif isinstance(tags, list):
            tag_list = tags
        else:
            tag_list = []

        if len(tag_list) < MemoryValidator.REQUIRED_TAGS:
            errors.append(
                f"Insufficient tags. Found {len(tag_list)}, required {MemoryValidator.REQUIRED_TAGS}."
            )

        # 5. Check HSL bounds completely
        hsl_val = metadata.get("hsl")
        if hsl_val is not None:
            hsl_errors = MemoryValidator._validate_hsl(hsl_val)
            if hsl_errors:
                errors.extend(hsl_errors)
        else:
            warnings.append("Missing 'hsl' emotional coordinate. Using default.")

        return ValidationResult(
            is_valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    @staticmethod
    def _validate_hsl(hsl_val: Union[str, List[Any]]) -> List[str]:
        """Strict validation of HSL formats and bounds supporting strings or lists."""
        errors = []

        if isinstance(hsl_val, list):
            if len(hsl_val) != 3:
                return [
                    f"Invalid HSL list length ({len(hsl_val)} items). Expected exactly 3 elements [H, S, L]."
                ]
            try:
                h = float(str(hsl_val[0]).strip().replace("°", ""))
                s = float(str(hsl_val[1]).strip().replace("%", ""))
                l = float(str(hsl_val[2]).strip().replace("%", ""))
            except (ValueError, TypeError) as e:
                return [f"Could not parse HSL list elements as numbers: {e}"]
        else:
            hsl_str = str(hsl_val).strip()
            # Clean possible Python stringified list quotes: "['120', '70%', '50%']" -> "120, 70%, 50%"
            hsl_str = hsl_str.replace("'", "").replace('"', "")
            match = MemoryValidator.HSL_PATTERN.search(hsl_str)
            if not match:
                return [
                    f"Invalid HSL format: '{hsl_val}'. Expected format: 'H, S, L' or '[H, S%, L%]'"
                ]
            try:
                h_str, s_str, l_str = match.groups()
                h = float(h_str)
                s = float(s_str.replace("%", ""))
                l = float(l_str.replace("%", ""))
            except ValueError as e:
                return [f"Could not parse HSL values as floats: {e}"]

        if not (0 <= h <= 360):
            errors.append(f"Hue {h} is out of bounds (0-360).")
        if not (0 <= s <= 100):
            errors.append(f"Saturation {s} is out of bounds (0-100).")
        if not (0 <= l <= 100):
            errors.append(f"Lightness {l} is out of bounds (0-100).")

        return errors
