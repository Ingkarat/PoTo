import pytest
pytest
import os
from mock import Mock, PropertyMock, patch
import bokeh.io.util as biu

@pytest.mark.skip(reason='error')
def test_detect_current_filename() -> None:
    assert biu.detect_current_filename().endswith(('py.test', 'pytest', 'py.test-script.py', 'pytest-script.py'))

@patch('bokeh.io.util.NamedTemporaryFile')
def test_temp_filename(mock_tmp) -> None:
    fn = Mock()
    type(fn).name = PropertyMock(return_value='Junk.test')
    mock_tmp.return_value = fn
    r = biu.temp_filename('test')
    assert r == 'Junk.test'
    assert mock_tmp.called
    assert mock_tmp.call_args[0] == ()
    assert mock_tmp.call_args[1] == {'suffix': '.test'}

def test_default_filename() -> None:
    old_detect_current_filename = biu.detect_current_filename
    old__no_access = biu._no_access
    old__shares_exec_prefix = biu._shares_exec_prefix
    biu.detect_current_filename = lambda : '/a/b/foo.py'
    try:
        with pytest.raises(RuntimeError):
            biu.default_filename('py')
        biu._no_access = lambda x: False
        r = biu.default_filename('test')
        assert os.path.normpath(r) == os.path.normpath('/a/b/foo.test')
        biu._no_access = lambda x: True
        r = biu.default_filename('test')
        assert os.path.normpath(r) != os.path.normpath('/a/b/foo.test')
        assert r.endswith('.test')
        biu._no_access = lambda x: False
        biu._shares_exec_prefix = lambda x: True
        r = biu.default_filename('test')
        assert os.path.normpath(r) != os.path.normpath('/a/b/foo.test')
        assert r.endswith('.test')
        biu.detect_current_filename = lambda : None
        biu._no_access = lambda x: False
        biu._shares_exec_prefix = lambda x: False
        r = biu.default_filename('test')
        assert os.path.normpath(r) != os.path.normpath('/a/b/foo.test')
        assert r.endswith('.test')
    finally:
        biu.detect_current_filename = old_detect_current_filename
        biu._no_access = old__no_access
        biu._shares_exec_prefix = old__shares_exec_prefix

@patch('os.access')
def test__no_access(mock_access) -> None:
    biu._no_access('test')
    assert mock_access.called
    assert mock_access.call_args[0] == ('test', os.W_OK | os.X_OK)
    assert mock_access.call_args[1] == {}

def test__shares_exec_prefix() -> None:
    import sys
    old_ex = sys.exec_prefix
    try:
        sys.exec_prefix = '/foo/bar'
        assert biu._shares_exec_prefix('/foo/bar') == True
        sys.exec_prefix = '/baz/bar'
        assert biu._shares_exec_prefix('/foo/bar') == False
        sys.exec_prefix = None
        assert biu._shares_exec_prefix('/foo/bar') == False
    finally:
        sys.exec_prefix = old_ex