from zfsp.zfs.lzjb import decompress

from typing import ByteString

def test_PT_decompress():
    decompress(ByteString, 5)