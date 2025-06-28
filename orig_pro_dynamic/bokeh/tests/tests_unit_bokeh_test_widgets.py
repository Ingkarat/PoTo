import pytest
pytest
import inspect

def get_prop_set(class_object):
    base_classes = list(inspect.getmro(class_object))
    base_classes.remove(class_object)
    base_properties = []
    for base_class in base_classes:
        base_properties.extend(dir(base_class))
    class_properties = set(dir(class_object)).difference(set(base_properties))
    return class_properties

def TestPanel_setup_method(self):
    from bokeh.models import Panel
    self.panelCls = Panel

def TestPanel_test_expectedprops(self) -> None:
    expected_properties = {'title', 'child'}
    actual_properties = get_prop_set(self.panelCls)
    assert expected_properties.issubset(actual_properties)

def TestPanel_test_prop_defaults(self) -> None:
    p1 = Panel()
    p2 = Panel()
    assert p1.title == ''
    assert p2.title == ''
    assert p1.child == None

def TestTabs_setup_method(self):
    from bokeh.models import Tabs, Panel
    self.tabsCls = Tabs
    self.panelCls = Panel

def TestTabs_test_expected_props(self) -> None:
    expected_properties = {'tabs', 'active'}
    actual_properties = get_prop_set(self.tabsCls)
    assert expected_properties.issubset(actual_properties)

def TestTabs_test_props_defaults(self) -> None:
    tab = Tabs()
    assert tab.tabs == []
    assert tab.active == 0