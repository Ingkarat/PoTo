import pytest
pytest
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from flaky import flaky
from tornado.ioloop import IOLoop
from bokeh.util.tornado import _CallbackGroup

def _make_invocation_counter(loop, stop_after=1):
    from types import MethodType
    counter = {'count': 0}

    def func():
        counter['count'] += 1
        if stop_after is not None and counter['count'] >= stop_after:
            loop.stop()

    def count(self):
        return self.counter['count']
    func.count = MethodType(count, func)
    func.counter = counter
    return func

def run(loop):
    try:
        loop.start()
    except KeyboardInterrupt:
        print('Keyboard interrupt')

def LoopAndGroup___init__(self, quit_after=None):
    self.io_loop = IOLoop()
    IOLoop().make_current()
    self.group = _CallbackGroup(self.io_loop)
    if quit_after is not None:
        IOLoop().call_later(quit_after / 1000.0, lambda : IOLoop().stop())

def LoopAndGroup___exit__(self, type, value, traceback):
    run(self.io_loop)
    IOLoop().close()

def LoopAndGroup___enter__(self):
    return self

@flaky(max_runs=10)
def TestCallbackGroup_test_next_tick_runs(self) -> None:
    with LoopAndGroup() as ctx:
        func = _make_invocation_counter(ctx.io_loop)
        assert 0 == len(ctx.group._next_tick_callback_removers)
        ctx.group.add_next_tick_callback(func)
        assert 1 == len(ctx.group._next_tick_callback_removers)
    assert 1 == func.count()
    assert 0 == len(ctx.group._next_tick_callback_removers)

@flaky(max_runs=10)
def TestCallbackGroup_test_timeout_runs(self) -> None:
    with LoopAndGroup() as ctx:
        func = _make_invocation_counter(ctx.io_loop)
        assert 0 == len(ctx.group._timeout_callback_removers)
        ctx.group.add_timeout_callback(func, timeout_milliseconds=1)
        assert 1 == len(ctx.group._timeout_callback_removers)
    assert 1 == func.count()
    assert 0 == len(ctx.group._timeout_callback_removers)

@flaky(max_runs=10)
def TestCallbackGroup_test_periodic_runs(self) -> None:
    with LoopAndGroup() as ctx:
        func = _make_invocation_counter(ctx.io_loop, stop_after=5)
        assert 0 == len(ctx.group._periodic_callback_removers)
        cb_id = ctx.group.add_periodic_callback(func, period_milliseconds=1)
        assert 1 == len(ctx.group._periodic_callback_removers)
    assert 5 == func.count()
    assert 1 == len(ctx.group._periodic_callback_removers)
    ctx.group.remove_periodic_callback(cb_id)
    assert 0 == len(ctx.group._periodic_callback_removers)

@flaky(max_runs=10)
def TestCallbackGroup_test_next_tick_does_not_run_if_removed_immediately(self) -> None:
    with LoopAndGroup(quit_after=15) as ctx:
        func = _make_invocation_counter(ctx.io_loop)
        cb_id = ctx.group.add_next_tick_callback(func)
        ctx.group.remove_next_tick_callback(cb_id)
    assert 0 == func.count()

@flaky(max_runs=10)
def TestCallbackGroup_test_timeout_does_not_run_if_removed_immediately(self) -> None:
    with LoopAndGroup(quit_after=15) as ctx:
        func = _make_invocation_counter(ctx.io_loop)
        cb_id = ctx.group.add_timeout_callback(func, timeout_milliseconds=1)
        ctx.group.remove_timeout_callback(cb_id)
    assert 0 == func.count()

@flaky(max_runs=10)
def TestCallbackGroup_test_periodic_does_not_run_if_removed_immediately(self) -> None:
    with LoopAndGroup(quit_after=15) as ctx:
        func = _make_invocation_counter(ctx.io_loop, stop_after=5)
        cb_id = ctx.group.add_periodic_callback(func, period_milliseconds=1)
        ctx.group.remove_periodic_callback(cb_id)
    assert 0 == func.count()

