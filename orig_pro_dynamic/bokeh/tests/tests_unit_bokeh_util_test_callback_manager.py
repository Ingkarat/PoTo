import pytest
pytest
from functools import partial
from bokeh.document import Document
import bokeh.util.callback_manager as cbm

def _good_property(x, y, z):
    pass

def _bad_property(x, y):
    pass

def _partially_good_property(w, x, y, z):
    pass

def _just_fine_property(w, x, y, z='default'):
    pass

def _good_event(event):
    pass

def _bad_event(x, y, z):
    pass

def _partially_good_event(arg, event):
    pass

def _partially_bad_event(event):
    pass

def _GoodPropertyCallback___init__(self):
    self.last_name = None
    self.last_old = None
    self.last_new = None

def _GoodPropertyCallback___call__(self, name, old, new):
    self.method(name, old, new)

def _GoodPropertyCallback_method(self, name, old, new):
    self.last_name = name
    self.last_old = old
    self.last_new = new

def _GoodPropertyCallback_partially_good(self, name, old, new, newer):
    pass

def _GoodPropertyCallback_just_fine(self, name, old, new, extra='default'):
    pass

def _BadPropertyCallback___call__(self, x, y):
    pass

def _BadPropertyCallback_method(self, x, y):
    pass

def _GoodEventCallback___init__(self):
    self.last_name = None
    self.last_old = None
    self.last_new = None

def _GoodEventCallback___call__(self, event):
    self.method(event)

def _GoodEventCallback_method(self, event):
    self.event = event

def _GoodEventCallback_partially_good(self, arg, event):
    pass

def _BadEventCallback___call__(self):
    pass

def _BadEventCallback_method(self):
    pass

def TestPropertyCallbackManager_test_creation(self) -> None:
    m = cbm.PropertyCallbackManager()
    assert len(m._callbacks) == 0

def TestPropertyCallbackManager_test_on_change_good_method(self) -> None:
    m = cbm.PropertyCallbackManager()
    good = _GoodPropertyCallback()
    m.on_change('foo', good.method)
    assert len(m._callbacks) == 1
    assert m._callbacks['foo'] == [good.method]

def TestPropertyCallbackManager_test_on_change_good_partial_function(self) -> None:
    m = cbm.PropertyCallbackManager()
    p = partial(_partially_good_property, 'foo')
    m.on_change('bar', p)
    assert len(m._callbacks) == 1

def TestPropertyCallbackManager_test_on_change_good_partial_method(self) -> None:
    m = cbm.PropertyCallbackManager()
    good = _GoodPropertyCallback()
    p = partial(good.partially_good, 'foo')
    m.on_change('bar', p)
    assert len(m._callbacks) == 1

def TestPropertyCallbackManager_test_on_change_good_extra_kwargs_function(self) -> None:
    m = cbm.PropertyCallbackManager()
    m.on_change('bar', _just_fine_property)
    assert len(m._callbacks) == 1

def TestPropertyCallbackManager_test_on_change_good_extra_kwargs_method(self) -> None:
    m = cbm.PropertyCallbackManager()
    good = _GoodPropertyCallback()
    m.on_change('bar', good.just_fine)
    assert len(m._callbacks) == 1

def TestPropertyCallbackManager_test_on_change_good_functor(self) -> None:
    m = cbm.PropertyCallbackManager()
    good = _GoodPropertyCallback()
    m.on_change('foo', good)
    assert len(m._callbacks) == 1
    assert m._callbacks['foo'] == [good]

def TestPropertyCallbackManager_test_on_change_good_function(self) -> None:
    m = cbm.PropertyCallbackManager()
    m.on_change('foo', _good_property)
    assert len(m._callbacks) == 1
    assert m._callbacks['foo'] == [_good_property]

def TestPropertyCallbackManager_test_on_change_good_lambda(self) -> None:
    m = cbm.PropertyCallbackManager()
    good = lambda x, y, z: x
    m.on_change('foo', good)
    assert len(m._callbacks) == 1
    assert m._callbacks['foo'] == [good]

def TestPropertyCallbackManager_test_on_change_good_closure(self) -> None:

    def good(x, y, z):
        pass
    m = cbm.PropertyCallbackManager()
    m.on_change('foo', good)
    assert len(m._callbacks) == 1
    assert len(m._callbacks['foo']) == 1

