import pytest
pytest
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
import bokeh.core.property.auto as bcpa
ALL = ('Auto',)
Test___all__ = verify_all(bcpa, ALL)

def Test_Auto_test_valid(self) -> None:
    prop = bcpa.Auto()
    assert prop.is_valid(None)
    assert prop.is_valid('auto')

def Test_Auto_test_invalid(self) -> None:
    prop = bcpa.Auto()
    assert not prop.is_valid(False)
    assert not prop.is_valid(True)
    assert not prop.is_valid(0)
    assert not prop.is_valid(1)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())

def Test_Auto_test_has_ref(self) -> None:
    prop = bcpa.Auto()
    assert not prop.has_ref

def Test_Auto_test_str(self) -> None:
    prop = bcpa.Auto()
    assert str(prop) == 'Auto'