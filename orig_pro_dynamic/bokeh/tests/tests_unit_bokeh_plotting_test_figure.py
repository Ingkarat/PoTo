import pytest
pytest
import re
from bokeh.core.enums import MarkerType
from bokeh.core.properties import value
from bokeh.models import BoxZoomTool, Circle, ColumnDataSource, LassoSelectTool, Legend, LinearAxis, LogScale, PanTool, ResetTool, Scatter, Title
from bokeh.plotting import _figure as bpf

def Test_figure_legends_DEPRECATED(obejct):

    def test_glyph_label_is_legend_if_column_in_datasource_is_added_as_legend(self, p, source) -> None:
        p.circle(x='x', y='y', legend='label', source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].label == {'field': 'label'}

    def test_glyph_label_is_value_if_column_not_in_datasource_is_added_as_legend(self, p, source) -> None:
        p.circle(x='x', y='y', legend='milk', source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].label == {'value': 'milk'}

    def test_glyph_label_is_legend_if_column_in_df_datasource_is_added_as_legend(self, p, pd) -> None:
        source = pd.DataFrame(data=dict(x=[1, 2, 3], y=[1, 2, 3], label=['a', 'b', 'c']))
        p.circle(x='x', y='y', legend='label', source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].label == {'field': 'label'}

    def test_glyph_label_is_value_if_column_not_in_df_datasource_is_added_as_legend(self, p, pd) -> None:
        source = pd.DataFrame(data=dict(x=[1, 2, 3], y=[1, 2, 3], label=['a', 'b', 'c']))
        p.circle(x='x', y='y', legend='milk', source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].label == {'value': 'milk'}

    def test_glyph_label_is_just_added_directly_if_not_string(self, p, source) -> None:
        p.circle(x='x', y='y', legend={'field': 'milk'}, source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].label == {'field': 'milk'}

    def test_no_legend_if_legend_is_none(self, p, source) -> None:
        p.circle(x='x', y='y', legend=None, source=source)
        legends = p.select(Legend)
        assert len(legends) == 0

    def test_legend_added_when_legend_set(self, p, source) -> None:
        renderer = p.circle(x='x', y='y', legend='label', source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].renderers == [renderer]

    def test_legend_not_added_when_no_legend(self, p, source) -> None:
        p.circle(x='x', y='y', source=source)
        legends = p.select(Legend)
        assert len(legends) == 0

    def test_adding_legend_doesnt_work_when_legends_already_added(self, p, source) -> None:
        p.add_layout(Legend())
        p.add_layout(Legend())
        with pytest.raises(RuntimeError):
            p.circle(x='x', y='y', legend='label', source=source)

    def test_multiple_renderers_correctly_added_to_legend(self, p, source) -> None:
        square = p.square(x='x', y='y', legend='square', source=source)
        circle = p.circle(x='x', y='y', legend='circle', source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].renderers == [square]
        assert legends[0].items[0].label == value('square')
        assert legends[0].items[1].renderers == [circle]
        assert legends[0].items[1].label == value('circle')

    def test_compound_legend_behavior_initiated_if_labels_are_same_on_multiple_renderers(self, p, source) -> None:
        square = p.square(x='x', y='y', legend='compound legend string')
        circle = p.circle(x='x', y='y', legend='compound legend string')
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].renderers == [square, circle]
        assert legends[0].items[0].label == value('compound legend string')

    def test_compound_legend_behavior_initiated_if_labels_are_same_on_multiple_renderers_and_are_field(self, p, source) -> None:
        square = p.square(x='x', y='y', legend='label', source=source)
        circle = p.circle(x='x', y='y', legend='label', source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].renderers == [square, circle]
        assert legends[0].items[0].label == {'field': 'label'}

