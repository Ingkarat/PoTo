import pytest
pytest
import bokeh.client.util as bcu

def Test_server_url_for_websocket_url_test_with_ws(self) -> None:
    assert bcu.server_url_for_websocket_url('ws://foo.com/ws') == 'http://foo.com/'

def Test_server_url_for_websocket_url_test_with_wss(self) -> None:
    assert bcu.server_url_for_websocket_url('wss://foo.com/ws') == 'https://foo.com/'

def Test_server_url_for_websocket_url_test_bad_proto(self) -> None:
    with pytest.raises(ValueError):
        bcu.server_url_for_websocket_url('junk://foo.com/ws')

def Test_server_url_for_websocket_url_test_bad_ending(self) -> None:
    with pytest.raises(ValueError):
        bcu.server_url_for_websocket_url('ws://foo.com/junk')
    with pytest.raises(ValueError):
        bcu.server_url_for_websocket_url('wss://foo.com/junk')

def Test_websocket_url_for_server_url_test_with_http(self) -> None:
    assert bcu.websocket_url_for_server_url('http://foo.com') == 'ws://foo.com/ws'
    assert bcu.websocket_url_for_server_url('http://foo.com/') == 'ws://foo.com/ws'

def Test_websocket_url_for_server_url_test_with_https(self) -> None:
    assert bcu.websocket_url_for_server_url('https://foo.com') == 'wss://foo.com/ws'
    assert bcu.websocket_url_for_server_url('https://foo.com/') == 'wss://foo.com/ws'

def Test_websocket_url_for_server_url_test_bad_proto(self) -> None:
    with pytest.raises(ValueError):
        bcu.websocket_url_for_server_url('junk://foo.com')