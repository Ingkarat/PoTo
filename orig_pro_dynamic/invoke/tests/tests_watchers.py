from threading import Thread, Event
from invoke.vendor.six.moves.queue import Queue, Empty
from invoke import Responder, FailingResponder, ResponseNotAccepted

def Responder__keeps_track_of_seen_index_per_thread(self):
    r = Responder(pattern='foo', response='bar fight')

    def body(responder, in_q, out_q, finished):
        while not finished.is_set():
            try:
                stream = in_q.get_nowait()
                for response in r.submit(stream):
                    out_q.put_nowait(response)
            except Empty:
                pass
    (t1_in, t1_out, t1_finished) = (Queue(), Queue(), Event())
    (t2_in, t2_out, t2_finished) = (Queue(), Queue(), Event())
    t1 = Thread(target=body, args=(r, t1_in, t1_out, t1_finished))
    t2 = Thread(target=body, args=(r, t2_in, t2_out, t2_finished))
    t1.start()
    t2.start()
    try:
        stream = 'foo fighters'
        t1_in.put(stream)
        assert t1_out.get() == 'bar fight'
        t2_in.put(stream)
        assert t2_out.get(timeout=1) == 'bar fight'
    except Empty:
        assert False, 'Unable to read from thread 2 - implies threadlocal indices are broken!'
    finally:
        t1_finished.set()
        t2_finished.set()
        t1.join()
        t2.join()

def Responder__yields_response_when_regular_string_pattern_seen(self):
    r = Responder(pattern='empty', response='handed')
    assert list(r.submit('the house was empty')) == ['handed']

def Responder__yields_response_when_regex_seen(self):
    r = Responder(pattern='tech.*debt', response='pay it down')
    response = r.submit("technically, it's still debt")
    assert list(response) == ['pay it down']

def Responder__multiple_hits_within_stream_yield_multiple_responses(self):
    r = Responder(pattern='jump', response='how high?')
    assert list(r.submit('jump, wait, jump, wait')) == ['how high?'] * 2

def Responder__patterns_span_multiple_lines(self):
    r = Responder(pattern='call.*problem', response='So sorry')
    output = '\nYou only call me\nwhen you have a problem\nYou never call me\nJust to say hi\n'
    assert list(r.submit(output)) == ['So sorry']

def FailingResponder__behaves_like_regular_responder_by_default(self):
    r = FailingResponder(pattern='ju[^ ]{2}', response='how high?', sentinel='lolnope')
    assert list(r.submit('jump, wait, jump, wait')) == ['how high?'] * 2

def FailingResponder__raises_failure_exception_when_sentinel_detected(self):
    r = FailingResponder(pattern='ju[^ ]{2}', response='how high?', sentinel='lolnope')
    assert list(r.submit('jump')) == ['how high?']
    try:
        r.submit('lolnope')
    except ResponseNotAccepted as e:
        message = str(e)
        err = "Didn't see pattern in {!r}".format(message)
        assert 'ju[^ ]{2}' in message, err
        err = "Didn't see failure sentinel in {!r}".format(message)
        assert 'lolnope' in message, err
    else:
        assert False, 'Did not raise ResponseNotAccepted!'