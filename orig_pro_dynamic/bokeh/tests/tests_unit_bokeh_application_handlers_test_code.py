import pytest
pytest
from bokeh.document import Document
import bokeh.application.handlers.code as bahc
script_adds_two_roots = '\nfrom bokeh.io import curdoc\nfrom bokeh.model import Model\nfrom bokeh.core.properties import Int, Instance\n\nclass AnotherModelInTestScript(Model):\n    bar = Int(1)\n\nclass SomeModelInTestScript(Model):\n    foo = Int(2)\n    child = Instance(Model)\n\ncurdoc().add_root(AnotherModelInTestScript())\ncurdoc().add_root(SomeModelInTestScript())\n'

def TestCodeHandler_test_missing_source(self) -> None:
    with pytest.raises(ValueError) as e:
        bahc.CodeHandler()
        assert str(e) == 'Must pass source to CodeHandler'

def TestCodeHandler_test_missing_filename(self) -> None:
    with pytest.raises(ValueError) as e:
        bahc.CodeHandler(source='# This script does nothing')
        assert str(e) == 'Must pass filename to CodeHandler'

def TestCodeHandler_test_empty_script(self) -> None:
    doc = Document()
    handler = bahc.CodeHandler(source='# This script does nothing', filename='path/to/test_filename')
    handler.modify_document(doc)
    if handler.failed:
        raise RuntimeError(handler.error)
    assert not doc.roots

def TestCodeHandler_test_script_adds_roots(self) -> None:
    doc = Document()
    handler = bahc.CodeHandler(source=script_adds_two_roots, filename='path/to/test_filename')
    handler.modify_document(doc)
    if handler.failed:
        raise RuntimeError(handler.error)
    assert len(doc.roots) == 2

def TestCodeHandler_test_script_bad_syntax(self) -> None:
    doc = Document()
    handler = bahc.CodeHandler(source='This is a syntax error', filename='path/to/test_filename')
    handler.modify_document(doc)
    assert handler.error is not None
    assert 'Invalid syntax' in handler.error

def TestCodeHandler_test_script_runtime_error(self) -> None:
    doc = Document()
    handler = bahc.CodeHandler(source="raise RuntimeError('nope')", filename='path/to/test_filename')
    handler.modify_document(doc)
    assert handler.error is not None
    assert 'nope' in handler.error

def TestCodeHandler_test_script_sys_path(self) -> None:
    doc = Document()
    handler = bahc.CodeHandler(source='import sys; raise RuntimeError("path: \'%s\'" % sys.path[0])', filename='path/to/test_filename')
    handler.modify_document(doc)
    assert handler.error is not None
    assert "path: 'path/to'" in handler.error

def TestCodeHandler_test_script_argv(self) -> None:
    doc = Document()
    handler = bahc.CodeHandler(source='import sys; raise RuntimeError("argv: %r" % sys.argv)', filename='path/to/test_filename')
    handler.modify_document(doc)
    assert handler.error is not None
    assert "argv: ['test_filename']" in handler.error
    doc = Document()
    handler = bahc.CodeHandler(source='import sys; raise RuntimeError("argv: %r" % sys.argv)', filename='path/to/test_filename', argv=[10, 20, 30])
    handler.modify_document(doc)
    assert handler.error is not None
    assert "argv: ['test_filename', 10, 20, 30]" in handler.error

def TestCodeHandler_test_safe_to_fork(self) -> None:
    doc = Document()
    handler = bahc.CodeHandler(source='# This script does nothing', filename='path/to/test_filename')
    assert handler.safe_to_fork
    handler.modify_document(doc)
    if handler.failed:
        raise RuntimeError(handler.error)
    assert not handler.safe_to_fork