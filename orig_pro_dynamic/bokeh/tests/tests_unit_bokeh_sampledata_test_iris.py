import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('flowers',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.iris', ALL))

@pytest.mark.sampledata
def test_flowers(pd) -> None:
    import bokeh.sampledata.iris as bsi
    assert isinstance(bsi.flowers, pd.DataFrame)
    assert len(bsi.flowers) == 150