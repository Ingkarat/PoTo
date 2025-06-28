import re
import six
from mock import patch
import invoke
import invoke.collection
import invoke.exceptions
import invoke.tasks
import invoke.program

def Init_dunder_version_info(self):
    assert hasattr(invoke, '__version_info__')
    ver = invoke.__version_info__
    assert isinstance(ver, tuple)
    assert all((isinstance(x, int) for x in ver))

def Init_dunder_version(self):
    assert hasattr(invoke, '__version__')
    ver = invoke.__version__
    assert isinstance(ver, six.string_types)
    assert re.match('\\d+\\.\\d+\\.\\d+', ver)

def Init_dunder_version_looks_generated_from_dunder_version_info(self):
    ver_part = invoke.__version__.split('.')[0]
    ver_info_part = invoke.__version_info__[0]
    assert ver_part == str(ver_info_part)

def exposes_bindings_task_decorator(self):
    assert invoke.task is invoke.tasks.task

def exposes_bindings_task_class(self):
    assert invoke.Task is invoke.tasks.Task

def exposes_bindings_collection_class(self):
    assert invoke.Collection is invoke.collection.Collection

def exposes_bindings_context_class(self):
    assert invoke.Context is invoke.context.Context

def exposes_bindings_mock_context_class(self):
    assert invoke.MockContext is invoke.context.MockContext

def exposes_bindings_config_class(self):
    assert invoke.Config is invoke.config.Config

def exposes_bindings_pty_size_function(self):
    assert invoke.pty_size is invoke.terminals.pty_size

def exposes_bindings_local_class(self):
    assert invoke.Local is invoke.runners.Local

def exposes_bindings_runner_class(self):
    assert invoke.Runner is invoke.runners.Runner

def exposes_bindings_promise_class(self):
    assert invoke.Promise is invoke.runners.Promise

def exposes_bindings_failure_class(self):
    assert invoke.Failure is invoke.runners.Failure

def exposes_bindings_exceptions(self):
    for obj in vars(invoke.exceptions).values():
        if isinstance(obj, type) and issubclass(obj, BaseException):
            top_level = getattr(invoke, obj.__name__)
            real = getattr(invoke.exceptions, obj.__name__)
            assert top_level is real

def exposes_bindings_runner_result(self):
    assert invoke.Result is invoke.runners.Result

def exposes_bindings_watchers(self):
    assert invoke.StreamWatcher is invoke.watchers.StreamWatcher
    assert invoke.Responder is invoke.watchers.Responder
    assert invoke.FailingResponder is invoke.watchers.FailingResponder

def exposes_bindings_program(self):
    assert invoke.Program is invoke.program.Program

def exposes_bindings_filesystemloader(self):
    assert invoke.FilesystemLoader is invoke.loader.FilesystemLoader

def exposes_bindings_argument(self):
    assert invoke.Argument is invoke.parser.Argument

def exposes_bindings_parsercontext(self):
    assert invoke.ParserContext is invoke.parser.ParserContext

def exposes_bindings_parser(self):
    assert invoke.Parser is invoke.parser.Parser

def exposes_bindings_parseresult(self):
    assert invoke.ParseResult is invoke.parser.ParseResult

def exposes_bindings_executor(self):
    assert invoke.Executor is invoke.executor.Executor

def exposes_bindings_call(self):
    assert invoke.call is invoke.tasks.call

def exposes_bindings_Call(self):
    assert invoke.Call is invoke.tasks.Call

@patch('invoke.Context')
def offers_singletons_run(self, Context):
    result = invoke.run('foo', bar='biz')
    ctx = Context.return_value
    ctx.run.assert_called_once_with('foo', bar='biz')
    assert result is ctx.run.return_value

@patch('invoke.Context')
def offers_singletons_sudo(self, Context):
    result = invoke.sudo('foo', bar='biz')
    ctx = Context.return_value
    ctx.sudo.assert_called_once_with('foo', bar='biz')
    assert result is ctx.sudo.return_value