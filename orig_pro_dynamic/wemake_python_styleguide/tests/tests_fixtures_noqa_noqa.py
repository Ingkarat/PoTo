"""
This file contains all possible violations.

It is used for e2e tests.
"""
from __future__ import print_function
from typing import List
import os.path
import sys as sys
from _some import protected
from some import _protected
from foo import bar
from foo.bar import baz
from .version import get_version
import import1
import import2
import import3
import import4
from some_name import name1, name2, name3, name4, name5, name6, name7, name8, name9, name10, name11, name12, name13, name14, name15, name16, name17, name18, name19, name20, name21, name22, name23, name24, name25, name26, name27, name28, name29, name30, name31, name32, name33, name34, name35, name36, name37, name38
some_int = 1 # type: int
full_name = u'Nikita Sobolev'
phone_number = 555123999
partial_number = 0.05
float_zero = 0.0
formatted_string = f'Hi, {full_name}'
formatted_string_complex = f'1+1={1 + 1}'

def __getattr__():
    anti_wps428 = 1

def foo_func():
    yield (1, 2, 3, 4, 5, 6)
my_print(x > 2 > y > 4)
try:
    my_print(1)
    my_print(2)
    my_print(3)
except AnyError:
    my_print('nope')

class TooManyPublicAtts(object):

    def __init__(self):
        self.first = 1
        self.second = 2
        self.third = 3
        self.fourth = 4
        self.fifth = 5
        self.sixth = 6
        self.boom = 7

@property
def function_name(value: int=0):
    anti_wps428 = 1

def some():
    from my_module import some_import

    class Nested(object):
        ...

    def nested():
        anti_wps428 = 1
    raise NotImplemented
del {'a': 1}['a']
hasattr(object, 'some')
value = 1
VALUE = 1
x = 2
__private = 3
star_wars_episode_7 = 'the worst episode ever after 8 and 9'
consecutive__underscores = 4
cls = 5
__author__ = 'Nikita Sobolev'
extremely_long_name_that_needs_to_be_shortened_to_work_fine = 2
привет_по_русски = 'Hello, world!'
wrong_alias_ = 'some fake builtin alias'

def some_function():
    _should_not_be_used = 1
    my_print(_should_not_be_used)
(used, __) = (1, 2)

class Mem0Output(object):
    anti_wps124 = 'unreadable class'
type = 'type'
some._execute()

def many_locals():
    (arg1, arg2, arg3, arg4, arg5, arg6) = range(6)

def many_arguments(_arg1, _arg2, _arg3, _arg4, _arg5, _arg6):
    anti_wps428 = 1

def many_returns(xy):
    if xy > 1:
        return 1
    if xy > 2:
        return 2
    if xy > 3:
        return 3
    if xy > 4:
        return 4
    if xy > 5:
        return 5
    return 6

def many_expressions(xy):
    my_print(xy)
    my_print(xy)
    my_print(xy)
    my_print(xy)
    my_print(xy)
    my_print(xy)
    my_print(xy)
    my_print(xy)
    my_print(xy)
    my_print(xy)

class TooManyMethods(object):

    def method1(self):
        anti_wps428 = 1

    def method2(self):
        anti_wps428 = 1

    def method3(self):
        anti_wps428 = 1

    def method4(self):
        anti_wps428 = 1

    def method5(self):
        anti_wps428 = 1

    def method6(self):
        anti_wps428 = 1

    def method7(self):
        anti_wps428 = 1

    def method8(self):
        anti_wps428 = 1

class ManyParents(First, Second, Third, Exception):
    anti_wps428 = 1

async def too_many_awaits():
    await test_function(1)
    await test_function(2)
    await test_function(3)
    await test_function(4)
    await test_function(5)
    await test_function(6)
    await test_function(7)

async def too_many_asserts():
    assert test_function(1)
    assert test_function(2)
    assert test_function(3)
    assert test_function(4)
    assert test_function(5)
    assert test_function(6)
deep_access = some.other[0].field.type.boom

def test_function():
    if xy > 1:
        if xy > 2:
            if xy > 3:
                if xy > 4:
                    if xy > 5:
                        test(5)
line = some.call(7 * 2, 3 / 4) / some.run(5 / some, 8 - 2 + 6)
if line and line > 2 and (line > 3) and (line > 4) and (line > 5):
    anti_wps428 = 1
