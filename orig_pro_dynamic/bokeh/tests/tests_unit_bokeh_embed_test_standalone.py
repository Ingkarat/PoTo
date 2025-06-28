import pytest
pytest
from collections import OrderedDict
import bs4
from jinja2 import Template
from mock import patch
import bokeh.resources as resources
import bokeh.util.version as buv
from bokeh.document import Document
from bokeh.embed.util import RenderRoot, standalone_docs_json
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.resources import CDN, CSSResources, JSResources
import bokeh.embed.standalone as bes
pytest_plugins = ('bokeh._testing.plugins.project', 'bokeh._testing.plugins.selenium')

def stable_id():
    return 'ID'

@pytest.fixture
def test_plot() -> None:
    from bokeh.plotting import figure
    test_plot = figure(title="'foo'")
    test_plot.circle([1, 2], [2, 3])
    return test_plot
PAGE = Template('\n<!DOCTYPE html>\n<html lang="en">\n<head>\n</head>\n\n<body>\n  <script>\n  {{js}}\n  </script>\n  {{tag}}\n</body>\n')

def Test_autoload_static_test_return_type(self, test_plot) -> None:
    test_plot = test_plot()
    r = bes.autoload_static(test_plot, CDN, 'some/path')
    assert len(r) == 2

def Test_autoload_static_test_script_attrs(self, test_plot) -> None:
    test_plot = test_plot()
    (js, tag) = bes.autoload_static(test_plot, CDN, 'some/path')
    html = bs4.BeautifulSoup(tag, 'html.parser')
    scripts = html.findAll(name='script')
    assert len(scripts) == 1
    attrs = scripts[0].attrs
    assert set(attrs) == {'src', 'id'}
    assert attrs['src'] == 'some/path'

@pytest.mark.parametrize('version', ['1.4.0rc1', '2.0.0dev3'])
@pytest.mark.selenium
def Test_autoload_static_test_js_dev_cdn(self, version, monkeypatch, driver, test_file_path_and_url, test_plot) -> None:
    version = '1.4.0rc1'
    test_plot = test_plot()
    monkeypatch.setattr(buv, '__version__', '1.4.0rc1')
    monkeypatch.setattr(resources, '__version__', '1.4.0rc1')
    (js, tag) = bes.autoload_static(test_plot, CDN, 'some/path')
    page = PAGE.render(js=js, tag=tag)
    (path, url) = test_file_path_and_url
    with open(path, 'w') as f:
        f.write(page)
    driver.get(url)
    scripts = driver.find_elements_by_css_selector('head script')
    assert len(scripts) == 3
    for script in scripts:
        assert script.get_attribute('crossorigin') == None
        assert script.get_attribute('integrity') == ''

@pytest.mark.selenium
def Test_autoload_static_test_js_release_cdn(self, monkeypatch, driver, test_file_path_and_url, test_plot) -> None:
    test_plot = test_plot()
    monkeypatch.setattr(buv, '__version__', '2.0.0')
    monkeypatch.setattr(resources, '__version__', '2.0.0')
    (js, tag) = bes.autoload_static(test_plot, CDN, 'some/path')
    page = PAGE.render(js=js, tag=tag)
    (path, url) = test_file_path_and_url
    with open(path, 'w') as f:
        f.write(page)
    driver.get(url)
    scripts = driver.find_elements_by_css_selector('head script')
    for x in scripts:
        print(x.get_attribute('src'))
    assert len(scripts) == 3
    for script in scripts:
        assert script.get_attribute('crossorigin') == 'anonymous'
        assert script.get_attribute('integrity').startswith('sha384-')

@pytest.mark.selenium
def Test_autoload_static_test_js_release_dev_cdn(self, monkeypatch, driver, test_file_path_and_url, test_plot) -> None:
    test_plot = test_plot()
    monkeypatch.setattr(buv, '__version__', '2.0.0-foo')
    monkeypatch.setattr(resources, '__version__', '2.0.0-foo')
    (js, tag) = bes.autoload_static(test_plot, CDN, 'some/path')
    page = PAGE.render(js=js, tag=tag)
    (path, url) = test_file_path_and_url
    with open(path, 'w') as f:
        f.write(page)
    driver.get(url)
    scripts = driver.find_elements_by_css_selector('head script')
    for x in scripts:
        print(x.get_attribute('src'))
    assert len(scripts) == 3
    for script in scripts:
        assert script.get_attribute('crossorigin') == 'anonymous'
        assert script.get_attribute('integrity').startswith('sha384-')