def Test_figure_legends(obejct):

    def test_glyph_legend_field(self, p, source) -> None:
        p.circle(x='x', y='y', legend_field='label', source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].label == {'field': 'label'}

    def test_no_legend_if_legend_is_none(self, p, source) -> None:
        p.circle(x='x', y='y', legend_label=None, source=source)
        legends = p.select(Legend)
        assert len(legends) == 0

    def test_legend_added_when_legend_set(self, p, source) -> None:
        renderer = p.circle(x='x', y='y', legend_label='label', source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].renderers == [renderer]

    def test_legend_not_added_when_no_legend(self, p, source) -> None:
        p.circle(x='x', y='y', source=source)
        legends = p.select(Legend)
        assert len(legends) == 0

    def test_adding_legend_doesnt_work_when_legends_already_added(self, p, source) -> None:
        p.add_layout(Legend())
        p.add_layout(Legend())
        with pytest.raises(RuntimeError):
            p.circle(x='x', y='y', legend_label='label', source=source)
        with pytest.raises(RuntimeError):
            p.circle(x='x', y='y', legend_field='label', source=source)
        with pytest.raises(RuntimeError):
            p.circle(x='x', y='y', legend_group='label', source=source)

    def test_multiple_renderers_correctly_added_to_legend(self, p, source) -> None:
        square = p.square(x='x', y='y', legend_label='square', source=source)
        circle = p.circle(x='x', y='y', legend_label='circle', source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].renderers == [square]
        assert legends[0].items[0].label == value('square')
        assert legends[0].items[1].renderers == [circle]
        assert legends[0].items[1].label == value('circle')

    def test_compound_legend_behavior_initiated_if_labels_are_same_on_multiple_renderers(self, p, source) -> None:
        square = p.square(x='x', y='y', legend_label='compound legend string')
        circle = p.circle(x='x', y='y', legend_label='compound legend string')
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].renderers == [square, circle]
        assert legends[0].items[0].label == value('compound legend string')

    def test_compound_legend_behavior_initiated_if_labels_are_same_on_multiple_renderers_and_are_field(self, p, source) -> None:
        square = p.square(x='x', y='y', legend_field='label', source=source)
        circle = p.circle(x='x', y='y', legend_field='label', source=source)
        legends = p.select(Legend)
        assert len(legends) == 1
        assert legends[0].items[0].renderers == [square, circle]
        assert legends[0].items[0].label == {'field': 'label'}

@pytest.fixture
def source():
    return ColumnDataSource(dict(x=[1, 2, 3], y=[1, 2, 3], label=['a', 'b', 'c']))

@pytest.fixture
def p():
    return bpf.figure()

def TestFigure_test_basic(self) -> None:
    p = bpf.figure()
    q = bpf.figure()
    q.circle([1, 2, 3], [1, 2, 3])
    assert p != q
    r = bpf.figure()
    assert p != r
    assert q != r

def TestFigure_test_width_height(self) -> None:
    p = bpf.figure(width=100, height=120)
    assert p.plot_width == 100
    assert p.plot_height == 120
    p = bpf.figure(plot_width=100, plot_height=120)
    assert p.plot_width == 100
    assert p.plot_height == 120
    with pytest.raises(ValueError):
        bpf.figure(plot_width=100, width=120)
    with pytest.raises(ValueError):
        bpf.figure(plot_height=100, height=120)

def TestFigure_test_xaxis(self) -> None:
    p = bpf.figure()
    p.circle([1, 2, 3], [1, 2, 3])
    assert len(p.xaxis) == 1
    expected = set(p.xaxis)
    ax = LinearAxis()
    expected.add(ax)
    p.above.append(ax)
    assert set(p.xaxis) == expected
    ax2 = LinearAxis()
    expected.add(ax2)
    p.above.append(ax2)
    assert set(p.xaxis) == expected
    p.left.append(LinearAxis())
    assert set(p.xaxis) == expected
    p.right.append(LinearAxis())
    assert set(p.xaxis) == expected

def TestFigure_test_yaxis(self) -> None:
    p = bpf.figure()
    p.circle([1, 2, 3], [1, 2, 3])
    assert len(p.yaxis) == 1
    expected = set(p.yaxis)
    ax = LinearAxis()
    expected.add(ax)
    p.right.append(ax)
    assert set(p.yaxis) == expected
    ax2 = LinearAxis()
    expected.add(ax2)
    p.right.append(ax2)
    assert set(p.yaxis) == expected
    p.above.append(LinearAxis())
    assert set(p.yaxis) == expected
    p.below.append(LinearAxis())
    assert set(p.yaxis) == expected

def TestFigure_test_axis(self) -> None:
    p = bpf.figure()
    p.circle([1, 2, 3], [1, 2, 3])
    assert len(p.axis) == 2
    expected = set(p.axis)
    ax = LinearAxis()
    expected.add(ax)
    p.above.append(ax)
    assert set(p.axis) == expected
    ax2 = LinearAxis()
    expected.add(ax2)
    p.below.append(ax2)
    assert set(p.axis) == expected
    ax3 = LinearAxis()
    expected.add(ax3)
    p.left.append(ax3)
    assert set(p.axis) == expected
    ax4 = LinearAxis()
    expected.add(ax4)
    p.right.append(ax4)
    assert set(p.axis) == expected

def TestFigure_test_log_axis(self) -> None:
    p = bpf.figure(x_axis_type='log')
    p.circle([1, 2, 3], [1, 2, 3])
    assert isinstance(p.x_scale, LogScale)
    p = bpf.figure(y_axis_type='log')
    p.circle([1, 2, 3], [1, 2, 3])
    assert isinstance(p.y_scale, LogScale)

def TestFigure_test_grid_tickers(self) -> None:
    p = bpf.figure()
    assert p.xgrid[0].axis == p.xaxis[0]
    assert p.xgrid[0].ticker is None
    assert p.ygrid[0].axis == p.yaxis[0]
    assert p.ygrid[0].ticker is None

