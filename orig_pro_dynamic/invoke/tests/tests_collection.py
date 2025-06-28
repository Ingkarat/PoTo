from __future__ import print_function
import operator
from invoke.util import reduce
from pytest import raises
from invoke.collection import Collection
from invoke.tasks import task, Task
from _util import load, support_path

@task
def _mytask(c):
    print('woo!')

def _func(c):
    pass

def init_can_accept_task_varargs(self):
    """can accept tasks as *args"""

    @task
    def task1(c):
        pass

    @task
    def task2(c):
        pass
    c = Collection(task1, task2)
    assert 'task1' in c
    assert 'task2' in c

def init_can_accept_collections_as_varargs_too(self):
    sub = Collection('sub')
    ns = Collection(sub)
    assert ns.collections['sub'] == sub

def init_kwargs_act_as_name_args_for_given_objects(self):
    sub = Collection()

    @task
    def task1(c):
        pass
    ns = Collection(loltask=task1, notsub=sub)
    assert ns['loltask'] == task1
    assert ns.collections['notsub'] == sub

def init_initial_string_arg_acts_as_name(self):
    sub = Collection('sub')
    ns = Collection(sub)
    assert ns.collections['sub'] == sub

def init_initial_string_arg_meshes_with_varargs_and_kwargs(self):

    @task
    def task1(c):
        pass

    @task
    def task2(c):
        pass
    sub = Collection('sub')
    ns = Collection('root', task1, sub, sometask=task2)
    for (x, y) in ((ns.name, 'root'), (ns['task1'], task1), (ns.collections['sub'], sub), (ns['sometask'], task2)):
        assert x == y

def init_accepts_load_path_kwarg(self):
    assert Collection().loaded_from is None
    assert Collection(loaded_from='a/path').loaded_from == 'a/path'

def init_accepts_auto_dash_names_kwarg(self):
    assert Collection().auto_dash_names is True
    assert Collection(auto_dash_names=False).auto_dash_names is False

def useful_special_methods__meh(self):

    @task
    def task1(c):
        pass

    @task
    def task2(c):
        pass

    @task
    def task3(c):
        pass
    submeh = Collection('submeh', task3)
    return Collection('meh', task1, task2, submeh)

def useful_special_methods_setup(self):
    self.c = self._meh()

def useful_special_methods_repr_(self):
    """__repr__"""
    expected = "<Collection 'meh': task1, task2, submeh...>"
    assert expected == repr(self.c)

def useful_special_methods_equality_consists_of_name_tasks_and_collections(self):
    assert self.c == self._meh()
    diffname = self._meh()
    diffname.name = 'notmeh'
    assert diffname != self.c
    assert not diffname == self.c
    diffcols = self._meh()
    del diffcols.collections['submeh']
    assert diffcols != self.c
    difftasks = self._meh()
    del difftasks.tasks['task1']
    assert difftasks != self.c

def useful_special_methods_boolean_is_equivalent_to_tasks_and_or_collections(self):
    assert not Collection()

    @task
    def foo(c):
        pass
    assert Collection(foo)
    assert Collection(foo=Collection(foo))
    assert not Collection(foo=Collection())

def from_module_setup(self):
    self.c = Collection.from_module(load('integration'))

def parameters_setup(self):
    self.mod = load('integration')
    self.from_module = Collection.from_module

def parameters_name_override(self):
    assert Collection.from_module(self.mod).name == 'integration'
    override = Collection.from_module(self.mod, name='not-integration')
    assert override.name == 'not-integration'

def parameters_inline_configuration(self):
    assert Collection.from_module(self.mod).configuration() == {}
    coll = Collection.from_module(self.mod, config={'foo': 'bar'})
    assert coll.configuration() == {'foo': 'bar'}

def parameters_name_and_config_simultaneously(self):
    c = Collection.from_module(self.mod, 'the name', {'the': 'config'})
    assert c.name == 'the name'
    assert c.configuration() == {'the': 'config'}

