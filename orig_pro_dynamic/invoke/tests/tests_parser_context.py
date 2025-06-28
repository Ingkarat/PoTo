import copy
from pytest import raises
from invoke.parser import Argument, Context
from invoke.tasks import task
from invoke.collection import Collection

def Context__may_have_a_name(self):
    c = Context(name='taskname')
    assert c.name == 'taskname'

def Context__may_have_aliases(self):
    c = Context(name='realname', aliases=('othername', 'yup'))
    assert 'othername' in c.aliases

def Context__may_give_arg_list_at_init_time(self):
    a1 = Argument('foo')
    a2 = Argument('bar')
    c = Context(name='name', args=(a1, a2))
    assert c.args['foo'] is a1

def args_setup(self):
    self.c = Context(args=(Argument('foo'), Argument(names=('bar', 'biz')), Argument('baz', attr_name='wat')))

def args_exposed_as_dict(self):
    assert 'foo' in Context(args=(Argument('foo'), Argument(names=('bar', 'biz')), Argument('baz', attr_name='wat'))).args.keys()

def args_exposed_as_Lexicon(self):
    assert Context(args=(Argument('foo'), Argument(names=('bar', 'biz')), Argument('baz', attr_name='wat'))).args.bar == Context(args=(Argument('foo'), Argument(names=('bar', 'biz')), Argument('baz', attr_name='wat'))).args['bar']

def args_args_dict_includes_all_arg_names(self):
    for x in ('foo', 'bar', 'biz'):
        assert x in Context(args=(Argument('foo'), Argument(names=('bar', 'biz')), Argument('baz', attr_name='wat'))).args

def args_argument_attr_names_appear_in_args_but_not_flags(self):
    for x in ('baz', 'wat'):
        assert x in Context(args=(Argument('foo'), Argument(names=('bar', 'biz')), Argument('baz', attr_name='wat'))).args
    assert 'wat' not in Context(args=(Argument('foo'), Argument(names=('bar', 'biz')), Argument('baz', attr_name='wat'))).flags

def add_arg_setup(self):
    self.c = Context()

def add_arg_can_take_Argument_instance(self):
    a = Argument(names=('foo',))
    Context().add_arg(a)
    assert Context().args['foo'] is a

def add_arg_can_take_name_arg(self):
    Context().add_arg('foo')
    assert 'foo' in Context().args

def add_arg_can_take_kwargs_for_single_Argument(self):
    Context().add_arg(names=('foo', 'bar'))
    assert 'foo' in Context().args and 'bar' in Context().args

def add_arg_raises_ValueError_on_duplicate(self):
    Context().add_arg(names=('foo', 'bar'))
    with raises(ValueError):
        Context().add_arg(name='bar')

def add_arg_adds_flaglike_name_to_dot_flags(self):
    """adds flaglike name to .flags"""
    Context().add_arg('foo')
    assert '--foo' in Context().flags

def add_arg_adds_all_names_to_dot_flags(self):
    """adds all names to .flags"""
    Context().add_arg(names=('foo', 'bar'))
    assert '--foo' in Context().flags
    assert '--bar' in Context().flags

def add_arg_adds_true_bools_to_inverse_flags(self):
    Context().add_arg(name='myflag', default=True, kind=bool)
    assert '--myflag' in Context().flags
    assert '--no-myflag' in Context().inverse_flags
    assert Context().inverse_flags['--no-myflag'] == '--myflag'

def add_arg_inverse_flags_works_right_with_task_driven_underscored_names(self):

    @task
    def mytask(c, underscored_option=True):
        pass
    Context().add_arg(mytask.get_arguments()[0])
    flags = Context().inverse_flags['--no-underscored-option']
    assert flags == '--underscored-option'

def add_arg_turns_single_character_names_into_short_flags(self):
    Context().add_arg('f')
    assert '-f' in Context().flags
    assert '--f' not in Context().flags

def add_arg_adds_positional_args_to_positional_args(self):
    Context().add_arg(name='pos', positional=True)
    assert Context().positional_args[0].name == 'pos'

def add_arg_positional_args_empty_when_none_given(self):
    assert len(Context().positional_args) == 0

def add_arg_positional_args_filled_in_order(self):
    Context().add_arg(name='pos1', positional=True)
    assert Context().positional_args[0].name == 'pos1'
    Context().add_arg(name='abc', positional=True)
    assert Context().positional_args[1].name == 'abc'

def add_arg_positional_arg_modifications_affect_args_copy(self):
    Context().add_arg(name='hrm', positional=True)
    assert Context().args['hrm'].value == Context().positional_args[0].value
    Context().positional_args[0].value = 17
    assert Context().args['hrm'].value == Context().positional_args[0].value

def deepcopy_setup(self):
    self.arg = Argument('--boolean')
    self.orig = Context(name='mytask', args=(self.arg,), aliases=('othername',))
    self.new = copy.deepcopy(self.orig)

def deepcopy_returns_correct_copy(self):
    assert self.new is not self.orig
    assert copy.deepcopy(self.orig).name == 'mytask'
    assert 'othername' in copy.deepcopy(self.orig).aliases

def deepcopy_includes_arguments(self):
    assert len(copy.deepcopy(self.orig).args) == 1
    assert copy.deepcopy(self.orig).args['--boolean'] is not self.arg

