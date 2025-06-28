import pytest
pytest
from bokeh._testing.util.api import verify_all
import bokeh.sampledata as bs
ALL = ('download',)
Test___all__ = verify_all(bs, ALL)