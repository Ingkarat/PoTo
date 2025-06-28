from pygal.util import float_format
from pygal.util import deg
from pygal.util import compute_logarithmic_scale
from pygal.util import safe_enumerate

def test_PT_float_format():
    float_format(1.23)

def test_PT_float_format():
    deg(1.23)

def test_PT_compute_logarithmic_scale():
    compute_logarithmic_scale()

def test_PT_safe_enumerate():
    safe_enumerate()