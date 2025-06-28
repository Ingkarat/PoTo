import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('frontalface_default_path',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.haar_cascade', ALL))

@pytest.mark.sampledata
def test_data(pd) -> None:
    import bokeh.sampledata.haar_cascade as bsh
    assert isinstance(bsh.frontalface_default_path, str)