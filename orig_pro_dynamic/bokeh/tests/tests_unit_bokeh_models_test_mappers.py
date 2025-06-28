import pytest
pytest
from _util_models import check_properties_existence
from bokeh.palettes import Spectral6
import bokeh.models.mappers as bmm

def Test_CategoricalColorMapper_test_basic(self) -> None:
    mapper = bmm.CategoricalColorMapper()
    check_properties_existence(mapper, ['factors', 'palette', 'start', 'end', 'nan_color'])

def Test_CategoricalColorMapper_test_warning_with_short_palette(self, recwarn) -> None:
    bmm.CategoricalColorMapper(factors=['a', 'b', 'c'], palette=['red', 'green'])
    assert len(recwarn) == 1

def Test_CategoricalColorMapper_test_no_warning_with_long_palette(self, recwarn) -> None:
    bmm.CategoricalColorMapper(factors=['a', 'b', 'c'], palette=['red', 'green', 'orange', 'blue'])
    assert len(recwarn) == 0

def Test_CategoricalColorMapper_test_with_pandas_index(self, pd) -> None:
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    years = ['2015', '2016', '2017']
    data = {'2015': [2, 1, 4, 3, 2, 4], '2016': [5, 3, 3, 2, 4, 6], '2017': [3, 2, 4, 4, 5, 3]}
    df = pd.DataFrame(data, index=fruits)
    fruits = df.index
    years = df.columns
    m = bmm.CategoricalColorMapper(palette=Spectral6, factors=years, start=1, end=2)
    assert list(m.factors) == list(years)
    assert isinstance(m.factors, pd.Index)

def Test_CategoricalPatternMapper_test_basic(self) -> None:
    mapper = bmm.CategoricalPatternMapper()
    check_properties_existence(mapper, ['factors', 'patterns', 'start', 'end', 'default_value'])

def Test_CategoricalMarkerMapper_test_basic(self) -> None:
    mapper = bmm.CategoricalMarkerMapper()
    check_properties_existence(mapper, ['factors', 'markers', 'start', 'end', 'default_value'])

def Test_LinearColorMapper_test_basic(self) -> None:
    mapper = bmm.LinearColorMapper()
    check_properties_existence(mapper, ['palette', 'domain', 'low', 'high', 'low_color', 'high_color', 'nan_color'])

def Test_LogColorMapper_test_basic(self) -> None:
    mapper = bmm.LogColorMapper()
    check_properties_existence(mapper, ['palette', 'domain', 'low', 'high', 'low_color', 'high_color', 'nan_color'])