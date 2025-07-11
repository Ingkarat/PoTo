import pytest
pytest
from bokeh._testing.util.selenium import RECORD
from bokeh.models import ColumnDataSource, CustomAction, CustomJS, PanTool, Plot, Range1d, Rect
pytest_plugins = ('bokeh._testing.plugins.project',)

def _make_plot(dimensions='both'):
    source = ColumnDataSource(dict(x=[1, 2], y=[1, 1]))
    plot = Plot(plot_height=400, plot_width=400, x_range=Range1d(0, 1), y_range=Range1d(0, 1), min_border=0)
    plot.add_glyph(source, Rect(x='x', y='y', width=0.9, height=0.9))
    plot.add_tools(PanTool(dimensions=dimensions))
    code = RECORD('xrstart', 'p.x_range.start', final=False) + RECORD('xrend', 'p.x_range.end', final=False) + RECORD('yrstart', 'p.y_range.start', final=False) + RECORD('yrend', 'p.y_range.end')
    plot.add_tools(CustomAction(callback=CustomJS(args=dict(p=plot), code=code)))
    plot.toolbar_sticky = False
    return plot
_css = dict(both='pan', width='xpan', height='ypan')

@pytest.mark.parametrize('dim', ['both', 'width', 'height'])
def Test_PanTool_test_selected_by_default(self, dim, single_plot_page) -> None:
    dim = 'both'
    plot = _make_plot(dim)
    page = single_plot_page(plot)
    target = 'bk-tool-icon-%s' % _css[dim]
    button = page.driver.find_element_by_class_name(target)
    assert 'active' in button.get_attribute('class')
    assert page.has_no_console_errors()

@pytest.mark.parametrize('dim', ['both', 'width', 'height'])
def Test_PanTool_test_can_be_deselected_and_selected(self, dim, single_plot_page) -> None:
    dim = 'both'
    plot = _make_plot(dim)
    page = single_plot_page(plot)
    target = 'bk-tool-icon-%s' % _css[dim]
    button = page.driver.find_element_by_class_name(target)
    assert 'active' in button.get_attribute('class')
    button = page.driver.find_element_by_class_name(target)
    button.click()
    assert 'active' not in button.get_attribute('class')
    button = page.driver.find_element_by_class_name(target)
    button.click()
    assert 'active' in button.get_attribute('class')
    assert page.has_no_console_errors()

@pytest.mark.parametrize('dim', ['both', 'width', 'height'])
def Test_PanTool_test_pan_has_no_effect_when_deslected(self, dim, single_plot_page) -> None:
    dim = 'both'
    plot = _make_plot(dim)
    page = single_plot_page(plot)
    target = 'bk-tool-icon-%s' % _css[dim]
    button = page.driver.find_element_by_class_name(target)
    button.click()
    page.drag_canvas_at_position(100, 100, 20, 20)
    page.click_custom_action()
    results = page.results
    assert results['xrstart'] == 0
    assert results['xrend'] == 1
    assert results['yrstart'] == 0
    assert results['yrend'] == 1
    assert page.has_no_console_errors()

def Test_PanTool_test_pan_updates_both_ranges(self, single_plot_page) -> None:
    plot = _make_plot()
    page = single_plot_page(plot)
    page.drag_canvas_at_position(100, 100, 20, 20)
    page.click_custom_action()
    results = page.results
    assert results['xrstart'] < 0
    assert results['xrend'] < 1
    assert results['yrstart'] > 0
    assert results['yrend'] > 1
    assert page.has_no_console_errors()

def Test_PanTool_test_xpan_upates_only_xrange(self, single_plot_page) -> None:
    plot = _make_plot('width')
    page = single_plot_page(plot)
    page.drag_canvas_at_position(100, 100, 20, 20)
    page.click_custom_action()
    results = page.results
    assert results['xrstart'] < 0
    assert results['xrend'] < 1
    assert results['yrstart'] == 0
    assert results['yrend'] == 1
    assert page.has_no_console_errors()

def Test_PanTool_test_ypan_updates_only_yrange(self, single_plot_page) -> None:
    plot = _make_plot('height')
    page = single_plot_page(plot)
    page.drag_canvas_at_position(100, 100, 20, 20)
    page.click_custom_action()
    results = page.results
    assert results['xrstart'] == 0
    assert results['xrend'] == 1
    assert results['yrstart'] > 0
    assert results['yrend'] > 1
    assert page.has_no_console_errors()