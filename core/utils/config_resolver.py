# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any


class ConfigResolver:
    """4-tier path resolution for AURA configuration."""

    @staticmethod
    def resolve_aura_home(cli_override: Optional[str] = None) -> Path:
        # Tier 1: CLI Override
        if cli_override:
            return Path(cli_override)

        # Tier 2: Environment Variable
        env_home = os.environ.get("AURA_HOME")
        if env_home:
            return Path(env_home)

        # Tier 3: aura_config.json
        config_file = Path(os.path.expanduser("~/.aura_config.json"))
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                if "aura_home" in config:
                    return Path(config["aura_home"])
            except json.JSONDecodeError:
                pass

        # Tier 4: Default fallback
        return Path(os.path.expanduser("~/.aura"))

    @staticmethod
    def load_config(aura_home: Path) -> Dict[str, Any]:
        config_path = aura_home / "config" / "aura_config.json"
        if not config_path.exists():
            return {}
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
