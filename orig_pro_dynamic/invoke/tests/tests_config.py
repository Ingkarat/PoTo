import pickle
import os
from os.path import join, expanduser
from invoke.util import six
from mock import patch, call, Mock
import pytest
from pytest_relaxed import raises
from invoke.runners import Local
from invoke.config import Config
from invoke.exceptions import AmbiguousEnvVar, UncastableEnvVar, UnknownFileType, UnpicklableConfigMember
from _util import skip_if_windows, support
pytestmark = pytest.mark.usefixtures('integration')
CONFIGS_PATH = 'configs'
TYPES = ('yaml', 'yml', 'json', 'python')

def _load(kwarg, type_, **kwargs):
    path = join(CONFIGS_PATH, type_ + '/')
    kwargs[kwarg] = path
    return Config(**kwargs)

def prefix_defaults_to_invoke(self):
    assert Config().prefix == 'invoke'

@patch.object(Config, '_load_yaml')
def prefix_informs_config_filenames(self, load_yaml):

    class MyConf(Config):
        prefix = 'other'
    MyConf(system_prefix='dir/')
    load_yaml.assert_any_call('dir/other.yaml')

def prefix_informs_env_var_prefix(self):
    os.environ['OTHER_FOO'] = 'bar'

    class MyConf(Config):
        prefix = 'other'
    c = MyConf(defaults={'foo': 'notbar'})
    c.load_shell_env()
    assert c.foo == 'bar'

def file_prefix_defaults_to_None(self):
    assert Config().file_prefix is None

@patch.object(Config, '_load_yaml')
def file_prefix_informs_config_filenames(self, load_yaml):

    class MyConf(Config):
        file_prefix = 'other'
    MyConf(system_prefix='dir/')
    load_yaml.assert_any_call('dir/other.yaml')

def env_prefix_defaults_to_None(self):
    assert Config().env_prefix is None

def env_prefix_informs_env_vars_loaded(self):
    os.environ['OTHER_FOO'] = 'bar'

    class MyConf(Config):
        env_prefix = 'other'
    c = MyConf(defaults={'foo': 'notbar'})
    c.load_shell_env()
    assert c.foo == 'bar'

@skip_if_windows
def global_defaults_basic_settings(self):
    expected = {'run': {'asynchronous': False, 'disown': False, 'dry': False, 'echo': False, 'echo_stdin': None, 'encoding': None, 'env': {}, 'err_stream': None, 'fallback': True, 'hide': None, 'in_stream': None, 'out_stream': None, 'pty': False, 'replace_env': False, 'shell': '/bin/bash', 'warn': False, 'watchers': []}, 'runners': {'local': Local}, 'sudo': {'password': None, 'prompt': '[sudo] password: ', 'user': None}, 'tasks': {'auto_dash_names': True, 'collection_name': 'tasks', 'dedupe': True, 'executor_class': None, 'search_root': None}, 'timeouts': {'command': None}}
    assert Config.global_defaults() == expected

def init_can_be_empty(self):
    assert Config().__class__ == Config

@patch.object(Config, '_load_yaml')
def init_configure_global_location_prefix(self, load_yaml):
    Config(system_prefix='meh/')
    load_yaml.assert_any_call('meh/invoke.yaml')

@skip_if_windows
@patch.object(Config, '_load_yaml')
def init_default_system_prefix_is_etc(self, load_yaml):
    Config()
    load_yaml.assert_any_call('/etc/invoke.yaml')

@patch.object(Config, '_load_yaml')
def init_configure_user_location_prefix(self, load_yaml):
    Config(user_prefix='whatever/')
    load_yaml.assert_any_call('whatever/invoke.yaml')

@patch.object(Config, '_load_yaml')
def init_default_user_prefix_is_homedir_plus_dot(self, load_yaml):
    Config()
    load_yaml.assert_any_call(expanduser('~/.invoke.yaml'))

@patch.object(Config, '_load_yaml')
def init_configure_project_location(self, load_yaml):
    Config(project_location='someproject').load_project()
    load_yaml.assert_any_call(join('someproject', 'invoke.yaml'))

@patch.object(Config, '_load_yaml')
def init_configure_runtime_path(self, load_yaml):
    Config(runtime_path='some/path.yaml').load_runtime()
    load_yaml.assert_any_call('some/path.yaml')

def init_accepts_defaults_dict_kwarg(self):
    c = Config(defaults={'super': 'low level'})
    assert c.super == 'low level'

def init_overrides_dict_is_first_posarg(self):
    c = Config({'new': 'data', 'run': {'hide': True}})
    assert c.run.hide is True
    assert c.run.warn is False
    assert c.new == 'data'

