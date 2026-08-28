from typing import Dict, Any, List

class MemoryValidator:
    """Quality gates for AURA memory files."""
    
    MIN_WORD_COUNT = 50
    REQUIRED_TAGS = 1
    
    @staticmethod
    def validate_memory(metadata: Dict[str, Any], content: str) -> List[str]:
        """Validate a memory against AURA quality gates."""
        errors = []
        
        # Check word count
        words = content.split()
        if len(words) < MemoryValidator.MIN_WORD_COUNT:
            errors.append(f"Content too short ({len(words)} words). Minimum {MemoryValidator.MIN_WORD_COUNT}.")
            
        # Check tags
        tags = metadata.get("tags", "")
        if isinstance(tags, str):
            tag_list = [t.strip() for t in tags.split(',') if t.strip()]
        elif isinstance(tags, list):
            tag_list = tags
        else:
            tag_list = []
            
        if len(tag_list) < MemoryValidator.REQUIRED_TAGS:
            errors.append(f"Missing required tags. Found {len(tag_list)}.")
            
        # Check HSL ranges if present
        if "hsl" in metadata:
            try:
                hsl_str = metadata["hsl"]
                # parse format like "[120, 70, 50]"
                clean_str = hsl_str.strip('[]')
                h, s, l = [float(x.strip()) for x in clean_str.split(',')]
                
                if not (0 <= h <= 360):
                    errors.append(f"Hue {h} out of bounds (0-360).")
                if not (0 <= s <= 100):
                    errors.append(f"Saturation {s} out of bounds (0-100).")
                if not (0 <= l <= 100):
                    errors.append(f"Lightness {l} out of bounds (0-100).")
            except Exception as e:
                errors.append(f"Invalid HSL format: {e}")
                
        return errors
