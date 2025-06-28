import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('data',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.world_cities', ALL))

@pytest.mark.sampledata
def test_data(pd) -> None:
    import bokeh.sampledata.world_cities as bsw
    assert isinstance(bsw.data, pd.DataFrame)