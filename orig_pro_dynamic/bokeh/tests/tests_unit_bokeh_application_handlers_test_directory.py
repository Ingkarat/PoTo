import pytest
pytest
import jinja2
from bokeh._testing.util.filesystem import with_directory_contents
from bokeh.core.templates import FILE
from bokeh.document import Document
import bokeh.application.handlers.directory as bahd
script_adds_two_roots_template = '\nfrom bokeh.io import curdoc\nfrom bokeh.model import Model\nfrom bokeh.core.properties import Int, Instance\n\nclass %s(Model):\n    bar = Int(1)\n\nclass %s(Model):\n    foo = Int(2)\n    child = Instance(Model)\n\ncurdoc().add_root(%s())\ncurdoc().add_root(%s())\n'
script_has_lifecycle_handlers = '\ndef on_server_loaded(server_context):\n    return "on_server_loaded"\ndef on_server_unloaded(server_context):\n    return "on_server_unloaded"\ndef on_session_created(session_context):\n    return "on_session_created"\ndef on_session_destroyed(session_context):\n    return "on_session_destroyed"\n'
script_has_request_handler = "\ndef process_request(request):\n    return request['headers']\n"
script_has_lifecycle_and_request_handlers = script_has_lifecycle_handlers + script_has_request_handler

def script_adds_two_roots(some_model_name, another_model_name):
    return script_adds_two_roots_template % (another_model_name, some_model_name, another_model_name, some_model_name)

def Test_DirectoryHandler_test_directory_empty_mainpy(self) -> None:
    doc = Document()

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        handler.modify_document(doc)
        if handler.failed:
            raise RuntimeError(handler.error)
    with_directory_contents({'main.py': '# This script does nothing'}, load)
    assert not doc.roots

def Test_DirectoryHandler_test_directory_initpy(self) -> None:
    doc = Document()
    results = {}

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        handler.modify_document(doc)
        handler.on_server_loaded('server_context')
        results['package'] = handler._package is not None and handler._package_runner is not None and handler._package_runner.ran
        if handler.failed:
            raise RuntimeError(handler.error)
    with_directory_contents({'main.py': 'from . import foo\n' + script_adds_two_roots('SomeModelInTestDirectory', 'AnotherModelInTestDirectory'), '__init__.py': '', 'foo.py': ' # this script does nothing'}, load)
    assert len(doc.roots) == 2
    assert results['package'] == True

def Test_DirectoryHandler_test_directory_mainpy_adds_roots(self) -> None:
    doc = Document()

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        handler.modify_document(doc)
        if handler.failed:
            raise RuntimeError(handler.error)
    with_directory_contents({'main.py': script_adds_two_roots('SomeModelInTestDirectory', 'AnotherModelInTestDirectory')}, load)
    assert len(doc.roots) == 2

def Test_DirectoryHandler_test_directory_empty_mainipynb(self) -> None:
    import nbformat
    doc = Document()
    source = nbformat.v4.new_notebook()
    result = {}

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        handler.modify_document(doc)
        result['handler'] = handler
        result['filename'] = filename
        if handler.failed:
            raise RuntimeError(handler.error)
    with_directory_contents({'main.ipynb': nbformat.writes(source)}, load)
    assert not doc.roots

def Test_DirectoryHandler_test_directory_mainipynb_adds_roots(self) -> None:
    import nbformat
    doc = Document()
    source = nbformat.v4.new_notebook()
    code = script_adds_two_roots('SomeModelInNbTestDirectory', 'AnotherModelInNbTestDirectory')
    source.cells.append(nbformat.v4.new_code_cell(code))
    result = {}

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        handler.modify_document(doc)
        result['handler'] = handler
        result['filename'] = filename
        if handler.failed:
            raise RuntimeError(handler.error)
    with_directory_contents({'main.ipynb': nbformat.writes(source)}, load)
    assert len(doc.roots) == 2

def Test_DirectoryHandler_test_directory_both_mainipynb_and_mainpy(self) -> None:
    doc = Document()

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        handler.modify_document(doc)
        if handler.failed:
            raise RuntimeError(handler.error)
    import nbformat
    source = nbformat.v4.new_notebook()
    with_directory_contents({'main.py': script_adds_two_roots('SomeModelInTestDirectory', 'AnotherModelInTestDirectory'), 'main.ipynb': nbformat.writes(source)}, load)
    assert len(doc.roots) == 2

def Test_DirectoryHandler_test_directory_missing_main(self) -> None:
    doc = Document()

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        handler.modify_document(doc)
        if handler.failed:
            raise RuntimeError(handler.error)
    with pytest.raises(ValueError):
        with_directory_contents({}, load)

