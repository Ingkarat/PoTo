import pathlib

from mtgjson.mtgjson5.providers.whats_in_standard import WhatsInStandardProvider

def test_PT_download():
    gh = WhatsInStandardProvider()
    url = "testurl"
    p = {"s":1}
    gh.download(url,p)

def test_PT_standard_legal_set_codes():
    gh = WhatsInStandardProvider()
    gh.standard_legal_set_codes()