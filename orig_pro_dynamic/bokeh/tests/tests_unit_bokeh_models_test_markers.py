import pytest
pytest
from bokeh.models.markers import Marker, Scatter, marker_types

def test_all_markers_in_markers_dictionary() -> None:
    not_found = [marker for marker in Marker.__subclasses__() if marker not in marker_types.values()]
    assert len(not_found) == 1
    assert not_found[0] == Scatter