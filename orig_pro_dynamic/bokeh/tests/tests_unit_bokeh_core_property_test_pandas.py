import pytest
pytest
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
import bokeh.core.property.pandas as bcpp
ALL = ('PandasDataFrame', 'PandasGroupBy')
Test___all__ = verify_all(bcpp, ALL)

def Test_PandasDataFrame_test_valid(self, pd) -> None:
    prop = bcpp.PandasDataFrame()
    assert prop.is_valid(pd.DataFrame())

def Test_PandasDataFrame_test_invalid(self) -> None:
    prop = bcpp.PandasDataFrame()
    assert not prop.is_valid(None)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())

def Test_PandasGroupBy_test_valid(self, pd) -> None:
    prop = bcpp.PandasGroupBy()
    assert prop.is_valid(pd.core.groupby.GroupBy(pd.DataFrame()))

def Test_PandasGroupBy_test_invalid(self) -> None:
    prop = bcpp.PandasGroupBy()
    assert not prop.is_valid(None)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())