import pytest
pytest
from bokeh._testing.util.api import verify_all
from bokeh.core.has_props import HasProps
from bokeh.core.properties import Int, Override, String
import bokeh.core.property.include as bcpi
ALL = ('Include',)
Test___all__ = verify_all(bcpi, ALL)

def Test_Include_test_include_with_prefix(self) -> None:

    class IncludesDelegateWithPrefix(HasProps):
        z = bcpi.Include(IsDelegate, use_prefix=True)
        z_y = Int(57)
    o = IncludesDelegateWithPrefix()
    assert o.z_x == 12
    assert o.z_y == 57
    assert not hasattr(o, 'z')
    assert not hasattr(o, 'x')
    assert not hasattr(o, 'y')
    assert 'z' not in o.properties_with_values(include_defaults=True)
    assert 'x' not in o.properties_with_values(include_defaults=True)
    assert 'y' not in o.properties_with_values(include_defaults=True)
    assert 'z_x' in o.properties_with_values(include_defaults=True)
    assert 'z_y' in o.properties_with_values(include_defaults=True)
    assert 'z_x' not in o.properties_with_values(include_defaults=False)
    assert 'z_y' not in o.properties_with_values(include_defaults=False)

def Test_Include_test_include_without_prefix(self) -> None:

    class IncludesDelegateWithoutPrefix(HasProps):
        z = bcpi.Include(IsDelegate, use_prefix=False)
        y = Int(42)
    o = IncludesDelegateWithoutPrefix()
    assert o.x == 12
    assert o.y == 42
    assert not hasattr(o, 'z')
    assert 'x' in o.properties_with_values(include_defaults=True)
    assert 'y' in o.properties_with_values(include_defaults=True)
    assert 'x' not in o.properties_with_values(include_defaults=False)
    assert 'y' not in o.properties_with_values(include_defaults=False)

def Test_Include_test_include_without_prefix_using_override(self) -> None:

    class IncludesDelegateWithoutPrefixUsingOverride(HasProps):
        z = bcpi.Include(IsDelegate, use_prefix=False)
        y = Override(default='world')
    o = IncludesDelegateWithoutPrefixUsingOverride()
    assert o.x == 12
    assert o.y == 'world'
    assert not hasattr(o, 'z')
    assert 'x' in o.properties_with_values(include_defaults=True)
    assert 'y' in o.properties_with_values(include_defaults=True)
    assert 'x' not in o.properties_with_values(include_defaults=False)
    assert 'y' not in o.properties_with_values(include_defaults=False)