from zfsp.zfs.objectset import ObjectSet
from zfsp.zfs import ondisk

def test_PT_from_struct():
    os = ObjectSet()
    os.from_struct()

def test_PT_from_block():
    os = ObjectSet()
    os.from_block()

def test_PT_get_dnode():
    os = ObjectSet()
    os.get_dnode(5)

def test_PT_parse_dnode():
    os = ObjectSet()
    d = ondisk.DNode()
    os.parse_dnode(d, 5)

def test_PT_read_default():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_default(d)

def test_PT_read_none():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_none(d)

def test_PT_read_directory():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_directory(d)

def test_PT_read_file():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_file(d)

def test_PT_read_zap():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_zap(d)

def test_PT_read_attr_registration():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_attr_registration(d)

def test_PT_read_bpobj():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_bpobj(d)

def test_PT_read_object_array():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_object_array(d)

def test_PT_read_nvlist():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_nvlist(d)

def test_PT_read_dataset():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_dataset(d)

def test_PT_read_dsldir():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_dsldir(d)

def test_PT_read_history():
    os = ObjectSet()
    d = ondisk.DNode()
    os.read_history(d)