def TestPropertyCallbackManager_test_on_change_bad_method(self) -> None:
    m = cbm.PropertyCallbackManager()
    bad = _BadPropertyCallback()
    with pytest.raises(ValueError):
        m.on_change('foo', bad.method)
    assert len(m._callbacks) == 1
    assert len(m._callbacks['foo']) == 0

def TestPropertyCallbackManager_test_on_change_bad_functor(self) -> None:
    m = cbm.PropertyCallbackManager()
    bad = _BadPropertyCallback()
    with pytest.raises(ValueError):
        m.on_change('foo', bad)
    assert len(m._callbacks) == 1
    assert len(m._callbacks['foo']) == 0

def TestPropertyCallbackManager_test_on_change_bad_function(self) -> None:
    m = cbm.PropertyCallbackManager()
    with pytest.raises(ValueError):
        m.on_change('foo', _bad_property)
    assert len(m._callbacks) == 1
    assert len(m._callbacks['foo']) == 0

def TestPropertyCallbackManager_test_on_change_bad_lambda(self) -> None:
    m = cbm.PropertyCallbackManager()
    with pytest.raises(ValueError):
        m.on_change('foo', lambda x, y: x)
    assert len(m._callbacks) == 1
    assert len(m._callbacks['foo']) == 0

def TestPropertyCallbackManager_test_on_change_bad_closure(self) -> None:

    def bad(x, y):
        pass
    m = cbm.PropertyCallbackManager()
    with pytest.raises(ValueError):
        m.on_change('foo', bad)
    assert len(m._callbacks) == 1
    assert len(m._callbacks['foo']) == 0

def TestPropertyCallbackManager_test_on_change_same_attr_twice_multiple_calls(self) -> None:

    def good1(x, y, z):
        pass

    def good2(x, y, z):
        pass
    m1 = cbm.PropertyCallbackManager()
    m1.on_change('foo', good1)
    m1.on_change('foo', good2)
    assert len(m1._callbacks) == 1
    assert m1._callbacks['foo'] == [good1, good2]

def TestPropertyCallbackManager_test_on_change_same_attr_twice_one_call(self) -> None:

    def good1(x, y, z):
        pass

    def good2(x, y, z):
        pass
    m2 = cbm.PropertyCallbackManager()
    m2.on_change('foo', good1, good2)
    assert len(m2._callbacks) == 1
    assert m2._callbacks['foo'] == [good1, good2]

def TestPropertyCallbackManager_test_on_change_different_attrs(self) -> None:

    def good1(x, y, z):
        pass

    def good2(x, y, z):
        pass
    m1 = cbm.PropertyCallbackManager()
    m1.on_change('foo', good1)
    m1.on_change('bar', good2)
    assert len(m1._callbacks) == 2
    assert m1._callbacks['foo'] == [good1]
    assert m1._callbacks['bar'] == [good2]

def TestPropertyCallbackManager_test_trigger(self) -> None:
    m = cbm.PropertyCallbackManager()
    good = _GoodPropertyCallback()
    m.on_change('foo', good.method)
    m.trigger('foo', 42, 43)
    assert good.last_name == 'foo'
    assert good.last_old == 42
    assert good.last_new == 43

def TestPropertyCallbackManager_test_trigger_with_two_callbacks(self) -> None:
    m = cbm.PropertyCallbackManager()
    good1 = _GoodPropertyCallback()
    good2 = _GoodPropertyCallback()
    m.on_change('foo', good1.method)
    m.on_change('foo', good2.method)
    m.trigger('foo', 42, 43)
    assert good1.last_name == 'foo'
    assert good1.last_old == 42
    assert good1.last_new == 43
    assert good2.last_name == 'foo'
    assert good2.last_old == 42
    assert good2.last_new == 43

def TestEventCallbackManager_test_creation(self) -> None:
    m = cbm.EventCallbackManager()
    assert len(m._event_callbacks) == 0

