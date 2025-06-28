from sc2.portconfig import Portconfig

def test_PT_as_json():
    pc = Portconfig()
    pc.as_json()

def test_PT_from_json():
    pc = Portconfig()
    pc.from_json()