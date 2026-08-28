from core.ingestion.registry import PlatformRegistry

def test_get_platform_name():
    assert PlatformRegistry.get_platform_name("AG") == "Google Antigravity"
    assert PlatformRegistry.get_platform_name("AS") == "Android Studio Gemini"
    assert PlatformRegistry.get_platform_name("CG") == "OpenAI ChatGPT"
    assert PlatformRegistry.get_platform_name("CL") == "Anthropic Claude Web / Artifacts"
    assert PlatformRegistry.get_platform_name("UNKNOWN") == "Unknown Platform"
    
def test_is_valid_prefix():
    assert PlatformRegistry.is_valid_prefix("AG") is True
    assert PlatformRegistry.is_valid_prefix("CU") is True
    assert PlatformRegistry.is_valid_prefix("CL") is True
    assert PlatformRegistry.is_valid_prefix("ZZ") is False

def test_list_all_prefixes():
    all_prefixes = PlatformRegistry.list_all_prefixes()
    assert len(all_prefixes) >= 50
    assert "AG" in all_prefixes
    assert "GC" in all_prefixes

