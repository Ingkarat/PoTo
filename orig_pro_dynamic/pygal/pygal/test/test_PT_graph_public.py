from pygal.graph.public import PublicApi

def test_PT_render_in_browser():
    pa = PublicApi()
    pa.render_in_browser()

def test_PT_render_response():
    pa = PublicApi()
    pa.render_response()

def test_PT_render_django_response():
    pa = PublicApi()
    pa.render_django_response()

def test_PT_render_data_uri():
    pa = PublicApi()
    pa.render_data_uri()

def test_PT_render_to_file():
    pa = PublicApi()
    pa.render_to_file()

def test_PT_render_to_png():
    pa = PublicApi()
    pa.render_to_png()

def test_PT_render_sparkline():
    pa = PublicApi()
    pa.render_sparkline()