import pytest
pytest
from bokeh.core.properties import Int, String
from bokeh.util.options import Options

def test_empty() -> None:
    empty = dict()
    o = DummyOpts(empty)
    assert o.foo == 'thing'
    assert o.bar == None
    assert empty == {}

def test_exact() -> None:
    exact = dict(foo='stuff', bar=10)
    o = DummyOpts(exact)
    assert o.foo == 'stuff'
    assert o.bar == 10
    assert exact == {}

def test_extra() -> None:
    extra = dict(foo='stuff', bar=10, baz=22.2)
    o = DummyOpts(extra)
    assert o.foo == 'stuff'
    assert o.bar == 10
    assert extra == {'baz': 22.2}

def test_mixed() -> None:
    mixed = dict(foo='stuff', baz=22.2)
    o = DummyOpts(mixed)
    assert o.foo == 'stuff'
    assert o.bar == None
    assert mixed == {'baz': 22.2}