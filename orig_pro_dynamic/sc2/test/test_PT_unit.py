from sc2.unit import PassengerUnit
from sc2.unit import Unit
from sc2.unit import UnitOrder
from sc2.position import Point2
from sc2.position import Point3

def test_PT_type_id():
    pu = PassengerUnit()
    pu.type_id()

def test_PT_name():
    pu = PassengerUnit()
    pu.name()

def test_PT_race():
    pu = PassengerUnit()
    pu.race()

def test_PT_tag():
    pu = PassengerUnit()
    pu.tag()

def test_PT_is_structure():
    pu = PassengerUnit()
    pu.is_structure()

def test_PT_is_light():
    pu = PassengerUnit()
    pu.is_light()

def test_PT_is_armored():
    pu = PassengerUnit()
    pu.is_armored()

def test_PT_is_biological():
    pu = PassengerUnit()
    pu.is_biological()

def test_PT_is_mechanical():
    pu = PassengerUnit()
    pu.is_mechanical()

def test_PT_is_robotic():
    pu = PassengerUnit()
    pu.is_robotic()

def test_PT_is_massive():
    pu = PassengerUnit()
    pu.is_massive()

def test_PT_is_psionic():
    pu = PassengerUnit()
    pu.is_psionic()

def test_PT_cargo_size():
    pu = PassengerUnit()
    pu.cargo_size()

def test_PT_can_attack():
    pu = PassengerUnit()
    pu.can_attack()

def test_PT_can_attack_ground():
    pu = PassengerUnit()
    pu.can_attack_ground()

def test_PT_ground_dps():
    pu = PassengerUnit()
    pu.ground_dps()

def test_PT_ground_range():
    pu = PassengerUnit()
    pu.ground_range()

def test_PT_can_attack_air():
    pu = PassengerUnit()
    pu.can_attack_air()

def test_PT_air_dps():
    pu = PassengerUnit()
    pu.air_dps()

def test_PT_air_range():
    pu = PassengerUnit()
    pu.air_range()

def test_PT_bonus_damage():
    pu = PassengerUnit()
    pu.bonus_damage()

def test_PT_armor():
    pu = PassengerUnit()
    pu.armor()

def test_PT_sight_range():
    pu = PassengerUnit()
    pu.sight_range()

def test_PT_movement_speed():
    pu = PassengerUnit()
    pu.movement_speed()

def test_PT_health():
    pu = PassengerUnit()
    pu.health()

def test_PT_health_max():
    pu = PassengerUnit()
    pu.health_max()

def test_PT_health_percentage():
    pu = PassengerUnit()
    pu.health_percentage()

def test_PT_shield():
    pu = PassengerUnit()
    pu.shield()

def test_PT_shield_max():
    pu = PassengerUnit()
    pu.shield_max()

def test_PT_shield_percentage():
    pu = PassengerUnit()
    pu.shield_percentage()

def test_PT_energy():
    pu = PassengerUnit()
    pu.energy()

def test_PT_energy_max():
    pu = PassengerUnit()
    pu.energy_max()

def test_PT_energy_percentage():
    pu = PassengerUnit()
    pu.energy_percentage()

def test_PT_Unit_is_snapshot():
    un = Unit()
    un.is_snapshot()

def test_PT_Unit_is_visible():
    un = Unit()
    un.is_visible()

def test_PT_Unit_alliance():
    un = Unit()
    un.alliance()

def test_PT_Unit_is_mine():
    un = Unit()
    un.is_mine()

def test_PT_Unit_is_enemy():
    un = Unit()
    un.is_enemy()

def test_PT_Unit_owner_id():
    un = Unit()
    un.owner_id()

def test_PT_Unit_position():
    un = Unit()
    un.position()

def test_PT_Unit_position3d():
    un = Unit()
    un.position3d()

def test_PT_Unit_distance_to():
    un = Unit()
    un2 = Unit()
    un3 = Unit()
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    un.distance_to(u)
    un2.distance_to(p2)
    un3.distance_to(p3)

def test_PT_Unit_facing():
    un = Unit()
    un.facing()

def test_PT_Unit_radius():
    un = Unit()
    un.radius()

def test_PT_Unit_detect_range():
    un = Unit()
    un.detect_range()

def test_PT_Unit_radar_range():
    un = Unit()
    un.radar_range()

def test_PT_Unit_build_progress():
    un = Unit()
    un.build_progress()

def test_PT_Unit_is_ready():
    un = Unit()
    un.is_ready()

def test_PT_Unit_cloak():
    un = Unit()
    un.cloak()

def test_PT_Unit_is_cloaked():
    un = Unit()
    un.is_cloaked()

def test_PT_Unit_is_blip():
    un = Unit()
    un.is_blip()

