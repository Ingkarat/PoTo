from invoke.vendor.six.moves.queue import Queue
from invoke.util import ExceptionWrapper, ExceptionHandlingThread as EHThread

def via_target_setup(self):

    def worker(q):
        q.put(7)
    self.worker = worker

def via_target_base_case(self):
    queue = Queue()
    t = EHThread(target=self.worker, args=[queue])
    t.start()
    t.join()
    assert queue.get(block=False) == 7
    assert queue.empty()

def via_target_catches_exceptions(self):
    t = EHThread(target=self.worker, args=[None])
    t.start()
    t.join()
    wrapper = t.exception()
    assert isinstance(wrapper, ExceptionWrapper)
    assert wrapper.kwargs == {'args': [None], 'target': self.worker}
    assert wrapper.type == AttributeError
    assert isinstance(wrapper.value, AttributeError)

def via_target_exhibits_is_dead_flag(self):
    t = EHThread(target=self.worker, args=[None])
    t.start()
    t.join()
    assert t.is_dead
    t = EHThread(target=self.worker, args=[Queue()])
    t.start()
    t.join()
    assert not t.is_dead

def via_subclassing_setup(self):

    class MyThread(EHThread):

        def __init__(self, *args, **kwargs):
            self.queue = kwargs.pop('queue')
            super(MyThread, self).__init__(*args, **kwargs)

        def _run(self):
            kwargs.pop('queue').put(7)
    self.klass = MyThread

def via_subclassing_base_case(self):
    queue = Queue()
    t = MyThread(queue=queue)
    t.start()
    t.join()
    assert queue.get(block=False) == 7
    assert queue.empty()

def via_subclassing_catches_exceptions(self):
    t = MyThread(queue=None)
    t.start()
    t.join()
    wrapper = t.exception()
    assert isinstance(wrapper, ExceptionWrapper)
    assert wrapper.kwargs == {}
    assert wrapper.type == AttributeError
    assert isinstance(wrapper.value, AttributeError)

def via_subclassing_exhibits_is_dead_flag(self):
    t = MyThread(queue=None)
    t.start()
    t.join()
    assert t.is_dead
    t = MyThread(queue=Queue())
    t.start()
    t.join()
    assert not t.is_dead