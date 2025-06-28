from sc2.client import Client
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2
from sc2.position import Point3
from sc2.ids.ability_id import AbilityId

def test_PT_in_game():
    c = Client()
    c.in_game()

def test_PT_join_game():
    c = Client()
    c.join_game()

def test_PT_leave():
    c = Client()
    c.leave()

def test_PT_debug_leave():
    c = Client()
    c.debug_leave()

def test_PT_save_replay():
    c = Client()
    c.save_replay("testpath")

def test_PT_observation():
    c = Client()
    c.observation()

def test_PT_step():
    c = Client()
    c.step()

def test_PT_get_game_data():
    c = Client()
    c.get_game_data()

def test_PT_get_game_info():
    c = Client()
    c.get_game_info()

def test_PT_actions():
    c = Client()
    c.actions(actions, game_data, False)

def test_PT_query_pathing():
    c = Client()
    c2 = Client()
    c3 = Client()
    c4 = Client()
    c5 = Client()
    c6 = Client()
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    pp2 = Point2()
    pp3 = Point3()
    c.query_pathing(u, pp2)
    c2.query_pathing(u, pp3)
    c3.query_pathing(p2, pp2)
    c4.query_pathing(p2, pp3)
    c5.query_pathing(p3, pp2)
    c6.query_pathing(p3, pp3)

def test_PT_query_building_placement():
    c = Client()
    c2 = Client()
    c3 = Client()
    a = AbilityId().MOVE
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    c.query_building_placement(a,u,True)
    c2.query_building_placement(a,p2,True)
    c3.query_building_placement(a,p3,True)

def test_PT_query_available_abilities():
    c = Client()
    c2 = Client()
    u = Unit()
    c.query_available_abilities([u], False)
    c2.query_available_abilities("Units", False)

def test_PT_chat_send():
    c = Client()
    c.chat_send("testtext", True)

def test_PT_debug_create_unit():
    c = Client()
    c.debug_create_unit(unit_spawn_commands)

def test_PT_debug_kill_unit():
    c = Client()
    c2 = Client()
    c3 = Client()
    us = Units()
    c.debug_kill_unit(us)
    c2.debug_kill_unit([1,2])
    c3.debug_kill_unit({3,4})

def test_PT_move_camera():
    c = Client()
    c2 = Client()
    c3 = Client()
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    c.move_camera(u)
    c2.move_camera(p2)
    c3.move_camera(p3)

def test_PT_move_camera_spatial():
    c = Client()
    c2 = Client()
    p2 = Point2()
    p3 = Point3()
    c.move_camera_spatial(p2)
    c2.move_camera_spatial(p3)

def test_PT_debug_text():
    c = Client()
    c2 = Client()
    c3 = Client()
    c4 = Client()
    c.debug_text("text", [1], (0, 255, 0), 16)
    c2.debug_text("text", {1}, (0, 255, 0), 16)
    c3.debug_text(["text"], [1], (0, 255, 0), 16)
    c4.debug_text(["text"], {1}, (0, 255, 0), 16)


def test_PT_debug_text_simple():
    c = Client()
    c.debug_text_simple("testtext")

def test_PT_debug_text_screen():
    c = Client()
    c2 = Client()
    c3 = Client()
    c4 = Client()
    t = "testtext"
    p2 = Point2()
    p3 = Point3()
    tu = (1,2)
    l = [1,2]
    c.debug_text_screen(t,p2)
    c2.debug_text_screen(t,p3)
    c3.debug_text_screen(t,tu)
    c4.debug_text_screen(t,l)

def test_PT_debug_text_2d():
    c = Client()
    c2 = Client()
    c3 = Client()
    c4 = Client()
    t = "testtext"
    p2 = Point2()
    p3 = Point3()
    tu = (1,2)
    l = [1,2]
    c.debug_text_2d(t,p2)
    c2.debug_text_2d(t,p3)
    c3.debug_text_2d(t,tu)
    c4.debug_text_2d(t,l)

def test_PT_debug_text_world():
    c = Client()
    c2 = Client()
    c3 = Client()
    t = "testtext"
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    c.debug_text_world(t,u)
    c2.debug_text_world(t,p2)
    c3.debug_text_world(t,p3)

def test_PT_debug_text_3d():
    c = Client()
    c2 = Client()
    c3 = Client()
    t = "testtext"
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    c.debug_text_3d(t,u)
    c2.debug_text_3d(t,p2)
    c3.debug_text_3d(t,p3)

def test_PT_debug_line_out():
    c = Client()
    c2 = Client()
    c3 = Client()
    c4 = Client()
    c5 = Client()
    c6 = Client()
    c7 = Client()
    c8 = Client()
    c9 = Client()
    u = Unit()
    ua = Unit()
    p2 = Point2()
    p2a = Point2()
    p3 = Point3()
    p3a = Point3()
    c.debug_line_out(u,ua)
    c2.debug_line_out(u,p2a)
    c3.debug_line_out(u,p3a)
    c4.debug_line_out(p2,ua)
    c5.debug_line_out(p2,p2a)
    c6.debug_line_out(p2,p3a)
    c7.debug_line_out(p3,ua)
    c8.debug_line_out(p3,p2a)
    c9.debug_line_out(p3,p3a)

def test_PT_debug_box_out():
    c = Client()
    c2 = Client()
    c3 = Client()
    c4 = Client()
    c5 = Client()
    c6 = Client()
    c7 = Client()
    c8 = Client()
    c9 = Client()
    u = Unit()
    ua = Unit()
    p2 = Point2()
    p2a = Point2()
    p3 = Point3()
    p3a = Point3()
    c.debug_box_out(u,ua)
    c2.debug_box_out(u,p2a)
    c3.debug_box_out(u,p3a)
    c4.debug_box_out(p2,ua)
    c5.debug_box_out(p2,p2a)
    c6.debug_box_out(p2,p3a)
    c7.debug_box_out(p3,ua)
    c8.debug_box_out(p3,p2a)
    c9.debug_box_out(p3,p3a)

def test_PT_debug_sphere_out():
    c = Client()
    c2 = Client()
    c3 = Client()
    c4 = Client()
    c5 = Client()
    c6 = Client()
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    i = 1
    f = 1.2
    c.debug_sphere_out(u,i)
    c2.debug_sphere_out(u,f)
    c3.debug_sphere_out(p2,i)
    c4.debug_sphere_out(p2,f)
    c5.debug_sphere_out(p3,i)
    c6.debug_sphere_out(p3,f)

def test_PT_send_debug():
    c = Client()
    c.send_debug()

def test_PT_to_debug_color():
    c = Client()
    c.to_debug_color(color)

def test_PT_to_debug_point():
    c = Client()
    c2 = Client()
    c3 = Client()
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    c.to_debug_point(u)
    c2.to_debug_point(p2)
    c3.to_debug_point(p3)

def test_PT_to_debug_message():
    c = Client()
    c2 = Client()
    t = "testtext"
    p2 = Point2()
    p3 = Point3()
    c.to_debug_message(t,None,p2)
    c2.to_debug_message(t,None,p3)
