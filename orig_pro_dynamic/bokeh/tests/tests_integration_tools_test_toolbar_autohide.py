import pytest
pytest
from selenium.webdriver.common.action_chains import ActionChains
from bokeh.plotting import figure
pytest_plugins = ('bokeh._testing.plugins.project',)

def Test_Toobar_Autohide_test_toolbar_is_visible_by_default_and_stays_visible(self, single_plot_page) -> None:
    plot = figure(height=800, width=1000)
    plot.rect(x=[1, 2], y=[1, 1], width=1, height=1)
    page = single_plot_page(plot)
    assert page.driver.find_element_by_class_name('bk-toolbar').value_of_css_property('visibility') == 'visible'
    ActionChains(page.driver).move_to_element(page.canvas).perform()
    assert page.driver.find_element_by_class_name('bk-toolbar').value_of_css_property('visibility') == 'visible'
    page.drag_canvas_at_position(100, 100, 20, 20)
    assert page.driver.find_element_by_class_name('bk-toolbar').value_of_css_property('visibility') == 'visible'
    assert page.has_no_console_errors()

def Test_Toobar_Autohide_test_toolbar_with_autohide_becomes_visible_when_cursor_is_over_plot(self, single_plot_page) -> None:
    plot = figure(height=800, width=1000)
    plot.toolbar.autohide = True
    plot.rect(x=[1, 2], y=[1, 1], width=1, height=1)
    page = single_plot_page(plot)
    assert page.driver.find_element_by_class_name('bk-toolbar').value_of_css_property('visibility') == 'hidden'
    ActionChains(page.driver).move_to_element(page.canvas).perform()
    assert page.driver.find_element_by_class_name('bk-toolbar').value_of_css_property('visibility') == 'visible'
    page.drag_canvas_at_position(100, 100, 20, 20)
    plot.tools
    assert page.driver.find_element_by_class_name('bk-toolbar').value_of_css_property('visibility') == 'visible'
    button = page.get_toolbar_button('reset')
    button.click()
    assert page.driver.find_element_by_class_name('bk-toolbar').value_of_css_property('visibility') == 'visible'
    assert page.has_no_console_errors()