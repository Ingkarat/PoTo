from pygal.interpolate import quadratic_interpolate
from pygal.interpolate import cubic_interpolate
from pygal.interpolate import hermite_interpolate
from pygal.interpolate import lagrange_interpolate
from pygal.interpolate import trigonometric_interpolate

def test_PT_quadratic_interpolate():
    quadratic_interpolate(x,y,250)
    
def test_PT_cubic_interpolate():
    cubic_interpolate(x,y,250)
    
def test_PT_hermite_interpolate():
    hermite_interpolate()
    
def test_PT_lagrange_interpolate():
    lagrange_interpolate(x,y,250)
    
def test_PT_trigonometric_interpolate():
    trigonometric_interpolate(x,y,250)