import pytest
from wemake_python_styleguide.compat.constants import PY38
function_with_single_argument = 'def function(arg1): ...'
function_with_arguments = 'def function(arg1, arg2): ...'
function_with_args_kwargs = 'def function(*args, **kwargs): ...'
function_with_kwonly = 'def function(*, kwonly1, kwonly2=True): ...'
function_with_posonly = 'def function(arg1, arg2, /): ...'
method_without_arguments = '\nclass Test(object):\n    def method(self): ...\n'
method_with_single_argument = '\nclass Test(object):\n    def method(self, arg): ...\n'
method_with_single_args = '\nclass Test(object):\n    def method(self, *args): ...\n'
method_with_single_posonly_arg = '\nclass Test(object):\n    def method(self, arg, /): ...\n'
method_with_single_kwargs = '\nclass Test(object):\n    def method(self, **kwargs): ...\n'
method_with_single_kwonly = '\nclass Test(object):\n    def method(self, *, kwonly=True): ...\n'
classmethod_without_arguments = '\nclass Test(object):\n    @classmethod\n    def method(cls): ...\n'
classmethod_with_single_argument = '\nclass Test(object):\n    @classmethod\n    def method(cls, arg1): ...\n'
new_method_without_arguments = '\nclass Test(object):\n    def __new__(cls): ...\n'
new_method_single_argument = '\nclass Test(object):\n    def __new__(cls, arg1): ...\n'
metaclass_without_arguments = '\nclass TestMeta(type):\n    def method(cls): ...\n'
metaclass_with_single_argument = '\nclass TestMeta(type):\n    def method(cls, arg1): ...\n'

@pytest.fixture(params=[function_with_single_argument, method_without_arguments, classmethod_without_arguments, new_method_without_arguments, metaclass_without_arguments])
def single_argument(request):
    """Fixture that returns different code examples that have one arg."""
    return request.param

@pytest.fixture(params=[function_with_arguments, function_with_args_kwargs, function_with_kwonly, pytest.param(function_with_posonly, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), method_with_single_argument, method_with_single_args, method_with_single_kwargs, method_with_single_kwonly, pytest.param(method_with_single_posonly_arg, marks=pytest.mark.skipif(not PY38, reason='posonly appeared in 3.8')), classmethod_with_single_argument, new_method_single_argument, metaclass_with_single_argument])
def two_arguments(request):
    """Fixture that returns different code examples that have two args."""
    return request.param