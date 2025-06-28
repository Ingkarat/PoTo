import logging
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.websocket import websocket_connect
log = logging.getLogger(__name__)
__all__ = ('http_get', 'url', 'websocket_open', 'ws_url')

def url(server, prefix=''):
    return 'http://localhost:' + str(server.port) + prefix + '/'

def ws_url(server, prefix=''):
    return 'ws://localhost:' + str(server.port) + prefix + '/ws'

async def http_get(io_loop, url, headers=None):
    http_client = AsyncHTTPClient()
    if not headers:
        headers = dict()
    return await http_client.fetch(url, headers=headers)

async def websocket_open(io_loop, url, origin=None, subprotocols=[]):
    request = HTTPRequest(url)
    if origin is not None:
        request.headers['Origin'] = origin
    result = await websocket_connect(request, subprotocols=subprotocols)
    result.close()
    return result