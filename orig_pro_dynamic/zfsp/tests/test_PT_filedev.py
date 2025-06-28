from zfsp.zfs.filedev import FileDev

def test_PT_read():
    fd = FileDev()
    fd.read()

def test_PT_write():
    fd = FileDev()
    fd.write()

def test_PT_flush():
    fd = FileDev()
    fd.flush()

def test_PT_seek():
    fd = FileDev()
    fd.seek()