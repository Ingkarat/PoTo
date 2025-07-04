import pytest
pytest
from bokeh.colors import RGB
import bokeh.colors.hsl as bch

def Test_HSL_test_init(self) -> None:
    c = bch.HSL(10, 0.2, 0.3)
    assert c
    assert c.a == 1.0
    assert c.h == 10
    assert c.s == 0.2
    assert c.l == 0.3
    c = bch.HSL(10, 0.2, 0.3, 0.3)
    assert c
    assert c.a == 0.3
    assert c.h == 10
    assert c.s == 0.2
    assert c.l == 0.3

def Test_HSL_test_repr(self) -> None:
    c = bch.HSL(10, 0.2, 0.3)
    assert repr(c) == c.to_css()
    c = bch.HSL(10, 0.2, 0.3, 0.3)
    assert repr(c) == c.to_css()

def Test_HSL_test_copy(self) -> None:
    c = bch.HSL(10, 0.2, 0.3)
    c2 = c.copy()
    assert c2 is not c
    assert c2.a == c.a
    assert c2.h == c.h
    assert c2.s == c.s
    assert c2.l == c.l

def Test_HSL_test_from_hsl(self) -> None:
    c = bch.HSL(10, 0.2, 0.3)
    c2 = bch.HSL.from_hsl(c)
    assert c2 is not c
    assert c2.a == c.a
    assert c2.h == c.h
    assert c2.s == c.s
    assert c2.l == c.l
    c = bch.HSL(10, 0.2, 0.3, 0.1)
    c2 = bch.HSL.from_hsl(c)
    assert c2 is not c
    assert c2.a == c.a
    assert c2.h == c.h
    assert c2.s == c.s
    assert c2.l == c.l

def Test_HSL_test_from_rgb(self) -> None:
    c = RGB(255, 100, 0)
    c2 = bch.HSL.from_rgb(c)
    assert c2 is not c
    assert c2.a == 1
    assert c2.h == 24
    assert c2.s == 1.0
    assert c2.l == 0.5
    c = RGB(255, 100, 0, 0.1)
    c2 = bch.HSL.from_rgb(c)
    assert c2 is not c
    assert c2.a == 0.1
    assert c2.h == 24
    assert c2.s == 1.0
    assert c2.l == 0.5

def Test_HSL_test_to_css(self) -> None:
    c = bch.HSL(10, 0.2, 0.3)
    assert c.to_css() == 'hsl(10, 20.0%, 30.0%)'
    c = bch.HSL(10, 0.2, 0.3, 0.3)
    assert c.to_css() == 'hsla(10, 20.0%, 30.0%, 0.3)'

def Test_HSL_test_to_hsl(self) -> None:
    c = bch.HSL(10, 0.2, 0.3)
    c2 = c.to_hsl()
    assert c2 is not c
    assert c2.a == c.a
    assert c2.h == c.h
    assert c2.s == c.s
    assert c2.l == c.l
    c = bch.HSL(10, 0.2, 0.3, 0.1)
    c2 = c.to_hsl()
    assert c2 is not c
    assert c2.a == c.a
    assert c2.h == c.h
    assert c2.s == c.s
    assert c2.l == c.l

def Test_HSL_test_to_rgb(self) -> None:
    c = bch.HSL(10, 0.2, 0.3)
    c2 = c.to_rgb()
    assert c2 is not c
    assert c2.a == 1.0
    assert c2.r == 92
    assert c2.g == 66
    assert c2.b == 61
    c = bch.HSL(10, 0.2, 0.3, 0.1)
    c2 = c.to_rgb()
    assert c2 is not c
    assert c.a == 0.1
    assert c2.r == 92
    assert c2.g == 66
    assert c2.b == 61