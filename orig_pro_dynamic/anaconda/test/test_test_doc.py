import sys
import jedi
from commands.doc import Doc
from handlers.jedi_handler import JediHandler
src = 'def test_src():\n\t"""Test String\n\t"""\n\ntest_src'
src_escape = 'def test_src():\n\t"""<strong>Espa&nacute;a currency €</strong>"""\n\ntest_src'

def TestDoc_test_doc_command(self):
    Doc(self._check_html, 0, jedi.Script(src), True)

def TestDoc_test_doc_plain(self):
    Doc(self._check_plain, 0, jedi.Script(src), False)

def TestDoc_test_doc_html_escape(self):
    Doc(self._check_html_escape, 0, jedi.Script(src_escape), True)

def TestDoc_test_doc_no_definiion(self):
    Doc(self._check_no_definition, 0, jedi.Script('nothing'), False)

def TestDoc_test_doc_handler(self):
    data = {'source': src, 'line': 5, 'offset': 8, 'html': True}
    handler = JediHandler('doc', data, 0, 0, {}, self._check_handler)
    handler.run()

def TestDoc__check_html(self, kwrgs):
    self._common_assertions(kwrgs)
    assert kwrgs['doc'].strip() == '__main__.test_src\ntest_src()<br><br>Test String<br>'

def TestDoc__check_plain(self, kwrgs):
    self._common_assertions(kwrgs)
    assert kwrgs['doc'].strip() == 'Docstring for {0}\n{1}\n{2}'.format('__main__.test_src', '=' * 40, 'test_src()\n\nTest String')

def TestDoc__check_html_escape(self, kwrgs):
    self._common_assertions(kwrgs)
    if sys.version_info >= (3, 4):
        print(kwrgs['doc'])
        assert kwrgs['doc'].strip() == '__main__.test_src\ntest_src()<br><br>&lt;strong&gt;Espańa currency €&lt;/strong&gt;'
    if sys.version_info < (3, 0):
        print(repr(kwrgs['doc']))
        assert kwrgs['doc'].strip() == '__main__.test_src\ntest_src()<br><br>&lt;strong&gt;Espa&amp;nacute;a currency â\x82¬&lt;/strong&gt;'

def TestDoc__check_no_definition(self, kwrgs):
    assert kwrgs['success'] is False
    assert kwrgs['uid'] == 0
    assert kwrgs['doc'] == ''

def TestDoc__check_handler(self, kwrgs):
    self._check_html(kwrgs)

def TestDoc__common_assertions(self, kwrgs):
    assert kwrgs['success'] is True
    assert kwrgs['uid'] == 0