import pytest
pytest
from bokeh._testing.util.filesystem import with_file_contents
from bokeh.document import Document
import bokeh.application.handlers.server_lifecycle as bahs
script_adds_four_handlers = '\ndef on_server_loaded(server_context):\n    return "on_server_loaded"\ndef on_server_unloaded(server_context):\n    return "on_server_unloaded"\ndef on_session_created(session_context):\n    return "on_session_created"\ndef on_session_destroyed(session_context):\n    return "on_session_destroyed"\n'

def Test_ServerLifecycleHandler_load(filename):
    handler = bahs.ServerLifecycleHandler(filename=filename)
    handler.modify_document(doc)
    out['handler'] = handler

def Test_ServerLifecycleHandler_test_lifecycle_bad_syntax(self) -> None:
    result = {}

    def load(filename):
        handler = bahs.ServerLifecycleHandler(filename=filename)
        result['handler'] = handler
    with_file_contents('This is a syntax error', load)
    handler = result['handler']
    assert handler.error is not None
    assert 'Invalid syntax' in handler.error

def Test_ServerLifecycleHandler_test_lifecycle_runtime_error(self) -> None:
    result = {}

    def load(filename):
        handler = bahs.ServerLifecycleHandler(filename=filename)
        result['handler'] = handler
    with_file_contents("raise RuntimeError('nope')", load)
    handler = result['handler']
    assert handler.error is not None
    assert 'nope' in handler.error

def Test_ServerLifecycleHandler_test_lifecycle_bad_server_loaded_signature(self) -> None:
    result = {}

    def load(filename):
        handler = bahs.ServerLifecycleHandler(filename=filename)
        result['handler'] = handler
    with_file_contents('\ndef on_server_loaded(a,b):\n    pass\n', load)
    handler = result['handler']
    assert handler.error is not None
    assert 'on_server_loaded must have signature func(server_context)' in handler.error
    assert 'func(a, b)' in handler.error
    assert 'Traceback' in handler.error_detail

def Test_ServerLifecycleHandler_test_lifecycle_bad_server_unloaded_signature(self) -> None:
    result = {}

    def load(filename):
        handler = bahs.ServerLifecycleHandler(filename=filename)
        result['handler'] = handler
    with_file_contents('\ndef on_server_unloaded(a,b):\n    pass\n', load)
    handler = result['handler']
    assert handler.error is not None
    assert 'on_server_unloaded must have signature func(server_context)' in handler.error
    assert 'func(a, b)' in handler.error
    assert 'Traceback' in handler.error_detail

def Test_ServerLifecycleHandler_test_lifecycle_bad_session_created_signature(self) -> None:
    result = {}

    def load(filename):
        handler = bahs.ServerLifecycleHandler(filename=filename)
        result['handler'] = handler
    with_file_contents('\ndef on_session_created(a,b):\n    pass\n', load)
    handler = result['handler']
    assert handler.error is not None
    assert 'on_session_created must have signature func(session_context)' in handler.error
    assert 'func(a, b)' in handler.error

def Test_ServerLifecycleHandler_test_lifecycle_bad_session_destroyed_signature(self) -> None:
    result = {}

    def load(filename):
        handler = bahs.ServerLifecycleHandler(filename=filename)
        result['handler'] = handler
    with_file_contents('\ndef on_session_destroyed(a,b):\n    pass\n', load)
    handler = result['handler']
    assert handler.error is not None
    assert 'on_session_destroyed must have signature func(session_context)' in handler.error
    assert 'func(a, b)' in handler.error

def Test_ServerLifecycleHandler_load(filename):
    handler = result['handler'] = bahs.ServerLifecycleHandler(filename=filename)
    if handler.failed:
        raise RuntimeError(handler.error)

def Test_ServerLifecycleHandler_test_missing_filename_raises(self) -> None:
    with pytest.raises(ValueError):
        bahs.ServerLifecycleHandler()

def Test_ServerLifecycleHandler_test_url_path(self) -> None:
    result = {}

    def load(filename):
        handler = bahs.ServerLifecycleHandler(filename=filename)
        result['handler'] = handler
    with_file_contents('\ndef on_server_unloaded(server_context):\n    pass\n', load)
    handler = result['handler']
    assert handler.error is None
    assert handler.url_path().startswith('/')

def Test_ServerLifecycleHandler_test_url_path_failed(self) -> None:
    result = {}

    def load(filename):
        handler = bahs.ServerLifecycleHandler(filename=filename)
        result['handler'] = handler
    with_file_contents('\n# bad signature\ndef on_server_unloaded():\n    pass\n', load)
    handler = result['handler']
    assert handler.error is not None
    assert handler.url_path() is None