@pytest.mark.selenium
def Test_autoload_static_test_js_release_server(self, monkeypatch, driver, test_file_path_and_url, test_plot) -> None:
    test_plot = test_plot()
    monkeypatch.setattr(buv, '__version__', '2.0.0')
    monkeypatch.setattr(resources, '__version__', '2.0.0')
    (js, tag) = bes.autoload_static(test_plot, resources.Resources(mode='server'), 'some/path')
    page = PAGE.render(js=js, tag=tag)
    (path, url) = test_file_path_and_url
    with open(path, 'w') as f:
        f.write(page)
    driver.get(url)
    scripts = driver.find_elements_by_css_selector('head script')
    assert len(scripts) == 3
    for script in scripts:
        assert script.get_attribute('crossorigin') == None
        assert script.get_attribute('integrity') == ''

def Test_components_test_return_type(self) -> None:
    plot1 = figure()
    plot1.circle([], [])
    plot2 = figure()
    plot2.circle([], [])
    curdoc().add_root(plot1)
    curdoc().add_root(plot2)
    r = bes.components(plot1)
    assert len(r) == 2
    (_, divs) = bes.components((plot1, plot2))
    assert isinstance(divs, tuple)
    (_, divs) = bes.components([plot1, plot2])
    assert isinstance(divs, tuple)
    (_, divs) = bes.components({'Plot 1': plot1, 'Plot 2': plot2})
    assert isinstance(divs, dict)
    assert all((isinstance(x, str) for x in divs.keys()))
    (_, divs) = bes.components(OrderedDict([('Plot 1', plot1), ('Plot 2', plot2)]))
    assert isinstance(divs, OrderedDict)
    assert all((isinstance(x, str) for x in divs.keys()))

@patch('bokeh.embed.util.make_globally_unique_id', new_callable=lambda : stable_id)
def Test_components_test_plot_dict_returned_when_wrap_plot_info_is_false(self, mock_make_id) -> None:
    doc = Document()
    plot1 = figure()
    plot1.circle([], [])
    doc.add_root(plot1)
    plot2 = figure()
    plot2.circle([], [])
    doc.add_root(plot2)
    expected_plotdict_1 = RenderRoot(elementid='ID', id='ID')
    expected_plotdict_2 = RenderRoot(elementid='ID', id='ID')
    (_, plotdict) = bes.components(plot1, wrap_plot_info=False)
    assert plotdict == expected_plotdict_1
    (_, plotids) = bes.components((plot1, plot2), wrap_plot_info=False)
    assert plotids == (expected_plotdict_1, expected_plotdict_2)
    (_, plotiddict) = bes.components({'p1': plot1, 'p2': plot2}, wrap_plot_info=False)
    assert plotiddict == {'p1': expected_plotdict_1, 'p2': expected_plotdict_2}

def Test_components_test_result_attrs(self, test_plot) -> None:
    test_plot = test_plot()
    (script, div) = bes.components(test_plot)
    html = bs4.BeautifulSoup(script, 'html.parser')
    scripts = html.findAll(name='script')
    assert len(scripts) == 1
    assert scripts[0].attrs == {'type': 'text/javascript'}

@patch('bokeh.embed.util.make_globally_unique_id', new=stable_id)
def Test_components_test_div_attrs(self, test_plot) -> None:
    test_plot = test_plot()
    (script, div) = bes.components(test_plot)
    html = bs4.BeautifulSoup(div, 'html.parser')
    divs = html.findAll(name='div')
    assert len(divs) == 1
    div = divs[0]
    assert set(div.attrs) == {'class', 'id', 'data-root-id'}
    assert div.attrs['class'] == ['bk-root']
    assert div.attrs['id'] == 'ID'
    assert div.attrs['data-root-id'] == test_plot.id
    assert div.string is None

def Test_components_test_script_is_utf8_encoded(self, test_plot) -> None:
    test_plot = test_plot()
    (script, div) = bes.components(test_plot)
    assert isinstance(script, str)

def Test_components_test_quoting(self, test_plot) -> None:
    test_plot = test_plot()
    (script, div) = bes.components(test_plot)
    assert '&quot;' not in script
    assert "'foo'" not in script
    assert '&#x27;foo&#x27;' in script

def Test_components_test_output_is_without_script_tag_when_wrap_script_is_false(self, test_plot) -> None:
    test_plot = test_plot()
    (script, div) = bes.components(test_plot)
    html = bs4.BeautifulSoup(script, 'html.parser')
    scripts = html.findAll(name='script')
    assert len(scripts) == 1