@flaky(max_runs=10)
def TestCallbackGroup_test_same_callback_as_all_three_types(self) -> None:
    with LoopAndGroup() as ctx:
        func = _make_invocation_counter(ctx.io_loop, stop_after=5)
        ctx.group.add_periodic_callback(func, period_milliseconds=2)
        ctx.group.add_timeout_callback(func, timeout_milliseconds=1)
        ctx.group.add_next_tick_callback(func)
    assert 5 == func.count()

@flaky(max_runs=10)
def TestCallbackGroup_test_adding_next_tick_twice(self) -> None:
    with LoopAndGroup() as ctx:
        func = _make_invocation_counter(ctx.io_loop, stop_after=2)
        ctx.group.add_next_tick_callback(func)
        ctx.group.add_next_tick_callback(func)
    assert 2 == func.count()

@flaky(max_runs=10)
def TestCallbackGroup_test_adding_timeout_twice(self) -> None:
    with LoopAndGroup() as ctx:
        func = _make_invocation_counter(ctx.io_loop, stop_after=2)
        ctx.group.add_timeout_callback(func, timeout_milliseconds=1)
        ctx.group.add_timeout_callback(func, timeout_milliseconds=2)
    assert 2 == func.count()

@flaky(max_runs=10)
def TestCallbackGroup_test_adding_periodic_twice(self) -> None:
    with LoopAndGroup() as ctx:
        func = _make_invocation_counter(ctx.io_loop, stop_after=2)
        ctx.group.add_periodic_callback(func, period_milliseconds=3)
        ctx.group.add_periodic_callback(func, period_milliseconds=2)
    assert 2 == func.count()

@flaky(max_runs=10)
def TestCallbackGroup_test_remove_all_callbacks(self) -> None:
    with LoopAndGroup(quit_after=15) as ctx:

        def remove_all():
            ctx.group.remove_all_callbacks()
        ctx.group.add_next_tick_callback(remove_all)
        func = _make_invocation_counter(ctx.io_loop, stop_after=5)
        ctx.group.add_periodic_callback(func, period_milliseconds=2)
        ctx.group.add_timeout_callback(func, timeout_milliseconds=1)
        ctx.group.add_next_tick_callback(func)
    assert 0 == func.count()

@flaky(max_runs=10)
def TestCallbackGroup_test_removing_next_tick_twice(self) -> None:
    with LoopAndGroup(quit_after=15) as ctx:
        func = _make_invocation_counter(ctx.io_loop)
        cb_id = ctx.group.add_next_tick_callback(func)
        ctx.group.remove_next_tick_callback(cb_id)
        with pytest.raises(ValueError) as exc:
            ctx.group.remove_next_tick_callback(cb_id)
    assert 0 == func.count()
    assert 'twice' in repr(exc.value)

@flaky(max_runs=10)
def TestCallbackGroup_test_removing_timeout_twice(self) -> None:
    with LoopAndGroup(quit_after=15) as ctx:
        func = _make_invocation_counter(ctx.io_loop)
        cb_id = ctx.group.add_timeout_callback(func, timeout_milliseconds=1)
        ctx.group.remove_timeout_callback(cb_id)
        with pytest.raises(ValueError) as exc:
            ctx.group.remove_timeout_callback(cb_id)
    assert 0 == func.count()
    assert 'twice' in repr(exc.value)

@flaky(max_runs=10)
def TestCallbackGroup_test_removing_periodic_twice(self) -> None:
    with LoopAndGroup(quit_after=15) as ctx:
        func = _make_invocation_counter(ctx.io_loop, stop_after=5)
        cb_id = ctx.group.add_periodic_callback(func, period_milliseconds=1)
        ctx.group.remove_periodic_callback(cb_id)
        with pytest.raises(ValueError) as exc:
            ctx.group.remove_periodic_callback(cb_id)
    assert 0 == func.count()
    assert 'twice' in repr(exc.value)

@flaky(max_runs=10)
def TestCallbackGroup_test_adding_next_tick_from_another_thread(self) -> None:
    with LoopAndGroup(quit_after=15) as ctx:
        n = 1000
        func = _make_invocation_counter(ctx.io_loop, stop_after=n)
        tpe = ThreadPoolExecutor(n)
        list(tpe.map(ctx.group.add_next_tick_callback, repeat(func, n)))
    assert n == func.count()