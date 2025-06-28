import pytest
pytest
import numpy as np
from _util_property import _TestHasProps, _TestModel
from bokeh._testing.util.api import verify_all
import bokeh.core.property.primitive as bcpp
ALL = ('Bool', 'Complex', 'Int', 'Float', 'String')
Test___all__ = verify_all(bcpp, ALL)

def Test_Bool_test_valid(self) -> None:
    prop = bcpp.Bool()
    assert prop.is_valid(None)
    assert prop.is_valid(False)
    assert prop.is_valid(True)
    assert prop.is_valid(np.bool8(False))
    assert prop.is_valid(np.bool8(True))

def Test_Bool_test_invalid(self) -> None:
    prop = bcpp.Bool()
    assert not prop.is_valid(0)
    assert not prop.is_valid(1)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid(np.int8(0))
    assert not prop.is_valid(np.int8(1))
    assert not prop.is_valid(np.int16(0))
    assert not prop.is_valid(np.int16(1))
    assert not prop.is_valid(np.int32(0))
    assert not prop.is_valid(np.int32(1))
    assert not prop.is_valid(np.int64(0))
    assert not prop.is_valid(np.int64(1))
    assert not prop.is_valid(np.uint8(0))
    assert not prop.is_valid(np.uint8(1))
    assert not prop.is_valid(np.uint16(0))
    assert not prop.is_valid(np.uint16(1))
    assert not prop.is_valid(np.uint32(0))
    assert not prop.is_valid(np.uint32(1))
    assert not prop.is_valid(np.uint64(0))
    assert not prop.is_valid(np.uint64(1))
    assert not prop.is_valid(np.float16(0))
    assert not prop.is_valid(np.float16(1))
    assert not prop.is_valid(np.float32(0))
    assert not prop.is_valid(np.float32(1))
    assert not prop.is_valid(np.float64(0))
    assert not prop.is_valid(np.float64(1))
    assert not prop.is_valid(np.complex64(1.0 + 1j))
    assert not prop.is_valid(np.complex128(1.0 + 1j))
    if hasattr(np, 'complex256'):
        assert not prop.is_valid(np.complex256(1.0 + 1j))

def Test_Bool_test_has_ref(self) -> None:
    prop = bcpp.Bool()
    assert not prop.has_ref

def Test_Bool_test_str(self) -> None:
    prop = bcpp.Bool()
    assert str(prop) == 'Bool'

def Test_Complex_test_valid(self) -> None:
    prop = bcpp.Complex()
    assert prop.is_valid(None)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(0.0)
    assert prop.is_valid(1.0)
    assert prop.is_valid(1.0 + 1j)
    assert prop.is_valid(np.int8(0))
    assert prop.is_valid(np.int8(1))
    assert prop.is_valid(np.int16(0))
    assert prop.is_valid(np.int16(1))
    assert prop.is_valid(np.int32(0))
    assert prop.is_valid(np.int32(1))
    assert prop.is_valid(np.int64(0))
    assert prop.is_valid(np.int64(1))
    assert prop.is_valid(np.uint8(0))
    assert prop.is_valid(np.uint8(1))
    assert prop.is_valid(np.uint16(0))
    assert prop.is_valid(np.uint16(1))
    assert prop.is_valid(np.uint32(0))
    assert prop.is_valid(np.uint32(1))
    assert prop.is_valid(np.uint64(0))
    assert prop.is_valid(np.uint64(1))
    assert prop.is_valid(np.float16(0))
    assert prop.is_valid(np.float16(1))
    assert prop.is_valid(np.float32(0))
    assert prop.is_valid(np.float32(1))
    assert prop.is_valid(np.float64(0))
    assert prop.is_valid(np.float64(1))
    assert prop.is_valid(np.complex64(1.0 + 1j))
    assert prop.is_valid(np.complex128(1.0 + 1j))
    if hasattr(np, 'complex256'):
        assert prop.is_valid(np.complex256(1.0 + 1j))
    assert prop.is_valid(False)
    assert prop.is_valid(True)

def Test_Complex_test_invalid(self) -> None:
    prop = bcpp.Complex()
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid(np.bool8(False))
    assert not prop.is_valid(np.bool8(True))

def Test_Complex_test_has_ref(self) -> None:
    prop = bcpp.Complex()
    assert not prop.has_ref

def Test_Complex_test_str(self) -> None:
    prop = bcpp.Complex()
    assert str(prop) == 'Complex'

