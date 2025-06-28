import pytest
pytest
from mock import patch
from bokeh._testing.util.api import verify_all
from bokeh.core.properties import Int, List
from bokeh.model import Model
import bokeh.core.property.descriptors as bcpd
ALL = ('BasicPropertyDescriptor', 'ColumnDataPropertyDescriptor', 'DataSpecPropertyDescriptor', 'PropertyDescriptor', 'UnitsSpecPropertyDescriptor')
Test___all__ = verify_all(bcpd, ALL)

def Test_PropertyDescriptor_test___init__(self) -> None:
    d = bcpd.PropertyDescriptor('foo')
    assert d.name == 'foo'

def Test_PropertyDescriptor_test___str__(self) -> None:
    d = bcpd.PropertyDescriptor('foo')
    assert str(d) == 'PropertyDescriptor(foo)'

def Test_PropertyDescriptor_test_abstract(self) -> None:
    d = bcpd.PropertyDescriptor('foo')

    class Foo:
        pass
    f = Foo()
    with pytest.raises(NotImplementedError):
        d.__get__(f, f.__class__)
    with pytest.raises(NotImplementedError):
        d.__set__(f, 11)
    with pytest.raises(NotImplementedError):
        d.__delete__(f)
    with pytest.raises(NotImplementedError):
        d.class_default(f)
    with pytest.raises(NotImplementedError):
        d.serialized
    with pytest.raises(NotImplementedError):
        d.readonly
    with pytest.raises(NotImplementedError):
        d.has_ref
    with pytest.raises(NotImplementedError):
        d.trigger_if_changed(f, 11)
    with pytest.raises(NotImplementedError):
        d._internal_set(f, 11)

@patch('bokeh.core.property.descriptors.PropertyDescriptor._internal_set')
def Test_PropertyDescriptor_test_set_from_json(self, mock_iset) -> None:

    class Foo:
        pass
    f = Foo()
    d = bcpd.PropertyDescriptor('foo')
    d.set_from_json(f, 'bar', 10)
    assert mock_iset.called_once_with((f, 'bar', 10), {})

def Test_PropertyDescriptor_test_erializable_value(self) -> None:
    result = {}

    class Foo:

        def serialize_value(self, val):
            result['foo'] = val
    f = Foo()
    f.foo = 10
    d = bcpd.PropertyDescriptor('foo')
    d.property = Foo()
    d.__get__ = lambda obj, owner: f.foo
    d.serializable_value(f)
    assert result['foo'] == 10

def Test_PropertyDescriptor_test_add_prop_descriptor_to_class_dupe_name(self) -> None:
    d = bcpd.PropertyDescriptor('foo')
    new_class_attrs = {'foo': 10}
    with pytest.raises(RuntimeError) as e:
        d.add_prop_descriptor_to_class('bar', new_class_attrs, [], [], {})
    assert str(e.value).endswith('Two property generators both created bar.foo')

def Test_BasicPropertyDescriptor_test___init__(self) -> None:

    class Foo:
        """doc"""
        pass
    f = Foo()
    d = bcpd.BasicPropertyDescriptor('foo', f)
    assert d.name == 'foo'
    assert d.property == f
    assert d.__doc__ == f.__doc__

def Test_BasicPropertyDescriptor_test___str__(self) -> None:

    class Foo:
        pass
    f = Foo()
    d = bcpd.BasicPropertyDescriptor('foo', f)
    assert str(d) == str(f)

def Test_BasicPropertyDescriptor_test___get__improper(self) -> None:

    class Foo:
        pass
    f = Foo()
    d = bcpd.BasicPropertyDescriptor('foo', f)
    with pytest.raises(ValueError) as e:
        d.__get__(None, None)
    assert str(e.value).endswith("both 'obj' and 'owner' are None, don't know what to do")

def Test_BasicPropertyDescriptor_test___set__improper(self) -> None:

    class Foo:
        pass
    f = Foo()
    d = bcpd.BasicPropertyDescriptor('foo', f)
    with pytest.raises(RuntimeError) as e:
        d.__set__('junk', None)
    assert str(e.value).endswith("Cannot set a property value 'foo' on a str instance before HasProps.__init__")