def parameters_auto_dash_names_passed_to_constructor(self):
    assert Collection.from_module(self.mod).auto_dash_names is True
    coll = Collection.from_module(self.mod, auto_dash_names=False)
    assert coll.auto_dash_names is False

def from_module_adds_tasks(self):
    assert 'print-foo' in self.c

def from_module_derives_collection_name_from_module_name(self):
    assert Collection.from_module(load('integration')).name == 'integration'

def from_module_copies_docstring_from_module(self):
    expected = 'A semi-integration-test style fixture spanning multiple feature examples.'
    assert Collection.from_module(load('integration')).__doc__.strip().split('\n')[0] == expected

def from_module_works_great_with_subclassing(self):

    class MyCollection(Collection):
        pass
    c = MyCollection.from_module(load('integration'))
    assert isinstance(c, MyCollection)

def from_module_submodule_names_are_stripped_to_last_chunk(self):
    with support_path():
        from package import module
    c = Collection.from_module(module)
    assert module.__name__ == 'package.module'
    assert c.name == 'module'
    assert 'mytask' in c

def from_module_honors_explicit_collections(self):
    coll = Collection.from_module(load('explicit_root'))
    assert 'top-level' in coll.tasks
    assert 'sub-level' in coll.collections
    assert 'sub-task' not in coll.tasks

def from_module_allows_tasks_with_explicit_names_to_override_bound_name(self):
    coll = Collection.from_module(load('subcollection_task_name'))
    assert 'explicit-name' in coll.tasks

def from_module_returns_unique_Collection_objects_for_same_input_module(self):
    mod = load('integration')
    c1 = Collection.from_module(mod)
    c2 = Collection.from_module(mod)
    assert c1 is not c2
    mod2 = load('explicit_root')
    c3 = Collection.from_module(mod2)
    c4 = Collection.from_module(mod2)
    assert c3 is not c4

def explicit_root_ns_setup(self):
    mod = load('explicit_root')
    mod.ns.configure({'key': 'builtin', 'otherkey': 'yup', 'subconfig': {'mykey': 'myvalue'}})
    mod.ns.name = 'builtin_name'
    self.unchanged = Collection.from_module(mod)
    self.changed = Collection.from_module(mod, name='override_name', config={'key': 'override', 'subconfig': {'myotherkey': 'myothervalue'}})

def explicit_root_ns_inline_config_with_root_namespaces_overrides_builtin(self):
    assert Collection.from_module(mod).configuration()['key'] == 'builtin'
    assert Collection.from_module(mod, name='override_name', config={'key': 'override', 'subconfig': {'myotherkey': 'myothervalue'}}).configuration()['key'] == 'override'

def explicit_root_ns_inline_config_overrides_via_merge_not_replacement(self):
    assert 'otherkey' in Collection.from_module(mod, name='override_name', config={'key': 'override', 'subconfig': {'myotherkey': 'myothervalue'}}).configuration()

def explicit_root_ns_config_override_merges_recursively(self):
    subconfig = Collection.from_module(mod, name='override_name', config={'key': 'override', 'subconfig': {'myotherkey': 'myothervalue'}}).configuration()['subconfig']
    assert subconfig['mykey'] == 'myvalue'

def explicit_root_ns_inline_name_overrides_root_namespace_object_name(self):
    assert Collection.from_module(mod).name == 'builtin-name'
    assert Collection.from_module(mod, name='override_name', config={'key': 'override', 'subconfig': {'myotherkey': 'myothervalue'}}).name == 'override-name'

def explicit_root_ns_root_namespace_object_name_overrides_module_name(self):
    assert Collection.from_module(mod).name == 'builtin-name'

def explicit_root_ns_docstring_still_copied_from_module(self):
    expected = 'EXPLICIT LYRICS'
    assert Collection.from_module(mod).__doc__.strip() == expected
    assert Collection.from_module(mod, name='override_name', config={'key': 'override', 'subconfig': {'myotherkey': 'myothervalue'}}).__doc__.strip() == expected

def add_task_setup(self):
    self.c = Collection()

