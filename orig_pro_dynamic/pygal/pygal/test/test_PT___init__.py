from pygal import PluginImportFixer

def test_PT_find_module():
    pi = PluginImportFixer()
    pi.find_module(fullname, "testpath")

def test_PT_load_module():
    pi = PluginImportFixer()
    pi.find_module(name)
