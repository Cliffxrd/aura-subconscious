# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class ConfigResolver:
    """4-tier path resolution for AURA configuration."""

    @staticmethod
    def resolve_aura_home(cli_override: Optional[str] = None) -> Path:
        """Resolve the active AURA root directory via 4-tier hierarchy."""
        # Tier 1: CLI Override
        if cli_override:
            return Path(cli_override).resolve()

        # Tier 2: Environment Variable
        env_home = os.environ.get("AURA_HOME")
        if env_home:
            return Path(env_home).resolve()

        # Tier 3: aura_config.json
        config_file = Path(os.path.expanduser("~/.aura_config.json"))
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                if "aura_home" in config and config["aura_home"]:
                    return Path(config["aura_home"]).resolve()
            except json.JSONDecodeError as e:
                logger.warning(
                    f"Malformed ~/.aura_config.json detected: {e}. Falling back to default."
                )
            except Exception as e:
                logger.warning(
                    f"Error reading ~/.aura_config.json: {e}. Falling back to default."
                )

        # Tier 4: Default fallback (~/.aura)
        return ConfigResolver.get_default_home()

    @staticmethod
    def get_default_home() -> Path:
        """Get standard ~/.aura path."""
        return Path(os.path.expanduser("~/.aura")).resolve()

    @staticmethod
    def load_config(aura_home: Path) -> Dict[str, Any]:
        """Load optional configuration from ~/.aura/config/aura_config.json."""
        config_path = aura_home / "config" / "aura_config.json"
        if not config_path.exists():
            return {}
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.warning(f"Malformed config file at {config_path}: {e}")
            return {}
        except Exception as e:
            logger.warning(f"Could not load config file at {config_path}: {e}")
            return {}
