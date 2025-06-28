import pytest
pytest
from os import chdir
from subprocess import run
from . import TOP_PATH

@pytest.mark.skip(reason='error')
def test_balck() -> None:
    """ Assures that the Python codebase imports are correctly formatted.

    """
    chdir(TOP_PATH)
    proc = run(['black', '-l', '160', '--diff', '--check', 'release'], capture_output=True)
    assert proc.returncode == 0, f"black issues:\n{proc.stdout.decode('utf-8')}"