def TestEventCallbackManager_test_on_change_good_method(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    good = _GoodEventCallback()
    m.on_event('foo', good.method)
    assert len(m._event_callbacks) == 1
    assert m._event_callbacks['foo'] == [good.method]

def TestEventCallbackManager_test_on_change_good_partial_function(self) -> None:
    m = cbm.EventCallbackManager()
    p = partial(_partially_good_event, 'foo')
    m.subscribed_events = []
    m.on_event('foo', p)
    assert len(m._event_callbacks) == 1
    assert m._event_callbacks['foo'] == [p]

def TestEventCallbackManager_test_on_change_bad_partial_function(self) -> None:
    m = cbm.EventCallbackManager()
    p = partial(_partially_bad_event, 'foo')
    m.subscribed_events = []
    m.on_event('foo', p)
    assert len(m._event_callbacks) == 1

def TestEventCallbackManager_test_on_change_good_partial_method(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    good = _GoodEventCallback()
    p = partial(good.partially_good, 'foo')
    m.on_event('foo', p)
    assert len(m._event_callbacks) == 1

def TestEventCallbackManager_test_on_change_good_functor(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    good = _GoodEventCallback()
    m.on_event('foo', good)
    assert len(m._event_callbacks) == 1
    assert m._event_callbacks['foo'] == [good]

def TestEventCallbackManager_test_on_change_good_function(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    m.on_event('foo', _good_event)
    assert len(m._event_callbacks) == 1
    assert m._event_callbacks['foo'] == [_good_event]

def TestEventCallbackManager_test_on_change_unicode_event_name(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    m.on_event('foo', _good_event)
    assert len(m._event_callbacks) == 1
    assert m._event_callbacks['foo'] == [_good_event]

def TestEventCallbackManager_test_on_change_good_lambda(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    good = lambda event: event
    m.on_event('foo', good)
    assert len(m._event_callbacks) == 1
    assert m._event_callbacks['foo'] == [good]

def TestEventCallbackManager_test_on_change_good_closure(self) -> None:

    def good(event):
        pass
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    m.on_event('foo', good)
    assert len(m._event_callbacks) == 1
    assert len(m._event_callbacks['foo']) == 1

def TestEventCallbackManager_test_on_change_bad_method(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    bad = _BadEventCallback()
    m.on_event('foo', bad.method)
    assert len(m._event_callbacks) == 1

def TestEventCallbackManager_test_on_change_bad_functor(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    bad = _BadEventCallback()
    m.on_event('foo', bad)
    assert len(m._event_callbacks) == 1

def TestEventCallbackManager_test_on_change_bad_function(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    with pytest.raises(ValueError):
        m.on_event('foo', _bad_event)
    assert len(m._event_callbacks) == 0

def TestEventCallbackManager_test_on_change_bad_lambda(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    with pytest.raises(ValueError):
        m.on_event('foo', lambda x, y: x)
    assert len(m._event_callbacks) == 0

def TestEventCallbackManager_test_on_change_bad_closure(self) -> None:

    def bad(event, y):
        pass
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    with pytest.raises(ValueError):
        m.on_event('foo', bad)
    assert len(m._event_callbacks) == 0

def TestEventCallbackManager_test_on_change_with_two_callbacks(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    good1 = _GoodEventCallback()
    good2 = _GoodEventCallback()
    m.on_event('foo', good1.method)
    m.on_event('foo', good2.method)

def TestEventCallbackManager_test_on_change_with_two_callbacks_one_bad(self) -> None:
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    good = _GoodEventCallback()
    bad = _BadEventCallback()
    m.on_event('foo', good.method, bad.method)
    assert len(m._event_callbacks) == 1

def TestEventCallbackManager_test__trigger_event_wraps_curdoc(self) -> None:
    from bokeh.io.doc import set_curdoc
    from bokeh.io import curdoc
    oldcd = curdoc()
    d1 = Document()
    d2 = Document()
    set_curdoc(d1)
    out = {}

    def cb():
        out['curdoc'] = curdoc()
    m = cbm.EventCallbackManager()
    m.subscribed_events = []
    m.on_event('foo', cb)
    m.id = 10
    m._document = d2
    assert len(m._event_callbacks) == 1
    assert m._event_callbacks['foo'] == [cb]

    class ev:
        _model_id = 10
        event_name = 'foo'
    m._trigger_event(ev())
    assert out['curdoc'] is d2
    set_curdoc(oldcd)