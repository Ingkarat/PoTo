from sc2.units import Units
from sc2.units import UnitSelection
from sc2.unit import Unit
from sc2.position import Point2
from sc2.position import Point3
from sc2.ids.unit_typeid import UnitTypeId

def test_PT_from_proto():
    un = Units()
    un.from_proto()

def test_PT_select():
    un = Units()
    un.select()

def test_PT_copy():
    un = Units()
    un.copy()

def test_PT_amount():
    un = Units()
    un.amount()

def test_PT_empty():
    un = Units()
    un.empty()

def test_PT_exists():
    un = Units()
    un.exists()

def test_PT_find_by_tag():
    un = Units()
    un.find_by_tag(tag)

def test_PT_by_tag():
    un = Units()
    un.by_tag(tag)

def test_PT_first():
    un = Units()
    un.first()

def test_PT_take():
    un = Units()
    i = 1
    un.take(i, True)

def test_PT_random():
    un = Units()
    un.random()

def test_PT_random_or():
    un = Units()
    un.random_or(other)

def test_PT_random_group_of():
    un = Units()
    i = 1
    un.random_group_of(i)

def test_PT_in_attack_range_of():
    un = Units()
    un2 = Units()
    u = Unit()
    i = 1
    f = 1.23
    un.in_attack_range_of(u,i)
    un2.in_attack_range_of(u,f)

def test_PT_closest_distance_to():
    un = Units()
    un2 = Units()
    un3 = Units()
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    un.closest_distance_to(u)
    un2.closest_distance_to(p2)
    un3.closest_distance_to(p3)

def test_PT_furthest_distance_to():
    un = Units()
    un2 = Units()
    un3 = Units()
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    un.furthest_distance_to(u)
    un2.furthest_distance_to(p2)
    un3.furthest_distance_to(p3)

def test_PT_closest_to():
    un = Units()
    un2 = Units()
    un3 = Units()
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    un.closest_to(u)
    un2.closest_to(p2)
    un3.closest_to(p3)

def test_PT_furthest_to():
    un = Units()
    un2 = Units()
    un3 = Units()
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    un.furthest_to(u)
    un2.furthest_to(p2)
    un3.furthest_to(p3)

def test_PT_closer_than():
    un = Units()
    un2 = Units()
    un3 = Units()
    un4 = Units()
    un5 = Units()
    un6 = Units()
    i = 1
    f = 1.23
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    un.closer_than(i,u)
    un2.closer_than(i,p2)
    un3.closer_than(i,p3)
    un4.closer_than(f,u)
    un5.closer_than(f,p2)
    un6.closer_than(f,p3)

def test_PT_further_than():
    un = Units()
    un2 = Units()
    un3 = Units()
    un4 = Units()
    un5 = Units()
    un6 = Units()
    i = 1
    f = 1.23
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    un.further_than(i,u)
    un2.further_than(i,p2)
    un3.further_than(i,p3)
    un4.further_than(f,u)
    un5.further_than(f,p2)
    un6.further_than(f,p3)

def test_PT_subgroup():
    un = Units()
    us = Units()
    un.subgroup(us)

def test_PT_filter():
    un = Units()
    un.filter(pred)

def test_PT_sorted():
    un = Units()
    un.sorted(keyfn,False)

def test_PT_sorted_by_distance_to():
    un = Units()
    un2 = Units()
    u = Unit()
    p2 = Point2()
    un.sorted_by_distance_to(u, False)
    un2.sorted_by_distance_to(p2, False)

def test_PT_tags_in():
    un = Units()
    un2 = Units()
    un3 = Units()
    s = {1,2}
    l = [1,2]
    d = {1:"a"}
    un.tags_in(s)
    un2.tags_in(l)
    un3.tags_in(d)

def test_PT_tags_not_in():
    un = Units()
    un2 = Units()
    un3 = Units()
    s = {1,2}
    l = [1,2]
    d = {1:"a"}
    un.tags_not_in(s)
    un2.tags_not_in(l)
    un3.tags_not_in(d)

def test_PT_of_type():
    un = Units()
    un2 = Units()
    un3 = Units()
    un4 = Units()
    u = UnitTypeId().NEXUS
    u2 = UnitTypeId().SHEEP
    s = {u,u2}
    l = [u]
    d = {u:"a"}
    un.of_type(u)
    un2.of_type(s)
    un3.of_type(l)
    un4.of_type(d)

def test_PT_exclude_type():
    un = Units()
    un2 = Units()
    un3 = Units()
    un4 = Units()
    u = UnitTypeId().NEXUS
    u2 = UnitTypeId().SHEEP
    s = {u,u2}
    l = [u]
    d = {u:"a"}
    un.exclude_type(u)
    un2.exclude_type(s)
    un3.exclude_type(l)
    un4.exclude_type(d)

def test_PT_same_tech():
    un = Units()
    un2 = Units()
    un3 = Units()
    un4 = Units()
    u = UnitTypeId().NEXUS
    u2 = UnitTypeId().SHEEP
    s = {u,u2}
    l = [u]
    d = {u:"a"}
    un.same_tech(u)
    un2.same_tech(s)
    un3.same_tech(l)
    un4.same_tech(d)

def test_PT_same_unit():
    un = Units()
    un2 = Units()
    un3 = Units()
    un4 = Units()
    u = UnitTypeId().NEXUS
    u2 = UnitTypeId().SHEEP
    s = {u,u2}
    l = [u]
    d = {u:"a"}
    un.same_unit(u)
    un2.same_unit(s)
    un3.same_unit(l)
    un4.same_unit(d)

def test_PT_center():
    un = Units()
    un.center()

def test_PT_selected():
    un = Units()
    un.selected()

def test_PT_tags():
    un = Units()
    un.tags()

def test_PT_ready():
    un = Units()
    un.ready()

def test_PT_not_ready():
    un = Units()
    un.not_ready()

def test_PT_noqueue():
    un = Units()
    un.noqueue()

def test_PT_idle():
    un = Units()
    un.idle()

def test_PT_owned():
    un = Units()
    un.owned()

def test_PT_enemy():
    un = Units()
    un.enemy()

def test_PT_flying():
    un = Units()
    un.flying()

def test_PT_not_flying():
    un = Units()
    un.not_flying()

def test_PT_structure():
    un = Units()
    un.structure()

def test_PT_not_structure():
    un = Units()
    un.not_structure()

def test_PT_gathering():
    un = Units()
    un.gathering()

def test_PT_returning():
    un = Units()
    un.returning()

def test_PT_collecting():
    un = Units()
    un.collecting()

def test_PT_visible():
    un = Units()
    un.visible()

def test_PT_mineral_field():
    un = Units()
    un.mineral_field()

def test_PT_vespene_geyser():
    un = Units()
    un.vespene_geyser()

def test_PT_prefer_idle():
    un = Units()
    un.prefer_idle()

def test_PT_prefer_close_to():
    un = Units()
    un.prefer_close_to()

def test_PT_UnitSelection_matches():
    us = UnitSelection()
    us.matches(unit)