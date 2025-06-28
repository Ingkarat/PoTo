from pygal.adapters import positive
from pygal.adapters import not_zero
from pygal.adapters import none_to_zero
from pygal.adapters import decimal_to_float

def test_PT_positive():
    positive(5)
    positive("a")
    positive(None)

def test_PT_not_zero():
    not_zero(5)

def test_PT_none_to_zero():
    none_to_zero(None)
    none_to_zero(5)

def test_PT_decimal_to_float():
    decimal_to_float(1.23)