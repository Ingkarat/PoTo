from wemake_python_styleguide.options.config import Configuration

def test_all_violations_are_documented(all_module_violations):
    all_module_violations = all_module_violations()
    'Ensures that all violations are documented.'
    for (module, classes) in all_module_violations.items():
        for violation_class in classes:
            assert module.__doc__.count(violation_class.__qualname__) == 2

def test_all_violations_have_versionadded(all_violations):
    all_violations = all_violations()
    'Ensures that all violations have `versionadded` tag.'
    for violation in all_violations:
        assert '.. versionadded:: ' in violation.__doc__

def test_violation_name(all_violations):
    all_violations = all_violations()
    'Ensures that all violations have `Violation` suffix.'
    for violation in all_violations:
        class_name = violation.__qualname__
        assert class_name.endswith('Violation'), class_name

def test_violation_template_ending(all_violations):
    all_violations = all_violations()
    'Ensures that all violation templates do not end with a dot.'
    for violation in all_violations:
        assert not violation.error_template.endswith('.'), violation

def test_previous_codes_versionchanged(all_violations):
    all_violations = all_violations()
    'Tests that we put both in case violation changes.'
    for violation in all_violations:
        previous_codes = getattr(violation, 'previous_codes', None)
        if previous_codes is not None:
            assert violation.__doc__.count('.. versionchanged::') >= len(violation.previous_codes)

def test_configuration(all_violations):
    all_violations = all_violations()
    'Ensures that all configuration options are listed in the docs.'
    option_listed = {option.long_option_name: False for option in Configuration._options}
    for violation in all_violations:
        for listed in option_listed:
            if listed in violation.__doc__:
                option_listed[listed] = True
                assert 'Configuration:' in violation.__doc__
                assert 'Default:' in violation.__doc__
    for (option_item, is_listed) in option_listed.items():
        assert is_listed, option_item
import inspect
from operator import attrgetter, itemgetter
import pytest
from wemake_python_styleguide.violations import best_practices, complexity, consistency, naming, oop, refactoring, system
from wemake_python_styleguide.violations.base import ASTViolation, BaseViolation, MaybeASTViolation, SimpleViolation, TokenizeViolation
VIOLATIONS_MODULES = (system, naming, complexity, consistency, best_practices, refactoring, oop)
_SESSION_SCOPE = 'session'

def _is_violation_class(cls) -> bool:
    base_classes = {ASTViolation, BaseViolation, SimpleViolation, TokenizeViolation, MaybeASTViolation}
    if not inspect.isclass(cls):
        return False
    return issubclass(cls, BaseViolation) and cls not in base_classes

def _load_all_violation_classes():
    classes = {}
    for module in VIOLATIONS_MODULES:
        classes_names_list = inspect.getmembers(module, _is_violation_class)
        only_classes = map(itemgetter(1), classes_names_list)
        classes.update({module: sorted(only_classes, key=attrgetter('code'))})
    return classes

@pytest.fixture(scope=_SESSION_SCOPE)
def all_violations():
    """Loads all violations from the package and creates a flat list."""
    classes = _load_all_violation_classes()
    all_errors_container = []
    for module_classes in classes.values():
        all_errors_container.extend(module_classes)
    return all_errors_container

@pytest.fixture(scope=_SESSION_SCOPE)
def all_controlled_violations():
    """Loads all violations which may be tweaked using `i_control_code`."""
    classes = _load_all_violation_classes()
    controlled_errors_container = []
    for module_classes in classes.values():
        for violation_class in module_classes:
            if '--i-control-code' in violation_class.__doc__:
                controlled_errors_container.append(violation_class)
    return controlled_errors_container

@pytest.fixture(scope=_SESSION_SCOPE)
def all_module_violations():
    """Loads all violations from the package."""
    return _load_all_violation_classes()

@pytest.fixture(scope=_SESSION_SCOPE)
def all_violation_codes(all_module_violations):
    """Loads all codes and their violation classes from the package."""
    all_codes = {}
    for module in all_module_violations.keys():
        all_codes[module] = {violation.code: violation for violation in all_module_violations[module]}
    return all_codes
import inspect
from operator import attrgetter, itemgetter
import pytest
from wemake_python_styleguide.violations import best_practices, complexity, consistency, naming, oop, refactoring, system
from wemake_python_styleguide.violations.base import ASTViolation, BaseViolation, MaybeASTViolation, SimpleViolation, TokenizeViolation
VIOLATIONS_MODULES = (system, naming, complexity, consistency, best_practices, refactoring, oop)
_SESSION_SCOPE = 'session'

def _is_violation_class(cls) -> bool:
    base_classes = {ASTViolation, BaseViolation, SimpleViolation, TokenizeViolation, MaybeASTViolation}
    if not inspect.isclass(cls):
        return False
    return issubclass(cls, BaseViolation) and cls not in base_classes

def _load_all_violation_classes():
    classes = {}
    for module in VIOLATIONS_MODULES:
        classes_names_list = inspect.getmembers(module, _is_violation_class)
        only_classes = map(itemgetter(1), classes_names_list)
        classes.update({module: sorted(only_classes, key=attrgetter('code'))})
    return classes

@pytest.fixture(scope=_SESSION_SCOPE)
def all_violations():
    """Loads all violations from the package and creates a flat list."""
    classes = _load_all_violation_classes()
    all_errors_container = []
    for module_classes in classes.values():
        all_errors_container.extend(module_classes)
    return all_errors_container

@pytest.fixture(scope=_SESSION_SCOPE)
def all_controlled_violations():
    """Loads all violations which may be tweaked using `i_control_code`."""
    classes = _load_all_violation_classes()
    controlled_errors_container = []
    for module_classes in classes.values():
        for violation_class in module_classes:
            if '--i-control-code' in violation_class.__doc__:
                controlled_errors_container.append(violation_class)
    return controlled_errors_container

@pytest.fixture(scope=_SESSION_SCOPE)
def all_module_violations():
    """Loads all violations from the package."""
    return _load_all_violation_classes()

@pytest.fixture(scope=_SESSION_SCOPE)
def all_violation_codes(all_module_violations):
    """Loads all codes and their violation classes from the package."""
    all_codes = {}
    for module in all_module_violations.keys():
        all_codes[module] = {violation.code: violation for violation in all_module_violations[module]}
    return all_codes