import pytest
pytest
from bokeh.models import Circle
import bokeh.plotting._renderer as bpr

def Test__pop_visuals_test_basic_prop(self) -> None:
    kwargs = dict(fill_alpha=0.7, line_alpha=0.8, line_color='red')
    ca = bpr.pop_visuals(Circle, kwargs)
    assert ca['fill_alpha'] == 0.7
    assert ca['line_alpha'] == 0.8
    assert ca['line_color'] == 'red'
    assert ca['fill_color'] == '#1f77b4'
    assert set(ca) == {'fill_color', 'line_color', 'fill_alpha', 'line_alpha'}

def Test__pop_visuals_test_basic_trait(self) -> None:
    kwargs = dict(fill_alpha=0.7, alpha=0.8, color='red')
    ca = bpr.pop_visuals(Circle, kwargs)
    assert ca['fill_alpha'] == 0.7
    assert ca['line_alpha'] == 0.8
    assert ca['line_color'] == 'red'
    assert ca['fill_color'] == 'red'
    assert set(ca) == {'fill_color', 'line_color', 'fill_alpha', 'line_alpha'}

def Test__pop_visuals_test_override_defaults_with_prefix(self) -> None:
    glyph_kwargs = dict(fill_alpha=1, line_alpha=1)
    kwargs = dict(alpha=0.6)
    ca = bpr.pop_visuals(Circle, kwargs, prefix='nonselection_', defaults=glyph_kwargs, override_defaults={'alpha': 0.1})
    assert ca['fill_alpha'] == 0.1
    assert ca['line_alpha'] == 0.1

def Test__pop_visuals_test_defaults(self) -> None:
    kwargs = dict(fill_alpha=0.7, line_alpha=0.8, line_color='red')
    ca = bpr.pop_visuals(Circle, kwargs, defaults=dict(line_color='blue', fill_color='green'))
    assert ca['fill_alpha'] == 0.7
    assert ca['line_alpha'] == 0.8
    assert ca['line_color'] == 'red'
    assert ca['fill_color'] == 'green'
    assert set(ca) == {'fill_color', 'line_color', 'fill_alpha', 'line_alpha'}

def Test__pop_visuals_test_override_defaults(self) -> None:
    kwargs = dict(fill_alpha=0.7, line_alpha=0.8)
    ca = bpr.pop_visuals(Circle, kwargs, defaults=dict(line_color='blue', fill_color='green'), override_defaults=dict(color='white'))
    assert ca['fill_alpha'] == 0.7
    assert ca['line_alpha'] == 0.8
    assert ca['line_color'] == 'white'
    assert ca['fill_color'] == 'white'
    assert set(ca) == {'fill_color', 'line_color', 'fill_alpha', 'line_alpha'}