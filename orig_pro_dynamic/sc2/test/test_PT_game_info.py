from sc2.game_info import Ramp
from sc2.game_info import GameInfo
from sc2.position import Point2

def test_PT_size():
    r = Ramp()
    r.size()

def test_PT_height_at():
    r = Ramp()
    p2 = Point2()
    r.height_at(p2)

def test_PT_points():
    r = Ramp()
    r.points()

def test_PT_upper():
    r = Ramp()
    r.upper()

def test_PT_upper2_for_ramp_wall():
    r = Ramp()
    r.upper2_for_ramp_wall()

def test_PT_top_center():
    r = Ramp()
    r.top_center()

def test_PT_lower():
    r = Ramp()
    r.lower()

def test_PT_bottom_center():
    r = Ramp()
    r.bottom_center()

def test_PT_barracks_in_middle():
    r = Ramp()
    r.barracks_in_middle()

def test_PT_depot_in_middle():
    r = Ramp()
    r.depot_in_middle()

def test_PT_corner_depots():
    r = Ramp()
    r.corner_depots()

def test_PT_barracks_can_fit_addon():
    r = Ramp()
    r.barracks_can_fit_addon()

def test_PT_barracks_correct_placement():
    r = Ramp()
    r.barracks_correct_placement()

def test_PT_map_center():
    gi = GameInfo()
    gi.map_center()
