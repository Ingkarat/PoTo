import pytest
pytest
from mock import patch
import bokeh.client.session as bcs

def test_DEFAULT_SESSION_ID() -> None:
    assert bcs.DEFAULT_SESSION_ID == 'default'

def test_DEFAULT_SERVER_WEBSOCKET_URL() -> None:
    assert bcs.DEFAULT_SERVER_WEBSOCKET_URL == 'ws://localhost:5006/ws'

def Test_ClientSession_test_creation_defaults(self) -> None:
    s = bcs.ClientSession()
    assert s.connected == False
    assert s.document is None
    assert s._connection._arguments is None
    assert isinstance(s.id, str)
    assert len(s.id) == 44

def Test_ClientSession_test_creation_with_session_id(self) -> None:
    s = bcs.ClientSession('sid')
    assert s.connected == False
    assert s.document is None
    assert s._connection._arguments is None
    assert s.id == 'sid'

def Test_ClientSession_test_creation_with_ws_url(self) -> None:
    s = bcs.ClientSession(websocket_url='wsurl')
    assert s.connected == False
    assert s.document is None
    assert s._connection._arguments is None
    assert s._connection.url == 'wsurl'
    assert isinstance(s.id, str)
    assert len(s.id) == 44

def Test_ClientSession_test_creation_with_ioloop(self) -> None:
    s = bcs.ClientSession(io_loop='io_loop')
    assert s.connected == False
    assert s.document is None
    assert s._connection._arguments is None
    assert s._connection.io_loop == 'io_loop'
    assert isinstance(s.id, str)
    assert len(s.id) == 44

def Test_ClientSession_test_creation_with_arguments(self) -> None:
    s = bcs.ClientSession(arguments='args')
    assert s.connected == False
    assert s.document is None
    assert s._connection._arguments == 'args'
    assert len(s.id) == 44

@patch('bokeh.client.connection.ClientConnection.connect')
def Test_ClientSession_test_connect(self, mock_connect) -> None:
    s = bcs.ClientSession()
    s.connect()
    assert mock_connect.call_count == 1
    assert mock_connect.call_args[0] == ()
    assert mock_connect.call_args[1] == {}

@patch('bokeh.client.connection.ClientConnection.close')
def Test_ClientSession_test_close(self, mock_close) -> None:
    s = bcs.ClientSession()
    s.close()
    assert mock_close.call_count == 1
    assert mock_close.call_args[0] == ('closed',)
    assert mock_close.call_args[1] == {}

@patch('bokeh.client.connection.ClientConnection.close')
def Test_ClientSession_test_context_manager(self, mock_close) -> None:
    with bcs.ClientSession() as session:
        assert isinstance(session, bcs.ClientSession)
    assert mock_close.call_count == 1
    assert mock_close.call_args[0] == ('closed',)
    assert mock_close.call_args[1] == {}

@patch('bokeh.client.connection.ClientConnection.close')
def Test_ClientSession_test_close_with_why(self, mock_close) -> None:
    s = bcs.ClientSession()
    s.close('foo')
    assert mock_close.call_count == 1
    assert mock_close.call_args[0] == ('foo',)
    assert mock_close.call_args[1] == {}

@patch('bokeh.client.connection.ClientConnection.force_roundtrip')
def Test_ClientSession_test_force_roundtrip(self, mock_force_roundtrip) -> None:
    s = bcs.ClientSession()
    s.force_roundtrip()
    assert mock_force_roundtrip.call_count == 1
    assert mock_force_roundtrip.call_args[0] == ()
    assert mock_force_roundtrip.call_args[1] == {}

@patch('bokeh.client.connection.ClientConnection.request_server_info')
def Test_ClientSession_test_request_server_info(self, mock_request_server_info) -> None:
    s = bcs.ClientSession()
    s.request_server_info()
    assert mock_request_server_info.call_count == 1
    assert mock_request_server_info.call_args[0] == ()
    assert mock_request_server_info.call_args[1] == {}