def init_overrides_dict_is_also_a_kwarg(self):
    c = Config(overrides={'run': {'hide': True}})
    assert c.run.hide is True

@patch.object(Config, 'load_system')
@patch.object(Config, 'load_user')
@patch.object(Config, 'merge')
def init_system_and_user_files_loaded_automatically(self, merge, load_u, load_s):
    Config()
    load_s.assert_called_once_with(merge=False)
    load_u.assert_called_once_with(merge=False)
    merge.assert_called_once_with()

@patch.object(Config, 'load_system')
@patch.object(Config, 'load_user')
def init_can_defer_loading_system_and_user_files(self, load_u, load_s):
    config = Config(lazy=True)
    assert not load_s.called
    assert not load_u.called
    assert config.run.echo is False

def basic_API_can_be_used_directly_after_init(self):
    c = Config({'lots of these': 'tests look similar'})
    assert c['lots of these'] == 'tests look similar'

def basic_API_allows_dict_and_attr_access(self):
    c = Config({'foo': 'bar'})
    assert c.foo == 'bar'
    assert c['foo'] == 'bar'

def basic_API_nested_dict_values_also_allow_dual_access(self):
    c = Config({'foo': 'bar', 'biz': {'baz': 'boz'}})
    assert c.foo == 'bar'
    assert c['foo'] == 'bar'
    assert c.biz.baz == 'boz'
    assert c['biz']['baz'] == 'boz'
    assert c.biz['baz'] == 'boz'
    assert c['biz'].baz == 'boz'

def basic_API_attr_access_has_useful_error_msg(self):
    c = Config()
    try:
        c.nope
    except AttributeError as e:
        expected = "\nNo attribute or config key found for 'nope'\n\nValid keys: ['run', 'runners', 'sudo', 'tasks', 'timeouts']\n\nValid real attributes: ['clear', 'clone', 'env_prefix', 'file_prefix', 'from_data', 'global_defaults', 'load_base_conf_files', 'load_collection', 'load_defaults', 'load_overrides', 'load_project', 'load_runtime', 'load_shell_env', 'load_system', 'load_user', 'merge', 'pop', 'popitem', 'prefix', 'set_project_location', 'set_runtime_path', 'setdefault', 'update']\n".strip()
        assert str(e) == expected
    else:
        assert False, "Didn't get an AttributeError on bad key!"

def basic_API_subkeys_get_merged_not_overwritten(self):
    defaults = {'foo': {'bar': 'baz'}}
    overrides = {'foo': {'notbar': 'notbaz'}}
    c = Config(defaults=defaults, overrides=overrides)
    assert c.foo.notbar == 'notbaz'
    assert c.foo.bar == 'baz'

def basic_API_is_iterable_like_dict(self):
    c = Config(defaults={'a': 1, 'b': 2})
    assert set(c.keys()) == {'a', 'b'}
    assert set(list(c)) == {'a', 'b'}

def basic_API_supports_readonly_dict_protocols(self):
    c = Config(defaults={'foo': 'bar'})
    c2 = Config(defaults={'foo': 'bar'})
    assert 'foo' in c
    assert 'foo' in c2
    assert c == c2
    assert len(c) == 1
    assert c.get('foo') == 'bar'
    if six.PY2:
        assert c.has_key('foo') is True
        assert list(c.iterkeys()) == ['foo']
        assert list(c.itervalues()) == ['bar']
    assert list(c.items()) == [('foo', 'bar')]
    assert list(six.iteritems(c)) == [('foo', 'bar')]
    assert list(c.keys()) == ['foo']
    assert list(c.values()) == ['bar']

def runtime_loading_of_defaults_and_overrides_defaults_can_be_given_via_method(self):
    c = Config()
    assert 'foo' not in c
    c.load_defaults({'foo': 'bar'})
    assert c.foo == 'bar'

def runtime_loading_of_defaults_and_overrides_defaults_can_skip_merging(self):
    c = Config()
    c.load_defaults({'foo': 'bar'}, merge=False)
    assert 'foo' not in c
    c.merge()
    assert c.foo == 'bar'

def runtime_loading_of_defaults_and_overrides_overrides_can_be_given_via_method(self):
    c = Config(defaults={'foo': 'bar'})
    assert c.foo == 'bar'
    c.load_overrides({'foo': 'notbar'})
    assert c.foo == 'notbar'

def runtime_loading_of_defaults_and_overrides_overrides_can_skip_merging(self):
    c = Config()
    c.load_overrides({'foo': 'bar'}, merge=False)
    assert 'foo' not in c
    c.merge()
    assert c.foo == 'bar'

