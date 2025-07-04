import pytest
pytest
import logging
from copy import copy
from mock import patch
from _util_document import AnotherModelInTestDocument, ModelThatOverridesName, ModelWithSpecInTestDocument, SomeModelInTestDocument
from bokeh.document.events import ColumnsPatchedEvent, ColumnsStreamedEvent, ModelChangedEvent, RootAddedEvent, RootRemovedEvent, SessionCallbackAdded, SessionCallbackRemoved, TitleChangedEvent
from bokeh.io.doc import curdoc
from bokeh.models import ColumnDataSource
from bokeh.protocol.messages.patch_doc import process_document_events
from bokeh.util.logconfig import basicConfig
import bokeh.document.document as document
extra = []
basicConfig()

@pytest.mark.parametrize('policy', document.HoldPolicy)
def TestDocumentHold_test_hold(self, policy) -> None:
    policy = document.HoldPolicy[0]
    d = document.Document()
    assert d._hold == None
    assert d._held_events == []
    d.hold(policy)
    assert d._hold == policy

def TestDocumentHold_test_hold_bad_policy(self) -> None:
    d = document.Document()
    with pytest.raises(ValueError):
        d.hold('junk')

@pytest.mark.parametrize('first,second', [('combine', 'collect'), ('collect', 'combine')])
def TestDocumentHold_test_rehold(self, first, second, caplog) -> None:
    (first, second) = ('combine', 'collect')
    d = document.Document()
    with caplog.at_level(logging.WARN):
        d.hold(first)
        assert caplog.text == ''
        assert len(caplog.records) == 0
        d.hold(first)
        assert caplog.text == ''
        assert len(caplog.records) == 0
        d.hold(second)
        assert caplog.text.strip().endswith("hold already active with '%s', ignoring '%s'" % (first, second))
        assert len(caplog.records) == 1
        d.unhold()
        d.hold(second)
        assert len(caplog.records) == 1

@pytest.mark.parametrize('policy', document.HoldPolicy)
def TestDocumentHold_test_unhold(self, policy) -> None:
    policy = document.HoldPolicy[0]
    d = document.Document()
    assert d._hold == None
    assert d._held_events == []
    d.hold(policy)
    assert d._hold == policy
    d.unhold()
    assert d._hold == None

@patch('bokeh.document.document.Document._trigger_on_change')
def TestDocumentHold_test_unhold_triggers_events(self, mock_trigger) -> None:
    d = document.Document()
    d.hold('collect')
    d._held_events = [1, 2, 3]
    d.unhold()
    assert mock_trigger.call_count == 3
    assert mock_trigger.call_args[0] == (3,)
    assert mock_trigger.call_args[1] == {}

def Test_Document_delete_modules_test_basic(self) -> None:
    d = document.Document()
    assert not d.roots

    class FakeMod:
        __name__ = 'junkjunkjunk'
    mod = FakeMod()
    import sys
    assert 'junkjunkjunk' not in sys.modules
    sys.modules['junkjunkjunk'] = mod
    d._modules.append(mod)
    assert 'junkjunkjunk' in sys.modules
    d.delete_modules()
    assert 'junkjunkjunk' not in sys.modules
    assert d._modules is None

def Test_Document_delete_modules_test_extra_referrer_error(self, caplog) -> None:
    d = document.Document()
    assert not d.roots

    class FakeMod:
        __name__ = 'junkjunkjunk'
    mod = FakeMod()
    import sys
    assert 'junkjunkjunk' not in sys.modules
    sys.modules['junkjunkjunk'] = mod
    d._modules.append(mod)
    assert 'junkjunkjunk' in sys.modules
    extra.append(mod)
    import gc
    assert len(gc.get_referrers(mod)) in (3, 4)
    with caplog.at_level(logging.ERROR):
        d.delete_modules()
        assert 'Module %r has extra unexpected referrers! This could indicate a serious memory leak. Extra referrers:' % mod in caplog.text
        assert len(caplog.records) == 1
    assert 'junkjunkjunk' not in sys.modules
    assert d._modules is None

def TestDocument_test_empty(self) -> None:
    d = document.Document()
    assert not d.roots

def TestDocument_test_default_template_vars(self) -> None:
    d = document.Document()
    assert not d.roots
    assert d.template_variables == {}

