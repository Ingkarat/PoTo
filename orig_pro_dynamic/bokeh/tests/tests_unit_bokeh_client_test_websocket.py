import pytest
pytest
from tornado import locks
import bokeh.client.websocket as bcw

def Test_WebSocketClientConnectionWrapper_test_creation_raises_with_None(self) -> None:
    with pytest.raises(ValueError):
        bcw.WebSocketClientConnectionWrapper(None)

def Test_WebSocketClientConnectionWrapper_test_creation(self) -> None:
    w = bcw.WebSocketClientConnectionWrapper('socket')
    assert w._socket == 'socket'
    assert isinstance(w.write_lock, locks.Lock)