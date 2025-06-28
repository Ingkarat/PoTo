import pytest
pytest
from bokeh.server.views.auth_mixin import AuthMixin
from bokeh.server.views.root_handler import RootHandler

def test_uses_auth_mixin() -> None:
    assert issubclass(RootHandler, AuthMixin)