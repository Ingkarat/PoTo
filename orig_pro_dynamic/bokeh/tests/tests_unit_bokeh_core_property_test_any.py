import pytest
pytest
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
import bokeh.core.property.any as bcpa
ALL = ('Any', 'AnyRef')
Test___all__ = verify_all(bcpa, ALL)

def Test_Any_test_valid(self) -> None:
    prop = bcpa.Any()
    assert prop.is_valid(None)
    assert prop.is_valid(False)
    assert prop.is_valid(True)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(0.0)
    assert prop.is_valid(1.0)
    assert prop.is_valid(1.0 + 1j)
    assert prop.is_valid('')
    assert prop.is_valid(())
    assert prop.is_valid([])
    assert prop.is_valid({})
    assert prop.is_valid(_TestHasProps())
    assert prop.is_valid(_TestModel())

def Test_Any_test_invalid(self) -> None:
    pass

def Test_Any_test_has_ref(self) -> None:
    prop = bcpa.Any()
    assert not prop.has_ref

def Test_AnyRef_test_valid(self) -> None:
    prop = bcpa.AnyRef()
    assert prop.is_valid(None)
    assert prop.is_valid(False)
    assert prop.is_valid(True)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(0.0)
    assert prop.is_valid(1.0)
    assert prop.is_valid(1.0 + 1j)
    assert prop.is_valid('')
    assert prop.is_valid(())
    assert prop.is_valid([])
    assert prop.is_valid({})
    assert prop.is_valid(_TestHasProps())
    assert prop.is_valid(_TestModel())

def Test_AnyRef_test_invalid(self) -> None:
    pass

def Test_AnyRef_test_has_ref(self) -> None:
    prop = bcpa.AnyRef()
    assert prop.has_ref