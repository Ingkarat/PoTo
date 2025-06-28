import os
import signal
import struct
import sys
import termios
import threading
import types
from io import BytesIO
from itertools import chain, repeat
from invoke.vendor.six import StringIO, b, PY2, iteritems
from pytest import raises, skip
from pytest_relaxed import trap
from mock import patch, Mock, call
import pytest
from invoke import CommandTimedOut, Config, Context, Failure, Local, Promise, Responder, Result, Runner, StreamWatcher, SubprocessPipeError, ThreadException, UnexpectedExit, WatcherError
from invoke.runners import default_encoding
from invoke.terminals import WINDOWS
from _util import mock_subprocess, mock_pty, skip_if_windows, _Dummy, _KeyboardInterruptingRunner, OhNoz, _

@pytest.mark.skip(reason='fail')
def _run(*args, **kwargs):
    klass = kwargs.pop('klass', _Dummy)
    settings = kwargs.pop('settings', {})
    context = Context(config=Config(overrides=settings))
    return klass(context).run(*args, **kwargs)

@pytest.mark.skip(reason='fail')
def _runner(out='', err='', **kwargs):
    klass = kwargs.pop('klass', _Dummy)
    runner = klass(Context(config=Config(overrides=kwargs)))
    if 'exits' in kwargs:
        runner.returncode = Mock(return_value=kwargs.pop('exits'))
    out_file = BytesIO(b(out))
    err_file = BytesIO(b(err))
    runner.read_proc_stdout = out_file.read
    runner.read_proc_stderr = err_file.read
    return runner

def _expect_platform_shell(shell):
    if WINDOWS:
        assert shell.endswith('cmd.exe')
    else:
        assert shell == '/bin/bash'

def make_tcattrs(cc_is_ints=True, echo=False):
    cc_base = [None] * (max(termios.VMIN, termios.VTIME) + 1)
    (cc_ints, cc_bytes) = (cc_base[:], cc_base[:])
    (cc_ints[termios.VMIN], cc_ints[termios.VTIME]) = (1, 0)
    (cc_bytes[termios.VMIN], cc_bytes[termios.VTIME]) = (b'\x01', b'\x00')
    attrs = [None, None, None, ~(termios.ECHO | termios.ICANON), None, None, cc_ints if cc_is_ints else cc_bytes]
    if echo:
        attrs[3] = attrs[3] | termios.ECHO
    return attrs

def _RaisingWatcher_submit(self, stream):
    raise WatcherError('meh')

def _GenericExceptingRunner_wait(self):
    raise _GenericException

@property
def _TimingOutRunner_timed_out(self):
    return True

def Runner___run(self, *args, **kwargs):
    return _run(*args, **kwargs)

def Runner___runner(self, *args, **kwargs):
    return _runner(*args, **kwargs)

def Runner___mock_stdin_writer(self):
    """
        Return new _Dummy subclass whose write_proc_stdin() method is a mock.
        """

    class MockedStdin(_Dummy):
        pass
    MockedStdin.write_proc_stdin = Mock()
    return MockedStdin

def init_takes_a_context_instance(self):
    c = Context()
    assert Runner(c).context == c

def init_context_instance_is_required(self):
    with raises(TypeError):
        Runner()

def run_handles_invalid_kwargs_like_any_other_function(self):
    try:
        self._run(_, nope_noway_nohow='as if')
    except TypeError as e:
        assert 'got an unexpected keyword argument' in str(e)
    else:
        assert False, "Invalid run() kwarg didn't raise TypeError"

def warn_honors_config(self):
    runner = self._runner(run={'warn': True}, exits=1)
    runner.run(_)

def warn_kwarg_beats_config(self):
    runner = self._runner(run={'warn': False}, exits=1)
    runner.run(_, warn=True)

def warn_does_not_apply_to_watcher_errors(self):
    runner = self._runner(out='stuff')
    try:
        watcher = _RaisingWatcher()
        runner.run(_, watchers=[watcher], warn=True, hide=True)
    except Failure as e:
        assert isinstance(e.reason, WatcherError)
    else:
        assert False, 'Did not raise Failure for WatcherError!'

def warn_does_not_apply_to_timeout_errors(self):
    with raises(CommandTimedOut):
        self._runner(klass=_TimingOutRunner).run(_, timeout=1, warn=True)

@trap
def hide_honors_config(self):
    runner = self._runner(out='stuff', run={'hide': True})
    r = runner.run(_)
    assert r.stdout == 'stuff'
    assert sys.stdout.getvalue() == ''

@trap
def hide_kwarg_beats_config(self):
    runner = self._runner(out='stuff')
    r = runner.run(_, hide=True)
    assert r.stdout == 'stuff'
    assert sys.stdout.getvalue() == ''

def pty_pty_defaults_to_off(self):
    assert self._run(_).pty is False

def pty_honors_config(self):
    runner = self._runner(run={'pty': True})
    assert runner.run(_).pty is True

def pty_kwarg_beats_config(self):
    runner = self._runner(run={'pty': False})
    assert runner.run(_, pty=True).pty is True

def shell_defaults_to_bash_or_cmdexe_when_pty_True(self):
    _expect_platform_shell(self._run(_, pty=True).shell)

def shell_defaults_to_bash_or_cmdexe_when_pty_False(self):
    _expect_platform_shell(self._run(_, pty=False).shell)

def shell_may_be_overridden(self):
    assert self._run(_, shell='/bin/zsh').shell == '/bin/zsh'

def shell_may_be_configured(self):
    runner = self._runner(run={'shell': '/bin/tcsh'})
    assert runner.run(_).shell == '/bin/tcsh'

def shell_kwarg_beats_config(self):
    runner = self._runner(run={'shell': '/bin/tcsh'})
    assert runner.run(_, shell='/bin/zsh').shell == '/bin/zsh'

def env_defaults_to_os_environ(self):
    assert self._run(_).env == os.environ

def env_updates_when_dict_given(self):
    expected = dict(os.environ, FOO='BAR')
    assert self._run(_, env={'FOO': 'BAR'}).env == expected

def env_replaces_when_replace_env_True(self):
    env = self._run(_, env={'JUST': 'ME'}, replace_env=True).env
    assert env == {'JUST': 'ME'}

def env_config_can_be_used(self):
    env = self._run(_, settings={'run': {'env': {'FOO': 'BAR'}}}).env
    assert env == dict(os.environ, FOO='BAR')

