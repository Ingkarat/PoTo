import pytest
pytest
from bokeh._testing.util.filesystem import with_file_contents
from bokeh.document import Document
import bokeh.application.handlers.script as bahs

def Test_ScriptHandler_test_runner_uses_source_from_filename(self) -> None:
    doc = Document()
    source = '# Test contents for script'
    result = {}

    def load(filename):
        handler = bahs.ScriptHandler(filename=filename)
        handler.modify_document(doc)
        result['handler'] = handler
        result['filename'] = filename
    with_file_contents(source, load)
    assert result['handler']._runner.path == result['filename']
    assert result['handler']._runner.source == source
    assert not doc.roots

def Test_ScriptHandler_test_runner_script_with_encoding(self) -> None:
    doc = Document()
    source = '# -*- coding: utf-8 -*-\nimport os'
    result = {}

    def load(filename):
        handler = bahs.ScriptHandler(filename=filename)
        handler.modify_document(doc)
        result['handler'] = handler
        result['filename'] = filename
    with_file_contents(source, load)
    assert result['handler'].error is None
    assert result['handler'].failed is False
    assert not doc.roots

def Test_ScriptHandler_test_missing_filename_raises(self) -> None:
    with pytest.raises(ValueError):
        bahs.ScriptHandler()