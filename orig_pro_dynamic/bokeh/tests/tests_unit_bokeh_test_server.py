import pytest
pytest
import logging
from tornado.ioloop import IOLoop
from bokeh.application import Application
from bokeh.server.server import Server
logging.basicConfig(level=logging.DEBUG)

def TestServer_test_port(self) -> None:
    loop = IOLoop()
    loop.make_current()
    server = Server(Application(), port=1234)
    assert server.port == 1234
    server.stop()
    server.unlisten()

@pytest.mark.skip(reason='error')
def TestServer_test_address(self) -> None:
    loop = IOLoop()
    loop.make_current()
    server = Server(Application(), address='0.0.0.0')
    assert server.address == '0.0.0.0'
    server.stop()
    server.unlisten()