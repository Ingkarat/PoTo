import os
import pickle
import re
import sys
from mock import patch, Mock, call
from pytest_relaxed import trap
from pytest import skip, raises
from invoke import AuthFailure, Context, Config, FailingResponder, ResponseNotAccepted, StreamWatcher, MockContext, Result
from _util import mock_subprocess, _Dummy
local_path = 'invoke.config.Local'

def init_takes_optional_config_arg(self):
    Context()
    Context(config={'foo': 'bar'})

def methods_exposed__expect_attr(self, attr):
    c = Context()
    assert hasattr(c, attr) and callable(getattr(c, attr))

def run_exists(self):
    self._expect_attr('run')

@patch(local_path)
def run_defaults_to_Local(self, Local):
    c = Context()
    c.run('foo')
    assert Local.mock_calls == [call(c), call().run('foo')]

def run_honors_runner_config_setting(self):
    runner_class = Mock()
    config = Config({'runners': {'local': runner_class}})
    c = Context(config)
    c.run('foo')
    assert runner_class.mock_calls == [call(c), call().run('foo')]

def methods_exposed_sudo(self):
    self._expect_attr('sudo')

def configuration_proxy_setup(self):
    config = Config(defaults={'foo': 'bar', 'biz': {'baz': 'boz'}})
    self.c = Context(config=config)

def configuration_proxy_direct_access_allowed(self):
    assert Context(config=config).config.__class__ == Config
    assert Context(config=config).config['foo'] == 'bar'
    assert Context(config=config).config.foo == 'bar'

def configuration_proxy_config_attr_may_be_overwritten_at_runtime(self):
    new_config = Config(defaults={'foo': 'notbar'})
    Context(config=config).config = new_config
    assert Context(config=config).foo == 'notbar'

def configuration_proxy_getitem(self):
    """___getitem__"""
    assert self.c['foo'] == 'bar'
    assert self.c['biz']['baz'] == 'boz'

def configuration_proxy_getattr(self):
    """__getattr__"""
    assert Context(config=config).foo == 'bar'
    assert Context(config=config).biz.baz == 'boz'

def configuration_proxy_get(self):
    assert Context(config=config).get('foo') == 'bar'
    assert Context(config=config).get('nope', 'wut') == 'wut'
    assert Context(config=config).biz.get('nope', 'hrm') == 'hrm'

def configuration_proxy_pop(self):
    assert Context(config=config).pop('foo') == 'bar'
    assert Context(config=config).pop('foo', 'notbar') == 'notbar'
    assert Context(config=config).biz.pop('baz') == 'boz'

def configuration_proxy_popitem(self):
    assert Context(config=config).biz.popitem() == ('baz', 'boz')
    del self.c['biz']
    assert Context(config=config).popitem() == ('foo', 'bar')
    assert Context(config=config).config == {}

def configuration_proxy_del_(self):
    """del"""
    del self.c['foo']
    del self.c['biz']['baz']
    assert Context(config=config).biz == {}
    del self.c['biz']
    assert Context(config=config).config == {}

def configuration_proxy_clear(self):
    Context(config=config).biz.clear()
    assert Context(config=config).biz == {}
    Context(config=config).clear()
    assert Context(config=config).config == {}

def configuration_proxy_setdefault(self):
    assert Context(config=config).setdefault('foo') == 'bar'
    assert Context(config=config).biz.setdefault('baz') == 'boz'
    assert Context(config=config).setdefault('notfoo', 'notbar') == 'notbar'
    assert Context(config=config).notfoo == 'notbar'
    assert Context(config=config).biz.setdefault('otherbaz', 'otherboz') == 'otherboz'
    assert Context(config=config).biz.otherbaz == 'otherboz'

def configuration_proxy_update(self):
    Context(config=config).update({'newkey': 'newval'})
    assert self.c['newkey'] == 'newval'
    assert Context(config=config).foo == 'bar'
    Context(config=config).biz.update(otherbaz='otherboz')
    assert Context(config=config).biz.otherbaz == 'otherboz'

def cwd_setup(self):
    self.c = Context()

