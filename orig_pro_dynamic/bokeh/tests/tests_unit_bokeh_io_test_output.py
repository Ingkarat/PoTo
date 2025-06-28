import pytest
pytest
from mock import patch
from bokeh.io.state import curstate
from bokeh.resources import Resources
import bokeh.io.output as bio

@patch('bokeh.io.state.State.reset')
def test_reset_output(mock_reset) -> None:
    original_call_count = curstate().reset.call_count
    bio.reset_output()
    assert curstate().reset.call_count == original_call_count + 1

@patch('bokeh.io.state.State.output_file')
def Test_output_file_test_no_args(self, mock_output_file) -> None:
    default_kwargs = dict(title='Bokeh Plot', mode=None, root_dir=None)
    bio.output_file('foo.html')
    assert mock_output_file.call_count == 1
    assert mock_output_file.call_args[0] == ('foo.html',)
    assert mock_output_file.call_args[1] == default_kwargs

@patch('bokeh.io.state.State.output_file')
def Test_output_file_test_with_args(self, mock_output_file) -> None:
    kwargs = dict(title='title', mode='cdn', root_dir='foo')
    bio.output_file('foo.html', **kwargs)
    assert mock_output_file.call_count == 1
    assert mock_output_file.call_args[0] == ('foo.html',)
    assert mock_output_file.call_args[1] == kwargs

@patch('bokeh.io.output.run_notebook_hook')
def Test_output_notebook_test_no_args(self, mock_run_notebook_hook) -> None:
    default_load_jupyter_args = (None, False, False, 5000)
    bio.output_notebook()
    assert mock_run_notebook_hook.call_count == 1
    assert mock_run_notebook_hook.call_args[0] == ('jupyter', 'load') + default_load_jupyter_args
    assert mock_run_notebook_hook.call_args[1] == {}

@patch('bokeh.io.output.run_notebook_hook')
def Test_output_notebook_test_with_args(self, mock_run_notebook_hook) -> None:
    load_jupyter_args = (Resources(), True, True, 1000)
    bio.output_notebook(*load_jupyter_args)
    assert mock_run_notebook_hook.call_count == 1
    assert mock_run_notebook_hook.call_args[0] == ('jupyter', 'load') + load_jupyter_args
    assert mock_run_notebook_hook.call_args[1] == {}