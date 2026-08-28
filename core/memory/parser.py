import re
from typing import Dict, Any, Tuple, List

class MemoryParser:
    """Parses AURA memory markdown files (YAML frontmatter & content)."""
    
    FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)', re.DOTALL)
    
    @staticmethod
    def parse_file(content: str) -> Tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter and markdown content."""
        match = MemoryParser.FRONTMATTER_PATTERN.match(content)
        metadata = {}
        body = content
        
        if match:
            frontmatter_str = match.group(1)
            body = match.group(2)
            # Basic YAML parser fallback for common key-value pairs
            for line in frontmatter_str.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    metadata[key.strip()] = val.strip()
                    
        return metadata, body
        
    @staticmethod
    def extract_bullets(content: str) -> List[str]:
        """Extract bullet points as a fallback for structural parsing."""
        bullets = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('- ') or line.startswith('* '):
                bullets.append(line[2:].strip())
        return bullets