def cwd_simple(self):
    Context().command_cwds = ['a', 'b']
    assert Context().cwd == os.path.join('a', 'b')

def cwd_nested_absolute_path(self):
    Context().command_cwds = ['a', '/b', 'c']
    assert Context().cwd == os.path.join('/b', 'c')

def cwd_multiple_absolute_paths(self):
    Context().command_cwds = ['a', '/b', 'c', '/d', 'e']
    assert Context().cwd == os.path.join('/d', 'e')

def cwd_home(self):
    Context().command_cwds = ['a', '~b', 'c']
    assert Context().cwd == os.path.join('~b', 'c')

def cd_setup(self):
    self.escaped_prompt = re.escape(Config().sudo.prompt)

@patch(local_path)
def cd_should_apply_to_run(self, Local):
    runner = Local.return_value
    c = Context()
    with c.cd('foo'):
        c.run('whoami')
    cmd = 'cd foo && whoami'
    assert runner.run.called, 'run() never called runner.run()!'
    assert runner.run.call_args[0][0] == cmd

@patch(local_path)
def cd_should_apply_to_sudo(self, Local):
    runner = Local.return_value
    c = Context()
    with c.cd('foo'):
        c.sudo('whoami')
    cmd = "sudo -S -p '[sudo] password: ' cd foo && whoami"
    assert runner.run.called, 'sudo() never called runner.run()!'
    assert runner.run.call_args[0][0] == cmd

@patch(local_path)
def cd_should_occur_before_prefixes(self, Local):
    runner = Local.return_value
    c = Context()
    with c.prefix('source venv'):
        with c.cd('foo'):
            c.run('whoami')
    cmd = 'cd foo && source venv && whoami'
    assert runner.run.called, 'run() never called runner.run()!'
    assert runner.run.call_args[0][0] == cmd

@patch(local_path)
def cd_should_use_finally_to_revert_changes_on_exceptions(self, Local):

    class Oops(Exception):
        pass
    runner = Local.return_value
    c = Context()
    try:
        with c.cd('foo'):
            c.run('whoami')
            assert runner.run.call_args[0][0] == 'cd foo && whoami'
            raise Oops
    except Oops:
        pass
    c.run('ls')
    assert runner.run.call_args[0][0] == 'ls'

def prefix_setup(self):
    self.escaped_prompt = re.escape(Config().sudo.prompt)

@patch(local_path)
def prefix_prefixes_should_apply_to_run(self, Local):
    runner = Local.return_value
    c = Context()
    with c.prefix('cd foo'):
        c.run('whoami')
    cmd = 'cd foo && whoami'
    assert runner.run.called, 'run() never called runner.run()!'
    assert runner.run.call_args[0][0] == cmd

@patch(local_path)
def prefix_prefixes_should_apply_to_sudo(self, Local):
    runner = Local.return_value
    c = Context()
    with c.prefix('cd foo'):
        c.sudo('whoami')
    cmd = "sudo -S -p '[sudo] password: ' cd foo && whoami"
    assert runner.run.called, 'sudo() never called runner.run()!'
    assert runner.run.call_args[0][0] == cmd

@patch(local_path)
def prefix_nesting_should_retain_order(self, Local):
    runner = Local.return_value
    c = Context()
    with c.prefix('cd foo'):
        with c.prefix('cd bar'):
            c.run('whoami')
            cmd = 'cd foo && cd bar && whoami'
            assert runner.run.called, 'run() never called runner.run()!'
            assert runner.run.call_args[0][0] == cmd
        c.run('whoami')
        cmd = 'cd foo && whoami'
        assert runner.run.called, 'run() never called runner.run()!'
        assert runner.run.call_args[0][0] == cmd
    c.run('whoami')
    cmd = 'whoami'
    assert runner.run.called, 'run() never called runner.run()!'
    assert runner.run.call_args[0][0] == cmd

@patch(local_path)
def prefix_should_use_finally_to_revert_changes_on_exceptions(self, Local):

    class Oops(Exception):
        pass
    runner = Local.return_value
    c = Context()
    try:
        with c.prefix('cd foo'):
            c.run('whoami')
            assert runner.run.call_args[0][0] == 'cd foo && whoami'
            raise Oops
    except Oops:
        pass
    c.run('ls')
    assert runner.run.call_args[0][0] == 'ls'

