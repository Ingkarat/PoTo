import pytest
pytest
import asyncio
import logging
import os
import sys
from flaky import flaky
from mock import patch
from tornado.httpclient import HTTPError
import bokeh.document as document
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.client import ClientSession, pull_session, push_session
from bokeh.core.properties import AngleSpec, Any, Dict, DistanceSpec, Instance, Int, String
from bokeh.document import Document
from bokeh.document.events import ModelChangedEvent, TitleChangedEvent
from bokeh.model import Model
from bokeh.models import Plot
from bokeh.util.token import generate_jwt_token
from server._util_server import http_get, url, websocket_open, ws_url
logging.basicConfig(level=logging.DEBUG)

def test_client_changes_do_not_boomerang(monkeypatch, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        client_root = SomeModelInTestClientServer(foo=42)
        doc.add_root(client_root)
        client_session = push_session(doc, session_id='test_client_changes_do_not_boomerang', url=url(server), io_loop=server.io_loop)
        server_session = server.get_session('/', client_session.id)
        assert len(server_session.document.roots) == 1
        server_root = next(iter(server_session.document.roots))
        assert client_root.foo == 42
        assert server_root.foo == 42
        got_angry = {}
        got_angry['result'] = None

        def get_angry(message):
            got_angry['result'] = message
        monkeypatch.setattr(client_session, '_handle_patch', get_angry)
        client_root.foo = 57

        def server_change_made():
            return server_root.foo == 57
        client_session._connection._loop_until(server_change_made)
        assert server_root.foo == 57
        client_session.force_roundtrip()
        assert got_angry['result'] is None
        client_session.close()
        client_session._loop_until_closed()
        assert not client_session.connected
        server.unlisten()

def test_server_changes_do_not_boomerang(monkeypatch, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        client_root = SomeModelInTestClientServer(foo=42)
        doc.add_root(client_root)
        client_session = push_session(doc, session_id='test_server_changes_do_not_boomerang', url=url(server), io_loop=server.io_loop)
        server_session = server.get_session('/', client_session.id)
        assert len(server_session.document.roots) == 1
        server_root = next(iter(server_session.document.roots))
        assert client_root.foo == 42
        assert server_root.foo == 42
        got_angry = {}
        got_angry['result'] = None

        def get_angry(message, connection):
            got_angry['result'] = message
        monkeypatch.setattr(server_session, '_handle_patch', get_angry)

        def do_set_foo_property():
            server_root.foo = 57
        server.io_loop.spawn_callback(server_session.with_document_locked, do_set_foo_property)

        def client_change_made():
            return client_root.foo == 57
        client_session._connection._loop_until(client_change_made)
        assert client_root.foo == 57
        client_session.force_roundtrip()
        assert got_angry['result'] is None
        client_session.close()
        client_session._loop_until_closed()
        assert not client_session.connected

def test_unit_spec_changes_do_not_boomerang(monkeypatch, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        client_root = UnitsSpecModel()
        doc.add_root(client_root)
        client_session = push_session(doc, session_id='test_unit_spec_changes_do_not_boomerang', url=url(server), io_loop=server.io_loop)
        server_session = server.get_session('/', client_session.id)
        assert len(server_session.document.roots) == 1
        server_root = next(iter(server_session.document.roots))
        assert client_root.distance == 42
        assert server_root.angle == 0

        def change_to(new_distance, new_angle):
            got_angry = {}
            got_angry['result'] = None

            def get_angry(message):
                got_angry['result'] = message
            monkeypatch.setattr(client_session, '_handle_patch', get_angry)
            server_previous_distance = server_root.distance
            server_previous_angle = server_root.angle
            client_root.distance = new_distance
            client_root.angle = new_angle

            def server_change_made():
                return server_root.distance != server_previous_distance and server_root.angle != server_previous_angle
            client_session._connection._loop_until(server_change_made)
            client_session.force_roundtrip()
            assert got_angry['result'] is None
        change_to(57, 1)
        change_to({'value': 58}, {'value': 2})
        change_to({'field': 'foo'}, {'field': 'bar'})
        change_to({'value': 59, 'units': 'screen'}, {'value': 30, 'units': 'deg'})
        client_session.close()
        client_session._loop_until_closed()
        assert not client_session.connected
        server.unlisten()

@patch('bokeh.client.session.show_session')
def test_session_show_adds_obj_to_curdoc_if_necessary(m) -> None:
    session = ClientSession()
    session._document = Document()
    p = Plot()
    assert session.document.roots == []
    session.show(p)
    assert session.document.roots == [p]

def TestClientServer_test_minimal_connect_and_disconnect(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        session = ClientSession(session_id='test_minimal_connect_and_disconnect', io_loop=server.io_loop, websocket_url=ws_url(server))
        session.connect()
        assert session.connected

def TestClientServer_test_disconnect_on_error(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        session = ClientSession(session_id='test_disconnect_on_error', websocket_url=ws_url(server), io_loop=server.io_loop)
        session.connect()
        assert session.connected
        server.io_loop.spawn_callback(session._connection._socket.write_message, b'xx', binary=True)
        session._loop_until_closed()
        assert not session.connected
        session.close()
        session._loop_until_closed()
        assert not session.connected

def TestClientServer_test_connect_with_prefix(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application, prefix='foo') as server:
        session = ClientSession(io_loop=server.io_loop, websocket_url=ws_url(server, '/foo'))
        session.connect()
        assert session.connected
        session.close()
        session._loop_until_closed()
        session = ClientSession(io_loop=server.io_loop, websocket_url=ws_url(server))
        session.connect()
        assert not session.connected
        session.close()
        session._loop_until_closed()

def TestClientServer_test_push_document(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        doc.add_root(AnotherModelInTestClientServer(bar=43))
        doc.add_root(SomeModelInTestClientServer(foo=42))
        client_session = push_session(doc, session_id='test_push_document', url=url(server), io_loop=server.io_loop)
        assert client_session.document == doc
        assert len(client_session.document.roots) == 2
        server_session = server.get_session('/', client_session.id)
        assert len(server_session.document.roots) == 2
        results = {}
        for r in server_session.document.roots:
            if hasattr(r, 'foo'):
                results['foo'] = r.foo
            if hasattr(r, 'bar'):
                results['bar'] = r.bar
        assert results['foo'] == 42
        assert results['bar'] == 43
        client_session.close()
        client_session._loop_until_closed()
        assert not client_session.connected

def TestClientServer_test_pull_document(self, ManagedServerLoop) -> None:
    application = Application()

    def add_roots(doc):
        doc.add_root(AnotherModelInTestClientServer(bar=43))
        doc.add_root(SomeModelInTestClientServer(foo=42))
    handler = FunctionHandler(add_roots)
    application.add(handler)
    with ManagedServerLoop(application) as server:
        client_session = pull_session(session_id='test_pull_document', url=url(server), io_loop=server.io_loop)
        assert len(client_session.document.roots) == 2
        server_session = server.get_session('/', client_session.id)
        assert len(server_session.document.roots) == 2
        results = {}
        for r in server_session.document.roots:
            if hasattr(r, 'foo'):
                results['foo'] = r.foo
            if hasattr(r, 'bar'):
                results['bar'] = r.bar
        assert results['foo'] == 42
        assert results['bar'] == 43
        client_session.close()
        client_session._loop_until_closed()
        assert not client_session.connected

def TestClientServer_test__check_error_404(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        with pytest.raises(IOError):
            pull_session(session_id='test__check_error_404', url=url(server) + 'file_not_found', io_loop=server.io_loop)

def TestClientServer_test_request_server_info(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        session = ClientSession(session_id='test_request_server_info', websocket_url=ws_url(server), io_loop=server.io_loop)
        session.connect()
        assert session.connected
        assert session.document is None
        info = session.request_server_info()
        from bokeh import __version__
        assert info['version_info']['bokeh'] == __version__
        assert info['version_info']['server'] == __version__
        session.close()
        session._loop_until_closed()
        assert not session.connected

@pytest.mark.skipif(sys.platform == 'win32', reason='uninmportant failure on win')
@flaky(max_runs=10)
def TestClientServer_test_ping(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application, keep_alive_milliseconds=0) as server:
        session = ClientSession(session_id='test_ping', websocket_url=ws_url(server), io_loop=server.io_loop)
        session.connect()
        assert session.connected
        assert session.document is None
        connection = next(iter(server._tornado._clients))
        expected_pong = connection._ping_count
        server._tornado._keep_alive()
        session.force_roundtrip()
        assert expected_pong == connection._socket.latest_pong
        server._tornado._keep_alive()
        session.force_roundtrip()
        assert expected_pong + 1 == connection._socket.latest_pong
        session.close()
        session._loop_until_closed()
        assert not session.connected

def TestClientServer_test_client_changes_go_to_server(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        client_root = SomeModelInTestClientServer(foo=42)
        client_session = push_session(doc, session_id='test_client_changes_go_to_server', url=url(server), io_loop=server.io_loop)
        server_session = server.get_session('/', client_session.id)
        assert len(server_session.document.roots) == 0
        doc.add_root(client_root)
        client_session.force_roundtrip()
        assert len(server_session.document.roots) == 1
        server_root = next(iter(server_session.document.roots))
        assert client_root.foo == 42
        assert server_root.foo == 42
        assert server_session.document.title == document.DEFAULT_TITLE
        doc.title = 'Client Title'
        client_session.force_roundtrip()
        assert server_session.document.title == 'Client Title'
        client_root.foo = 57

        def server_change_made():
            return server_root.foo == 57
        client_session._connection._loop_until(server_change_made)
        assert server_root.foo == 57
        doc.remove_root(client_root)
        client_session.force_roundtrip()
        assert len(server_session.document.roots) == 0
        client_session.close()
        client_session._loop_until_closed()
        assert not client_session.connected

def TestClientServer_test_server_changes_go_to_client(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        client_session = push_session(doc, session_id='test_server_changes_go_to_client', url=url(server), io_loop=server.io_loop)
        server_session = server.get_session('/', client_session.id)
        assert len(client_session.document.roots) == 0
        server_root = SomeModelInTestClientServer(foo=42)

        def do_add_server_root():
            server_session.document.add_root(server_root)
        server.io_loop.spawn_callback(server_session.with_document_locked, do_add_server_root)

        def client_has_root():
            return len(doc.roots) > 0
        client_session._connection._loop_until(client_has_root)
        client_root = next(iter(client_session.document.roots))
        assert client_root.foo == 42
        assert server_root.foo == 42

        def do_set_server_title():
            server_session.document.title = 'Server Title'
        server.io_loop.spawn_callback(server_session.with_document_locked, do_set_server_title)

        def client_title_set():
            return client_session.document.title != document.DEFAULT_TITLE
        client_session._connection._loop_until(client_title_set)
        assert client_session.document.title == 'Server Title'

        def do_set_property_on_server():
            server_root.foo = 57
        server.io_loop.spawn_callback(server_session.with_document_locked, do_set_property_on_server)

        def client_change_made():
            return client_root.foo == 57
        client_session._connection._loop_until(client_change_made)
        assert client_root.foo == 57

        def do_remove_server_root():
            server_session.document.remove_root(server_root)
        server.io_loop.spawn_callback(server_session.with_document_locked, do_remove_server_root)

        def client_lacks_root():
            return len(doc.roots) == 0
        client_session._connection._loop_until(client_lacks_root)
        assert len(client_session.document.roots) == 0
        client_session.close()
        client_session._loop_until_closed()
        assert not client_session.connected

def TestClientServer_test_client_session_timeout_async(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        client_session = push_session(doc, session_id='test_client_session_timeout_async', url=url(server), io_loop=server.io_loop)
        result = DictModel()
        doc.add_root(result)

        async def cb():
            result.values['a'] = 0
            result.values['b'] = await self.async_value(1)
            result.values['c'] = await self.async_value(2)
            result.values['d'] = await self.async_value(3)
            result.values['e'] = await self.async_value(4)
            client_session.close()
            return 5
        cb_id = doc.add_timeout_callback(cb, 10)
        client_session._loop_until_closed()
        with pytest.raises(ValueError) as exc:
            doc.remove_timeout_callback(cb_id)
        assert 'already removed' in repr(exc.value)
        assert dict(a=0, b=1, c=2, d=3, e=4) == result.values

def TestClientServer_test_client_session_timeout_async_added_before_push(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        result = DictModel()
        doc.add_root(result)

        async def cb():
            result.values['a'] = 0
            result.values['b'] = await self.async_value(1)
            result.values['c'] = await self.async_value(2)
            result.values['d'] = await self.async_value(3)
            result.values['e'] = await self.async_value(4)
            client_session.close()
            return 5
        cb_id = doc.add_timeout_callback(cb, 10)
        client_session = push_session(doc, session_id='test_client_session_timeout_async', url=url(server), io_loop=server.io_loop)
        client_session._loop_until_closed()
        with pytest.raises(ValueError) as exc:
            doc.remove_timeout_callback(cb_id)
        assert 'already removed' in repr(exc.value)
        assert dict(a=0, b=1, c=2, d=3, e=4) == result.values

@pytest.mark.skip(reason='broken (see PR #9426)')
def TestClientServer_test_server_session_timeout_async(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        doc.add_root(DictModel())
        client_session = push_session(doc, session_id='test_server_session_timeout_async', url=url(server), io_loop=server.io_loop)
        server_session = server.get_session('/', client_session.id)
        result = next(iter(server_session.document.roots))

        async def cb():
            result.values['a'] = 0
            result.values['b'] = await self.async_value(1)
            result.values['c'] = await self.async_value(2)
            result.values['d'] = await self.async_value(3)
            result.values['e'] = await self.async_value(4)
            client_session.close()
            return 5
        cb_id = server_session.document.add_timeout_callback(cb, 10)
        client_session._loop_until_closed()
        with pytest.raises(ValueError) as exc:
            server_session.document.remove_timeout_callback(cb_id)
        assert 'already removed' in repr(exc.value)
        assert dict(a=0, b=1, c=2, d=3, e=4) == result.values

def TestClientServer_test_client_session_next_tick_async(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        client_session = push_session(doc, session_id='test_client_session_next_tick_async', url=url(server), io_loop=server.io_loop)
        result = DictModel()
        doc.add_root(result)

        async def cb():
            result.values['a'] = 0
            result.values['b'] = await self.async_value(1)
            result.values['c'] = await self.async_value(2)
            result.values['d'] = await self.async_value(3)
            result.values['e'] = await self.async_value(4)
            client_session.close()
            return 5
        cb_id = doc.add_next_tick_callback(cb)
        client_session._loop_until_closed()
        with pytest.raises(ValueError) as exc:
            doc.remove_next_tick_callback(cb_id)
        assert 'already removed' in repr(exc.value)
        assert dict(a=0, b=1, c=2, d=3, e=4) == result.values

def TestClientServer_test_client_session_next_tick_async_added_before_push(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        result = DictModel()
        doc.add_root(result)

        async def cb():
            result.values['a'] = 0
            result.values['b'] = await self.async_value(1)
            result.values['c'] = await self.async_value(2)
            result.values['d'] = await self.async_value(3)
            result.values['e'] = await self.async_value(4)
            client_session.close()
            return 5
        cb_id = doc.add_next_tick_callback(cb)
        client_session = push_session(doc, session_id='test_client_session_next_tick_async', url=url(server), io_loop=server.io_loop)
        client_session._loop_until_closed()
        with pytest.raises(ValueError) as exc:
            doc.remove_next_tick_callback(cb_id)
        assert 'already removed' in repr(exc.value)
        assert dict(a=0, b=1, c=2, d=3, e=4) == result.values

@pytest.mark.skip(reason='broken (see PR #9426)')
def TestClientServer_test_server_session_next_tick_async(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        doc.add_root(DictModel())
        client_session = push_session(doc, session_id='test_server_session_next_tick_async', url=url(server), io_loop=server.io_loop)
        server_session = server.get_session('/', client_session.id)
        result = next(iter(server_session.document.roots))

        async def cb():
            result.values['a'] = 0
            result.values['b'] = await self.async_value(1)
            result.values['c'] = await self.async_value(2)
            result.values['d'] = await self.async_value(3)
            result.values['e'] = await self.async_value(4)
            client_session.close()
            return 5
        cb_id = server_session.document.add_next_tick_callback(cb)
        client_session._loop_until_closed()
        with pytest.raises(ValueError) as exc:
            server_session.document.remove_next_tick_callback(cb_id)
        assert 'already removed' in repr(exc.value)
        assert dict(a=0, b=1, c=2, d=3, e=4) == result.values

def TestClientServer_test_client_session_periodic_async(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        client_session = push_session(doc, session_id='test_client_session_periodic_async', url=url(server), io_loop=server.io_loop)
        result = DictModel()
        doc.add_root(result)

        async def cb():
            result.values['a'] = 0
            result.values['b'] = await self.async_value(1)
            result.values['c'] = await self.async_value(2)
            result.values['d'] = await self.async_value(3)
            result.values['e'] = await self.async_value(4)
            client_session.close()
            return 5
        cb_id = doc.add_periodic_callback(cb, 10)
        client_session._loop_until_closed()
        doc.remove_periodic_callback(cb_id)
        assert dict(a=0, b=1, c=2, d=3, e=4) == result.values

def TestClientServer_test_client_session_periodic_async_added_before_push(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        result = DictModel()
        doc.add_root(result)

        async def cb():
            result.values['a'] = 0
            result.values['b'] = await self.async_value(1)
            result.values['c'] = await self.async_value(2)
            result.values['d'] = await self.async_value(3)
            result.values['e'] = await self.async_value(4)
            client_session.close()
            return 5
        cb_id = doc.add_periodic_callback(cb, 10)
        client_session = push_session(doc, session_id='test_client_session_periodic_async', url=url(server), io_loop=server.io_loop)
        client_session._loop_until_closed()
        doc.remove_periodic_callback(cb_id)
        assert dict(a=0, b=1, c=2, d=3, e=4) == result.values

@pytest.mark.skip(reason='broken (see PR #9426)')
def TestClientServer_test_server_session_periodic_async(self, ManagedServerLoop) -> None:
    application = Application()
    with ManagedServerLoop(application) as server:
        doc = document.Document()
        doc.add_root(DictModel())
        client_session = push_session(doc, session_id='test_server_session_periodic_async', url=url(server), io_loop=server.io_loop)
        server_session = server.get_session('/', client_session.id)
        result = next(iter(server_session.document.roots))

        async def cb():
            result.values['a'] = 0
            result.values['b'] = await self.async_value(1)
            result.values['c'] = await self.async_value(2)
            result.values['d'] = await self.async_value(3)
            result.values['e'] = await self.async_value(4)
            client_session.close()
            return 5
        cb_id = server_session.document.add_periodic_callback(cb, 10)
        client_session._loop_until_closed()
        server_session.document.remove_periodic_callback(cb_id)
        assert dict(a=0, b=1, c=2, d=3, e=4) == result.values

@pytest.mark.skip(reason='broken (see PR #9426)')
def TestClientServer_test_lots_of_concurrent_messages(self, ManagedServerLoop) -> None:
    application = Application()

    def setup_stuff(doc):
        m1 = AnotherModelInTestClientServer(bar=43, name='m1')
        m2 = SomeModelInTestClientServer(foo=42, name='m2')
        m3 = SomeModelInTestClientServer(foo=68, name='m3')
        doc.add_root(m1)
        doc.add_root(m2)
        doc.add_root(m3)

        def timeout1():
            m1.bar += 1
        timeout1_cb_id = doc.add_timeout_callback(timeout1, 1)

        def timeout2():
            m2.foo += 1
        timeout2_cb_id = doc.add_timeout_callback(timeout2, 3)

        def periodic1():
            m1.bar += 1
            doc.remove_timeout_callback(timeout1_cb_id)
            doc.add_timeout_callback(timeout1, m1.bar % 7)
        doc.add_periodic_callback(periodic1, 3)

        def periodic2():
            m2.foo += 1
            doc.remove_timeout_callback(timeout2_cb_id)
            doc.add_timeout_callback(timeout2, m2.foo % 7)
        doc.add_periodic_callback(periodic2, 1)

        def server_on_change(event):
            if isinstance(event, ModelChangedEvent) and event.model is m3:
                return
            m3.foo += 1
        doc.on_change(server_on_change)
    handler = FunctionHandler(setup_stuff)
    application.add(handler)
    with ManagedServerLoop(application, keep_alive_milliseconds=1) as server:
        session = pull_session(session_id='test_lots_of_concurrent_messages', url=url(server), io_loop=server.io_loop)
        assert session.connected
        server_session = server.get_session('/', session.id)

        def client_timeout():
            m = session.document.roots[0]
            m.name = m.name[::-1]
        cb_id = session.document.add_timeout_callback(client_timeout, 3)

        def client_periodic():
            m = session.document.roots[1]
            m.name = m.name[::-1]
            session.document.remove_timeout_callback(cb_id)
            session.document.add_timeout_callback(client_timeout, 3)
        session.document.add_periodic_callback(client_periodic, 1)
        result = {}

        def end_test():
            result['connected'] = session.connected
            result['server_connection_count'] = server_session.connection_count
            result['server_close_code'] = next(iter(server._tornado._clients))._socket.close_code
            result['doc'] = session.document.to_json()
            session.close()
        session.document.add_timeout_callback(end_test, 250)

        def client_on_change(event):
            if not isinstance(event, TitleChangedEvent):
                session.document.title = session.document.title[::-1]
        session.document.on_change(client_on_change)
        session._loop_until_closed()
        assert not session.connected
        assert 'connected' in result
        assert result['connected']
        assert result['server_connection_count'] == 1
        assert result['server_close_code'] is None