def add_task_associates_given_callable_with_given_name(self):
    Collection().add_task(_mytask, 'foo')
    assert self.c['foo'] == _mytask

def add_task_uses_function_name_as_implicit_name(self):
    Collection().add_task(_mytask)
    assert '_mytask' in self.c

def add_task_prefers_name_kwarg_over_task_name_attr(self):
    Collection().add_task(Task(_func, name='notfunc'), name='yesfunc')
    assert 'yesfunc' in self.c
    assert 'notfunc' not in self.c

def add_task_prefers_task_name_attr_over_function_name(self):
    Collection().add_task(Task(_func, name='notfunc'))
    assert 'notfunc' in self.c
    assert '_func' not in self.c

def add_task_raises_ValueError_if_no_name_found(self):

    class Callable(object):

        def __call__(self):
            pass
    with raises(ValueError):
        Collection().add_task(Task(Callable()))

def add_task_raises_ValueError_on_multiple_defaults(self):
    t1 = Task(_func, default=True)
    t2 = Task(_func, default=True)
    Collection().add_task(t1, 'foo')
    with raises(ValueError):
        Collection().add_task(t2, 'bar')

def add_task_raises_ValueError_if_task_added_mirrors_subcollection_name(self):
    Collection().add_collection(Collection('sub'))
    with raises(ValueError):
        Collection().add_task(_mytask, 'sub')

def add_task_allows_specifying_task_defaultness(self):
    Collection().add_task(_mytask, default=True)
    assert Collection().default == '_mytask'

def add_task_specifying_default_False_overrides_task_setting(self):

    @task(default=True)
    def its_me(c):
        pass
    Collection().add_task(its_me, default=False)
    assert Collection().default is None

def add_task_allows_specifying_aliases(self):
    Collection().add_task(_mytask, aliases=('task1', 'task2'))
    assert self.c['_mytask'] is self.c['task1'] is self.c['task2']

def add_task_aliases_are_merged(self):

    @task(aliases=('foo', 'bar'))
    def biz(c):
        pass
    Collection().add_task(biz, aliases=['baz', 'boz'])
    for x in ('foo', 'bar', 'biz', 'baz', 'boz'):
        assert self.c[x] is self.c['biz']

def add_collection_setup(self):
    self.c = Collection()

def add_collection_adds_collection_as_subcollection_of_self(self):
    c2 = Collection('foo')
    Collection().add_collection(c2)
    assert 'foo' in Collection().collections

def add_collection_can_take_module_objects(self):
    Collection().add_collection(load('integration'))
    assert 'integration' in Collection().collections

def add_collection_raises_ValueError_if_collection_without_name(self):
    root = Collection()
    sub = Collection()
    with raises(ValueError):
        root.add_collection(sub)

def add_collection_raises_ValueError_if_collection_named_same_as_task(self):
    Collection().add_task(_mytask, 'sub')
    with raises(ValueError):
        Collection().add_collection(Collection('sub'))

def getitem_setup(self):
    self.c = Collection()

def getitem_finds_own_tasks_by_name(self):
    Collection().add_task(_mytask, 'foo')
    assert self.c['foo'] == _mytask

def getitem_finds_subcollection_tasks_by_dotted_name(self):
    sub = Collection('sub')
    sub.add_task(_mytask)
    Collection().add_collection(sub)
    assert self.c['sub._mytask'] == _mytask

def getitem_honors_aliases_in_own_tasks(self):
    t = Task(_func, aliases=['bar'])
    Collection().add_task(t, 'foo')
    assert self.c['bar'] == t

def getitem_honors_subcollection_task_aliases(self):
    Collection().add_collection(load('decorators'))
    assert 'decorators.bar' in self.c

def getitem_honors_own_default_task_with_no_args(self):
    t = Task(_func, default=True)
    Collection().add_task(t)
    assert self.c[''] == t

def getitem_honors_subcollection_default_tasks_on_subcollection_name(self):
    sub = Collection.from_module(load('decorators'))
    Collection().add_collection(sub)
    assert self.c['decorators.biz'] is sub['biz']
    assert self.c['decorators'] is self.c['decorators.biz']