def sudo_setup(self):
    self.escaped_prompt = re.escape(Config().sudo.prompt)

@patch(local_path)
def sudo_prefixes_command_with_sudo(self, Local):
    runner = Local.return_value
    Context().sudo('whoami')
    cmd = "sudo -S -p '[sudo] password: ' whoami"
    assert runner.run.called, 'sudo() never called runner.run()!'
    assert runner.run.call_args[0][0] == cmd

@patch(local_path)
def sudo_optional_user_argument_adds_u_and_H_flags(self, Local):
    runner = Local.return_value
    Context().sudo('whoami', user='rando')
    cmd = "sudo -S -p '[sudo] password: ' -H -u rando whoami"
    assert runner.run.called, 'sudo() never called runner.run()!'
    assert runner.run.call_args[0][0] == cmd

@patch(local_path)
def sudo_honors_config_for_user_value(self, Local):
    runner = Local.return_value
    config = Config(overrides={'sudo': {'user': 'rando'}})
    Context(config=config).sudo('whoami')
    cmd = "sudo -S -p '[sudo] password: ' -H -u rando whoami"
    assert runner.run.call_args[0][0] == cmd

@patch(local_path)
def sudo_user_kwarg_wins_over_config(self, Local):
    runner = Local.return_value
    config = Config(overrides={'sudo': {'user': 'rando'}})
    Context(config=config).sudo('whoami', user='calrissian')
    cmd = "sudo -S -p '[sudo] password: ' -H -u calrissian whoami"
    assert runner.run.call_args[0][0] == cmd

@trap
@mock_subprocess()
def sudo_echo_hides_extra_sudo_flags(self):
    skip()
    config = Config(overrides={'runner': _Dummy})
    Context(config=config).sudo('nope', echo=True)
    output = sys.stdout.getvalue()
    sys.__stderr__.write(repr(output) + '\n')
    assert '-S' not in output
    assert Context().sudo.prompt not in output
    assert 'sudo nope' in output

@patch(local_path)
def sudo_honors_config_for_prompt_value(self, Local):
    runner = Local.return_value
    config = Config(overrides={'sudo': {'prompt': 'FEED ME: '}})
    Context(config=config).sudo('whoami')
    cmd = "sudo -S -p 'FEED ME: ' whoami"
    assert runner.run.call_args[0][0] == cmd

def sudo_prompt_value_is_properly_shell_escaped(self):
    skip()

def sudo__expect_responses(self, expected, config=None, kwargs=None):
    """
            Execute mocked sudo(), expecting watchers= kwarg in its run().

            * expected: list of 2-tuples of FailingResponder prompt/response
            * config: Config object, if an overridden one is needed
            * kwargs: sudo() kwargs, if needed
            """
    if kwargs is None:
        kwargs = {}
    Local = Mock()
    runner = Local.return_value
    context = Context(config=config) if config else Context()
    context.config.runners.local = Local
    context.sudo('whoami', **kwargs)
    prompt_responses = [(watcher.pattern, watcher.response) for watcher in runner.run.call_args[1]['watchers']]
    assert prompt_responses == expected

def sudo_autoresponds_with_password_kwarg(self):
    expected = [(self.escaped_prompt, 'secret\n')]
    self._expect_responses(expected, kwargs={'password': 'secret'})

def sudo_honors_configured_sudo_password(self):
    config = Config(overrides={'sudo': {'password': 'secret'}})
    expected = [(self.escaped_prompt, 'secret\n')]
    self._expect_responses(expected, config=config)

def sudo_sudo_password_kwarg_wins_over_config(self):
    config = Config(overrides={'sudo': {'password': 'notsecret'}})
    kwargs = {'password': 'secret'}
    expected = [(self.escaped_prompt, 'secret\n')]
    self._expect_responses(expected, config=config, kwargs=kwargs)

def auto_response_merges_with_other_responses_setup(self):

    class DummyWatcher(StreamWatcher):

        def submit(self, stream):
            pass
    self.watcher_klass = DummyWatcher

