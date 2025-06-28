import pytest
pytest
import bokeh.application.handlers.handler as bahh

def Test_Handler_test_create(self) -> None:
    h = bahh.Handler()
    assert h.failed == False
    assert h.url_path() is None
    assert h.static_path() is None
    assert h.error is None
    assert h.error_detail is None

def Test_Handler_test_modify_document_abstract(self) -> None:
    h = bahh.Handler()
    with pytest.raises(NotImplementedError):
        h.modify_document('doc')

def Test_Handler_test_default_server_hooks_return_none(self) -> None:
    h = bahh.Handler()
    assert h.on_server_loaded('context') is None
    assert h.on_server_unloaded('context') is None

def Test_Handler_test_static_path(self) -> None:
    h = bahh.Handler()
    assert h.static_path() is None
    h._static = 'path'
    assert h.static_path() == 'path'
    h._failed = True
    assert h.static_path() is None

def Test_Handler_test_process_request(self) -> None:
    h = bahh.Handler()
    assert h.process_request('request') == {}