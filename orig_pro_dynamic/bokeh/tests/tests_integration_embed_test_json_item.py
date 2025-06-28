import pytest
pytest
import json
from jinja2 import Template
from bokeh.embed import json_item
from bokeh.models import Plot
from bokeh.resources import INLINE
pytest_plugins = ('bokeh._testing.plugins.project', 'bokeh._testing.plugins.selenium')
PAGE = Template('\n<!DOCTYPE html>\n<html lang="en">\n<head>\n  {{ resources }}\n</head>\n\n<body>\n  <div id="_target"></div>\n  <script>\n    Bokeh.embed.embed_item({{ item }}, "_target");\n  </script>\n</body>\n')

def Test_json_item_test_bkroot_added_to_target(self, driver, test_file_path_and_url) -> None:
    p = Plot()
    html = PAGE.render(item=json.dumps(json_item(p)), resources=INLINE.render())
    (path, url) = test_file_path_and_url
    with open(path, 'w') as f:
        f.write(html)
    driver.get(url)
    div = driver.find_elements_by_class_name('bk-root')
    assert len(div) == 1