import math
from typing import Tuple

class HSLVector:
    """HSL circular math and vector operations for AURA memories."""
    
    @staticmethod
    def shortest_circular_distance(hue1: float, hue2: float) -> float:
        """Calculate the shortest distance between two hues on a 360 degree circle."""
        diff = abs(hue1 - hue2)
        return min(diff, 360 - diff)
        
    @staticmethod
    def calculate_weight(memory_hsl: Tuple[float, float, float], session_hsl: Tuple[float, float, float]) -> float:
        """
        Calculate memory weight scoring formula:
        Wm = Sm * (1.0 - (|Hm - Hsession| / 180)) * (1.0 - |Lm - Lsession|)
        """
        h_m, s_m, l_m = memory_hsl
        h_s, s_s, l_s = session_hsl
        
        hue_dist = HSLVector.shortest_circular_distance(h_m, h_s)
        lightness_dist = abs(l_m - l_s)
        
        # Normalize saturation and lightness (assuming they are 0-100 percentages)
        s_m_norm = s_m / 100.0
        lightness_dist_norm = lightness_dist / 100.0
        
        weight = s_m_norm * (1.0 - (hue_dist / 180.0)) * (1.0 - lightness_dist_norm)
        return max(0.0, weight)
        
    @staticmethod
    def map_sentiment(valence: float, arousal: float) -> Tuple[float, float, float]:
        """Map valence (-1 to 1) and arousal (-1 to 1) to an HSL vector."""
        # This is a basic mapping, can be refined based on AURA's exact emotional model
        # Hue: Valence determines color (0 = bad/red, 120 = good/green)
        hue = ((valence + 1) / 2) * 120 
        
        # Saturation: Arousal determines intensity (0 to 100%)
        saturation = ((arousal + 1) / 2) * 100
        
        # Lightness: Default to 50% for neutral
        lightness = 50.0 + (valence * 30.0) 
        
        return (hue, saturation, lightness)
