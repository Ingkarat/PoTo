import pytest
pytest
import mock
from mock import patch
from bokeh.core.validation import check_integrity
from bokeh.models import CategoricalScale, DataRange1d, FactorRange, GlyphRenderer, Label, LinearAxis, LinearScale, LogScale, PanTool, Plot, Range1d
from bokeh.plotting import figure
import bokeh.models.plots as bmp
_LEGEND_EMPTY_WARNING = '\nYou are attempting to set `plot.legend.location` on a plot that has zero legends added, this will have no effect.\n\nBefore legend properties can be set, you must add a Legend explicitly, or call a glyph method with a legend parameter set.\n'

def test_plot_add_layout_raises_error_if_not_render() -> None:
    plot = figure()
    with pytest.raises(ValueError):
        plot.add_layout(Range1d())

def test_plot_add_layout_adds_label_to_plot_renderers() -> None:
    plot = figure()
    label = Label()
    plot.add_layout(label)
    assert label in plot.center

def test_plot_add_layout_adds_axis_to_renderers_and_side_renderers() -> None:
    plot = figure()
    axis = LinearAxis()
    plot.add_layout(axis, 'left')
    assert axis in plot.left

def test_sizing_mode_property_is_fixed_by_default() -> None:
    plot = figure()
    assert plot.sizing_mode is None

def test_plot_with_no_title_specified_creates_an_empty_title() -> None:
    plot = Plot()
    assert plot.title.text == ''

def test_plot__scale_classmethod() -> None:
    assert isinstance(Plot._scale('auto'), LinearScale)
    assert isinstance(Plot._scale('linear'), LinearScale)
    assert isinstance(Plot._scale('log'), LogScale)
    assert isinstance(Plot._scale('categorical'), CategoricalScale)
    with pytest.raises(ValueError):
        Plot._scale('malformed_type')

def test__check_required_scale_has_scales() -> None:
    plot = Plot()
    check = plot._check_required_scale()
    assert check == []

def test__check_required_scale_missing_scales() -> None:
    plot = Plot(x_scale=None, y_scale=None)
    check = plot._check_required_scale()
    assert check != []

def test__check_compatible_scale_and_ranges_compat_numeric() -> None:
    plot = Plot(x_scale=LinearScale(), x_range=Range1d())
    check = plot._check_compatible_scale_and_ranges()
    assert check == []
    plot = Plot(y_scale=LogScale(), y_range=DataRange1d())
    check = plot._check_compatible_scale_and_ranges()
    assert check == []

def test__check_compatible_scale_and_ranges_compat_factor() -> None:
    plot = Plot(x_scale=CategoricalScale(), x_range=FactorRange())
    check = plot._check_compatible_scale_and_ranges()
    assert check == []

def test__check_compatible_scale_and_ranges_incompat_numeric_scale_and_factor_range() -> None:
    plot = Plot(x_scale=LinearScale(), x_range=FactorRange())
    check = plot._check_compatible_scale_and_ranges()
    assert check != []

def test__check_compatible_scale_and_ranges_incompat_factor_scale_and_numeric_range() -> None:
    plot = Plot(x_scale=CategoricalScale(), x_range=DataRange1d())
    check = plot._check_compatible_scale_and_ranges()
    assert check != []

def TestPlotLegendProperty_test_basic(self) -> None:
    plot = figure(tools='')
    x = plot.legend
    assert isinstance(x, bmp._list_attr_splat)
    assert len(x) == 0
    plot.circle([1, 2], [3, 4], legend_label='foo')
    x = plot.legend
    assert isinstance(x, bmp._list_attr_splat)
    assert len(x) == 1

def TestPlotLegendProperty_test_warnign(self) -> None:
    plot = figure(tools='')
    with pytest.warns(UserWarning) as warns:
        plot.legend.location = 'above'
        assert len(warns) == 1
        assert warns[0].message.args[0] == _LEGEND_EMPTY_WARNING

def TestPlotSelect_setup_method(self):
    self._plot = figure(tools='pan')
    figure(tools='pan').circle([1, 2, 3], [3, 2, 1], name='foo')

@patch('bokeh.models.plots.find')
def TestPlotSelect_test_string_arg(self, mock_find) -> None:
    figure(tools='pan').select('foo')
    assert mock_find.called
    assert mock_find.call_args[0][1] == dict(name='foo')

