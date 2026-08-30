# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import os
import sys
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from core.utils.config_resolver import ConfigResolver
from core.ingestion.registry import PlatformRegistry
from core.ingestion.raw_chat_importer import RawChatImporter
from core.ingestion.antigravity_scraper import AntigravityScraper
from core.ingestion.android_studio_scraper import AndroidStudioScraper


class AuraScrapeWizard:
    """Dedicated interactive wizard for multi-source chat scraping and transcript ingestion."""

    def __init__(self, aura_home: Optional[Path] = None):
        self.aura_home = aura_home or ConfigResolver.resolve_aura_home()
        self.rawchats_dir = self.aura_home / "documents" / "rawchats"
        self.chronicle_dir = self.aura_home / "Chronicle"
        self.chat_files_dir = self.chronicle_dir / "chat_files"
        self.chat_log_file = self.chronicle_dir / "chat_log.md"

        # Ensure directories exist
        self.rawchats_dir.mkdir(parents=True, exist_ok=True)
        self.chat_files_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_rawchats_readme()

    def _ensure_rawchats_readme(self):
        readme = self.rawchats_dir / "README.md"
        if not readme.exists():
            readme.write_text(
                "# Raw Chat Drop Directory\n\n"
                "Drop your external chat exports here to ingest them into your AURA Subconscious Mind:\n"
                "- ChatGPT exports (`conversations.json` or markdown files named `CG001.md`, etc.)\n"
                "- Claude exports (`CL001.json`, `CL002.md`, etc.)\n"
                "- DeepSeek (`DS001.json`), Cursor (`CU001.json`), or other AI transcripts.\n\n"
                "To ingest all files dropped here, run:\n"
                "```bash\n"
                "aura scrape\n"
                "# or\n"
                "aura import\n"
                "```\n",
                encoding="utf-8",
            )

    def run_menu(self):
        """Display interactive scraping wizard menu."""
        while True:
            print("\n" + "=" * 65)
            print("🌐 A.U.R.A. UNIVERSAL CHAT INGESTION & SCRAPING WIZARD")
            print("=" * 65)
            print(f"Target Subconscious Archive: {self.aura_home}\n")
            print("Select an ingestion source:")
            print("  1. 📂 Ingest Raw Chat Drops (from ~/.aura/documents/rawchats/)")
            print("  2. 🤖 Scrape Local Google Antigravity Transcripts")
            print("  3. 📱 Scrape Android Studio Gemini Chat SQLite Database")
            print("  4. 🌐 Web Browser Chat Scraper (Chrome DevTools MCP instructions)")
            print("  5. 🔍 Full Auto-Discovery (Scan & Ingest All Available Sources)")
            print("  6. 🏷️  View 52-Platform 2-Letter Prefix Registry")
            print("  0. ↩️  Exit")
            print("=" * 65)

            choice = input("\nEnter choice [1-6, 0 to exit]: ").strip()

            if choice == "1":
                self.ingest_raw_drops()
            elif choice == "2":
                self.scrape_antigravity()
            elif choice == "3":
                self.scrape_android_studio()
            elif choice == "4":
                self.show_browser_scraper_guide()
            elif choice == "5":
                self.run_full_auto_discovery()
            elif choice == "6":
                self.show_platform_registry()
            elif choice in ["0", "q", "exit"]:
                print("\n[AURA] Exiting Chat Ingestion Wizard. Stay persistent!\n")
                break
            else:
                print("\n[WARN] Invalid option. Please select 1-6 or 0.")

    def ingest_raw_drops(self, custom_path: Optional[Path] = None) -> int:
        """Ingest raw JSON/MD chat drops from documents/rawchats."""
        target_dir = custom_path or self.rawchats_dir
        print(f"\n[INGEST] Scanning raw chat drops in: {target_dir}")

        importer = RawChatImporter(
            staging_dir=target_dir, output_dir=self.chat_files_dir
        )
        records = importer.import_chats()

        if records:
            print(
                f"  [SUCCESS] Ingested {len(records)} transcripts to {self.chat_files_dir}"
            )
            self._update_chat_log(records)
        else:
            print(f"  [INFO] No new chat files found in {target_dir}.")
            print(f"  💡 Tip: Drop `.json` or `.md` chat files into:")
            print(f"       {target_dir}")
        return len(records)

    def scrape_antigravity(self) -> int:
        """Scrape local Antigravity brain transcripts."""
        print("\n[SCRAPE] Searching for Google Antigravity brain directories...")
        default_brain = Path.home() / ".gemini" / "antigravity" / "brain"

        if not default_brain.exists():
            print(
                f"  [INFO] Antigravity brain path not found at default: {default_brain}"
            )
            custom = input(
                "  Enter custom Antigravity brain path (or press Enter to skip): "
            ).strip()
            if custom:
                default_brain = Path(custom)
                if not default_brain.is_dir():
                    print(f"  [ERROR] Path is not a valid directory: {default_brain}")
                    return 0
            else:
                return 0

        scraper = AntigravityScraper(
            brain_dir=default_brain, output_dir=self.chat_files_dir
        )
        count = scraper.scrape_all()
        print(f"  [SUCCESS] Ingested {count} Antigravity transcripts (Prefix: AG###).")
        return count

    def scrape_android_studio(self) -> int:
        """Scrape Android Studio Gemini chat database."""
        print("\n[SCRAPE] Searching for Android Studio Gemini SQLite database...")
        db_path = None

        appdata = os.environ.get("APPDATA")
        if appdata:
            possible_paths = list(
                Path(appdata).glob("Google/AndroidStudio*/gemini_chat.db")
            )
            if possible_paths:
                db_path = possible_paths[0]

        if not db_path or not db_path.exists():
            print("  [INFO] Standard Android Studio database not found automatically.")
            custom = input(
                "  Enter path to gemini_chat.db (or press Enter to skip): "
            ).strip()
            if custom:
                db_path = Path(custom)
                if not db_path.is_file():
                    print(f"  [ERROR] Path is not a valid file: {db_path}")
                    return 0
            else:
                return 0

        scraper = AndroidStudioScraper(db_path=db_path, output_dir=self.chat_files_dir)
        count = scraper.scrape_all()
        print(f"  [SUCCESS] Ingested {count} Android Studio chats (Prefix: AS###).")
        return count

    def show_browser_scraper_guide(self):
        """Display instructions for interactive browser chat scraping."""
        print("\n" + "-" * 65)
        print("🌐 INTERACTIVE WEB BROWSER CHAT SCRAPER (Chrome DevTools MCP)")
        print("-" * 65)
        print("To scrape an active ChatGPT, Claude, DeepSeek, or Gemini web chat:")
        print("1. Open the chat conversation in your Chrome browser.")
        print("2. In your AI agent environment (Antigravity / Claude Code):")
        print("   Ask: 'Scrape the active browser tab into my AURA Chronicle.'")
        print("3. The agent will execute `core/ingestion/browser_scraper.py` via MCP,")
        print("   extract the DOM messages, assign the appropriate 2-letter prefix,")
        print(f"   and save the transcript to: {self.chat_files_dir}")
        print("-" * 65)

    def run_full_auto_discovery(self):
        """Run all available scrapers."""
        print("\n[AUTO-DISCOVERY] Running all scrapers across local environment...")
        raw_count = self.ingest_raw_drops()
        ag_count = self.scrape_antigravity()
        as_count = self.scrape_android_studio()
        total = raw_count + ag_count + as_count
        print(
            f"\n✨ [COMPLETED] Auto-Discovery finished! Total new transcripts indexed: {total}"
        )

    def show_platform_registry(self):
        """Display full 52-platform prefix table."""
        platforms = PlatformRegistry.list_all_prefixes()
        print(
            f"\n🌐 Universal 2-Letter Prefix Master Registry ({len(platforms)} Platforms):\n"
        )
        print(f"  {'Prefix':<8} {'Platform Name'}")
        print("  " + "-" * 40)
        for prefix, name in sorted(platforms.items()):
            print(f"  [{prefix:<4}] {name}")
        print("")

    def _update_chat_log(self, records: List[Dict[str, Any]]):
        """Append ingested records to Chronicle/chat_log.md."""
        if not self.chat_log_file.exists():
            self.chat_log_file.write_text(
                "# AURA Chronicle: Chat Log Index\n\n", encoding="utf-8"
            )

        with open(self.chat_log_file, "a", encoding="utf-8") as f:
            for rec in records:
                cid = rec.get("id", "UNKNOWN")
                meta = rec.get("metadata", {})
                date_str = meta.get("imported_at", "Unknown Date")[:10]
                summary = meta.get("summary", "Ingested chat conversation transcript.")
                f.write(f"## [{cid}] - {date_str}\n{summary}\n\n")
