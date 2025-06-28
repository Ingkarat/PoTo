import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('airports', 'routes')
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.airport_routes', ALL))

@pytest.mark.sampledata
def test_airports(pd) -> None:
    import bokeh.sampledata.airport_routes as bsa
    assert isinstance(bsa.airports, pd.DataFrame)

@pytest.mark.sampledata
def test_routes(pd) -> None:
    import bokeh.sampledata.airport_routes as bsa
    assert isinstance(bsa.routes, pd.DataFrame)