def Test_BasicPropertyDescriptor_test___delete__(self) -> None:

    class Foo(Model):
        foo = Int()
        bar = List(Int, default=[10])
        baz = Int(default=20)
        quux = List(Int, default=[30])
    f = Foo()
    f.foo
    f.bar
    f.baz
    f.quux
    calls = []

    def cb(attr, old, new):
        calls.append(attr)
    for name in ['foo', 'bar', 'baz', 'quux']:
        f.on_change(name, cb)
    assert f._property_values == {}
    assert f._unstable_default_values == dict(bar=[10], quux=[30])
    del f.foo
    assert f._property_values == {}
    assert f._unstable_default_values == dict(bar=[10], quux=[30])
    assert calls == []
    f.baz = 50
    assert f.baz == 50
    assert f._unstable_default_values == dict(bar=[10], quux=[30])
    assert calls == ['baz']
    del f.baz
    assert f.baz == 20
    assert f._unstable_default_values == dict(bar=[10], quux=[30])
    assert calls == ['baz', 'baz']
    del f.bar
    assert f._property_values == {}
    assert f._unstable_default_values == dict(quux=[30])
    assert calls == ['baz', 'baz']
    f.bar = [60]
    assert f.bar == [60]
    assert f._unstable_default_values == dict(quux=[30])
    assert calls == ['baz', 'baz', 'bar']
    del f.bar
    assert f.bar == [10]
    assert f._unstable_default_values == dict(bar=[10], quux=[30])
    assert calls == ['baz', 'baz', 'bar', 'bar']
    del f.quux
    assert f._unstable_default_values == dict(bar=[10])
    assert calls == ['baz', 'baz', 'bar', 'bar']

def Test_BasicPropertyDescriptor_test_class_default(self) -> None:
    result = {}

    class Foo:

        def themed_default(*args, **kw):
            result['called'] = True
    f = Foo()
    f.readonly = 'stuff'
    d = bcpd.BasicPropertyDescriptor('foo', f)
    d.class_default(d)
    assert result['called']

def Test_BasicPropertyDescriptor_test_serialized(self) -> None:

    class Foo:
        pass
    f = Foo()
    f.serialized = 'stuff'
    d = bcpd.BasicPropertyDescriptor('foo', f)
    assert d.serialized == 'stuff'

def Test_BasicPropertyDescriptor_test_readonly(self) -> None:

    class Foo:
        pass
    f = Foo()
    f.readonly = 'stuff'
    d = bcpd.BasicPropertyDescriptor('foo', f)
    assert d.readonly == 'stuff'

def Test_BasicPropertyDescriptor_test_has_ref(self) -> None:

    class Foo:
        pass
    f = Foo()
    f.has_ref = 'stuff'
    d = bcpd.BasicPropertyDescriptor('foo', f)
    assert d.has_ref == 'stuff'

@patch('bokeh.core.property.descriptors.BasicPropertyDescriptor._trigger')
def Test_BasicPropertyDescriptor_test__trigger(self, mock_trigger) -> None:

    class Foo:
        _property_values = dict(foo=10, bar=20)

    class Match:

        def matches(*args, **kw):
            return True

    class NoMatch:

        def matches(*args, **kw):
            return False
    m = Match()
    nm = NoMatch()
    d1 = bcpd.BasicPropertyDescriptor('foo', m)
    d2 = bcpd.BasicPropertyDescriptor('bar', nm)
    d1.trigger_if_changed(Foo, 'junk')
    assert not mock_trigger.called
    d2.trigger_if_changed(Foo, 'junk')
    assert mock_trigger.called

def Test_UnitSpecDescriptor_test___init__(self) -> None:

    class Foo:
        """doc"""
        pass
    f = Foo()
    g = Foo()
    d = bcpd.UnitsSpecPropertyDescriptor('foo', f, g)
    assert d.name == 'foo'
    assert d.property == f
    assert d.__doc__ == f.__doc__
    assert d.units_prop == g