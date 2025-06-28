import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('movie_path',)
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.movies_data', ALL))

@pytest.mark.sampledata
def test_movie_path() -> None:
    import bokeh.sampledata.movies_data as bsm
    assert isinstance(bsm.movie_path, str)