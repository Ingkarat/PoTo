from pytest import raises
from invoke.parser import Parser, Context, Argument, ParseError

def Parser__can_take_initial_context(self):
    c = Context()
    p = Parser(initial=c)
    assert p.initial == c

def Parser__can_take_initial_and_other_contexts(self):
    c1 = Context('foo')
    c2 = Context('bar')
    p = Parser(initial=Context(), contexts=[c1, c2])
    assert p.contexts['foo'] == c1
    assert p.contexts['bar'] == c2

def Parser__can_take_just_other_contexts(self):
    c = Context('foo')
    p = Parser(contexts=[c])
    assert p.contexts['foo'] == c

def Parser__can_take_just_contexts_as_non_keyword_arg(self):
    c = Context('foo')
    p = Parser([c])
    assert p.contexts['foo'] == c

def Parser__raises_ValueError_for_unnamed_Contexts_in_contexts(self):
    with raises(ValueError):
        Parser(initial=Context(), contexts=[Context()])

def Parser__raises_error_for_context_name_clashes(self):
    with raises(ValueError):
        Parser(contexts=(Context('foo'), Context('foo')))

def Parser__raises_error_for_context_alias_and_name_clashes(self):
    with raises(ValueError):
        Parser((Context('foo', aliases=('bar',)), Context('bar')))

def Parser__raises_error_for_context_name_and_alias_clashes(self):
    with raises(ValueError):
        Parser((Context('foo'), Context('bar', aliases=('foo',))))

def Parser__takes_ignore_unknown_kwarg(self):
    Parser(ignore_unknown=True)

def Parser__ignore_unknown_defaults_to_False(self):
    assert Parser().ignore_unknown is False

def parse_argv_parses_sys_argv_style_list_of_strings(self):
    """parses sys.argv-style list of strings"""
    mytask = Context(name='mytask')
    mytask.add_arg('arg')
    p = Parser(contexts=[mytask])
    p.parse_argv(['mytask', '--arg', 'value'])

def parse_argv_returns_only_contexts_mentioned(self):
    task1 = Context('mytask')
    task2 = Context('othertask')
    result = Parser((task1, task2)).parse_argv(['othertask'])
    assert len(result) == 1
    assert result[0].name == 'othertask'

def parse_argv_raises_error_if_unknown_contexts_found(self):
    with raises(ParseError):
        Parser().parse_argv(['foo', 'bar'])

def parse_argv_unparsed_does_not_share_state(self):
    r = Parser(ignore_unknown=True).parse_argv(['self'])
    assert r.unparsed == ['self']
    r2 = Parser(ignore_unknown=True).parse_argv(['contained'])
    assert r.unparsed == ['self']
    assert r2.unparsed == ['contained']

def parse_argv_ignore_unknown_returns_unparsed_argv_instead(self):
    r = Parser(ignore_unknown=True).parse_argv(['foo', 'bar', '--baz'])
    assert r.unparsed == ['foo', 'bar', '--baz']

def parse_argv_ignore_unknown_does_not_mutate_rest_of_argv(self):
    p = Parser([Context('ugh')], ignore_unknown=True)
    r = p.parse_argv(['ugh', 'what', '-nowai'])
    assert r.unparsed == ['what', '-nowai']

def parse_argv_always_includes_initial_context_if_one_was_given(self):
    t1 = Context('t1')
    init = Context()
    result = Parser((t1,), initial=init).parse_argv(['t1'])
    assert result[0].name is None
    assert result[1].name == 't1'

def parse_argv_returned_contexts_are_in_order_given(self):
    (t1, t2) = (Context('t1'), Context('t2'))
    r = Parser((t1, t2)).parse_argv(['t2', 't1'])
    assert [x.name for x in r] == ['t2', 't1']

def parse_argv_returned_context_member_arguments_contain_given_values(self):
    c = Context('mytask', args=(Argument('boolean', kind=bool),))
    result = Parser((c,)).parse_argv(['mytask', '--boolean'])
    assert result[0].args['boolean'].value is True

def parse_argv_inverse_bools_get_set_correctly(self):
    arg = Argument('myarg', kind=bool, default=True)
    c = Context('mytask', args=(arg,))
    r = Parser((c,)).parse_argv(['mytask', '--no-myarg'])
    assert r[0].args['myarg'].value is False

