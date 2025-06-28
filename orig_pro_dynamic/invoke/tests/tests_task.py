from mock import Mock
from pytest import raises, skip
from invoke import Context, Config, task, Task, Call, Collection
from invoke import FilesystemLoader as Loader
from _util import support

def _func(c):
    pass
_ = object()

def task___load(self, name):
    (mod, _) = self.loader.load(name)
    return Collection.from_module(mod)

def task__setup(self):
    self.loader = Loader(start=support)
    self.vanilla = self._load('decorators')

def task__allows_access_to_wrapped_object(self):

    def lolcats(c):
        pass
    assert task(lolcats).body == lolcats

def task__allows_alias_specification(self):
    assert self.vanilla['foo'] == self.vanilla['bar']

def task__allows_multiple_aliases(self):
    assert self.vanilla['foo'] == self.vanilla['otherbar']

def task__allows_default_specification(self):
    assert self.vanilla[''] == self.vanilla['biz']

def task__has_autoprint_option(self):
    ap = self._load('autoprint')
    assert ap['nope'].autoprint is False
    assert ap['yup'].autoprint is True

def task__raises_ValueError_on_multiple_defaults(self):
    with raises(ValueError):
        self._load('decorator_multi_default')

def task__sets_arg_help(self):
    assert self.vanilla['punch'].help['why'] == 'Motive'

def task__sets_arg_kind(self):
    skip()

def task__sets_which_args_are_optional(self):
    assert self.vanilla['optional_values'].optional == ('myopt',)

def task__allows_annotating_args_as_positional(self):
    assert self.vanilla['one_positional'].positional == ['pos']
    assert self.vanilla['two_positionals'].positional == ['pos1', 'pos2']

def task__allows_annotating_args_as_iterable(self):
    assert self.vanilla['iterable_values'].iterable == ['mylist']

def task__allows_annotating_args_as_incrementable(self):
    arg = self.vanilla['incrementable_values']
    assert arg.incrementable == ['verbose']

def task__when_positional_arg_missing_all_non_default_args_are_positional(self):
    arg = self.vanilla['implicit_positionals']
    assert arg.positional == ['pos1', 'pos2']

def task__context_arguments_should_not_appear_in_implicit_positional_list(self):

    @task
    def mytask(c):
        pass
    assert len(mytask.positional) == 0

def task__pre_tasks_stored_directly(self):

    @task
    def whatever(c):
        pass

    @task(pre=[whatever])
    def func(c):
        pass
    assert func.pre == [whatever]

def task__allows_star_args_as_shortcut_for_pre(self):

    @task
    def pre1(c):
        pass

    @task
    def pre2(c):
        pass

    @task(pre1, pre2)
    def func(c):
        pass
    assert func.pre == (pre1, pre2)

def task__disallows_ambiguity_between_star_args_and_pre_kwarg(self):

    @task
    def pre1(c):
        pass

    @task
    def pre2(c):
        pass
    with raises(TypeError):

        @task(pre1, pre=[pre2])
        def func(c):
            pass

def task__sets_name(self):

    @task(name='foo')
    def bar(c):
        pass
    assert bar.name == 'foo'

def task__returns_Task_instances_by_default(self):

    @task
    def mytask(c):
        pass
    assert isinstance(mytask, Task)

def task__klass_kwarg_allows_overriding_class_used(self):

    class MyTask(Task):
        pass

    @task(klass=MyTask)
    def mytask(c):
        pass
    assert isinstance(mytask, MyTask)

def task__klass_kwarg_works_for_subclassers_without_kwargs(self):

    class MyTask(Task):
        pass

    def uses_MyTask(*args, **kwargs):
        kwargs.setdefault('klass', MyTask)
        return task(*args, **kwargs)

    @uses_MyTask
    def mytask(c):
        pass
    assert isinstance(mytask, MyTask)

def task__unknown_kwargs_get_mad_at_Task_level(self):
    with raises(TypeError):

        @task(whatever='man')
        def mytask(c):
            pass

