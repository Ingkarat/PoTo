import pytest
pytest
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
from bokeh.core.properties import Float, Int
import bokeh.core.property.numeric as bcpn
ALL = ('Angle', 'Byte', 'Interval', 'NonNegativeInt', 'Percent', 'PositiveInt', 'Size')
Test___all__ = verify_all(bcpn, ALL)

def Test_Angle_test_valid(self) -> None:
    prop = bcpn.Angle()
    assert prop.is_valid(None)
    assert prop.is_valid(False)
    assert prop.is_valid(True)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(0.0)
    assert prop.is_valid(1.0)

def Test_Angle_test_invalid(self) -> None:
    prop = bcpn.Angle()
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())

def Test_Angle_test_has_ref(self) -> None:
    prop = bcpn.Angle()
    assert not prop.has_ref

def Test_Angle_test_str(self) -> None:
    prop = bcpn.Angle()
    assert str(prop) == 'Angle'

def Test_Interval_test_init(self) -> None:
    with pytest.raises(TypeError):
        bcpn.Interval()
    with pytest.raises(ValueError):
        bcpn.Interval(Int, 0.0, 1.0)

def Test_Interval_test_valid_int(self) -> None:
    prop = bcpn.Interval(Int, 0, 255)
    assert prop.is_valid(None)
    assert prop.is_valid(False)
    assert prop.is_valid(True)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(127)

def Test_Interval_test_invalid_int(self) -> None:
    prop = bcpn.Interval(Int, 0, 255)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid(-1)
    assert not prop.is_valid(256)

def Test_Interval_test_valid_float(self) -> None:
    prop = bcpn.Interval(Float, 0.0, 1.0)
    assert prop.is_valid(None)
    assert prop.is_valid(False)
    assert prop.is_valid(True)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(0.0)
    assert prop.is_valid(1.0)
    assert prop.is_valid(0.5)

def Test_Interval_test_invalid_float(self) -> None:
    prop = bcpn.Interval(Float, 0.0, 1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid(-0.001)
    assert not prop.is_valid(1.001)

def Test_Interval_test_has_ref(self) -> None:
    prop = bcpn.Interval(Float, 0.0, 1.0)
    assert not prop.has_ref

def Test_Interval_test_str(self) -> None:
    prop = bcpn.Interval(Float, 0.0, 1.0)
    assert str(prop) == 'Interval(Float, 0.0, 1.0)'

def Test_Size_test_valid(self) -> None:
    prop = bcpn.Size()
    assert prop.is_valid(None)
    assert prop.is_valid(False)
    assert prop.is_valid(True)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(0.0)
    assert prop.is_valid(1.0)
    assert prop.is_valid(100)
    assert prop.is_valid(100.1)

def Test_Size_test_invalid(self) -> None:
    prop = bcpn.Size()
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid(-100)
    assert not prop.is_valid(-0.001)

def Test_Size_test_has_ref(self) -> None:
    prop = bcpn.Size()
    assert not prop.has_ref

def Test_Size_test_str(self) -> None:
    prop = bcpn.Size()
    assert str(prop) == 'Size'

def Test_Percent_test_valid(self) -> None:
    prop = bcpn.Percent()
    assert prop.is_valid(None)
    assert prop.is_valid(False)
    assert prop.is_valid(True)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(0.0)
    assert prop.is_valid(1.0)
    assert prop.is_valid(0.5)

def Test_Percent_test_invalid(self) -> None:
    prop = bcpn.Percent()
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid(-0.001)
    assert not prop.is_valid(1.001)

def Test_Percent_test_has_ref(self) -> None:
    prop = bcpn.Percent()
    assert not prop.has_ref

def Test_Percent_test_str(self) -> None:
    prop = bcpn.Percent()
    assert str(prop) == 'Percent'

def Test_NonNegativeInt_test_valid(self) -> None:
    prop = bcpn.NonNegativeInt()
    assert prop.is_valid(None)
    assert prop.is_valid(False)
    assert prop.is_valid(True)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(2)
    assert prop.is_valid(100)

def Test_NonNegativeInt_test_invalid(self) -> None:
    prop = bcpn.NonNegativeInt()
    assert not prop.is_valid(-1)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid(-100)
    assert not prop.is_valid(-0.001)

def Test_NonNegativeInt_test_has_ref(self) -> None:
    prop = bcpn.NonNegativeInt()
    assert not prop.has_ref

def Test_NonNegativeInt_test_str(self) -> None:
    prop = bcpn.NonNegativeInt()
    assert str(prop) == 'NonNegativeInt'

def Test_PositiveInt_test_valid(self) -> None:
    prop = bcpn.PositiveInt()
    assert prop.is_valid(None)
    assert prop.is_valid(True)
    assert prop.is_valid(1)
    assert prop.is_valid(2)
    assert prop.is_valid(100)

def Test_PositiveInt_test_invalid(self) -> None:
    prop = bcpn.PositiveInt()
    assert not prop.is_valid(False)
    assert not prop.is_valid(-1)
    assert not prop.is_valid(0)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid(-100)
    assert not prop.is_valid(-0.001)

def Test_PositiveInt_test_has_ref(self) -> None:
    prop = bcpn.PositiveInt()
    assert not prop.has_ref

def Test_PositiveInt_test_str(self) -> None:
    prop = bcpn.PositiveInt()
    assert str(prop) == 'PositiveInt'