def parse_argv_arguments_which_take_values_get_defaults_overridden_correctly(self):
    args = (Argument('arg', kind=str), Argument('arg2', kind=int))
    c = Context('mytask', args=args)
    argv = ['mytask', '--arg', 'myval', '--arg2', '25']
    result = Parser((c,)).parse_argv(argv)
    assert result[0].args['arg'].value == 'myval'
    assert result[0].args['arg2'].value == 25

def parse_argv_returned_arguments_not_given_contain_default_values(self):
    a = Argument('name', kind=str)
    b = Argument('age', default=7)
    c = Context('mytask', args=(a, b))
    Parser((c,)).parse_argv(['mytask', '--name', 'blah'])
    assert c.args['age'].value == 7

def parse_argv_returns_remainder(self):
    """returns -- style remainder string chunk"""
    r = Parser((Context('foo'),)).parse_argv(['foo', '--', 'bar', 'biz'])
    assert r.remainder == 'bar biz'

def parse_argv_clones_initial_context(self):
    a = Argument('foo', kind=bool)
    assert a.value is None
    c = Context(args=(a,))
    p = Parser(initial=c)
    assert p.initial is c
    r = p.parse_argv(['--foo'])
    assert p.initial is c
    c2 = r[0]
    assert c2 is not c
    a2 = c2.args['foo']
    assert a2 is not a
    assert a.value is None
    assert a2.value is True

def parse_argv_clones_noninitial_contexts(self):
    a = Argument('foo')
    assert a.value is None
    c = Context(name='mytask', args=(a,))
    p = Parser(contexts=(c,))
    assert p.contexts['mytask'] is c
    r = p.parse_argv(['mytask', '--foo', 'val'])
    assert p.contexts['mytask'] is c
    c2 = r[0]
    assert c2 is not c
    a2 = c2.args['foo']
    assert a2 is not a
    assert a.value is None
    assert a2.value == 'val'

def parsing_errors_setup(self):
    self.p = Parser([Context(name='foo', args=[Argument('bar')])])

def parsing_errors_missing_flag_values_raise_ParseError(self):
    with raises(ParseError):
        Parser([Context(name='foo', args=[Argument('bar')])]).parse_argv(['foo', '--bar'])

def parsing_errors_attaches_context_to_ParseErrors(self):
    try:
        Parser([Context(name='foo', args=[Argument('bar')])]).parse_argv(['foo', '--bar'])
    except ParseError as e:
        assert e.context is not None

def parsing_errors_attached_context_is_None_outside_contexts(self):
    try:
        Parser().parse_argv(['wat'])
    except ParseError as e:
        assert e.context is None

def positional_arguments__basic(self):
    arg = Argument('pos', positional=True)
    mytask = Context(name='mytask', args=[arg])
    return Parser(contexts=[mytask])

def positional_arguments_single_positional_arg(self):
    r = self._basic().parse_argv(['mytask', 'posval'])
    assert r[0].args['pos'].value == 'posval'

def positional_arguments_omitted_positional_arg_raises_ParseError(self):
    try:
        self._basic().parse_argv(['mytask'])
    except ParseError as e:
        expected = "'mytask' did not receive required positional arguments: 'pos'"
        assert str(e) == expected
    else:
        assert False, 'Did not raise ParseError!'

def positional_arguments_omitted_positional_args_raises_ParseError(self):
    try:
        arg = Argument('pos', positional=True)
        arg2 = Argument('morepos', positional=True)
        mytask = Context(name='mytask', args=[arg, arg2])
        Parser(contexts=[mytask]).parse_argv(['mytask'])
    except ParseError as e:
        expected = "'mytask' did not receive required positional arguments: 'pos', 'morepos'"
        assert str(e) == expected
    else:
        assert False, 'Did not raise ParseError!'

def positional_arguments_positional_args_eat_otherwise_valid_context_names(self):
    mytask = Context('mytask', args=[Argument('pos', positional=True), Argument('nonpos', default='default')])
    Context('lolwut')
    result = Parser([mytask]).parse_argv(['mytask', 'lolwut'])
    r = result[0]
    assert r.args['pos'].value == 'lolwut'
    assert r.args['nonpos'].value == 'default'
    assert len(result) == 1

def positional_arguments_positional_args_can_still_be_given_as_flags(self):
    pos1 = Argument('pos1', positional=True)
    pos2 = Argument('pos2', positional=True)
    nonpos = Argument('nonpos', positional=False, default='lol')
    mytask = Context('mytask', args=[pos1, pos2, nonpos])
    assert mytask.positional_args == [pos1, pos2]
    r = Parser([mytask]).parse_argv(['mytask', '--nonpos', 'wut', '--pos2', 'pos2val', 'pos1val'])[0]
    assert r.args['pos1'].value == 'pos1val'
    assert r.args['pos2'].value == 'pos2val'
    assert r.args['nonpos'].value == 'wut'

