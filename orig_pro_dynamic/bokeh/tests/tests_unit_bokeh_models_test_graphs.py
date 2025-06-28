import pytest
pytest
import networkx as nx
from bokeh.models.graphs import StaticLayoutProvider, from_networkx

def test_staticlayoutprovider_init_props() -> None:
    provider = StaticLayoutProvider()
    assert provider.graph_layout == {}

def test_from_networkx_deprecated() -> None:
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3])
    G.add_edges_from([[0, 1], [0, 2], [2, 3]])
    from bokeh.util.deprecation import BokehDeprecationWarning
    with pytest.warns(BokehDeprecationWarning):
        from_networkx(G, nx.circular_layout)