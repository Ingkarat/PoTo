import pytest
pytest
import logging
from bokeh.document import Document
import bokeh.application.handlers.document_lifecycle as bahd

def MockSessionContext___init__(self, doc):
    self._document = doc
    self.status = None
    self.counter = 0

def Test_DocumentLifecycleHandler_test_document_bad_on_session_destroyed_signature(self) -> None:
    doc = Document()

    def destroy(a, b):
        pass
    with pytest.raises(ValueError):
        doc.on_session_destroyed(destroy)

def Test_DocumentLifecycleHandler_destroy(session_context):
    assert doc is session_context._document
    session_context.status = 'Destroyed'

def Test_DocumentLifecycleHandler_increment(session_context):
    session_context.counter += 1

def Test_DocumentLifecycleHandler_increment_by_two(session_context):
    session_context.counter += 2

def Test_DocumentLifecycleHandler_blowup(session_context):
    raise ValueError('boom!')