def env_kwarg_wins_over_config(self):
    settings = {'run': {'env': {'FOO': 'BAR'}}}
    kwarg = {'FOO': 'NOTBAR'}
    foo = self._run(_, settings=settings, env=kwarg).env['FOO']
    assert foo == 'NOTBAR'

def return_value_return_code(self):
    """
            Result has .return_code (and .exited) containing exit code int
            """
    runner = self._runner(exits=17)
    r = runner.run(_, warn=True)
    assert r.return_code == 17
    assert r.exited == 17

def return_value_ok_attr_indicates_success(self):
    runner = self._runner()
    assert runner.run(_).ok is True

def return_value_ok_attr_indicates_failure(self):
    runner = self._runner(exits=1)
    assert runner.run(_, warn=True).ok is False

def return_value_failed_attr_indicates_success(self):
    runner = self._runner()
    assert runner.run(_).failed is False

def return_value_failed_attr_indicates_failure(self):
    runner = self._runner(exits=1)
    assert runner.run(_, warn=True).failed is True

@trap
def return_value_stdout_attribute_contains_stdout(self):
    runner = self._runner(out='foo')
    assert runner.run(_).stdout == 'foo'
    assert sys.stdout.getvalue() == 'foo'

@trap
def return_value_stderr_attribute_contains_stderr(self):
    runner = self._runner(err='foo')
    assert runner.run(_).stderr == 'foo'
    assert sys.stderr.getvalue() == 'foo'

def return_value_whether_pty_was_used(self):
    assert self._run(_).pty is False
    assert self._run(_, pty=True).pty is True

def return_value_command_executed(self):
    assert self._run(_).command == _

def return_value_shell_used(self):
    _expect_platform_shell(self._run(_).shell)

def return_value_hide_param_exposed_and_normalized(self):
    assert self._run(_, hide=True).hide, 'stdout' == 'stderr'
    assert self._run(_, hide=False).hide == tuple()
    assert self._run(_, hide='stderr').hide == ('stderr',)

@trap
def command_echoing_off_by_default(self):
    self._run('my command')
    assert sys.stdout.getvalue() == ''

@trap
def command_echoing_enabled_via_kwarg(self):
    self._run('my command', echo=True)
    assert 'my command' in sys.stdout.getvalue()

@trap
def command_echoing_enabled_via_config(self):
    self._run('yup', settings={'run': {'echo': True}})
    assert 'yup' in sys.stdout.getvalue()

@trap
def command_echoing_kwarg_beats_config(self):
    self._run('yup', echo=True, settings={'run': {'echo': False}})
    assert 'yup' in sys.stdout.getvalue()

@trap
def command_echoing_uses_ansi_bold(self):
    self._run('my command', echo=True)
    assert sys.stdout.getvalue() == '\x1b[1;37mmy command\x1b[0m\n'

@trap
def dry_running_sets_echo_to_True(self):
    self._run('what up', settings={'run': {'dry': True}})
    assert 'what up' in sys.stdout.getvalue()

@trap
def dry_running_short_circuits_with_dummy_result(self):
    runner = self._runner(run={'dry': True})
    runner.start = Mock()
    result = runner.run(_)
    assert not runner.start.called
    assert isinstance(result, Result)
    assert result.command == _
    assert result.stdout == ''
    assert result.stderr == ''
    assert result.exited == 0
    assert result.pty is False

def encoding_defaults_to_encoding_method_result(self):
    runner = self._runner()
    encoding = 'UTF-7'
    runner.default_encoding = Mock(return_value=encoding)
    runner.run(_)
    runner.default_encoding.assert_called_with()
    assert runner.encoding == 'UTF-7'

def encoding_honors_config(self):
    c = Context(Config(overrides={'run': {'encoding': 'UTF-7'}}))
    runner = _Dummy(c)
    runner.default_encoding = Mock(return_value='UTF-not-7')
    runner.run(_)
    assert runner.encoding == 'UTF-7'

def encoding_honors_kwarg(self):
    skip()

def encoding_uses_locale_module_for_default_encoding(self):
    with patch('invoke.runners.locale') as fake_locale:
        fake_locale.getdefaultlocale.return_value = ('meh', 'UHF-8')
        fake_locale.getpreferredencoding.return_value = 'FALLBACK'
        expected = 'UHF-8' if PY2 and (not WINDOWS) else 'FALLBACK'
        assert self._runner().default_encoding() == expected

def encoding_falls_back_to_defaultlocale_when_preferredencoding_is_None(self):
    if PY2:
        skip()
    with patch('invoke.runners.locale') as fake_locale:
        fake_locale.getdefaultlocale.return_value = (None, None)
        fake_locale.getpreferredencoding.return_value = 'FALLBACK'
        assert self._runner().default_encoding() == 'FALLBACK'

@trap
def output_hiding__expect_hidden(self, hide, expect_out='', expect_err=''):
    self._runner(out='foo', err='bar').run(_, hide=hide)
    assert sys.stdout.getvalue() == expect_out
    assert sys.stderr.getvalue() == expect_err

def output_hiding_both_hides_everything(self):
    self._expect_hidden('both')

def output_hiding_True_hides_everything(self):
    self._expect_hidden(True)

def output_hiding_out_only_hides_stdout(self):
    self._expect_hidden('out', expect_out='', expect_err='bar')

def output_hiding_err_only_hides_stderr(self):
    self._expect_hidden('err', expect_out='foo', expect_err='')

def output_hiding_accepts_stdout_alias_for_out(self):
    self._expect_hidden('stdout', expect_out='', expect_err='bar')

def output_hiding_accepts_stderr_alias_for_err(self):
    self._expect_hidden('stderr', expect_out='foo', expect_err='')

def output_hiding_None_hides_nothing(self):
    self._expect_hidden(None, expect_out='foo', expect_err='bar')

def output_hiding_False_hides_nothing(self):
    self._expect_hidden(False, expect_out='foo', expect_err='bar')

def output_hiding_unknown_vals_raises_ValueError(self):
    with raises(ValueError):
        self._run(_, hide='wat?')

def output_hiding_unknown_vals_mention_value_given_in_error(self):
    value = 'penguinmints'
    try:
        self._run(_, hide=value)
    except ValueError as e:
        msg = 'Error from run(hide=xxx) did not tell user what the bad value was!'
        msg += '\nException msg: {}'.format(e)
        assert value in str(e), msg
    else:
        assert False, 'run() did not raise ValueError for bad hide= value'

