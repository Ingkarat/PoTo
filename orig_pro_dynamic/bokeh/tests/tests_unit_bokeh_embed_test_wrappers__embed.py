import pytest
pytest
import bokeh.embed.wrappers as bew

def test__ONLOAD() -> None:
    assert bew._ONLOAD == '(function() {\n  var fn = function() {\n%(code)s\n  };\n  if (document.readyState != "loading") fn();\n  else document.addEventListener("DOMContentLoaded", fn);\n})();'

def test__SAFELY() -> None:
    assert bew._SAFELY == 'Bokeh.safely(function() {\n%(code)s\n});'

def Test_wrap_in_onload_test_render(self) -> None:
    assert bew.wrap_in_onload('code\nmorecode') == '(function() {\n  var fn = function() {\n    code\n    morecode\n  };\n  if (document.readyState != "loading") fn();\n  else document.addEventListener("DOMContentLoaded", fn);\n})();'

def Test_wrap_in_safely_test_render(self) -> None:
    assert bew.wrap_in_safely('code\nmorecode') == 'Bokeh.safely(function() {\n  code\n  morecode\n});'

def Test_wrap_in_script_tag_test_render(self) -> None:
    assert bew.wrap_in_script_tag('code\nmorecode') == '\n<script type="text/javascript">\n  code\n  morecode\n</script>'