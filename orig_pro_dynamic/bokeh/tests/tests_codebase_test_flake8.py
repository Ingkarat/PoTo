import pytest
pytest
from os import chdir
from subprocess import run
from . import TOP_PATH, ls_files

@pytest.mark.skip(reason='error')
def test_flake8() -> None:
    """ Assures that the Python codebase passes configured Flake8 checks

    """
    chdir(TOP_PATH)
    proc = run(['flake8', *ls_files('*.py')], capture_output=True)
    assert proc.returncode == 0, f"Flake8 issues:\n{proc.stdout.decode('utf-8')}"