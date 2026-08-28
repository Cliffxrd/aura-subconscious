import math
from typing import Tuple, Dict

class HSLVector:
    """
    HSL (Hue, Saturation, Lightness) 3D Polar Vector Space for AURA Neuro-Cognitive Memory.
    
    Dimensions:
    1. Hue (H in [0.0, 360.0]): Cognitive Domain & Operational Stance.
       - 0° / Crimson Red: Defects, Crashes, Broken Builds, Crisis Triage
       - 45° / Warm Amber: Investigation, Refactoring, Code Scrutiny, Code Review
       - 90° / Electric Lime: Warnings, High Complexity, Architectural Risk
       - 120° / Emerald Green: Milestones, Achievements, 100% Test Pass
       - 180° / Cyan / Teal: Calm Blueprints, Clean Architecture, Interfaces
       - 240° / Sapphire Blue: Foundational Truth, Identity Anchors, Core Lore
       - 300° / Electric Magenta: UX/UI Polish, Design Tokens, Visual Art
       
    2. Saturation (S in [0.0, 100.0]): Cognitive Arousal, Urgency & Attention Focus.
       - 90% - 100%: Critical Priority / Explicit User Command / High-Stakes Defect
       - 65% - 85%: Standard Pair Programming / Iterative Engineering Flow State
       - 20% - 50%: Passive Maintenance / Low-Intensity Background Circadian Tasks
       
    3. Lightness (L in [0.0, 100.0]): Emotional Valence & Evaluative Tone.
       - 75% - 90%: Positive Valence / Triumph / Optimistic Approval
       - 45% - 55%: Balanced Neutral / Objective Factual Assessment
       - 20% - 35%: Negative Valence / Severe Critique / Post-Mortem Rejection
    """
    
    # Standard Cognitive Hue Milestones
    HUE_DEFECT = 0.0          # Red
    HUE_INVESTIGATION = 45.0  # Amber
    HUE_WARNING = 90.0        # Lime/Yellow
    HUE_MILESTONE = 120.0     # Green
    HUE_BLUEPRINT = 180.0     # Cyan
    HUE_FOUNDATIONAL = 240.0  # Sapphire Blue
    HUE_UI_DESIGN = 300.0     # Magenta
    
    DOMAIN_HUE_MAP: Dict[str, float] = {
        "defect": HUE_DEFECT,
        "bug": HUE_DEFECT,
        "crash": HUE_DEFECT,
        "failure": HUE_DEFECT,
        "investigation": HUE_INVESTIGATION,
        "refactor": HUE_INVESTIGATION,
        "review": HUE_INVESTIGATION,
        "test": HUE_INVESTIGATION,
        "warning": HUE_WARNING,
        "debt": HUE_WARNING,
        "risk": HUE_WARNING,
        "milestone": HUE_MILESTONE,
        "success": HUE_MILESTONE,
        "achievement": HUE_MILESTONE,
        "blueprint": HUE_BLUEPRINT,
        "architecture": HUE_BLUEPRINT,
        "spec": HUE_BLUEPRINT,
        "truth": HUE_FOUNDATIONAL,
        "foundational": HUE_FOUNDATIONAL,
        "identity": HUE_FOUNDATIONAL,
        "lore": HUE_FOUNDATIONAL,
        "ui": HUE_UI_DESIGN,
        "ux": HUE_UI_DESIGN,
        "design": HUE_UI_DESIGN,
        "styling": HUE_UI_DESIGN,
        "glassmorphism": HUE_UI_DESIGN
    }

    @classmethod
    def get_hue_for_domain(cls, domain: str) -> float:
        """Resolve cognitive domain string to standard hue angle (default 180° Blueprint)."""
        key = domain.lower().strip()
        return cls.DOMAIN_HUE_MAP.get(key, cls.HUE_BLUEPRINT)
    
    @staticmethod
    def shortest_circular_distance(hue1: float, hue2: float) -> float:
        """
        Calculate the shortest circular distance between two hues on a 360° circle.
        Example: distance between 10° and 350° is 20°, not 340°.
        """
        h1 = hue1 % 360.0
        h2 = hue2 % 360.0
        diff = abs(h1 - h2)
        return min(diff, 360.0 - diff)
        
    @classmethod
    def calculate_weight(cls, memory_hsl: Tuple[float, float, float], session_hsl: Tuple[float, float, float]) -> float:
        """
        Calculate memory proximity resonance weight:
        Wm = (Sm / 100) * (1.0 - (dist_circ(Hm, Hsession) / 180°)) * (1.0 - |Lm - Lsession| / 100)
        
        Returns float in range [0.0, 1.0].
        """
        h_m, s_m, l_m = memory_hsl
        h_s, s_s, l_s = session_hsl
        
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
        - Valence: maps from Red (0°) for negative to Green (120°) for positive.
        - Arousal: maps from 0% (lethargic/calm) to 100% (high intensity/urgency).
        - Lightness: modulated around 50% neutral baseline.
        """
        v_clamped = max(-1.0, min(1.0, valence))
        a_clamped = max(-1.0, min(1.0, arousal))
        
        # Hue: 0° (failure) to 120° (success)
        hue = ((v_clamped + 1.0) / 2.0) * 120.0
        
        # Saturation: 20% to 100% based on arousal
        saturation = 20.0 + (((a_clamped + 1.0) / 2.0) * 80.0)
        
        # Lightness: 30% (gloomy critique) to 80% (bright triumph)
        lightness = 50.0 + (v_clamped * 30.0)
        
        return (round(hue, 1), round(saturation, 1), round(lightness, 1))

