import pytest
pytest
from bokeh._testing.util.selenium import RECORD
from bokeh.models import ColumnDataSource, CustomAction, CustomJS, Plot, Range1d, RangeTool, Rect
pytest_plugins = ('bokeh._testing.plugins.project',)

def _make_plot():
    source = ColumnDataSource(dict(x=[1, 2], y=[1, 1]))
    r = Range1d(start=0.4, end=0.6)
    plot = Plot(plot_height=400, plot_width=1100, x_range=Range1d(0, 1), y_range=Range1d(0, 1), min_border=0)
    plot.add_glyph(source, Rect(x='x', y='y', width=0.9, height=0.9))
    tool = RangeTool(x_range=r)
    plot.add_tools(tool)
    plot.min_border_right = 100
    code = RECORD('start', 't.x_range.start', final=False) + RECORD('end', 't.x_range.end')
    plot.add_tools(CustomAction(callback=CustomJS(args=dict(t=tool), code=code)))
    plot.toolbar_sticky = False
    return plot

def Test_RangeTool_test_selected_by_default(self, single_plot_page) -> None:
    plot = _make_plot()
    page = single_plot_page(plot)
    target = 'range'
    button = page.get_toolbar_button(target)
    assert 'active' in button.get_attribute('class')
    assert page.has_no_console_errors()

def Test_RangeTool_test_can_be_deselected_and_selected(self, single_plot_page) -> None:
    plot = _make_plot()
    page = single_plot_page(plot)
    target = 'range'
    button = page.get_toolbar_button(target)
    assert 'active' in button.get_attribute('class')
    button = page.get_toolbar_button(target)
    button.click()
    assert 'active' not in button.get_attribute('class')
    button = page.get_toolbar_button(target)
    button.click()
    assert 'active' in button.get_attribute('class')
    assert page.has_no_console_errors()

def Test_RangeTool_test_center_pan_has_no_effect_when_deselected(self, single_plot_page) -> None:
    plot = _make_plot()
    page = single_plot_page(plot)
    target = 'range'
    button = page.get_toolbar_button(target)
    button.click()
    page.drag_canvas_at_position(500, 200, 100, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.4
    assert results['end'] == 0.6
    assert page.has_no_console_errors()

def Test_RangeTool_test_center_pan_updates_range_when_selected(self, single_plot_page) -> None:
    plot = _make_plot()
    page = single_plot_page(plot)
    page.drag_canvas_at_position(500, 200, 100, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.5
    assert results['end'] == 0.7
    page.drag_canvas_at_position(600, 200, -300, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.2
    assert results['end'] == 0.4
    assert page.has_no_console_errors()

def Test_RangeTool_test_center_pan_with_right_side_outside(self, single_plot_page) -> None:
    plot = _make_plot()
    plot.tools[0].x_range.end = 1.1
    page = single_plot_page(plot)
    page.drag_canvas_at_position(500, 200, 100, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.5
    assert results['end'] == 1.2
    page.drag_canvas_at_position(600, 200, -300, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.2
    assert results['end'] == 0.9
    assert page.has_no_console_errors()

def Test_RangeTool_test_center_pan_with_left_side_outside(self, single_plot_page) -> None:
    plot = _make_plot()
    plot.tools[0].x_range.start = -0.1
    page = single_plot_page(plot)
    page.drag_canvas_at_position(500, 200, -100, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == -0.2
    assert results['end'] == 0.5
    page.drag_canvas_at_position(400, 200, 300, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.1
    assert results['end'] == 0.8
    assert page.has_no_console_errors()

def Test_RangeTool_test_left_edge_drag_updates_start(self, single_plot_page) -> None:
    plot = _make_plot()
    page = single_plot_page(plot)
    page.drag_canvas_at_position(400, 200, 100, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.5
    assert results['end'] == 0.6
    page.drag_canvas_at_position(500, 200, -300, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.2
    assert results['end'] == 0.6

def Test_RangeTool_test_left_edge_drag_can_flip(self, single_plot_page) -> None:
    plot = _make_plot()
    page = single_plot_page(plot)
    page.drag_canvas_at_position(400, 200, 300, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.6
    assert results['end'] == 0.7

def Test_RangeTool_test_left_edge_drag_with_right_edge_outside(self, single_plot_page) -> None:
    plot = _make_plot()
    plot.tools[0].x_range.end = 1.1
    page = single_plot_page(plot)
    page.drag_canvas_at_position(400, 200, 300, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.7
    assert results['end'] == 1.1

def Test_RangeTool_test_right_edge_drag_updates_end(self, single_plot_page) -> None:
    plot = _make_plot()
    page = single_plot_page(plot)
    page.drag_canvas_at_position(600, 200, 100, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.4
    assert results['end'] == 0.7
    page.drag_canvas_at_position(700, 200, -200, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.4
    assert results['end'] == 0.5

def Test_RangeTool_test_right_edge_drag_can_flip(self, single_plot_page) -> None:
    plot = _make_plot()
    page = single_plot_page(plot)
    page.drag_canvas_at_position(600, 200, -300, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.3
    assert results['end'] == 0.4

def Test_RangeTool_test_right_edge_drag_with_left_edge_outside(self, single_plot_page) -> None:
    plot = _make_plot()
    plot.tools[0].x_range.start = -0.1
    page = single_plot_page(plot)
    page.drag_canvas_at_position(600, 200, -300, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == -0.1
    assert results['end'] == 0.3

@pytest.mark.skip
def Test_RangeTool_test_center_pan_stops_at_plot_range_limit(self, single_plot_page) -> None:
    plot = _make_plot()
    page = single_plot_page(plot)
    page.drag_canvas_at_position(500, 200, 300, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.7
    assert results['end'] == 0.9
    page.drag_canvas_at_position(800, 200, 150, 0)
    page.click_custom_action()
    results = page.results
    assert results['start'] == 0.8
    assert results['end'] == 1
    assert page.has_no_console_errors()