@patch('bokeh.models.plots.find')
def TestPlotSelect_test_type_arg(self, mock_find) -> None:
    figure(tools='pan').select(PanTool)
    assert mock_find.called
    assert mock_find.call_args[0][1] == dict(type=PanTool)

@patch('bokeh.models.plots.find')
def TestPlotSelect_test_kwargs(self, mock_find) -> None:
    kw = dict(name='foo', type=GlyphRenderer)
    figure(tools='pan').select(**kw)
    assert mock_find.called
    assert mock_find.call_args[0][1] == kw

@patch('bokeh.models.plots.find')
def TestPlotSelect_test_single_selector_kwarg(self, mock_find) -> None:
    kw = dict(name='foo', type=GlyphRenderer)
    figure(tools='pan').select(selector=kw)
    assert mock_find.called
    assert mock_find.call_args[0][1] == kw

def TestPlotSelect_test_selector_kwarg_and_extra_kwargs(self) -> None:
    with pytest.raises(TypeError) as exc:
        figure(tools='pan').select(selector=dict(foo='foo'), bar='bar')
    assert "when passing 'selector' keyword arg, not other keyword args may be present" == str(exc.value)

def TestPlotSelect_test_bad_arg_type(self) -> None:
    with pytest.raises(TypeError) as exc:
        figure(tools='pan').select(10)
    assert 'selector must be a dictionary, string or plot object.' == str(exc.value)

def TestPlotSelect_test_too_many_args(self) -> None:
    with pytest.raises(TypeError) as exc:
        figure(tools='pan').select('foo', 'bar')
    assert 'select accepts at most ONE positional argument.' == str(exc.value)

def TestPlotSelect_test_no_input(self) -> None:
    with pytest.raises(TypeError) as exc:
        figure(tools='pan').select()
    assert 'select requires EITHER a positional argument, OR keyword arguments.' == str(exc.value)

def TestPlotSelect_test_arg_and_kwarg(self) -> None:
    with pytest.raises(TypeError) as exc:
        figure(tools='pan').select('foo', type=PanTool)
    assert 'select accepts EITHER a positional argument, OR keyword arguments (not both).' == str(exc.value)

def TestPlotValidation_test_missing_renderers(self) -> None:
    p = figure()
    p.renderers = []
    with mock.patch('bokeh.core.validation.check.log') as mock_logger:
        check_integrity([p])
    assert mock_logger.warning.call_count == 1
    assert mock_logger.warning.call_args[0][0].startswith('W-1000 (MISSING_RENDERERS): Plot has no renderers')

def TestPlotValidation_test_missing_scale(self) -> None:
    p = figure()
    p.x_scale = None
    with mock.patch('bokeh.core.validation.check.log') as mock_logger:
        check_integrity([p])
    assert mock_logger.error.call_count == 1
    assert mock_logger.error.call_args[0][0].startswith('E-1008 (REQUIRED_SCALE): A required Scale object is missing: x_scale')
    p.y_scale = None
    with mock.patch('bokeh.core.validation.check.log') as mock_logger:
        check_integrity([p])
    assert mock_logger.error.call_count == 1
    assert mock_logger.error.call_args[0][0].startswith('E-1008 (REQUIRED_SCALE): A required Scale object is missing: x_scale, y_scale')

def TestPlotValidation_test_missing_range(self) -> None:
    p = figure()
    p.x_range = None
    with mock.patch('bokeh.core.validation.check.log') as mock_logger:
        check_integrity([p])
    assert mock_logger.error.call_count == 1
    assert mock_logger.error.call_args[0][0].startswith('E-1004 (REQUIRED_RANGE): A required Range object is missing: x_range')
    p.y_range = None
    with mock.patch('bokeh.core.validation.check.log') as mock_logger:
        check_integrity([p])
    assert mock_logger.error.call_count == 1
    assert mock_logger.error.call_args[0][0].startswith('E-1004 (REQUIRED_RANGE): A required Range object is missing: x_range, y_range')

