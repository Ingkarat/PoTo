from mock import Mock
import pytest
from invoke import Collection, Config, Context, Executor, Task, call, task
from invoke.parser import ParserContext, ParseResult
from _util import expect
pytestmark = pytest.mark.usefixtures('integration')

def Executor__setup(self):
    self.task1 = Task(Mock(return_value=7))
    self.task2 = Task(Mock(return_value=10), pre=[self.task1])
    self.task3 = Task(Mock(), pre=[self.task1])
    self.task4 = Task(Mock(return_value=15), post=[self.task1])
    self.contextualized = Task(Mock())
    coll = Collection()
    coll.add_task(self.task1, name='task1')
    coll.add_task(self.task2, name='task2')
    coll.add_task(self.task3, name='task3')
    coll.add_task(self.task4, name='task4')
    coll.add_task(self.contextualized, name='contextualized')
    self.executor = Executor(collection=coll)

def init_allows_collection_and_config(self):
    coll = Collection()
    conf = Config()
    e = Executor(collection=coll, config=conf)
    assert e.collection is coll
    assert e.config is conf

def init_uses_blank_config_by_default(self):
    e = Executor(collection=Collection())
    assert isinstance(e.config, Config)

def init_can_grant_access_to_core_arg_parse_result(self):
    c = ParseResult([ParserContext(name='mytask')])
    e = Executor(collection=Collection(), core=c)
    assert e.core is c
    assert len(e.core) == 1
    assert e.core[0].name == 'mytask'
    assert len(e.core[0].args) == 0

def init_core_arg_parse_result_defaults_to_None(self):
    assert Executor(collection=Collection()).core is None

def execute_base_case(self):
    self.executor.execute('task1')
    assert self.task1.body.called

def execute_kwargs(self):
    k = {'foo': 'bar'}
    self.executor.execute(('task1', k))
    args = self.task1.body.call_args[0]
    kwargs = self.task1.body.call_args[1]
    assert isinstance(args[0], Context)
    assert len(args) == 1
    assert kwargs['foo'] == 'bar'

def execute_contextualized_tasks_are_given_parser_context_arg(self):
    self.executor.execute('contextualized')
    args = self.contextualized.body.call_args[0]
    assert len(args) == 1
    assert isinstance(args[0], Context)

def execute_default_tasks_called_when_no_tasks_specified(self):
    task = Task(Mock('default-task'))
    coll = Collection()
    coll.add_task(task, name='mytask', default=True)
    executor = Executor(collection=coll)
    executor.execute()
    args = task.body.call_args[0]
    assert isinstance(args[0], Context)
    assert len(args) == 1

def basic_pre_post_pre_tasks(self):
    self.executor.execute('task2')
    assert self.task1.body.call_count == 1

def basic_pre_post_post_tasks(self):
    self.executor.execute('task4')
    assert self.task1.body.call_count == 1

def basic_pre_post_calls_default_to_empty_args_always(self):
    (pre_body, post_body) = (Mock(), Mock())
    t1 = Task(pre_body)
    t2 = Task(post_body)
    t3 = Task(Mock(), pre=[t1], post=[t2])
    e = Executor(collection=Collection(t1=t1, t2=t2, t3=t3))
    e.execute(('t3', {'something': 'meh'}))
    for body in (pre_body, post_body):
        args = body.call_args[0]
        assert len(args) == 1
        assert isinstance(args[0], Context)

def basic_pre_post__call_objs(self):
    (pre_body, post_body) = (Mock(), Mock())
    t1 = Task(pre_body)
    t2 = Task(post_body)
    t3 = Task(Mock(), pre=[call(t1, 5, foo='bar')], post=[call(t2, 7, biz='baz')])
    c = Collection(t1=t1, t2=t2, t3=t3)
    e = Executor(collection=c)
    e.execute('t3')
    (args, kwargs) = pre_body.call_args
    assert kwargs == {'foo': 'bar'}
    assert isinstance(args[0], Context)
    assert args[1] == 5
    (args, kwargs) = post_body.call_args
    assert kwargs == {'biz': 'baz'}
    assert isinstance(args[0], Context)
    assert args[1] == 7

def basic_pre_post_call_objs_play_well_with_context_args(self):
    self._call_objs()

def deduping_and_chaining_chaining_is_depth_first(self):
    expect('-c depth_first deploy', out='\nCleaning HTML\nCleaning .tar.gz files\nCleaned everything\nMaking directories\nBuilding\nDeploying\nPreparing for testing\nTesting\n'.lstrip())

def deduping_and_chaining__expect(self, args, expected):
    expect('-c integration {}'.format(args), out=expected.lstrip())

def adjacent_hooks_deduping(self):
    self._expect('biz', '\nfoo\nbar\nbiz\npost1\npost2\n')

def adjacent_hooks_no_deduping(self):
    self._expect('--no-dedupe biz', '\nfoo\nfoo\nbar\nbiz\npost1\npost2\npost2\n')

def non_adjacent_hooks_deduping(self):
    self._expect('boz', '\nfoo\nbar\nboz\npost2\npost1\n')