def deletion_methods_pop(self):
    c = Config(defaults={'foo': 'bar'})
    assert c.pop('foo') == 'bar'
    assert c == {}
    assert c.pop('wut', 'fine then') == 'fine then'
    c.nested = {'leafkey': 'leafval'}
    assert c.nested.pop('leafkey') == 'leafval'
    assert c == {'nested': {}}

def deletion_methods_delitem(self):
    """__delitem__"""
    c = Config(defaults={'foo': 'bar'})
    del c['foo']
    assert c == {}
    c.nested = {'leafkey': 'leafval'}
    del c.nested['leafkey']
    assert c == {'nested': {}}

def deletion_methods_delattr(self):
    """__delattr__"""
    c = Config(defaults={'foo': 'bar'})
    del c.foo
    assert c == {}
    c.nested = {'leafkey': 'leafval'}
    del c.nested.leafkey
    assert c == {'nested': {}}

def deletion_methods_clear(self):
    c = Config(defaults={'foo': 'bar'})
    c.clear()
    assert c == {}
    c.nested = {'leafkey': 'leafval'}
    c.nested.clear()
    assert c == {'nested': {}}

def deletion_methods_popitem(self):
    c = Config(defaults={'foo': 'bar'})
    assert c.popitem() == ('foo', 'bar')
    assert c == {}
    c.nested = {'leafkey': 'leafval'}
    assert c.nested.popitem() == ('leafkey', 'leafval')
    assert c == {'nested': {}}

def modification_methods_setitem(self):
    c = Config(defaults={'foo': 'bar'})
    c['foo'] = 'notbar'
    assert c.foo == 'notbar'
    del c['foo']
    c['nested'] = {'leafkey': 'leafval'}
    assert c == {'nested': {'leafkey': 'leafval'}}

def modification_methods_setdefault(self):
    c = Config({'foo': 'bar', 'nested': {'leafkey': 'leafval'}})
    assert c.setdefault('foo') == 'bar'
    assert c.nested.setdefault('leafkey') == 'leafval'
    assert c.setdefault('notfoo', 'notbar') == 'notbar'
    assert c.notfoo == 'notbar'
    nested = c.nested.setdefault('otherleaf', 'otherval')
    assert nested == 'otherval'
    assert c.nested.otherleaf == 'otherval'

def modification_methods_update(self):
    c = Config(defaults={'foo': 'bar', 'nested': {'leafkey': 'leafval'}})
    c.update({'foo': 'notbar'})
    assert c.foo == 'notbar'
    c.nested.update({'leafkey': 'otherval'})
    assert c.nested.leafkey == 'otherval'
    c.update()
    expected = {'foo': 'notbar', 'nested': {'leafkey': 'otherval'}}
    assert c == expected
    c.update(foo='otherbar')
    assert c.foo == 'otherbar'
    c.nested.update([('leafkey', 'yetanotherval'), ('newleaf', 'turnt')])
    assert c.nested.leafkey == 'yetanotherval'
    assert c.nested.newleaf == 'turnt'

def basic_API_reinstatement_of_deleted_values_works_ok(self):
    c = Config(defaults={'foo': 'bar'})
    assert c.foo == 'bar'
    del c['foo']
    assert 'foo' not in c
    assert len(c) == 0
    c.foo = 'formerly bar'
    assert c.foo == 'formerly bar'

def basic_API_deleting_parent_keys_of_deleted_keys_subsumes_them(self):
    c = Config({'foo': {'bar': 'biz'}})
    del c.foo['bar']
    del c.foo
    assert c._deletions == {'foo': None}

def basic_API_supports_mutation_via_attribute_access(self):
    c = Config({'foo': 'bar'})
    assert c.foo == 'bar'
    c.foo = 'notbar'
    assert c.foo == 'notbar'
    assert c['foo'] == 'notbar'

def basic_API_supports_nested_mutation_via_attribute_access(self):
    c = Config({'foo': {'bar': 'biz'}})
    assert c.foo.bar == 'biz'
    c.foo.bar = 'notbiz'
    assert c.foo.bar == 'notbiz'
    assert c['foo']['bar'] == 'notbiz'

def basic_API_real_attrs_and_methods_win_over_attr_proxying(self):

    class MyConfig(Config):
        myattr = None

        def mymethod(self):
            return 7
    c = MyConfig({'myattr': 'foo', 'mymethod': 'bar'})
    assert c.myattr is None
    assert c['myattr'] == 'foo'
    c.myattr = 'notfoo'
    assert c.myattr == 'notfoo'
    assert c['myattr'] == 'foo'
    assert callable(c.mymethod)
    assert c.mymethod() == 7
    assert c['mymethod'] == 'bar'

    def monkeys():
        return 13
    c.mymethod = monkeys
    assert c.mymethod() == 13
    assert c['mymethod'] == 'bar'

