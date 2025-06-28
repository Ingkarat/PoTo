import pytest
pytest
import asyncio
from tornado.ioloop import IOLoop
from bokeh.application import Application
import bokeh.server.contexts as bsc

def TestBokehServerContext_test_init(self) -> None:
    ac = bsc.ApplicationContext('app', io_loop='ioloop')
    c = bsc.BokehServerContext(ac)
    assert c.application_context == ac

def TestBokehServerContext_test_sessions(self) -> None:
    ac = bsc.ApplicationContext('app', io_loop='ioloop')
    ac._sessions = dict(foo=1, bar=2)
    c = bsc.BokehServerContext(ac)
    assert set(c.sessions) == {1, 2}

def TestBokehSessionContext_test_init(self) -> None:
    ac = bsc.ApplicationContext('app', io_loop='ioloop')
    sc = bsc.BokehServerContext(ac)
    c = bsc.BokehSessionContext('id', sc, 'doc')
    assert c.session is None
    assert c.request is None
    assert not c.destroyed
    assert c.logout_url is None

def TestBokehSessionContext_test_destroyed(self) -> None:

    class FakeSession:
        destroyed = False
    ac = bsc.ApplicationContext('app', io_loop='ioloop')
    sc = bsc.BokehServerContext(ac)
    c = bsc.BokehSessionContext('id', sc, 'doc')
    sess = FakeSession()
    c._session = sess
    assert not c.destroyed
    sess.destroyed = True
    assert c.destroyed

def TestBokehSessionContext_test_logout_url(self) -> None:
    ac = bsc.ApplicationContext('app', io_loop='ioloop')
    sc = bsc.BokehServerContext(ac)
    c = bsc.BokehSessionContext('id', sc, 'doc', logout_url='/logout')
    assert c.session is None
    assert c.request is None
    assert not c.destroyed
    assert c.logout_url == '/logout'

def TestApplicationContext_test_init(self) -> None:
    c = bsc.ApplicationContext('app', io_loop='ioloop')
    assert c.io_loop == 'ioloop'
    assert c.application == 'app'
    assert c.url is None
    c = bsc.ApplicationContext('app', io_loop='ioloop', url='url')
    assert c.io_loop == 'ioloop'
    assert c.application == 'app'
    assert c.url == 'url'

def TestApplicationContext_test_sessions(self) -> None:
    c = bsc.ApplicationContext('app', io_loop='ioloop')
    c._sessions = dict(foo=1, bar=2)
    assert set(c.sessions) == {1, 2}

def TestApplicationContext_test_get_session_success(self) -> None:
    c = bsc.ApplicationContext('app', io_loop='ioloop')
    c._sessions = dict(foo=1, bar=2)
    assert c.get_session('foo') == 1

def TestApplicationContext_test_get_session_failure(self) -> None:
    c = bsc.ApplicationContext('app', io_loop='ioloop')
    c._sessions = dict(foo=1, bar=2)
    with pytest.raises(bsc.ProtocolError) as e:
        c.get_session('bax')
    assert str(e.value).endswith('No such session bax')