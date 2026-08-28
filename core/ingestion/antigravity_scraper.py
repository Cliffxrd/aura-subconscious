import os
from pathlib import Path
from typing import List

class AntigravityScraper:
    """Parses Google Antigravity transcripts."""
    
    def __init__(self, brain_dir: Path):
        self.brain_dir = brain_dir
        
    def scrape(self) -> List[dict]:
        """Scrape transcript.jsonl files from the brain directory."""
        transcripts = []
        if not self.brain_dir.exists():
            return transcripts
            
        for root, _, files in os.walk(self.brain_dir):
            for file in files:
                if file == "transcript.jsonl":
                    transcripts.append({
                        "source": "Antigravity",
                        "path": os.path.join(root, file)
                    })
        return transcripts
