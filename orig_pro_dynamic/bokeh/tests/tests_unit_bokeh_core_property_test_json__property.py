import pytest
pytest
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
import bokeh.core.property.json as bcpj
ALL = ('JSON',)
Test___all__ = verify_all(bcpj, ALL)

def Test_JSON_test_valid(self) -> None:
    prop = bcpj.JSON()
    assert prop.is_valid(None)
    assert prop.is_valid('[]')
    assert prop.is_valid('[{"foo": 10}]')

def Test_JSON_test_invalid(self) -> None:
    prop = bcpj.JSON()
    assert not prop.is_valid('')
    assert not prop.is_valid('foo')
    assert not prop.is_valid('[]]')
    assert not prop.is_valid("[{'foo': 10}]")
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

def Test_JSON_test_has_ref(self) -> None:
    prop = bcpj.JSON()
    assert not prop.has_ref

def Test_JSON_test_str(self) -> None:
    prop = bcpj.JSON()
    assert str(prop) == 'JSON'