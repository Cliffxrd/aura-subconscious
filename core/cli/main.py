# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import sys
import argparse
from pathlib import Path
from core.cli.wizard import AuraWizard
from core.cli.doctor import AuraDoctor
from core.cli.scrape_wizard import AuraScrapeWizard
from core.ingestion.registry import PlatformRegistry
from core.utils.config_resolver import ConfigResolver


def main():
    """Unified CLI entrypoint for AURA."""
    parser = argparse.ArgumentParser(
        description="A.U.R.A. — Agentic Unified Recollection Archive (The Synthetic Subconscious)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # aura init
    init_parser = subparsers.add_parser(
        "init", help="Run interactive onboarding wizard"
    )
    init_parser.add_argument(
        "--non-interactive", action="store_true", help="Run in automated headless mode"
    )

    # aura scrape / aura import
    scrape_parser = subparsers.add_parser(
        "scrape", help="Run interactive chat scraping & ingestion wizard"
    )
    scrape_parser.add_argument(
        "--source",
        type=str,
        choices=["raw", "antigravity", "android-studio", "all"],
        help="Direct ingestion source",
    )
    scrape_parser.add_argument(
        "--path", type=str, help="Custom path for raw chats or brain directory"
    )

    import_parser = subparsers.add_parser(
        "import", help="Alias for `aura scrape` (Ingests chat files)"
    )
    import_parser.add_argument(
        "--source",
        type=str,
        choices=["raw", "antigravity", "android-studio", "all"],
        help="Direct ingestion source",
    )
    import_parser.add_argument(
        "--path", type=str, help="Custom path for raw chats or brain directory"
    )

    # aura doctor
    doctor_parser = subparsers.add_parser("doctor", help="Run diagnostic health checks")
    doctor_parser.add_argument("--aura-home", type=str, help="Custom AURA home path")

    # aura list-platforms
    platforms_parser = subparsers.add_parser(
        "platforms", help="List all 50+ supported AI platforms"
    )

    args = parser.parse_args()

    if args.command == "init":
        wizard = AuraWizard()
        wizard.run_wizard(interactive=not args.non_interactive)
    elif args.command in ["scrape", "import"]:
        scrape_wizard = AuraScrapeWizard()
        if args.source == "raw":
            scrape_wizard.ingest_raw_drops(
                custom_path=Path(args.path) if args.path else None
            )
        elif args.source == "antigravity":
            scrape_wizard.scrape_antigravity()
        elif args.source == "android-studio":
            scrape_wizard.scrape_android_studio()
        elif args.source == "all":
            scrape_wizard.run_full_auto_discovery()
        else:
            scrape_wizard.run_menu()
    elif args.command == "doctor":
        healthy = AuraDoctor.run_health_check(cli_override=args.aura_home)
        sys.exit(0 if healthy else 1)
    elif args.command == "platforms":
        platforms = PlatformRegistry.list_all_prefixes()
        print(
            f"\n🌐 Universal Platform Registry ({len(platforms)} Platforms Supported):\n"
        )
        for prefix, name in sorted(platforms.items()):
            print(f"  [{prefix}] {name}")
        print("")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
