# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

from core.ingestion.registry import PlatformRegistry


def test_get_platform_name():
    assert PlatformRegistry.get_platform_name("AG") == "Google Antigravity"
    assert (
        PlatformRegistry.get_platform_name("CL") == "Anthropic Claude Web / Artifacts"
    )
    assert PlatformRegistry.get_platform_name("ZZ") == "Unknown Platform"
    # Null and type boundary checks
    assert PlatformRegistry.get_platform_name(None) == "Unknown Platform"
    assert PlatformRegistry.get_platform_name(123) == "Unknown Platform"


def test_is_valid_prefix():
    assert PlatformRegistry.is_valid_prefix("AG") is True
    assert PlatformRegistry.is_valid_prefix("cg") is True
    assert PlatformRegistry.is_valid_prefix("ZZ") is False
    # Null and type boundary checks
    assert PlatformRegistry.is_valid_prefix(None) is False
    assert PlatformRegistry.is_valid_prefix(99) is False


def test_list_all_prefixes():
    prefixes = PlatformRegistry.list_all_prefixes()
    assert isinstance(prefixes, dict)
    assert "AG" in prefixes
    assert "CG" in prefixes
    assert len(prefixes) >= 50


def test_boundary_states_registry():
    assert PlatformRegistry.get_platform_name(None) == "Unknown Platform"
    assert PlatformRegistry.is_valid_prefix(None) is False
    assert PlatformRegistry.get_platform(None) is None
    prefixes = PlatformRegistry.list_all_prefixes()
    assert len(prefixes) >= 50