def basic_API_config_itself_stored_as_private_name(self):
    c = Config()
    c['foo'] = {'bar': 'baz'}
    c['whatever'] = {'config': 'myconfig'}
    assert c.foo.bar == 'baz'
    assert c.whatever.config == 'myconfig'

def basic_API_inherited_real_attrs_also_win_over_config_keys(self):

    class MyConfigParent(Config):
        parent_attr = 17

    class MyConfig(MyConfigParent):
        pass
    c = MyConfig()
    assert c.parent_attr == 17
    c.parent_attr = 33
    oops = 'Oops! Looks like config won over real attr!'
    assert 'parent_attr' not in c, oops
    assert c.parent_attr == 33
    c['parent_attr'] = 'fifteen'
    assert c.parent_attr == 33
    assert c['parent_attr'] == 'fifteen'

def basic_API_nonexistent_attrs_can_be_set_to_create_new_top_level_configs(self):
    c = Config()
    c.some_setting = 'some_value'
    assert c['some_setting'] == 'some_value'

def basic_API_nonexistent_attr_setting_works_nested_too(self):
    c = Config()
    c.a_nest = {}
    assert c['a_nest'] == {}
    c.a_nest.an_egg = True
    assert c['a_nest']['an_egg']

def basic_API_string_display(self):
    """__str__ and friends"""
    config = Config(defaults={'foo': 'bar'})
    assert repr(config) == "<Config: {'foo': 'bar'}>"

def basic_API_merging_does_not_wipe_user_modifications_or_deletions(self):
    c = Config({'foo': {'bar': 'biz'}, 'error': True})
    c.foo.bar = 'notbiz'
    del c['error']
    assert c['foo']['bar'] == 'notbiz'
    assert 'error' not in c
    c.merge()
    assert c['foo']['bar'] == 'notbiz'
    assert 'error' not in c

def config_file_loading_system_global(self):
    """Systemwide conf files"""
    for type_ in TYPES:
        config = _load('system_prefix', type_, lazy=True)
        assert 'outer' not in config
        config.load_system()
        assert config.outer.inner.hooray == type_

def config_file_loading_system_can_skip_merging(self):
    config = _load('system_prefix', 'yml', lazy=True)
    assert 'outer' not in config._system
    assert 'outer' not in config
    config.load_system(merge=False)
    assert 'outer' in config._system
    assert 'outer' not in config

def config_file_loading_user_specific(self):
    """User-specific conf files"""
    for type_ in TYPES:
        config = _load('user_prefix', type_, lazy=True)
        assert 'outer' not in config
        config.load_user()
        assert config.outer.inner.hooray == type_

def config_file_loading_user_can_skip_merging(self):
    config = _load('user_prefix', 'yml', lazy=True)
    assert 'outer' not in config._user
    assert 'outer' not in config
    config.load_user(merge=False)
    assert 'outer' in config._user
    assert 'outer' not in config

def config_file_loading_project_specific(self):
    """Local-to-project conf files"""
    for type_ in TYPES:
        c = Config(project_location=join(CONFIGS_PATH, type_))
        assert 'outer' not in c
        c.load_project()
        assert c.outer.inner.hooray == type_

def config_file_loading_project_can_skip_merging(self):
    config = Config(project_location=join(CONFIGS_PATH, 'yml'), lazy=True)
    assert 'outer' not in config._project
    assert 'outer' not in config
    config.load_project(merge=False)
    assert 'outer' in config._project
    assert 'outer' not in config

def config_file_loading_loads_no_project_specific_file_if_no_project_location_given(self):
    c = Config()
    assert c._project_path is None
    c.load_project()
    assert list(c._project.keys()) == []
    defaults = ['tasks', 'run', 'runners', 'sudo', 'timeouts']
    assert set(c.keys()) == set(defaults)

def config_file_loading_project_location_can_be_set_after_init(self):
    c = Config()
    assert 'outer' not in c
    c.set_project_location(join(CONFIGS_PATH, 'yml'))
    c.load_project()
    assert c.outer.inner.hooray == 'yml'

def config_file_loading_runtime_conf_via_cli_flag(self):
    c = Config(runtime_path=join(CONFIGS_PATH, 'yaml', 'invoke.yaml'))
    c.load_runtime()
    assert c.outer.inner.hooray == 'yaml'

