import pytest
pytest
from bokeh.models import Circle, ColumnDataSource, IndexFilter, Line, MultiLine, Patch
import bokeh.models.renderers as bmr

@pytest.mark.parametrize('glyph', [Line, Patch])
def TestGlyphRenderer_test_check_cdsview_filters_with_connected_error(self, glyph) -> None:
    glyph = Line
    renderer = bmr.GlyphRenderer()
    renderer.glyph = glyph()
    check = renderer._check_cdsview_filters_with_connected()
    assert check == []
    renderer.view.filters = [IndexFilter()]
    check = renderer._check_cdsview_filters_with_connected()
    assert check != []

def TestGraphRenderer_test_init_props(self) -> None:
    renderer = bmr.GraphRenderer()
    assert renderer.x_range_name == 'default'
    assert renderer.y_range_name == 'default'
    assert renderer.node_renderer.data_source.data == dict(index=[])
    assert renderer.edge_renderer.data_source.data == dict(start=[], end=[])
    assert renderer.layout_provider is None

def TestGraphRenderer_test_check_malformed_graph_source_no_errors(self) -> None:
    renderer = bmr.GraphRenderer()
    check = renderer._check_malformed_graph_source()
    assert check == []

def TestGraphRenderer_test_check_malformed_graph_source_no_node_index(self) -> None:
    node_source = ColumnDataSource()
    node_renderer = bmr.GlyphRenderer(data_source=node_source, glyph=Circle())
    renderer = bmr.GraphRenderer(node_renderer=node_renderer)
    check = renderer._check_malformed_graph_source()
    assert check != []

def TestGraphRenderer_test_check_malformed_graph_source_no_edge_start_or_end(self) -> None:
    edge_source = ColumnDataSource()
    edge_renderer = bmr.GlyphRenderer(data_source=edge_source, glyph=MultiLine())
    renderer = bmr.GraphRenderer(edge_renderer=edge_renderer)
    check = renderer._check_malformed_graph_source()
    assert check != []