import pytest
pytest
import bokeh.document as document
from bokeh.core.properties import Instance, Int
from bokeh.model import Model
from bokeh.protocol import Protocol
proto = Protocol()

def TestPushDocument__sample_doc(self):
    doc = document.Document()
    another = AnotherModelInTestPushDoc()
    doc.add_root(SomeModelInTestPushDoc(child=another))
    doc.add_root(SomeModelInTestPushDoc())
    return doc

def TestPushDocument_test_create(self) -> None:
    sample = self._sample_doc()
    proto.create('PUSH-DOC', sample)

def TestPushDocument_test_create_then_parse(self) -> None:
    sample = self._sample_doc()
    msg = proto.create('PUSH-DOC', sample)
    copy = document.Document()
    msg.push_to_document(copy)
    assert len(sample.roots) == 2
    assert len(copy.roots) == 2