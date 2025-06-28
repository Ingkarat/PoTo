import pytest
pytest
from pytest import raises
from bokeh.models import Slider
from bokeh.models import CustomJS

def test_js_callback() -> None:
    slider = Slider()
    cb = CustomJS(code='foo();', args=dict(x=slider))
    assert 'foo()' in cb.code
    assert cb.args['x'] is slider
    cb = CustomJS(code='foo();', args=dict(x=3))
    assert 'foo()' in cb.code
    assert cb.args['x'] == 3
    with raises(AttributeError):
        CustomJS(code='foo();', x=slider)