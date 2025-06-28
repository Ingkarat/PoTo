import pytest
pytest
from tornado.ioloop import IOLoop
from bokeh.client.states import NOT_YET_CONNECTED
import bokeh.client.connection as bcc

def Test_ClientConnection_test_creation(self) -> None:
    c = bcc.ClientConnection('session', 'wsurl')
    assert c.url == 'wsurl'
    assert c.connected == False
    assert isinstance(c.io_loop, IOLoop)
    assert c._session == 'session'
    assert isinstance(c._state, NOT_YET_CONNECTED)
    assert c._until_predicate is None
    assert c._server_info is None
    assert c._arguments is None

def Test_ClientConnection_test_creation_with_arguments(self) -> None:
    c = bcc.ClientConnection('session', 'wsurl', arguments=dict(foo='bar'))
    assert c.url == 'wsurl'
    assert c.connected == False
    assert isinstance(c.io_loop, IOLoop)
    assert c._session == 'session'
    assert isinstance(c._state, NOT_YET_CONNECTED)
    assert c._until_predicate is None
    assert c._server_info is None
    assert c._arguments == dict(foo='bar')