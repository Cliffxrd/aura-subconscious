# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import sys
import argparse
import logging
from typing import Optional
from core.cli.wizard import AuraWizard
from core.cli.doctor import AuraDoctor
from core.cli.scrape_wizard import AuraScrapeWizard
from core.circadian.heartbeat import CircadianHeartbeat
from core.ingestion.registry import PlatformRegistry
from core import __version__

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="aura",
        description=f"AURA: Agentic Unified Recollection Archive CLI (v{__version__})",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    # 1. aura init
    subparsers.add_parser("init", help="Run interactive setup & personalization wizard")

    # 2. aura doctor
    subparsers.add_parser("doctor", help="Run system diagnostics and health checks")

    # 3. aura scrape / aura import
    scrape_p = subparsers.add_parser(
        "scrape", help="Launch chat scraper & ingestion engine"
    )
    scrape_p.add_argument(
        "--source",
        choices=["all", "raw", "antigravity", "android-studio"],
        default=None,
        help="Specify source to scrape directly",
    )

    import_p = subparsers.add_parser("import", help="Alias for 'scrape'")
    import_p.add_argument(
        "--source",
        choices=["all", "raw", "antigravity", "android-studio"],
        default=None,
        help="Specify source to import directly",
    )

    # 4. aura heartbeat
    subparsers.add_parser(
        "heartbeat", help="Trigger Heather's Circadian sweep and triage consolidation"
    )

    # 5. aura platforms
    subparsers.add_parser(
        "platforms", help="List all 50+ supported AI platform ID prefixes"
    )

    return parser


def main() -> None:
    """Main CLI execution entrypoint with global error boundary."""
    try:
        parser = build_parser()
        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            sys.exit(0)

        if args.command == "init":
            wizard = AuraWizard()
            wizard.run(interactive=True)
        elif args.command == "doctor":
            doctor = AuraDoctor()
            success = doctor.run_diagnostics()
            sys.exit(0 if success else 1)
        elif args.command in ["scrape", "import"]:
            scrape_wiz = AuraScrapeWizard()
            if args.source:
                scrape_wiz.run_direct_source(args.source)
            else:
                scrape_wiz.run_interactive()
        elif args.command == "heartbeat":
            heartbeat = CircadianHeartbeat()
            heartbeat.run_heartbeat()
        elif args.command == "platforms":
            platforms = PlatformRegistry.list_platforms()
            print("\n" + "=" * 65)
            print("🌐 AURA UNIVERSAL 50+ AI PLATFORM REGISTRY")
            print("=" * 65)
            for p in sorted(platforms, key=lambda x: x["prefix"]):
                print(f"  [{p['prefix']}] {p['name']:<28} ({p['category']})")
            print("=" * 65 + "\n")
    except KeyboardInterrupt:
        print("\n\n[AURA] Operation canceled by user. Exiting cleanly.\n")
        sys.exit(130)
    except Exception as e:
        print(f"\n[AURA ERROR] Fatal execution failure: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
