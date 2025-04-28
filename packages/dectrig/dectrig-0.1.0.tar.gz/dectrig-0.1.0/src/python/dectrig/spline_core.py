"""
DecTrig reference implementation (Phase-2 v0.1)
Loads cubic-spline tables in CSV form and evaluates sin, cos, tan for 0–100 DT°.
"""

from pathlib import Path
from bisect import bisect_right
import csv

# --------------------------------------------------
# Helper to load CSV of rows: x0,a,b,c,d  (one per interval)
# --------------------------------------------------
def _load_table(filename):
    rows = []
    here = Path(__file__).resolve()
    csv_path = here.parent / 'data' / filename   # ..\..\data\<file>
    with csv_path.open() as f:
        rd = csv.DictReader(f)
        for r in rd:
            rows.append((
                float(r['x0']),
                float(r['a']), float(r['b']),
                float(r['c']), float(r['d'])
            ))
    breaks = [r[0] for r in rows]
    return rows, breaks

# Load the three spline tables
_SIN, _SIN_BRK = _load_table('sin_spline.csv')
_COS, _COS_BRK = _load_table('cos_spline.csv')
_TAN, _TAN_BRK = _load_table('tan_spline.csv')   # up to 99 DT°

# --------------------------------
# Cubic-evaluation helper
# --------------------------------
def _eval(dt, table, brk):
    i = bisect_right(brk, dt) - 1
    x0, a, b, c, d = table[i]
    dx = dt - x0
    # Horner form:  (((a*dx) + b)*dx + c)*dx + d
    return ((a*dx + b)*dx + c)*dx + d

# Public API ----------------------------------------------------------
def sin_dt(dt): return _eval(dt, _SIN, _SIN_BRK)
def cos_dt(dt): return _eval(dt, _COS, _COS_BRK)

def tan_dt(dt):
    if dt >= 99.999:
        raise ValueError("tan undefined at 100 DT° (≈90°)")
    return _eval(dt, _TAN, _TAN_BRK)

def dt_to_deg(dt):  return dt * 0.9
def deg_to_dt(deg): return deg / 0.9

def sin_full_dt(x):
    # normalize into [0,400)
    x_mod = x % 400
    q, r = divmod(x_mod, 100)
    if q == 0:
        return sin_dt(r)
    elif q == 1:
        return sin_dt(100 - r)
    elif q == 2:
        return -sin_dt(r)
    else:  # q == 3
        return -sin_dt(100 - r)

def cos_full_dt(x):
    x_mod = x % 400
    q, r = divmod(x_mod, 100)
    if q == 0:
        return cos_dt(r)
    elif q == 1:
        return -cos_dt(100 - r)
    elif q == 2:
        return -cos_dt(r)
    else:  # q == 3
        return cos_dt(100 - r)

def tan_full_dt(x):
    # caution: poles at 100, 300 DT°
    c = cos_full_dt(x)
    if abs(c) < 1e-12:
        raise ValueError(f"tan undefined near {x} DT°")
    return sin_full_dt(x) / c

# —— Full-circle support (0–400 DT°) —————————————

def sin_full_dt(x):
    """Compute sin for x in 0–400 DT° via quadrant symmetry."""
    x_mod = x % 400
    q, r = divmod(x_mod, 100)
    if q == 0:
        return sin_dt(r)
    elif q == 1:
        return sin_dt(100 - r)
    elif q == 2:
        return -sin_dt(r)
    else:  # q == 3
        return -sin_dt(100 - r)

def cos_full_dt(x):
    """Compute cos for x in 0–400 DT° via quadrant symmetry."""
    x_mod = x % 400
    q, r = divmod(x_mod, 100)
    if q == 0:
        return cos_dt(r)
    elif q == 1:
        return -cos_dt(100 - r)
    elif q == 2:
        return -cos_dt(r)
    else:  # q == 3
        return cos_dt(100 - r)

def tan_full_dt(x):
    """Compute tan for x in 0–400 DT°; error at poles (100, 300 DT°)."""
    c = cos_full_dt(x)
    if abs(c) < 1e-12:
        raise ValueError(f"tan undefined near {x} DT°")
    return sin_full_dt(x) / c