def Test_file_html_test_return_type(self, test_plot) -> None:
    test_plot = test_plot()

    class fake_template:

        def __init__(self, tester, user_template_variables=None):
            self.tester = tester
            self.template_variables = {'title', 'bokeh_js', 'bokeh_css', 'plot_script', 'doc', 'docs', 'base'}
            if user_template_variables is not None:
                {'title', 'bokeh_js', 'bokeh_css', 'plot_script', 'doc', 'docs', 'base'}.update(user_template_variables)

        def render(self, template_variables):
            assert {'title', 'bokeh_js', 'bokeh_css', 'plot_script', 'doc', 'docs', 'base'}.issubset(set(template_variables.keys()))
            return 'template result'
    r = bes.file_html(test_plot, CDN, 'title')
    assert isinstance(r, str)
    r = bes.file_html(test_plot, CDN, 'title', fake_template(self))
    assert isinstance(r, str)
    r = bes.file_html(test_plot, CDN, 'title', fake_template(self, {'test_var'}), {'test_var': 'test'})
    assert isinstance(r, str)

@patch('bokeh.embed.bundle.warn')
def Test_file_html_test_file_html_handles_js_only_resources(self, mock_warn, test_plot) -> None:
    test_plot = test_plot()
    js_resources = JSResources(mode='relative', components=['bokeh'])
    template = Template('<head>{{ bokeh_js }}</head><body></body>')
    output = bes.file_html(test_plot, (js_resources, None), 'title', template=template)
    html = '<head>%s</head><body></body>' % js_resources.render_js()
    assert output == html

@patch('bokeh.embed.bundle.warn')
def Test_file_html_test_file_html_provides_warning_if_no_css(self, mock_warn, test_plot) -> None:
    test_plot = test_plot()
    js_resources = JSResources()
    bes.file_html(test_plot, (js_resources, None), 'title')
    mock_warn.assert_called_once_with('No Bokeh CSS Resources provided to template. If required you will need to provide them manually.')

@patch('bokeh.embed.bundle.warn')
def Test_file_html_test_file_html_handles_css_only_resources(self, mock_warn, test_plot) -> None:
    test_plot = test_plot()
    css_resources = CSSResources(mode='relative', components=['bokeh'])
    template = Template('<head>{{ bokeh_css }}</head><body></body>')
    output = bes.file_html(test_plot, (None, css_resources), 'title', template=template)
    html = '<head>%s</head><body></body>' % css_resources.render_css()
    assert output == html

@patch('bokeh.embed.bundle.warn')
def Test_file_html_test_file_html_provides_warning_if_no_js(self, mock_warn, test_plot) -> None:
    test_plot = test_plot()
    css_resources = CSSResources()
    bes.file_html(test_plot, (None, css_resources), 'title')
    mock_warn.assert_called_once_with('No Bokeh JS Resources provided to template. If required you will need to provide them manually.')

def Test_file_html_test_file_html_title_is_escaped(self, test_plot) -> None:
    test_plot = test_plot()
    r = bes.file_html(test_plot, CDN, '&<')
    assert '<title>&amp;&lt;</title>' in r

def Test_file_html_test_entire_doc_is_not_used(self) -> None:
    from bokeh.document import Document
    from bokeh.models import Button
    fig = figure()
    fig.x([0], [0])
    button = Button(label='Button')
    d = Document()
    d.add_root(fig)
    d.add_root(button)
    out = bes.file_html([fig], CDN)
    assert 'bokeh-widgets' not in out

def Test_json_item_test_with_target_id(self, test_plot) -> None:
    test_plot = test_plot()
    out = bes.json_item(test_plot, target='foo')
    assert out['target_id'] == 'foo'

def Test_json_item_test_without_target_id(self, test_plot) -> None:
    test_plot = test_plot()
    out = bes.json_item(test_plot)
    assert out['target_id'] == None

def Test_json_item_test_doc_json(self, test_plot) -> None:
    test_plot = test_plot()
    out = bes.json_item(test_plot, target='foo')
    expected = list(standalone_docs_json([test_plot]).values())[0]
    assert out['doc'] == expected

def Test_json_item_test_doc_title(self, test_plot) -> None:
    test_plot = test_plot()
    out = bes.json_item(test_plot, target='foo')
    assert out['doc']['title'] == ''

def Test_json_item_test_root_id(self, test_plot) -> None:
    test_plot = test_plot()
    out = bes.json_item(test_plot, target='foo')
    assert out['doc']['roots']['root_ids'][0] == out['root_id']

@patch('bokeh.embed.standalone.OutputDocumentFor')
def Test_json_item_test_apply_theme(self, mock_OFD, test_plot) -> None:
    test_plot = test_plot()
    try:
        bes.json_item(test_plot, theme='foo')
    except ValueError:
        pass
    mock_OFD.assert_called_once_with([test_plot], apply_theme='foo')