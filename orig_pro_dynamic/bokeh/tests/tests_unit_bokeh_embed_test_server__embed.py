import pytest
pytest
import bs4
import bokeh.embed.server as bes

@pytest.fixture
def test_plot() -> None:
    from bokeh.plotting import figure
    test_plot = figure()
    test_plot.circle([1, 2], [2, 3])
    return test_plot

def Test__src_path(object):

    def test_args(self) -> None:
        assert bes._src_path('http://foo', '1234') == 'http://foo/autoload.js?bokeh-autoload-element=1234'

def TestServerDocument_test_invalid_resources_param(self) -> None:
    with pytest.raises(ValueError):
        bes.server_document(url='http://localhost:8081/foo/bar/sliders', resources=123)
    with pytest.raises(ValueError):
        bes.server_document(url='http://localhost:8081/foo/bar/sliders', resources='whatever')

def TestServerDocument_test_resources_default_is_implicit(self) -> None:
    r = bes.server_document(url='http://localhost:8081/foo/bar/sliders', resources='default')
    assert 'resources=' not in r

def TestServerDocument_test_resources_none(self) -> None:
    r = bes.server_document(url='http://localhost:8081/foo/bar/sliders', resources=None)
    assert 'resources=none' in r

def TestServerDocument_test_general(self) -> None:
    r = bes.server_document(url='http://localhost:8081/foo/bar/sliders')
    assert 'bokeh-app-path=/foo/bar/sliders' in r
    assert 'bokeh-absolute-url=http://localhost:8081/foo/bar/sliders' in r
    html = bs4.BeautifulSoup(r, 'html.parser')
    scripts = html.findAll(name='script')
    assert len(scripts) == 1
    script = scripts[0]
    attrs = script.attrs
    assert list(attrs) == ['id']
    divid = attrs['id']
    request = 'xhr.open(\'GET\', "%s/autoload.js?bokeh-autoload-element=%s&bokeh-app-path=/foo/bar/sliders&bokeh-absolute-url=%s", true);' % ('http://localhost:8081/foo/bar/sliders', divid, 'http://localhost:8081/foo/bar/sliders')
    assert request in script.string

def TestServerDocument_test_script_attrs_arguments_provided(self) -> None:
    r = bes.server_document(arguments=dict(foo=10))
    assert 'foo=10' in r
    html = bs4.BeautifulSoup(r, 'html.parser')
    scripts = html.findAll(name='script')
    assert len(scripts) == 1
    script = scripts[0]
    attrs = script.attrs
    assert list(attrs) == ['id']
    divid = attrs['id']
    request = 'xhr.open(\'GET\', "%s/autoload.js?bokeh-autoload-element=%s&bokeh-absolute-url=%s&foo=10", true);' % ('http://localhost:5006', divid, 'http://localhost:5006')
    assert request in script.string

def TestServerDocument_test_script_attrs_url_provided_absolute_resources(self) -> None:
    r = bes.server_document(url='http://localhost:8081/foo/bar/sliders')
    assert 'bokeh-app-path=/foo/bar/sliders' in r
    assert 'bokeh-absolute-url=http://localhost:8081/foo/bar/sliders' in r
    html = bs4.BeautifulSoup(r, 'html.parser')
    scripts = html.findAll(name='script')
    assert len(scripts) == 1
    script = scripts[0]
    attrs = script.attrs
    assert list(attrs) == ['id']
    divid = attrs['id']
    request = 'xhr.open(\'GET\', "%s/autoload.js?bokeh-autoload-element=%s&bokeh-app-path=/foo/bar/sliders&bokeh-absolute-url=%s", true);' % ('http://localhost:8081/foo/bar/sliders', divid, 'http://localhost:8081/foo/bar/sliders')
    assert request in script.string

def TestServerDocument_test_script_attrs_url_provided(self) -> None:
    r = bes.server_document(url='http://localhost:8081/foo/bar/sliders', relative_urls=True)
    assert 'bokeh-app-path=/foo/bar/sliders' in r
    html = bs4.BeautifulSoup(r, 'html.parser')
    scripts = html.findAll(name='script')
    assert len(scripts) == 1
    script = scripts[0]
    attrs = script.attrs
    assert list(attrs) == ['id']
    divid = attrs['id']
    request = 'xhr.open(\'GET\', "%s/autoload.js?bokeh-autoload-element=%s&bokeh-app-path=/foo/bar/sliders", true);' % ('http://localhost:8081/foo/bar/sliders', divid)
    assert request in script.string

def TestServerSession_test_return_type(self, test_plot) -> None:
    test_plot = test_plot()
    r = bes.server_session(test_plot, session_id='fakesession')
    assert isinstance(r, str)

