import pytest
pytest
from mock import patch
from bokeh._testing.util.api import verify_all
from bokeh.core.properties import Angle, Any, Bool, Color, ColumnData, Complex, DashPattern, Dict, Either, Enum, Float, Instance, Int, Interval, List, MinMaxBounds, Percent, Regex, Seq, Size, String, Tuple
from bokeh.models import ColumnDataSource
import bokeh.core.property.wrappers as bcpw
ALL = ('notify_owner', 'PropertyValueContainer', 'PropertyValueList', 'PropertyValueDict', 'PropertyValueColumnData')

def test_notify_owner() -> None:
    result = {}

    class Foo:

        @bcpw.notify_owner
        def test(self):
            pass

        def _notify_owners(self, old):
            result['old'] = old

        def _saved_copy(self):
            return 'foo'
    f = Foo()
    f.test()
    assert result['old'] == 'foo'
    assert f.test.__doc__ == 'Container method ``test`` instrumented to notify property owners'

def test_PropertyValueContainer() -> None:
    pvc = bcpw.PropertyValueContainer()
    assert pvc._owners == set()
    pvc._register_owner('owner', 'prop')
    assert pvc._owners == {('owner', 'prop')}
    pvc._unregister_owner('owner', 'prop')
    assert pvc._owners == set()
    with pytest.raises(RuntimeError):
        pvc._saved_copy()

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueDict_mutators(mock_notify) -> None:
    pvd = bcpw.PropertyValueDict(dict(foo=10, bar=20, baz=30))
    mock_notify.reset_mock()
    del pvd['foo']
    assert mock_notify.called
    mock_notify.reset_mock()
    pvd['foo'] = 11
    assert mock_notify.called
    mock_notify.reset_mock()
    pvd.pop('foo')
    assert mock_notify.called
    mock_notify.reset_mock()
    pvd.popitem()
    assert mock_notify.called
    mock_notify.reset_mock()
    pvd.setdefault('baz')
    assert mock_notify.called
    mock_notify.reset_mock()
    pvd.clear()
    assert mock_notify.called
    mock_notify.reset_mock()
    pvd.update(bar=1)
    assert mock_notify.called

@patch('bokeh.core.property.descriptors.ColumnDataPropertyDescriptor._notify_mutated')
def test_PropertyValueColumnData___setitem__(mock_notify) -> None:
    from bokeh.document.events import ColumnDataChangedEvent
    source = ColumnDataSource(data=dict(foo=[10], bar=[20], baz=[30]))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    pvcd._register_owner(source, source.lookup('data'))
    mock_notify.reset_mock()
    pvcd['foo'] = [11]
    assert pvcd == dict(foo=[11], bar=[20], baz=[30])
    assert mock_notify.call_count == 1
    assert mock_notify.call_args[0] == (source, dict(foo=[10], bar=[20], baz=[30]))
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnDataChangedEvent)
    assert mock_notify.call_args[1]['hint'].column_source == source
    assert mock_notify.call_args[1]['hint'].cols == ['foo']