def getitem_raises_ValueError_for_no_name_and_no_default(self):
    with raises(ValueError):
        self.c['']

def getitem_ValueError_for_empty_subcol_task_name_and_no_default(self):
    Collection().add_collection(Collection('whatever'))
    with raises(ValueError):
        self.c['whatever']

def to_contexts_setup(self):

    @task
    def mytask(c, text, boolean=False, number=5):
        print(text)

    @task(aliases=['mytask27'])
    def mytask2(c):
        pass

    @task(aliases=['othertask'], default=True)
    def subtask(c):
        pass
    sub = Collection('sub', subtask)
    self.c = Collection(mytask, mytask2, sub)
    self.contexts = Collection(mytask, mytask2, sub).to_contexts()
    alias_tups = [list(x.aliases) for x in self.contexts]
    self.aliases = reduce(operator.add, alias_tups, [])
    self.context = [x for x in self.contexts if x.name == 'mytask'][0]

def to_contexts_returns_iterable_of_Contexts_corresponding_to_tasks(self):
    assert [x for x in self.contexts if x.name == 'mytask'][0].name == 'mytask'
    assert len(self.contexts) == 3

def auto_dash_names_context_names_automatically_become_dashed(self):

    @task
    def my_task(c):
        pass
    contexts = Collection(my_task).to_contexts()
    assert contexts[0].name == 'my-task'

def auto_dash_names_percolates_to_subcollection_tasks(self):

    @task
    def outer_task(c):
        pass

    @task
    def inner_task(c):
        pass
    coll = Collection(outer_task, inner=Collection(inner_task))
    contexts = coll.to_contexts()
    expected = {'outer-task', 'inner.inner-task'}
    assert {x.name for x in contexts} == expected

def auto_dash_names_percolates_to_subcollection_names(self):

    @task
    def my_task(c):
        pass
    coll = Collection(inner_coll=Collection(my_task))
    contexts = coll.to_contexts()
    assert contexts[0].name == 'inner-coll.my-task'

def auto_dash_names_aliases_are_dashed_too(self):

    @task(aliases=['hi_im_underscored'])
    def whatever(c):
        pass
    contexts = Collection(whatever).to_contexts()
    assert 'hi-im-underscored' in contexts[0].aliases

def auto_dash_names_leading_and_trailing_underscores_are_not_affected(self):

    @task
    def _what_evers_(c):
        pass

    @task
    def _inner_cooler_(c):
        pass
    inner = Collection('inner', _inner_cooler_)
    contexts = Collection(_what_evers_, inner).to_contexts()
    expected = {'_what-evers_', 'inner._inner-cooler_'}
    assert {x.name for x in contexts} == expected

def auto_dash_names__nested_underscores(self, auto_dash_names=None):

    @task(aliases=['other_name'])
    def my_task(c):
        pass

    @task(aliases=['other_inner'])
    def inner_task(c):
        pass
    sub = Collection('inner_coll', inner_task)
    return Collection(my_task, sub, auto_dash_names=auto_dash_names)

def auto_dash_names_honors_init_setting_on_topmost_namespace(self):
    coll = self._nested_underscores(auto_dash_names=False)
    contexts = coll.to_contexts()
    names = ['my_task', 'inner_coll.inner_task']
    aliases = [['other_name'], ['inner_coll.other_inner']]
    assert sorted((x.name for x in contexts)) == sorted(names)
    assert sorted((x.aliases for x in contexts)) == sorted(aliases)

def auto_dash_names_transforms_are_applied_to_explicit_module_namespaces(self):
    namespace = self._nested_underscores()

    class FakeModule(object):
        __name__ = 'my_module'
        ns = namespace
    coll = Collection.from_module(FakeModule(), auto_dash_names=False)
    expected = {'my_task', 'inner_coll.inner_task'}
    assert {x.name for x in coll.to_contexts()} == expected

def to_contexts_allows_flaglike_access_via_flags(self):
    assert '--text' in [x for x in self.contexts if x.name == 'mytask'][0].flags

