# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import re
from typing import Dict, Any, List, Optional
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
    HSL_PATTERN = re.compile(r'\[?\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?%?)\s*,\s*(\d+(?:\.\d+)?%?)\s*\]?')

    @staticmethod
    def validate_memory(metadata: Dict[str, Any], content: str) -> ValidationResult:
        """Validate a memory against AURA quality gates and constraints."""
        errors = []
        warnings = []
        
        # Check word count
        words = content.split()
        if len(words) < MemoryValidator.MIN_WORD_COUNT:
            errors.append(f"Content length ({len(words)} words) is below minimum required ({MemoryValidator.MIN_WORD_COUNT}).")
            
        # Check required metadata fields
        if "title" not in metadata:
            errors.append("Missing required metadata field: 'title'.")
            
        # Check tags
        tags = metadata.get("tags", [])
        if isinstance(tags, str):
            tag_list = [t.strip() for t in tags.split(',') if t.strip()]
        elif isinstance(tags, list):
            tag_list = tags
        else:
            tag_list = []
            
        if len(tag_list) < MemoryValidator.REQUIRED_TAGS:
            errors.append(f"Insufficient tags. Found {len(tag_list)}, required {MemoryValidator.REQUIRED_TAGS}.")
            
        # Check HSL bounds completely
        hsl_val = metadata.get("hsl")
        if hsl_val:
            hsl_errors = MemoryValidator._validate_hsl(str(hsl_val))
            if hsl_errors:
                errors.extend(hsl_errors)
        else:
            warnings.append("Missing 'hsl' emotional coordinate. Using default.")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    @staticmethod
    def _validate_hsl(hsl_str: str) -> List[str]:
        """Strict validation of HSL string formats and bounds."""
        errors = []
        match = MemoryValidator.HSL_PATTERN.search(hsl_str)
        if not match:
            return [f"Invalid HSL format: '{hsl_str}'. Expected format: 'H, S, L' or '[H, S%, L%]'."]
            
        try:
            h_str, s_str, l_str = match.groups()
            
            h = float(h_str)
            s = float(s_str.replace('%', ''))
            l = float(l_str.replace('%', ''))
            
            if not (0 <= h <= 360):
                errors.append(f"Hue {h} is out of bounds (0-360).")
            if not (0 <= s <= 100):
                errors.append(f"Saturation {s} is out of bounds (0-100).")
            if not (0 <= l <= 100):
                errors.append(f"Lightness {l} is out of bounds (0-100).")
        except ValueError as e:
            errors.append(f"Could not parse HSL values as floats: {e}")
            
        return errors
