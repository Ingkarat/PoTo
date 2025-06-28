from zfsp.zfs.raidzdev import convert
from zfsp.zfs.raidzdev import should_resize
from zfsp.zfs.raidzdev import locate_data
from zfsp.zfs.raidzdev import xor_blocks
from zfsp.zfs.raidzdev import RaidZDev
from zfsp.zfs import ondisk

def test_PT_convert():
    convert(5,6,7,8)
    
def test_PT_should_resize():
    should_resize(5,6,7,8)
    
def test_PT_locate_data():
    locate_data(5,6,7,8)
    
def test_PT_xor_blocks():
    xor_blocks()
    
def test_PT_read_dva():
    rz = RaidZDev()
    dva = ondisk.dva()
    rz.read_dva(dva)
    
def test_PT_read():
    rz = RaidZDev()
    rz2 = RaidZDev()
    rz.read(1,2)
    rz2.read((1,2), 2)
