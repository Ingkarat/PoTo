def test_all_unique_violation_codes(all_violations):
    all_violations = all_violations()
    'Ensures that all violations have unique violation codes.'
    codes = []
    for violation in all_violations:
        codes.append(int(violation.code))
    assert len(set(codes)) == len(all_violations)

def test_all_violations_correct_numbers(all_module_violations):
    all_module_violations = all_module_violations()
    'Ensures that all violations has correct violation code numbers.'
    assert len(all_module_violations) == 7
    for (index, module) in enumerate(all_module_violations.keys()):
        code_number = index * 100
        for violation_class in all_module_violations[module]:
            assert code_number <= violation_class.code <= code_number + 100 - 1, violation_class.__qualname__

def test_violations_start_zero(all_module_violations):
    all_module_violations = all_module_violations()
    'Ensures that all violations start at zero.'
    for (index, module) in enumerate(all_module_violations.keys()):
        starting_code = min((violation_class.code for violation_class in all_module_violations[module]))
        assert starting_code == index * 100

def test_no_holes(all_violation_codes):
    all_violation_codes = all_violation_codes()
    'Ensures that there are no off-by-one errors.'
    for module_codes in all_violation_codes.values():
        previous_code = None
        for code in sorted(module_codes.keys()):
            if previous_code is not None:
                diff = code - previous_code
                assert diff == 1 or diff > 2, module_codes[code].__qualname__
            previous_code = code
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