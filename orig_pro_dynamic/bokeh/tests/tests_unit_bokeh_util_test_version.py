import pytest
pytest
import re
import mock
from bokeh._version import get_versions
import bokeh.util.version as buv
VERSION_PAT = re.compile('^(\\d+\\.\\d+\\.\\d+)$')

def Test___version___test_basic(self) -> None:
    assert isinstance(buv.__version__, str)
    assert buv.__version__ == get_versions()['version']

def Test_base_version_test_returns_helper(self) -> None:
    with mock.patch('bokeh.util.version._base_version_helper') as helper:
        buv.base_version()
        assert helper.called

def Test_is_full_release_test_actual(self) -> None:
    assert buv.is_full_release() == bool(VERSION_PAT.match(buv.__version__))

def Test_is_full_release_test_mock_full(self, monkeypatch) -> None:
    monkeypatch.setattr(buv, '__version__', '1.5.0')
    assert buv.is_full_release()

@pytest.mark.parametrize('v', ('1.2.3dev2', '1.4.5rc3', 'junk'))
def Test_is_full_release_test_mock_not_full(self, monkeypatch, v) -> None:
    v = ('1.2.3dev2', '1.4.5rc3', 'junk')[0]
    monkeypatch.setattr(buv, '__version__', v)
    assert not buv.is_full_release()

def Test__base_version_helper_test_release_version_unchanged(self) -> None:
    assert buv._base_version_helper('0.2.3') == '0.2.3'
    assert buv._base_version_helper('1.2.3') == '1.2.3'

def Test__base_version_helper_test_dev_version_stripped(self) -> None:
    assert buv._base_version_helper('0.2.3dev2') == '0.2.3'
    assert buv._base_version_helper('1.2.3dev10') == '1.2.3'

def Test__base_version_helper_test_rc_version_stripped(self) -> None:
    assert buv._base_version_helper('0.2.3rc2') == '0.2.3'
    assert buv._base_version_helper('1.2.3rc10') == '1.2.3'