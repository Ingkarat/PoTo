import pytest
pytest
import json
import os
from mock import patch
import bokeh.util.compiler as buc

def test_nodejs_compile_javascript() -> None:
    assert buc.nodejs_compile('function f(a, b) { return a + b; };', 'javascript', 'some.js') == dict(code='function f(a, b) { return a + b; }\n;\n', deps=[])
    assert buc.nodejs_compile("var some = require('some/module');", 'javascript', 'some.js') == dict(code="var some = require('some/module');\n", deps=['some/module'])
    assert buc.nodejs_compile('\nconst {Model} = require("lib/model");\n\nclass MyModel extends Model {\n    static __name__ = \'MyModel\';\n}\n\nexports.MyModel = MyModel;\n', 'javascript', 'some.js') == dict(code='const { Model } = require("lib/model");\nclass MyModel extends Model {\n}\nMyModel.__name__ = \'MyModel\';\nexports.MyModel = MyModel;\n', deps=['lib/model'])
    assert buc.nodejs_compile('function f(a, b) { eturn a + b; };', 'javascript', 'some.js') == dict(error="\x1b[96msome.js\x1b[0m:\x1b[93m1\x1b[0m:\x1b[93m26\x1b[0m - \x1b[91merror\x1b[0m\x1b[90m TS1005: \x1b[0m';' expected.\n\n\x1b[7m1\x1b[0m function f(a, b) { eturn a + b; };\n\x1b[7m \x1b[0m \x1b[91m                         ~\x1b[0m\n")

def test_nodejs_compile_less() -> None:
    assert buc.nodejs_compile('.bk-some-style { color: mix(#ff0000, #0000ff, 50%); }', 'less', 'some.less') == dict(code='.bk-some-style{color:#800080}')
    assert buc.nodejs_compile('.bk-some-style color: green; }', 'less', 'some.less') == dict(error='ParseError: Unrecognised input in some.less on line 1, column 21:\n1 .bk-some-style color: green; }\n')

def test_Implementation() -> None:
    obj = buc.Implementation()
    assert obj.file == None

def test_Inline() -> None:
    obj = buc.Inline('code')
    assert obj.code == 'code'
    assert obj.file == None
    obj = buc.Inline('code', 'file')
    assert obj.code == 'code'
    assert obj.file == 'file'

def test_TypeScript() -> None:
    obj = buc.TypeScript('code')
    assert isinstance(obj, buc.Inline)
    assert obj.code == 'code'
    assert obj.file == None
    assert obj.lang == 'typescript'

def test_JavaScript() -> None:
    obj = buc.JavaScript('code')
    assert isinstance(obj, buc.Inline)
    assert obj.code == 'code'
    assert obj.file == None
    assert obj.lang == 'javascript'

def test_Less() -> None:
    obj = buc.Less('code')
    assert isinstance(obj, buc.Inline)
    assert obj.code == 'code'
    assert obj.file == None
    assert obj.lang == 'less'

@patch('builtins.open')
def test_FromFile(mock_open) -> None:
    obj = buc.FromFile('path.ts')
    assert obj.lang == 'typescript'
    obj = buc.FromFile('path.js')
    assert obj.lang == 'javascript'
    obj = buc.FromFile('path.css')
    assert obj.lang == 'less'
    obj = buc.FromFile('path.less')
    assert obj.lang == 'less'

def test_exts() -> None:
    assert buc.exts == ('.ts', '.js', '.css', '.less')

def test_jsons() -> None:
    for file in os.listdir(os.path.join(buc.bokehjs_dir, 'js')):
        if file.endswith('.json'):
            with open(os.path.join(buc.bokehjs_dir, 'js', file), encoding='utf-8') as f:
                assert all(['\\' not in mod for mod in json.loads(f.read())])

def test_inline_extension() -> None:
    from bokeh.io import save
    from bokeh.models import TickFormatter
    from bokeh.plotting import figure
    from bokeh.util.compiler import TypeScript
    TS_CODE = '\n    import {TickFormatter} from "models/formatters/tick_formatter"\n\n    export class TestFormatter extends TickFormatter {\n\n      doFormat(ticks: number[]): string[] {\n        if (ticks.length == 0)\n          return[]\n        else {\n          const formatted = [`${ticks[0]}`]\n          for (let i = 1; i < ticks.length; i++) {\n            const difference = (ticks[i] - ticks[0]).toPrecision(2)\n            formatted.push(`+${difference}}`)\n          }\n          return formatted\n        }\n      }\n    }\n    '

    class TestFormatter(TickFormatter):
        __implementation__ = TypeScript(TS_CODE)

    class TestFormatter2(TickFormatter):
        __implementation__ = TypeScript('^')
    p = figure()
    p.circle([1, 2, 3, 4, 6], [5, 7, 3, 2, 4])
    p.xaxis.formatter = TestFormatter()
    save(p)