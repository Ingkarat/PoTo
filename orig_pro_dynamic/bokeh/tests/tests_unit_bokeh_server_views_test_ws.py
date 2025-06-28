import pytest
pytest
import logging
from tornado.websocket import WebSocketClosedError
from bokeh.server.views.auth_mixin import AuthMixin
from bokeh.util.logconfig import basicConfig
from bokeh.server.views.ws import WSHandler
basicConfig()

async def test_send_message_raises(caplog) -> None:

    class ExcMessage:

        def ExcMessage_send(self, handler):
            raise WebSocketClosedError()
    assert len(caplog.records) == 0
    with caplog.at_level(logging.WARN):
        ret = await WSHandler.send_message('self', ExcMessage())
        assert len(caplog.records) == 1
        assert caplog.text.endswith('Failed sending message as connection was closed\n')
        assert ret is None

def test_uses_auth_mixin() -> None:
    assert issubclass(WSHandler, AuthMixin)

def ExcMessage_send(self, handler):
    raise WebSocketClosedError()