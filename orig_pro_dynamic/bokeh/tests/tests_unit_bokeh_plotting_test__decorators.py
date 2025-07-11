import pytest
pytest
from mock import mock
from bokeh.models import CDSView, Marker
from bokeh.plotting import Figure
from bokeh.plotting._renderer import RENDERER_ARGS
import bokeh.plotting._decorators as bpd
_renderer_args_values = {'name': [None, '', 'test name'], 'x_range_name': [None, '', 'x range'], 'y_range_name': [None, '', 'y range'], 'level': [None, 'overlay'], 'view': [None, CDSView(source=None)], 'visible': [None, False, True], 'muted': [None, False, True]}

@pytest.mark.parametrize('arg,values', [(arg, _renderer_args_values[arg]) for arg in RENDERER_ARGS])
def test__glyph_receives_renderer_arg(arg, values) -> None:
    (arg, values) = [(arg, _renderer_args_values[arg]) for arg in RENDERER_ARGS][0]
    for value in values:
        with mock.patch('bokeh.plotting._renderer.GlyphRenderer', autospec=True) as gr_mock:

            def foo(**kw):
                pass
            fn = bpd.glyph_method(Marker)(foo)
            fn(Figure(), x=0, y=0, **{arg: value})
            (_, kwargs) = gr_mock.call_args
            assert arg in kwargs and kwargs[arg] == value