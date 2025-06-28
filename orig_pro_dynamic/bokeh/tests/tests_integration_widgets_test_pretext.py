import pytest
pytest
from html import escape
from bokeh.models import PreText
pytest_plugins = ('bokeh._testing.plugins.project',)
text = '\nYour <a href="https://en.wikipedia.org/wiki/HTML">HTML</a>-supported text is initialized with the <b>text</b> argument.  The\nremaining div arguments are <b>width</b> and <b>height</b>. For this example, those values\nare <i>200</i> and <i>100</i> respectively.'

def Test_PreText_test_displays_div_as_text(self, bokeh_model_page) -> None:
    para = PreText(text=text, css_classes=['foo'])
    page = bokeh_model_page(para)
    el = page.driver.find_element_by_css_selector('.foo div pre')
    assert el.get_attribute('innerHTML') == escape(text, quote=None)
    assert page.has_no_console_errors()

def Test_PreText_test_set_style(self, bokeh_model_page) -> None:
    para = PreText(text=text, css_classes=['foo'], style={'font-size': '26px'})
    page = bokeh_model_page(para)
    el = page.driver.find_element_by_css_selector('.foo div')
    assert 'font-size: 26px;' in el.get_attribute('style')
    assert page.has_no_console_errors()