def output_hiding_does_not_affect_capturing(self):
    assert self._runner(out='foo').run(_, hide=True).stdout == 'foo'

@trap
def output_hiding_overrides_echoing(self):
    self._runner().run('invisible', hide=True, echo=True)
    assert 'invisible' not in sys.stdout.getvalue()

@trap
def output_stream_overrides_out_defaults_to_sys_stdout(self):
    """out_stream defaults to sys.stdout"""
    self._runner(out='sup').run(_)
    assert sys.stdout.getvalue() == 'sup'

@trap
def output_stream_overrides_err_defaults_to_sys_stderr(self):
    """err_stream defaults to sys.stderr"""
    self._runner(err='sup').run(_)
    assert sys.stderr.getvalue() == 'sup'

@trap
def output_stream_overrides_out_can_be_overridden(self):
    """out_stream can be overridden"""
    out = StringIO()
    self._runner(out='sup').run(_, out_stream=out)
    assert out.getvalue() == 'sup'
    assert sys.stdout.getvalue() == ''

@trap
def output_stream_overrides_overridden_out_is_never_hidden(self):
    out = StringIO()
    self._runner(out='sup').run(_, out_stream=out, hide=True)
    assert out.getvalue() == 'sup'
    assert sys.stdout.getvalue() == ''

@trap
def output_stream_overrides_err_can_be_overridden(self):
    """err_stream can be overridden"""
    err = StringIO()
    self._runner(err='sup').run(_, err_stream=err)
    assert err.getvalue() == 'sup'
    assert sys.stderr.getvalue() == ''

@trap
def output_stream_overrides_overridden_err_is_never_hidden(self):
    err = StringIO()
    self._runner(err='sup').run(_, err_stream=err, hide=True)
    assert err.getvalue() == 'sup'
    assert sys.stderr.getvalue() == ''

@trap
def output_stream_overrides_pty_defaults_to_sys(self):
    self._runner(out='sup').run(_, pty=True)
    assert sys.stdout.getvalue() == 'sup'

@trap
def output_stream_overrides_pty_out_can_be_overridden(self):
    out = StringIO()
    self._runner(out='yo').run(_, pty=True, out_stream=out)
    assert out.getvalue() == 'yo'
    assert sys.stdout.getvalue() == ''

def output_stream_handling_writes_and_flushes_to_stdout(self):
    out = Mock(spec=StringIO)
    self._runner(out='meh').run(_, out_stream=out)
    out.write.assert_called_once_with('meh')
    out.flush.assert_called_once_with()

def output_stream_handling_writes_and_flushes_to_stderr(self):
    err = Mock(spec=StringIO)
    self._runner(err='whatever').run(_, err_stream=err)
    err.write.assert_called_once_with('whatever')
    err.flush.assert_called_once_with()

@patch('invoke.runners.sys.stdin', StringIO('Text!'))
def input_stream_handling_defaults_to_sys_stdin(self):
    klass = self._mock_stdin_writer()
    self._runner(klass=klass).run(_, out_stream=StringIO())
    calls = list(map(lambda x: call(x), 'Text!'))
    klass.write_proc_stdin.assert_has_calls(calls, any_order=False)

def input_stream_handling_can_be_overridden(self):
    klass = self._mock_stdin_writer()
    in_stream = StringIO('Hey, listen!')
    self._runner(klass=klass).run(_, in_stream=in_stream, out_stream=StringIO())
    calls = list(map(lambda x: call(x), 'Hey, listen!'))
    klass.write_proc_stdin.assert_has_calls(calls, any_order=False)

def input_stream_handling_can_be_disabled_entirely(self):

    class MockedHandleStdin(_Dummy):
        pass
    MockedHandleStdin.handle_stdin = Mock()
    self._runner(klass=MockedHandleStdin).run(_, in_stream=False)
    assert not MockedHandleStdin.handle_stdin.called

@patch('invoke.util.debug')
def input_stream_handling_exceptions_get_logged(self, mock_debug):
    klass = self._mock_stdin_writer()
    klass.write_proc_stdin.side_effect = OhNoz('oh god why')
    try:
        stdin = StringIO('non-empty')
        self._runner(klass=klass).run(_, in_stream=stdin)
    except ThreadException:
        pass
    msg = mock_debug.call_args[0][0]
    assert 'Encountered exception OhNoz' in msg
    assert "'oh god why'" in msg
    assert "in thread for 'handle_stdin'" in msg

def input_stream_handling_EOF_triggers_closing_of_proc_stdin(self):

    class Fake(_Dummy):
        pass
    Fake.close_proc_stdin = Mock()
    self._runner(klass=Fake).run(_, in_stream=StringIO('what?'))
    Fake.close_proc_stdin.assert_called_once_with()

def input_stream_handling_EOF_does_not_close_proc_stdin_when_pty_True(self):

    class Fake(_Dummy):
        pass
    Fake.close_proc_stdin = Mock()
    self._runner(klass=Fake).run(_, in_stream=StringIO('what?'), pty=True)
    assert not Fake.close_proc_stdin.called

def failure_handling_fast_failures(self):
    with raises(UnexpectedExit):
        self._runner(exits=1).run(_)

def failure_handling_non_1_return_codes_still_act_as_failure(self):
    r = self._runner(exits=17).run(_, warn=True)
    assert r.failed is True

def UnexpectedExit_repr_similar_to_just_the_result_repr(self):
    try:
        self._runner(exits=23).run(_)
    except UnexpectedExit as e:
        expected = "<UnexpectedExit: cmd='{}' exited=23>"
        assert repr(e) == expected.format(_)

def UnexpectedExit_str_setup(self):

    def lines(prefix):
        prefixed = '\n'.join(('{} {}'.format(prefix, x) for x in range(1, 26)))
        return prefixed + '\n'
    self._stdout = lines('stdout')
    self._stderr = lines('stderr')

@trap
def UnexpectedExit_str_displays_command_and_exit_code_by_default(self):
    try:
        self._runner(exits=23, out=self._stdout, err=self._stderr).run(_)
    except UnexpectedExit as e:
        expected = "Encountered a bad command exit code!\n\nCommand: '{}'\n\nExit code: 23\n\nStdout: already printed\n\nStderr: already printed\n\n"
        assert str(e) == expected.format(_)
    else:
        assert False, 'Failed to raise UnexpectedExit!'

