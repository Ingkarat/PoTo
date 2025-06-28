from sc2.position import Pointlike
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2
from sc2.position import Point3
from sc2.position import Size
from sc2.position import React

def test_PT_rounded():
    pl = Pointlike()
    pl.rounded()

def test_PT_position():
    pl = Pointlike()
    pl.position()

def test_PT_distance_to():
    pl = Pointlike()
    pl2 = Pointlike()
    pl3 = Pointlike()
    u = Unit()
    p2 = Point2()
    p3 = Point3()
    pl.distance_to(u)
    pl2.distance_to(p2)
    pl3.distance_to(p3)

def test_PT_distance_to_point2():
    pl = Pointlike()
    p2 = Point2()
    pl.distance_to_point2(p2)

def test_PT_sort_by_distance():
    pl = Pointlike()
    pl2 = Pointlike()
    us = Units()
    p2 = Point2()
    pl.sort_by_distance(us)
    pl2.sort_by_distance([p2])

def test_PT_closest():
    pl = Pointlike()
    pl2 = Pointlike()
    pl3 = Pointlike()
    us = Units()
    p2 = Point2()
    p3 = Point2()
    pl.closest(us)
    pl2.closest([p2])
    pl3.closest({p2})

def test_PT_distance_to_closest():
    pl = Pointlike()
    pl2 = Pointlike()
    pl3 = Pointlike()
    us = Units()
    p2 = Point2()
    p3 = Point2()
    pl.distance_to_closest(us)
    pl2.distance_to_closest([p2])
    pl3.distance_to_closest({p2})

def test_PT_furthest():
    pl = Pointlike()
    pl2 = Pointlike()
    pl3 = Pointlike()
    us = Units()
    p2 = Point2()
    p3 = Point2()
    s = {p2}
    pl.furthest(us)
    pl2.furthest([p2])
    pl3.furthest(s)

def test_PT_distance_to_furthest():
    pl = Pointlike()
    pl2 = Pointlike()
    pl3 = Pointlike()
    us = Units()
    p2 = Point2()
    p3 = Point2()
    s = {p2}
    pl.distance_to_furthest(us)
    pl2.distance_to_furthest([p2])
    pl3.distance_to_furthest(s)

def test_PT_offset():
    pl = Pointlike()
    pl.offset(p)

def test_PT_unit_axes_towards():
    pl = Pointlike()
    pl.unit_axes_towards(p)

def test_PT_towards():
    pl = Pointlike()
    pl2 = Pointlike()
    pl3 = Pointlike()
    pl4 = Pointlike()
    u = Unit()
    p2 = Pointlike()
    i = 1
    f = 1.23
    pl.towards(u,i)
    pl2.towards(u,f)
    pl3.towards(p2,i)
    pl4.towards(p2,f)

def test_PT_from_proto():
    pp = Point2()
    pp.from_proto(data)

def test_PT_x():
    pp = Point2()
    pp.x()

def test_PT_y():
    pp = Point2()
    pp.y()

def test_PT_to2():
    pp = Point2()
    pp.to2()

def test_PT_to3():
    pp = Point2()
    pp.to3()

def test_PT_distance2_to():
    pp = Point2()
    p2 = Point2()
    pp.distance2_to(p2)

def test_PT_random_on_distance():
    pp = Point2()
    pp.random_on_distance(distance)

def test_PT_towards_with_random_angle():
    pp = Point2()
    pp2 = Point2()
    pp3 = Point2()
    pp4 = Point2()
    pp5 = Point2()
    pp6 = Point2()
    p2 = Point2()
    p3 = Point3()
    i = 1
    f = 1.23
    pp.towards_with_random_angle(p2,distance,max_difference)
    pp2.towards_with_random_angle(p3,distance,max_difference)
    pp3.towards_with_random_angle(p, i, max_difference)
    pp4.towards_with_random_angle(p, f, max_difference)
    pp5.towards_with_random_angle(p, distance, i)
    pp6.towards_with_random_angle(p, distance, f)

def test_PT_circle_intersection():
    pp = Point2()
    pp2 = Point2()
    p2 = Point2()
    i = 1
    f = 1.23
    pp.circle_intersection(p2,i)
    pp2.circle_intersection(p2,f)

def test_PT_neighbors4():
    pp = Point2()
    pp.neighbors4()

def test_PT_neighbors8():
    pp = Point2()
    pp.neighbors8()

def test_PT_negative_offset():
    pp = Point2()
    p2 = Point2()
    pp.negative_offset(p2)

def test_PT_is_same_as():
    pp = Point2()
    p2 = Point2()
    pp.is_same_as(p2)

def test_PT_direction_vector():
    pp = Point2()
    p2 = Point2()
    pp.direction_vector(p2)

def test_PT_manhattan_distance():
    pp = Point2()
    p2 = Point2()
    pp.manhattan_distance(p2)

def test_PT_center():
    pp = Point2()
    pp2 = Point2()
    p2 = Point2()
    pp.center({p2})
    pp2.center([p2])

def test_PT_Point3_from_proto():
    pp = Point3()
    pp.from_proto(data)

def test_PT_Point3_z():
    pp = Point3()
    pp.z()

def test_PT_Point3_to3():
    pp = Point3()
    pp.to3()

def test_PT_Size_width():
    sz = Size()
    sz.width()

def test_PT_Size_height():
    sz = Size()
    sz.height()

def test_PT_Rect_from_proto():
    re = Rect()
    re.from_proto()

def test_PT_Rect_x():
    re = Rect()
    re.x()

def test_PT_Rect_y():
    re = Rect()
    re.y()

def test_PT_Rect_():
    re = Rect()
    re.xxx()

def test_PT_Rect_width():
    re = Rect()
    re.width()

def test_PT_Rect_height():
    re = Rect()
    re.height()

def test_PT_Rect_size():
    re = Rect()
    re.size()

def test_PT_Rect_center():
    re = Rect()
    re.center()

def test_PT_Rect_offset():
    re = Rect()
    re.offset(p)