@patch(local_path)
def auto_response_merges_with_other_responses_kwarg_only_adds_to_kwarg(self, Local):
    runner = Local.return_value
    context = Context()
    watcher = DummyWatcher()
    context.sudo('whoami', watchers=[watcher])
    watchers = runner.run.call_args[1]['watchers']
    watchers.remove(watcher)
    assert len(watchers) == 1
    assert isinstance(watchers[0], FailingResponder)
    assert watchers[0].pattern == self.escaped_prompt

@patch(local_path)
def auto_response_merges_with_other_responses_config_only(self, Local):
    runner = Local.return_value
    watcher = DummyWatcher()
    overrides = {'run': {'watchers': [watcher]}}
    config = Config(overrides=overrides)
    Context(config=config).sudo('whoami')
    watchers = runner.run.call_args[1]['watchers']
    watchers.remove(watcher)
    assert len(watchers) == 1
    assert isinstance(watchers[0], FailingResponder)
    assert watchers[0].pattern == self.escaped_prompt

@patch(local_path)
def auto_response_merges_with_other_responses_config_use_does_not_modify_config(self, Local):
    runner = Local.return_value
    watcher = DummyWatcher()
    overrides = {'run': {'watchers': [watcher]}}
    config = Config(overrides=overrides)
    Context(config=config).sudo('whoami')
    watchers = runner.run.call_args[1]['watchers']
    err = 'Found sudo() reusing config watchers list directly!'
    assert watchers is not config.run.watchers, err
    err = 'Our config watchers list was modified!'
    assert config.run.watchers == [watcher], err

@patch(local_path)
def auto_response_merges_with_other_responses_both_kwarg_and_config(self, Local):
    runner = Local.return_value
    conf_watcher = DummyWatcher()
    overrides = {'run': {'watchers': [conf_watcher]}}
    config = Config(overrides=overrides)
    kwarg_watcher = DummyWatcher()
    Context(config=config).sudo('whoami', watchers=[kwarg_watcher])
    watchers = runner.run.call_args[1]['watchers']
    watchers.remove(kwarg_watcher)
    assert len(watchers) == 1
    assert conf_watcher not in watchers
    assert isinstance(watchers[0], FailingResponder)
    assert watchers[0].pattern == self.escaped_prompt

@patch(local_path)
def sudo_passes_through_other_run_kwargs(self, Local):
    runner = Local.return_value
    Context().sudo('whoami', echo=True, warn=False, hide=True, encoding='ascii')
    assert runner.run.called, 'sudo() never called runner.run()!'
    kwargs = runner.run.call_args[1]
    assert kwargs['echo'] is True
    assert kwargs['warn'] is False
    assert kwargs['hide'] is True
    assert kwargs['encoding'] == 'ascii'

@patch(local_path)
def sudo_returns_run_result(self, Local):
    runner = Local.return_value
    expected = runner.run.return_value
    result = Context().sudo('whoami')
    err = "sudo() did not return run()'s return value!"
    assert result is expected, err

@mock_subprocess(out='something', exit=None)
def sudo_raises_auth_failure_when_failure_detected(self):
    with patch('invoke.context.FailingResponder') as klass:
        unacceptable = Mock(side_effect=ResponseNotAccepted)
        klass.return_value.submit = unacceptable
        excepted = False
        try:
            config = Config(overrides={'sudo': {'password': 'nope'}})
            Context(config=config).sudo('meh', hide=True)
        except AuthFailure as e:
            assert e.result.exited is None
            expected = "The password submitted to prompt '[sudo] password: ' was rejected."
            assert str(e) == expected
            excepted = True
        if not excepted:
            assert False, 'Did not raise AuthFailure!'

def Context__can_be_pickled(self):
    c = Context()
    c.foo = {'bar': {'biz': ['baz', 'buzz']}}
    c2 = pickle.loads(pickle.dumps(c))
    assert c == c2
    assert c is not c2
    assert c.foo.bar.biz is not c2.foo.bar.biz

def MockContext__init_still_acts_like_superclass_init(self):
    assert isinstance(MockContext().config, Config)
    config = Config(overrides={'foo': 'bar'})
    assert MockContext(config).config is config
    assert MockContext(config=config).config is config