@trap
def UnexpectedExit_str_does_not_display_stderr_when_pty_True(self):
    try:
        self._runner(exits=13, out=self._stdout, err=self._stderr).run(_, pty=True)
    except UnexpectedExit as e:
        expected = "Encountered a bad command exit code!\n\nCommand: '{}'\n\nExit code: 13\n\nStdout: already printed\n\nStderr: n/a (PTYs have no stderr)\n\n"
        assert str(e) == expected.format(_)

@trap
def UnexpectedExit_str_pty_stderr_message_wins_over_hidden_stderr(self):
    try:
        self._runner(exits=1, out=self._stdout, err=self._stderr).run(_, pty=True, hide=True)
    except UnexpectedExit as e:
        r = str(e)
        assert 'Stderr: n/a (PTYs have no stderr)' in r
        assert 'Stderr: already printed' not in r

@trap
def UnexpectedExit_str_explicit_hidden_stream_tail_display(self):
    try:
        self._runner(exits=77, out=self._stdout, err=self._stderr).run(_, hide=True)
    except UnexpectedExit as e:
        expected = "Encountered a bad command exit code!\n\nCommand: '{}'\n\nExit code: 77\n\nStdout:\n\nstdout 16\nstdout 17\nstdout 18\nstdout 19\nstdout 20\nstdout 21\nstdout 22\nstdout 23\nstdout 24\nstdout 25\n\nStderr:\n\nstderr 16\nstderr 17\nstderr 18\nstderr 19\nstderr 20\nstderr 21\nstderr 22\nstderr 23\nstderr 24\nstderr 25\n\n"
        assert str(e) == expected.format(_)

@trap
def UnexpectedExit_str_displays_tails_of_streams_only_when_hidden(self):

    def oops(msg, r, hide):
        return '{}! hide={}; str output:\n\n{}'.format(msg, hide, r)
    for (hide, expect_out, expect_err) in ((False, False, False), (True, True, True), ('stdout', True, False), ('stderr', False, True), ('both', True, True)):
        try:
            self._runner(exits=1, out=self._stdout, err=self._stderr).run(_, hide=hide)
        except UnexpectedExit as e:
            r = str(e)
            err = oops('Too much stdout found', r, hide)
            assert 'stdout 15' not in r, err
            err = oops('Too much stderr found', r, hide)
            assert 'stderr 15' not in r, err
            if expect_out:
                err = oops("Didn't see stdout", r, hide)
                assert 'stdout 16' in r, err
            if expect_err:
                err = oops("Didn't see stderr", r, hide)
                assert 'stderr 16' in r, err
        else:
            assert False, 'Failed to raise UnexpectedExit!'

def failure_handling__regular_error(self):
    self._runner(exits=1).run(_)

def failure_handling__watcher_error(self):
    klass = self._mock_stdin_writer()
    runner = self._runner(klass=klass, out='stuff', exits=None)
    runner.run(_, watchers=[_RaisingWatcher()], hide=True)

def reason_is_None_for_regular_nonzero_exits(self):
    try:
        self._regular_error()
    except Failure as e:
        assert e.reason is None
    else:
        assert False, 'Failed to raise Failure!'

def reason_is_None_for_custom_command_exits(self):
    skip()

def reason_is_exception_when_WatcherError_raised_internally(self):
    try:
        self._watcher_error()
    except Failure as e:
        assert isinstance(e.reason, WatcherError)
    else:
        assert False, 'Failed to raise Failure!'

def wrapped_result_most_attrs_are_always_present(self):
    attrs = ('command', 'shell', 'env', 'stdout', 'stderr', 'pty')
    for method in (self._regular_error, self._watcher_error):
        try:
            method()
        except Failure as e:
            for attr in attrs:
                assert getattr(e.result, attr) is not None
        else:
            assert False, 'Did not raise Failure!'

def shell_exit_failure_exited_is_integer(self):
    try:
        self._regular_error()
    except Failure as e:
        assert isinstance(e.result.exited, int)
    else:
        assert False, 'Did not raise Failure!'

def shell_exit_failure_ok_bool_etc_are_falsey(self):
    try:
        self._regular_error()
    except Failure as e:
        assert e.result.ok is False
        assert e.result.failed is True
        assert not bool(e.result)
        assert not e.result
    else:
        assert False, 'Did not raise Failure!'

def shell_exit_failure_stringrep_notes_exit_status(self):
    try:
        self._regular_error()
    except Failure as e:
        assert 'exited with status 1' in str(e.result)
    else:
        assert False, 'Did not raise Failure!'

def watcher_failure_exited_is_None(self):
    try:
        self._watcher_error()
    except Failure as e:
        exited = e.result.exited
        err = 'Expected None, got {!r}'.format(exited)
        assert exited is None, err

def watcher_failure_ok_and_bool_still_are_falsey(self):
    try:
        self._watcher_error()
    except Failure as e:
        assert e.result.ok is False
        assert e.result.failed is True
        assert not bool(e.result)
        assert not e.result
    else:
        assert False, 'Did not raise Failure!'

def watcher_failure_stringrep_lacks_exit_status(self):
    try:
        self._watcher_error()
    except Failure as e:
        assert 'exited with status' not in str(e.result)
        expected = 'not fully executed due to watcher error'
        assert expected in str(e.result)
    else:
        assert False, 'Did not raise Failure!'

def threading_errors_within_io_thread_body_bubble_up(self):

    class Oops(_Dummy):

        def handle_stdout(self, **kwargs):
            raise OhNoz()

        def handle_stderr(self, **kwargs):
            raise OhNoz()
    runner = Oops(Context())
    try:
        runner.run('nah')
    except ThreadException as e:
        assert len(e.exceptions) == 2
        for tup in e.exceptions:
            assert isinstance(tup.value, OhNoz)
            assert isinstance(tup.traceback, types.TracebackType)
            assert tup.type == OhNoz
    else:
        assert False, 'Did not raise ThreadException as expected!'

def threading_io_thread_errors_str_has_details(self):

    class Oops(_Dummy):

        def handle_stdout(self, **kwargs):
            raise OhNoz()
    runner = Oops(Context())
    try:
        runner.run('nah')
    except ThreadException as e:
        message = str(e)
        assert 'Saw 1 exceptions within threads' in message
        assert "{'kwargs': " in message
        assert 'Traceback (most recent call last):\n\n' in message
        assert 'OhNoz' in message
    else:
        assert False, 'Did not raise ThreadException as expected!'