def config_file_loading_runtime_can_skip_merging(self):
    path = join(CONFIGS_PATH, 'yaml', 'invoke.yaml')
    config = Config(runtime_path=path, lazy=True)
    assert 'outer' not in config._runtime
    assert 'outer' not in config
    config.load_runtime(merge=False)
    assert 'outer' in config._runtime
    assert 'outer' not in config

@raises(UnknownFileType)
def config_file_loading_unknown_suffix_in_runtime_path_raises_useful_error(self):
    c = Config(runtime_path=join(CONFIGS_PATH, 'screw.ini'))
    c.load_runtime()

def config_file_loading_python_modules_dont_load_special_vars(self):
    """Python modules don't load special vars"""
    c = _load('system_prefix', 'python')
    assert c.outer.inner.hooray == 'python'
    for special in ('builtins', 'file', 'package', 'name', 'doc'):
        assert '__{}__'.format(special) not in c

def config_file_loading_python_modules_except_usefully_on_unpicklable_modules(self):
    c = Config()
    c.set_runtime_path(join(support, 'has_modules.py'))
    expected = "'os' is a module.*giving a tasks file.*mistake"
    with pytest.raises(UnpicklableConfigMember, match=expected):
        c.load_runtime(merge=False)

@patch('invoke.config.debug')
def config_file_loading_nonexistent_files_are_skipped_and_logged(self, mock_debug):
    c = Config()
    c._load_yml = Mock(side_effect=IOError(2, 'aw nuts'))
    c.set_runtime_path('is-a.yml')
    c.load_runtime()
    mock_debug.assert_any_call("Didn't see any is-a.yml, skipping.")

@raises(IOError)
def config_file_loading_non_missing_file_IOErrors_are_raised(self):
    c = Config()
    c._load_yml = Mock(side_effect=IOError(17, 'uh, what?'))
    c.set_runtime_path('is-a.yml')
    c.load_runtime()

def collection_level_config_loading_performed_explicitly_and_directly(self):
    c = Config()
    assert 'foo' not in c
    c.load_collection({'foo': 'bar'})
    assert c.foo == 'bar'

def collection_level_config_loading_merging_can_be_deferred(self):
    c = Config()
    assert 'foo' not in c._collection
    assert 'foo' not in c
    c.load_collection({'foo': 'bar'}, merge=False)
    assert 'foo' in c._collection
    assert 'foo' not in c

def comparison_and_hashing_comparison_looks_at_merged_config(self):
    c1 = Config(defaults={'foo': {'bar': 'biz'}})
    c2 = Config(defaults={}, overrides={'foo': {'bar': 'biz'}})
    assert c1 is not c2
    assert c1._defaults != c2._defaults
    assert c1 == c2

def comparison_and_hashing_allows_comparison_with_real_dicts(self):
    c = Config({'foo': {'bar': 'biz'}})
    assert c['foo'] == {'bar': 'biz'}

@raises(TypeError)
def comparison_and_hashing_is_explicitly_not_hashable(self):
    hash(Config())

def env_vars_base_case_defaults_to_INVOKE_prefix(self):
    os.environ['INVOKE_FOO'] = 'bar'
    c = Config(defaults={'foo': 'notbar'})
    c.load_shell_env()
    assert c.foo == 'bar'

def env_vars_non_predeclared_settings_do_not_get_consumed(self):
    os.environ['INVOKE_HELLO'] = "is it me you're looking for?"
    c = Config()
    c.load_shell_env()
    assert 'HELLO' not in c
    assert 'hello' not in c

def env_vars_underscores_top_level(self):
    os.environ['INVOKE_FOO_BAR'] = 'biz'
    c = Config(defaults={'foo_bar': 'notbiz'})
    c.load_shell_env()
    assert c.foo_bar == 'biz'

def env_vars_underscores_nested(self):
    os.environ['INVOKE_FOO_BAR'] = 'biz'
    c = Config(defaults={'foo': {'bar': 'notbiz'}})
    c.load_shell_env()
    assert c.foo.bar == 'biz'

def env_vars_both_types_of_underscores_mixed(self):
    os.environ['INVOKE_FOO_BAR_BIZ'] = 'baz'
    c = Config(defaults={'foo_bar': {'biz': 'notbaz'}})
    c.load_shell_env()
    assert c.foo_bar.biz == 'baz'

@raises(AmbiguousEnvVar)
def env_vars_ambiguous_underscores_dont_guess(self):
    os.environ['INVOKE_FOO_BAR'] = 'biz'
    c = Config(defaults={'foo_bar': 'wat', 'foo': {'bar': 'huh'}})
    c.load_shell_env()

