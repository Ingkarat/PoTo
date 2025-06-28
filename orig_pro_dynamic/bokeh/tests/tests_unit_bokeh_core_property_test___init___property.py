import pytest
pytest
from bokeh._testing.util.api import verify_all
import bokeh.core.property as bcp
ALL = ()
Test___all__ = verify_all(bcp, ALL)