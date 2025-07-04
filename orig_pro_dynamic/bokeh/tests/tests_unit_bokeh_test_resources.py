import pytest
import os
import re
import subprocess
import sys
import bs4
from packaging.version import Version as V
import bokeh.util.version as buv
from bokeh import __version__
from bokeh.models import Model
from bokeh.resources import _get_cdn_urls
import bokeh.resources as resources
if os.environ.get('BOKEH_RESOURCES'):
    raise RuntimeError('Cannot run the unit tests with BOKEH_RESOURCES set')
LOG_LEVELS = ['trace', 'debug', 'info', 'warn', 'error', 'fatal']
DEFAULT_LOG_JS_RAW = 'Bokeh.set_log_level("info");'

def teardown_module() -> None:
    Model._clear_extensions()
VERSION_PAT = re.compile('^(\\d+\\.\\d+\\.\\d+)$')

def test_external_js_and_css_resource_embedding() -> None:
    """ This test method has to be at the end of the test modules because
    subclassing a Model causes the CustomModel to be added as a Model and
    messes up the Resources state for the other tests.
    """

    class CustomModel1(Model):
        __javascript__ = 'external_js_1'
        __css__ = 'external_css_1'

    class CustomModel2(Model):
        __javascript__ = ['external_js_2', 'external_js_3']
        __css__ = ['external_css_2', 'external_css_3']

    class CustomModel3(Model):
        __javascript__ = ['external_js_1', 'external_js_3']
        __css__ = ['external_css_1', 'external_css_2']
    r = resources.Resources()
    assert 'external_js_1' in r.js_files
    assert 'external_css_1' in r.css_files
    assert 'external_js_2' in r.js_files
    assert 'external_js_3' in r.js_files
    assert 'external_css_2' in r.css_files
    assert 'external_css_3' in r.css_files
    assert r.css_files.count('external_css_1') == 1
    assert r.css_files.count('external_css_2') == 1
    assert r.js_files.count('external_js_3') == 1
    assert r.js_files.count('external_js_1') == 1

def test_external_js_and_css_resource_ordering() -> None:

    class ZClass(Model):
        __javascript__ = 'z_class'

    class AClass(Model):
        __javascript__ = 'a_class'
    r = resources.Resources()
    assert r.js_files.index('a_class') < r.js_files.index('z_class')
    assert r.css_files.index('external_css_3') > r.css_files.index('external_css_2')
    assert r.js_files.index('external_js_3') > r.js_files.index('external_js_2')

def TestSRIHashes_test_get_all_hashes_valid_format(self) -> None:
    all_hashes = resources.get_all_sri_hashes()
    for (key, value) in all_hashes.items():
        assert VERSION_PAT.match(key), f'{key} is not a valid version for the SRI hashes dict'
        assert isinstance(value, dict)
        assert len(value)
        assert f'bokeh-{key}.js' in value
        assert f'bokeh-{key}.min.js' in value
        for h in value.values():
            assert len(h) == 64

def TestSRIHashes_test_get_all_hashes_copies(self) -> None:
    ah1 = resources.get_all_sri_hashes()
    ah2 = resources.get_all_sri_hashes()
    assert ah1 == ah2 == resources._SRI_HASHES
    assert ah1 is not ah2
    assert ah1 is not resources._SRI_HASHES
    assert ah2 is not resources._SRI_HASHES

@pytest.mark.skip
def TestSRIHashes_test_get_all_hashes_no_future_keys(self) -> None:
    current = V(__version__.split('-', 1)[0])
    all_hashes = resources.get_all_sri_hashes()
    for key in all_hashes:
        assert V(key) < current, f'SRI hash dict contains vesion {key} which is newer than current version {__version__}'

def TestSRIHashes_test_get_sri_hashes_for_version(self) -> None:
    all_hashes = resources.get_all_sri_hashes()
    for (key, value) in all_hashes.items():
        h = resources.get_sri_hashes_for_version(key)
        assert h == all_hashes[key]

def TestSRIHashes_test_get_sri_hashes_for_version_bad(self) -> None:
    with pytest.raises(KeyError):
        resources.get_sri_hashes_for_version('junk')

def TestJSResources_test_js_resources_default_mode_is_cdn(self) -> None:
    r = resources.JSResources()
    assert r.mode == 'cdn'

@pytest.mark.skip(reason='error')
def TestJSResources_test_js_resources_inline_has_no_css_resources(self) -> None:
    r = resources.JSResources(mode='inline')
    assert r.mode == 'inline'
    assert r.dev is False
    assert len(r.js_raw) == 4
    assert r.js_raw[-1] == DEFAULT_LOG_JS_RAW
    assert hasattr(r, 'css_raw') is False
    assert r.messages == []

def TestJSResources_test_js_resources_hashes_mock_full(self, monkeypatch) -> None:
    monkeypatch.setattr(buv, '__version__', '1.4.0')
    monkeypatch.setattr(resources, '__version__', '1.4.0')
    r = resources.JSResources()
    assert r.mode == 'cdn'
    hashes = resources.get_sri_hashes_for_version('1.4.0')
    min_hashes = {v for (k, v) in hashes.items() if k.endswith('.min.js') and 'api' not in k and ('gl' not in k)}
    assert set(r.hashes.values()) == min_hashes

