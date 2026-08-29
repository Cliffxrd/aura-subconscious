# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import os
import shutil
from pathlib import Path
from core.utils.config_resolver import ConfigResolver


class AuraWizard:
    """Interactive setup wizard to initialize and personalize AURA."""

    AVAILABLE_SUBAGENTS = [
        {
            "id": 1,
            "name": "Heather",
            "emoji": "🧭",
            "role": "Proactive Ecosystem Caretaker & Circadian Heartbeat",
            "desc": "Manages 3 PM triage sweeps, memory repair, and health protocols.",
            "recommended": True,
        },
        {
            "id": 2,
            "name": "Mike",
            "emoji": "⚙️ ",
            "role": "Production Workhorse & Systems Stability Specialist",
            "desc": "High-reliability code, robust error boundaries, and flight checks.",
            "recommended": True,
        },
        {
            "id": 3,
            "name": "Diana",
            "emoji": "🎨",
            "role": "Visionary UX/UI Designer & Brand Styling Architect",
            "desc": "Modern UI, responsive layouts, design tokens, and aesthetic polish.",
            "recommended": True,
        },
        {
            "id": 4,
            "name": "Miranda",
            "emoji": "🔍",
            "role": "Perfectionist Fact-Checker & Quality Gatekeeper",
            "desc": "Zero-tolerance audits, code verification, and empirical testing.",
            "recommended": True,
        },
        {
            "id": 5,
            "name": "Ben",
            "emoji": "🛡️ ",
            "role": "OCD Code Quality Watchdog & Decoupling Specialist",
            "desc": "Path normalization, architectural boundaries, and refactoring.",
            "recommended": True,
        },
        {
            "id": 6,
            "name": "Alex",
            "emoji": "📢",
            "role": "DevRel, Marketing & Technical Showcase Curator",
            "desc": "High-impact READMEs, case studies, release notes, and architecture charts.",
            "recommended": False,
        },
        {
            "id": 7,
            "name": "James",
            "emoji": "🔒",
            "role": "Security, Auth & Zero-Trust Compliance Guardian",
            "desc": "Firestore rules, Intent security, credential scanning, and auth flows.",
            "recommended": False,
        },
        {
            "id": 8,
            "name": "Ryan",
            "emoji": "🚀",
            "role": "DevOps, Multiplatform CI/CD & Platform Engineer",
            "desc": "GitHub Actions workflows, build speed tuning, and release pipelines.",
            "recommended": False,
        },
        {
            "id": 9,
            "name": "Taylor",
            "emoji": "📚",
            "role": "Documentation Architect & API Scribe",
            "desc": "KDoc & Dokka API documentation, interactive recipe cookbooks, and ADRs.",
            "recommended": False,
        },
        {
            "id": 10,
            "name": "Tessa",
            "emoji": "🧪",
            "role": "Automated QA & Test Matrix Commander",
            "desc": "Exhaustive golden screenshot suites, Turbine assertions, and stress tests.",
            "recommended": False,
        },
    ]

    def __init__(self, target_home: Path = None):
        self.target_home = target_home or ConfigResolver.get_default_home()
        self.user_name = "Cliffxrd"
        self.companion_name = "Aura"
        self.tech_stack = "Kotlin Multiplatform, Jetpack Compose, Python, Firebase"
        self.communication_style = "Crisp, architectural, zero-fluff, empathetic"
        self.selected_subagent_ids = [1, 2, 3, 4, 5]

    def run(self, interactive: bool = True):
        """Execute the bootstrap initialization workflow."""
        print("\n" + "=" * 65)
        print("🌌 WELCOME TO A.U.R.A. (The Synthetic Subconscious)")
        print("=" * 65 + "\n")

        if interactive:
            # 1. User Persona Setup
            inp_user = input(
                f"? Your Name / GitHub Handle (Default: {self.user_name}): "
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

            # 5. Subagent Roster Selection
            self.prompt_subagent_roster()

        # 6. Initialize Directory Architecture
        self.scaffold_directories()

        # 7. Hydrate Templates
        self.hydrate_templates()

        # 8. Scaffold Selected Subagent Personas
        self.scaffold_subagents()

        # 9. Seed Starter Memories
        self.seed_starter_memories()

        # 10. Deploy IDE Root Rules
        self.deploy_rules()

        # 11. Optional Private Git Synchronization (Skippable)
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

        print("\n" + "=" * 65)
        print(f"✨ AURA SUCCESSFULLY INITIALIZED at: {self.target_home}")
        print(f"   Companion Name: {self.companion_name}")
        print(f"   Subagent Personas: {len(self.selected_subagent_ids)} active")
        print("   Run `aura doctor` to verify system health.")
        print("=" * 65 + "\n")

    def prompt_subagent_roster(self):
        """Interactive prompt for selecting subagent roster."""
        print("\n" + "=" * 65)
        print("👥 STEP 5: SELECT YOUR A.U.R.A. SUBAGENT ROSTER")
        print("=" * 65)
        print("Choose which specialized autonomous personas to scaffold into your")
        print(f"active subconscious archive ({self.target_home}/Personas/):\n")

        print("[★] RECOMMENDED CORE SQUAD (Enabled by default):")
        for agent in self.AVAILABLE_SUBAGENTS[:5]:
            print(
                f"  [X] {agent['id']}. {agent['emoji']} {agent['name']:<8} — {agent['role']}"
            )
            print(f"       └─ {agent['desc']}")

        print("\n[+] SPECIALIZED DOMAIN EXPANSIONS:")
        for agent in self.AVAILABLE_SUBAGENTS[5:]:
            print(
                f"  [ ] {agent['id']}. {agent['emoji']} {agent['name']:<8} — {agent['role']}"
            )
            print(f"       └─ {agent['desc']}")

        print("\n" + "-" * 65)
        print("Selection Options:")
        print("  • Press [ENTER] to install Recommended Core Squad (1-5)")
        print("  • Type 'all' to install all 10 subagents")
        print(
            "  • Enter comma-separated numbers/ranges (e.g. '1,2,3,4,5,8,9,10' or '1-5,9')"
        )
        print("-" * 65)

        raw = input("Your Choice [1-5]: ").strip().lower()
        if not raw or raw == "default":
            self.selected_subagent_ids = [1, 2, 3, 4, 5]
        elif raw == "all":
            self.selected_subagent_ids = list(range(1, 11))
        else:
            selected = set()
            parts = raw.split(",")
            for part in parts:
                part = part.strip()
                if "-" in part:
                    try:
                        start, end = map(int, part.split("-"))
                        for i in range(start, end + 1):
                            if 1 <= i <= 10:
                                selected.add(i)
                    except ValueError:
                        pass
                else:
                    try:
                        val = int(part)
                        if 1 <= val <= 10:
                            selected.add(val)
                    except ValueError:
                        pass
            self.selected_subagent_ids = (
                sorted(list(selected)) if selected else [1, 2, 3, 4, 5]
            )

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

    def scaffold_subagents(self):
        """Copy selected subagent personas into user Personas/ directory."""
        repo_root = Path(__file__).resolve().parent.parent.parent
        tpl_personas = repo_root / "templates" / "Personas"
        dest_personas = self.target_home / "Personas"
        dest_personas.mkdir(parents=True, exist_ok=True)

        for agent in self.AVAILABLE_SUBAGENTS:
            if agent["id"] in self.selected_subagent_ids:
                name = agent["name"]

                # Copy YAML manifest
                yaml_file = tpl_personas / f"{name}.agent.yaml"
                if yaml_file.exists():
                    shutil.copy(yaml_file, dest_personas / f"{name}.agent.yaml")

                # Scaffold directory structure
                agent_dir = dest_personas / name
                agent_dir.mkdir(parents=True, exist_ok=True)
                (agent_dir / "Diary").mkdir(exist_ok=True)

                src_agent_dir = tpl_personas / name
                if src_agent_dir.exists():
                    for item in src_agent_dir.glob("*"):
                        if item.is_file():
                            shutil.copy(item, agent_dir / item.name)

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
                print(
                    f"  [SUCCESS] Initialized private Git repository in: {self.target_home}"
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
