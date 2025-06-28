import pytest
pytest
from bokeh.colors.hsl import HSL
import bokeh.colors.color as bcc

def Test_Color_test_init(self) -> None:
    c = bcc.Color()
    assert c

def Test_Color_test_abstract(self) -> None:
    c = bcc.Color()
    with pytest.raises(NotImplementedError):
        c.copy()
    with pytest.raises(NotImplementedError):
        c.from_hsl('foo')
    with pytest.raises(NotImplementedError):
        c.from_rgb('foo')
    with pytest.raises(NotImplementedError):
        c.to_css()
    with pytest.raises(NotImplementedError):
        c.to_hsl()
    with pytest.raises(NotImplementedError):
        c.to_rgb()

def Test_Color_test_repr(self) -> None:
    c = bcc.Color()
    with pytest.raises(NotImplementedError):
        repr(c)

def Test_Color_test_clamp(self) -> None:
    assert bcc.Color.clamp(10) == 10
    assert bcc.Color.clamp(10, 20) == 10
    assert bcc.Color.clamp(10, 5) == 5
    assert bcc.Color.clamp(-10) == 0

def Test_Color_test_darken(self) -> None:
    c = HSL(10, 0.2, 0.2, 0.2)
    c2 = c.darken(0.1)
    assert c2 is not c
    assert c2.a == 0.2
    assert c2.h == 10
    assert c2.s == 0.2
    assert c2.l == 0.1
    c2 = c.darken(0.3)
    assert c2 is not c
    assert c2.a == 0.2
    assert c2.h == 10
    assert c2.s == 0.2
    assert c2.l == 0

def Test_Color_test_lighten(self) -> None:
    c = HSL(10, 0.2, 0.2, 0.2)
    c2 = c.lighten(0.2)
    assert c2 is not c
    assert c2.a == 0.2
    assert c2.h == 10
    assert c2.s == 0.2
    assert c2.l == 0.4
    c2 = c.lighten(1.2)
    assert c2 is not c
    assert c2.a == 0.2
    assert c2.h == 10
    assert c2.s == 0.2
    assert c2.l == 1.0