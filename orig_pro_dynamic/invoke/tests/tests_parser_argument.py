from pytest import skip, raises
from invoke.parser import Argument

def init_may_take_names_list(self):
    names = ('--foo', '-f')
    a = Argument(names=names)
    for name in names:
        assert name in a.names

def init_may_take_name_arg(self):
    assert '-b' in Argument(name='-b').names

def init_must_get_at_least_one_name(self):
    with raises(TypeError):
        Argument()

def init_default_arg_is_name_not_names(self):
    assert 'b' in Argument('b').names

def init_can_declare_positional(self):
    assert Argument(name='foo', positional=True).positional is True

def init_positional_is_False_by_default(self):
    assert Argument(name='foo').positional is False

def init_can_set_attr_name_to_control_name_attr(self):
    a = Argument('foo', attr_name='bar')
    assert a.name == 'bar'

def repr_shows_useful_info(self):
    arg = Argument(names=('name', 'nick1', 'nick2'))
    expected = '<Argument: {} ({})>'.format('name', 'nick1, nick2')
    assert repr(arg) == expected

def repr_does_not_show_nickname_parens_if_no_nicknames(self):
    assert repr(Argument('name')) == '<Argument: name>'

def repr_shows_positionalness(self):
    arg = Argument('name', positional=True)
    assert repr(arg) == '<Argument: name *>'

def repr_shows_optionalness(self):
    arg = Argument('name', optional=True)
    assert repr(arg) == '<Argument: name ?>'

def repr_positionalness_and_optionalness_stick_together(self):
    arg = Argument('name', optional=True, positional=True)
    assert repr(arg) == '<Argument: name *?>'

def repr_shows_kind_if_not_str(self):
    assert repr(Argument('age', kind=int)) == '<Argument: age [int]>'

def repr_all_the_things_together(self):
    arg = Argument(names=('meh', 'm'), kind=int, optional=True, positional=True)
    assert repr(arg) == '<Argument: meh (m) [int] *?>'

def kind_kwarg_is_optional(self):
    Argument(name='a')
    Argument(name='b', kind=int)

def kind_kwarg_defaults_to_str(self):
    assert Argument('a').kind == str

def kind_kwarg_non_bool_implies_value_needed(self):
    assert Argument(name='a', kind=int).takes_value
    assert Argument(name='b', kind=str).takes_value
    assert Argument(name='c', kind=list).takes_value

def kind_kwarg_bool_implies_no_value_needed(self):
    assert not Argument(name='a', kind=bool).takes_value

def kind_kwarg_bool_implies_default_False_not_None(self):
    skip()

def kind_kwarg_may_validate_on_set(self):
    with raises(ValueError):
        Argument('a', kind=int).value = 'five'

def kind_kwarg_list_implies_initial_value_of_empty_list(self):
    assert Argument('mylist', kind=list).value == []

def names_returns_tuple_of_all_names(self):
    assert Argument(names=('--foo', '-b')).names == ('--foo', '-b')
    assert Argument(name='--foo').names == ('--foo',)

def names_is_normalized_to_a_tuple(self):
    assert isinstance(Argument(names=('a', 'b')).names, tuple)

def name_returns_first_name(self):
    assert Argument(names=('a', 'b')).name == 'a'

def nicknames_returns_rest_of_names(self):
    assert Argument(names=('a', 'b')).nicknames == ('b',)

def takes_value_True_by_default(self):
    assert Argument(name='a').takes_value

def takes_value_False_if_kind_is_bool(self):
    assert not Argument(name='-b', kind=bool).takes_value

def value_set_available_as_dot_raw_value(self):
    """available as .raw_value"""
    a = Argument('a')
    a.value = 'foo'
    assert a.raw_value == 'foo'

def value_set_untransformed_appears_as_dot_value(self):
    """untransformed, appears as .value"""
    a = Argument('a', kind=str)
    a.value = 'foo'
    assert a.value == 'foo'

def value_set_transformed_appears_as_dot_value_with_original_as_raw_value(self):
    """transformed, modified value is .value, original is .raw_value"""
    a = Argument('a', kind=int)
    a.value = '5'
    assert a.value == 5
    assert a.raw_value == '5'

def value_set_list_kind_triggers_append_instead_of_overwrite(self):
    a = Argument('mylist', kind=list)
    assert a.value == []
    a.value = 'val1'
    assert a.value == ['val1']
    a.value = 'val2'
    assert a.value == ['val1', 'val2']

def value_set_incrementable_True_triggers_increment_of_default(self):
    a = Argument('verbose', kind=int, default=0, incrementable=True)
    assert a.value == 0
    a.value = True
    assert a.value == 1
    for _ in range(4):
        a.value = True
    assert a.value == 5

def value_returns_default_if_not_set(self):
    a = Argument('a', default=25)
    assert a.value == 25

def raw_value_is_None_when_no_value_was_actually_seen(self):
    a = Argument('a', kind=int)
    assert a.raw_value is None

def got_value_non_list_kind_tests_for_None_value(self):
    arg = Argument('a')
    assert not arg.got_value
    arg.value = 'something'
    assert arg.got_value

def got_value_list_kind_test_for_empty_list_value(self):
    arg = Argument('a', kind=list)
    assert not arg.got_value
    arg.value = 'append-me'
    assert arg.got_value

def set_value_casts_by_default(self):
    a = Argument('a', kind=int)
    a.set_value('5')
    assert a.value == 5

def set_value_allows_setting_value_without_casting(self):
    a = Argument('a', kind=int)
    a.set_value('5', cast=False)
    assert a.value == '5'