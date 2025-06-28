import pytest
pytest
from bokeh.models import FixedTicker
import bokeh.models.axes as bma

def test_ticker_accepts_number_sequences() -> None:
    a = bma.Axis(ticker=[-10, 0, 10, 20.7])
    assert isinstance(a.ticker, FixedTicker)
    assert a.ticker.ticks == [-10, 0, 10, 20.7]
    a = bma.Axis()
    a.ticker = [-10, 0, 10, 20.7]
    assert isinstance(a.ticker, FixedTicker)
    assert a.ticker.ticks == [-10, 0, 10, 20.7]