def TestDocument_test_add_roots(self) -> None:
    d = document.Document()
    assert not d.roots
    d.add_root(AnotherModelInTestDocument())
    assert len(d.roots) == 1
    assert next(iter(d.roots)).document == d

def TestDocument_test_roots_preserves_insertion_order(self) -> None:
    d = document.Document()
    assert not d.roots
    roots = [AnotherModelInTestDocument(), AnotherModelInTestDocument(), AnotherModelInTestDocument()]
    for r in roots:
        d.add_root(r)
    assert len(d.roots) == 3
    assert type(d.roots) is list
    roots_iter = iter(d.roots)
    assert next(roots_iter) is roots[0]
    assert next(roots_iter) is roots[1]
    assert next(roots_iter) is roots[2]

def TestDocument_test_set_title(self) -> None:
    d = document.Document()
    assert d.title == document.DEFAULT_TITLE
    d.title = 'Foo'
    assert d.title == 'Foo'

def TestDocument_test_all_models(self) -> None:
    d = document.Document()
    assert not d.roots
    assert len(d._all_models) == 0
    m = SomeModelInTestDocument()
    m2 = AnotherModelInTestDocument()
    m.child = m2
    d.add_root(m)
    assert len(d.roots) == 1
    assert len(d._all_models) == 2
    m.child = None
    assert len(d._all_models) == 1
    m.child = m2
    assert len(d._all_models) == 2
    d.remove_root(m)
    assert len(d._all_models) == 0

def TestDocument_test_get_model_by_id(self) -> None:
    d = document.Document()
    assert not d.roots
    assert len(d._all_models) == 0
    m = SomeModelInTestDocument()
    m2 = AnotherModelInTestDocument()
    m.child = m2
    d.add_root(m)
    assert len(d.roots) == 1
    assert len(d._all_models) == 2
    assert d.get_model_by_id(m.id) == m
    assert d.get_model_by_id(m2.id) == m2
    assert d.get_model_by_id('not a valid ID') is None

def TestDocument_test_get_model_by_name(self) -> None:
    d = document.Document()
    assert not d.roots
    assert len(d._all_models) == 0
    m = SomeModelInTestDocument(name='foo')
    m2 = AnotherModelInTestDocument(name='bar')
    m.child = m2
    d.add_root(m)
    assert len(d.roots) == 1
    assert len(d._all_models) == 2
    assert len(d._all_models_by_name._dict) == 2
    assert d.get_model_by_name(m.name) == m
    assert d.get_model_by_name(m2.name) == m2
    assert d.get_model_by_name('not a valid name') is None

def TestDocument_test_get_model_by_changed_name(self) -> None:
    d = document.Document()
    m = SomeModelInTestDocument(name='foo')
    d.add_root(m)
    assert d.get_model_by_name('foo') == m
    m.name = 'bar'
    assert d.get_model_by_name('foo') == None
    assert d.get_model_by_name('bar') == m

def TestDocument_test_get_model_by_changed_from_none_name(self) -> None:
    d = document.Document()
    m = SomeModelInTestDocument(name=None)
    d.add_root(m)
    assert d.get_model_by_name('bar') == None
    m.name = 'bar'
    assert d.get_model_by_name('bar') == m

def TestDocument_test_get_model_by_changed_to_none_name(self) -> None:
    d = document.Document()
    m = SomeModelInTestDocument(name='bar')
    d.add_root(m)
    assert d.get_model_by_name('bar') == m
    m.name = None
    assert d.get_model_by_name('bar') == None

def TestDocument_test_can_get_name_overriding_model_by_name(self) -> None:
    d = document.Document()
    m = ModelThatOverridesName(name='foo')
    d.add_root(m)
    assert d.get_model_by_name('foo') == m
    m.name = 'bar'
    assert d.get_model_by_name('bar') == m

def TestDocument_test_cannot_get_model_with_duplicate_name(self) -> None:
    d = document.Document()
    m = SomeModelInTestDocument(name='foo')
    m2 = SomeModelInTestDocument(name='foo')
    d.add_root(m)
    d.add_root(m2)
    got_error = False
    try:
        d.get_model_by_name('foo')
    except ValueError as e:
        got_error = True
        assert 'Found more than one' in repr(e)
    assert got_error
    d.remove_root(m)
    assert d.get_model_by_name('foo') == m2

