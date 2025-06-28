from sc2.power_source import PowerSource
from sc2.power_source import PsionicMatrix

def test_PT_from_proto():
    ps = PowerSource()
    ps.from_proto(proto)

def test_PT_covers():
    ps = PowerSource()
    ps.covers(position)

def test_PT_PsionicMatrix_from_proto():
    pm = PsionicMatrix()
    pm.from_proto(proto)

def test_PT_PsionicMatrix_covers():
    pm = PsionicMatrix()
    pm.covers(position)