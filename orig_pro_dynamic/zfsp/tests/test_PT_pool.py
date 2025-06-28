from zfsp.zfs.pool import vdev_list_to_dict
from zfsp.zfs import vdevs
from zfsp.zfs import ondisk

def test_PT_vdev_list_to_dict():
    v = vdevs.VDev()
    vdev_list_to_dict(v)

def test_PT_first_vdev():
    p = Pool()
    p.first_vdev()

def test_PT_context():
    p = Pool()
    p.context()

def test_PT_read_block():
    p = Pool()
    p.read_block(blkptr)

def test_PT_read_indirect():
    p = Pool()
    p.read_indirect(blkptr)

def test_PT_read_dnode():
    p = Pool()
    d = ondisk.DNode()
    p.read_dnode(d)

def test_PT_read_file():
    p = Pool()
    p.read_file("testpath")

def test_PT_objset_for_vdev():
    p = Pool()
    p.objset_for_vdev(5)

def test_PT_root_dataset():
    p = Pool()
    p.root_dataset()

def test_PT_metaslab_array():
    p = Pool()
    p.metaslab_array()

def test_PT_dataset_for():
    p = Pool()
    p.dataset_for("teststr")

def test_PT_open():
    p = Pool()
    p.open("testpath")