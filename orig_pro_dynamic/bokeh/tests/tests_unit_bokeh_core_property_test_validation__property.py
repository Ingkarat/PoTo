import pytest
pytest
import re
from bokeh._testing.util.api import verify_all
from bokeh.core.has_props import HasProps
from bokeh.core.properties import Angle, AngleSpec, Bool, Color, ColorSpec, ColumnData, Complex, DashPattern, DataDistanceSpec, Date, Datetime, Dict, DistanceSpec, Either, Enum, Float, FontSize, FontSizeSpec, Instance, Int, Interval, List, MarkerType, MinMaxBounds, NumberSpec, Percent, Regex, ScreenDistanceSpec, Seq, Size, String, StringSpec, Tuple
from bokeh.core.property.bases import validation_on
import bokeh.core.property.validation as bcpv
ALL = ('validate', 'without_property_validation')
SPECS = (AngleSpec, ColorSpec, DataDistanceSpec, DistanceSpec, FontSizeSpec, NumberSpec, ScreenDistanceSpec, StringSpec)

def matches(string, pattern):
    return re.match(pattern, string) is not None
Test___all__ = verify_all(bcpv, ALL)

def TestValidationControl_test_validate(self) -> None:
    assert validation_on()
    with bcpv.validate(False):
        assert not validation_on()
    assert validation_on()
    with bcpv.validate(False):
        assert not validation_on()
        with bcpv.validate(True):
            assert validation_on()
        assert not validation_on()
    assert validation_on()
    bcpv.validate(False)
    assert not validation_on()
    bcpv.validate(True)
    assert validation_on()

def TestValidationControl_test_without_property_validation(self) -> None:

    @bcpv.without_property_validation
    def f():
        assert not validation_on()
    assert validation_on()
    f()
    assert validation_on()

def TestValidateDetailDefault_test_Angle(self) -> None:
    p = Angle()
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), 'expected a value of type Real, got junk of type str')

def TestValidateDetailDefault_test_Bool(self) -> None:
    p = Bool()
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), 'expected a value of type bool or bool_, got junk of type str')

def TestValidateDetailDefault_test_Complex(self) -> None:
    p = Complex()
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), 'expected a value of type Complex, got junk of type str')

def TestValidateDetailDefault_test_Float(self) -> None:
    p = Float()
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), 'expected a value of type Real, got junk of type str')

def TestValidateDetailDefault_test_Int(self) -> None:
    p = Int()
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), 'expected a value of type Integral, got junk of type str')

def TestValidateDetailDefault_test_Interval(self) -> None:
    p = Interval(Float, 0.0, 1.0)
    with pytest.raises(ValueError) as e:
        p.validate(2)
    assert matches(str(e.value), 'expected a value of type Float in range \\[0.0, 1.0\\], got 2')

def TestValidateDetailDefault_test_Percent(self) -> None:
    p = Percent()
    with pytest.raises(ValueError) as e:
        p.validate(10)
    assert matches(str(e.value), 'expected a value in range \\[0, 1\\], got 10')

def TestValidateDetailDefault_test_Size(self) -> None:
    p = Size()
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), 'expected a value of type Real, got junk of type str')

def TestValidateDetailDefault_test_List(self) -> None:
    p = List(Float)
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), "expected an element of List\\(Float\\), got 'junk'")

def TestValidateDetailDefault_test_Seq(self) -> None:
    p = Seq(Float)
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), "expected an element of Seq\\(Float\\), got 'junk'")

def TestValidateDetailDefault_test_Dict(self) -> None:
    p = Dict(String, Float)
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), "expected an element of Dict\\(String, Float\\), got 'junk'")

def TestValidateDetailDefault_test_Tuple(self) -> None:
    p = Tuple(Int, Int)
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), "expected an element of Tuple\\(Int, Int\\), got 'junk'")

def TestValidateDetailDefault_test_Color(self) -> None:
    p = Color()
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), "expected an element of either Enum\\(.*\\), .* or RGB, got 'junk'")

def TestValidateDetailDefault_test_ColumnData(self) -> None:
    p = ColumnData(String, Seq(Float))
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), "expected an element of ColumnData\\(String, Seq\\(Float\\)\\), got 'junk'")

def TestValidateDetailDefault_test_Datetime(self) -> None:
    p = Datetime()
    with pytest.raises(ValueError) as e:
        p.validate(object())
    assert matches(str(e.value), 'Expected a date, datetime object, or timestamp, got <object object at 0x.*>')

def TestValidateDetailDefault_test_Date(self) -> None:
    p = Date()
    with pytest.raises(ValueError) as e:
        p.validate(object())
    assert matches(str(e.value), 'Expected an ISO date string, got <object object at 0x.*>')