def TestPlotValidation_test_bad_extra_range_name(self) -> None:
    p = figure()
    p.xaxis.x_range_name = 'junk'
    with mock.patch('bokeh.core.validation.check.log') as mock_logger:
        check_integrity([p])
    assert mock_logger.error.call_count == 1
    assert mock_logger.error.call_args[0][0].startswith("E-1020 (BAD_EXTRA_RANGE_NAME): An extra range name is configued with a name that does not correspond to any range: x_range_name='junk' [LinearAxis")
    p = figure()
    p.extra_x_ranges['foo'] = Range1d()
    p.grid.x_range_name = 'junk'
    with mock.patch('bokeh.core.validation.check.log') as mock_logger:
        check_integrity([p])
    assert mock_logger.error.call_count == 1
    assert mock_logger.error.call_args[0][0].startswith("E-1020 (BAD_EXTRA_RANGE_NAME): An extra range name is configued with a name that does not correspond to any range: x_range_name='junk' [Grid")
    assert mock_logger.error.call_args[0][0].count('Grid') == 2
    (p, dep) = (figure(), figure())
    dep.extra_x_ranges['foo'] = Range1d()
    dep.grid.x_range_name = 'foo'
    with mock.patch('bokeh.core.validation.check.log') as mock_logger:
        check_integrity([p])
    assert mock_logger.error.call_count == 0

def BaseTwinAxis_verify_axis(self, axis_name):
    plot = Plot()
    range_obj = getattr(plot, f'extra_{axis_name}_ranges')
    range_obj['foo_range'] = self.get_range_instance()
    assert range_obj['foo_range']

def BaseTwinAxis_test_x_range(self) -> None:
    self.verify_axis('x')

def BaseTwinAxis_test_y_range(self) -> None:
    self.verify_axis('y')

@staticmethod
def BaseTwinAxis_get_range_instance():
    raise NotImplementedError

@staticmethod
def TestCategoricalTwinAxis_get_range_instance():
    return FactorRange('foo', 'bar')

@staticmethod
def TestLinearTwinAxis_get_range_instance():
    return Range1d(0, 42)

def Test_list_attr_splat_test_set(self) -> None:
    obj = bmp._list_attr_splat([DataRange1d(), DataRange1d()])
    assert len(obj) == 2
    assert obj[0].start == None
    assert obj[1].start == None
    obj.start = 10
    assert obj[0].start == 10
    assert obj[1].start == 10

def Test_list_attr_splat_test_set_empty(self) -> None:
    obj = bmp._list_attr_splat([])
    assert len(obj) == 0
    obj.start = 10
    assert len(obj) == 0

def Test_list_attr_splat_test_get_set_single(self) -> None:
    p = figure()
    assert len(p.xaxis) == 1
    assert p.xaxis.formatter.power_limit_low != 100
    assert p.xaxis[0].formatter.power_limit_low != 100
    p.axis.formatter.power_limit_low = 100
    assert p.xaxis.formatter.power_limit_low == 100
    assert p.xaxis[0].formatter.power_limit_low == 100

def Test_list_attr_splat_test_get_set_multi(self) -> None:
    p = figure()
    assert len(p.axis) == 2
    assert p.axis[0].formatter.power_limit_low != 100
    assert p.axis[1].formatter.power_limit_low != 100
    assert p.axis.formatter[0].power_limit_low != 100
    assert p.axis.formatter[1].power_limit_low != 100
    p.axis.formatter.power_limit_low = 100
    assert p.axis[0].formatter.power_limit_low == 100
    assert p.axis[1].formatter.power_limit_low == 100
    assert p.axis.formatter[0].power_limit_low == 100
    assert p.axis.formatter[1].power_limit_low == 100

def Test_list_attr_splat_test_get_set_multi_mismatch(self) -> None:
    obj = bmp._list_attr_splat([LinearAxis(), FactorRange()])
    with pytest.raises(AttributeError) as e:
        obj.formatter.power_limit_low == 10
    assert str(e.value).endswith('list items have no %r attribute' % 'formatter')

def Test_list_attr_splat_test_get_empty(self) -> None:
    obj = bmp._list_attr_splat([])
    with pytest.raises(AttributeError) as e:
        obj.start
    assert str(e.value).endswith("Trying to access %r attribute on an empty 'splattable' list" % 'start')

def Test_list_attr_splat_test_get_index(self) -> None:
    obj = bmp._list_attr_splat([1, 2, 3])
    assert obj.index(2) == 1

def Test_list_attr_splat_test_pop_value(self) -> None:
    obj = bmp._list_attr_splat([1, 2, 3])
    obj.pop(1)
    assert obj == [1, 3]