def to_contexts_positional_arglist_preserves_order_given(self):

    @task(positional=('second', 'first'))
    def mytask(c, first, second, third):
        pass
    coll = Collection()
    coll.add_task(mytask)
    c = coll.to_contexts()[0]
    expected = [c.args['second'], c.args['first']]
    assert c.positional_args == expected

def to_contexts_exposes_namespaced_task_names(self):
    assert 'sub.subtask' in [x.name for x in self.contexts]

def to_contexts_exposes_namespaced_task_aliases(self):
    assert 'sub.othertask' in self.aliases

def to_contexts_exposes_subcollection_default_tasks(self):
    assert 'sub' in self.aliases

def to_contexts_exposes_aliases(self):
    assert 'mytask27' in self.aliases

def task_names_setup(self):
    self.c = Collection.from_module(load('explicit_root'))

def task_names_returns_all_task_names_including_subtasks(self):
    names = set(Collection.from_module(load('explicit_root')).task_names.keys())
    assert names == {'top-level', 'sub-level.sub-task'}

def task_names_includes_aliases_and_defaults_as_values(self):
    names = Collection.from_module(load('explicit_root')).task_names
    assert names['top-level'] == ['other-top']
    subtask_names = names['sub-level.sub-task']
    assert subtask_names == ['sub-level.other-sub', 'sub-level']

def configuration_setup(self):
    self.root = Collection()
    self.task = Task(_func, name='task')

def configuration_basic_set_and_get(self):
    Collection().configure({'foo': 'bar'})
    assert Collection().configuration() == {'foo': 'bar'}

def configuration_configure_performs_merging(self):
    Collection().configure({'foo': 'bar'})
    assert Collection().configuration()['foo'] == 'bar'
    Collection().configure({'biz': 'baz'})
    assert set(Collection().configuration().keys()), {'foo' == 'biz'}

def configuration_configure_merging_is_recursive_for_nested_dicts(self):
    Collection().configure({'foo': 'bar', 'biz': {'baz': 'boz'}})
    Collection().configure({'biz': {'otherbaz': 'otherboz'}})
    c = Collection().configuration()
    assert c['biz']['baz'] == 'boz'
    assert c['biz']['otherbaz'] == 'otherboz'

def configuration_configure_allows_overwriting(self):
    Collection().configure({'foo': 'one'})
    assert Collection().configuration()['foo'] == 'one'
    Collection().configure({'foo': 'two'})
    assert Collection().configuration()['foo'] == 'two'

def configuration_call_returns_dict(self):
    assert Collection().configuration() == {}
    Collection().configure({'foo': 'bar'})
    assert Collection().configuration() == {'foo': 'bar'}

def configuration_access_merges_from_subcollections(self):
    inner = Collection('inner', self.task)
    inner.configure({'foo': 'bar'})
    Collection().configure({'biz': 'baz'})
    assert set(Collection().configuration().keys()) == {'biz'}
    Collection().add_collection(inner)
    keys = set(Collection().configuration('inner.task').keys())
    assert keys == {'foo', 'biz'}

def configuration_parents_overwrite_children_in_path(self):
    inner = Collection('inner', self.task)
    inner.configure({'foo': 'inner'})
    Collection().add_collection(inner)
    assert Collection().configuration('inner.task')['foo'] == 'inner'
    Collection().configure({'foo': 'outer'})
    assert Collection().configuration('inner.task')['foo'] == 'outer'

def configuration_sibling_subcollections_ignored(self):
    inner = Collection('inner', self.task)
    inner.configure({'foo': 'hi there'})
    inner2 = Collection('inner2', Task(_func, name='task2'))
    inner2.configure({'foo': 'nope'})
    root = Collection(inner, inner2)
    assert root.configuration('inner.task')['foo'] == 'hi there'
    assert root.configuration('inner2.task2')['foo'] == 'nope'

def configuration_subcollection_paths_may_be_dotted(self):
    leaf = Collection('leaf', self.task)
    leaf.configure({'key': 'leaf-value'})
    middle = Collection('middle', leaf)
    root = Collection('root', middle)
    config = root.configuration('middle.leaf.task')
    assert config == {'key': 'leaf-value'}

