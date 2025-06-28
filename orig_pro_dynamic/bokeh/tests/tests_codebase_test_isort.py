import pytest
pytest
from os import chdir
from subprocess import run
from . import TOP_PATH, ls_files

@pytest.mark.skip(reason='error')
def test_isort() -> None:
    """ Assures that the Python codebase imports are correctly sorted.

    """
    chdir(TOP_PATH)
    proc = run(['isort', '-df', '-rc', '-c', *ls_files('*.py')], capture_output=True)
    assert proc.returncode == 0, f"isort issues:\n{proc.stdout.decode('utf-8')}"