def Task__has_useful_repr(self):
    i = repr(Task(_func))
    assert '_func' in i, "'func' not found in {!r}".format(i)
    e = repr(Task(_func, name='funky'))
    assert 'funky' in e, "'funky' not found in {!r}".format(e)
    assert '_func' not in e, "'_func' unexpectedly seen in {!r}".format(e)

def Task__equality_testing(self):
    t1 = Task(_func, name='foo')
    t2 = Task(_func, name='foo')
    assert t1 == t2
    t3 = Task(_func, name='bar')
    assert t1 != t3

def function_like_behavior_inherits_module_from_body(self):
    mytask = Task(_func, name='funky')
    assert mytask.__module__ is _func.__module__

def attributes_has_default_flag(self):
    assert Task(_func).is_default is False

def attributes_name_defaults_to_body_name(self):
    assert Task(_func).name == '_func'

def attributes_can_override_name(self):
    assert Task(_func, name='foo').name == 'foo'

def callability_setup(self):

    @task
    def foo(c):
        """My docstring"""
        return 5
    self.task = foo

def callability_dunder_call_wraps_body_call(self):
    context = Context()
    assert foo(context) == 5

def callability_errors_if_first_arg_not_Context(self):

    @task
    def mytask(c):
        pass
    with raises(TypeError):
        mytask(5)

def callability_errors_if_no_first_arg_at_all(self):
    with raises(TypeError):

        @task
        def mytask():
            pass

def callability_tracks_times_called(self):
    context = Context()
    assert foo.called is False
    foo(context)
    assert foo.called is True
    assert foo.times_called == 1
    foo(context)
    assert foo.times_called == 2

def callability_wraps_body_docstring(self):
    assert foo.__doc__ == 'My docstring'

def callability_wraps_body_name(self):
    assert foo.__name__ == 'foo'

def get_arguments_setup(self):

    @task(positional=['arg_3', 'arg1'], optional=['arg1'])
    def mytask(c, arg1, arg2=False, arg_3=5):
        pass
    self.task = mytask
    self.args = mytask.get_arguments()
    self.argdict = self._arglist_to_dict(self.args)

def get_arguments__arglist_to_dict(self, arglist):
    ret = {}
    for arg in arglist:
        for name in arg.names:
            ret[name] = arg
    return ret

def get_arguments__task_to_dict(self, task):
    return self._arglist_to_dict(task.get_arguments())

def get_arguments_positional_args_come_first(self):
    assert self.args[0].name == 'arg_3'
    assert self.args[1].name == 'arg1'
    assert self.args[2].name == 'arg2'

def get_arguments_kinds_are_preserved(self):
    assert [x.kind for x in self.args] == [int, str, bool]

def get_arguments_positional_flag_is_preserved(self):
    assert [x.positional for x in self.args] == [True, True, False]

def get_arguments_optional_flag_is_preserved(self):
    assert [x.optional for x in self.args] == [False, True, False]

def get_arguments_optional_prevents_bool_defaults_from_affecting_kind(self):

    @task(optional=['myarg'])
    def mytask(c, myarg=False):
        pass
    arg = mytask.get_arguments()[0]
    assert arg.kind is str

def get_arguments_optional_plus_nonbool_default_does_not_override_kind(self):

    @task(optional=['myarg'])
    def mytask(c, myarg=17):
        pass
    arg = mytask.get_arguments()[0]
    assert arg.kind is int

def get_arguments_turns_function_signature_into_Arguments(self):
    assert len(self.args), 3 == str(self.args)
    assert 'arg2' in self.argdict

def get_arguments_shortflags_created_by_default(self):
    assert 'a' in self.argdict
    assert self.argdict['a'] is self.argdict['arg1']

def get_arguments_shortflags_dont_care_about_positionals(self):
    """Positionalness doesn't impact whether shortflags are made"""
    for (short, long_) in (('a', 'arg1'), ('r', 'arg2'), ('g', 'arg-3')):
        assert self.argdict[short] is self.argdict[long_]

def get_arguments_autocreated_short_flags_can_be_disabled(self):

    @task(auto_shortflags=False)
    def mytask(c, arg):
        pass
    args = self._task_to_dict(mytask)
    assert 'a' not in args
    assert 'arg' in args