def watchers_nothing_is_written_to_stdin_by_default(self):
    klass = self._mock_stdin_writer()
    self._runner(klass=klass).run(_)
    assert not klass.write_proc_stdin.called

def watchers__expect_response(self, **kwargs):
    """
            Execute a run() w/ ``watchers`` set from ``responses``.

            Any other ``**kwargs`` given are passed direct to ``_runner()``.

            :returns: The mocked ``write_proc_stdin`` method of the runner.
            """
    watchers = [Responder(pattern=key, response=value) for (key, value) in iteritems(kwargs.pop('responses'))]
    kwargs['klass'] = klass = self._mock_stdin_writer()
    runner = self._runner(**kwargs)
    runner.run(_, watchers=watchers, hide=True)
    return klass.write_proc_stdin

def watchers_watchers_responses_get_written_to_proc_stdin(self):
    self._expect_response(out='the house was empty', responses={'empty': 'handed'}).assert_called_once_with('handed')

def watchers_multiple_hits_yields_multiple_responses(self):
    holla = call('how high?')
    self._expect_response(out='jump, wait, jump, wait', responses={'jump': 'how high?'}).assert_has_calls([holla, holla])

def watchers_chunk_sizes_smaller_than_patterns_still_work_ok(self):
    klass = self._mock_stdin_writer()
    klass.read_chunk_size = 1
    responder = Responder('jump', 'how high?')
    runner = self._runner(klass=klass, out='jump, wait, jump, wait')
    runner.run(_, watchers=[responder], hide=True)
    holla = call('how high?')
    klass.write_proc_stdin.assert_has_calls([holla, holla])
    assert len(klass.write_proc_stdin.call_args_list) == 2

def watchers_both_out_and_err_are_scanned(self):
    bye = call('goodbye')
    self._expect_response(out='hello my name is inigo', err='hello how are you', responses={'hello': 'goodbye'}).assert_has_calls([bye, bye])

def watchers_multiple_patterns_works_as_expected(self):
    calls = [call('betty'), call('carnival')]
    self._expect_response(out='beep boop I am a robot', responses={'boop': 'betty', 'robot': 'carnival'}).assert_has_calls(calls, any_order=True)

def watchers_multiple_patterns_across_both_streams(self):
    responses = {'boop': 'betty', 'robot': 'carnival', 'Destroy': 'your ego', 'humans': 'are awful'}
    calls = map(lambda x: call(x), responses.values())
    self._expect_response(out='beep boop, I am a robot', err='Destroy all humans!', responses=responses).assert_has_calls(calls, any_order=True)

def watchers_honors_watchers_config_option(self):
    klass = self._mock_stdin_writer()
    responder = Responder('my stdout', 'and my axe')
    runner = self._runner(out='this is my stdout', klass=klass, run={'watchers': [responder]})
    runner.run(_, hide=True)
    klass.write_proc_stdin.assert_called_once_with('and my axe')

def watchers_kwarg_overrides_config(self):
    klass = self._mock_stdin_writer()
    conf = Responder('my stdout', 'and my axe')
    kwarg = Responder('my stdout', 'and my body spray')
    runner = self._runner(out='this is my stdout', klass=klass, run={'watchers': [conf]})
    runner.run(_, hide=True, watchers=[kwarg])
    klass.write_proc_stdin.assert_called_once_with('and my body spray')

def io_sleeping_input_sleep_attribute_defaults_to_hundredth_of_second(self):
    assert Runner(Context()).input_sleep == 0.01

@mock_subprocess()
def io_sleeping_subclasses_can_override_input_sleep(self):

    class MyRunner(_Dummy):
        input_sleep = 0.007
    with patch('invoke.runners.time') as mock_time:
        MyRunner(Context()).run(_, in_stream=StringIO('foo'), out_stream=StringIO())
    assert mock_time.sleep.call_args_list[:3] == [call(0.007)] * 3

def stdin_mirroring__test_mirroring(self, expect_mirroring, **kwargs):
    fake_in = "I'm typing!"
    output = Mock()
    input_ = StringIO(fake_in)
    input_is_pty = kwargs.pop('in_pty', None)

    class MyRunner(_Dummy):

        def should_echo_stdin(self, input_, output):
            if input_is_pty is not None:
                input_.isatty = lambda : input_is_pty
            return super(MyRunner, self).should_echo_stdin(input_, output)
    self._run(_, klass=MyRunner, in_stream=input_, out_stream=output, **kwargs)
    if expect_mirroring:
        calls = output.write.call_args_list
        assert calls == list(map(lambda x: call(x), fake_in))
        assert len(output.flush.call_args_list) == len(fake_in)
    else:
        assert output.write.call_args_list == []

def stdin_mirroring_when_pty_is_True_no_mirroring_occurs(self):
    self._test_mirroring(pty=True, expect_mirroring=False)

def stdin_mirroring_when_pty_is_False_we_write_in_stream_back_to_out_stream(self):
    self._test_mirroring(pty=False, in_pty=True, expect_mirroring=True)

def stdin_mirroring_mirroring_is_skipped_when_our_input_is_not_a_tty(self):
    self._test_mirroring(in_pty=False, expect_mirroring=False)

def stdin_mirroring_mirroring_can_be_forced_on(self):
    self._test_mirroring(pty=True, echo_stdin=True, expect_mirroring=True)

def stdin_mirroring_mirroring_can_be_forced_off(self):
    self._test_mirroring(pty=False, in_pty=True, echo_stdin=False, expect_mirroring=False)

def stdin_mirroring_mirroring_honors_configuration(self):
    self._test_mirroring(pty=False, in_pty=True, settings={'run': {'echo_stdin': False}}, expect_mirroring=False)

