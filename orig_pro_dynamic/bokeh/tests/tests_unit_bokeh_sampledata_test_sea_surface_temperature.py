import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('sea_surface_temperature',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.sea_surface_temperature', ALL))

@pytest.mark.sampledata
def test_sea_surface_temperature(pd) -> None:
    import bokeh.sampledata.sea_surface_temperature as bss
    assert isinstance(bss.sea_surface_temperature, pd.DataFrame)
    assert len(bss.sea_surface_temperature) == 19226