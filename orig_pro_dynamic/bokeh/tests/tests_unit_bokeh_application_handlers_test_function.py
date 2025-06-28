import pytest
pytest
from bokeh.core.properties import Instance, Int
from bokeh.document import Document
from bokeh.model import Model
import bokeh.application.handlers.function as bahf

def Test_FunctionHandler_test_empty_func(self) -> None:

    def noop(doc):
        pass
    handler = bahf.FunctionHandler(noop)
    doc = Document()
    handler.modify_document(doc)
    if handler.failed:
        raise RuntimeError(handler.error)
    assert not doc.roots

def Test_FunctionHandler_test_func_adds_roots(self) -> None:

    def add_roots(doc):
        doc.add_root(AnotherModelInTestFunction())
        doc.add_root(SomeModelInTestFunction())
    handler = bahf.FunctionHandler(add_roots)
    doc = Document()
    handler.modify_document(doc)
    if handler.failed:
        raise RuntimeError(handler.error)
    assert len(doc.roots) == 2

def Test_FunctionHandler_test_safe_to_fork(self) -> None:

    def noop(doc):
        pass
    handler = bahf.FunctionHandler(noop)
    doc = Document()
    assert handler.safe_to_fork
    handler.modify_document(doc)
    if handler.failed:
        raise RuntimeError(handler.error)
    assert not handler.safe_to_fork