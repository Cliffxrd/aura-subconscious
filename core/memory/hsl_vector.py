# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import math
from typing import Tuple, Dict, Any


class HSLVector:
    """
    HSL (Hue, Saturation, Lightness) 3D Polar Vector Space for AURA Neuro-Cognitive Memory.
    """

    @staticmethod
    def shortest_circular_distance(hue1: float, hue2: float) -> float:
        """
        Calculate the shortest distance between two hues on a 360° circular polar ring.
        Formula: min(|H1 - H2|, 360 - |H1 - H2|)
        Returns float in range [0.0, 180.0].
        """
        try:
            h1 = float(hue1) % 360.0
            h2 = float(hue2) % 360.0
        except (ValueError, TypeError):
            return 180.0

        raw_diff = abs(h1 - h2)
        return min(raw_diff, 360.0 - raw_diff)

    @classmethod
    def calculate_weight(
        cls,
        memory_hsl: Tuple[float, float, float],
        session_hsl: Tuple[float, float, float],
    ) -> float:
        """
        Calculate memory proximity resonance weight:
        Wm = (Sm / 100) * (1.0 - (dist_circ(Hm, Hsession) / 180°)) * (1.0 - |Lm - Lsession| / 100)

        Returns float in range [0.0, 1.0].
        """
        try:
            h_m, s_m, l_m = (
                float(memory_hsl[0]),
                float(memory_hsl[1]),
                float(memory_hsl[2]),
            )
        except (ValueError, TypeError, IndexError):
            h_m, s_m, l_m = 240.0, 70.0, 50.0

        try:
            h_s, s_s, l_s = (
                float(session_hsl[0]),
                float(session_hsl[1]),
                float(session_hsl[2]),
            )
        except (ValueError, TypeError, IndexError):
            h_s, s_s, l_s = 240.0, 70.0, 50.0

        hue_dist = cls.shortest_circular_distance(h_m, h_s)
        lightness_dist = abs(l_m - l_s)

        # Normalize to [0.0, 1.0]
        s_m_norm = max(0.0, min(100.0, s_m)) / 100.0
        lightness_dist_norm = max(0.0, min(100.0, lightness_dist)) / 100.0
        hue_similarity = max(0.0, 1.0 - (hue_dist / 180.0))

        weight = s_m_norm * hue_similarity * (1.0 - lightness_dist_norm)
        return max(0.0, min(1.0, weight))

    @staticmethod
    def map_sentiment(valence: float, arousal: float) -> Tuple[float, float, float]:
        """
        Map Russell's Circumplex Model (Valence [-1.0, 1.0], Arousal [-1.0, 1.0]) to HSL coordinates.
        """
        v_clamped = max(-1.0, min(1.0, float(valence)))
        a_clamped = max(-1.0, min(1.0, float(arousal)))

        # Hue: 0° (failure) to 120° (success)
        hue = ((v_clamped + 1.0) / 2.0) * 120.0

        # Saturation: 20% to 100% based on arousal
        saturation = 20.0 + (((a_clamped + 1.0) / 2.0) * 80.0)

        # Lightness: 30% (gloomy critique) to 80% (bright triumph)
        lightness = 50.0 + (v_clamped * 30.0)

        return (round(hue, 1), round(saturation, 1), round(lightness, 1))
