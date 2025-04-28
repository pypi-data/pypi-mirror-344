import math, pytest
from src.python import dectrig as dt

# 0 – 100 DT° in 0.1-unit steps
@pytest.mark.parametrize("x", [i/10 for i in range(0, 1001)])
def test_sin(x):
    assert abs(dt.sin_dt(x) - math.sin(math.radians(x*0.9))) < 1e-8

@pytest.mark.parametrize("x", [i/10 for i in range(0, 1001)])
def test_cos(x):
    assert abs(dt.cos_dt(x) - math.cos(math.radians(x*0.9))) < 1e-8

# Tangent up to 80 DT°, where splin remains stable
@pytest.mark.parametrize("x", [i/10 for i in range(0, 801)])
def test_tan(x):
    assert abs(dt.tan_dt(x) - math.tan(math.radians(x*0.9))) < 1e-4

# Full-circle tests
@pytest.mark.parametrize("x", [0, 50, 100, 150, 200, 250, 300, 350, 399.9])
def test_sin_full(x):
    expected = math.sin(math.radians(x * 0.9))
    assert abs(dt.sin_full_dt(x) - expected) < 1e-8

@pytest.mark.parametrize("x", [0, 50, 100, 150, 200, 250, 300, 350, 399.9])
def test_cos_full(x):
    expected = math.cos(math.radians(x * 0.9))
    assert abs(dt.cos_full_dt(x) - expected) < 1e-8

@pytest.mark.parametrize("x", [10, 110, 210, 310])
def test_tan_full(x):
    # avoid poles at 100 & 300 DT°
    expected = math.tan(math.radians(x * 0.9))
    assert abs(dt.tan_full_dt(x) - expected) < 1e-4



