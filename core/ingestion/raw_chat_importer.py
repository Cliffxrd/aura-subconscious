from pathlib import Path
from typing import List

class RawChatImporter:
    """Importer for raw chat drops (CG###, CL###)."""
    
    def __init__(self, staging_dir: Path):
        self.staging_dir = staging_dir
        
    def import_chats(self) -> List[str]:
        """Import markdown files from staging."""
        imported = []
        if not self.staging_dir.exists():
            return imported
            
        for file in self.staging_dir.glob("*.md"):
            imported.append(file.name)
        return imported
