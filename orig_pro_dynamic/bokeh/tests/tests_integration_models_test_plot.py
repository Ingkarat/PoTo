import pytest
pytest
import time
from flaky import flaky
from bokeh.events import LODEnd, LODStart
from bokeh.layouts import column
from bokeh.models import Button, Plot, Range1d
from bokeh.plotting import figure
pytest_plugins = ('bokeh._testing.plugins.project',)

@flaky(max_runs=10)
def Test_Plot_test_inner_dims_trigger_on_dynamic_add(self, bokeh_server_page) -> None:
    data = {}

    def modify_doc(doc):
        p1 = Plot(plot_height=400, plot_width=400, x_range=Range1d(0, 1), y_range=Range1d(0, 1), min_border=10)
        p2 = Plot(plot_height=400, plot_width=400, x_range=Range1d(0, 1), y_range=Range1d(0, 1), min_border=10)
        button = Button(css_classes=['foo'])
        layout = column(p1, button)

        def cb(event):
            if p2 not in layout.children:
                layout.children = [p1, button, p2]
        button.on_event('button_click', cb)

        def iw(attr, old, new):
            data['iw'] = (old, new)

        def ih(attr, old, new):
            data['ih'] = (old, new)
        p2.on_change('inner_width', iw)
        p2.on_change('inner_height', ih)
        doc.add_root(layout)
    page = bokeh_server_page(modify_doc)
    button = page.driver.find_element_by_css_selector('.foo .bk-btn')
    button.click()
    time.sleep(0.5)
    assert data['iw'][0] is None
    assert isinstance(data['iw'][1], int)
    assert data['iw'][1] < 400
    assert data['ih'][0] is None
    assert isinstance(data['ih'][1], int)
    assert data['ih'][1] < 400

@flaky(max_runs=10)
def Test_Plot_test_lod_event_triggering(self, bokeh_server_page) -> None:
    goodEvents = []
    badEvents = []

    def modify_doc(doc):
        x_range = Range1d(0, 4)
        y_range = Range1d(0, 4)
        p1 = figure(plot_height=400, plot_width=400, x_range=x_range, y_range=y_range, lod_interval=200, lod_timeout=300)
        p1.line([1, 2, 3], [1, 2, 3])
        p2 = figure(plot_height=400, plot_width=400, x_range=x_range, y_range=y_range, lod_interval=200, lod_timeout=300)
        p2.line([1, 2, 3], [1, 2, 3])
        p1.on_event(LODStart, lambda : goodEvents.append('LODStart'))
        p1.on_event(LODEnd, lambda : goodEvents.append('LODEnd'))
        p2.on_event(LODStart, lambda : badEvents.append('LODStart'))
        p2.on_event(LODEnd, lambda : badEvents.append('LODEnd'))
        layout = column(p1, p2)
        doc.add_root(layout)
    page = bokeh_server_page(modify_doc)
    page.drag_canvas_at_position(100, 100, 200, 200)
    time.sleep(0.1)
    assert goodEvents == ['LODStart']
    assert badEvents == []
    time.sleep(0.3)
    assert goodEvents == ['LODStart', 'LODEnd']
    assert badEvents == []