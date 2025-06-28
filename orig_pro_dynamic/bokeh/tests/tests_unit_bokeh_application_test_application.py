import pytest
pytest
import logging
import mock
from bokeh.application.handlers import CodeHandler, FunctionHandler, Handler
from bokeh.core.properties import Instance, Int
from bokeh.document import Document
from bokeh.model import Model
from bokeh.plotting import figure
from bokeh.util.logconfig import basicConfig
import bokeh.application.application as baa
basicConfig()

def RequestHandler___init__(self, data):
    self._data = data

def RequestHandler_process_request(self, request):
    return self._data

def Test_Application_test_empty(self) -> None:
    a = baa.Application()
    doc = a.create_document()
    assert not doc.roots

def Test_Application_test_invalid_kwarg(self) -> None:
    with pytest.raises(TypeError):
        baa.Application(junk='foo')

def Test_Application_test_process_request(self) -> None:
    a = baa.Application()
    a.add(RequestHandler(dict(a=10)))
    a.add(RequestHandler(dict(b=20)))
    a.add(RequestHandler(dict(a=30)))
    assert a.process_request('request') == dict(a=30, b=20)

def Test_Application_test_one_handler(self) -> None:
    a = baa.Application()

    def add_roots(doc):
        doc.add_root(AnotherModelInTestApplication())
        doc.add_root(SomeModelInTestApplication())
    handler = FunctionHandler(add_roots)
    a.add(handler)
    doc = a.create_document()
    assert len(doc.roots) == 2

def Test_Application_test_two_handlers(self) -> None:
    a = baa.Application()

    def add_roots(doc):
        doc.add_root(AnotherModelInTestApplication())
        doc.add_root(SomeModelInTestApplication())

    def add_one_root(doc):
        doc.add_root(AnotherModelInTestApplication())
    handler = FunctionHandler(add_roots)
    a.add(handler)
    handler2 = FunctionHandler(add_one_root)
    a.add(handler2)
    doc = a.create_document()
    assert len(doc.roots) == 3

def Test_Application_test_two_handlers_in_init(self) -> None:

    def add_roots(doc):
        doc.add_root(AnotherModelInTestApplication())
        doc.add_root(SomeModelInTestApplication())

    def add_one_root(doc):
        doc.add_root(AnotherModelInTestApplication())
    handler = FunctionHandler(add_roots)
    handler2 = FunctionHandler(add_one_root)
    a = baa.Application(handler, handler2)
    doc = a.create_document()
    assert len(doc.roots) == 3

def Test_Application_test_safe_to_fork(self) -> None:

    def add_roots(doc):
        doc.add_root(AnotherModelInTestApplication())
        doc.add_root(SomeModelInTestApplication())

    def add_one_root(doc):
        doc.add_root(AnotherModelInTestApplication())
    handler = FunctionHandler(add_roots)
    handler2 = FunctionHandler(add_one_root)
    a = baa.Application(handler, handler2)
    assert a.safe_to_fork
    a.create_document()
    assert not a.safe_to_fork

def Test_Application_test_metadata(self) -> None:
    a = baa.Application(metadata='foo')
    a.create_document()
    assert a.metadata == 'foo'

def Test_Application_test_failed_handler(self, caplog) -> None:
    a = baa.Application()
    handler = CodeHandler(filename='junk', source='bad(')
    a.add(handler)
    d = Document()
    with caplog.at_level(logging.ERROR):
        assert len(caplog.records) == 0
        a.initialize_document(d)
        assert len(caplog.records) == 1

def Test_Application_test_no_static_path(self) -> None:
    a = baa.Application()

    def add_roots(doc):
        doc.add_root(AnotherModelInTestApplication())
        doc.add_root(SomeModelInTestApplication())

    def add_one_root(doc):
        doc.add_root(AnotherModelInTestApplication())
    handler = FunctionHandler(add_roots)
    a.add(handler)
    handler2 = FunctionHandler(add_one_root)
    a.add(handler2)
    assert a.static_path == None

def Test_Application_test_static_path(self) -> None:
    a = baa.Application()

    def add_roots(doc):
        doc.add_root(AnotherModelInTestApplication())
        doc.add_root(SomeModelInTestApplication())

    def add_one_root(doc):
        doc.add_root(AnotherModelInTestApplication())
    handler = FunctionHandler(add_roots)
    handler._static = 'foo'
    a.add(handler)
    handler2 = FunctionHandler(add_one_root)
    a.add(handler2)
    assert a.static_path == 'foo'

def Test_Application_test_excess_static_path(self) -> None:
    a = baa.Application()

    def add_roots(doc):
        doc.add_root(AnotherModelInTestApplication())
        doc.add_root(SomeModelInTestApplication())

    def add_one_root(doc):
        doc.add_root(AnotherModelInTestApplication())
    handler = FunctionHandler(add_roots)
    handler._static = 'foo'
    a.add(handler)
    handler2 = FunctionHandler(add_one_root)
    handler2._static = 'bar'
    with pytest.raises(RuntimeError) as e:
        a.add(handler2)
    assert 'More than one static path' in str(e.value)

@mock.patch('bokeh.document.document.check_integrity')
def Test_Application_test_application_validates_document_by_default(self, check_integrity) -> None:
    a = baa.Application()
    d = Document()
    d.add_root(figure())
    a.initialize_document(d)
    assert check_integrity.called

@mock.patch('bokeh.document.document.check_integrity')
def Test_Application_test_application_doesnt_validate_document_due_to_env_var(self, check_integrity, monkeypatch) -> None:
    monkeypatch.setenv('BOKEH_VALIDATE_DOC', 'false')
    a = baa.Application()
    d = Document()
    d.add_root(figure())
    a.initialize_document(d)
    assert not check_integrity.called

def Test_ServerContext_test_abstract(self) -> None:
    with pytest.raises(TypeError):
        baa.ServerContext()

def Test_SessionContext_test_abstract(self) -> None:
    with pytest.raises(TypeError):
        baa.SessionContext()