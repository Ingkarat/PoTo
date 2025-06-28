import pytest
pytest
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import Figure
from bokeh.models.layouts import Row, Column, LayoutDOM, WidgetBox

def check_props(layout):
    assert layout.width is None
    assert layout.height is None
    assert layout.children == []

def check_props_with_sizing_mode(layout):
    assert layout.width is None
    assert layout.height is None
    assert layout.children == []
    assert layout.sizing_mode == None

def check_children_prop(layout_callable):
    components = [Row(), Column(), Figure()]
    layout1 = layout_callable(*components)
    assert layout1.children == components
    layout2 = layout_callable(children=components)
    assert layout2.children == components
    with pytest.raises(ValueError):
        layout_callable(children=[ColumnDataSource()])

def test_Row() -> None:
    check_props_with_sizing_mode(Row())
    check_children_prop(Row)

def test_Column() -> None:
    check_props_with_sizing_mode(Column())
    check_children_prop(Column)

def check_widget_box_children_prop(layout_callable):
    components = [Slider()]
    layout1 = layout_callable(*components)
    assert layout1.children == components
    layout2 = layout_callable(children=components)
    assert layout2.children == components
    with pytest.raises(ValueError):
        layout_callable(children=[ColumnDataSource()])

def test_LayoutDOM_css_classes() -> None:
    m = LayoutDOM()
    assert m.css_classes == []
    m.css_classes = ['foo']
    assert m.css_classes == ['foo']
    m.css_classes = ('bar',)
    assert m.css_classes == ['bar']

def test_widgetbox_deprecated() -> None:
    from bokeh.util.deprecation import BokehDeprecationWarning
    with pytest.warns(BokehDeprecationWarning):
        WidgetBox()