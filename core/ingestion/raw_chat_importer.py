import json
import logging
import shutil
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class RawChatImporter:
    """Importer for raw chat drops (CG###, CL###) supporting JSON and Markdown formats."""
    
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
                    logger.info(f"Skipping unsupported file type: {file_path}")
                    continue
                    
                if record:
                    self._archive_file(file_path, record["id"])
                    imported_records.append(record)
                    
            except Exception as e:
                logger.error(f"Failed to import {file_path}: {e}")
                
        return imported_records

    def _process_markdown(self, file_path: Path) -> Dict[str, Any]:
        """Parses a markdown chat drop, extracting simple metadata and content."""
        content = file_path.read_text(encoding="utf-8")
        chat_id = file_path.stem.upper()
        
        # Super simple frontmatter extraction fallback if memory/parser isn't injected
        metadata = {"original_format": "markdown", "imported_at": datetime.utcnow().isoformat()}
        
        output_file = self.output_dir / f"{chat_id}.json"
        record = {
            "id": chat_id,
            "metadata": metadata,
            "content": content
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)
            
        return record

    def _process_json(self, file_path: Path) -> Dict[str, Any]:
        """Parses a JSON chat drop and standardizes it."""
        chat_id = file_path.stem.upper()
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        record = {
            "id": chat_id,
            "metadata": data.get("metadata", {"original_format": "json"}),
            "content": data.get("content", str(data)),
            "imported_at": datetime.utcnow().isoformat()
        }
        
        output_file = self.output_dir / f"{chat_id}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)
            
        return record

    def _archive_file(self, file_path: Path, chat_id: str):
        """Moves processed files into an archive directory."""
        archive_dir = self.staging_dir / "archived"
        archive_dir.mkdir(exist_ok=True)
        dest = archive_dir / f"{chat_id}{file_path.suffix}"
        shutil.move(str(file_path), str(dest))
        logger.info(f"Archived {file_path.name} to {dest.name}")