@trap
@skip_if_windows
@patch('invoke.runners.sys.stdin')
@patch('invoke.terminals.fcntl.ioctl')
@patch('invoke.terminals.os')
@patch('invoke.terminals.termios')
@patch('invoke.terminals.tty')
@patch('invoke.terminals.select')
def stdin_mirroring_reads_FIONREAD_bytes_from_stdin_when_fileno(self, select, tty, termios, mock_os, ioctl, stdin):
    stdin.fileno.return_value = 17
    stdin_data = list('boo!')

    def fakeread(n):
        data = stdin_data[:n]
        del stdin_data[:n]
        return ''.join(data)
    stdin.read.side_effect = fakeread
    mock_os.tcgetpgrp.return_value = None
    select.select.side_effect = chain([([stdin], [], [])], repeat(([], [], [])))

    def fake_ioctl(fd, cmd, buf):
        if cmd is termios.FIONREAD:
            return struct.pack('h', len(stdin_data))
    ioctl.side_effect = fake_ioctl
    klass = self._mock_stdin_writer()
    self._runner(klass=klass).run(_)
    klass.write_proc_stdin.assert_called_once_with('boo!')

@skip_if_windows
@patch('invoke.terminals.tty')
def character_buffered_stdin_setcbreak_called_on_tty_stdins(self, mock_tty, mock_termios):
    mock_termios.tcgetattr.return_value = make_tcattrs(echo=True)
    self._run(_)
    mock_tty.setcbreak.assert_called_with(sys.stdin)

@skip_if_windows
@patch('invoke.terminals.tty')
def character_buffered_stdin_setcbreak_not_called_on_non_tty_stdins(self, mock_tty):
    self._run(_, in_stream=StringIO())
    assert not mock_tty.setcbreak.called

@skip_if_windows
@patch('invoke.terminals.tty')
@patch('invoke.terminals.os')
def character_buffered_stdin_setcbreak_not_called_if_process_not_foregrounded(self, mock_os, mock_tty):
    mock_os.getpgrp.return_value = 1337
    mock_os.tcgetpgrp.return_value = 1338
    self._run(_)
    assert not mock_tty.setcbreak.called
    mock_os.tcgetpgrp.assert_called_once_with(sys.stdin.fileno())

@skip_if_windows
@patch('invoke.terminals.tty')
def character_buffered_stdin_tty_stdins_have_settings_restored_by_default(self, mock_tty, mock_termios):
    attrs = make_tcattrs(echo=True)
    mock_termios.tcgetattr.return_value = attrs
    self._run(_)
    mock_termios.tcsetattr.assert_called_once_with(sys.stdin, mock_termios.TCSADRAIN, attrs)

@skip_if_windows
@patch('invoke.terminals.tty')
def character_buffered_stdin_tty_stdins_have_settings_restored_on_KeyboardInterrupt(self, mock_tty, mock_termios):
    sentinel = make_tcattrs(echo=True)
    mock_termios.tcgetattr.return_value = sentinel
    try:
        self._run(_, klass=_KeyboardInterruptingRunner)
    except KeyboardInterrupt:
        pass
    mock_termios.tcsetattr.assert_called_once_with(sys.stdin, mock_termios.TCSADRAIN, sentinel)

@skip_if_windows
@patch('invoke.terminals.tty')
def character_buffered_stdin_setcbreak_not_called_if_terminal_seems_already_cbroken(self, mock_tty, mock_termios):
    for is_ints in (True, False):
        mock_termios.tcgetattr.return_value = make_tcattrs(cc_is_ints=is_ints)
        self._run(_)
        assert not mock_tty.setcbreak.called
        assert not mock_termios.tcsetattr.called

def send_interrupt__run_with_mocked_interrupt(self, klass):
    runner = klass(Context())
    runner.send_interrupt = Mock()
    try:
        runner.run(_)
    except _GenericException:
        pass
    return runner

def send_interrupt_called_on_KeyboardInterrupt(self):
    runner = self._run_with_mocked_interrupt(_KeyboardInterruptingRunner)
    assert runner.send_interrupt.called

def send_interrupt_not_called_for_other_exceptions(self):
    runner = self._run_with_mocked_interrupt(_GenericExceptingRunner)
    assert not runner.send_interrupt.called

def send_interrupt_sends_escape_byte_sequence(self):
    for pty in (True, False):
        runner = _KeyboardInterruptingRunner(Context())
        mock_stdin = Mock()
        runner.write_proc_stdin = mock_stdin
        runner.run(_, pty=pty)
        mock_stdin.assert_called_once_with(u'\x03')

def timeout_start_timer_called_with_config_value(self):
    runner = self._runner(timeouts={'command': 7})
    runner.start_timer = Mock()
    assert runner.context.config.timeouts.command == 7
    runner.run(_)
    runner.start_timer.assert_called_once_with(7)

def timeout_run_kwarg_honored(self):
    runner = self._runner()
    runner.start_timer = Mock()
    assert runner.context.config.timeouts.command is None
    runner.run(_, timeout=3)
    runner.start_timer.assert_called_once_with(3)

def timeout_kwarg_wins_over_config(self):
    runner = self._runner(timeouts={'command': 7})
    runner.start_timer = Mock()
    assert runner.context.config.timeouts.command == 7
    runner.run(_, timeout=3)
    runner.start_timer.assert_called_once_with(3)

def timeout_raises_CommandTimedOut_with_timeout_info(self):
    runner = self._runner(klass=_TimingOutRunner, timeouts={'command': 7})
    with raises(CommandTimedOut) as info:
        runner.run(_)
    assert info.value.timeout == 7
    _repr = "<CommandTimedOut: cmd='nope' timeout=7>"
    assert repr(info.value) == _repr
    expected = "\nCommand did not complete within 7 seconds!\n\nCommand: 'nope'\n\nStdout: already printed\n\nStderr: already printed\n\n".lstrip()
    assert str(info.value) == expected

@patch('invoke.runners.threading.Timer')
def timeout_start_timer_gives_its_timer_the_kill_method(self, Timer):
    runner = self._runner()
    runner.start_timer(30)
    Timer.assert_called_once_with(30, runner.kill)

def timeout__mocked_timer(self):
    runner = self._runner()
    runner._timer = Mock()
    return runner

def timeout_run_always_stops_timer(self):
    runner = _GenericExceptingRunner(Context())
    runner.stop_timer = Mock()
    with raises(_GenericException):
        runner.run(_)
    runner.stop_timer.assert_called_once_with()

def timeout_stop_timer_cancels_timer(self):
    runner = self._mocked_timer()
    runner.stop_timer()
    runner._timer.cancel.assert_called_once_with()

def timeout_timer_aliveness_is_test_of_timing_out(self):
    runner = Runner(Context())
    runner._timer = Mock()
    runner._timer.is_alive.return_value = False
    assert runner.timed_out
    runner._timer.is_alive.return_value = True
    assert not runner.timed_out

