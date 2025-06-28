from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2
from sc2.position import Point3
from sc2.game_data import AbilityData
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId

def test_PT_enemy_race():
    ba = BotAI()
    ba.enemy_race()

def test_PT_time():
    ba = BotAI()
    ba.time()

def test_PT_time_formatted():
    ba = BotAI()
    ba.time_formatted()

def test_PT_game_info():
    ba = BotAI()
    ba.game_info()

def test_PT_start_location():
    ba = BotAI()
    ba.start_location()

def test_PT_enemy_start_locations():
    ba = BotAI()
    ba.enemy_start_locations()

def test_PT_known_enemy_units():
    ba = BotAI()
    ba.known_enemy_units()

def test_PT_known_enemy_structures():
    ba = BotAI()
    ba.known_enemy_structures()

def test_PT_main_base_ramp():
    ba = BotAI()
    ba.main_base_ramp()

def test_PT_expansion_locations():
    ba = BotAI()
    ba.expansion_locations()

def test_PT_get_available_abilities():
    ba = BotAI()
    u = Unit()
    ba.get_available_abilities(u, False)
    ba2 = BotAI()
    u2 = Unit()
    ba2.get_available_abilities([u2], False)

def test_PT_expand_now():
    ba = BotAI()
    p2 = Point2()
    u = UnitTypeId().NEXUS
    ba.expand_now(u, 10, p2)

def test_PT_get_next_expansion():
    ba = BotAI()
    ba.get_next_expansion()

def test_PT_distribute_workers():
    ba = BotAI()
    ba.distribute_workers()

def test_PT_owned_expansions():
    ba = BotAI()
    ba.owned_expansions()

def test_PT_can_feed():
    ba = BotAI()
    u = UnitTypeId().NEXUS
    ba.can_feed(u)

def test_PT_can_afford():
    ba = BotAI()
    u = UnitTypeId().NEXUS
    ba.can_afford(u, True)

def test_PT_can_cast():
    ba = BotAI()
    u = Unit()
    a = AbilityId()
    u2 = Unit()
    ba.can_cast(ba,u,a,u2,False,[a])

def test_PT_select_build_worker():
    ba = BotAI()
    p1 = Unit()
    ba2 = BotAI()
    p2 = Point2()
    ba3 = BotAI()
    p3 = Point3()
    ba.select_build_worker(p1, False)
    ba2.select_build_worker(p2, False)
    ba3.select_build_worker(p3, False)

def test_PT_can_place():
    ba = BotAI()
    a1 = AbilityData()
    p1 = Point2()
    ba2 = BotAI()
    a2 = AbilityId().MOVE
    p2 = Point2()
    ba3 = BotAI()
    a3 = UnitTypeId().REACTOR
    p3 = Point2()
    ba.can_place(a1, p1)
    ba2.can_place(a2, p2)
    ba3.can_place(a3, p3)

def test_PT_find_placement():
    ba = BotAI()
    b = UnitTypeId().REACTOR
    n = Unit()
    ba2 = BotAI()
    p2 = Point2()
    ba3 = BotAI()
    p3 = Point3()
    ba.find_placement(b,n,20,True,2)
    ba2.find_placement(b,p2,20,True,2)
    ba3.find_placement(b,p3,20,True,2)

def test_PT_already_pending_upgrade():
    ba = BotAI()
    u = UnitTypeId().REACTOR
    ba.already_pending_upgrade(u)

def test_PT_already_pending():
    ba = BotAI()
    u = UpgradeID().HALTECH
    ba2 = BotAI()
    u2 = UnitTypeId().REACTOR
    ba.already_pending(u, False)
    ba2.already_pending(u2, False)

def test_PT_build():
    ba = BotAI()
    b = UnitTypeId().REACTOR
    n = Point2()
    u = Unit()
    ba.build(b,n,20,u,True,2)
    ba2 = BotAI()
    b2 = UnitTypeId().REACTOR
    n2 = Point3()
    u2 = Unit()
    ba2.build(b2,n2,20,u2,True,2)

def test_PT_do():
    ba = BotAI()
    ba.do(a)

def test_PT_do_actions():
    ba = BotAI()
    ba.do_actions(["UnitCommand"])

def test_PT_chat_send():
    ba = BotAI()
    ba.chat_send("chat")

def test_PT_get_terrain_height():
    ba = BotAI()
    p = Point2()
    ba.get_terrain_height(p)
    ba2 = BotAI()
    p2 = Point3()
    ba2.get_terrain_height(p2)
    ba3 = BotAI()
    p3 = Unit()
    ba3.get_terrain_height(p3)

def test_PT_in_placement_grid():
    ba = BotAI()
    p = Point2()
    ba.in_placement_grid(p)
    ba2 = BotAI()
    p2 = Point3()
    ba2.in_placement_grid(p2)
    ba3 = BotAI()
    p3 = Unit()
    ba3.in_placement_grid(p3)

def test_PT_in_pathing_grid():
    ba = BotAI()
    p = Point2()
    ba.in_pathing_grid(p)
    ba2 = BotAI()
    p2 = Point3()
    ba2.in_pathing_grid(p2)
    ba3 = BotAI()
    p3 = Unit()
    ba3.in_pathing_grid(p3)

def test_PT_is_visible():
    ba = BotAI()
    p = Point2()
    ba.is_visible(p)
    ba2 = BotAI()
    p2 = Point3()
    ba2.is_visible(p2)
    ba3 = BotAI()
    p3 = Unit()
    ba3.is_visible(p3)

def test_PT_has_creep():
    ba = BotAI()
    p = Point2()
    ba.has_creep(p)
    ba2 = BotAI()
    p2 = Point3()
    ba2.has_creep(p2)
    ba3 = BotAI()
    p3 = Unit()
    ba3.has_creep(p3)

def test_PT_issue_events():
    ba = BotAI()
    ba.issue_events()

def test_PT_on_unit_destroyed():
    ba = BotAI()
    ba.on_unit_destroyed(ut)

def test_PT_on_unit_created():
    ba = BotAI()
    u = Unit()
    ba.on_unit_created(u)

def test_PT_on_building_construction_started():
    ba = BotAI()
    u = Unit()
    ba.on_building_construction_started()

def test_PT_on_building_construction_complete():
    ba = BotAI()
    u = Unit()
    ba.on_building_construction_complete()

def test_PT_on_start():
    ba = BotAI()
    ba.on_start()

def test_PT_on_step():
    ba = BotAI()
    ba.on_step()

def test_PT_on_end():
    ba = BotAI()
    ba.on_end()

def test_PT_action_result():
    c = CanAffordWrapper()
    c.action_result()