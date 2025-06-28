import pytest
pytest
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
import bokeh.core.property.string as bcpr
ALL = ('Regex', 'Base64String')
Test___all__ = verify_all(bcpr, ALL)

def Test_Regex_test_init(self) -> None:
    with pytest.raises(TypeError):
        bcpr.Regex()

def Test_Regex_test_valid(self) -> None:
    prop = bcpr.Regex('^x*$')
    assert prop.is_valid(None)
    assert prop.is_valid('')
    assert prop.is_valid('x')

def Test_Regex_test_invalid(self) -> None:
    prop = bcpr.Regex('^x*$')
    assert not prop.is_valid('xy')
    assert not prop.is_valid(False)
    assert not prop.is_valid(True)
    assert not prop.is_valid(0)
    assert not prop.is_valid(1)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())

def Test_Regex_test_has_ref(self) -> None:
    prop = bcpr.Regex('')
    assert not prop.has_ref

def Test_Regex_test_str(self) -> None:
    prop = bcpr.Regex('')
    assert str(prop).startswith('Regex(')