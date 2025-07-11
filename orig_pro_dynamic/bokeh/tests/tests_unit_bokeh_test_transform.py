import pytest
pytest
from bokeh._testing.util.api import verify_all
from bokeh.models import CategoricalColorMapper, CategoricalMarkerMapper, CategoricalPatternMapper, CumSum, Dodge, FactorRange, Jitter, LinearColorMapper, LogColorMapper, Stack
import bokeh.transform as bt
ALL = ('cumsum', 'dodge', 'factor_cmap', 'factor_hatch', 'factor_mark', 'jitter', 'linear_cmap', 'log_cmap', 'stack', 'transform')
Test___all__ = verify_all(bt, ALL)

def Test_cumsum_test_basic(object) -> None:
    s = bt.cumsum('foo')
    assert isinstance(s, dict)
    assert list(s.keys()) == ['expr']
    assert isinstance(s['expr'], CumSum)
    assert s['expr'].field == 'foo'
    assert s['expr'].include_zero == False

def Test_cumsum_test_include_zero(object) -> None:
    s = bt.cumsum('foo', include_zero=True)
    assert isinstance(s, dict)
    assert list(s.keys()) == ['expr']
    assert isinstance(s['expr'], CumSum)
    assert s['expr'].field == 'foo'
    assert s['expr'].include_zero == True

def Test_dodge_test_basic(self) -> None:
    t = bt.dodge('foo', 0.5)
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], Dodge)
    assert t['transform'].value == 0.5
    assert t['transform'].range is None

def Test_dodge_test_with_range(self) -> None:
    r = FactorRange('a')
    t = bt.dodge('foo', 0.5, range=r)
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], Dodge)
    assert t['transform'].value == 0.5
    assert t['transform'].range is r
    assert t['transform'].range.factors == ['a']

def Test_factor_cmap_test_basic(self) -> None:
    t = bt.factor_cmap('foo', ['red', 'green'], ['foo', 'bar'], start=1, end=2, nan_color='pink')
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], CategoricalColorMapper)
    assert t['transform'].palette == ['red', 'green']
    assert t['transform'].factors == ['foo', 'bar']
    assert t['transform'].start == 1
    assert t['transform'].end == 2
    assert t['transform'].nan_color == 'pink'

def Test_factor_cmap_test_defaults(self) -> None:
    t = bt.factor_cmap('foo', ['red', 'green'], ['foo', 'bar'])
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], CategoricalColorMapper)
    assert t['transform'].palette == ['red', 'green']
    assert t['transform'].factors == ['foo', 'bar']
    assert t['transform'].start == 0
    assert t['transform'].end is None
    assert t['transform'].nan_color == 'gray'

def Test_factor_hatch_test_basic(self) -> None:
    t = bt.factor_hatch('foo', ['+', '-'], ['foo', 'bar'], start=1, end=2)
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], CategoricalPatternMapper)
    assert t['transform'].patterns == ['+', '-']
    assert t['transform'].factors == ['foo', 'bar']
    assert t['transform'].start == 1
    assert t['transform'].end == 2

def Test_factor_hatch_test_defaults(self) -> None:
    t = bt.factor_hatch('foo', ['+', '-'], ['foo', 'bar'])
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], CategoricalPatternMapper)
    assert t['transform'].patterns == ['+', '-']
    assert t['transform'].factors == ['foo', 'bar']
    assert t['transform'].start == 0
    assert t['transform'].end is None

def Test_factor_mark_test_basic(self) -> None:
    t = bt.factor_mark('foo', ['hex', 'square'], ['foo', 'bar'], start=1, end=2)
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], CategoricalMarkerMapper)
    assert t['transform'].markers == ['hex', 'square']
    assert t['transform'].factors == ['foo', 'bar']
    assert t['transform'].start == 1
    assert t['transform'].end == 2

def Test_factor_mark_test_defaults(self) -> None:
    t = bt.factor_mark('foo', ['hex', 'square'], ['foo', 'bar'])
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], CategoricalMarkerMapper)
    assert t['transform'].markers == ['hex', 'square']
    assert t['transform'].factors == ['foo', 'bar']
    assert t['transform'].start == 0
    assert t['transform'].end is None

def Test_jitter_test_basic(self) -> None:
    t = bt.jitter('foo', width=0.5, mean=0.1, distribution='normal')
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], Jitter)
    assert t['transform'].width == 0.5
    assert t['transform'].mean == 0.1
    assert t['transform'].distribution == 'normal'
    assert t['transform'].range is None

def Test_jitter_test_defaults(self) -> None:
    t = bt.jitter('foo', width=0.5)
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], Jitter)
    assert t['transform'].width == 0.5
    assert t['transform'].mean == 0
    assert t['transform'].distribution == 'uniform'
    assert t['transform'].range is None

def Test_jitter_test_with_range(self) -> None:
    r = FactorRange('a')
    t = bt.jitter('foo', width=0.5, mean=0.1, range=r)
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], Jitter)
    assert t['transform'].width == 0.5
    assert t['transform'].mean == 0.1
    assert t['transform'].distribution == 'uniform'
    assert t['transform'].range is r
    assert t['transform'].range.factors == ['a']

def Test_linear_cmap_test_basic(self) -> None:
    t = bt.linear_cmap('foo', ['red', 'green'], 0, 10, low_color='orange', high_color='blue', nan_color='pink')
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], LinearColorMapper)
    assert t['transform'].palette == ['red', 'green']
    assert t['transform'].low == 0
    assert t['transform'].high == 10
    assert t['transform'].low_color == 'orange'
    assert t['transform'].high_color == 'blue'
    assert t['transform'].nan_color == 'pink'

def Test_linear_cmap_test_defaults(self) -> None:
    t = bt.linear_cmap('foo', ['red', 'green'], 0, 10)
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], LinearColorMapper)
    assert t['transform'].palette == ['red', 'green']
    assert t['transform'].low == 0
    assert t['transform'].high == 10
    assert t['transform'].low_color is None
    assert t['transform'].high_color is None
    assert t['transform'].nan_color == 'gray'

def Test_log_cmap_test_basic(self) -> None:
    t = bt.log_cmap('foo', ['red', 'green'], 0, 10, low_color='orange', high_color='blue', nan_color='pink')
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], LogColorMapper)
    assert t['transform'].palette == ['red', 'green']
    assert t['transform'].low == 0
    assert t['transform'].high == 10
    assert t['transform'].low_color == 'orange'
    assert t['transform'].high_color == 'blue'
    assert t['transform'].nan_color == 'pink'

def Test_log_cmap_test_defaults(self) -> None:
    t = bt.log_cmap('foo', ['red', 'green'], 0, 10)
    assert isinstance(t, dict)
    assert set(t) == {'field', 'transform'}
    assert t['field'] == 'foo'
    assert isinstance(t['transform'], LogColorMapper)
    assert t['transform'].palette == ['red', 'green']
    assert t['transform'].low == 0
    assert t['transform'].high == 10
    assert t['transform'].low_color is None
    assert t['transform'].high_color is None
    assert t['transform'].nan_color == 'gray'

def Test_stack_test_basic(object) -> None:
    s = bt.stack('foo', 'junk')
    assert isinstance(s, dict)
    assert list(s.keys()) == ['expr']
    assert isinstance(s['expr'], Stack)
    assert s['expr'].fields == ('foo', 'junk')

def Test_transform_test_basic(object) -> None:
    t = bt.transform('foo', 'junk')
    assert t == dict(field='foo', transform='junk')