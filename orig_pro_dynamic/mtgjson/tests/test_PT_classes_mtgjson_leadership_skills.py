from mtgjson.mtgjson5.classes.mtgjson_leadership_skills import MtgjsonLeadershipSkillsObject

def test_PT_to_json():
    mf = MtgjsonLeadershipSkillsObject()
    mf.to_json()
