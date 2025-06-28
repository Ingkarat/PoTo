import pytest
pytest
from bokeh._testing.util.api import verify_all
import bokeh.embed as be
ALL = ('autoload_static', 'components', 'file_html', 'json_item', 'server_document', 'server_session')
Test___all__ = verify_all(be, ALL)