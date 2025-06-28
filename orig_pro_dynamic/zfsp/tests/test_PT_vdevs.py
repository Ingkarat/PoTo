from zfsp.zfs.vdevs import VDev
from zfsp.zfs import ondisk

def test_PT_parse_uberblocks():
    vd = VDev()
    ub = ondisk.Uberblock()
    vd.parse_uberblocks([ub])

def test_PT_select_uberblock():
    vd = VDev()
    vd.select_uberblock(5)

def test_PT_read_label():
    vd = VDev()
    vd.read_label((1,2))

def test_PT_read_dva():
    vd = VDev()
    dv = ondisk.dva()
    vd.read_dva(dv)

def test_PT_read():
    vd = VDev()
    vd2 = VDev()
    vd.read(1,2)
    vd2.read((1,2),2)