@pytest.mark.parametrize('v', ['1.4.0dev6', '1.4.0rc1', '1.4.0dev6-50-foo'])
def TestJSResources_test_js_resources_hashes_mock_non_full(self, v, monkeypatch) -> None:
    v = '1.4.0dev6'
    monkeypatch.setattr(buv, '__version__', v)
    monkeypatch.setattr(resources, '__version__', v)
    r = resources.JSResources()
    assert r.mode == 'cdn'
    assert r.hashes == {}

def TestCSSResources_test_css_resources_default_mode_is_cdn(self) -> None:
    r = resources.CSSResources()
    assert r.mode == 'cdn'

def TestCSSResources_test_inline_css_resources(self) -> None:
    r = resources.CSSResources(mode='inline')
    assert r.mode == 'inline'
    assert r.dev is False
    assert len(r.css_raw) == 0
    assert hasattr(r, 'js_raw') is False
    assert r.messages == []

def TestResources_test_basic(self) -> None:
    r = resources.Resources()
    assert r.mode == 'cdn'

def TestResources_test_log_level(self) -> None:
    r = resources.Resources()
    for level in LOG_LEVELS:
        r.log_level = level
        assert r.log_level == level
        if not r.dev:
            assert r.js_raw[-1] == 'Bokeh.set_log_level("%s");' % level
    with pytest.raises(ValueError):
        setattr(r, 'log_level', 'foo')

def TestResources_test_module_attrs(self) -> None:
    assert resources.CDN.mode == 'cdn'
    assert resources.INLINE.mode == 'inline'

@pytest.mark.skip(reason='error')
def TestResources_test_inline(self) -> None:
    r = resources.Resources(mode='inline')
    assert r.mode == 'inline'
    assert r.dev == False
    assert len(r.js_raw) == 4
    assert r.js_raw[-1] == DEFAULT_LOG_JS_RAW
    assert len(r.css_raw) == 0
    assert r.messages == []

def TestResources_test_get_cdn_urls(self) -> None:
    dev_version = '0.0.1dev2'
    result = _get_cdn_urls(version=dev_version)
    url = result['urls'](['bokeh'], 'js')[0]
    assert 'bokeh/dev' in url

def TestResources_test_cdn(self, monkeypatch) -> None:
    monkeypatch.setattr(resources, '__version__', '1.0')
    r = resources.Resources(mode='cdn', version='1.0')
    assert r.mode == 'cdn'
    assert r.dev == False
    assert r.js_raw == [DEFAULT_LOG_JS_RAW]
    assert r.css_raw == []
    assert r.messages == []
    resources.__version__ = '1.0-1-abc'
    r = resources.Resources(mode='cdn', version='1.0')
    assert r.messages == [{'text': "Requesting CDN BokehJS version '1.0' from Bokeh development version '1.0-1-abc'. This configuration is unsupported and may not work!", 'type': 'warn'}]

def TestResources_test_server_default(self) -> None:
    r = resources.Resources(mode='server')
    assert r.mode == 'server'
    assert r.dev == False
    assert r.js_raw == [DEFAULT_LOG_JS_RAW]
    assert r.css_raw == []
    assert r.messages == []
    assert r.js_files == ['http://localhost:5006/static/js/bokeh.min.js', 'http://localhost:5006/static/js/bokeh-widgets.min.js', 'http://localhost:5006/static/js/bokeh-tables.min.js']

def TestResources_test_server_root_url(self) -> None:
    r = resources.Resources(mode='server', root_url='http://foo/')
    assert r.js_raw == [DEFAULT_LOG_JS_RAW]
    assert r.css_raw == []
    assert r.messages == []
    assert r.js_files == ['http://foo/static/js/bokeh.min.js', 'http://foo/static/js/bokeh-widgets.min.js', 'http://foo/static/js/bokeh-tables.min.js']

def TestResources_test_server_root_url_empty(self) -> None:
    r = resources.Resources(mode='server', root_url='')
    assert r.js_raw == [DEFAULT_LOG_JS_RAW]
    assert r.css_raw == []
    assert r.messages == []
    assert r.js_files == ['static/js/bokeh.min.js', 'static/js/bokeh-widgets.min.js', 'static/js/bokeh-tables.min.js']

def TestResources_test_server_with_versioner(self) -> None:

    def versioner(path):
        return path + '?v=VERSIONED'
    r = resources.Resources(mode='server', root_url='http://foo/', path_versioner=versioner)
    assert r.js_files == ['http://foo/static/js/bokeh.min.js?v=VERSIONED', 'http://foo/static/js/bokeh-widgets.min.js?v=VERSIONED', 'http://foo/static/js/bokeh-tables.min.js?v=VERSIONED']

