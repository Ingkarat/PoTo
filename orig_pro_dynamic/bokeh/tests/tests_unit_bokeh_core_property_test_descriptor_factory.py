import pytest
pytest
from bokeh._testing.util.api import verify_all
import bokeh.core.property.descriptor_factory as bcpdf
ALL = ('PropertyDescriptorFactory',)

def test_autocreate() -> None:
    obj = Child()
    value = obj.autocreate()
    assert isinstance(value, Child)

def test_make_descriptors_not_implemented() -> None:
    obj = bcpdf.PropertyDescriptorFactory()
    with pytest.raises(NotImplementedError):
        obj.make_descriptors('foo')
Test___all__ = verify_all(bcpdf, ALL)