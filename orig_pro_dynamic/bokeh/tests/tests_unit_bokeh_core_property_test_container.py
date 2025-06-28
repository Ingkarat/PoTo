import pytest
pytest
import numpy as np
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
from bokeh.core.properties import Float, Instance, Int, String
import bokeh.core.property.container as bcpc
ALL = ('Array', 'ColumnData', 'Dict', 'List', 'RelativeDelta', 'Seq', 'Tuple')
Test___all__ = verify_all(bcpc, ALL)

def Test_Array_test_init(self) -> None:
    with pytest.raises(TypeError):
        bcpc.Array()

def Test_Array_test_valid(self) -> None:
    prop = bcpc.Array(Float)
    assert prop.is_valid(None)
    assert prop.is_valid(np.array([1, 2, 3]))

def Test_Array_test_invalid(self) -> None:
    prop = bcpc.Array(Float)
    assert not prop.is_valid(False)
    assert not prop.is_valid(True)
    assert not prop.is_valid(0)
    assert not prop.is_valid(1)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())

def Test_Array_test_has_ref(self) -> None:
    prop = bcpc.Array(Float)
    assert not prop.has_ref

def Test_Array_test_str(self) -> None:
    prop = bcpc.Array(Float)
    assert str(prop) == 'Array(Float)'

def Test_Dict_test_init(self) -> None:
    with pytest.raises(TypeError):
        bcpc.Dict()

def Test_Dict_test_valid(self) -> None:
    prop = bcpc.Dict(String, bcpc.List(Int))
    assert prop.is_valid(None)
    assert prop.is_valid({})
    assert prop.is_valid({'foo': [1, 2, 3]})

def Test_Dict_test_invalid(self) -> None:
    prop = bcpc.Dict(String, bcpc.List(Int))
    assert not prop.is_valid(False)
    assert not prop.is_valid(True)
    assert not prop.is_valid(0)
    assert not prop.is_valid(1)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({'foo': [1, 2, 3.5]})
    assert not prop.is_valid(np.array([1, 2, 3]))
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())

def Test_Dict_test_has_ref(self) -> None:
    prop = bcpc.Dict(String, Int)
    assert not prop.has_ref
    prop = bcpc.Dict(String, Instance(_TestModel))
    assert prop.has_ref

def Test_Dict_test_str(self) -> None:
    prop = bcpc.Dict(String, Int)
    assert str(prop) == 'Dict(String, Int)'

def Test_List_test_init(self) -> None:
    with pytest.raises(TypeError):
        bcpc.List()

def Test_List_test_valid(self) -> None:
    prop = bcpc.List(Int)
    assert prop.is_valid(None)
    assert prop.is_valid([])
    assert prop.is_valid([1, 2, 3])

def Test_List_test_invalid(self) -> None:
    prop = bcpc.List(Int)
    assert not prop.is_valid(False)
    assert not prop.is_valid(True)
    assert not prop.is_valid(0)
    assert not prop.is_valid(1)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid([1, 2, 3.5])
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid({})
    assert not prop.is_valid(np.array([1, 2, 3]))
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())

def Test_List_test_has_ref(self) -> None:
    prop = bcpc.List(Int)
    assert not prop.has_ref
    prop = bcpc.List(Instance(_TestModel))
    assert prop.has_ref

def Test_List_test_str(self) -> None:
    prop = bcpc.List(Int)
    assert str(prop) == 'List(Int)'

def Test_Seq_test_init(self) -> None:
    with pytest.raises(TypeError):
        bcpc.Seq()

def Test_Seq_test_valid(self) -> None:
    prop = bcpc.Seq(Int)
    assert prop.is_valid(None)
    assert prop.is_valid(())
    assert prop.is_valid([])
    assert prop.is_valid(np.array([1, 2, 3]))
    assert prop.is_valid((1, 2))
    assert prop.is_valid([1, 2])
    assert prop.is_valid(np.array([1, 2]))

def Test_Seq_test_invalid(self) -> None:
    prop = bcpc.Seq(Int)
    assert not prop.is_valid(False)
    assert not prop.is_valid(True)
    assert not prop.is_valid(0)
    assert not prop.is_valid(1)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(set())
    assert not prop.is_valid({})
    assert not prop.is_valid({1, 2})
    assert not prop.is_valid({1: 2})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())

def Test_Seq_test_with_pandas_valid(self, pd) -> None:
    prop = bcpc.Seq(Int)
    df = pd.DataFrame([1, 2])
    assert prop.is_valid(df.index)
    assert prop.is_valid(df.iloc[0])

def Test_Seq_test_has_ref(self) -> None:
    prop = bcpc.Seq(Int)
    assert not prop.has_ref
    prop = bcpc.Seq(Instance(_TestModel))
    assert prop.has_ref

def Test_Seq_test_str(self) -> None:
    prop = bcpc.Seq(Int)
    assert str(prop) == 'Seq(Int)'

def Test_Tuple_test_Tuple(self) -> None:
    with pytest.raises(TypeError):
        bcpc.Tuple()
    with pytest.raises(TypeError):
        bcpc.Tuple(Int)

def Test_Tuple_test_valid(self) -> None:
    prop = bcpc.Tuple(Int, String, bcpc.List(Int))
    assert prop.is_valid(None)
    assert prop.is_valid((1, '', [1, 2, 3]))

def Test_Tuple_test_invalid(self) -> None:
    prop = bcpc.Tuple(Int, String, bcpc.List(Int))
    assert not prop.is_valid(False)
    assert not prop.is_valid(True)
    assert not prop.is_valid(0)
    assert not prop.is_valid(1)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(np.array([1, 2, 3]))
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid((1.0, '', [1, 2, 3]))
    assert not prop.is_valid((1, True, [1, 2, 3]))
    assert not prop.is_valid((1, '', (1, 2, 3)))
    assert not prop.is_valid((1, '', [1, 2, 'xyz']))

def Test_Tuple_test_has_ref(self) -> None:
    prop = bcpc.Tuple(Int, Int)
    assert not prop.has_ref
    prop = bcpc.Tuple(Int, Instance(_TestModel))
    assert prop.has_ref

def Test_Tuple_test_str(self) -> None:
    prop = bcpc.Tuple(Int, Int)
    assert str(prop) == 'Tuple(Int, Int)'