def non_adjacent_hooks_no_deduping(self):
    self._expect('--no-dedupe boz', '\nfoo\nbar\nfoo\nboz\npost2\npost1\npost2\n')

def adjacent_top_level_tasks_deduping(self):
    self._expect('foo bar', '\nfoo\nbar\n')

def adjacent_top_level_tasks_no_deduping(self):
    self._expect('--no-dedupe foo bar', '\nfoo\nfoo\nbar\n')

def non_adjacent_top_level_tasks_deduping(self):
    self._expect('foo bar', '\nfoo\nbar\n')

def non_adjacent_top_level_tasks_no_deduping(self):
    self._expect('--no-dedupe foo bar', '\nfoo\nfoo\nbar\n')

def deduping_and_chaining_deduping_treats_different_calls_to_same_task_differently(self):
    body = Mock()
    t1 = Task(body)
    pre = [call(t1, 5), call(t1, 7), call(t1, 5)]
    t2 = Task(Mock(), pre=pre)
    c = Collection(t1=t1, t2=t2)
    e = Executor(collection=c)
    e.execute('t2')
    param_list = []
    for body_call in body.call_args_list:
        assert isinstance(body_call[0][0], Context)
        param_list.append(body_call[0][1])
    assert set(param_list) == {5, 7}

def collection_driven_config_hands_collection_configuration_to_context(self):

    @task
    def mytask(c):
        assert c.my_key == 'value'
    c = Collection(mytask)
    c.configure({'my_key': 'value'})
    Executor(collection=c).execute('mytask')

def collection_driven_config_hands_task_specific_configuration_to_context(self):

    @task
    def mytask(c):
        assert c.my_key == 'value'

    @task
    def othertask(c):
        assert c.my_key == 'othervalue'
    inner1 = Collection('inner1', mytask)
    inner1.configure({'my_key': 'value'})
    inner2 = Collection('inner2', othertask)
    inner2.configure({'my_key': 'othervalue'})
    c = Collection(inner1, inner2)
    e = Executor(collection=c)
    e.execute('inner1.mytask', 'inner2.othertask')

def collection_driven_config_subcollection_config_works_with_default_tasks(self):

    @task(default=True)
    def mytask(c):
        assert c.my_key == 'value'
    sub = Collection('sub', mytask=mytask)
    sub.configure({'my_key': 'value'})
    main = Collection(sub=sub)
    Executor(collection=main).execute('sub')

def returns_return_value_of_specified_task_base_case(self):
    assert self.executor.execute('task1') == {self.task1: 7}

def returns_return_value_of_specified_task_with_pre_tasks(self):
    result = self.executor.execute('task2')
    assert result == {self.task1: 7, self.task2: 10}

def returns_return_value_of_specified_task_with_post_tasks(self):
    result = self.executor.execute('task4')
    assert result == {self.task1: 7, self.task4: 15}

def autoprinting_defaults_to_off_and_no_output(self):
    expect('-c autoprint nope', out='')

def autoprinting_prints_return_value_to_stdout_when_on(self):
    expect('-c autoprint yup', out="It's alive!\n")

def autoprinting_prints_return_value_to_stdout_when_on_and_in_collection(self):
    expect('-c autoprint sub.yup', out="It's alive!\n")

def autoprinting_does_not_fire_on_pre_tasks(self):
    expect('-c autoprint pre-check', out='')

def autoprinting_does_not_fire_on_post_tasks(self):
    expect('-c autoprint post-check', out='')

def inter_task_context_and_config_sharing_context_is_new_but_config_is_same(self):

    @task
    def task1(c):
        return c

    @task
    def task2(c):
        return c
    coll = Collection(task1, task2)
    ret = Executor(collection=coll).execute('task1', 'task2')
    c1 = ret[task1]
    c2 = ret[task2]
    assert c1 is not c2
    assert c1.config is c2.config

def inter_task_context_and_config_sharing_new_config_data_is_preserved_between_tasks(self):

    @task
    def task1(c):
        c.foo = 'bar'
        return c

    @task
    def task2(c):
        return c
    coll = Collection(task1, task2)
    ret = Executor(collection=coll).execute('task1', 'task2')
    c2 = ret[task2]
    assert 'foo' in c2.config
    assert c2.foo == 'bar'

def inter_task_context_and_config_sharing_config_mutation_is_preserved_between_tasks(self):

    @task
    def task1(c):
        c.config.run.echo = True
        return c

    @task
    def task2(c):
        return c
    coll = Collection(task1, task2)
    ret = Executor(collection=coll).execute('task1', 'task2')
    c2 = ret[task2]
    assert c2.config.run.echo is True

def inter_task_context_and_config_sharing_config_deletion_is_preserved_between_tasks(self):

    @task
    def task1(c):
        del c.config.run.echo
        return c

    @task
    def task2(c):
        return c
    coll = Collection(task1, task2)
    ret = Executor(collection=coll).execute('task1', 'task2')
    c2 = ret[task2]
    assert 'echo' not in c2.config.run