def TestFigure_test_xgrid(self) -> None:
    p = bpf.figure()
    p.circle([1, 2, 3], [1, 2, 3])
    assert len(p.xgrid) == 1
    assert p.xgrid[0].dimension == 0

def TestFigure_test_ygrid(self) -> None:
    p = bpf.figure()
    p.circle([1, 2, 3], [1, 2, 3])
    assert len(p.ygrid) == 1
    assert p.ygrid[0].dimension == 1

def TestFigure_test_grid(self) -> None:
    p = bpf.figure()
    p.circle([1, 2, 3], [1, 2, 3])
    assert len(p.grid) == 2

def TestFigure_test_tools(self) -> None:
    TOOLS = 'pan,box_zoom,reset,lasso_select'
    fig = bpf.figure(tools=TOOLS)
    expected = [PanTool, BoxZoomTool, ResetTool, LassoSelectTool]
    assert len(fig.tools) == len(expected)
    for (i, _type) in enumerate(expected):
        assert isinstance(fig.tools[i], _type)

def TestFigure_test_plot_fill_props(self) -> None:
    p = bpf.figure(background_fill_color='red', background_fill_alpha=0.5, border_fill_color='blue', border_fill_alpha=0.8)
    assert p.background_fill_color == 'red'
    assert p.background_fill_alpha == 0.5
    assert p.border_fill_color == 'blue'
    assert p.border_fill_alpha == 0.8
    p.background_fill_color = 'green'
    p.border_fill_color = 'yellow'
    assert p.background_fill_color == 'green'
    assert p.border_fill_color == 'yellow'

def TestFigure_test_title_kwarg_no_warning(self, recwarn) -> None:
    bpf.figure(title='title')
    assert len(recwarn) == 0

def TestFigure_test_title_should_accept_Title(self) -> None:
    title = Title(text='Great Title')
    plot = bpf.figure(title=title)
    plot.line([1, 2, 3], [1, 2, 3])
    assert plot.title.text == 'Great Title'

def TestFigure_test_title_should_accept_string(self) -> None:
    plot = bpf.figure(title='Great Title 2')
    plot.line([1, 2, 3], [1, 2, 3])
    assert plot.title.text == 'Great Title 2'

def TestFigure_test_columnsource_auto_conversion_from_dict(self) -> None:
    p = bpf.figure()
    dct = {'x': [1, 2, 3], 'y': [2, 3, 4]}
    p.circle(x='x', y='y', source=dct)

def TestFigure_test_columnsource_auto_conversion_from_pandas(self, pd) -> None:
    p = bpf.figure()
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 3, 4]})
    p.circle(x='x', y='y', source=df)

def TestFigure_test_glyph_method_errors_on_sequence_literals_with_source(self) -> None:
    p = bpf.figure()
    source = ColumnDataSource({'x': [1, 2, 3], 'y': [2, 3, 4]})
    with pytest.raises(RuntimeError, match='Expected y to reference fields in the supplied data source.'):
        p.circle(x='x', y=[1, 2, 3], source=source)
    with pytest.raises(RuntimeError, match='Expected y and line_color to reference fields in the supplied data source.'):
        p.circle(x='x', y=[1, 2, 3], line_color=['red', 'green', 'blue'], source=source)
    with pytest.raises(RuntimeError) as e:
        p.circle(x='x', y=[1, 2, 3], color=['red', 'green', 'blue'], source=source)
    m = re.search('Expected y, (.+) and (.+) to reference fields in the supplied data source.', str(e.value))
    assert m is not None
    assert set(m.groups()) == {'fill_color', 'line_color'}

@pytest.mark.parametrize('marker', list(MarkerType))
def TestMarkers_test_mixed_inputs(self, marker) -> None:
    marker = list(MarkerType)[0]
    p = bpf.figure()
    rgb = (100, 0, 0)
    rgb_other = (0, 100, 0)
    alpha1 = 0.5
    alpha2 = 0.75
    func = getattr(p, marker)
    r = func([1, 2, 3], [1, 2, 3], color=rgb, line_color=rgb_other)
    assert r.glyph.fill_color == rgb
    assert r.glyph.line_color == rgb_other
    r = func([1, 2, 3], [1, 2, 3], color=rgb, fill_color=rgb_other)
    assert r.glyph.line_color == rgb
    assert r.glyph.fill_color == rgb_other
    r = func([1, 2, 3], [1, 2, 3], color=rgb, alpha=alpha1, line_alpha=alpha2)
    assert r.glyph.line_alpha == alpha2
    assert r.glyph.fill_alpha == alpha1