def Test_Float_test_valid(self) -> None:
    prop = bcpp.Float()
    assert prop.is_valid(None)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(0.0)
    assert prop.is_valid(1.0)
    assert prop.is_valid(np.int8(0))
    assert prop.is_valid(np.int8(1))
    assert prop.is_valid(np.int16(0))
    assert prop.is_valid(np.int16(1))
    assert prop.is_valid(np.int32(0))
    assert prop.is_valid(np.int32(1))
    assert prop.is_valid(np.int64(0))
    assert prop.is_valid(np.int64(1))
    assert prop.is_valid(np.uint8(0))
    assert prop.is_valid(np.uint8(1))
    assert prop.is_valid(np.uint16(0))
    assert prop.is_valid(np.uint16(1))
    assert prop.is_valid(np.uint32(0))
    assert prop.is_valid(np.uint32(1))
    assert prop.is_valid(np.uint64(0))
    assert prop.is_valid(np.uint64(1))
    assert prop.is_valid(np.float16(0))
    assert prop.is_valid(np.float16(1))
    assert prop.is_valid(np.float32(0))
    assert prop.is_valid(np.float32(1))
    assert prop.is_valid(np.float64(0))
    assert prop.is_valid(np.float64(1))
    assert prop.is_valid(False)
    assert prop.is_valid(True)

def Test_Float_test_invalid(self) -> None:
    prop = bcpp.Float()
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid(np.bool8(False))
    assert not prop.is_valid(np.bool8(True))
    assert not prop.is_valid(np.complex64(1.0 + 1j))
    assert not prop.is_valid(np.complex128(1.0 + 1j))
    if hasattr(np, 'complex256'):
        assert not prop.is_valid(np.complex256(1.0 + 1j))

def Test_Float_test_has_ref(self) -> None:
    prop = bcpp.Float()
    assert not prop.has_ref

def Test_Float_test_str(self) -> None:
    prop = bcpp.Float()
    assert str(prop) == 'Float'

def Test_Int_test_valid(self) -> None:
    prop = bcpp.Int()
    assert prop.is_valid(None)
    assert prop.is_valid(0)
    assert prop.is_valid(1)
    assert prop.is_valid(np.int8(0))
    assert prop.is_valid(np.int8(1))
    assert prop.is_valid(np.int16(0))
    assert prop.is_valid(np.int16(1))
    assert prop.is_valid(np.int32(0))
    assert prop.is_valid(np.int32(1))
    assert prop.is_valid(np.int64(0))
    assert prop.is_valid(np.int64(1))
    assert prop.is_valid(np.uint8(0))
    assert prop.is_valid(np.uint8(1))
    assert prop.is_valid(np.uint16(0))
    assert prop.is_valid(np.uint16(1))
    assert prop.is_valid(np.uint32(0))
    assert prop.is_valid(np.uint32(1))
    assert prop.is_valid(np.uint64(0))
    assert prop.is_valid(np.uint64(1))
    assert prop.is_valid(False)
    assert prop.is_valid(True)

def Test_Int_test_invalid(self) -> None:
    prop = bcpp.Int()
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid('')
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())
    assert not prop.is_valid(np.bool8(False))
    assert not prop.is_valid(np.bool8(True))
    assert not prop.is_valid(np.float16(0))
    assert not prop.is_valid(np.float16(1))
    assert not prop.is_valid(np.float32(0))
    assert not prop.is_valid(np.float32(1))
    assert not prop.is_valid(np.float64(0))
    assert not prop.is_valid(np.float64(1))
    assert not prop.is_valid(np.complex64(1.0 + 1j))
    assert not prop.is_valid(np.complex128(1.0 + 1j))
    if hasattr(np, 'complex256'):
        assert not prop.is_valid(np.complex256(1.0 + 1j))

def Test_Int_test_has_ref(self) -> None:
    prop = bcpp.Int()
    assert not prop.has_ref

def Test_Int_test_str(self) -> None:
    prop = bcpp.Int()
    assert str(prop) == 'Int'

def Test_String_test_valid(self) -> None:
    prop = bcpp.String()
    assert prop.is_valid(None)
    assert prop.is_valid('')
    assert prop.is_valid('6')

def Test_String_test_invalid(self) -> None:
    prop = bcpp.String()
    assert not prop.is_valid(False)
    assert not prop.is_valid(True)
    assert not prop.is_valid(0)
    assert not prop.is_valid(1)
    assert not prop.is_valid(0.0)
    assert not prop.is_valid(1.0)
    assert not prop.is_valid(1.0 + 1j)
    assert not prop.is_valid(())
    assert not prop.is_valid([])
    assert not prop.is_valid({})
    assert not prop.is_valid(_TestHasProps())
    assert not prop.is_valid(_TestModel())

def Test_String_test_has_ref(self) -> None:
    prop = bcpp.String()
    assert not prop.has_ref

def Test_String_test_str(self) -> None:
    prop = bcpp.String()
    assert str(prop) == 'String'