def TestServerSession_test_script_attrs_session_id_provided(self, test_plot) -> None:
    test_plot = test_plot()
    r = bes.server_session(test_plot, session_id='fakesession')
    html = bs4.BeautifulSoup(r, 'html.parser')
    scripts = html.findAll(name='script')
    assert len(scripts) == 1
    script = scripts[0]
    attrs = script.attrs
    assert list(attrs) == ['id']
    divid = attrs['id']
    request = 'xhr.open(\'GET\', "%s/autoload.js?bokeh-autoload-element=%s&bokeh-absolute-url=%s", true);' % ('http://localhost:5006', divid, 'http://localhost:5006')
    assert request in script.string
    assert 'xhr.setRequestHeader("Bokeh-Session-Id", "fakesession")' in script.string

def TestServerSession_test_invalid_resources_param(self, test_plot) -> None:
    test_plot = test_plot()
    with pytest.raises(ValueError):
        bes.server_session(test_plot, session_id='fakesession', resources=123)
    with pytest.raises(ValueError):
        bes.server_session(test_plot, session_id='fakesession', resources='whatever')

def TestServerSession_test_resources_default_is_implicit(self, test_plot) -> None:
    test_plot = test_plot()
    r = bes.server_session(test_plot, session_id='fakesession', resources='default')
    assert 'resources=' not in r

def TestServerSession_test_resources_none(self, test_plot) -> None:
    test_plot = test_plot()
    r = bes.server_session(test_plot, session_id='fakesession', resources=None)
    assert 'resources=none' in r

def TestServerSession_test_model_none(self) -> None:
    r = bes.server_session(None, session_id='fakesession')
    html = bs4.BeautifulSoup(r, 'html.parser')
    scripts = html.findAll(name='script')
    assert len(scripts) == 1
    script = scripts[0]
    attrs = script.attrs
    assert list(attrs) == ['id']
    divid = attrs['id']
    request = '%s/autoload.js?bokeh-autoload-element=%s&bokeh-absolute-url=%s' % ('http://localhost:5006', divid, 'http://localhost:5006')
    assert request in script.string
    assert 'xhr.setRequestHeader("Bokeh-Session-Id", "fakesession")' in script.string

def TestServerSession_test_general(self, test_plot) -> None:
    test_plot = test_plot()
    r = bes.server_session(test_plot, session_id='fakesession')
    html = bs4.BeautifulSoup(r, 'html.parser')
    scripts = html.findAll(name='script')
    assert len(scripts) == 1
    script = scripts[0]
    attrs = script.attrs
    assert list(attrs) == ['id']
    divid = attrs['id']
    request = 'xhr.open(\'GET\', "%s/autoload.js?bokeh-autoload-element=%s&bokeh-absolute-url=%s", true);' % ('http://localhost:5006', divid, 'http://localhost:5006')
    assert request in script.string
    assert 'xhr.setRequestHeader("Bokeh-Session-Id", "fakesession")' in script.string

def Test__clean_url_test_default(self) -> None:
    assert bes._clean_url('default') == bes.DEFAULT_SERVER_HTTP_URL.rstrip('/')

def Test__clean_url_test_bad_ws(self) -> None:
    with pytest.raises(ValueError):
        bes._clean_url('ws://foo')

def Test__clean_url_test_arg(self) -> None:
    assert bes._clean_url('http://foo/bar') == 'http://foo/bar'
    assert bes._clean_url('http://foo/bar/') == 'http://foo/bar'

def Test__get_app_path_test_arg(self) -> None:
    assert bes._get_app_path('foo') == '/foo'
    assert bes._get_app_path('http://foo') == '/'
    assert bes._get_app_path('http://foo/bar') == '/bar'
    assert bes._get_app_path('https://foo') == '/'
    assert bes._get_app_path('https://foo/bar') == '/bar'

def Test__process_arguments_test_None(self) -> None:
    assert bes._process_arguments(None) == ''

def Test__process_arguments_test_args(self) -> None:
    args = dict(foo=10, bar='baz')
    r = bes._process_arguments(args)
    assert r == '&foo=10&bar=baz' or r == '&bar=baz&foo=10'

def Test__process_arguments_test_args_ignores_bokeh_prefixed(self) -> None:
    args = dict(foo=10, bar='baz')
    args['bokeh-junk'] = 20
    r = bes._process_arguments(args)
    assert r == '&foo=10&bar=baz' or r == '&bar=baz&foo=10'

def Test__process_app_path_test_root(self) -> None:
    assert bes._process_app_path('/') == ''

def Test__process_app_path_test_arg(self) -> None:
    assert bes._process_app_path('/stuff') == '&bokeh-app-path=/stuff'

def Test__process_relative_urls_test_True(self) -> None:
    assert bes._process_relative_urls(True, '') == ''
    assert bes._process_relative_urls(True, '/stuff') == ''

def Test__process_relative_urls_test_Flase(self) -> None:
    assert bes._process_relative_urls(False, '/stuff') == '&bokeh-absolute-url=/stuff'

def Test__process_resources_test_bad_input(self) -> None:
    with pytest.raises(ValueError):
        bes._process_resources('foo')

def Test__process_resources_test_None(self) -> None:
    assert bes._process_resources(None) == '&resources=none'

def Test__process_resources_test_default(self) -> None:
    assert bes._process_resources('default') == ''