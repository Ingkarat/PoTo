import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('data',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.us_marriages_divorces', ALL))

@pytest.mark.sampledata
def test_data(pd) -> None:
    import bokeh.sampledata.us_marriages_divorces as bsu
    assert isinstance(bsu.data, pd.DataFrame)
    assert len(bsu.data) == 145