def TestResources_test_server_dev(self) -> None:
    r = resources.Resources(mode='server-dev')
    assert r.mode == 'server'
    assert r.dev == True
    assert len(r.js_raw) == 2
    assert r.css_raw == []
    assert r.messages == []
    r = resources.Resources(mode='server-dev', root_url='http://foo/')
    assert r.js_raw == [DEFAULT_LOG_JS_RAW, 'Bokeh.settings.dev = true']
    assert r.css_raw == []
    assert r.messages == []

def TestResources_test_relative(self) -> None:
    r = resources.Resources(mode='relative')
    assert r.mode == 'relative'
    assert r.dev == False
    assert r.js_raw == [DEFAULT_LOG_JS_RAW]
    assert r.css_raw == []
    assert r.messages == []

def TestResources_test_relative_dev(self) -> None:
    r = resources.Resources(mode='relative-dev')
    assert r.mode == 'relative'
    assert r.dev == True
    assert r.js_raw == [DEFAULT_LOG_JS_RAW, 'Bokeh.settings.dev = true']
    assert r.css_raw == []
    assert r.messages == []

def TestResources_test_absolute(self) -> None:
    r = resources.Resources(mode='absolute')
    assert r.mode == 'absolute'
    assert r.dev == False
    assert r.js_raw == [DEFAULT_LOG_JS_RAW]
    assert r.css_raw == []
    assert r.messages == []

def TestResources_test_absolute_dev(self) -> None:
    r = resources.Resources(mode='absolute-dev')
    assert r.mode == 'absolute'
    assert r.dev == True
    assert r.js_raw == [DEFAULT_LOG_JS_RAW, 'Bokeh.settings.dev = true']
    assert r.css_raw == []
    assert r.messages == []

def TestResources_test_argument_checks(self) -> None:
    with pytest.raises(ValueError):
        resources.Resources('foo')
    for mode in ('inline', 'cdn', 'server', 'server-dev', 'absolute', 'absolute-dev'):
        with pytest.raises(ValueError):
            resources.Resources(mode, root_dir='foo')
    for mode in ('inline', 'server', 'server-dev', 'relative', 'relative-dev', 'absolute', 'absolute-dev'):
        with pytest.raises(ValueError):
            resources.Resources(mode, version='foo')
    for mode in ('inline', 'cdn', 'relative', 'relative-dev', 'absolute', 'absolute-dev'):
        with pytest.raises(ValueError):
            resources.Resources(mode, root_url='foo')

@pytest.mark.parametrize('env', ['BOKEH_CDN_VERSION', 'BOKEH_ROOTDIR'])
def TestResources_test_builtin_importable_with_env(self, monkeypatch, env) -> None:
    env = 'BOKEH_CDN_VERSION'
    cmd = [sys.executable, '-c', 'import bokeh.resources']
    monkeypatch.setenv(env, 'foo')
    try:
        subprocess.check_call(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        pytest.fail(f'resources import failed with {env} set')

def TestResources_test_render_js_cdn_release(self, monkeypatch) -> None:
    monkeypatch.setattr(buv, '__version__', '2.0.0')
    monkeypatch.setattr(resources, '__version__', '2.0.0')
    out = resources.CDN.render_js()
    html = bs4.BeautifulSoup(out, 'html.parser')
    scripts = html.findAll(name='script')
    for script in scripts:
        if 'src' not in script.attrs:
            continue
        assert script.attrs['crossorigin'] == 'anonymous'
        assert script.attrs['integrity'].startswith('sha384-')

@pytest.mark.parametrize('v', ['1.8.0rc1', '1.8.0dev6'])
def TestResources_test_render_js_cdn_dev_release(self, v, monkeypatch) -> None:
    v = '1.8.0rc1'
    monkeypatch.setattr(buv, '__version__', v)
    monkeypatch.setattr(resources, '__version__', v)
    out = resources.CDN.render_js()
    html = bs4.BeautifulSoup(out, 'html.parser')
    scripts = html.findAll(name='script')
    for script in scripts:
        assert 'crossorigin' not in script.attrs
        assert 'integrity' not in script.attrs

def TestResources_test_render_js_cdn_dev_local(self, monkeypatch) -> None:
    monkeypatch.setattr(buv, '__version__', '2.0.0-foo')
    monkeypatch.setattr(resources, '__version__', '2.0.0-foo')
    out = resources.CDN.render_js()
    html = bs4.BeautifulSoup(out, 'html.parser')
    scripts = html.findAll(name='script')
    for script in scripts:
        if 'src' not in script.attrs:
            continue
        assert script.attrs['crossorigin'] == 'anonymous'
        assert script.attrs['integrity'].startswith('sha384-')

@pytest.mark.skip(reason='error')
@pytest.mark.parametrize('v', ['2.0.0', '2.0.0-foo', '1.8.0rc1', '1.8.0dev6'])
def TestResources_test_render_js_inline(self, v, monkeypatch) -> None:
    v = '2.0.0'
    monkeypatch.setattr(buv, '__version__', v)
    monkeypatch.setattr(resources, '__version__', v)
    out = resources.INLINE.render_js()
    html = bs4.BeautifulSoup(out, 'html.parser')
    scripts = html.findAll(name='script')
    for script in scripts:
        assert 'crossorigin' not in script.attrs
        assert 'integrity' not in script.attrs