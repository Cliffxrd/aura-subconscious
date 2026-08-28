from pathlib import Path
from core.utils.config_resolver import ConfigResolver

def test_resolve_aura_home():
    # Test fallback
    path = ConfigResolver.resolve_aura_home()
    assert path is not None
    
    # Test CLI override
    override_path = ConfigResolver.resolve_aura_home(cli_override="/tmp/aura")
    assert override_path == Path("/tmp/aura")

