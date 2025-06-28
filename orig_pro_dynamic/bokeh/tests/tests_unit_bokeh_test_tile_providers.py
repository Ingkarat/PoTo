import pytest
pytest
from bokeh.models import WMTSTileSource
import bokeh.tile_providers as bt
ALL = ('CARTODBPOSITRON', 'CARTODBPOSITRON_RETINA', 'STAMEN_TERRAIN', 'STAMEN_TERRAIN_RETINA', 'STAMEN_TONER', 'STAMEN_TONER_BACKGROUND', 'STAMEN_TONER_LABELS', 'OSM', 'WIKIMEDIA', 'ESRI_IMAGERY', 'get_provider', 'Vendors')
_CARTO_URLS = {'CARTODBPOSITRON': 'https://tiles.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', 'CARTODBPOSITRON_RETINA': 'https://tiles.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png'}
_STAMEN_URLS = {'STAMEN_TERRAIN': 'https://stamen-tiles.a.ssl.fastly.net/terrain/{Z}/{X}/{Y}.png', 'STAMEN_TERRAIN_RETINA': 'https://stamen-tiles.a.ssl.fastly.net/terrain/{Z}/{X}/{Y}@2x.png', 'STAMEN_TONER': 'https://stamen-tiles.a.ssl.fastly.net/toner/{Z}/{X}/{Y}.png', 'STAMEN_TONER_BACKGROUND': 'https://stamen-tiles.a.ssl.fastly.net/toner-background/{Z}/{X}/{Y}.png', 'STAMEN_TONER_LABELS': 'https://stamen-tiles.a.ssl.fastly.net/toner-labels/{Z}/{X}/{Y}.png'}
_STAMEN_LIC = {'STAMEN_TERRAIN': '<a href="https://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>', 'STAMEN_TERRAIN_RETINA': '<a href="https://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>', 'STAMEN_TONER': '<a href="https://www.openstreetmap.org/copyright">ODbL</a>', 'STAMEN_TONER_BACKGROUND': '<a href="https://www.openstreetmap.org/copyright">ODbL</a>', 'STAMEN_TONER_LABELS': '<a href="https://www.openstreetmap.org/copyright">ODbL</a>'}
_OSM_URLS = {'OSM': 'https://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png'}
_WIKIMEDIA_URLS = {'WIKIMEDIA': 'https://maps.wikimedia.org/osm-intl/{Z}/{X}/{Y}@2x.png'}
_ESRI_URLS = {'ESRI_IMAGERY': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{Y}/{X}.jpg'}

def Test_StamenProviders_test_type(self, name) -> None:
    p = getattr(bt, name)
    assert isinstance(p, str)

def Test_StamenProviders_test_url(self, name) -> None:
    p = bt.get_provider(getattr(bt, name))
    assert p.url == _STAMEN_URLS[name]

def Test_StamenProviders_test_attribution(self, name) -> None:
    p = bt.get_provider(getattr(bt, name))
    assert p.attribution == 'Map tiles by <a href="https://stamen.com">Stamen Design</a>, under <a href="https://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="https://openstreetmap.org">OpenStreetMap</a>, under %s.' % _STAMEN_LIC[name]

def Test_StamenProviders_test_copies(self, name) -> None:
    p1 = bt.get_provider(getattr(bt, name))
    p2 = bt.get_provider(getattr(bt, name))
    assert p1 is not p2

def Test_CartoProviders_test_type(self, name) -> None:
    p = getattr(bt, name)
    assert isinstance(p, str)

def Test_CartoProviders_test_url(self, name) -> None:
    p = bt.get_provider(getattr(bt, name))
    assert p.url == _CARTO_URLS[name]

def Test_CartoProviders_test_attribution(self, name) -> None:
    p = bt.get_provider(getattr(bt, name))
    assert p.attribution == '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors,&copy; <a href="https://cartodb.com/attributions">CartoDB</a>'

def Test_CartoProviders_test_copies(self, name) -> None:
    p1 = bt.get_provider(getattr(bt, name))
    p2 = bt.get_provider(getattr(bt, name))
    assert p1 is not p2

def Test_OsmProvider_test_type(self, name) -> None:
    p = getattr(bt, name)
    assert isinstance(p, str)

def Test_OsmProvider_test_url(self, name) -> None:
    p = bt.get_provider(getattr(bt, name))
    assert p.url == _OSM_URLS[name]

def Test_OsmProvider_test_attribution(self, name) -> None:
    p = bt.get_provider(getattr(bt, name))
    assert p.attribution == '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

def Test_OsmProvider_test_copies(self, name) -> None:
    p1 = bt.get_provider(getattr(bt, name))
    p2 = bt.get_provider(getattr(bt, name))
    assert p1 is not p2

def Test_WikimediaProvider_test_type(self, name) -> None:
    p = getattr(bt, name)
    assert isinstance(p, str)

def Test_WikimediaProvider_test_url(self, name) -> None:
    p = bt.get_provider(getattr(bt, name))
    assert p.url == _WIKIMEDIA_URLS[name]

def Test_WikimediaProvider_test_attribution(self, name) -> None:
    p = bt.get_provider(getattr(bt, name))
    assert p.attribution == '&copy; <a href="https://foundation.wikimedia.org/wiki/Maps_Terms_of_Use">Wikimedia Maps</a> contributors'

def Test_WikimediaProvider_test_copies(self, name) -> None:
    p1 = bt.get_provider(getattr(bt, name))
    p2 = bt.get_provider(getattr(bt, name))
    assert p1 is not p2

def Test_EsriProvider_test_type(self, name) -> None:
    p = getattr(bt, name)
    assert isinstance(p, str)

def Test_EsriProvider_test_url(self, name) -> None:
    p = bt.get_provider(getattr(bt, name))
    assert p.url == _ESRI_URLS[name]

def Test_EsriProvider_test_attribution(self, name) -> None:
    p = bt.get_provider(getattr(bt, name))
    assert p.attribution == '&copy; <a href="http://downloads.esri.com/ArcGISOnline/docs/tou_summary.pdf">Esri</a>, Earthstar Geographics'

def Test_EsriProvider_test_copies(self, name) -> None:
    p1 = bt.get_provider(getattr(bt, name))
    p2 = bt.get_provider(getattr(bt, name))
    assert p1 is not p2

@pytest.mark.parametrize('name', ['CARTODBPOSITRON', 'CARTODBPOSITRON_RETINA', 'STAMEN_TERRAIN', 'STAMEN_TERRAIN_RETINA', 'STAMEN_TONER', 'STAMEN_TONER_BACKGROUND', 'STAMEN_TONER_LABELS', 'OSM', 'WIKIMEDIA', 'ESRI_IMAGERY'])
def Test_GetProvider_test_get_provider(self, name) -> None:
    name = 'CARTODBPOSITRON'
    assert name in bt.Vendors
    enum_member = getattr(bt.Vendors, name)
    assert hasattr(bt, name)
    mod_member = getattr(bt, name)
    p1 = bt.get_provider(enum_member)
    p2 = bt.get_provider(name)
    p3 = bt.get_provider(name.lower())
    p4 = bt.get_provider(mod_member)
    assert isinstance(p1, WMTSTileSource)
    assert isinstance(p2, WMTSTileSource)
    assert isinstance(p3, WMTSTileSource)
    assert isinstance(p4, WMTSTileSource)
    assert p1 is not p2
    assert p2 is not p3
    assert p2 is not p4
    assert p4 is not p1
    assert p1.url == p2.url == p3.url == p4.url
    assert p1.attribution == p2.attribution == p3.attribution == p4.attribution

def Test_GetProvider_test_unknown_vendor(self) -> None:
    with pytest.raises(ValueError):
        bt.get_provider('This is not a valid tile vendor')