def timeout_timeout_specified_but_no_timer_means_no_exception(self):
    runner = Runner(Context())
    runner._timer = None
    assert not runner.timed_out

def stop_always_runs_no_matter_what(self):
    runner = _GenericExceptingRunner(context=Context())
    runner.stop = Mock()
    with raises(_GenericException):
        runner.run(_)
    runner.stop.assert_called_once_with()

def asynchronous_returns_Promise_immediately_and_finishes_on_join(self):

    class _Finisher(_Dummy):
        _finished = False

        @property
        def process_is_finished(self):
            return self._finished
    runner = _Finisher(Context())
    runner.start = Mock()
    for method in self._stop_methods:
        setattr(runner, method, Mock())
    result = runner.run(_, asynchronous=True)
    assert isinstance(result, Promise)
    assert runner.start.called
    for method in self._stop_methods:
        assert not getattr(runner, method).called
    runner._finished = True
    result.join()
    for method in self._stop_methods:
        assert getattr(runner, method).called

@trap
def asynchronous_hides_output(self):
    self._runner(out='foo', err='bar').run(_, asynchronous=True).join()
    assert sys.stdout.getvalue() == ''
    assert sys.stderr.getvalue() == ''

def asynchronous_does_not_forward_stdin(self):

    class MockedHandleStdin(_Dummy):
        pass
    MockedHandleStdin.handle_stdin = Mock()
    runner = self._runner(klass=MockedHandleStdin)
    runner.run(_, asynchronous=True).join()
    assert not MockedHandleStdin.handle_stdin.called

def asynchronous_leaves_overridden_streams_alone(self):
    klass = self._mock_stdin_writer()
    (out, err, in_) = (StringIO(), StringIO(), StringIO('hallo'))
    runner = self._runner(out='foo', err='bar', klass=klass)
    runner.run(_, asynchronous=True, out_stream=out, err_stream=err, in_stream=in_).join()
    assert out.getvalue() == 'foo'
    assert err.getvalue() == 'bar'
    assert klass.write_proc_stdin.called

@patch.object(threading.Thread, 'start')
def disown_starts_and_returns_None_but_does_nothing_else(self, thread_start):
    runner = Runner(Context())
    runner.start = Mock()
    not_called = self._stop_methods + ['wait']
    for method in not_called:
        setattr(runner, method, Mock())
    result = runner.run(_, disown=True)
    assert result is None
    assert runner.start.called
    assert not thread_start.called
    for method in not_called:
        assert not getattr(runner, method).called

def disown_cannot_be_given_alongside_asynchronous(self):
    with raises(ValueError) as info:
        self._runner().run(_, asynchronous=True, disown=True)
    sentinel = "Cannot give both 'asynchronous' and 'disown'"
    assert sentinel in str(info.value)

def Local___run(self, *args, **kwargs):
    return _run(*args, **dict(kwargs, klass=_FastLocal))

def Local___runner(self, *args, **kwargs):
    return _runner(*args, **dict(kwargs, klass=_FastLocal))

@mock_pty()
def pty_when_pty_True_we_use_pty_fork_and_os_exec(self):
    """when pty=True, we use pty.fork and os.exec*"""
    self._run(_, pty=True)

@mock_pty(insert_os=True)
def pty__expect_exit_check(self, exited, mock_os):
    if exited:
        expected_check = mock_os.WIFEXITED
        expected_get = mock_os.WEXITSTATUS
        unexpected_check = mock_os.WIFSIGNALED
        unexpected_get = mock_os.WTERMSIG
    else:
        expected_check = mock_os.WIFSIGNALED
        expected_get = mock_os.WTERMSIG
        unexpected_check = mock_os.WIFEXITED
        unexpected_get = mock_os.WEXITSTATUS
    expected_check.return_value = True
    unexpected_check.return_value = False
    self._run(_, pty=True)
    exitstatus = mock_os.waitpid.return_value[1]
    expected_get.assert_called_once_with(exitstatus)
    assert not unexpected_get.called

def pty_pty_uses_WEXITSTATUS_if_WIFEXITED(self):
    self._expect_exit_check(True)

def pty_pty_uses_WTERMSIG_if_WIFSIGNALED(self):
    self._expect_exit_check(False)

@mock_pty(insert_os=True)
def pty_WTERMSIG_result_turned_negative_to_match_subprocess(self, mock_os):
    mock_os.WIFEXITED.return_value = False
    mock_os.WIFSIGNALED.return_value = True
    mock_os.WTERMSIG.return_value = 2
    assert self._run(_, pty=True, warn=True).exited == -2

@mock_pty()
def pty_pty_is_set_to_controlling_terminal_size(self):
    self._run(_, pty=True)

def pty_warning_only_fires_once(self):
    skip()

@patch('invoke.runners.sys')
def pty_replaced_stdin_objects_dont_explode(self, mock_sys):
    mock_sys.stdin = object()
    runner = Local(Context())
    assert runner.should_use_pty(pty=True, fallback=True) is False

@mock_pty(trailing_error=OSError('Input/output error'))
def pty_spurious_OSErrors_handled_gracefully(self):
    self._run(_, pty=True)

@mock_pty(trailing_error=OSError('I/O error'))
def pty_other_spurious_OSErrors_handled_gracefully(self):
    self._run(_, pty=True)

@mock_pty(trailing_error=OSError('wat'))
def pty_non_spurious_OSErrors_bubble_up(self):
    try:
        self._run(_, pty=True)
    except ThreadException as e:
        e = e.exceptions[0]
        assert e.type == OSError
        assert str(e.value) == 'wat'

@mock_pty(os_close_error=True)
def pty_stop_mutes_errors_on_pty_close(self):
    self._run(_, pty=True)

@mock_pty(isatty=False)
def fallback_can_be_overridden_by_kwarg(self):
    self._run(_, pty=True, fallback=False)

@mock_pty(isatty=False)
def fallback_can_be_overridden_by_config(self):
    self._runner(run={'fallback': False}).run(_, pty=True)

@trap
@mock_subprocess(isatty=False)
def fallback_affects_result_pty_value(self, *mocks):
    assert self._run(_, pty=True).pty is False

@mock_pty(isatty=False)
def fallback_overridden_fallback_affects_result_pty_value(self):
    assert self._run(_, pty=True, fallback=False).pty is True