def TestDocument_test_select(self) -> None:
    d = document.Document()
    root1 = SomeModelInTestDocument(foo=42, name='a')
    child1 = SomeModelInTestDocument(foo=43, name='b')
    root2 = SomeModelInTestDocument(foo=44, name='c')
    root3 = SomeModelInTestDocument(foo=44, name='d')
    child3 = SomeModelInTestDocument(foo=45, name='c')
    root4 = AnotherModelInTestDocument(bar=20, name='A')
    root1.child = child1
    root3.child = child3
    d.add_root(root1)
    d.add_root(root2)
    d.add_root(root3)
    d.add_root(root4)
    assert {root1} == set(d.select(dict(foo=42)))
    assert {root1} == set(d.select(dict(name='a')))
    assert {root2, child3} == set(d.select(dict(name='c')))
    assert set() == set(d.select(dict(name='nope')))
    assert set() == set(root3.select(dict(name='a')))
    assert {child3} == set(root3.select(dict(name='c')))
    assert root3 == d.select_one(dict(name='d'))
    assert None == d.select_one(dict(name='nope'))
    got_error = False
    try:
        d.select_one(dict(name='c'))
    except ValueError as e:
        got_error = True
        assert 'Found more than one' in repr(e)
    assert got_error
    assert None == root3.select_one(dict(name='a'))
    assert child3 == root3.select_one(dict(name='c'))
    d.set_select(dict(foo=44), dict(name='c'))
    assert {root2, child3, root3} == set(d.select(dict(name='c')))
    root3.set_select(dict(name='c'), dict(foo=57))
    assert {child3, root3} == set(d.select(dict(foo=57)))
    assert {child3, root3} == set(root3.select(dict(foo=57)))
    d.set_select(SomeModelInTestDocument, dict(name='new_name'))
    assert len(d.select(dict(name='new_name'))) == 5
    assert len(d.select(dict(name='A'))) == 1
    d.set_select(AnotherModelInTestDocument, dict(name='B'))
    assert {root4} == set(d.select(dict(name='B')))

def TestDocument_test_is_single_string_selector(self) -> None:
    d = document.Document()
    assert d._is_single_string_selector(dict(foo='c'), 'foo')
    assert not d._is_single_string_selector(dict(foo='c', bar='d'), 'foo')
    assert not d._is_single_string_selector(dict(foo=42), 'foo')

def TestDocument_test_all_models_with_multiple_references(self) -> None:
    d = document.Document()
    assert not d.roots
    assert len(d._all_models) == 0
    root1 = SomeModelInTestDocument()
    root2 = SomeModelInTestDocument()
    child1 = AnotherModelInTestDocument()
    root1.child = child1
    root2.child = child1
    d.add_root(root1)
    d.add_root(root2)
    assert len(d.roots) == 2
    assert len(d._all_models) == 3
    root1.child = None
    assert len(d._all_models) == 3
    root2.child = None
    assert len(d._all_models) == 2
    root1.child = child1
    assert len(d._all_models) == 3
    root2.child = child1
    assert len(d._all_models) == 3
    d.remove_root(root1)
    assert len(d._all_models) == 2
    d.remove_root(root2)
    assert len(d._all_models) == 0

def TestDocument_test_all_models_with_cycles(self) -> None:
    d = document.Document()
    assert not d.roots
    assert len(d._all_models) == 0
    root1 = SomeModelInTestDocument()
    root2 = SomeModelInTestDocument()
    child1 = SomeModelInTestDocument()
    root1.child = child1
    root2.child = child1
    child1.child = root1
    print('adding root1')
    d.add_root(root1)
    print('adding root2')
    d.add_root(root2)
    assert len(d.roots) == 2
    assert len(d._all_models) == 3
    print('clearing child of root1')
    root1.child = None
    assert len(d._all_models) == 3
    print('clearing child of root2')
    root2.child = None
    assert len(d._all_models) == 2
    print('putting child1 back in root1')
    root1.child = child1
    assert len(d._all_models) == 3
    print('Removing root1')
    d.remove_root(root1)
    assert len(d._all_models) == 1
    print('Removing root2')
    d.remove_root(root2)
    assert len(d._all_models) == 0

