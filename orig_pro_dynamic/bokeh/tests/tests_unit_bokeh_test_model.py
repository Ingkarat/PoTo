import pytest
pytest
from bokeh.core.properties import Int, List, String
from bokeh.models import *
from bokeh.models import CustomJS
from bokeh.plotting import *
from bokeh.document import document
from bokeh.model import Model

def test_all_builtin_models_default_constructible() -> None:
    bad = []
    for (name, cls) in Model.model_class_reverse_map.items():
        try:
            cls()
        except Exception:
            bad.append(name)
        assert bad == []

def test_select() -> None:
    d = document.Document()
    root1 = SomeModel(a=42, name='a')
    root2 = SomeModel(a=43, name='c')
    root3 = SomeModel(a=44, name='d')
    root4 = SomeModel(a=45, name='d')
    d.add_root(root1)
    d.add_root(root2)
    d.add_root(root3)
    d.add_root(root4)
    assert {root1} == set(root1.select(dict(a=42)))
    assert {root1} == set(root1.select(dict(name='a')))
    assert {root2} == set(root2.select(dict(name='c')))
    assert set() == set(root1.select(dict(name='nope')))
    assert set() == set(root3.select(dict(name='a')))
    assert {root3} == set(root3.select(dict(a=44)))
    assert root3 == root3.select_one(dict(name='d'))
    assert None == root1.select_one(dict(name='nope'))
    with pytest.raises(ValueError) as e:
        d.select_one(dict(name='d'))
    assert 'Found more than one' in repr(e)
    assert None == root3.select_one(dict(name='a'))
    assert None == root3.select_one(dict(name='c'))
    root1.set_select(dict(a=42), dict(name='c', a=44))
    assert {root1} == set(root1.select(dict(name='c')))
    assert {root1} == set(root1.select(dict(a=44)))
    root3.set_select(dict(name='d'), dict(a=57))
    assert {root3} == set(root3.select(dict(a=57)))
    root2.set_select(SomeModel, dict(name='new_name'))
    assert {root2} == set(root2.select(dict(name='new_name')))

def Test_js_on_change_test_exception_for_no_callbacks(self) -> None:
    m = SomeModel()
    with pytest.raises(ValueError):
        m.js_on_change('foo')

def Test_js_on_change_test_exception_for_bad_callbacks(self) -> None:
    m = SomeModel()
    for val in [10, 'bar', None, [1], {}, 10.2]:
        with pytest.raises(ValueError):
            m.js_on_change('foo', val)

def Test_js_on_change_test_with_propname(self) -> None:
    cb = CustomJS(code='')
    m0 = SomeModel()
    for name in m0.properties(self):
        m = SomeModel()
        m.js_on_change(name, cb)
        assert m.js_property_callbacks == {'change:%s' % name: [cb]}

def Test_js_on_change_test_with_non_propname(self) -> None:
    cb = CustomJS(code='')
    m1 = SomeModel()
    m1.js_on_change('foo', cb)
    assert m1.js_property_callbacks == {'foo': [cb]}
    m2 = SomeModel()
    m2.js_on_change('change:b', cb)
    assert m2.js_property_callbacks == {'change:b': [cb]}

def Test_js_on_change_test_with_multple_callbacks(self) -> None:
    cb1 = CustomJS(code='')
    cb2 = CustomJS(code='')
    m = SomeModel()
    m.js_on_change('foo', cb1, cb2)
    assert m.js_property_callbacks == {'foo': [cb1, cb2]}

def Test_js_on_change_test_with_multple_callbacks_separately(self) -> None:
    cb1 = CustomJS(code='')
    cb2 = CustomJS(code='')
    m = SomeModel()
    m.js_on_change('foo', cb1)
    assert m.js_property_callbacks == {'foo': [cb1]}
    m.js_on_change('foo', cb2)
    assert m.js_property_callbacks == {'foo': [cb1, cb2]}

def Test_js_on_change_test_ignores_dupe_callbacks(self) -> None:
    cb = CustomJS(code='')
    m = SomeModel()
    m.js_on_change('foo', cb, cb)
    assert m.js_property_callbacks == {'foo': [cb]}

def Test_js_link_test_value_error_on_bad_attr(self) -> None:
    m1 = SomeModel()
    m2 = SomeModel()
    with pytest.raises(ValueError) as e:
        m1.js_link('junk', m2, 'b')
    assert str(e.value).endswith('%r is not a property of self (%r)' % ('junk', m1))

def Test_js_link_test_value_error_on_bad_other(self) -> None:
    m1 = SomeModel()
    with pytest.raises(ValueError) as e:
        m1.js_link('a', 'junk', 'b')
    assert str(e.value).endswith("'other' is not a Bokeh model: %r" % 'junk')

def Test_js_link_test_value_error_on_bad_other_attr(self) -> None:
    m1 = SomeModel()
    m2 = SomeModel()
    with pytest.raises(ValueError) as e:
        m1.js_link('a', m2, 'junk')
    assert str(e.value).endswith('%r is not a property of other (%r)' % ('junk', m2))

def Test_js_link_test_creates_customjs(self) -> None:
    m1 = SomeModel()
    m2 = SomeModel()
    assert len(m1.js_property_callbacks) == 0
    m1.js_link('a', m2, 'b')
    assert len(m1.js_property_callbacks) == 1
    assert 'change:a' in m1.js_property_callbacks
    cbs = m1.js_property_callbacks['change:a']
    assert len(cbs) == 1
    cb = cbs[0]
    assert isinstance(cb, CustomJS)
    assert cb.args == dict(other=m2)
    assert cb.code == 'other.b = this.a'

def Test_js_link_test_attr_selector_creates_customjs_int(self) -> None:
    m1 = SomeModel()
    m2 = SomeModel()
    assert len(m1.js_property_callbacks) == 0
    m1.js_link('a', m2, 'b', 1)
    assert len(m1.js_property_callbacks) == 1
    assert 'change:a' in m1.js_property_callbacks
    cbs = m1.js_property_callbacks['change:a']
    assert len(cbs) == 1
    cb = cbs[0]
    assert isinstance(cb, CustomJS)
    assert cb.args == dict(other=m2)
    assert cb.code == 'other.b = this.a[1]'

def Test_js_link_test_attr_selector_creates_customjs_with_zero(self) -> None:
    m1 = SomeModel()
    m2 = SomeModel()
    assert len(m1.js_property_callbacks) == 0
    m1.js_link('a', m2, 'b', 0)
    assert len(m1.js_property_callbacks) == 1
    assert 'change:a' in m1.js_property_callbacks
    cbs = m1.js_property_callbacks['change:a']
    assert len(cbs) == 1
    cb = cbs[0]
    assert isinstance(cb, CustomJS)
    assert cb.args == dict(other=m2)
    assert cb.code == 'other.b = this.a[0]'

def Test_js_link_test_attr_selector_creates_customjs_str(self) -> None:
    m1 = SomeModel()
    m2 = SomeModel()
    assert len(m1.js_property_callbacks) == 0
    m1.js_link('a', m2, 'b', 'test')
    assert len(m1.js_property_callbacks) == 1
    assert 'change:a' in m1.js_property_callbacks
    cbs = m1.js_property_callbacks['change:a']
    assert len(cbs) == 1
    cb = cbs[0]
    assert isinstance(cb, CustomJS)
    assert cb.args == dict(other=m2)
    assert cb.code == "other.b = this.a['test']"