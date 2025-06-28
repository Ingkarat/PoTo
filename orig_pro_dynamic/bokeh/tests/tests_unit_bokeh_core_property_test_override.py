import pytest
pytest
from bokeh._testing.util.api import verify_all
import bokeh.core.property.override as bcpo
ALL = ('Override',)
Test___all__ = verify_all(bcpo, ALL)

def Test_Override_test_create_default(self) -> None:
    o = bcpo.Override(default=10)
    assert o.default_overridden
    assert o.default == 10

def Test_Override_test_create_no_args(self) -> None:
    with pytest.raises(ValueError):
        bcpo.Override()

def Test_Override_test_create_unkown_args(self) -> None:
    with pytest.raises(ValueError):
        bcpo.Override(default=10, junk=20)
    with pytest.raises(ValueError):
        bcpo.Override(junk=20)