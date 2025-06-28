from sc2.game_state import Blip
from sc2.game_state import Common
from sc2.game_state import EffectData

def test_PT_is_blip():
    b = Blip()
    b.is_blip()

def test_PT_is_snapshot():
    b = Blip()
    b.is_snapshot()

def test_PT_is_visible():
    b = Blip()
    b.is_visible()

def test_PT_alliance():
    b = Blip()
    b.alliance()

def test_PT_is_mine():
    b = Blip()
    b.is_mine()

def test_PT_is_enemy():
    b = Blip()
    b.is_enemy()

def test_PT_position():
    b = Blip()
    b.position()

def test_PT_position3d():
    b = Blip()
    b.position3d()

def test_PT_id():
    ed = EffectData()
    ed.id()

def test_PT_positions():
    ed = EffectData()
    ed.positions()