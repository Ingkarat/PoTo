from sc2.main import SlidingTimeWindow
from sc2.main import run_game

def test_PT_push():
    st = SlidingTimeWindow()
    f = 1.23
    st.push(f)

def test_PT_clear():
    st = SlidingTimeWindow()
    st.clear()

def test_PT_sum():
    st = SlidingTimeWindow()
    st.sum()

def test_PT_available():
    st = SlidingTimeWindow()
    st.available()

def test_PT_available_fmt():
    st = SlidingTimeWindow()
    st.available_fmt()

def test_PT_run_game():
    run_game(map_settings,players)