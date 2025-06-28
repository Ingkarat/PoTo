from zfsp.zfs.readcontext import ReadContext
from zfsp.zfs import ondisk

def test_PT_checksum():
    rc = ReadContext()
    rc.checksum(data,balid,checksum)
    
def test_PT_decompress():
    rc = ReadContext()
    rc.decompress(data,compression,5)
    
def test_PT_update_inherit():
    rc = ReadContext()
    rc.update_inherit(compression,checksum)
    
def test_PT_read_block():
    rc = ReadContext()
    b = ondisk.Blockptr()
    rc.read_block(b,0)
    
def test_PT_read_block_thorough():
    rc = ReadContext()
    b = ondisk.Blockptr()
    rc.read_block_thorough(b)
    
def test_PT_read_indirect():
    rc = ReadContext()
    b = ondisk.Blockptr()
    rc.read_indirect(b)
    
def test_PT_read_dnode():
    rc = ReadContext()
    d = ondisk.DNode
    rc.read_dnode(d)
    
def test_PT_context():
    rc = ReadContext()
    rc.context()