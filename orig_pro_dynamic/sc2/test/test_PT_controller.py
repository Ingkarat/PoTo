from sc2.controller import Controller

def test_PT_running():
    c = Controller()
    c.running()

def test_PT_create_game():
    c = Controller()
    c.create_game(game_map, players, realtime, None)