def TestValidateDetailDefault_test_DashPattern(self) -> None:
    p = DashPattern()
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), "expected an element of either Enum\\(.*\\), Regex\\(.*\\) or Seq\\(Int\\), got 'junk'")

def TestValidateDetailDefault_test_Either(self) -> None:
    p = Either(Int, Float)
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), "expected an element of either Int or Float, got 'junk'")

def TestValidateDetailDefault_test_Enum(self) -> None:
    p = Enum('red', 'green')
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), "invalid value: 'junk'; allowed values are red or green")

def TestValidateDetailDefault_test_FontSize(self) -> None:
    p = FontSize()
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), "'junk' is not a valid font size value")

def TestValidateDetailDefault_test_Instance(self) -> None:
    p = Instance(HasProps)
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), 'expected an instance of type HasProps, got junk of type str')

def TestValidateDetailDefault_test_MinMaxBounds(self) -> None:
    p = MinMaxBounds()
    with pytest.raises(ValueError) as e:
        p.validate(10)
    assert matches(str(e.value), 'expected an element of either Auto, Tuple\\(Float, Float\\) or Tuple\\(TimeDelta, TimeDelta\\), got 10')

def TestValidateDetailDefault_test_Regex(self) -> None:
    p = Regex('green')
    with pytest.raises(ValueError) as e:
        p.validate('junk')
    assert matches(str(e.value), "expected a string matching 'green' pattern, got 'junk'")

def TestValidateDetailDefault_test_String(self) -> None:
    p = String()
    with pytest.raises(ValueError) as e:
        p.validate(10)
    assert matches(str(e.value), 'expected a value of type str, got 10 of type int')

def TestValidateDetailDefault_test_MarkerType(self) -> None:
    p = MarkerType()
    with pytest.raises(ValueError) as e:
        p.validate('foo')
    assert matches(str(e.value), "invalid value: 'foo'; allowed values are asterisk, .* or y")

@pytest.mark.parametrize('spec', SPECS)
def TestValidateDetailDefault_test_Spec(self, spec) -> None:
    spec = SPECS[0]
    p = spec(default=None)
    with pytest.raises(ValueError) as e:
        p.validate(dict(bad='junk'))
    assert matches(str(e.value), "expected an element of either String, .*, got {'bad': 'junk'}")

def TestValidateDetailExplicit_test_Angle(self, detail) -> None:
    p = Angle()
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Bool(self, detail) -> None:
    p = Bool()
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Complex(self, detail) -> None:
    p = Complex()
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Float(self, detail) -> None:
    p = Float()
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Int(self, detail) -> None:
    p = Int()
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Interval(self, detail) -> None:
    p = Interval(Float, 0.0, 1.0)
    with pytest.raises(ValueError) as e:
        p.validate(2, detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Percent(self, detail) -> None:
    p = Percent()
    with pytest.raises(ValueError) as e:
        p.validate(10, detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Size(self, detail) -> None:
    p = Size()
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_List(self, detail) -> None:
    p = List(Float)
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Seq(self, detail) -> None:
    p = Seq(Float)
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Dict(self, detail) -> None:
    p = Dict(String, Float)
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Tuple(self, detail) -> None:
    p = Tuple(Int, Int)
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Color(self, detail) -> None:
    p = Color()
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_ColumnData(self, detail) -> None:
    p = ColumnData(String, Seq(Float))
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Date(self, detail) -> None:
    p = Date()
    with pytest.raises(ValueError) as e:
        p.validate(p, detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_DashPattern(self, detail) -> None:
    p = DashPattern()
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Either(self, detail) -> None:
    p = Either(Int, Float)
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Enum(self, detail) -> None:
    p = Enum('red', 'green')
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_FontSize(self, detail) -> None:
    p = FontSize()
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Instance(self, detail) -> None:
    p = Instance(HasProps)
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_MinMaxBounds(self, detail) -> None:
    p = MinMaxBounds()
    with pytest.raises(ValueError) as e:
        p.validate(10, detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_Regex(self, detail) -> None:
    p = Regex('green')
    with pytest.raises(ValueError) as e:
        p.validate('junk', detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_String(self, detail) -> None:
    p = String()
    with pytest.raises(ValueError) as e:
        p.validate(10, detail)
    assert (str(e.value) == '') == (not detail)

def TestValidateDetailExplicit_test_MarkerType(self, detail) -> None:
    p = MarkerType()
    with pytest.raises(ValueError) as e:
        p.validate('foo', detail)
    assert (str(e.value) == '') == (not detail)

@pytest.mark.parametrize('spec', SPECS)
def TestValidateDetailExplicit_test_Spec(self, detail, spec) -> None:
    spec = SPECS[0]
    p = spec(default=None)
    with pytest.raises(ValueError) as e:
        p.validate(dict(bad='junk'), detail)
    assert (str(e.value) == '') == (not detail)