def TestDocument_test_change_notification(self) -> None:
    d = document.Document()
    assert not d.roots
    m = AnotherModelInTestDocument()
    d.add_root(m)
    assert len(d.roots) == 1
    assert m.bar == 1
    assert curdoc() is not d
    events = []
    curdoc_from_listener = []

    def listener(event):
        curdoc_from_listener.append(curdoc())
        events.append(event)
    d.on_change(listener)
    m.bar = 42
    assert events
    event = events[0]
    assert isinstance(event, ModelChangedEvent)
    assert event.document == d
    assert event.model == m
    assert event.attr == 'bar'
    assert event.old == 1
    assert event.new == 42
    assert len(curdoc_from_listener) == 1
    assert curdoc_from_listener[0] is d

def TestDocument_test_stream_notification(self) -> None:
    d = document.Document()
    assert not d.roots
    m = ColumnDataSource(data=dict(a=[10], b=[20]))
    d.add_root(m)
    assert len(d.roots) == 1
    assert curdoc() is not d
    events = []
    curdoc_from_listener = []

    def listener(event):
        curdoc_from_listener.append(curdoc())
        events.append(event)
    d.on_change(listener)
    m.stream(dict(a=[11, 12], b=[21, 22]), 200)
    assert events
    event = events[0]
    assert isinstance(event, ModelChangedEvent)
    assert isinstance(event.hint, ColumnsStreamedEvent)
    assert event.document == d
    assert event.model == m
    assert event.hint.column_source == m
    assert event.hint.data == dict(a=[11, 12], b=[21, 22])
    assert event.hint.rollover == 200
    assert event.attr == 'data'
    assert event.old == dict(a=[10, 11, 12], b=[20, 21, 22])
    assert event.new == dict(a=[10, 11, 12], b=[20, 21, 22])
    assert len(curdoc_from_listener) == 1
    assert curdoc_from_listener[0] is d

def TestDocument_test_patch_notification(self) -> None:
    d = document.Document()
    assert not d.roots
    m = ColumnDataSource(data=dict(a=[10, 11], b=[20, 21]))
    d.add_root(m)
    assert len(d.roots) == 1
    assert curdoc() is not d
    events = []
    curdoc_from_listener = []

    def listener(event):
        curdoc_from_listener.append(curdoc())
        events.append(event)
    d.on_change(listener)
    m.patch(dict(a=[(0, 1)], b=[(0, 0), (1, 1)]))
    assert events
    event = events[0]
    assert isinstance(event, ModelChangedEvent)
    assert isinstance(event.hint, ColumnsPatchedEvent)
    assert event.document == d
    assert event.model == m
    assert event.hint.column_source == m
    assert event.hint.patches == dict(a=[(0, 1)], b=[(0, 0), (1, 1)])
    assert event.attr == 'data'
    assert event.old == dict(a=[1, 11], b=[0, 1])
    assert event.new == dict(a=[1, 11], b=[0, 1])
    assert len(curdoc_from_listener) == 1
    assert curdoc_from_listener[0] is d

def TestDocument_test_change_notification_removal(self) -> None:
    d = document.Document()
    assert not d.roots
    m = AnotherModelInTestDocument()
    d.add_root(m)
    assert len(d.roots) == 1
    assert m.bar == 1
    events = []

    def listener(event):
        events.append(event)
    d.on_change(listener)
    m.bar = 42
    assert len(events) == 1
    assert events[0].new == 42
    d.remove_on_change(listener)
    m.bar = 43
    assert len(events) == 1

def TestDocument_test_notification_of_roots(self) -> None:
    d = document.Document()
    assert not d.roots
    events = []

    def listener(event):
        events.append(event)
    d.on_change(listener)
    m = AnotherModelInTestDocument(bar=1)
    d.add_root(m)
    assert len(d.roots) == 1
    assert len(events) == 1
    assert isinstance(events[0], RootAddedEvent)
    assert events[0].model == m
    m2 = AnotherModelInTestDocument(bar=2)
    d.add_root(m2)
    assert len(d.roots) == 2
    assert len(events) == 2
    assert isinstance(events[1], RootAddedEvent)
    assert events[1].model == m2
    d.remove_root(m)
    assert len(d.roots) == 1
    assert len(events) == 3
    assert isinstance(events[2], RootRemovedEvent)
    assert events[2].model == m
    d.remove_root(m2)
    assert len(d.roots) == 0
    assert len(events) == 4
    assert isinstance(events[3], RootRemovedEvent)
    assert events[3].model == m2

