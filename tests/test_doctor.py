# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

from core.cli.doctor import AuraDoctor


def test_run_diagnostics(tmp_path):
    doctor = AuraDoctor(aura_home=tmp_path)
    status = doctor.run_diagnostics()
    # In empty tmp directory, returns True indicating engine is healthy and ready to scaffold
    assert status is True
