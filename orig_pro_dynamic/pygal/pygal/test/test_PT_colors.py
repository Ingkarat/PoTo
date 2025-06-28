from pygal.colors import normalize_float
from pygal.colors import is_foreground_light

def test_PT_normalize_float():
    normalize_float(1.23)

def test_PT_is_foreground_light():
    c = "#000000"
    is_foreground_light(c)