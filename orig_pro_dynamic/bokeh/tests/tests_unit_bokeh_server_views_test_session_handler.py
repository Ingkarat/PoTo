import pytest
pytest
from bokeh.server.views.auth_mixin import AuthMixin
from bokeh.server.views.session_handler import SessionHandler

def test_uses_auth_mixin() -> None:
    assert issubclass(SessionHandler, AuthMixin)