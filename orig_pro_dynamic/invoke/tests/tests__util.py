import os
import sys
try:
    import termios
except ImportError:
    termios = None
from contextlib import contextmanager
from invoke.vendor.six import BytesIO, b, wraps
from mock import patch, Mock
from pytest import skip
from pytest_relaxed import trap
from invoke import Program, Runner
from invoke.terminals import WINDOWS
support = os.path.join(os.path.dirname(__file__), '_support')
ROOT = os.path.abspath(os.path.sep)

def skip_if_windows(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if WINDOWS:
            skip()
        return fn(*args, **kwargs)
    return wrapper

@contextmanager
def support_path():
    sys.path.insert(0, support)
    try:
        yield
    finally:
        sys.path.pop(0)

def load(name):
    with support_path():
        imported = __import__(name)
        return imported

def support_file(subpath):
    with open(os.path.join(support, subpath)) as fd:
        return fd.read()

@trap
def run(invocation, program=None, invoke=True):
    """
    Run ``invocation`` via ``program``, returning output stream captures.

    ``program`` defaults to ``Program()``.

    To skip automatically assuming the argv under test starts with ``"invoke
    "``, say ``invoke=False``.

    :returns: Two-tuple of ``stdout, stderr`` strings.
    """
    if program is None:
        program = Program()
    if invoke:
        invocation = 'invoke {}'.format(invocation)
    program.run(invocation, exit=False)
    return (sys.stdout.getvalue(), sys.stderr.getvalue())

def expect(invocation, out=None, err=None, program=None, invoke=True, test=None):
    """
    Run ``invocation`` via ``program`` and expect resulting output to match.

    May give one or both of ``out``/``err`` (but not neither).

    ``program`` defaults to ``Program()``.

    To skip automatically assuming the argv under test starts with ``"invoke
    "``, say ``invoke=False``.

    To customize the operator used for testing (default: equality), use
    ``test`` (which should be an assertion wrapper of some kind).
    """
    (stdout, stderr) = run(invocation, program, invoke)
    if out is not None:
        if test:
            test(stdout, out)
        else:
            assert out == stdout
    if err is not None:
        if test:
            test(stderr, err)
        else:
            assert err == stderr
    elif stderr:
        assert False, 'Unexpected stderr: {}'.format(stderr)
    return (stdout, stderr)

def mock_subprocess(out='', err='', exit=0, isatty=None, insert_Popen=False):

    def decorator(f):

        @wraps(f)
        @patch('invoke.runners.pty')
        def wrapper(*args, **kwargs):
            proc = MockSubprocess(out=out, err=err, exit=exit, isatty=isatty, autostart=False)
            Popen = proc.start()
            args = list(args)
            args.pop()
            if insert_Popen:
                args.append(Popen)
            try:
                f(*args, **kwargs)
            finally:
                proc.stop()
        return wrapper
    return decorator

def mock_pty(out='', err='', exit=0, isatty=None, trailing_error=None, skip_asserts=False, insert_os=False, be_childish=False, os_close_error=False):
    if WINDOWS:
        return skip_if_windows

    def decorator(f):
        import fcntl
        ioctl_patch = patch('invoke.runners.fcntl.ioctl', wraps=fcntl.ioctl)

        @wraps(f)
        @patch('invoke.runners.pty')
        @patch('invoke.runners.os')
        @ioctl_patch
        def wrapper(*args, **kwargs):
            args = list(args)
            (pty, os, ioctl) = (args.pop(), args.pop(), args.pop())
            pty.fork.return_value = (12345 if be_childish else 0, 3)
            os.waitpid.return_value = (None, Mock(name='exitstatus'))
            os.WEXITSTATUS.return_value = exit
            os.WTERMSIG.return_value = exit
            if isatty is not None:
                os.isatty.return_value = isatty
            out_file = BytesIO(b(out))
            err_file = BytesIO(b(err))

            def fakeread(fileno, count):
                fd = {3: out_file, 2: err_file}[fileno]
                ret = fd.read(count)
                if not ret and trailing_error:
                    raise trailing_error
                return ret
            os.read.side_effect = fakeread
            if os_close_error:
                os.close.side_effect = IOError
            if insert_os:
                args.append(os)
            f(*args, **kwargs)
            if trailing_error:
                return
            pty.fork.assert_called_with()
            if be_childish:
                return
            assert ioctl.call_args_list[0][0][1] == termios.TIOCGWINSZ
            assert ioctl.call_args_list[1][0][1] == termios.TIOCSWINSZ
            if not skip_asserts:
                for name in ('execve', 'waitpid'):
                    assert getattr(os, name).called
                assert os.WEXITSTATUS.called or os.WTERMSIG.called
                os.close.assert_called_once_with(3)
        return wrapper
    return decorator
_ = 'nope'

def MockSubprocess___init__(self, out='', err='', exit=0, isatty=None, autostart=True):
    self.out_file = BytesIO(b(out))
    self.err_file = BytesIO(b(err))
    self.exit = exit
    self.isatty = isatty
    if autostart:
        self.start()

def MockSubprocess_start(self):
    self.popen = patch('invoke.runners.Popen')
    Popen = patch('invoke.runners.Popen').start()
    self.read = patch('os.read')
    read = patch('os.read').start()
    self.sys_stdin = patch('sys.stdin', new_callable=BytesIO)
    sys_stdin = patch('sys.stdin', new_callable=BytesIO).start()
    process = Popen.return_value
    process.returncode = self.exit
    process.stdout.fileno.return_value = 1
    process.stderr.fileno.return_value = 2
    if self.isatty is not None:
        sys_stdin.isatty = Mock(return_value=self.isatty)

    def fakeread(fileno, count):
        fd = {1: self.out_file, 2: self.err_file}[fileno]
        return fd.read(count)
    read.side_effect = fakeread
    return Popen

def MockSubprocess_stop(self):
    patch('invoke.runners.Popen').stop()
    patch('os.read').stop()
    patch('sys.stdin', new_callable=BytesIO).stop()

def _Dummy_start(self, command, shell, env, timeout=None):
    pass

def _Dummy_read_proc_stdout(self, num_bytes):
    return ''

def _Dummy_read_proc_stderr(self, num_bytes):
    return ''

def _Dummy__write_proc_stdin(self, data):
    pass

def _Dummy_close_proc_stdin(self):
    pass

@property
def _Dummy_process_is_finished(self):
    return True

def _Dummy_returncode(self):
    return 0

def _Dummy_stop(self):
    pass

@property
def _Dummy_timed_out(self):
    return False

def _KeyboardInterruptingRunner___init__(self, *args, **kwargs):
    super(_KeyboardInterruptingRunner, self).__init__(*args, **kwargs)
    self._interrupted = False

def _KeyboardInterruptingRunner_wait(self):
    if not self._interrupted:
        self._interrupted = True
        raise KeyboardInterrupt

def _KeyboardInterruptingRunner_process_is_finished(self):
    return self._interrupted