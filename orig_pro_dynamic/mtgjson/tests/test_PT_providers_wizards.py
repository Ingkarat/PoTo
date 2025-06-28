import pathlib

from mtgjson.mtgjson5.providers.wizards import WizardsProvider

def test_PT_download():
    gh = WizardsProvider()
    url = "testurl"
    p = {"s":1}
    gh.download(url,p)

def test_PT_get_translation_for_set():
    gh = WizardsProvider()
    gh.get_translation_for_set("teststr")

def test_PT_build_single_language():
    gh = WizardsProvider()
    gh.build_single_language("short","long",{"a":{"b":"c"}})

def test_PT_convert_keys_to_set_names():
    gh = WizardsProvider()
    d = {"a":{"b":"c"}}
    gh.convert_keys_to_set_names(d)

def test_PT_load_translation_table():
    gh = WizardsProvider()
    gh.load_translation_table()

def test_PT_build_translation_table():
    gh = WizardsProvider()
    gh.build_translation_table()

def test_PT_override_set_translations():
    gh = WizardsProvider()
    d = {"a":{"b":"c"}}
    gh.override_set_translations(d)

def test_PT_set_names_to_set_codes():
    gh = WizardsProvider()
    d = {"a":{"b":"c"}}
    gh.set_names_to_set_codes(d)

def test_PT_get_magic_rules():
    gh = WizardsProvider()
    gh.get_magic_rules()

def test_PT_build_single_set_code():
    gh = WizardsProvider()
    gh.build_single_set_code("teststr",{"a":"b"})