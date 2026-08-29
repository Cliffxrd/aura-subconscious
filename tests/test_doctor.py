# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

from core.cli.doctor import AuraDoctor


def test_run_health_check():
    assert AuraDoctor.run_health_check() is True
