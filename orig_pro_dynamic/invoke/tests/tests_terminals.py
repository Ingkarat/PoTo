import fcntl
import termios
from mock import Mock, patch
from pytest import skip, mark
from invoke.terminals import pty_size, bytes_to_read, WINDOWS
pytestmark = mark.skipif(WINDOWS, reason='Low level terminal tests only work well on POSIX')

@patch('fcntl.ioctl', wraps=fcntl.ioctl)
def pty_size_calls_fcntl_with_TIOCGWINSZ(self, ioctl):
    pty_size()
    assert ioctl.call_args_list[0][0][1] == termios.TIOCGWINSZ

@patch('sys.stdout')
@patch('fcntl.ioctl')
def pty_size_defaults_to_80x24_when_stdout_not_a_tty(self, ioctl, stdout):
    stdout.fileno.return_value = 1
    stdout.isatty.return_value = False
    assert pty_size() == (80, 24)

@patch('sys.stdout')
@patch('fcntl.ioctl')
def pty_size_uses_default_when_stdout_lacks_fileno(self, ioctl, stdout):
    stdout.fileno.side_effect = AttributeError
    assert pty_size() == (80, 24)

@patch('sys.stdout')
@patch('fcntl.ioctl')
def pty_size_uses_default_when_stdout_triggers_ioctl_error(self, ioctl, stdout):
    ioctl.side_effect = TypeError
    assert pty_size() == (80, 24)

@patch('invoke.terminals.fcntl')
def bytes_to_read__returns_1_when_stream_lacks_fileno(self, fcntl):
    assert bytes_to_read(Mock(fileno=lambda : None)) == 1
    assert not fcntl.ioctl.called

@patch('invoke.terminals.fcntl')
def bytes_to_read__returns_1_when_stream_has_fileno_but_is_not_a_tty(self, fcntl):
    fcntl.ioctl.side_effect = IOError('Operation not supported by device')
    stream = Mock(isatty=lambda : False, fileno=lambda : 17)
    assert bytes_to_read(stream) == 1
    assert not fcntl.ioctl.called

def bytes_to_read__returns_FIONREAD_result_when_stream_is_a_tty(self):
    skip()

def bytes_to_read__returns_1_on_windows(self):
    skip()