def deepcopy_modifications_to_copied_arguments_do_not_touch_originals(self):
    new_arg = copy.deepcopy(self.orig).args['--boolean']
    new_arg.value = True
    assert new_arg.value
    assert not Argument('--boolean').value

def help_for_setup(self):
    self.vanilla = Context(args=(Argument('foo'), Argument('bar', help='bar the baz')))

    @task(help={'otherarg': 'other help'}, optional=['optval'])
    def mytask(c, myarg, otherarg, optval, intval=5):
        pass
    col = Collection(mytask)
    self.tasked = col.to_contexts()[0]

def help_for_raises_ValueError_for_non_flag_values(self):
    with raises(ValueError):
        Context(args=(Argument('foo'), Argument('bar', help='bar the baz'))).help_for('foo')

def help_for_vanilla_no_helpstr(self):
    assert Context(args=(Argument('foo'), Argument('bar', help='bar the baz'))).help_for('--foo') == ('--foo=STRING', '')

def help_for_vanilla_with_helpstr(self):
    result = Context(args=(Argument('foo'), Argument('bar', help='bar the baz'))).help_for('--bar')
    assert result == ('--bar=STRING', 'bar the baz')

def help_for_task_driven_with_helpstr(self):
    result = col.to_contexts()[0].help_for('--otherarg')
    assert result == ('-o STRING, --otherarg=STRING', 'other help')

def help_for_task_driven_no_helpstr(self):
    result = col.to_contexts()[0].help_for('--myarg')
    assert result == ('-m STRING, --myarg=STRING', '')

def help_for_short_form_before_long_form(self):
    result = col.to_contexts()[0].help_for('--myarg')
    assert result == ('-m STRING, --myarg=STRING', '')

def help_for_equals_sign_for_long_form_only(self):
    result = col.to_contexts()[0].help_for('--myarg')
    assert result == ('-m STRING, --myarg=STRING', '')

def help_for_kind_to_placeholder_map(self):
    helpfor = col.to_contexts()[0].help_for('--myarg')
    assert helpfor == ('-m STRING, --myarg=STRING', '')
    helpfor = col.to_contexts()[0].help_for('--intval')
    assert helpfor == ('-i INT, --intval=INT', '')

def help_for_shortflag_inputs_work_too(self):
    m = col.to_contexts()[0].help_for('-m')
    myarg = col.to_contexts()[0].help_for('--myarg')
    assert m == myarg

def help_for_optional_values_use_brackets(self):
    result = col.to_contexts()[0].help_for('--optval')
    assert result == ('-p [STRING], --optval[=STRING]', '')

def help_for_underscored_args(self):
    c = Context(args=(Argument('i_have_underscores', help='yup'),))
    result = c.help_for('--i-have-underscores')
    assert result == ('--i-have-underscores=STRING', 'yup')

def help_for_true_default_args(self):
    c = Context(args=(Argument('truthy', kind=bool, default=True),))
    assert c.help_for('--truthy') == ('--[no-]truthy', '')

def help_tuples_returns_list_of_help_tuples(self):

    @task(help={'otherarg': 'other help'})
    def mytask(c, myarg, otherarg):
        pass
    c = Collection(mytask).to_contexts()[0]
    expected = [c.help_for('--myarg'), c.help_for('--otherarg')]
    assert c.help_tuples() == expected

def help_tuples__assert_order(self, name_tuples, expected_flag_order):
    c = Context(args=[Argument(names=x) for x in name_tuples])
    expected = [c.help_for(x) for x in expected_flag_order]
    assert c.help_tuples() == expected

def help_tuples_sorts_alphabetically_by_shortflag_first(self):
    self._assert_order([('zarg', 'a'), ('arg', 'z')], ['--zarg', '--arg'])

def help_tuples_case_ignored_during_sorting(self):
    self._assert_order([('a',), ('B',)], ['-a', '-B'])

def help_tuples_lowercase_wins_when_values_identical_otherwise(self):
    self._assert_order([('V',), ('v',)], ['-v', '-V'])

def help_tuples_sorts_alphabetically_by_longflag_when_no_shortflag(self):
    self._assert_order([('otherarg',), ('longarg',)], ['--longarg', '--otherarg'])

def help_tuples_sorts_heterogenous_help_output_with_longflag_only_options_first(self):
    self._assert_order([('c',), ('a', 'aaagh'), ('b', 'bah'), ('beta',), ('alpha',)], ['--alpha', '--beta', '-a', '-b', '-c'])

def help_tuples_mixed_corelike_options(self):
    self._assert_order([('V', 'version'), ('c', 'collection'), ('h', 'help'), ('l', 'list'), ('r', 'root')], ['-c', '-h', '-l', '-r', '-V'])

def missing_positional_args_represents_positional_args_missing_values(self):
    arg1 = Argument('arg1', positional=True)
    arg2 = Argument('arg2', positional=False)
    arg3 = Argument('arg3', positional=True)
    c = Context(name='foo', args=(arg1, arg2, arg3))
    assert c.missing_positional_args == [arg1, arg3]
    c.positional_args[0].value = 'wat'
    assert c.missing_positional_args == [arg3]
    c.positional_args[1].value = 'hrm'
    assert c.missing_positional_args == []

def str_with_no_args_output_is_simple(self):
    assert str(Context('foo')) == "<parser/Context 'foo'>"

def str_args_show_as_repr(self):
    string = str(Context('bar', args=[Argument('arg1')]))
    assert string == "<parser/Context 'bar': {'arg1': <Argument: arg1>}>"