def type_casting_strings_replaced_with_env_value(self):
    os.environ['INVOKE_FOO'] = u'myvalue'
    c = Config(defaults={'foo': 'myoldvalue'})
    c.load_shell_env()
    assert c.foo == u'myvalue'
    assert isinstance(c.foo, six.text_type)

def type_casting_unicode_replaced_with_env_value(self):
    if six.PY3:
        return
    os.environ['INVOKE_FOO'] = 'myunicode'
    c = Config(defaults={'foo': u'myoldvalue'})
    c.load_shell_env()
    assert c.foo == 'myunicode'
    assert isinstance(c.foo, str)

def type_casting_None_replaced(self):
    os.environ['INVOKE_FOO'] = 'something'
    c = Config(defaults={'foo': None})
    c.load_shell_env()
    assert c.foo == 'something'

def type_casting_booleans(self):
    for (input_, result) in (('0', False), ('1', True), ('', False), ('meh', True), ('false', True)):
        os.environ['INVOKE_FOO'] = input_
        c = Config(defaults={'foo': bool()})
        c.load_shell_env()
        assert c.foo == result

def type_casting_boolean_type_inputs_with_non_boolean_defaults(self):
    for input_ in ('0', '1', '', 'meh', 'false'):
        os.environ['INVOKE_FOO'] = input_
        c = Config(defaults={'foo': 'bar'})
        c.load_shell_env()
        assert c.foo == input_

def type_casting_numeric_types_become_casted(self):
    tests = [(int, '5', 5), (float, '5.5', 5.5)]
    if not six.PY3:
        tests.append((long, '5', long(5)))
    for (old, new_, result) in tests:
        os.environ['INVOKE_FOO'] = new_
        c = Config(defaults={'foo': old()})
        c.load_shell_env()
        assert c.foo == result

def type_casting_arbitrary_types_work_too(self):
    os.environ['INVOKE_FOO'] = 'whatever'

    class Meh(object):

        def __init__(self, thing=None):
            pass
    old_obj = Meh()
    c = Config(defaults={'foo': old_obj})
    c.load_shell_env()
    assert isinstance(c.foo, Meh)
    assert c.foo is not old_obj

@raises(UncastableEnvVar)
def uncastable_types__uncastable_type(self, default):
    os.environ['INVOKE_FOO'] = 'stuff'
    c = Config(defaults={'foo': default})
    c.load_shell_env()

def uncastable_types_lists(self):
    self._uncastable_type(['a', 'list'])

def uncastable_types_tuples(self):
    self._uncastable_type(('a', 'tuple'))

def hierarchy_collection_overrides_defaults(self):
    c = Config(defaults={'nested': {'setting': 'default'}})
    c.load_collection({'nested': {'setting': 'collection'}})
    assert c.nested.setting == 'collection'

def hierarchy_systemwide_overrides_collection(self):
    c = Config(system_prefix=join(CONFIGS_PATH, 'yaml/'))
    c.load_collection({'outer': {'inner': {'hooray': 'defaults'}}})
    assert c.outer.inner.hooray == 'yaml'

def hierarchy_user_overrides_systemwide(self):
    c = Config(system_prefix=join(CONFIGS_PATH, 'yaml/'), user_prefix=join(CONFIGS_PATH, 'json/'))
    assert c.outer.inner.hooray == 'json'

def hierarchy_user_overrides_collection(self):
    c = Config(user_prefix=join(CONFIGS_PATH, 'json/'))
    c.load_collection({'outer': {'inner': {'hooray': 'defaults'}}})
    assert c.outer.inner.hooray == 'json'

def hierarchy_project_overrides_user(self):
    c = Config(user_prefix=join(CONFIGS_PATH, 'json/'), project_location=join(CONFIGS_PATH, 'yaml'))
    c.load_project()
    assert c.outer.inner.hooray == 'yaml'

def hierarchy_project_overrides_systemwide(self):
    c = Config(system_prefix=join(CONFIGS_PATH, 'json/'), project_location=join(CONFIGS_PATH, 'yaml'))
    c.load_project()
    assert c.outer.inner.hooray == 'yaml'

def hierarchy_project_overrides_collection(self):
    c = Config(project_location=join(CONFIGS_PATH, 'yaml'))
    c.load_project()
    c.load_collection({'outer': {'inner': {'hooray': 'defaults'}}})
    assert c.outer.inner.hooray == 'yaml'

