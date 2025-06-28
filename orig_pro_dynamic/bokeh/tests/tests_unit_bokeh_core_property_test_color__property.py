import pytest
pytest
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
from bokeh.colors import RGB
import bokeh.core.property.color as bcpc
ALL = ('Color', 'RGB', 'ColorHex')
Test___all__ = verify_all(bcpc, ALL)

def Test_Color_test_valid(self) -> None:
    prop = bcpc.Color()
    assert prop.is_valid(None)
    assert prop.is_valid((0, 127, 255))
    assert prop.is_valid((0, 127, 255, 1.0))
    assert prop.is_valid('#00aaff')
    assert prop.is_valid('#00AAFF')
    assert prop.is_valid('#00AaFf')
    assert prop.is_valid('blue')
    assert prop.is_valid('BLUE')
    assert prop.is_valid('rgb(10, 20, 30)')
    assert prop.is_valid('rgba(10, 20, 30, 1)')
    assert prop.is_valid('rgba(10, 20, 30, 0.5)')
    assert prop.is_valid(RGB(10, 20, 30))

def Test_Color_test_invalid(self) -> None:
    prop = bcpc.Color()
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
    assert not prop.is_valid((0, -127, 255))
    assert not prop.is_valid((0, 127))
    assert not prop.is_valid((0, 127, 1.0))
    assert not prop.is_valid((0, 127, 255, 255))
    assert not prop.is_valid('(0, 127, 255)')
    assert not prop.is_valid('rgb(0, -127, 255)')
    assert not prop.is_valid('rgb(0, 127)')
    assert not prop.is_valid('rgb(0, 127, 1.0)')
    assert not prop.is_valid('rgb(256, 1, 1)')
    assert not prop.is_valid('rgb(256, 1, 1, 1.0)')
    assert not prop.is_valid('(10, 20, 30')
    assert not prop.is_valid('rgba(10, 20, 30')
    assert not prop.is_valid('rgba(10, 20, 30)')
    assert not prop.is_valid('rgba(10, 20, 30,)')
    assert not prop.is_valid('rgba(10, 20)')
    assert not prop.is_valid('rgba(10, 20, 256, 1)')
    assert not prop.is_valid('rgba(10, 20, 256, 10)')
    assert not prop.is_valid('rgba(10, 20, 30, 50)')
    assert not prop.is_valid('00aaff')
    assert not prop.is_valid('00AAFF')
    assert not prop.is_valid('00AaFf')
    assert not prop.is_valid('#00AaFg')
    assert not prop.is_valid('#00AaFff')
    assert not prop.is_valid('foobar')

def Test_Color_test_transform(self) -> None:
    prop = bcpc.Color()
    assert prop.transform((0, 127, 255)) == 'rgb(0, 127, 255)'
    assert prop.transform((0, 127, 255, 0.1)) == 'rgba(0, 127, 255, 0.1)'

def Test_Color_test_has_ref(self) -> None:
    prop = bcpc.Color()
    assert not prop.has_ref

def Test_Color_test_str(self) -> None:
    prop = bcpc.Color()
    assert str(prop) == 'Color'

def Test_RGB_test_valid(self) -> None:
    prop = bcpc.RGB()
    assert prop.is_valid(None)
    assert prop.is_valid(RGB(10, 20, 30))

def Test_RGB_test_invalid(self) -> None:
    prop = bcpc.RGB()
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
    assert not prop.is_valid((0, 127, 255))
    assert not prop.is_valid((0, 127, 255, 1.0))
    assert not prop.is_valid((0, -127, 255))
    assert not prop.is_valid((0, 127))
    assert not prop.is_valid((0, 127, 1.0))
    assert not prop.is_valid((0, 127, 255, 255))
    assert not prop.is_valid('#00aaff')
    assert not prop.is_valid('#00AAFF')
    assert not prop.is_valid('#00AaFf')
    assert not prop.is_valid('00aaff')
    assert not prop.is_valid('00AAFF')
    assert not prop.is_valid('00AaFf')
    assert not prop.is_valid('#00AaFg')
    assert not prop.is_valid('#00AaFff')
    assert not prop.is_valid('blue')
    assert not prop.is_valid('BLUE')
    assert not prop.is_valid('foobar')

def Test_RGB_test_has_ref(self) -> None:
    prop = bcpc.RGB()
    assert not prop.has_ref

def Test_RGB_test_str(self) -> None:
    prop = bcpc.RGB()
    assert str(prop) == 'RGB'

def Test_ColorHex_test_transform(self) -> None:
    prop = bcpc.ColorHex()
    assert prop.transform('#ff0000') == '#ff0000'
    assert prop.transform((255, 0, 0)) == '#ff0000'
    assert prop.transform((255, 0, 0, 0.1)) == '#ff0000'
    assert prop.transform('red') == '#ff0000'
    assert prop.transform('RED') == '#ff0000'
    assert prop.transform('rgba(255, 0, 0, 0.1)') == '#ff0000'
    assert prop.transform('rgb(255, 0, 0)') == '#ff0000'
    assert prop.transform(RGB(255, 0, 0)) == '#ff0000'