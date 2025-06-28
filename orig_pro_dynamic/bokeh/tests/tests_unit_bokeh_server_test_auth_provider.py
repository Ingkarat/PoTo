import pytest
pytest
from types import ModuleType
from tornado.web import RequestHandler
from bokeh._testing.util.api import verify_all
from bokeh._testing.util.filesystem import with_file_contents, with_file_contents_async
import bokeh.server.auth_provider as bsa
ALL = ('AuthModule', 'AuthProvider', 'NullAuth')

@pytest.fixture
def null_auth():
    return bsa.NullAuth()
Test___all__ = verify_all(bsa, ALL)
_source = '\ndef get_login_url():\n    pass\n\nlogout_url = "foo"\n\nclass LoginHandler(object):\n    pass\n'

def test_load_auth_module() -> None:

    def func(filename):
        m = bsa.load_auth_module(filename)
        assert isinstance(m, ModuleType)
        assert [x for x in sorted(dir(m)) if not x.startswith('__')] == ['LoginHandler', 'get_login_url', 'logout_url']
    with_file_contents(_source, func, suffix='.py')

def test_probably_relative_url() -> None:
    assert bsa.probably_relative_url('httpabc')
    assert bsa.probably_relative_url('httpsabc')
    assert bsa.probably_relative_url('/abc')
    assert not bsa.probably_relative_url('http://abc')
    assert not bsa.probably_relative_url('https://abc')
    assert not bsa.probably_relative_url('//abc')

def TestNullAuth_test_endpoints(self, null_auth) -> None:
    null_auth = null_auth()
    assert null_auth.endpoints == []

def TestNullAuth_test_get_user(self, null_auth) -> None:
    null_auth = null_auth()
    assert null_auth.get_user == None

def TestNullAuth_test_login_url(self, null_auth) -> None:
    null_auth = null_auth()
    assert null_auth.login_url == None

def TestNullAuth_test_get_login_url(self, null_auth) -> None:
    null_auth = null_auth()
    assert null_auth.get_login_url == None

def TestNullAuth_test_login_handler(self, null_auth) -> None:
    null_auth = null_auth()
    assert null_auth.login_handler == None

def TestNullAuth_test_logout_url(self, null_auth) -> None:
    null_auth = null_auth()
    assert null_auth.logout_url == None

def TestNullAuth_test_logout_handler(self, null_auth) -> None:
    null_auth = null_auth()
    assert null_auth.logout_handler == None

def TestAuthModule_properties_test_no_endpoints(self) -> None:

    def func(filename):
        am = bsa.AuthModule(filename)
        assert am.endpoints == []
    with_file_contents('\ndef get_user(): pass\ndef get_login_url(): pass\n        ', func, suffix='.py')
    with_file_contents('\ndef get_user(): pass\nlogin_url = "/foo"\n        ', func, suffix='.py')

def TestAuthModule_properties_test_login_url_endpoint(self) -> None:

    def func(filename):
        am = bsa.AuthModule(filename)
        assert am.endpoints[0][0] == '/foo'
        assert issubclass(am.endpoints[0][1], RequestHandler)
    with_file_contents('\nfrom tornado.web import RequestHandler\ndef get_user(): pass\nlogin_url = "/foo"\nclass LoginHandler(RequestHandler): pass\n        ', func, suffix='.py')

def TestAuthModule_properties_test_logout_url_endpoint(self) -> None:

    def func(filename):
        am = bsa.AuthModule(filename)
        assert am.endpoints[0][0] == '/bar'
        assert issubclass(am.endpoints[0][1], RequestHandler)
    with_file_contents('\nfrom tornado.web import RequestHandler\ndef get_user(): pass\nlogin_url = "/foo"\nlogout_url = "/bar"\nclass LogoutHandler(RequestHandler): pass\n        ', func, suffix='.py')

def TestAuthModule_properties_test_login_logout_url_endpoint(self) -> None:

    def func(filename):
        am = bsa.AuthModule(filename)
        endpoints = sorted(am.endpoints)
        assert endpoints[0][0] == '/bar'
        assert issubclass(endpoints[0][1], RequestHandler)
        assert endpoints[1][0] == '/foo'
        assert issubclass(endpoints[1][1], RequestHandler)
    with_file_contents('\ndef get_user(): pass\nlogin_url = "/foo"\nfrom tornado.web import RequestHandler\nclass LoginHandler(RequestHandler): pass\nlogout_url = "/bar"\nfrom tornado.web import RequestHandler\nclass LogoutHandler(RequestHandler): pass\n        ', func, suffix='.py')

def TestAuthModule_properties_test_get_user(self) -> None:

    def func(filename):
        am = bsa.AuthModule(filename)
        assert am.get_user is not None
        assert am.get_user('handler') == 10
    with_file_contents('\ndef get_user(handler): return 10\nlogin_url = "/foo"\n        ', func, suffix='.py')

def TestAuthModule_properties_test_login_url(self) -> None:

    def func(filename):
        am = bsa.AuthModule(filename)
        assert am.login_url == '/foo'
        assert am.get_login_url is None
        assert am.login_handler is None
        assert am.logout_url is None
        assert am.logout_handler is None
    with_file_contents('\ndef get_user(handler): return 10\nlogin_url = "/foo"\n        ', func, suffix='.py')

def TestAuthModule_properties_test_get_login_url(self) -> None:

    def func(filename):
        am = bsa.AuthModule(filename)
        assert am.login_url is None
        assert am.get_login_url('handler') == 20
        assert am.login_handler is None
        assert am.logout_url is None
        assert am.logout_handler is None
    with_file_contents('\ndef get_user(handler): return 10\ndef get_login_url(handler): return 20\n        ', func, suffix='.py')

