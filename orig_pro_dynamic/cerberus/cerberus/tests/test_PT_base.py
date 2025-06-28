from cerberus import base
from cerberus.base import UnconcernedValidator
from cerberus.base import Registry
from cerberus.typing import RulesSet

#Registry = base.Registry
#UnconcernedValidator = base.UnconcernedValidator

def test_PT__expand_composed_of_rules():
    d = {"a": 1, "b": 2}
    base._expand_composed_of_rules(d)

def test_PT_dummy_for_rule_validation():
    rule_constraints = "test_string"
    base.dummy_for_rule_validation(rule_constraints)

def test_PT_get():
    rg = Registry()
    rg.get("test", None)

def test_PT_clear_caches():
    uv = UnconcernedValidator()
    uv.clear_caches()

def test_PT_allow_unknown():
    uv = UnconcernedValidator()
    uv.allow_unknown(True)

def test_PT_validated():
    uv = UnconcernedValidator()
    uv.validated()

def test_PT_all():
    rg = Registry()
    rg.all()