"""
fast_core.py – first-cut Holoman sin² Method in pure Python
"""

import math

_TABLE_SIZE = 4096            # 1 quadrant → 4096 entries  (0.022°)
_DU_PER_QUAD = 100            # your public DecUnit scale
_STEP = _DU_PER_QUAD / _TABLE_SIZE

# Precompute sin² for one quadrant (0‥90°) at import-time
_sin2_table = [math.sin(i * _STEP * math.pi / 200)**2 for i in range(_TABLE_SIZE + 1)]

def _fold(angle_du: float) -> tuple[int, int]:
    """
    Fold any angle (DecUnits) into (index, sign) for the lookup.
    Returns:
        idx  – 0‥_TABLE_SIZE
        sign – +1 or –1
    """
    # wrap to 0‥400
    a = angle_du % 400.0

    # determine quadrant & sign
    if 0 <= a < 100:                     # Quadrant I,  0‥90°
        idx = a
        sign = +1
    elif 100 <= a < 200:                 # Quadrant II, 90‥180°
        idx = 200 - a
        sign = +1
    elif 200 <= a < 300:                 # Quadrant III,180‥270°
        idx = a - 200
        sign = -1
    else:                                # Quadrant IV,270‥360°
        idx = 400 - a
        sign = -1

    # scale to table index
    lut_idx = int(round(idx / _STEP))
    return lut_idx, sign


# ───────────────────────────────────────────────────────────────────
#  Public API
# ───────────────────────────────────────────────────────────────────

def dec_sin(angle_du: float) -> float:
    """Return sin(angle) where angle is in DecUnits (100 = 90°)."""
    idx, sign = _fold(angle_du)
    sin2 = _sin2_table[idx]
    return sign * math.sqrt(sin2)


# Holoman sin² Method – informal alias
holoman_sin2 = dec_sin


def dec_cos(angle_du: float) -> float:
    """cos θ  = sin(100 DU – θ)."""
    return dec_sin(100.0 - angle_du)


def dec_tan(angle_du: float) -> float:
    s = dec_sin(angle_du)
    c = dec_cos(angle_du)
    if abs(c) < 1e-12:
        raise ZeroDivisionError("tan undefined near 90°")
    return s / c