def TestAuthModule_properties_test_login_handler(self) -> None:

    def func(filename):
        am = bsa.AuthModule(filename)
        assert am.login_url == '/foo'
        assert am.get_login_url is None
        assert issubclass(am.login_handler, RequestHandler)
        assert am.logout_url is None
        assert am.logout_handler is None
    with_file_contents('\ndef get_user(handler): return 10\nlogin_url = "/foo"\nfrom tornado.web import RequestHandler\nclass LoginHandler(RequestHandler): pass\n        ', func, suffix='.py')

def TestAuthModule_properties_test_logout_url(self) -> None:

    def func(filename):
        am = bsa.AuthModule(filename)
        assert am.login_url == '/foo'
        assert am.get_login_url is None
        assert am.login_handler is None
        assert am.logout_url == '/bar'
        assert am.logout_handler is None
    with_file_contents('\ndef get_user(handler): return 10\nlogin_url = "/foo"\nlogout_url = "/bar"\n        ', func, suffix='.py')

def TestAuthModule_properties_test_logout_handler(self) -> None:

    def func(filename):
        am = bsa.AuthModule(filename)
        assert am.login_url == '/foo'
        assert am.get_login_url is None
        assert am.login_handler is None
        assert am.logout_url == '/bar'
        assert issubclass(am.logout_handler, RequestHandler)
    with_file_contents('\ndef get_user(handler): return 10\nlogin_url = "/foo"\nlogout_url = "/bar"\nfrom tornado.web import RequestHandler\nclass LogoutHandler(RequestHandler): pass\n    ', func, suffix='.py')

def TestAuthModule_validation_test_no_file(self) -> None:
    with pytest.raises(ValueError) as e:
        bsa.AuthModule('junkjunkjunk')
        assert str(e).startswith('no file exists at module_path:')

def TestAuthModule_validation_test_both_user(self) -> None:

    def func(filename):
        with pytest.raises(ValueError) as e:
            bsa.AuthModule(filename)
            assert str(e) == 'Only one of get_user or get_user_async should be supplied'
    with_file_contents('\ndef get_user(handler): return 10\nasync def get_user_async(handler): return 20\n    ', func, suffix='.py')

@pytest.mark.parametrize('user_func', ['get_user', 'get_user_async'])
def TestAuthModule_validation_test_no_login(self, user_func) -> None:
    user_func = 'get_user'

    def func(filename):
        with pytest.raises(ValueError) as e:
            bsa.AuthModule(filename)
            assert str(e) == 'When user authentication is enabled, one of login_url or get_login_url must be supplied'
    with_file_contents('\ndef %s(handler): return 10\n    ' % user_func, func, suffix='.py')

def TestAuthModule_validation_test_both_login(self) -> None:

    def func(filename):
        with pytest.raises(ValueError) as e:
            bsa.AuthModule(filename)
            assert str(e) == 'At most one of login_url or get_login_url should be supplied'
    with_file_contents('\ndef get_user(handler): return 10\ndef get_login_url(handler): return 20\nlogin_url = "/foo"\n    ', func, suffix='.py')

def TestAuthModule_validation_test_handler_with_get_login_url(self) -> None:

    def func(filename):
        with pytest.raises(ValueError) as e:
            bsa.AuthModule(filename)
            assert str(e) == 'LoginHandler cannot be used with a get_login_url() function'
    with_file_contents('\ndef get_user(handler): return 10\ndef get_login_url(handler): return 20\nfrom tornado.web import RequestHandler\nclass LoginHandler(RequestHandler): pass\n    ', func, suffix='.py')

def TestAuthModule_validation_test_login_handler_wrong_type(self) -> None:

    def func(filename):
        with pytest.raises(ValueError) as e:
            bsa.AuthModule(filename)
            assert str(e) == 'LoginHandler must be a Tornado RequestHandler'
    with_file_contents('\ndef get_user(handler): return 10\nlogin_url = "/foo"\nclass LoginHandler(object): pass\n    ', func, suffix='.py')

@pytest.mark.parametrize('login_url', ['http://foo.com', 'https://foo.com', '//foo.com'])
def TestAuthModule_validation_test_login_handler_wrong_url(self, login_url) -> None:
    login_url = 'http://foo.com'

    def func(filename):
        with pytest.raises(ValueError) as e:
            bsa.AuthModule(filename)
            assert str(e) == 'LoginHandler can only be used with a relative login_url'
    with_file_contents('\ndef get_user(handler): return 10\nlogin_url = %r\n    ' % login_url, func, suffix='.py')

def TestAuthModule_validation_test_logout_handler_wrong_type(self) -> None:

    def func(filename):
        with pytest.raises(ValueError) as e:
            bsa.AuthModule(filename)
            assert str(e) == 'LoginHandler must be a Tornado RequestHandler'
    with_file_contents('\ndef get_user(handler): return 10\nlogin_url = "/foo"\nclass LogoutHandler(object): pass\n    ', func, suffix='.py')

@pytest.mark.parametrize('logout_url', ['http://foo.com', 'https://foo.com', '//foo.com'])
def TestAuthModule_validation_test_logout_handler_wrong_url(self, logout_url) -> None:
    logout_url = 'http://foo.com'

    def func(filename):
        with pytest.raises(ValueError) as e:
            bsa.AuthModule(filename)
            assert str(e) == 'LoginHandler can only be used with a relative login_url'
    with_file_contents('\ndef get_user(handler): return 10\nlogout_url = %r\n    ' % logout_url, func, suffix='.py')