if line:
    anti_wps428 = 1
elif line > 1:
    anti_wps428 = 1
elif line > 2:
    anti_wps428 = 1
elif line > 3:
    anti_wps428 = 1
elif line > 4:
    anti_wps428 = 1
try:
    do_some_bad()
except ValueError:
    my_print('value')
except KeyError:
    my_print('key')
except IndexError as exc:
    my_print('index', exc)
except TypeError:
    my_print('type')

class BadClass:
    UPPER_CASE_ATTRIBUTE = 12

    def __del__(self, *_args, **_kwargs):
        anti_wps428 = 1

    class Nested:
        anti_wps428 = 1

    async def __eq__(self, other):
        anti_wps428 = 3
magic_numbers = 13.2 + 50
assert 1 < 1 < hex_number
assert 2 > octal_number
hex_number = 255
octal_number = 9
binary_number = 9
number_with_scientific_notation = 1.5e-10
number_with_useless_plus = +5
if '6' in nodes in '6':
    anti_wps428 = 1
assert hex_number == hex_number

async def test_async_function():
    return (123, 33)
if True:
    anti_wps428 = 1

class SomeTestClass(FirstParent, SecondParent, object):
    anti_wps428 = 1
with some_context as first_context, second_context:
    anti_wps428 = 1

class SomeClass(FirstParent, SecondParent, ThirdParent):
    anti_wps428 = 1
if SomeClass:
    my_print(SomeClass)
my_print(1, 2)

def function(arg: Optional[str,]) -> Optional[str,]:
    some_set = {1}
string_modifier = '(\\n)'
multiline_string = 'abc'
modulo_formatting = 'some %s'

def function_with_wrong_return():
    if some:
        my_print(some)
    return

def function_with_wrong_yield():
    if some:
        yield
    yield 1
bad_concatenation = 'ab'
for literal in bad_concatenation:
    continue
with open(bad_concatenation):
    pass
try:
    anti_wps428 = 1
except Exception as ex:
    raise ex

def some_other_function():
    some_value = 1
    return some_value
my_print(one > two and two > three)
my_print(biggesst > middle >= smallest)
for index in [1, 2]:
    my_print(index)
string_concat = 'a' + 'b'
my_print(one == 'a' or one == 'b')
file_obj = open('filaname.py')
my_print(type(file_obj) == int)
my_print(*[], **{'@': 1})
pi = 3.14
my_print(lambda : 0)
xterm += xterm + 1
for range_len in range(len(file_obj)):
    my_print(range_len)
sum_container = 0
for sum_item in file_obj:
    sum_container += sum_item
my_print(sum_container == [])
my_print(sum_container is 0)
try:
    anti_wps428 = 1
except BaseException:
    anti_wps428 = 1
call_with_positional_bool(True, keyword=1)

class MyInt(int):
    """My custom int subclass."""

class ShadowsAttribute(object):
    """Redefines attr from class."""
    first: int
    second = 1

    def __init__(self) -> None:
        self.first = 1
        self.second = 2
for symbol in 'abc':
    anti_wps428 = 1
else:
    anti_wps428 = 1
try:
    anti_wps428 = 1
finally:
    anti_wps428 = 1
nodes = nodes

class Example(object):
    """Correct class docstring."""

    def __init__(self):
        """Correct function docstring."""
        yield 10

    def __eq__(self, object_: object) -> bool:
        return super().__eq__(object_)
for loop_index in range(6):
    my_print(lambda : loop_index)

async def function_with_unreachable():
    await test_function()
    raise ValueError()
    my_print(1)
1 + 2
first = second = 2
(first, nodes[0]) = range(2)
try:
    anti_wps428 = 1
except ValueError:
    anti_wps428 = 1
except ValueError:
    anti_wps428 = 1

class MyBadException(BaseException):
    anti_wps428 = 1
some_if_expr = True if some_set else False
if some_if_expr:
    some_dict['x'] = True
else:
    some_dict['x'] = False

def another_wrong_if():
    if full_name != 'Nikita Sobolev':
        return False
    return True

class ClassWithWrongContents((lambda : object)()):
    __slots__ = ['a', 'a']
    for bad_body_node in range(1):
        anti_wps428 = 1

    def method_with_no_args():
        super(ClassWithWrongContents, self).method_with_no_args()
        self.some_set = {1, 1}

