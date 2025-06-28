from pygal.svg import Svg

def test_PT_gauge_background():
    s = Svg()
    s.gauge_background()
    
def test_PT_solid_gauge():
    s = Svg()
    s.solid_gauge()