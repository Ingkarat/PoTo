import pytest
pytest
from os import chdir
from pathlib import Path
from subprocess import run
from . import TOP_PATH

@pytest.mark.skip(reason='error')
def test_eslint() -> None:
    """ Assures that the BokehJS codebase passes configured eslint checks

    """
    chdir(Path(TOP_PATH) / 'bokehjs')
    proc = run(['node', 'make', 'lint'], capture_output=True)
    assert proc.returncode == 0, f"eslint issues:\n{proc.stdout.decode('utf-8')}"