def useless_returning_else():
    if some_set:
        return some_set
    else:
        return TypeError

def multiple_return_path():
    try:
        return 1
    except Exception:
        return 2
    else:
        return 3

def bad_default_values(self, withDoctest='PYFLAKES_DOCTEST' in os.environ):
    return True
for nodes[0] in (1, 2, 3):
    anti_wps428 = 1
with open('some') as MyBadException.custom:
    anti_wps428 = 1
anti_wps428.__truediv__(1)
if not some:
    my_print('False')
else:
    my_print('Wrong')
try:
    try:
        anti_wps428 = 1
    except ValueError:
        raise TypeError('Second')
except TypeError:
    my_print('WTF?')
if some and anti_wps428 == 1:
    anti_wps428 = 'some text'

class WrongMethodOrder(object):

    def _protected(self):
        return self

    def public(self):
        return self
leading_zero = 12.0
positive_exponent = 11.0
wrong_hex = 2748
wrong_escape_raw_string = '\\n'
bad_complex = 1j
zero_div = bad_complex / 0
mult_one = zero_div * 1
mult_one -= -1
CONSTANT = []
numbers = map(lambda string: int(string), ['1'])
if len(numbers) > 0:
    my_print('len!')
if numbers and numbers:
    my_print('duplicate boolop')
if not numbers == [1]:
    my_print('bad compare with not')
if numbers == CONSTANT != [2]:
    my_print(1 + (1 if number else 2))
my_print(numbers in [])
my_print(isinstance(number, int) or isinstance(number, (float, str)))
my_print(isinstance(numbers, (int,)))
if numbers:
    my_print('first')
elif numbers:
    my_print('other')

def sync_gen():
    yield
    raise StopIteration

async def async_gen():
    yield
    raise StopIteration

class CheckStopIteration(object):

    def sync_gen(self):
        yield
        raise StopIteration()

    async def async_gen(self):
        yield
        raise StopIteration()
bad_unicode = b'\\u1'
CheckStopIteration = 1
my_print(literal)
unhashable = {[]}
assert []
unhashable = [] * 2
from json import loads
some_model = MyModel.objects.filter(...).exclude(...)
swap_a = swap_b
swap_b = swap_a
my_print(constant[0:7])
var_a = var_a + var_b

class ChildClass(ParentClass):

    def some_method(self):
        super().some_other_method()
LOWERCASE_ALPH = 'abcdefghijklmnopqrstuvwxyz'
int()
for wrong_loop in call(1, 2, 3):
    my_print('bad loop')
if a in {1}:
    my_print('bad!')

def implicit_yield_from():
    for wrong_yield in call():
        yield wrong_yield
try:
    anti_wps428 = 1
except Exception:
    anti_wps428 = 1
except ValueError:
    anti_wps428 = 1
bad_frozenset = frozenset([1])

def wrong_yield_from():
    yield from []

def consecutive_yields():
    yield 1
    yield 2
for loop_var in loop_iter:
    my_print(loop_iter[loop_var])
if 'key' in some_dict:
    my_print(some_dict['key'])
    my_print(other_dict[1.0])
    my_print(some_sized[len(some_sized) - 2])
deep_func(a)(b)(c)(d)
annotated: List[List[List[List[int]]]]
extra_new_line = ['wrong']
(*numbers,) = [4, 7]
[first_number, second_number] = [4, 7]
for element in range(10):
    try:
        my_print(1)
    except AnyError:
        my_print('nope')
    finally:
        break
    my_print(4)

def raise_bad_exception():
    raise Exception
try:
    cause_errors()
except ValueError or TypeError:
    my_print('Oops.')
if float('NaN') < number:
    my_print('Greater than... what?')

def infinite_loop():
    while True:
        my_print('forever')
my_print(some_float == 1.0)
unnecessary_raw_string = 'no backslashes.'

def many_raises_function(parameter):
    if parameter == 1:
        raise ValueError('1')
    if parameter == 2:
        raise KeyError('2')
    if parameter == 3:
        raise IndexError('3')
    raise TypeError('4')
my_print('\ntext\n')

def get_item():
    return
bad_bitwise = True | True