import pytest
pytest
from _util_property import _TestHasProps, _TestModel, _TestModel2
from bokeh._testing.util.api import verify_all
from bokeh.core.has_props import HasProps
from bokeh.core.properties import Float, Int
import bokeh.core.property.instance as bcpi
ALL = ('Instance',)
Test___all__ = verify_all(bcpi, ALL)

def Test_Instance_test_init(self) -> None:
    with pytest.raises(TypeError):
        bcpi.Instance()

def Test_Instance_test_serialized(self) -> None:
    prop = bcpi.Instance(_TestModel)
    assert prop.serialized == True

def Test_Instance_test_readonly(self) -> None:
    prop = bcpi.Instance(_TestModel)
    assert prop.readonly == False

def Test_Instance_test_valid(self) -> None:
    prop = bcpi.Instance(_TestModel)
    assert prop.is_valid(None)
    assert prop.is_valid(_TestModel())

def Test_Instance_test_invalid(self) -> None:
    prop = bcpi.Instance(_TestModel)
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
    assert not prop.is_valid(_TestModel2())
    assert not prop.is_valid(_TestHasProps())

def Test_Instance_test_from_json(self) -> None:

    class MapOptions(HasProps):
        lat = Float
        lng = Float
        zoom = Int(12)
    v1 = bcpi.Instance(MapOptions).from_json(dict(lat=1, lng=2))
    v2 = MapOptions(lat=1, lng=2)
    assert v1.equals(v2)

def Test_Instance_test_has_ref(self) -> None:
    prop = bcpi.Instance(_TestModel)
    assert prop.has_ref

def Test_Instance_test_str(self) -> None:
    prop = bcpi.Instance(_TestModel)
    assert str(prop) == 'Instance(_TestModel)'