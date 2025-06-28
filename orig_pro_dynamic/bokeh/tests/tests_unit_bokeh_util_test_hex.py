import pytest
pytest
import numpy as np
import bokeh.util.hex as buh
np.random.seed(0)
n = 500
x = 2 + np.random.standard_normal(n)
y = 2 + np.random.standard_normal(n)

def Test_axial_to_cartesian_test_default_aspect_pointytop(self) -> None:
    q = np.array([0, 0, 0, 1, -1, 1, -1])
    r = np.array([0, 1, -1, 0, 1, -1, 0])
    (x, y) = buh.axial_to_cartesian(q, r, 1, 'pointytop')
    sq3 = np.sqrt(3)
    assert list(x) == [0, sq3 / 2, -sq3 / 2, sq3, -sq3 / 2, sq3 / 2, -sq3]
    assert list(y) == [-0.0, -1.5, 1.5, -0.0, -1.5, 1.5, -0.0]

def Test_axial_to_cartesian_test_default_aspect_flattop(self) -> None:
    q = np.array([0, 0, 0, 1, -1, 1, -1])
    r = np.array([0, 1, -1, 0, 1, -1, 0])
    (x, y) = buh.axial_to_cartesian(q, r, 1, 'flattop')
    sq3 = np.sqrt(3)
    assert list(x) == [0.0, 0.0, 0.0, 1.5, -1.5, 1.5, -1.5]
    assert list(y) == [0, -sq3, sq3, -sq3 / 2, -sq3 / 2, sq3 / 2, sq3 / 2]

def Test_cartesian_to_axial_test_default_aspect_pointytop(self) -> None:
    x = np.array([0, -2, 2, -1.5, -1.5, 1.5, 1.5])
    y = np.array([0, 0, 0, 1.5, -1.5, 1.5, -1.5])
    (q, r) = buh.cartesian_to_axial(x, y, 1, 'pointytop')
    assert list(zip(q, r)) == [(0, 0), (-1, 0), (1, 0), (0, -1), (-1, 1), (1, -1), (0, 1)]

def Test_cartesian_to_axial_test_default_aspect_flattop(self) -> None:
    x = np.array([0, 0, 0, 1.5, -1.5, 1.5, -1.5])
    y = np.array([0, -2, 2, -1.5, -1.5, 1.5, 1.5])
    (q, r) = buh.cartesian_to_axial(x, y, 1, 'flattop')
    assert list(zip(q, r)) == [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 1), (1, -1), (-1, 0)]

def Test_hexbin_test_gaussian_pointytop(self, pd) -> None:
    bins = buh.hexbin(x, y, 2)
    assert list(bins.q) == [0, 0, 1, 1, 1, 2, 2]
    assert list(bins.r) == [-1, 0, -2, -1, 0, -2, -1]
    assert list(bins.counts) == [9, 54, 1, 313, 98, 3, 22]
    assert bins.equals(buh.hexbin(x, y, 2, 'pointytop'))

def Test_hexbin_test_gaussian_flattop(self, pd) -> None:
    bins = buh.hexbin(x, y, 2, 'flattop')
    assert list(bins.q) == [0, 0, 1, 1, 1, 2]
    assert list(bins.r) == [-1, 0, -2, -1, 0, -2]
    assert list(bins.counts) == [95, 57, 14, 324, 8, 2]