def TestDocument_test_notification_of_title(self) -> None:
    d = document.Document()
    assert not d.roots
    assert d.title == document.DEFAULT_TITLE
    events = []

    def listener(event):
        events.append(event)
    d.on_change(listener)
    d.title = 'Foo'
    assert d.title == 'Foo'
    assert len(events) == 1
    assert isinstance(events[0], TitleChangedEvent)
    assert events[0].document is d
    assert events[0].title == 'Foo'

def TestDocument_test_add_remove_periodic_callback(self) -> None:
    d = document.Document()
    events = []

    def listener(event):
        events.append(event)
    d.on_change(listener)
    assert len(d.session_callbacks) == 0
    assert not events

    def cb():
        pass
    callback_obj = d.add_periodic_callback(cb, 1)
    assert len(d.session_callbacks) == len(events) == 1
    assert isinstance(events[0], SessionCallbackAdded)
    assert callback_obj == d.session_callbacks[0] == events[0].callback
    assert callback_obj.period == 1
    d.remove_periodic_callback(callback_obj)
    assert len(d.session_callbacks) == 0
    assert len(events) == 2
    assert isinstance(events[0], SessionCallbackAdded)
    assert isinstance(events[1], SessionCallbackRemoved)

def TestDocument_test_add_remove_timeout_callback(self) -> None:
    d = document.Document()
    events = []

    def listener(event):
        events.append(event)
    d.on_change(listener)
    assert len(d.session_callbacks) == 0
    assert not events

    def cb():
        pass
    callback_obj = d.add_timeout_callback(cb, 1)
    assert len(d.session_callbacks) == len(events) == 1
    assert isinstance(events[0], SessionCallbackAdded)
    assert callback_obj == d.session_callbacks[0] == events[0].callback
    assert callback_obj.timeout == 1
    d.remove_timeout_callback(callback_obj)
    assert len(d.session_callbacks) == 0
    assert len(events) == 2
    assert isinstance(events[0], SessionCallbackAdded)
    assert isinstance(events[1], SessionCallbackRemoved)

def TestDocument_test_add_partial_callback(self) -> None:
    from functools import partial
    d = document.Document()
    events = []

    def listener(event):
        events.append(event)
    d.on_change(listener)
    assert len(d.session_callbacks) == 0
    assert not events

    def _cb():
        pass
    cb = partial(_cb)
    callback_obj = d.add_timeout_callback(cb, 1)
    assert len(d.session_callbacks) == len(events) == 1
    assert isinstance(events[0], SessionCallbackAdded)
    assert callback_obj == d.session_callbacks[0] == events[0].callback
    assert callback_obj.timeout == 1

def TestDocument_test_add_remove_next_tick_callback(self) -> None:
    d = document.Document()
    events = []

    def listener(event):
        events.append(event)
    d.on_change(listener)
    assert len(d.session_callbacks) == 0
    assert not events

    def cb():
        pass
    callback_obj = d.add_next_tick_callback(cb)
    assert len(d.session_callbacks) == len(events) == 1
    assert isinstance(events[0], SessionCallbackAdded)
    assert callback_obj == d.session_callbacks[0] == events[0].callback
    d.remove_next_tick_callback(callback_obj)
    assert len(d.session_callbacks) == 0
    assert len(events) == 2
    assert isinstance(events[0], SessionCallbackAdded)
    assert isinstance(events[1], SessionCallbackRemoved)

def TestDocument_test_periodic_callback_gets_curdoc(self) -> None:
    d = document.Document()
    assert curdoc() is not d
    curdoc_from_cb = []

    def cb():
        curdoc_from_cb.append(curdoc())
    callback_obj = d.add_periodic_callback(cb, 1)
    callback_obj.callback()
    assert len(curdoc_from_cb) == 1
    assert curdoc_from_cb[0] is d

def TestDocument_test_timeout_callback_gets_curdoc(self) -> None:
    d = document.Document()
    assert curdoc() is not d
    curdoc_from_cb = []

    def cb():
        curdoc_from_cb.append(curdoc())
    callback_obj = d.add_timeout_callback(cb, 1)
    callback_obj.callback()
    assert len(curdoc_from_cb) == 1
    assert curdoc_from_cb[0] is d

def TestDocument_test_next_tick_callback_gets_curdoc(self) -> None:
    d = document.Document()
    assert curdoc() is not d
    curdoc_from_cb = []

    def cb():
        curdoc_from_cb.append(curdoc())
    callback_obj = d.add_next_tick_callback(cb)
    callback_obj.callback()
    assert len(curdoc_from_cb) == 1
    assert curdoc_from_cb[0] is d

