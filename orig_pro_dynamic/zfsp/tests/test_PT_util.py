from zfsp.zfs.util import decompress
from zfsp.zfs.util import checksum
from zfsp.zfs.util import sha256
from zfsp.zfs.util import unpack
from zfsp.zfs.util import fletcher2
from zfsp.zfs.util import fletcher4
from zfsp.zfs.constants import Compression
from zfsp.zfs.constants import Checksum
def test_PT_decompress():
    c = Compression()
    decompress(data,c,5,None)

def test_PT_checksum():
    cs = Checksum()
    ih = Checksum()
    checksum(data,(1,2,3,4),cs,ih,(5,6,7,8))

def test_PT_sha256():
    sha256(data)

def test_PT_unpack():
    unpack(data, "teststr")

def test_PT_fletcher2():
    fletcher2(data)

def test_PT_fletcher4():
    fletcher4(data)

