import pytest
pytest
import os
import sys
import webbrowser
from mock import patch
import bokeh.util.browser as bub
_open_args = None

def test_get_browser_controller_dummy() -> None:
    b = bub.get_browser_controller('none')
    assert isinstance(b, bub.DummyWebBrowser)

def test_get_browser_controller_None() -> None:
    b = bub.get_browser_controller(None)
    assert b == webbrowser

@patch('webbrowser.get')
def test_get_browser_controller_value(mock_get) -> None:
    bub.get_browser_controller('foo')
    assert mock_get.called
    assert mock_get.call_args[0] == ('foo',)
    assert mock_get.call_args[1] == {}

@patch('webbrowser.get')
def test_get_browser_controller_dummy_with_env(mock_get) -> None:
    os.environ['BOKEH_BROWSER'] = 'bar'
    bub.get_browser_controller('none')
    del os.environ['BOKEH_BROWSER']

@patch('webbrowser.get')
def test_get_browser_controller_None_with_env(mock_get) -> None:
    os.environ['BOKEH_BROWSER'] = 'bar'
    bub.get_browser_controller()
    assert mock_get.called
    assert mock_get.call_args[0] == ('bar',)
    assert mock_get.call_args[1] == {}
    del os.environ['BOKEH_BROWSER']

@patch('webbrowser.get')
def test_get_browser_controller_value_with_env(mock_get) -> None:
    os.environ['BOKEH_BROWSER'] = 'bar'
    bub.get_browser_controller('foo')
    assert mock_get.called
    assert mock_get.call_args[0] == ('foo',)
    assert mock_get.call_args[1] == {}
    del os.environ['BOKEH_BROWSER']

def test_view_bad_new() -> None:
    with pytest.raises(RuntimeError) as e:
        bub.view('foo', new='junk')
        assert str(e) == "invalid 'new' value passed to view: 'junk', valid values are: 'same', 'window', or 'tab'"

def test_view_args() -> None:
    db = bub.DummyWebBrowser
    bub.DummyWebBrowser = _RecordingWebBrowser
    bub.view('http://foo', browser='none')
    assert _open_args == (('http://foo',), {'autoraise': True, 'new': 0})
    bub.view('/foo/bar', browser='none')
    if sys.platform == 'win32':
        assert _open_args == (('file://' + os.path.splitdrive(os.getcwd())[0] + '\\foo\\bar',), {'autoraise': True, 'new': 0})
    else:
        assert _open_args == (('file:///foo/bar',), {'autoraise': True, 'new': 0})
    bub.view('http://foo', browser='none', autoraise=False)
    assert _open_args == (('http://foo',), {'autoraise': False, 'new': 0})
    bub.view('http://foo', browser='none', new='same')
    assert _open_args == (('http://foo',), {'autoraise': True, 'new': 0})
    bub.view('http://foo', browser='none', new='window')
    assert _open_args == (('http://foo',), {'autoraise': True, 'new': 1})
    bub.view('http://foo', browser='none', new='tab')
    assert _open_args == (('http://foo',), {'autoraise': True, 'new': 2})
    bub.DummyWebBrowser = db

def test_NEW_PARAM() -> None:
    assert bub.NEW_PARAM == {'tab': 2, 'window': 1}

def _RecordingWebBrowser_open(self, *args, **kw):
    global _open_args
    _open_args = (args, kw)