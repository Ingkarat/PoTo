import pytest
pytest
import bokeh.util.dependencies as dep

def Test_import_optional_test_success(self) -> None:
    assert dep.import_optional('sys') is not None

def Test_import_optional_test_fail(self) -> None:
    assert dep.import_optional('bleepbloop') is None

def Test_import_required_test_success(self) -> None:
    assert dep.import_required('sys', 'yep') is not None

def Test_import_required_test_fail(self) -> None:
    with pytest.raises(RuntimeError) as excinfo:
        dep.import_required('bleepbloop', 'nope')
    assert 'nope' in str(excinfo.value)