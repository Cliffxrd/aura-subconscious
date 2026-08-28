"""
AURA Universal Platform Registry
Standardized 2-Letter Uppercase Prefix System ([A-Z]{2}) for 50+ AI Platforms and ACP Agents.
"""

from typing import Dict, Any, Optional

class PlatformRegistry:
    """Universal 50+ AI platform 2-letter prefix master registry."""
    
    PLATFORMS: Dict[str, Dict[str, Any]] = {
        # Autonomous Agent IDEs & Coding Environments
        "AG": {"name": "Google Antigravity", "category": "Autonomous Agent IDE", "default_ext": "md"},
        "AS": {"name": "Android Studio Gemini", "category": "IDE Assistant", "default_ext": "db"},
        "CA": {"name": "Claude Agent (Anthropic)", "category": "Autonomous Agent", "default_ext": "json"},
        "CX": {"name": "OpenAI Codex / ACP", "category": "Autonomous Agent", "default_ext": "json"},
        "CR": {"name": "Corust Agent (Rust)", "category": "Agentic Coding IDE", "default_ext": "json"},
        "CU": {"name": "Cursor IDE", "category": "Agentic Coding IDE", "default_ext": "sqlite"},
        "CN": {"name": "Cline Bot", "category": "Autonomous Agent CLI", "default_ext": "json"},
        "GC": {"name": "GitHub Copilot / Workspace", "category": "IDE Copilot", "default_ext": "json"},
        "JU": {"name": "Junie (JetBrains)", "category": "IDE Native Agent", "default_ext": "json"},
        "WS": {"name": "Windsurf (Codeium)", "category": "Agentic Flow IDE", "default_ext": "json"},
        "DV": {"name": "Devin (Cognition)", "category": "Autonomous Software Engineer", "default_ext": "json"},
        "RP": {"name": "Replit Agent", "category": "Cloud Agent & IDE", "default_ext": "json"},
        "AR": {"name": "Agoragentic (ACRE)", "category": "Agent Marketplace", "default_ext": "json"},
        "AU": {"name": "Auggie CLI (Augment)", "category": "Agent CLI", "default_ext": "json"},
        "AH": {"name": "Autohand Code", "category": "AI Coding Agent", "default_ext": "json"},
        "CB": {"name": "Codebuddy (Tencent Cloud)", "category": "Intelligent Coding Tool", "default_ext": "json"},
        "CT": {"name": "Cortex Code (Snowflake)", "category": "Enterprise Coding Agent", "default_ext": "json"},
        "CW": {"name": "crow-cli", "category": "ACP Native Agent", "default_ext": "json"},
        "DA": {"name": "DeepAgents (LangChain)", "category": "Agent Framework", "default_ext": "json"},
        "DM": {"name": "DimCode (ArcShips)", "category": "Multi-Model Agent", "default_ext": "json"},
        "DC": {"name": "Dirac (Delta Labs)", "category": "Optimized Coding Agent", "default_ext": "json"},
        "FD": {"name": "Factory Droid", "category": "Enterprise AI Agent", "default_ext": "json"},
        "FA": {"name": "fast-agent", "category": "Multi-Provider Agent", "default_ext": "json"},
        "GM": {"name": "Gemini CLI", "category": "CLI Assistant", "default_ext": "json"},
        "GO": {"name": "goose (Block)", "category": "Open-Source Extensible Agent", "default_ext": "json"},
        "GB": {"name": "Grok Build (xAI)", "category": "Coding Agent & CLI", "default_ext": "json"},
        "KL": {"name": "Kilo Code", "category": "Open-Source Coding Agent", "default_ext": "json"},
        "KM": {"name": "Kimi CLI (Moonshot AI)", "category": "Long-Context Agent", "default_ext": "json"},
        "MC": {"name": "Minion Code (femto)", "category": "Coding Assistant", "default_ext": "json"},
        "MV": {"name": "Mistral Vibe", "category": "Open-Source Assistant", "default_ext": "json"},
        "NV": {"name": "Nova (Compass AI)", "category": "Autonomous Software Engineer", "default_ext": "json"},
        "OC": {"name": "OpenCode (Anomaly)", "category": "Open-Source Coding Agent", "default_ext": "json"},
        "PA": {"name": "pi ACP", "category": "ACP Adapter Agent", "default_ext": "json"},
        "PS": {"name": "Poolside", "category": "Foundation Coding Agent", "default_ext": "json"},
        "QD": {"name": "Qoder CLI", "category": "Agentic Coding CLI", "default_ext": "json"},
        "QW": {"name": "Qwen Code (Alibaba)", "category": "Open Weights Coding Agent", "default_ext": "json"},
        "SG": {"name": "siGit Code", "category": "Local-First Coding Agent", "default_ext": "json"},
        "SP": {"name": "Stakpak", "category": "Rust DevOps Agent", "default_ext": "json"},

        # Frontier Web & Conversational LLMs
        "CG": {"name": "OpenAI ChatGPT", "category": "Frontier Web / Desktop", "default_ext": "json"},
        "CL": {"name": "Anthropic Claude Web / Artifacts", "category": "Frontier Web", "default_ext": "json"},
        "XG": {"name": "Google Gemini Web", "category": "Frontier Web", "default_ext": "json"},
        "DS": {"name": "DeepSeek (V3 / R1)", "category": "Frontier Web / Coder", "default_ext": "json"},
        "PX": {"name": "Perplexity AI", "category": "Conversational Search", "default_ext": "json"},
        "ML": {"name": "Mistral Le Chat", "category": "Frontier Web", "default_ext": "json"},
        "GK": {"name": "xAI Grok Web", "category": "Frontier Web", "default_ext": "json"},
        "VO": {"name": "v0 by Vercel", "category": "Generative UI Agent", "default_ext": "json"},
        "PO": {"name": "Poe (Quora)", "category": "Multi-Bot Hub", "default_ext": "json"},
        "GS": {"name": "Google AI Studio", "category": "Prompt Prototyping Lab", "default_ext": "json"},

        # Local Inference & Offline Hubs
        "OL": {"name": "Ollama", "category": "Local LLM Runner & CLI", "default_ext": "json"},
        "LM": {"name": "LM Studio", "category": "Local LLM GUI", "default_ext": "json"},
        "HC": {"name": "HuggingChat", "category": "Open LLM Web Hub", "default_ext": "json"},
        "PC": {"name": "Pieces for Developers", "category": "Workstream Context AI", "default_ext": "json"}
    }
    
    @classmethod
    def get_platform(cls, prefix: str) -> Optional[Dict[str, Any]]:
        return cls.PLATFORMS.get(prefix.upper())
        
    @classmethod
    def get_platform_name(cls, prefix: str) -> str:
        platform = cls.PLATFORMS.get(prefix.upper())
        return platform["name"] if platform else "Unknown Platform"
        
    @classmethod
    def is_valid_prefix(cls, prefix: str) -> bool:
        return prefix.upper() in cls.PLATFORMS

    @classmethod
    def list_all_prefixes(cls) -> Dict[str, str]:
        return {k: v["name"] for k, v in cls.PLATFORMS.items()}

