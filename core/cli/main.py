import sys
import argparse
from core.cli.wizard import AuraWizard
from core.cli.doctor import AuraDoctor
from core.ingestion.registry import PlatformRegistry
from core.utils.config_resolver import ConfigResolver

def main():
    """Unified CLI entrypoint for AURA."""
    parser = argparse.ArgumentParser(
        description="A.U.R.A. — Agentic Unified Recollection Archive (The Synthetic Subconscious)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # aura init
    init_parser = subparsers.add_parser("init", help="Run interactive onboarding wizard")
    init_parser.add_argument("--non-interactive", action="store_true", help="Run in automated headless mode")
    
    # aura doctor
    doctor_parser = subparsers.add_parser("doctor", help="Run diagnostic health checks")
    doctor_parser.add_argument("--aura-home", type=str, help="Custom AURA home path")
    
    # aura list-platforms
    platforms_parser = subparsers.add_parser("platforms", help="List all 50+ supported AI platforms")
    
    args = parser.parse_args()
    
    if args.command == "init":
        wizard = AuraWizard()
        wizard.run_wizard(interactive=not args.non_interactive)
    elif args.command == "doctor":
        healthy = AuraDoctor.run_health_check(cli_override=args.aura_home)
        sys.exit(0 if healthy else 1)
    elif args.command == "platforms":
        platforms = PlatformRegistry.list_all_prefixes()
        print(f"\n🌐 Universal Platform Registry ({len(platforms)} Platforms Supported):\n")
        for prefix, name in sorted(platforms.items()):
            print(f"  [{prefix}] {name}")
        print("")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

