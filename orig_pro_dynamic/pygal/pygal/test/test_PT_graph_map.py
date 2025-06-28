from pygal.graph.map import BaseMap

def test_PT_enumerate_values():
    bm = BaseMap()
    bm.enumerate_values(serie)

def test_PT_adapt_code():
    bm = BaseMap()
    bm.adapt_code(area_code)