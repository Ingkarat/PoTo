from sc2.pixel_map import PixelMap
from sc2.position import Point2

def test_PT_width():
    pm = PixelMap()
    pm.width()

def test_PT_height():
    pm = PixelMap()
    pm.height()

def test_PT_bits_per_pixel():
    pm = PixelMap()
    pm.bits_per_pixel()

def test_PT_bytes_per_pixel():
    pm = PixelMap()
    pm.bytes_per_pixel()

def test_PT_is_set():
    pm = PixelMap()
    pm.is_set(p)

def test_PT_is_empty():
    pm = PixelMap()
    pm.is_empty(p)

def test_PT_invert():
    pm = PixelMap()
    pm.invert()

def test_PT_flood_fill():
    pm = PixelMap()
    p2 = Point2()
    pm.flood_fill(p2,pred)

def test_PT_flood_fill_all():
    pm = PixelMap()
    pm.flood_fill_all(pred)

def test_PT_print():
    pm = PixelMap()
    pm.print(False)

def test_PT_save_image():
    pm = PixelMap()
    pm.save_image("textname")