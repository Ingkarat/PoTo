import pytest
from wemake_python_styleguide.compat.constants import PY38
import_alias = '\nimport os as {0}\n'
from_import_alias = '\nfrom os import path as {0}\n'
class_name = 'class {0}: ...'
function_name = 'def {0}(): ...'
method_name = '\nclass Input(object):\n    def {0}(self): ...\n'
function_argument = 'def test(arg, {0}): ...'
method_argument = '\nclass Input(object):\n    def validate(self, {0}): ...\n'
function_keyword_argument = 'def test(arg, {0}=None): ...'
method_keyword_argument = '\nclass Input(object):\n    def validate(self, {0}=None): ...\n'
function_args_argument = 'def test(arg, *{0}): ...'
function_kwargs_argument = 'def test(arg, **{0}): ...'
method_args_argument = '\nclass Input(object):\n    def validate(self, *{0}): ...\n'
method_kwargs_argument = '\nclass Input(object):\n    def validate(self, **{0}): ...\n'
function_posonly_argument = '\ndef test({0}, /): ...\n'
function_kwonly_argument = '\ndef test(*, {0}): ...\n'
function_kwonly_default_argument = '\ndef test(*, {0}=True): ...\n'
method_kwonly_argument = '\nclass Input(object):\n    def test(self, *, {0}=True): ...\n'
lambda_argument = 'lambda {0}: ...'
lambda_posonly_argument = 'lambda {0}, /: ...'
static_attribute = '\nclass Test:\n    {0} = None\n'
static_typed_attribute = '\nclass Test:\n    {0}: int = None\n'
static_typed_annotation = '\nclass Test:\n    {0}: int\n'
instance_attribute = '\nclass Test(object):\n    def __init__(self):\n        self.{0} = 123\n'
instance_typed_attribute = '\nclass Test(object):\n    def __init__(self):\n        self.{0}: int = 123\n'
variable_def = '{0} = 1'
variable_typed_def = '{0}: int = 2'
variable_typed = '{0}: str'
assignment_expression = '({0} := 1)'
unpacking_variables = '\nfirst.attr, {0} = range(2)\n'
unpacking_star_variables = '\nfirst, *{0} = range(2)\n'
for_variable = '\ndef container():\n    for {0} in []:\n        ...\n'
for_star_variable = '\ndef container():\n    for index, *{0} in []:\n        ...\n'
with_variable = "\ndef container():\n    with open('test.py') as {0}:\n        ...\n"
with_star_variable = "\ndef container():\n    with open('test.py') as (first, *{0}):\n        ...\n"
exception = '\ntry:\n    1 / 0\nexcept Exception as {0}:\n    raise\n'
_ALL_FIXTURES = frozenset((import_alias, from_import_alias, class_name, function_name, method_name, function_argument, method_argument, function_keyword_argument, method_keyword_argument, function_args_argument, function_kwargs_argument, method_args_argument, method_kwargs_argument, function_kwonly_argument, function_kwonly_default_argument, method_kwonly_argument, lambda_argument, static_attribute, static_typed_attribute, static_typed_annotation, instance_attribute, instance_typed_attribute, variable_def, variable_typed_def, variable_typed, unpacking_variables, unpacking_star_variables, for_variable, for_star_variable, with_variable, with_star_variable, exception))
if PY38:
    _ALL_FIXTURES |= {function_posonly_argument, lambda_posonly_argument, assignment_expression}
_FORBIDDEN_UNUSED_TUPLE = frozenset((unpacking_variables, variable_def, with_variable, for_variable))
_FORBIDDEN_BOTH_RAW_AND_PROTECTED_UNUSED = frozenset((unpacking_variables, variable_def, with_variable, variable_typed_def, variable_typed, exception))
if PY38:
    _FORBIDDEN_BOTH_RAW_AND_PROTECTED_UNUSED |= {assignment_expression}
_FORBIDDEN_RAW_UNUSED = _FORBIDDEN_BOTH_RAW_AND_PROTECTED_UNUSED | {static_attribute, static_typed_attribute, static_typed_annotation}
_FORBIDDEN_PROTECTED_UNUSED = _FORBIDDEN_BOTH_RAW_AND_PROTECTED_UNUSED | {for_variable}

@pytest.fixture(params=_ALL_FIXTURES)
def naming_template(request):
    """Parametrized fixture that contains all possible naming templates."""
    return request.param

@pytest.fixture(params=_FORBIDDEN_UNUSED_TUPLE)
def forbidden_tuple_unused_template(request):
    """Returns template that can be used to define wrong unused tuples."""
    return request.param

@pytest.fixture(params=_FORBIDDEN_RAW_UNUSED)
def forbidden_raw_unused_template(request):
    """Returns template that forbids defining raw unused variables."""
    return request.param

@pytest.fixture(params=_ALL_FIXTURES - _FORBIDDEN_RAW_UNUSED)
def allowed_raw_unused_template(request):
    """Returns template that allows defining raw unused variables."""
    return request.param

@pytest.fixture(params=_FORBIDDEN_PROTECTED_UNUSED)
def forbidden_protected_unused_template(request):
    """Returns template that forbids defining protected unused variables."""
    return request.param

@pytest.fixture(params=_ALL_FIXTURES - _FORBIDDEN_PROTECTED_UNUSED)
def allowed_protected_unused_template(request):
    """Returns template that allows defining protected unused variables."""
    return request.param