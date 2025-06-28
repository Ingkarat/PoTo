import pytest
pytest
from bokeh._testing.util.api import verify_all
import bokeh.application.handlers as bah
ALL = ('CodeHandler', 'DirectoryHandler', 'FunctionHandler', 'Handler', 'NotebookHandler', 'ScriptHandler', 'ServerLifecycleHandler')
Test___all__ = verify_all(bah, ALL)