from zfsp.explore import PoolExplorer
from zfsp.explore import cli

def test_PT_setup_module_logs():
    pe = PoolExplorer()
    pe.setup_module_logs(args)

def test_PT_cli():
    pe = PoolExplorer()
    pe.cli()

def test_PT_load_pool():
    pe = PoolExplorer()
    pe.load_pool(args)

def test_PT_list_cmd():
    pe = PoolExplorer()
    pe.list_cmd()

def test_PT_cat():
    pe = PoolExplorer()
    pe.cat(args)

def test_PT_show_object():
    pe = PoolExplorer()
    pe.show_object(args,os,obj)

def test_PT_objset():
    pe = PoolExplorer()
    pe.objset(args)

def test_PT_nvparse():
    pe = PoolExplorer()
    pe.nvparse(args)

def test_PT_label():
    pe = PoolExplorer()
    pe.label(args)

def test_PT_mount_fuse():
    pe = PoolExplorer()
    pe.mount_fuse(args)

def test_PT_read_dva():
    pe = PoolExplorer()
    pe.read_dva(args)

def test_PT_outer_cli():
    cli()