def TestDocument_test_model_callback_gets_curdoc(self) -> None:
    d = document.Document()
    m = AnotherModelInTestDocument(bar=42)
    d.add_root(m)
    assert curdoc() is not d
    curdoc_from_cb = []

    def cb(attr, old, new):
        curdoc_from_cb.append(curdoc())
    m.on_change('bar', cb)
    m.bar = 43
    assert len(curdoc_from_cb) == 1
    assert curdoc_from_cb[0] is d

def TestDocument_test_clear(self) -> None:
    d = document.Document()
    assert not d.roots
    assert d.title == document.DEFAULT_TITLE
    d.add_root(AnotherModelInTestDocument())
    d.add_root(AnotherModelInTestDocument())
    d.title = 'Foo'
    assert len(d.roots) == 2
    assert d.title == 'Foo'
    d.clear()
    assert not d.roots
    assert not d._all_models
    assert d.title == 'Foo'

def TestDocument_test_serialization_one_model(self) -> None:
    d = document.Document()
    assert not d.roots
    assert len(d._all_models) == 0
    root1 = SomeModelInTestDocument()
    d.add_root(root1)
    d.title = 'Foo'
    json = d.to_json_string()
    copy = document.Document.from_json_string(json)
    assert len(copy.roots) == 1
    assert copy.title == 'Foo'

def TestDocument_test_serialization_more_models(self) -> None:
    d = document.Document()
    assert not d.roots
    assert len(d._all_models) == 0
    root1 = SomeModelInTestDocument(foo=42)
    root2 = SomeModelInTestDocument(foo=43)
    child1 = SomeModelInTestDocument(foo=44)
    root1.child = child1
    root2.child = child1
    d.add_root(root1)
    d.add_root(root2)
    assert len(d.roots) == 2
    json = d.to_json_string()
    copy = document.Document.from_json_string(json)
    assert len(copy.roots) == 2
    foos = []
    for r in copy.roots:
        foos.append(r.foo)
    foos.sort()
    assert [42, 43] == foos
    some_root = next(iter(copy.roots))
    assert some_root.child.foo == 44

def TestDocument_test_serialization_has_version(self) -> None:
    from bokeh import __version__
    d = document.Document()
    json = d.to_json()
    assert json['version'] == __version__

def TestDocument_test_patch_integer_property(self) -> None:
    d = document.Document()
    assert not d.roots
    assert len(d._all_models) == 0
    root1 = SomeModelInTestDocument(foo=42)
    root2 = SomeModelInTestDocument(foo=43)
    child1 = SomeModelInTestDocument(foo=44)
    root1.child = child1
    root2.child = child1
    d.add_root(root1)
    d.add_root(root2)
    assert len(d.roots) == 2
    event1 = ModelChangedEvent(d, root1, 'foo', root1.foo, 57, 57)
    (patch1, buffers) = process_document_events([event1])
    d.apply_json_patch_string(patch1)
    assert root1.foo == 57
    event2 = ModelChangedEvent(d, child1, 'foo', child1.foo, 67, 67)
    (patch2, buffers) = process_document_events([event2])
    d.apply_json_patch_string(patch2)
    assert child1.foo == 67

def TestDocument_test_patch_spec_property(self) -> None:
    d = document.Document()
    assert not d.roots
    assert len(d._all_models) == 0
    root1 = ModelWithSpecInTestDocument(foo=42)
    d.add_root(root1)
    assert len(d.roots) == 1

    def patch_test(new_value):
        serializable_new = root1.lookup('foo').property.to_serializable(root1, 'foo', new_value)
        event1 = ModelChangedEvent(d, root1, 'foo', root1.foo, new_value, serializable_new)
        (patch1, buffers) = process_document_events([event1])
        d.apply_json_patch_string(patch1)
        if isinstance(new_value, dict):
            expected = copy(new_value)
            if 'units' not in expected:
                expected['units'] = root1.foo_units
            assert expected == root1.lookup('foo').serializable_value(root1)
        else:
            assert new_value == root1.foo
    patch_test(57)
    assert 'data' == root1.foo_units
    patch_test(dict(value=58))
    assert 'data' == root1.foo_units
    patch_test(dict(value=58, units='screen'))
    assert 'screen' == root1.foo_units
    patch_test(dict(value=59, units='screen'))
    assert 'screen' == root1.foo_units
    patch_test(dict(value=59, units='data'))
    assert 'data' == root1.foo_units
    patch_test(dict(value=60, units='data'))
    assert 'data' == root1.foo_units
    patch_test(dict(value=60, units='data'))
    assert 'data' == root1.foo_units
    patch_test(61)
    assert 'data' == root1.foo_units
    root1.foo = 'a_string'
    patch_test('woot')
    assert 'data' == root1.foo_units
    patch_test(dict(field='woot2'))
    assert 'data' == root1.foo_units
    patch_test(dict(field='woot2', units='screen'))
    assert 'screen' == root1.foo_units
    patch_test(dict(field='woot3'))
    assert 'screen' == root1.foo_units
    patch_test(dict(value=70))
    assert 'screen' == root1.foo_units
    root1.foo = 123
    patch_test(71)
    assert 'screen' == root1.foo_units

