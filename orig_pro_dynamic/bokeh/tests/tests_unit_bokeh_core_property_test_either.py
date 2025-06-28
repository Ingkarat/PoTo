import pytest
pytest
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
from bokeh.core.properties import Int, Interval, List, Regex
import bokeh.core.property.either as bcpe
ALL = ('Either',)
Test___all__ = verify_all(bcpe, ALL)

def Test_Either_test_init(self) -> None:
    with pytest.raises(TypeError):
        bcpe.Either()

def Test_Either_test_valid(self) -> None:
    prop = bcpe.Either(Interval(Int, 0, 100), Regex('^x*$'), List(Int))
    assert prop.is_valid(None)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid('')
    assert prop.is_valid('xxx')
    assert prop.is_valid([])
    assert prop.is_valid([1, 2, 3])
    assert prop.is_valid(100)
    assert prop.is_valid(False)
    assert prop.is_valid(True)

def Test_Either_test_invalid(self) -> None:
    prop = bcpe.Either(Interval(Int, 0, 100), Regex('^x*$'), List(Int))
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid(())
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid(-100)
    assert not prop.is_valid('yyy')
    assert not prop.is_valid([1, 2, ''])

def Test_Either_test_has_ref(self) -> None:
    prop = bcpe.Either(Int, Int)
    assert not prop.has_ref

def Test_Either_test_str(self) -> None:
    prop = bcpe.Either(Int, Int)
    assert str(prop) == 'Either(Int, Int)'