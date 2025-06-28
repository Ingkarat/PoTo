import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('fertility', 'life_expectancy', 'population', 'regions')
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.gapminder', ALL))

@pytest.mark.sampledata
@pytest.mark.parametrize('name', ['fertility', 'life_expectancy', 'population', 'regions'])
def test_data(pd, name) -> None:
    name = 'fertility'
    import bokeh.sampledata.gapminder as bsg
    data = getattr(bsg, name)
    assert isinstance(data, pd.DataFrame)