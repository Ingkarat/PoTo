import pytest
pytest
from bokeh.server.views.auth_mixin import AuthMixin
from bokeh.server.views.metadata_handler import MetadataHandler

def test_uses_auth_mixin() -> None:
    assert issubclass(MetadataHandler, AuthMixin)