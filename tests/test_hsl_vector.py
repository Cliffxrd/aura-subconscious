# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

from core.memory.hsl_vector import HSLVector


def test_shortest_circular_distance():
    assert HSLVector.shortest_circular_distance(10, 350) == 20
    assert HSLVector.shortest_circular_distance(0, 180) == 180
    assert HSLVector.shortest_circular_distance(90, 100) == 10


def test_calculate_weight():
    weight = HSLVector.calculate_weight((120, 100, 50), (120, 100, 50))
    assert weight == 1.0

    weight2 = HSLVector.calculate_weight((0, 100, 50), (180, 100, 50))
    assert weight2 == 0.0


def test_map_sentiment():
    hsl = HSLVector.map_sentiment(1.0, 1.0)
    assert hsl == (120.0, 100.0, 80.0)
