import re
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional

class MemoryParser:
    """Parses AURA memory markdown files (YAML frontmatter & content)."""
    
    FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)', re.DOTALL)
    
    @classmethod
    def parse(cls, file_path: Path) -> Dict[str, Any]:
        """Read and parse a memory file from disk into a unified memory dictionary."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            metadata, body = cls.parse_file(content)
            result = dict(metadata)
            result["content"] = body.strip()
            result["file_name"] = file_path.name
            result["path"] = str(file_path)
            
            # Ensure id exists
            if "id" not in result:
                result["id"] = file_path.stem
                
            return result
        except Exception as e:
            return {"error": str(e), "file_name": file_path.name}

    @classmethod
    def parse_file(cls, content: str) -> Tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter and markdown content."""
        match = cls.FRONTMATTER_PATTERN.match(content)
        metadata: Dict[str, Any] = {}
        body = content
        
        if match:
            frontmatter_str = match.group(1)
            body = match.group(2)
            metadata = cls._parse_yaml(frontmatter_str)
            
        return metadata, body.strip()

    @staticmethod
    def _parse_yaml(yaml_str: str) -> Dict[str, Any]:
        """Pure-Python YAML parser supporting key-values, lists, and nested lists."""
        metadata: Dict[str, Any] = {}
        current_list_key = None
        
        for line in yaml_str.split('\n'):
            line_str = line.strip()
            if not line_str or line_str.startswith('#'):
                continue
                
            if line_str.startswith('- ') and current_list_key:
                val = line_str[2:].strip().strip('"\'')
                if isinstance(metadata.get(current_list_key), list):
                    metadata[current_list_key].append(val)
            elif ':' in line_str:
                key, val = line_str.split(':', 1)
                key = key.strip()
                val = val.strip().strip('"\'')
                
                if not val:
                    metadata[key] = []
                    current_list_key = key
                else:
                    current_list_key = None
                    if val.startswith('[') and val.endswith(']'):
                        items = [i.strip().strip('"\'') for i in val[1:-1].split(',') if i.strip()]
                        metadata[key] = items
                    else:
                        metadata[key] = val
                        
        return metadata
        
    @staticmethod
    def extract_bullets(content: str) -> List[str]:
        """Extract bullet points robustly from markdown content."""
        bullets = []
        for line in content.split('\n'):
            stripped = line.lstrip()
            if stripped.startswith('- ') or stripped.startswith('* '):
                bullets.append(stripped[2:].strip())
        return bullets

