from decimal import Decimal
from importlib import reload
from pkg_resources import Distribution, DistributionNotFound

from pytest import mark

from cerberus import validator_factory, TypeDefinition, Validator
from cerberus.base import UnconcernedValidator
from cerberus.tests import assert_fail, assert_success


def test_pkgresources_version(monkeypatch):
    def create_fake_distribution(name):
        return Distribution(project_name="cerberus", version="1.2.3")

    with monkeypatch.context() as m:
        cerberus = __import__("cerberus")
        m.setattr("pkg_resources.get_distribution", create_fake_distribution)
        reload(cerberus)
        assert cerberus.__version__ == "1.2.3"


def test_version_not_found(monkeypatch):
    def raise_distribution_not_found(name):
        raise DistributionNotFound("pkg_resources cannot get distribution")

    with monkeypatch.context() as m:
        cerberus = __import__("cerberus")
        m.setattr("pkg_resources.get_distribution", raise_distribution_not_found)
        reload(cerberus)
        assert cerberus.__version__ == "unknown"


def test_clear_cache(validator):
    assert len(validator._valid_schemas) > 0
    validator.clear_caches()
    assert len(validator._valid_schemas) == 0


def test_docstring(validator):
    assert validator.__doc__


# Test that testing with the sample schema works as expected
# as there might be rules with side-effects in it


@mark.parametrize(
    "test,document",
    ((assert_fail, {"an_integer": 60}), (assert_success, {"an_integer": 110})),
)
def test_that_test_fails(test, document):
    print("\n", test, document)
    try:
        test(document)
    except AssertionError:
        pass
    else:
        raise AssertionError("test didn't fail")


def test_dynamic_types():
    decimal_type = TypeDefinition("decimal", (Decimal,), ())
    document = {"measurement": Decimal(0)}
    schema = {"measurement": {"type": "decimal"}}

    validator = Validator()
    validator.types_mapping["decimal"] = decimal_type
    assert_success(document, schema, validator)

    class MyValidator(Validator):
        types_mapping = Validator.types_mapping.copy()
        types_mapping["decimal"] = decimal_type

    validator = MyValidator()
    assert_success(document, schema, validator)


def test_mro():
    assert Validator.__mro__ == (
        Validator,
        UnconcernedValidator,
        object,
    ), Validator.__mro__


def test_mixin_init():
    class Mixin(object):
        def __init__(self, *args, **kwargs):
            kwargs['test'] = True
            super().__init__(*args, **kwargs)

    MyValidator = validator_factory("MyValidator", Mixin)
    validator = MyValidator()
    assert validator._config["test"]


def test_sub_init():
    class MyValidator(Validator):
        def __init__(self, *args, **kwargs):
            kwargs['test'] = True
            super().__init__(*args, **kwargs)

    validator = MyValidator()
    assert validator._config["test"]


def test_PT_test_clear_cache():
    validator = Validator()
    test_clear_cache(validator)


def test_PT_test_docstring():
    validator = Validator()
    test_docstring(validator)

def test_PT_test_that_test_fails_1(test, document):
    document = {"an_integer": 60}
    test_that_test_fails(assert_fail, document)

def test_PT_test_that_test_fails_2(test, document):
    document = {"an_integer": 110}
    test_that_test_fails(assert_sucess, document)
"""
def PT_test():
    schema = {'name': {'type': 'string'}}
    v = Validator(schema)
    test_clear_cache(v)
    test_docstring(v)

def PT_test_test_that_test_fails():
    test = assert_fail
    document = {"an_integer": 60}
    test_that_test_fails(test, document)
    test = assert_sucess
    document = {"an_integer": 110}
    test_that_test_fails(test, document)
"""