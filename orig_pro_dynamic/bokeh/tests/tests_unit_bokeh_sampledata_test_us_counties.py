import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('data',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.us_counties', ALL))

@pytest.mark.sampledata
def test_data() -> None:
    import bokeh.sampledata.us_counties as bsu
    assert isinstance(bsu.data, dict)