def configuration_invalid_subcollection_paths_result_in_KeyError(self):
    with raises(KeyError):
        Collection('meh').configuration('nope.task')
    inner = Collection('inner', self.task)
    with raises(KeyError):
        Collection('root', inner).configuration('task')

def configuration_keys_dont_have_to_exist_in_full_path(self):
    leaf = Collection('leaf', self.task)
    leaf.configure({'key': 'leaf-value'})
    middle = Collection('middle', leaf)
    root = Collection('root', middle)
    config = root.configuration('middle.leaf.task')
    assert config == {'key': 'leaf-value'}
    middle.configure({'key': 'whoa'})
    assert root.configuration('middle.leaf.task') == {'key': 'whoa'}

def subcollection_from_path_top_level_path(self):
    collection = Collection.from_module(load('tree'))
    build = collection.collections['build']
    assert collection.subcollection_from_path('build') is build

def subcollection_from_path_nested_path(self):
    collection = Collection.from_module(load('tree'))
    docs = collection.collections['build'].collections['docs']
    assert collection.subcollection_from_path('build.docs') is docs

def subcollection_from_path_invalid_path(self):
    with raises(KeyError):
        collection = Collection.from_module(load('tree'))
        collection.subcollection_from_path('lol.whatever.man')

def serialized_empty_collection(self):
    expected = dict(name=None, help=None, tasks=[], default=None, collections=[])
    assert expected == Collection().serialized()

def serialized_empty_named_collection(self):
    expected = dict(name='foo', help=None, tasks=[], default=None, collections=[])
    assert expected == Collection('foo').serialized()

def serialized_empty_named_docstringed_collection(self):
    expected = dict(name='foo', help='Hi doc', tasks=[], default=None, collections=[])
    coll = Collection('foo')
    coll.__doc__ = 'Hi doc'
    assert expected == coll.serialized()

def serialized_name_docstring_default_and_tasks(self):
    expected = dict(name='deploy', help='How to deploy our code and configs.', tasks=[dict(name='db', help='Deploy to our database servers.', aliases=['db-servers']), dict(name='everywhere', help='Deploy to all targets.', aliases=[]), dict(name='web', help='Update and bounce the webservers.', aliases=[])], default='everywhere', collections=[])
    with support_path():
        from tree import deploy
        coll = Collection.from_module(deploy)
    assert expected == coll.serialized()

def serialized_name_docstring_default_tasks_and_collections(self):
    docs = dict(name='docs', help='Tasks for managing Sphinx docs.', tasks=[dict(name='all', help='Build all doc formats.', aliases=[]), dict(name='html', help='Build HTML output only.', aliases=[]), dict(name='pdf', help='Build PDF output only.', aliases=[])], default='all', collections=[])
    python = dict(name='python', help='PyPI/etc distribution artifacts.', tasks=[dict(name='all', help='Build all Python packages.', aliases=[]), dict(name='sdist', help='Build classic style tar.gz.', aliases=[]), dict(name='wheel', help='Build a wheel.', aliases=[])], default='all', collections=[])
    expected = dict(name='build', help='Tasks for compiling static code and assets.', tasks=[dict(name='all', help='Build all necessary artifacts.', aliases=['everything']), dict(name='c-ext', help='Build our internal C extension.', aliases=['ext']), dict(name='zap', help='A silly way to clean.', aliases=[])], default='all', collections=[docs, python])
    with support_path():
        from tree import build
        coll = Collection.from_module(build)
    assert expected == coll.serialized()

def serialized_unnamed_subcollections(self):
    subcoll = Collection()
    named_subcoll = Collection('hello')
    root = Collection(named_subcoll, subcoll=subcoll)
    expected = dict(name=None, default=None, help=None, tasks=[], collections=[dict(tasks=[], collections=[], name=None, default=None, help=None), dict(tasks=[], collections=[], name='hello', default=None, help=None)])
    assert expected == root.serialized()