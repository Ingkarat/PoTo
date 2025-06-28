import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('us_holidays',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.us_holidays', ALL))

@pytest.mark.sampledata
def test_us_holidays() -> None:
    import bokeh.sampledata.us_holidays as bsu
    assert isinstance(bsu.us_holidays, list)
    assert len(bsu.us_holidays) == 305