@patch('bokeh.core.property.descriptors.ColumnDataPropertyDescriptor._notify_mutated')
def test_PropertyValueColumnData_update(mock_notify) -> None:
    from bokeh.document.events import ColumnDataChangedEvent
    source = ColumnDataSource(data=dict(foo=[10], bar=[20], baz=[30]))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    pvcd._register_owner(source, source.lookup('data'))
    mock_notify.reset_mock()
    pvcd.update(foo=[11], bar=[21])
    assert pvcd == dict(foo=[11], bar=[21], baz=[30])
    assert mock_notify.call_count == 1
    assert mock_notify.call_args[0] == (source, dict(foo=[10], bar=[20], baz=[30]))
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnDataChangedEvent)
    assert mock_notify.call_args[1]['hint'].column_source == source
    assert sorted(mock_notify.call_args[1]['hint'].cols) == ['bar', 'foo']

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueColumnData__stream_list_to_list(mock_notify) -> None:
    from bokeh.document.events import ColumnsStreamedEvent
    source = ColumnDataSource(data=dict(foo=[10]))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    mock_notify.reset_mock()
    pvcd._stream('doc', source, dict(foo=[20]), setter='setter')
    assert mock_notify.call_count == 1
    assert mock_notify.call_args[0] == ({'foo': [10, 20]},)
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnsStreamedEvent)
    assert mock_notify.call_args[1]['hint'].setter == 'setter'
    assert mock_notify.call_args[1]['hint'].rollover == None

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueColumnData__stream_list_to_array(mock_notify) -> None:
    from bokeh.document.events import ColumnsStreamedEvent
    import numpy as np
    source = ColumnDataSource(data=dict(foo=np.array([10])))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    mock_notify.reset_mock()
    pvcd._stream('doc', source, dict(foo=[20]), setter='setter')
    assert mock_notify.call_count == 1
    assert (mock_notify.call_args[0][0]['foo'] == np.array([10])).all()
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnsStreamedEvent)
    assert mock_notify.call_args[1]['hint'].setter == 'setter'
    assert mock_notify.call_args[1]['hint'].rollover == None

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueColumnData__stream_list_with_rollover(mock_notify) -> None:
    from bokeh.document.events import ColumnsStreamedEvent
    source = ColumnDataSource(data=dict(foo=[10, 20, 30]))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    mock_notify.reset_mock()
    pvcd._stream('doc', source, dict(foo=[40]), rollover=3, setter='setter')
    assert mock_notify.call_count == 1
    assert mock_notify.call_args[0] == ({'foo': [20, 30, 40]},)
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnsStreamedEvent)
    assert mock_notify.call_args[1]['hint'].setter == 'setter'
    assert mock_notify.call_args[1]['hint'].rollover == 3

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueColumnData__stream_array_to_array(mock_notify) -> None:
    from bokeh.document.events import ColumnsStreamedEvent
    import numpy as np
    source = ColumnDataSource(data=dict(foo=np.array([10])))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    mock_notify.reset_mock()
    pvcd._stream('doc', source, dict(foo=[20]), setter='setter')
    assert mock_notify.call_count == 1
    assert len(mock_notify.call_args[0]) == 1
    assert 'foo' in mock_notify.call_args[0][0]
    assert (mock_notify.call_args[0][0]['foo'] == np.array([10])).all()
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnsStreamedEvent)
    assert mock_notify.call_args[1]['hint'].setter == 'setter'
    assert mock_notify.call_args[1]['hint'].rollover == None

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueColumnData__stream_array_to_list(mock_notify) -> None:
    from bokeh.document.events import ColumnsStreamedEvent
    source = ColumnDataSource(data=dict(foo=[10]))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    mock_notify.reset_mock()
    pvcd._stream('doc', source, dict(foo=[20]), setter='setter')
    assert mock_notify.call_count == 1
    assert len(mock_notify.call_args[0]) == 1
    assert 'foo' in mock_notify.call_args[0][0]
    assert mock_notify.call_args[0] == ({'foo': [10, 20]},)
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnsStreamedEvent)
    assert mock_notify.call_args[1]['hint'].setter == 'setter'
    assert mock_notify.call_args[1]['hint'].rollover == None

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueColumnData__stream_array_with_rollover(mock_notify) -> None:
    from bokeh.document.events import ColumnsStreamedEvent
    import numpy as np
    source = ColumnDataSource(data=dict(foo=np.array([10, 20, 30])))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    mock_notify.reset_mock()
    pvcd._stream('doc', source, dict(foo=[40]), rollover=3, setter='setter')
    assert mock_notify.call_count == 1
    assert len(mock_notify.call_args[0]) == 1
    assert 'foo' in mock_notify.call_args[0][0]
    assert (mock_notify.call_args[0][0]['foo'] == np.array([10, 20, 30])).all()
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnsStreamedEvent)
    assert mock_notify.call_args[1]['hint'].setter == 'setter'
    assert mock_notify.call_args[1]['hint'].rollover == 3

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueColumnData__patch_with_simple_indices(mock_notify) -> None:
    from bokeh.document.events import ColumnsPatchedEvent
    source = ColumnDataSource(data=dict(foo=[10, 20]))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    mock_notify.reset_mock()
    pvcd._patch('doc', source, dict(foo=[(1, 40)]), setter='setter')
    assert mock_notify.call_count == 1
    assert mock_notify.call_args[0] == ({'foo': [10, 40]},)
    assert pvcd == dict(foo=[10, 40])
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnsPatchedEvent)
    assert mock_notify.call_args[1]['hint'].setter == 'setter'

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueColumnData__patch_with_repeated_simple_indices(mock_notify) -> None:
    from bokeh.document.events import ColumnsPatchedEvent
    source = ColumnDataSource(data=dict(foo=[10, 20]))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    mock_notify.reset_mock()
    pvcd._patch('doc', source, dict(foo=[(1, 40), (1, 50)]), setter='setter')
    assert mock_notify.call_count == 1
    assert mock_notify.call_args[0] == ({'foo': [10, 50]},)
    assert pvcd == dict(foo=[10, 50])
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnsPatchedEvent)
    assert mock_notify.call_args[1]['hint'].setter == 'setter'

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueColumnData__patch_with_slice_indices(mock_notify) -> None:
    from bokeh.document.events import ColumnsPatchedEvent
    source = ColumnDataSource(data=dict(foo=[10, 20, 30, 40, 50]))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    mock_notify.reset_mock()
    pvcd._patch('doc', source, dict(foo=[(slice(2), [1, 2])]), setter='setter')
    assert mock_notify.call_count == 1
    assert mock_notify.call_args[0] == ({'foo': [1, 2, 30, 40, 50]},)
    assert pvcd == dict(foo=[1, 2, 30, 40, 50])
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnsPatchedEvent)
    assert mock_notify.call_args[1]['hint'].setter == 'setter'

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueColumnData__patch_with_overlapping_slice_indices(mock_notify) -> None:
    from bokeh.document.events import ColumnsPatchedEvent
    source = ColumnDataSource(data=dict(foo=[10, 20, 30, 40, 50]))
    pvcd = bcpw.PropertyValueColumnData(source.data)
    mock_notify.reset_mock()
    pvcd._patch('doc', source, dict(foo=[(slice(2), [1, 2]), (slice(1, 3), [1000, 2000])]), setter='setter')
    assert mock_notify.call_count == 1
    assert mock_notify.call_args[0] == ({'foo': [1, 1000, 2000, 40, 50]},)
    assert pvcd == dict(foo=[1, 1000, 2000, 40, 50])
    assert 'hint' in mock_notify.call_args[1]
    assert isinstance(mock_notify.call_args[1]['hint'], ColumnsPatchedEvent)
    assert mock_notify.call_args[1]['hint'].setter == 'setter'

