from commands.mccabe import McCabe
from handlers.qa_handler import QAHandler
from linting.anaconda_mccabe import AnacondaMcCabe

def TestQa_test_mccabe_command(self):
    McCabe(self._check_mccabe, 0, 0, AnacondaMcCabe, self._code, 0, '')

def TestQa_test_mccabe_high_threshold(self):

    def _check_threshold_4(result):
        assert result['success'] is True
        assert len(result['errors']) == 1

    def _check_threshold_7(result):
        assert result['success'] is True
        assert len(result['errors']) == 0
    McCabe(_check_threshold_4, 0, 0, AnacondaMcCabe, self._code, 4, '')
    McCabe(_check_threshold_7, 0, 0, AnacondaMcCabe, self._code, 7, '')

def TestQa_test_mccabe_handler(self):
    data = {'code': self._code, 'threshold': 4, 'filename': ''}
    handler = QAHandler('mccabe', data, 0, 0, {}, self._check_mccabe)
    handler.run()

def TestQa__check_mccabe(self, result):
    assert result['success'] is True
    assert result['uid'] == 0
    assert result['vid'] == 0
    assert len(result['errors']) == 1
    assert result['errors'][0]['message'] == "'f' is too complex (4)"
    assert result['errors'][0]['line'] == 2
    assert result['errors'][0]['code'] == 'C901'
    assert result['errors'][0]['offset'] == 1