def hierarchy_env_vars_override_project(self):
    os.environ['INVOKE_OUTER_INNER_HOORAY'] = 'env'
    c = Config(project_location=join(CONFIGS_PATH, 'yaml'))
    c.load_project()
    c.load_shell_env()
    assert c.outer.inner.hooray == 'env'

def hierarchy_env_vars_override_user(self):
    os.environ['INVOKE_OUTER_INNER_HOORAY'] = 'env'
    c = Config(user_prefix=join(CONFIGS_PATH, 'yaml/'))
    c.load_shell_env()
    assert c.outer.inner.hooray == 'env'

def hierarchy_env_vars_override_systemwide(self):
    os.environ['INVOKE_OUTER_INNER_HOORAY'] = 'env'
    c = Config(system_prefix=join(CONFIGS_PATH, 'yaml/'))
    c.load_shell_env()
    assert c.outer.inner.hooray == 'env'

def hierarchy_env_vars_override_collection(self):
    os.environ['INVOKE_OUTER_INNER_HOORAY'] = 'env'
    c = Config()
    c.load_collection({'outer': {'inner': {'hooray': 'defaults'}}})
    c.load_shell_env()
    assert c.outer.inner.hooray == 'env'

def hierarchy_runtime_overrides_env_vars(self):
    os.environ['INVOKE_OUTER_INNER_HOORAY'] = 'env'
    c = Config(runtime_path=join(CONFIGS_PATH, 'json', 'invoke.json'))
    c.load_runtime()
    c.load_shell_env()
    assert c.outer.inner.hooray == 'json'

def hierarchy_runtime_overrides_project(self):
    c = Config(runtime_path=join(CONFIGS_PATH, 'json', 'invoke.json'), project_location=join(CONFIGS_PATH, 'yaml'))
    c.load_runtime()
    c.load_project()
    assert c.outer.inner.hooray == 'json'

def hierarchy_runtime_overrides_user(self):
    c = Config(runtime_path=join(CONFIGS_PATH, 'json', 'invoke.json'), user_prefix=join(CONFIGS_PATH, 'yaml/'))
    c.load_runtime()
    assert c.outer.inner.hooray == 'json'

def hierarchy_runtime_overrides_systemwide(self):
    c = Config(runtime_path=join(CONFIGS_PATH, 'json', 'invoke.json'), system_prefix=join(CONFIGS_PATH, 'yaml/'))
    c.load_runtime()
    assert c.outer.inner.hooray == 'json'

def hierarchy_runtime_overrides_collection(self):
    c = Config(runtime_path=join(CONFIGS_PATH, 'json', 'invoke.json'))
    c.load_collection({'outer': {'inner': {'hooray': 'defaults'}}})
    c.load_runtime()
    assert c.outer.inner.hooray == 'json'

def hierarchy_cli_overrides_override_all(self):
    """CLI-driven overrides win vs all other layers"""
    c = Config(overrides={'outer': {'inner': {'hooray': 'overrides'}}}, runtime_path=join(CONFIGS_PATH, 'json', 'invoke.json'))
    c.load_runtime()
    assert c.outer.inner.hooray == 'overrides'

def hierarchy_yaml_prevents_yml_json_or_python(self):
    c = Config(system_prefix=join(CONFIGS_PATH, 'all-four/'))
    assert 'json-only' not in c
    assert 'python_only' not in c
    assert 'yml-only' not in c
    assert 'yaml-only' in c
    assert c.shared == 'yaml-value'

def hierarchy_yml_prevents_json_or_python(self):
    c = Config(system_prefix=join(CONFIGS_PATH, 'three-of-em/'))
    assert 'json-only' not in c
    assert 'python_only' not in c
    assert 'yml-only' in c
    assert c.shared == 'yml-value'

def hierarchy_json_prevents_python(self):
    c = Config(system_prefix=join(CONFIGS_PATH, 'json-and-python/'))
    assert 'python_only' not in c
    assert 'json-only' in c
    assert c.shared == 'json-value'

def clone_preserves_basic_members(self):
    c1 = Config(defaults={'key': 'default'}, overrides={'key': 'override'}, system_prefix='global', user_prefix='user', project_location='project', runtime_path='runtime.yaml')
    c2 = c1.clone()
    assert c2._defaults == c1._defaults
    assert c2._defaults is not c1._defaults
    assert c2._overrides == c1._overrides
    assert c2._overrides is not c1._overrides
    assert c2._system_prefix == c1._system_prefix
    assert c2._user_prefix == c1._user_prefix
    assert c2._project_prefix == c1._project_prefix
    assert c2.prefix == c1.prefix
    assert c2.file_prefix == c1.file_prefix
    assert c2.env_prefix == c1.env_prefix
    assert c2._runtime_path == c1._runtime_path

