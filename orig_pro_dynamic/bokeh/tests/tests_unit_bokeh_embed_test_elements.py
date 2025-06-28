import pytest
pytest
from bokeh.embed.util import RenderItem
import bokeh.embed.elements as bee

def Test_div_for_render_item_test_render(self) -> None:
    render_item = RenderItem(docid='doc123', elementid='foo123')
    assert bee.div_for_render_item(render_item).strip() == '<div class="bk-root" id="foo123"></div>'