def get_arguments_autocreated_shortflags_dont_collide(self):
    """auto-created short flags don't collide"""

    @task
    def mytask(c, arg1, arg2, barg):
        pass
    args = self._task_to_dict(mytask)
    assert 'a' in args
    assert args['a'] is args['arg1']
    assert 'r' in args
    assert args['r'] is args['arg2']
    assert 'b' in args
    assert args['b'] is args['barg']

def get_arguments_early_auto_shortflags_shouldnt_lock_out_real_shortflags(self):

    @task
    def mytask(c, longarg, l):
        pass
    args = self._task_to_dict(mytask)
    assert 'longarg' in args
    assert 'o' in args
    assert args['o'] is args['longarg']
    assert 'l' in args

def get_arguments_context_arguments_are_not_returned(self):

    @task
    def mytask(c):
        pass
    assert len(mytask.get_arguments()) == 0

def get_arguments_underscores_become_dashes(self):

    @task
    def mytask(c, longer_arg):
        pass
    arg = mytask.get_arguments()[0]
    assert arg.names == ('longer-arg', 'l')
    assert arg.attr_name == 'longer_arg'
    assert arg.name == 'longer_arg'

def Call__setup(self):
    self.task = Task(Mock(__name__='mytask'))

def task_is_required(self):
    with raises(TypeError):
        Call()

def task_is_first_posarg(self):
    assert Call(_).task is _

def called_as_defaults_to_None(self):
    assert Call(_).called_as is None

def called_as_may_be_given(self):
    assert Call(_, called_as='foo').called_as == 'foo'

def args_defaults_to_empty_tuple(self):
    assert Call(_).args == tuple()

def args_may_be_given(self):
    assert Call(_, args=(1, 2, 3)).args == (1, 2, 3)

def kwargs_defaults_to_empty_dict(self):
    assert Call(_).kwargs == dict()

def kwargs_may_be_given(self):
    assert Call(_, kwargs={'foo': 'bar'}).kwargs == {'foo': 'bar'}

def stringrep_includes_task_name(self):
    call = Call(self.task)
    assert str(call) == "<Call 'mytask', args: (), kwargs: {}>"

def stringrep_works_for_subclasses(self):

    class MyCall(Call):
        pass
    call = MyCall(self.task)
    assert '<MyCall' in str(call)

def stringrep_includes_args_and_kwargs(self):
    call = Call(self.task, args=('posarg1', 'posarg2'), kwargs={'kwarg1': 'val1'})
    expected = "<Call 'mytask', args: ('posarg1', 'posarg2'), kwargs: {'kwarg1': 'val1'}>"
    assert str(call) == expected

def stringrep_includes_aka_if_explicit_name_given(self):
    call = Call(self.task, called_as='notmytask')
    expected = "<Call 'mytask' (called as: 'notmytask'), args: (), kwargs: {}>"
    assert str(call) == expected

def stringrep_skips_aka_if_explicit_name_same_as_task_name(self):
    call = Call(self.task, called_as='mytask')
    assert str(call) == "<Call 'mytask', args: (), kwargs: {}>"

def make_context_requires_config_argument(self):
    with raises(TypeError):
        Call(_).make_context()

def make_context_creates_a_new_Context_from_given_config(self):
    conf = Config(defaults={'foo': 'bar'})
    c = Call(_).make_context(conf)
    assert isinstance(c, Context)
    assert c.foo == 'bar'

def clone_returns_new_but_equivalent_object(self):
    orig = Call(self.task)
    clone = orig.clone()
    assert clone is not orig
    assert clone == orig

def clone_can_clone_into_a_subclass(self):
    orig = Call(self.task)

    class MyCall(Call):
        pass
    clone = orig.clone(into=MyCall)
    assert clone == orig
    assert isinstance(clone, MyCall)

def clone_can_be_given_extra_kwargs_to_clone_with(self):
    orig = Call(self.task)

    class MyCall(Call):

        def __init__(self, *args, **kwargs):
            self.hooray = kwargs.pop('hooray')
            super(MyCall, self).__init__(*args, **kwargs)
    clone = orig.clone(into=MyCall, with_={'hooray': 'woo'})
    assert clone.hooray == 'woo'