def test_PT_Unit_is_powered():
    un = Unit()
    un.is_powered()

def test_PT_Unit_is_burrowed():
    un = Unit()
    un.is_burrowed()

def test_PT_Unit_is_flying():
    un = Unit()
    un.is_flying()

def test_PT_Unit_is_psionic():
    un = Unit()
    un.is_psionic()

def test_PT_Unit_is_mineral_field():
    un = Unit()
    un.is_mineral_field()

def test_PT_Unit_is_vespene_geyser():
    un = Unit()
    un.is_vespene_geyser()

def test_PT_Unit_tech_alias():
    un = Unit()
    un.tech_alias()

def test_PT_Unit_unit_alias():
    un = Unit()
    un.unit_alias()

def test_PT_Unit_mineral_contents():
    un = Unit()
    un.mineral_contents()

def test_PT_Unit_vespene_contents():
    un = Unit()
    un.vespene_contents()

def test_PT_Unit_has_vespene():
    un = Unit()
    un.has_vespene()

def test_PT_Unit_weapon_cooldown():
    un = Unit()
    un.weapon_cooldown()

def test_PT_Unit_has_cargo():
    un = Unit()
    un.has_cargo()

def test_PT_Unit_cargo_used():
    un = Unit()
    un.cargo_used()

def test_PT_Unit_cargo_max():
    un = Unit()
    un.cargo_max()

def test_PT_Unit_passengers():
    un = Unit()
    un.passengers()

def test_PT_Unit_passengers_tags():
    un = Unit()
    un.passengers_tags()

def test_PT_Unit_target_in_range():
    un = Unit()
    un.target_in_range()

def test_PT_Unit_is_carrying_minerals():
    un = Unit()
    un.is_carrying_minerals()

def test_PT_Unit_is_carrying_vespene():
    un = Unit()
    un.is_carrying_vespene()

def test_PT_Unit_is_selected():
    un = Unit()
    un.is_selected()

def test_PT_Unit_orders():
    un = Unit()
    un.orders()

def test_PT_Unit_noqueue():
    un = Unit()
    un.noqueue()

def test_PT_Unit_is_moving():
    un = Unit()
    un.is_moving()

def test_PT_Unit_is_attacking():
    un = Unit()
    un.is_attacking()

def test_PT_Unit_is_patrolling():
    un = Unit()
    un.is_patrolling()

def test_PT_Unit_is_gathering():
    un = Unit()
    un.is_gathering()

def test_PT_Unit_is_returning():
    un = Unit()
    un.is_returning()

def test_PT_Unit_is_collecting():
    un = Unit()
    un.is_collecting()

def test_PT_Unit_is_constructing_scv():
    un = Unit()
    un.is_constructing_scv()

def test_PT_Unit_is_repairing():
    un = Unit()
    un.is_repairing()

def test_PT_Unit_order_target():
    un = Unit()
    un.order_target()

def test_PT_Unit_is_idle():
    un = Unit()
    un.is_idle()

def test_PT_Unit_add_on_tag():
    un = Unit()
    un.add_on_tag()

def test_PT_Unit_add_on_land_position():
    un = Unit()
    un.add_on_land_position()

def test_PT_Unit_has_add_on():
    un = Unit()
    un.has_add_on()

def test_PT_Unit_assigned_harvesters():
    un = Unit()
    un.assigned_harvesters()

def test_PT_Unit_ideal_harvesters():
    un = Unit()
    un.ideal_harvesters()

def test_PT_Unit_surplus_harvesters():
    un = Unit()
    un.surplus_harvesters()

def test_PT_Unit_train():
    un = Unit()
    un.train(unit)

def test_PT_Unit_build():
    un = Unit()
    un.build(unit)

def test_PT_Unit_research():
    un = Unit()
    un.research(upgrade)

def test_PT_Unit_has_buff():
    un = Unit()
    un.has_buff(buff)

def test_PT_Unitwarp_in():
    un = Unit()
    un.warp_in(unit,placement)

def test_PT_Unit_attack():
    un = Unit()
    un.attack()

def test_PT_Unit_gather():
    un = Unit()
    un.gather()

def test_PT_Unit_return_resource():
    un = Unit()
    un.return_resource()

def test_PT_Unit_move():
    un = Unit()
    un.move()

def test_PT_Unit_scan_move():
    un = Unit()
    un.scan_move()

def test_PT_Unit_hold_position():
    un = Unit()
    un.hold_position()

def test_PT_Unit_stop():
    un = Unit()
    un.stop()

def test_PT_Unit_patrol():
    un = Unit()
    un.patrol()

def test_PT_Unit_repair():
    un = Unit()
    un.repair()

def test_PT_UnitOrder_from_proto():
    uo = UnitOrder()
    uo.from_proto()
