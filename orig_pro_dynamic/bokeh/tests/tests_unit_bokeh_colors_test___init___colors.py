import pytest
pytest
from bokeh._testing.util.api import verify_all
import bokeh.colors as bc
ALL = ('Color', 'HSL', 'RGB', 'groups', 'named')
Test___all__ = verify_all(bc, ALL)