def equals_signs__compare(self, argname, invoke, value):
    c = Context('mytask', args=(Argument(argname, kind=str),))
    r = Parser((c,)).parse_argv(['mytask', invoke])
    assert r[0].args[argname].value == value

def equals_signs_handles_equals_style_long_flags(self):
    self._compare('foo', '--foo=bar', 'bar')

def equals_signs_handles_equals_style_short_flags(self):
    self._compare('f', '-f=bar', 'bar')

def equals_signs_does_not_require_escaping_equals_signs_in_value(self):
    self._compare('f', '-f=biz=baz', 'biz=baz')

def parse_argv_handles_multiple_boolean_flags_per_context(self):
    c = Context('mytask', args=(Argument('foo', kind=bool), Argument('bar', kind=bool)))
    r = Parser([c]).parse_argv(['mytask', '--foo', '--bar'])
    a = r[0].args
    assert a.foo.value is True
    assert a.bar.value is True

def optional_arg_values_setup(self):
    self.parser = self._parser()

def optional_arg_values__parser(self, arguments=None):
    if arguments is None:
        arguments = (Argument(names=('foo', 'f'), optional=True, default='mydefault'),)
    self.context = Context('mytask', args=arguments)
    self.parser = Parser([self.context])
    return self.parser

def optional_arg_values__parse(self, argstr, parser=None):
    parser = parser or self.parser
    return parser.parse_argv(['mytask'] + argstr.split())

def optional_arg_values__expect(self, argstr, expected, parser=None):
    result = self._parse(argstr, parser)
    assert result[0].args.foo.value == expected

def optional_arg_values_no_value_becomes_True_not_default_value(self):
    self._expect('--foo', True)
    self._expect('-f', True)

def optional_arg_values_value_given_gets_preserved_normally(self):
    for argstr in ('--foo whatever', '--foo=whatever', '-f whatever', '-f=whatever'):
        self._expect(argstr, 'whatever')

def optional_arg_values_not_given_at_all_uses_default_value(self):
    self._expect('', 'mydefault')

def ambiguity_sanity_checks__test_for_ambiguity(self, invoke, parser=None):
    msg = 'is ambiguous'
    try:
        self._parse(invoke, parser or self.parser)
    except ParseError as e:
        assert msg in str(e)
    else:
        assert False

def ambiguity_sanity_checks_unfilled_posargs(self):
    p = self._parser((Argument('foo', optional=True), Argument('bar', positional=True)))
    self._test_for_ambiguity('--foo uhoh', p)

def ambiguity_sanity_checks_no_ambiguity_if_option_val_already_given(self):
    p = self._parser((Argument('foo', optional=True), Argument('bar', kind=bool)))
    result = self._parse('--foo hello --bar', p)
    assert result[0].args['foo'].value == 'hello'
    assert result[0].args['bar'].value is True

def ambiguity_sanity_checks_valid_argument_is_NOT_ambiguous(self):
    self._parser((Argument('foo', optional=True), Argument('bar')))
    for form in ('--bar barval', '--bar=barval'):
        result = self._parse('--foo {}'.format(form))
        assert len(result) == 1
        args = result[0].args
        assert args['foo'].value is True
        assert args['bar'].value == 'barval'

def ambiguity_sanity_checks_valid_flaglike_argument_is_NOT_ambiguous(self):
    self._parser((Argument('foo', optional=True), Argument('bar', kind=bool)))
    result = self._parse('--foo --bar')
    assert len(result) == 1
    args = result[0].args
    assert args['foo'].value is True
    assert args['bar'].value is True

def ambiguity_sanity_checks_invalid_flaglike_value_is_stored_as_value(self):
    self._parser((Argument('foo', optional=True),))
    result = self._parse('--foo --bar')
    assert result[0].args['foo'].value == '--bar'

def ambiguity_sanity_checks_task_name(self):
    c1 = Context('mytask', args=(Argument('foo', optional=True),))
    c2 = Context('othertask')
    p = Parser([c1, c2])
    self._test_for_ambiguity('--foo othertask', p)

def list_type_arguments__parse(self, *args):
    c = Context('mytask', args=(Argument('mylist', kind=list),))
    argv = ['mytask'] + list(args)
    return Parser([c]).parse_argv(argv)[0].args.mylist.value

