import sys
import jedi
from handlers.jedi_handler import JediHandler
from commands.complete_parameters import CompleteParameters
PYTHON3 = sys.version_info >= (3, 0)

def TestCompleteParameters_setUp(self):
    self.settings = {'complete_all_parameters': False}
    self.script = jedi.Script('open(')

def TestCompleteParameters_test_complete_parameters_command(self):
    CompleteParameters(self._check_parameters, 0, self.script, self.settings)

def TestCompleteParameters_test_complete_all_parameters(self):
    self.settings['complete_all_parameters'] = True
    CompleteParameters(self._check_all_parameters, 0, self.script, self.settings)

def TestCompleteParameters_test_complete_parameters_handler(self):
    data = {'source': 'open(', 'line': 1, 'offset': 5, 'filname': None, 'settings': self.settings}
    handler = JediHandler('parameters', data, 0, 0, self.settings, self._check_parameters)
    handler.run()

def TestCompleteParameters_test_complete_all_parameters_handler(self):
    self.settings['complete_all_parameters'] = True
    data = {'source': 'open(', 'line': 1, 'offset': 5, 'filname': None, 'settings': self.settings}
    handler = JediHandler('parameters', data, 0, 0, self.settings, self._check_all_parameters)
    handler.run()

def TestCompleteParameters__check_parameters(self, result):
    assert result['success'] is True
    assert result['template'] == '${1:file: Union[str, bytes, int]}' if PYTHON3 else u'${1:file}'
    assert result['uid'] == 0

def TestCompleteParameters__check_all_parameters(self, result):
    assert result['success'] is True
    assert result['template'] == '${1:file: Union[str, bytes, int]}, mode: str=${2:...}, buffering: int=${3:...}, encoding: Optional[str]=${4:...}, errors: Optional[str]=${5:...}, newline: Optional[str]=${6:...}, closefd: bool=${7:...}, opener: Optional[Callable[[str, int], int]]=${8:...}' if PYTHON3 else u"${1:file}, mode=${2:'r'}, buffering=${3:-1}, encoding=${4:None}, errors=${5:None}, newline=${6:None}, closefd=${7:True}"
    assert result['uid'] == 0