def MockContext__non_config_init_kwargs_used_as_return_values_for_methods(self):
    c = MockContext(run=Result('some output'))
    assert c.run("doesn't mattress").stdout == 'some output'

def MockContext__return_value_kwargs_can_take_iterables_too(self):
    c = MockContext(run=[Result('some output'), Result('more!')])
    assert c.run("doesn't mattress").stdout == 'some output'
    assert c.run("still doesn't mattress").stdout == 'more!'

def MockContext__return_value_kwargs_may_be_command_string_maps(self):
    c = MockContext(run={'foo': Result('bar')})
    assert c.run('foo').stdout == 'bar'

def MockContext__return_value_map_kwargs_may_take_iterables_too(self):
    c = MockContext(run={'foo': [Result('bar'), Result('biz')]})
    assert c.run('foo').stdout == 'bar'
    assert c.run('foo').stdout == 'biz'

def MockContext__methods_with_no_kwarg_values_raise_NotImplementedError(self):
    with raises(NotImplementedError):
        MockContext().run('onoz I did not anticipate this would happen')

def MockContext__sudo_also_covered(self):
    c = MockContext(sudo=Result(stderr='super duper'))
    assert c.sudo("doesn't mattress").stderr == 'super duper'
    try:
        MockContext().sudo('meh')
    except NotImplementedError:
        pass
    else:
        assert False, 'Did not get a NotImplementedError for sudo!'

def exhausted_return_values_also_raise_NotImplementedError__expect_NotImplementedError(self, context):
    context.run('something')
    try:
        context.run('something')
    except NotImplementedError:
        pass
    else:
        assert False, "Didn't raise NotImplementedError"

def exhausted_return_values_also_raise_NotImplementedError_single_value(self):
    self._expect_NotImplementedError(MockContext(run=Result('meh')))

def exhausted_return_values_also_raise_NotImplementedError_iterable(self):
    self._expect_NotImplementedError(MockContext(run=[Result('meh')]))

def exhausted_return_values_also_raise_NotImplementedError_mapping_to_single_value(self):
    self._expect_NotImplementedError(MockContext(run={'something': Result('meh')}))

def exhausted_return_values_also_raise_NotImplementedError_mapping_to_iterable(self):
    self._expect_NotImplementedError(MockContext(run={'something': [Result('meh')]}))

def MockContext__unexpected_kwarg_type_yields_TypeError(self):
    with raises(TypeError):
        MockContext(run=123)

def no_stored_result_run(self):
    mc = MockContext()
    with raises(TypeError):
        mc.set_result_for('run', 'whatever', Result('bar'))

def no_stored_result_sudo(self):
    mc = MockContext()
    with raises(TypeError):
        mc.set_result_for('sudo', 'whatever', Result('bar'))

def single_result_run(self):
    mc = MockContext(run=Result('foo'))
    with raises(TypeError):
        mc.set_result_for('run', 'whatever', Result('bar'))

def single_result_sudo(self):
    mc = MockContext(sudo=Result('foo'))
    with raises(TypeError):
        mc.set_result_for('sudo', 'whatever', Result('bar'))

def iterable_result_run(self):
    mc = MockContext(run=[Result('foo')])
    with raises(TypeError):
        mc.set_result_for('run', 'whatever', Result('bar'))

def iterable_result_sudo(self):
    mc = MockContext(sudo=[Result('foo')])
    with raises(TypeError):
        mc.set_result_for('sudo', 'whatever', Result('bar'))

def can_modify_return_value_maps_after_instantiation_run(self):
    mc = MockContext(run={'foo': Result('bar')})
    assert mc.run('foo').stdout == 'bar'
    mc.set_result_for('run', 'foo', Result('biz'))
    assert mc.run('foo').stdout == 'biz'

def can_modify_return_value_maps_after_instantiation_sudo(self):
    mc = MockContext(sudo={'foo': Result('bar')})
    assert mc.sudo('foo').stdout == 'bar'
    mc.set_result_for('sudo', 'foo', Result('biz'))
    assert mc.sudo('foo').stdout == 'biz'