"""
DecTrig package – v0.1.0
Exports the new Holoman sin² core.
"""

from .fast_core import (
    dec_sin,
    dec_cos,
    dec_tan,
    holoman_sin2,
)

__all__ = ["dec_sin", "dec_cos", "dec_tan", "holoman_sin2"]
__version__ = "0.1.0"
