import pytest
pytest
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
from bokeh.core.enums import LineJoin, NamedColor
import bokeh.core.property.enum as bcpe
ALL = ('Enum',)
Test___all__ = verify_all(bcpe, ALL)

def Test_Enum_test_init(self) -> None:
    with pytest.raises(TypeError):
        bcpe.Enum()
    with pytest.raises(TypeError):
        bcpe.Enum('red', 'green', 1)
    with pytest.raises(TypeError):
        bcpe.Enum('red', 'green', 'red')

def Test_Enum_test_from_values_valid(self) -> None:
    prop = bcpe.Enum('red', 'green', 'blue')
    assert prop.is_valid(None)
    assert prop.is_valid('red')
    assert prop.is_valid('green')
    assert prop.is_valid('blue')

def Test_Enum_test_from_values_invalid(self) -> None:
    prop = bcpe.Enum('red', 'green', 'blue')
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
    assert not prop.is_valid('RED')
    assert not prop.is_valid('GREEN')
    assert not prop.is_valid('BLUE')
    assert not prop.is_valid(' red')
    assert not prop.is_valid(' green')
    assert not prop.is_valid(' blue')

def Test_Enum_test_from_enum_valid(self) -> None:
    prop = bcpe.Enum(LineJoin)
    assert prop.is_valid(None)
    assert prop.is_valid('miter')
    assert prop.is_valid('round')
    assert prop.is_valid('bevel')

def Test_Enum_test_from_enum_invalid(self) -> None:
    prop = bcpe.Enum(LineJoin)
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
    assert not prop.is_valid('MITER')
    assert not prop.is_valid('ROUND')
    assert not prop.is_valid('BEVEL')
    assert not prop.is_valid(' miter')
    assert not prop.is_valid(' round')
    assert not prop.is_valid(' bevel')

def Test_Enum_test_case_insensitive_enum_valid(self) -> None:
    prop = bcpe.Enum(NamedColor)
    assert prop.is_valid('red')
    assert prop.is_valid('Red')
    assert prop.is_valid('RED')

def Test_Enum_test_has_ref(self) -> None:
    prop = bcpe.Enum('foo')
    assert not prop.has_ref

def Test_Enum_test_str(self) -> None:
    prop = bcpe.Enum('foo')
    assert str(prop).startswith('Enum(')