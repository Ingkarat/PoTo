from sc2.sc2process import kill_switch

def test_PT_add():
    ks = kill_switch()
    ks.add(value)

def test_PT_kill_all():
    ks = kill_switch()
    ks.kill_all()

def test_PT_SC2Process_ws_url():
    sc = SC2Process()
    sc.ws_url()