@patch('bokeh.core.property.wrappers.PropertyValueContainer._notify_owners')
def test_PropertyValueList_mutators(mock_notify) -> None:
    pvl = bcpw.PropertyValueList([10, 20, 30, 40, 50])
    mock_notify.reset_mock()
    del pvl[2]
    assert mock_notify.called
    mock_notify.reset_mock()
    del pvl[1:2]
    assert mock_notify.called
    mock_notify.reset_mock()
    pvl += [888]
    assert mock_notify.called
    mock_notify.reset_mock()
    pvl *= 2
    assert mock_notify.called
    mock_notify.reset_mock()
    pvl[0] = 2
    assert mock_notify.called
    mock_notify.reset_mock()
    pvl[3:1:-1] = [21, 31]
    assert mock_notify.called
    mock_notify.reset_mock()
    pvl.append(999)
    assert mock_notify.called
    mock_notify.reset_mock()
    pvl.extend([1000])
    assert mock_notify.called
    mock_notify.reset_mock()
    pvl.insert(0, 100)
    assert mock_notify.called
    mock_notify.reset_mock()
    pvl.pop()
    assert mock_notify.called
    mock_notify.reset_mock()
    pvl.remove(100)
    assert mock_notify.called
    mock_notify.reset_mock()
    pvl.reverse()
    assert mock_notify.called
    mock_notify.reset_mock()
    pvl.sort()
    assert mock_notify.called
    try:
        pvl.__setslice__(1, 2, 3)
    except:
        pass
    try:
        pvl.__delslice__(1, 2)
    except:
        pass

def test_PropertyValueColumnData___copy__() -> None:
    source = ColumnDataSource(data=dict(foo=[10]))
    pvcd = source.data.__copy__()
    assert source.data == pvcd
    assert id(source.data) != id(pvcd)
    pvcd['foo'][0] = 20
    assert source.data['foo'][0] == 20

def test_PropertyValueColumnData___deepcopy__() -> None:
    source = ColumnDataSource(data=dict(foo=[10]))
    pvcd = source.data.__deepcopy__()
    assert source.data == pvcd
    assert id(source.data) != id(pvcd)
    pvcd['foo'][0] = 20
    assert source.data['foo'][0] == 10

def test_Property_wrap() -> None:
    for x in (Bool, Int, Float, Complex, String, Enum, Color, Regex, Seq, Tuple, Instance, Any, Interval, Either, DashPattern, Size, Percent, Angle, MinMaxBounds):
        for y in (0, 1, 2.3, 'foo', None, (), [], {}):
            r = x.wrap(y)
            assert r == y
            assert isinstance(r, type(y))

def test_List_wrap() -> None:
    for y in (0, 1, 2.3, 'foo', None, (), {}):
        r = List.wrap(y)
        assert r == y
        assert isinstance(r, type(y))
    r = List.wrap([1, 2, 3])
    assert r == [1, 2, 3]
    assert isinstance(r, bcpw.PropertyValueList)
    r2 = List.wrap(r)
    assert r is r2

def test_Dict_wrap() -> None:
    for y in (0, 1, 2.3, 'foo', None, (), []):
        r = Dict.wrap(y)
        assert r == y
        assert isinstance(r, type(y))
    r = Dict.wrap(dict(a=1, b=2))
    assert r == dict(a=1, b=2)
    assert isinstance(r, bcpw.PropertyValueDict)
    r2 = Dict.wrap(r)
    assert r is r2

def test_ColumnData_wrap() -> None:
    for y in (0, 1, 2.3, 'foo', None, (), []):
        r = ColumnData.wrap(y)
        assert r == y
        assert isinstance(r, type(y))
    r = ColumnData.wrap(dict(a=1, b=2))
    assert r == dict(a=1, b=2)
    assert isinstance(r, bcpw.PropertyValueColumnData)
    r2 = ColumnData.wrap(r)
    assert r is r2
Test___all__ = verify_all(bcpw, ALL)