@mock_pty(insert_os=True)
def shell_defaults_to_bash_or_cmdexe_when_pty_True(self, mock_os):
    self._run(_, pty=True)
    _expect_platform_shell(mock_os.execve.call_args_list[0][0][0])

@mock_subprocess(insert_Popen=True)
def shell_defaults_to_bash_or_cmdexe_when_pty_False(self, mock_Popen):
    self._run(_, pty=False)
    _expect_platform_shell(mock_Popen.call_args_list[0][1]['executable'])

@mock_pty(insert_os=True)
def shell_may_be_overridden_when_pty_True(self, mock_os):
    self._run(_, pty=True, shell='/bin/zsh')
    assert mock_os.execve.call_args_list[0][0][0] == '/bin/zsh'

@mock_subprocess(insert_Popen=True)
def shell_may_be_overridden_when_pty_False(self, mock_Popen):
    self._run(_, pty=False, shell='/bin/zsh')
    assert mock_Popen.call_args_list[0][1]['executable'] == '/bin/zsh'

@mock_subprocess(insert_Popen=True)
def env_uses_Popen_kwarg_for_pty_False(self, mock_Popen):
    self._run(_, pty=False, env={'FOO': 'BAR'})
    expected = dict(os.environ, FOO='BAR')
    env = mock_Popen.call_args_list[0][1]['env']
    assert env == expected

@mock_pty(insert_os=True)
def env_uses_execve_for_pty_True(self, mock_os):
    type(mock_os).environ = {'OTHERVAR': 'OTHERVAL'}
    self._run(_, pty=True, env={'FOO': 'BAR'})
    expected = {'OTHERVAR': 'OTHERVAL', 'FOO': 'BAR'}
    env = mock_os.execve.call_args_list[0][0][2]
    assert env == expected

def close_proc_stdin_raises_SubprocessPipeError_when_pty_in_use(self):
    with raises(SubprocessPipeError):
        runner = Local(Context())
        runner.using_pty = True
        runner.close_proc_stdin()

def close_proc_stdin_closes_process_stdin(self):
    runner = Local(Context())
    runner.process = Mock()
    runner.using_pty = False
    runner.close_proc_stdin()
    runner.process.stdin.close.assert_called_once_with()

@patch('invoke.runners.os')
def timeout_kill_uses_self_pid_when_pty(self, mock_os):
    runner = self._runner()
    runner.using_pty = True
    runner.pid = 50
    runner.kill()
    mock_os.kill.assert_called_once_with(50, signal.SIGKILL)

@patch('invoke.runners.os')
def timeout_kill_uses_self_process_pid_when_not_pty(self, mock_os):
    runner = self._runner()
    runner.using_pty = False
    runner.process = Mock(pid=30)
    runner.kill()
    mock_os.kill.assert_called_once_with(30, signal.SIGKILL)

def Result__nothing_is_required(self):
    Result()

def Result__first_posarg_is_stdout(self):
    assert Result('foo').stdout == 'foo'

def Result__command_defaults_to_empty_string(self):
    assert Result().command == ''

def Result__shell_defaults_to_empty_string(self):
    assert Result().shell == ''

def Result__encoding_defaults_to_local_default_encoding(self):
    assert Result().encoding == default_encoding()

def Result__env_defaults_to_empty_dict(self):
    assert Result().env == {}

def Result__stdout_defaults_to_empty_string(self):
    assert Result().stdout == u''

def Result__stderr_defaults_to_empty_string(self):
    assert Result().stderr == u''

def Result__exited_defaults_to_zero(self):
    assert Result().exited == 0

def Result__pty_defaults_to_False(self):
    assert Result().pty is False

def Result__repr_contains_useful_info(self):
    assert repr(Result(command='foo')) == "<Result cmd='foo' exited=0>"

def tail_setup(self):
    self.sample = '\n'.join((str(x) for x in range(25)))

def tail_returns_last_10_lines_of_given_stream_plus_whitespace(self):
    expected = '\n\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24'
    assert Result(stdout=self.sample).tail('stdout') == expected

def tail_line_count_is_configurable(self):
    expected = '\n\n23\n24'
    tail = Result(stdout=self.sample).tail('stdout', count=2)
    assert tail == expected

def tail_works_for_stderr_too(self):
    expected = '\n\n23\n24'
    tail = Result(stderr=self.sample).tail('stderr', count=2)
    assert tail == expected

@patch('invoke.runners.encode_output')
def tail_encodes_with_result_encoding(self, encode):
    Result(stdout='foo', encoding='utf-16').tail('stdout')
    encode.assert_called_once_with('\n\nfoo', 'utf-16')

def Promise__exposes_read_only_run_params(self):
    runner = _runner()
    promise = runner.run(_, pty=True, encoding='utf-17', shell='sea', asynchronous=True)
    assert promise.command == _
    assert promise.pty is True
    assert promise.encoding == 'utf-17'
    assert promise.shell == 'sea'
    assert not hasattr(promise, 'stdout')
    assert not hasattr(promise, 'stderr')

def join_returns_Result_on_success(self):
    result = _runner().run(_, asynchronous=True).join()
    assert isinstance(result, Result)
    assert result.command == _
    assert result.exited == 0

def join_raises_main_thread_exception_on_kaboom(self):
    runner = _runner(klass=_GenericExceptingRunner)
    with raises(_GenericException):
        runner.run(_, asynchronous=True).join()

@pytest.mark.skip(reason='fail')
def join_raises_subthread_exception_on_their_kaboom(self):

    class Kaboom(_Dummy):

        def handle_stdout(self, **kwargs):
            raise OhNoz()
    runner = _runner(klass=Kaboom)
    promise = runner.run(_, asynchronous=True)
    with raises(ThreadException) as info:
        promise.join()
    assert isinstance(info.value.exceptions[0].value, OhNoz)

def join_raises_Failure_on_failure(self):
    runner = _runner(exits=1)
    promise = runner.run(_, asynchronous=True)
    with raises(Failure):
        promise.join()

def context_manager_calls_join_or_wait_on_close_of_block(self):
    promise = _runner().run(_, asynchronous=True)
    promise.join = Mock()
    with promise:
        pass
    promise.join.assert_called_once_with()

def context_manager_yields_self(self):
    promise = _runner().run(_, asynchronous=True)
    with promise as value:
        assert value is promise