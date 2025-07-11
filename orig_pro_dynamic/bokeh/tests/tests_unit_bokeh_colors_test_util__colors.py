import pytest
pytest
from bokeh.colors import named
import bokeh.colors.util as bcu

def Test_NamedColor_test_init(self) -> None:
    c = bcu.NamedColor('aliceblue', 240, 248, 255)
    assert c.name == 'aliceblue'

def Test_NamedColor_test_repr(self) -> None:
    c = bcu.NamedColor('aliceblue', 240, 248, 255)
    assert repr(c) == c.to_css()

def Test_NamedColor_test_to_css(self) -> None:
    c = bcu.NamedColor('aliceblue', 240, 248, 255)
    assert c.to_css() == 'aliceblue'

def Test_ColorGroup_test_len(self) -> None:
    assert len(_TestGroup) == 3

def Test_ColorGroup_test_iter(self) -> None:
    it = iter(_TestGroup)
    assert next(it) == named.red
    assert next(it) == named.green
    assert next(it) == named.blue

def Test_ColorGroup_test_getitem_string(self) -> None:
    assert _TestGroup['Red'] == named.red
    assert _TestGroup['Green'] == named.green
    assert _TestGroup['Blue'] == named.blue
    with pytest.raises(KeyError):
        _TestGroup['Junk']

def Test_ColorGroup_test_getitem_int(self) -> None:
    assert _TestGroup[0] == named.red
    assert _TestGroup[1] == named.green
    assert _TestGroup[2] == named.blue
    with pytest.raises(IndexError):
        _TestGroup[-1]
    with pytest.raises(IndexError):
        _TestGroup[3]

def Test_ColorGroup_test_getitem_bad(self) -> None:
    with pytest.raises(ValueError):
        _TestGroup[10.2]
    with pytest.raises(ValueError):
        _TestGroup[1,]
    with pytest.raises(ValueError):
        _TestGroup[[1]]