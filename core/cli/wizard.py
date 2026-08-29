# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import os
import shutil
from pathlib import Path
from typing import Dict, Any, List
from core.utils.config_resolver import ConfigResolver


class AuraWizard:
    """Interactive `aura init` onboarding wizard and environment deployer."""

    def __init__(self, target_home: Path = None):
        self.target_home = target_home or ConfigResolver.resolve_aura_home()
        self.companion_name = "Aura"
        self.user_name = "Partner"
        self.tech_stack = "Kotlin, Jetpack Compose, Python, TypeScript"
        self.communication_style = (
            "High-bandwidth, collaborative, concise, no robotic filler"
        )
        self.selected_platforms = ["Gemini", "Claude", "Cursor", "Copilot"]

    def run_wizard(self, interactive: bool = True):
        """Run the full onboarding questionnaire and deployment."""
        print("\n" + "=" * 60)
        print("🌌 WELCOME TO A.U.R.A.")
        print("   Agentic Unified Recollection Archive: The Synthetic Subconscious")
        print("=" * 60 + "\n")

        if interactive:
            # 1. User Persona Setup
            inp_user = input(
                f"? Your Name / GitHub Handle (Default: Cliffxrd): "
            ).strip()
            if inp_user:
                self.user_name = inp_user

            # 2. Companion Name
            print("\n? Choose your Companion Agent Identity:")
            print("  1. Aura (Default - The Ambient Engineering Partner)")
            print("  2. Custom Name (e.g. Jarvis, Nova, Athena)")
            choice = input("  Select (1/2, default 1): ").strip()
            if choice == "2":
                custom = input("  Enter companion name: ").strip()
                if custom:
                    self.companion_name = custom

            # 3. Preferred Tech Stack
            inp_stack = input(
                f"\n? Preferred Tech Stack (Default: {self.tech_stack}): "
            ).strip()
            if inp_stack:
                self.tech_stack = inp_stack

            # 4. Communication Style
            inp_style = input(
                f"\n? Communication Style (Default: {self.communication_style}): "
            ).strip()
            if inp_style:
                self.communication_style = inp_style

        # 5. Initialize Directory Architecture
        self.scaffold_directories()

        # 6. Hydrate Templates
        self.hydrate_templates()

        # 7. Seed Starter Memories
        self.seed_starter_memories()

        # 8. Deploy IDE Root Rules
        self.deploy_rules()

        # 9. Optional Private Git Synchronization (Skippable)
        if interactive:
            print("\n? Multi-Device Memory Sync & Private Backup (Optional):")
            print(f"  AURA stores all memories 100% locally in: {self.target_home}")
            print(
                "  There are zero central servers. You can optionally initialize Git to track your private archive."
            )
            git_choice = (
                input(
                    "  Initialize Git inside ~/.aura for private version control? [y/N]: "
                )
                .strip()
                .lower()
            )
            if git_choice in ["y", "yes"]:
                self.init_git_repo()

        print("\n" + "=" * 60)
        print(f"✨ AURA SUCCESSFULLY INITIALIZED at: {self.target_home}")
        print(f"   Companion Name: {self.companion_name}")
        print(f"   Run `aura doctor` to verify system health.")
        print("=" * 60 + "\n")

    def init_git_repo(self):
        """Optionally initialize a Git repository inside the user's AURA_HOME."""
        try:
            import subprocess

            if not (self.target_home / ".git").exists():
                subprocess.run(
                    ["git", "init"],
                    cwd=str(self.target_home),
                    check=True,
                    capture_output=True,
                )
                user_gitignore = self.target_home / ".gitignore"
                if not user_gitignore.exists():
                    user_gitignore.write_text(
                        "Cortex/current_thoughts.md\n__pycache__/\n*.tmp\n",
                        encoding="utf-8",
                    )
                print(
                    f"  [PASS] Initialized private Git repository in: {self.target_home}"
                )
                print(
                    "  💡 Tip: Link your own private GitHub remote to sync memories across devices:"
                )
                print(
                    "       cd ~/.aura && git add . && git commit -m 'feat: initial memory archive'"
                )
            else:
                print(f"  [INFO] Git repository already exists in: {self.target_home}")
        except Exception as e:
            print(f"  [WARN] Could not initialize Git in {self.target_home}: {e}")

    def scaffold_directories(self):
        """Create biological brain structure."""
        dirs = [
            "Cortex",
            "Hippocampus/triage",
            "Amygdala",
            "Circadian",
            "Chronicle/chat_files",
            "Context",
            "Personas",
            "Heritage",
            "config",
            "documents/rawchats",
        ]
        for d in dirs:
            (self.target_home / d).mkdir(parents=True, exist_ok=True)

        rawchats_readme = self.target_home / "documents" / "rawchats" / "README.md"
        if not rawchats_readme.exists():
            rawchats_readme.write_text(
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

    def hydrate_templates(self):
        """Copy and populate templates into user instance."""
        repo_root = Path(__file__).resolve().parent.parent.parent
        templates_dir = repo_root / "templates"

        # 1. PersonalContext.md
        context_file = self.target_home / "Context" / "PersonalContext.md"
        if not context_file.exists():
            content = f"""# {self.companion_name} Mind: Personal Context

## 1. Active Profile
* **Name / Persona**: {self.user_name}
* **Companion Name**: {self.companion_name}
* **Preferred Tech Stack**: {self.tech_stack}
* **Communication Style**: {self.communication_style}
* **Productivity & Cadence**: Night owl / flow state.

## 2. Core Directives
* Zero placeholder comments (`// TODO`).
* Maintain persistent cognitive continuity across sessions.
"""
            with open(context_file, "w", encoding="utf-8") as f:
                f.write(content)

        # 2. RequestedMemories.md
        req_file = self.target_home / "Context" / "RequestedMemories.md"
        if not req_file.exists():
            with open(req_file, "w", encoding="utf-8") as f:
                f.write(
                    "# Requested Memories (Tier 1 Directives)\n- MEM_001\n- MEM_002\n"
                )

        # 3. Topics.md & FrequentTasks.md
        topics_file = self.target_home / "Context" / "Topics.md"
        if not topics_file.exists():
            with open(topics_file, "w", encoding="utf-8") as f:
                f.write(
                    "# Topics Index\n\n## #Architecture\n\n## #Kotlin\n\n## #Compose\n\n## #Agents\n"
                )

        tasks_file = self.target_home / "Context" / "FrequentTasks.md"
        if not tasks_file.exists():
            with open(tasks_file, "w", encoding="utf-8") as f:
                f.write(
                    "# Frequent Tasks\n\n- Refactoring & Clean Architecture\n- Subconscious Memory Consolidation\n"
                )

    def seed_starter_memories(self):
        """Seed Hippocampus with universal engineering starter pack."""
        repo_root = Path(__file__).resolve().parent.parent.parent
        starter_dir = repo_root / "Extras" / "starter_memories"
        dest_hippocampus = self.target_home / "Hippocampus"

        if starter_dir.exists():
            for mem_file in starter_dir.glob("*.md"):
                shutil.copy(mem_file, dest_hippocampus / mem_file.name)

    def deploy_rules(self):
        """Deploy cross-platform rule files."""
        repo_root = Path(__file__).resolve().parent.parent.parent
        rules_dir = repo_root / "templates" / "rules"

        replacements = {
            "{{AGENT_NAME}}": self.companion_name,
            "{{AURA_HOME}}": str(self.target_home).replace("\\", "/"),
        }

        # 1. Gemini rule
        gemini_tpl = rules_dir / "GEMINI.md.template"
        if gemini_tpl.exists():
            dest = Path.home() / ".gemini" / "GEMINI.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(gemini_tpl, "r", encoding="utf-8") as f:
                content = f.read()
            for k, v in replacements.items():
                content = content.replace(k, v)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(content)

        # 2. Claude rule
        claude_tpl = rules_dir / "CLAUDE.md.template"
        if claude_tpl.exists():
            dest = Path.home() / ".claude" / "CLAUDE.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(claude_tpl, "r", encoding="utf-8") as f:
                content = f.read()
            for k, v in replacements.items():
                content = content.replace(k, v)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(content)
