from sc2.game_data import split_camel_case
from sc2.game_data import GameData
from sc2.game_data import AbilityData
from sc2.game_data import UnitTypeData
from sc2.game_data import UpgradeData
from sc2.game_data import Cost
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
# a3 = UnitTypeId().REACTOR
def test_PT_split_camel_case():
    split_camel_case("testtext")

def test_PT_calculate_ability_cost():
    g = GameData()
    a = AbilityId().MOVE
    g.calculate_ability_cost(a)

def test_PT_id_exists():
    ad = AbilityData()
    a = AbilityId().MOVE
    ad.id_exists(a)

def test_PT_id():
    ad = AbilityData()
    ad.id()

def test_PT_link_name():
    ad = AbilityData()
    ad.link_name()

def test_PT_button_name():
    ad = AbilityData()
    ad.button_name()

def test_PT_friendly_name():
    ad = AbilityData()
    ad.friendly_name()

def test_PT_is_free_morph():
    ad = AbilityData()
    ad.is_free_morph()

def test_PT_cost():
    ad = AbilityData()
    ad.cost()

def test_PT_UnitTypeData_id():
    ut = UnitTypeData()
    ut.id()

def test_PT_UnitTypeData_name():
    ut = UnitTypeData()
    ut.name()

def test_PT_UnitTypeData_creation_ability():
    ut = UnitTypeData()
    ut.creation_ability()

def test_PT_UnitTypeData_attributes():
    ut = UnitTypeData()
    ut.attributes()

def test_PT_UnitTypeData_has_attribute():
    ut = UnitTypeData()
    ut.has_attribute(attr)

def test_PT_UnitTypeData_has_minerals():
    ut = UnitTypeData()
    ut.has_minerals()

def test_PT_UnitTypeData_has_vespene():
    ut = UnitTypeData()
    ut.has_vespene()

def test_PT_UnitTypeData_cargo_size():
    ut = UnitTypeData()
    ut.cargo_size()

def test_PT_UnitTypeData_tech_requirement():
    ut = UnitTypeData()
    ut.tech_requirement()

def test_PT_UnitTypeData_tech_alias():
    ut = UnitTypeData()
    ut.tech_alias()

def test_PT_UnitTypeData_unit_alias():
    ut = UnitTypeData()
    ut.unit_alias()

def test_PT_UnitTypeData_race():
    ut = UnitTypeData()
    ut.race()

def test_PT_UnitTypeData_cost():
    ut = UnitTypeData()
    ut.cost()

def test_PT_UnitTypeData_cost_zerg_corrected():
    ut = UnitTypeData()
    ut.cost_zerg_corrected()

def test_PT_UnitTypeData_morph_cost():
    ut = UnitTypeData()
    ut.morph_cost()

def test_PT_UpgradeData_name():
    ud = UpgradeData()
    ud.name()

def test_PT_UpgradeData_research_ability():
    ud = UpgradeData()
    ud.research_ability()

def test_PT_UpgradeData_cost():
    ud = UpgradeData()
    ud.cost()