def Test_DirectoryHandler_test_directory_has_theme_file(self) -> None:
    doc = Document()

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        handler.modify_document(doc)
        if handler.failed:
            raise RuntimeError(handler.error)
    custom_theme = '\nattrs:\n    AnotherModelInTestDirectoryTheme:\n        bar: 42\n    SomeModelInTestDirectoryTheme:\n        foo: 14\n'
    with_directory_contents({'main.py': script_adds_two_roots('SomeModelInTestDirectoryTheme', 'AnotherModelInTestDirectoryTheme') + "\n# we're testing that the script can override the theme\nsome = next(m for m in curdoc().roots if isinstance(m, SomeModelInTestDirectoryTheme))\nsome.foo = 57\n            ", 'theme.yaml': custom_theme}, load)
    assert len(doc.roots) == 2
    some_model = next((m for m in doc.roots if m.__class__.__name__ == 'SomeModelInTestDirectoryTheme'))
    another_model = next((m for m in doc.roots if m.__class__.__name__ == 'AnotherModelInTestDirectoryTheme'))
    assert another_model.bar == 42
    assert some_model.foo == 57
    del some_model.foo
    assert some_model.foo == 14
    doc.theme = None
    assert some_model.foo == 2
    assert another_model.bar == 1

def Test_DirectoryHandler_load(filename):
    handler = bahd.DirectoryHandler(filename=filename)
    result['handler'] = handler
    handler.modify_document(doc)
    if handler.failed:
        raise RuntimeError(handler.error)

def Test_DirectoryHandler_load(filename):
    handler = bahd.DirectoryHandler(filename=filename)
    result['handler'] = handler
    handler.modify_document(doc)
    if handler.failed:
        raise RuntimeError(handler.error)

def Test_DirectoryHandler_load(filename):
    with pytest.raises(ValueError):
        bahd.DirectoryHandler(filename=filename)

def Test_DirectoryHandler_load(filename):
    handler = bahd.DirectoryHandler(filename=filename)
    result['handler'] = handler
    handler.modify_document(doc)
    if handler.failed:
        raise RuntimeError(handler.error)

def Test_DirectoryHandler_test_directory_with_static(self) -> None:
    doc = Document()
    result = {}

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        result['handler'] = handler
        handler.modify_document(doc)
        if handler.failed:
            raise RuntimeError(handler.error)
    with_directory_contents({'main.py': '# This script does nothing', 'static/js/foo.js': '# some JS'}, load)
    assert not doc.roots
    handler = result['handler']
    assert handler.static_path() is not None
    assert handler.static_path().endswith('static')

def Test_DirectoryHandler_test_directory_without_static(self) -> None:
    doc = Document()
    result = {}

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        result['handler'] = handler
        handler.modify_document(doc)
        if handler.failed:
            raise RuntimeError(handler.error)
    with_directory_contents({'main.py': '# This script does nothing'}, load)
    assert not doc.roots
    handler = result['handler']
    assert handler.static_path() is None

def Test_DirectoryHandler_test_directory_with_template(self) -> None:
    doc = Document()
    result = {}

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        result['handler'] = handler
        handler.modify_document(doc)
        if handler.failed:
            raise RuntimeError(handler.error)
    with_directory_contents({'main.py': '# This script does nothing', 'templates/index.html': '<div>some HTML</div>'}, load)
    assert not doc.roots
    assert isinstance(doc.template, jinja2.Template)

def Test_DirectoryHandler_test_directory_without_template(self) -> None:
    doc = Document()
    result = {}

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        result['handler'] = handler
        handler.modify_document(doc)
        if handler.failed:
            raise RuntimeError(handler.error)
    with_directory_contents({'main.py': '# This script does nothing'}, load)
    assert not doc.roots
    assert doc.template is FILE

def Test_DirectoryHandler_test_safe_to_fork(self) -> None:
    doc = Document()
    result = {}

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        assert handler.safe_to_fork
        result['handler'] = handler
        handler.modify_document(doc)
        if handler.failed:
            raise RuntimeError(handler.error)
        assert not handler.safe_to_fork
    with_directory_contents({'main.py': '# This script does nothing'}, load)

def Test_DirectoryHandler_test_missing_filename_raises(self) -> None:
    with pytest.raises(ValueError):
        bahd.DirectoryHandler()

def Test_DirectoryHandler_test_url_path(self) -> None:
    doc = Document()
    result = {}

    def load(filename):
        handler = bahd.DirectoryHandler(filename=filename)
        assert handler.safe_to_fork
        result['handler'] = handler
        handler.modify_document(doc)
        if handler.failed:
            raise RuntimeError(handler.error)
        assert not handler.safe_to_fork
    with_directory_contents({'main.py': '# This script does nothing'}, load)
    h = result['handler']
    assert h.url_path().startswith('/')
    h._main_handler._runner._failed = True
    assert h.url_path() is None