@pytest.mark.parametrize('marker', list(MarkerType))
@pytest.mark.parametrize('color', [(100.0, 100.0, 100.0), (50.0, 100.0, 50.0, 0.5), (100, 100, 100), (50, 100, 50, 0.5)])
def TestMarkers_test_color_input(self, color, marker) -> None:
    marker = list(MarkerType)[0]
    color = (100.0, 100.0, 100.0)
    p = bpf.figure()
    func = getattr(p, marker)
    r = func([1, 2, 3], [1, 2, 3], color=color)
    assert r.glyph.line_color == color
    assert r.glyph.fill_color == color
    for v in r.glyph.line_color[0:3]:
        assert isinstance(v, int)
    for v in r.glyph.fill_color[0:3]:
        assert isinstance(v, int)

@pytest.mark.parametrize('marker', list(MarkerType))
@pytest.mark.parametrize('color', [(100.0, 100.0, 100.0), (50.0, 100.0, 50.0, 0.5), (100, 100, 100), (50, 100, 50, 0.5)])
def TestMarkers_test_line_color_input(self, color, marker) -> None:
    marker = list(MarkerType)[0]
    color = (100.0, 100.0, 100.0)
    p = bpf.figure()
    func = getattr(p, marker)
    r = func([1, 2, 3], [1, 2, 3], line_color=color)
    assert r.glyph.line_color == color
    for v in r.glyph.line_color[0:3]:
        assert isinstance(v, int)

@pytest.mark.parametrize('marker', list(MarkerType))
@pytest.mark.parametrize('color', [(100.0, 100.0, 100.0), (50.0, 100.0, 50.0, 0.5), (50, 100, 50, 0.5)])
def TestMarkers_test_fill_color_input(self, color, marker) -> None:
    marker = list(MarkerType)[0]
    color = (100.0, 100.0, 100.0)
    p = bpf.figure()
    func = getattr(p, marker)
    r = func([1, 2, 3], [1, 2, 3], fill_color=color)
    assert r.glyph.fill_color == color
    for v in r.glyph.fill_color[0:3]:
        assert isinstance(v, int)

@pytest.mark.parametrize('marker', list(MarkerType))
def TestMarkers_test_render_level(self, marker) -> None:
    marker = list(MarkerType)[0]
    p = bpf.figure()
    func = getattr(p, marker)
    r = func([1, 2, 3], [1, 2, 3], level='underlay')
    assert r.level == 'underlay'
    with pytest.raises(ValueError):
        p.circle([1, 2, 3], [1, 2, 3], level='bad_input')

@pytest.mark.parametrize('marker', list(MarkerType))
def Test_scatter_test_marker_value(self, marker) -> None:
    marker = list(MarkerType)[0]
    p = bpf.figure()
    r = p.scatter([1, 2, 3], [1, 2, 3], marker=marker)
    assert isinstance(r.glyph, Scatter)
    assert r.glyph.marker == marker

def Test_scatter_test_marker_column(self) -> None:
    p = bpf.figure()
    data = dict(x=[1, 2, 3], y=[1, 2, 3], foo=['hex', 'square', 'circle'])
    r = p.scatter('x', 'y', marker='foo', source=data)
    assert isinstance(r.glyph, Scatter)
    assert r.glyph.marker == 'foo'

def Test_scatter_test_circle_with_radius(self) -> None:
    p = bpf.figure()
    r = p.scatter([1, 2, 3], [1, 2, 3], marker='circle', radius=0.2)
    assert isinstance(r.glyph, Circle)
    assert r.glyph.radius == 0.2

def Test_hbar_stack_test_returns_renderers(self) -> None:
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    years = ['2015', '2016', '2017']
    colors = ['#c9d9d3', '#718dbf', '#e84d60']
    data = {'fruits': fruits, '2015': [2, 1, 4, 3, 2, 4], '2016': [5, 3, 4, 2, 4, 6], '2017': [3, 2, 4, 4, 5, 3]}
    source = ColumnDataSource(data=data)
    p = bpf.figure()
    renderers = p.hbar_stack(years, y='fruits', height=0.9, color=colors, source=source, legend_label=years, name=years)
    assert len(renderers) == 3
    assert renderers[0].name == '2015'
    assert renderers[1].name == '2016'
    assert renderers[2].name == '2017'

def Test_vbar_stack_test_returns_renderers(self) -> None:
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    years = ['2015', '2016', '2017']
    colors = ['#c9d9d3', '#718dbf', '#e84d60']
    data = {'fruits': fruits, '2015': [2, 1, 4, 3, 2, 4], '2016': [5, 3, 4, 2, 4, 6], '2017': [3, 2, 4, 4, 5, 3]}
    source = ColumnDataSource(data=data)
    p = bpf.figure()
    renderers = p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=source, legend_label=years, name=years)
    assert len(renderers) == 3
    assert renderers[0].name == '2015'
    assert renderers[1].name == '2016'
    assert renderers[2].name == '2017'