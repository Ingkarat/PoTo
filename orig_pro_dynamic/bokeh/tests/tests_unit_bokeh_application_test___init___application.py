import pytest
pytest
from bokeh._testing.util.api import verify_all
import bokeh.application as ba
ALL = ('Application',)
Test___all__ = verify_all(ba, ALL)