def TestDocument_test_patch_reference_property(self) -> None:
    d = document.Document()
    assert not d.roots
    assert len(d._all_models) == 0
    root1 = SomeModelInTestDocument(foo=42)
    root2 = SomeModelInTestDocument(foo=43)
    child1 = SomeModelInTestDocument(foo=44)
    child2 = SomeModelInTestDocument(foo=45)
    child3 = SomeModelInTestDocument(foo=46, child=child2)
    root1.child = child1
    root2.child = child1
    d.add_root(root1)
    d.add_root(root2)
    assert len(d.roots) == 2
    assert child1.id in d._all_models
    assert child2.id not in d._all_models
    assert child3.id not in d._all_models
    event1 = ModelChangedEvent(d, root1, 'child', root1.child, child3, child3)
    (patch1, buffers) = process_document_events([event1])
    d.apply_json_patch_string(patch1)
    assert root1.child.id == child3.id
    assert root1.child.child.id == child2.id
    assert child1.id in d._all_models
    assert child2.id in d._all_models
    assert child3.id in d._all_models
    event2 = ModelChangedEvent(d, root1, 'child', root1.child, child1, child1)
    (patch2, buffers) = process_document_events([event2])
    d.apply_json_patch_string(patch2)
    assert root1.child.id == child1.id
    assert root1.child.child is None
    assert child1.id in d._all_models
    assert child2.id not in d._all_models
    assert child3.id not in d._all_models

def TestDocument_test_patch_two_properties_at_once(self) -> None:
    d = document.Document()
    assert not d.roots
    assert len(d._all_models) == 0
    root1 = SomeModelInTestDocument(foo=42)
    child1 = SomeModelInTestDocument(foo=43)
    root1.child = child1
    d.add_root(root1)
    assert len(d.roots) == 1
    assert root1.child == child1
    assert root1.foo == 42
    assert root1.child.foo == 43
    child2 = SomeModelInTestDocument(foo=44)
    event1 = ModelChangedEvent(d, root1, 'foo', root1.foo, 57, 57)
    event2 = ModelChangedEvent(d, root1, 'child', root1.child, child2, child2)
    (patch1, buffers) = process_document_events([event1, event2])
    d.apply_json_patch_string(patch1)
    assert root1.foo == 57
    assert root1.child.foo == 44

def TestDocument_test_scatter(self) -> None:
    from bokeh.io.doc import set_curdoc
    from bokeh.plotting import figure
    import numpy as np
    d = document.Document()
    set_curdoc(d)
    assert not d.roots
    assert len(d._all_models) == 0
    p1 = figure(tools=[])
    N = 10
    x = np.linspace(0, 4 * np.pi, N)
    y = np.sin(x)
    p1.scatter(x, y, color='#FF00FF', nonselection_fill_color='#FFFF00', nonselection_fill_alpha=1)
    d.add_root(p1)
    assert len(d.roots) == 1

def TestDocument_test_event_handles_new_callbacks_in_event_callback(self) -> None:
    from bokeh.models import Button
    d = document.Document()
    button1 = Button(label='1')
    button2 = Button(label='2')

    def clicked_1():
        button2.on_click(clicked_2)
        d.add_root(button2)

    def clicked_2():
        pass
    button1.on_click(clicked_1)
    d.add_root(button1)
    event_json = {'event_name': 'button_click', 'event_values': {'model': {'id': button1.id}}}
    try:
        d.apply_json_event(event_json)
    except RuntimeError:
        pytest.fail('apply_json_event probably did not copy models before modifying')