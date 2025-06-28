import sys
import jedi
from commands.autocomplete import AutoComplete
from handlers.jedi_handler import JediHandler
PYTHON36 = sys.version_info >= (3, 6)

def TestAutoCompletion_setUp(self):
    self.settings = {}

def TestAutoCompletion_test_autocomplete_command(self):
    AutoComplete(self._check, 0, jedi.Script('import os; os.'))

def TestAutoCompletion_test_autocomplete_handler(self):
    data = {'source': 'import os; os.', 'line': 1, 'offset': 14}
    handler = JediHandler('autocomplete', data, 0, 0, self.settings, self._check)
    handler.run()

def TestAutoCompletion_test_autocomplete_not_in_string(self):
    data = {'source': 'import os; "{os.', 'line': 1, 'offset': 16}
    handler = JediHandler('autocomplete', data, 0, 0, self.settings, self._check_false)
    handler.run()

def TestAutoCompletion_test_autocomplete_in_fstring(self):
    data = {'source': 'import os; f"{os.', 'line': 1, 'offset': 17}
    handler = JediHandler('autocomplete', data, 0, 0, self.settings, self._check if PYTHON36 else self._check_false)
    handler.run()

def TestAutoCompletion__check(self, kwrgs):
    assert kwrgs['success'] is True
    assert len(kwrgs['completions']) > 0
    if sys.version_info < (3, 6):
        assert kwrgs['completions'][0] == ('abort\tfunction', 'abort')
    else:
        assert kwrgs['completions'][0] == ('abc\tmodule', 'abc')
    assert kwrgs['uid'] == 0

def TestAutoCompletion__check_false(self, kwrgs):
    assert kwrgs['success'] is False