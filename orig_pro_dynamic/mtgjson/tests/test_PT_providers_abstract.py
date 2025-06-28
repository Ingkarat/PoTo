from mtgjson.mtgjson5.providers.abstract import AbstractProvider

def test_PT_download():
    ap = AbstractProvider()
    url = "testurl"
    p = {"s":1}
    ap.download(url,p)

def test_PT_get_class_name():
    ap = AbstractProvider()
    ap.get_class_name()

def test_PT_get_class_id():
    ap = AbstractProvider()
    ap.get_class_id()

def test_PT_get_configs():
    ap = AbstractProvider()
    ap.get_configs()

def test_PT_log_download():
    ap = AbstractProvider()
    ap.log_download()