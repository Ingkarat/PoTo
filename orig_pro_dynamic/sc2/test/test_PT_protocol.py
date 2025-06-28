from sc2.protocol import ProtocolError
from sc2.protocol import Protocol

def test_PT_is_game_over_error():
    pe = ProtocolError()
    pe.is_game_over_error()

def test_PT_ping():
    pr = Protocol()
    pr.ping()

def test_PT_quit():
    pr = Protocol()
    pr.quit()