import pytest
pytest
import bokeh.document as document
from bokeh.core.properties import Instance, Int
from bokeh.model import Model
from bokeh.protocol import Protocol
proto = Protocol()

def TestPullDocument__sample_doc(self):
    doc = document.Document()
    another = AnotherModelInTestPullDoc()
    doc.add_root(SomeModelInTestPullDoc(child=another))
    doc.add_root(SomeModelInTestPullDoc())
    return doc

def TestPullDocument_test_create_req(self) -> None:
    proto.create('PULL-DOC-REQ')

def TestPullDocument_test_create_reply(self) -> None:
    sample = self._sample_doc()
    proto.create('PULL-DOC-REPLY', 'fakereqid', sample)

def TestPullDocument_test_create_reply_then_parse(self) -> None:
    sample = self._sample_doc()
    msg = proto.create('PULL-DOC-REPLY', 'fakereqid', sample)
    copy = document.Document()
    msg.push_to_document(copy)
    assert len(sample.roots) == 2
    assert len(copy.roots) == 2