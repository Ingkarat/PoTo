import pytest
pytest
from bokeh._testing.util.api import verify_all
ALL = ('AAPL', 'FB', 'GOOG', 'IBM', 'MSFT')
Test___all__ = pytest.mark.sampledata(verify_all('bokeh.sampledata.stocks', ALL))

@pytest.mark.sampledata
@pytest.mark.parametrize('name', ['AAPL', 'FB', 'GOOG', 'IBM', 'MSFT'])
def test_data(name) -> None:
    name = 'AAPL'
    import bokeh.sampledata.stocks as bss
    data = getattr(bss, name)
    assert isinstance(data, dict)