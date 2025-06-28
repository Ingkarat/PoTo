from invoke.collection import Collection
from invoke.parser import Parser
from invoke.tasks import task

def CLIParsing_setup(self):

    @task(positional=[], iterable=['my_list'], incrementable=['verbose'])
    def my_task(c, mystring, s, boolean=False, b=False, v=False, long_name=False, true_bool=True, _leading_underscore=False, trailing_underscore_=False, my_list=None, verbose=0):
        pass

    @task(aliases=['my_task27'])
    def my_task2(c):
        pass

    @task(default=True)
    def my_task3(c, mystring):
        pass

    @task
    def my_task4(c, clean=False, browse=False):
        pass

    @task(aliases=['other'], default=True)
    def sub_task(c):
        pass
    sub_coll = Collection('sub_coll', sub_task)
    self.c = Collection(my_task, my_task2, my_task3, my_task4, sub_coll)

def CLIParsing__parser(self):
    return Parser(Collection(my_task, my_task2, my_task3, my_task4, sub_coll).to_contexts())

def CLIParsing__parse(self, argstr):
    return self._parser().parse_argv(argstr.split())

def CLIParsing__compare(self, invoke, flagname, value):
    invoke = 'my-task ' + invoke
    result = self._parse(invoke)
    assert result[0].args[flagname].value == value

def CLIParsing__compare_names(self, given, real):
    assert self._parse(given)[0].name == real

def CLIParsing_underscored_flags_can_be_given_as_dashed(self):
    self._compare('--long-name', 'long_name', True)

def CLIParsing_leading_underscores_are_ignored(self):
    self._compare('--leading-underscore', '_leading_underscore', True)

def CLIParsing_trailing_underscores_are_ignored(self):
    self._compare('--trailing-underscore', 'trailing_underscore_', True)

def CLIParsing_inverse_boolean_flags(self):
    self._compare('--no-true-bool', 'true_bool', False)

def CLIParsing_namespaced_task(self):
    self._compare_names('sub-coll.sub-task', 'sub-coll.sub-task')

def CLIParsing_aliases(self):
    self._compare_names('my-task27', 'my-task2')

def CLIParsing_subcollection_aliases(self):
    self._compare_names('sub-coll.other', 'sub-coll.sub-task')

def CLIParsing_subcollection_default_tasks(self):
    self._compare_names('sub-coll', 'sub-coll.sub-task')

def CLIParsing_boolean_args(self):
    """my-task --boolean"""
    self._compare('--boolean', 'boolean', True)

def CLIParsing_flag_then_space_then_value(self):
    """my-task --mystring foo"""
    self._compare('--mystring foo', 'mystring', 'foo')

def CLIParsing_flag_then_equals_sign_then_value(self):
    """my-task --mystring=foo"""
    self._compare('--mystring=foo', 'mystring', 'foo')

def CLIParsing_short_boolean_flag(self):
    """my-task -b"""
    self._compare('-b', 'b', True)

def CLIParsing_short_flag_then_space_then_value(self):
    """my-task -s value"""
    self._compare('-s value', 's', 'value')

def CLIParsing_short_flag_then_equals_sign_then_value(self):
    """my-task -s=value"""
    self._compare('-s=value', 's', 'value')

def CLIParsing_short_flag_with_adjacent_value(self):
    """my-task -svalue"""
    r = self._parse('my-task -svalue')
    assert r[0].args.s.value == 'value'

def CLIParsing__flag_value_task(self, value):
    r = self._parse('my-task -s {} my-task2'.format(value))
    assert len(r) == 2
    assert r[0].name == 'my-task'
    assert r[0].args.s.value == value
    assert r[1].name == 'my-task2'

def CLIParsing_flag_value_then_task(self):
    """my-task -s value my-task2"""
    self._flag_value_task('value')

def CLIParsing_flag_value_same_as_task_name(self):
    """my-task -s my-task2 my-task2"""
    self._flag_value_task('my-task2')

def CLIParsing_three_tasks_with_args(self):
    """my-task --boolean my-task3 --mystring foo my-task2"""
    r = self._parse('my-task --boolean my-task3 --mystring foo my-task2')
    assert len(r) == 3
    assert [x.name for x in r] == ['my-task', 'my-task3', 'my-task2']
    assert r[0].args.boolean.value
    assert r[1].args.mystring.value == 'foo'

def CLIParsing_tasks_with_duplicately_named_kwargs(self):
    """my-task --mystring foo my-task3 --mystring bar"""
    r = self._parse('my-task --mystring foo my-task3 --mystring bar')
    assert r[0].name == 'my-task'
    assert r[0].args.mystring.value == 'foo'
    assert r[1].name == 'my-task3'
    assert r[1].args.mystring.value == 'bar'

def CLIParsing_multiple_short_flags_adjacent(self):
    """my-task -bv (and inverse)"""
    for args in ('-bv', '-vb'):
        r = self._parse('my-task {}'.format(args))
        a = r[0].args
        assert a.b.value
        assert a.v.value

def CLIParsing_list_type_flag_can_be_given_N_times_building_a_list(self):
    """my-task --my-list foo --my-list bar"""
    self._compare('--my-list foo', 'my-list', ['foo'])
    self._compare('--my-list foo --my-list bar', 'my-list', ['foo', 'bar'])

def CLIParsing_incrementable_type_flag_can_be_used_as_a_switch_or_counter(self):
    """my-task -v, -vv, -vvvvv etc, except with explicit --verbose"""
    self._compare('', 'verbose', 0)
    self._compare('--verbose', 'verbose', 1)
    self._compare('--verbose --verbose --verbose', 'verbose', 3)