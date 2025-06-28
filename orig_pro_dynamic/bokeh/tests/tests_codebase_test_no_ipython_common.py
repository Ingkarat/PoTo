import pytest
pytest
from subprocess import PIPE, Popen
from sys import executable
BASIC_IMPORTS = ['import bokeh.application', 'import bokeh.client', 'import bokeh.embed', 'import bokeh.io', 'import bokeh.models', 'import bokeh.plotting', 'import bokeh.server']

def test_no_ipython_common() -> None:
    """ Basic usage of Bokeh should not result in any IPython code being
    imported. This test ensures that importing basic modules does not bring in
    IPython.

    """
    proc = Popen([executable, '-c', "import sys; %s; sys.exit(1 if any('IPython' in x for x in sys.modules.keys()) else 0)" % ';'.join(BASIC_IMPORTS)], stdout=PIPE)
    proc.communicate()
    proc.wait()
    if proc.returncode != 0:
        assert False