def list_type_arguments_can_be_given_no_times_resulting_in_default_empty_list(self):
    assert self._parse() == []

def list_type_arguments_given_once_becomes_single_item_list(self):
    assert self._parse('--mylist', 'foo') == ['foo']

def list_type_arguments_given_N_times_becomes_list_of_len_N(self):
    expected = ['foo', 'bar', 'biz']
    got = self._parse('--mylist', 'foo', '--mylist', 'bar', '--mylist', 'biz')
    assert got == expected

def list_type_arguments_iterables_work_correctly_outside_a_vacuum(self):
    c = Context('mytask', args=[Argument('mylist', kind=list)])
    c2 = Context('othertask')
    argv = ['mytask', '--mylist', 'val', '--mylist', 'val2', 'othertask']
    result = Parser([c, c2]).parse_argv(argv)
    mylist = result[0].args.mylist.value
    assert mylist == ['val', 'val2']
    contexts = len(result)
    err = 'Got {} parse context results instead of 2!'.format(contexts)
    assert contexts == 2, err
    assert result[1].name == 'othertask'

def task_repetition_is_happy_to_handle_same_task_multiple_times(self):
    task1 = Context('mytask')
    result = Parser((task1,)).parse_argv(['mytask', 'mytask'])
    assert len(result) == 2
    for x in result:
        assert x.name == 'mytask'

def task_repetition_task_args_work_correctly(self):
    task1 = Context('mytask', args=(Argument('meh'),))
    result = Parser((task1,)).parse_argv(['mytask', '--meh', 'mehval1', 'mytask', '--meh', 'mehval2'])
    assert result[0].args.meh.value == 'mehval1'
    assert result[1].args.meh.value == 'mehval2'

def general__echo(self):
    return Argument('echo', kind=bool, default=False)

def general_core_flags_work_normally_when_no_conflict(self):
    initial = Context(args=[self._echo()])
    task1 = Context('mytask')
    parser = Parser(initial=initial, contexts=[task1])
    result = parser.parse_argv(['mytask', '--echo'])
    assert result[0].args.echo.value is True

def general_when_conflict_per_task_args_win_out(self):
    initial = Context(args=[self._echo()])
    task1 = Context('mytask', args=[self._echo()])
    parser = Parser(initial=initial, contexts=[task1])
    result = parser.parse_argv(['mytask', '--echo'])
    assert result[0].args.echo.value is False
    assert result[1].args.echo.value is True

def general_value_requiring_core_flags_also_work_correctly(self):
    """value-requiring core flags also work correctly"""
    initial = Context(args=[Argument('hide')])
    task1 = Context('mytask')
    parser = Parser(initial=initial, contexts=[task1])
    result = parser.parse_argv(['mytask', '--hide', 'both'])
    assert result[0].args.hide.value == 'both'

def edge_cases_core_bool_but_per_task_string(self):
    initial = Context(args=[Argument('hide', kind=bool, default=False)])
    task1 = Context('mytask', args=[Argument('hide')])
    parser = Parser(initial=initial, contexts=[task1])
    result = parser.parse_argv(['mytask', '--hide', 'both'])
    assert result[0].args.hide.value is False
    assert result[1].args.hide.value == 'both'

def help_treats_context_name_as_its_value_by_itself_base_case(self):
    task1 = Context('mytask')
    init = Context(args=[Argument('help', optional=True)])
    parser = Parser(initial=init, contexts=[task1])
    result = parser.parse_argv(['mytask', '--help'])
    assert len(result) == 2
    assert result[0].args.help.value == 'mytask'
    assert 'help' not in result[1].args

def help_treats_context_name_as_its_value_other_tokens_afterwards_raise_parse_errors(self):
    task1 = Context('mytask')
    init = Context(args=[Argument('help', optional=True)])
    parser = Parser(initial=init, contexts=[task1])
    with raises(ParseError, match='.*foobar.*'):
        parser.parse_argv(['mytask', '--help', 'foobar'])

def ParseResult__setup(self):
    self.context = Context('mytask', args=(Argument('foo', kind=str), Argument('bar')))
    argv = ['mytask', '--foo', 'foo-val', '--', 'my', 'remainder']
    self.result = Parser((self.context,)).parse_argv(argv)

def ParseResult__acts_as_a_list_of_parsed_contexts(self):
    assert len(self.result) == 1
    assert self.result[0].name == 'mytask'

def ParseResult__exhibits_remainder_attribute(self):
    assert Parser((self.context,)).parse_argv(argv).remainder == 'my remainder'