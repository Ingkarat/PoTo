from zfsp.zfs.zfuse import locked
from zfsp.zfs.zfuse import ZFSFuse
from zfsp.zfs.zfuse import mount

def test_PT_locked():
    locked(f)

def test_PT_getattr():
    zf = ZFSFuse()
    zf.getattr("testpath",None)

def test_PT_getxattr():
    zf = ZFSFuse()
    zf.getxattr("testpath","testname",0)

def test_PT_listxattr():
    zf = ZFSFuse()
    zf.listxattr("testpath")

def test_PT_open():
    zf = ZFSFuse()
    zf.open("testpath", flags)

def test_PT_readlink():
    zf = ZFSFuse()
    zf.readlink("testpath")

def test_PT_read():
    zf = ZFSFuse()
    zf.read("testpath", 1,2,fh)

def test_PT_readdir():
    zf = ZFSFuse()
    zf.readdir("testpath",fh)

def test_PT_statfs():
    zf = ZFSFuse()
    zf.statfs("testpath")

def test_PT_mount():
    mount(pool, mountpoint)