def clone_preserves_merged_config(self):
    c = Config(defaults={'key': 'default'}, overrides={'key': 'override'})
    assert c.key == 'override'
    assert c._defaults['key'] == 'default'
    c2 = c.clone()
    assert c2.key == 'override'
    assert c2._defaults['key'] == 'default'
    assert c2._overrides['key'] == 'override'

def clone_preserves_file_data(self):
    c = Config(system_prefix=join(CONFIGS_PATH, 'yaml/'))
    assert c.outer.inner.hooray == 'yaml'
    c2 = c.clone()
    assert c2.outer.inner.hooray == 'yaml'
    assert c2._system == {'outer': {'inner': {'hooray': 'yaml'}}}

@patch.object(Config, '_load_yaml', return_value={'outer': {'inner': {'hooray': 'yaml'}}})
def clone_does_not_reload_file_data(self, load_yaml):
    path = join(CONFIGS_PATH, 'yaml/')
    c = Config(system_prefix=path)
    c2 = c.clone()
    assert c2.outer.inner.hooray == 'yaml'
    calls = load_yaml.call_args_list
    my_call = call('{}invoke.yaml'.format(path))
    try:
        calls.remove(my_call)
        assert my_call not in calls
    except ValueError:
        err = '{} not found in {} even once!'
        assert False, err.format(my_call, calls)

def clone_preserves_env_data(self):
    os.environ['INVOKE_FOO'] = 'bar'
    c = Config(defaults={'foo': 'notbar'})
    c.load_shell_env()
    c2 = c.clone()
    assert c2.foo == 'bar'

def clone_works_correctly_when_subclassed(self):

    class MyConfig(Config):
        pass
    c = MyConfig()
    assert isinstance(c, MyConfig)
    c2 = c.clone()
    assert isinstance(c2, MyConfig)

def into_kwarg_is_not_required(self):
    c = Config(defaults={'meh': 'okay'})
    c2 = c.clone()
    assert c2.meh == 'okay'

def into_kwarg_raises_TypeError_if_value_is_not_Config_subclass(self):
    try:
        Config().clone(into=17)
    except TypeError:
        pass
    else:
        assert False, 'Non-class obj did not raise TypeError!'

    class Foo(object):
        pass
    try:
        Config().clone(into=Foo)
    except TypeError:
        pass
    else:
        assert False, 'Non-subclass did not raise TypeError!'

def into_kwarg_resulting_clones_are_typed_as_new_class(self):

    class MyConfig(Config):
        pass
    c = Config()
    c2 = c.clone(into=MyConfig)
    assert type(c2) is MyConfig

def into_kwarg_non_conflicting_values_are_merged(self):

    class MyConfig(Config):

        @staticmethod
        def global_defaults():
            orig = Config.global_defaults()
            orig['new'] = {'data': 'ohai'}
            return orig
    c = Config(defaults={'other': {'data': 'hello'}})
    c['runtime'] = {'modification': 'sup'}
    c2 = c.clone(into=MyConfig)
    assert c2.new.data == 'ohai'
    assert c2.other.data == 'hello'
    assert c2.runtime.modification == 'sup'

def clone_does_not_deepcopy(self):
    c = Config(defaults={'oh': {'dear': {'god': object()}}, 'shallow': {'objects': ['copy', 'okay']}, 'welp': {'cannot': ['have', {'everything': 'we want'}]}})
    c2 = c.clone()
    assert c is not c2, 'Clone had same identity as original!'
    assert c.oh is not c2.oh, 'Top level key had same identity!'
    assert c.oh.dear is not c2.oh.dear, 'Midlevel key had same identity!'
    err = 'Leaf object() had same identity!'
    assert c.oh.dear.god is not c2.oh.dear.god, err
    assert c.shallow.objects == c2.shallow.objects
    err = 'Shallow list had same identity!'
    assert c.shallow.objects is not c2.shallow.objects, err
    err = 'Huh, a deeply nested dict-in-a-list had different identity?'
    assert c.welp.cannot[1] is c2.welp.cannot[1], err
    err = 'Huh, a deeply nested dict-in-a-list value had different identity?'
    assert c.welp.cannot[1]['everything'] is c2.welp.cannot[1]['everything'], err

def Config__can_be_pickled(self):
    c = Config(overrides={'foo': {'bar': {'biz': ['baz', 'buzz']}}})
    c2 = pickle.loads(pickle.dumps(c))
    assert c == c2
    assert c is not c2
    assert c.foo.bar.biz is not c2.foo.bar.biz