import pytest
from fixtures import complex_zpool

from zfs.constants import Checksum

checksums = {
    'fletcher2': Checksum.FLETCHER_2,
    'fletcher4': Checksum.FLETCHER_4,
    'sha256': Checksum.SHA256,
}


@pytest.mark.parametrize("mode", checksums)
def test_checksums(mode, complex_zpool):
    print(">>> ", mode, complex_zpool)
    root_dataset = complex_zpool.root_dataset
    zfile = root_dataset[mode][mode]
    assert zfile.dnode.blkptr[0].checksum_type == checksums[mode]
    zfile.read()

def test_PT_test_checksums():
    checksums = {
        'fletcher2': Checksum.FLETCHER_2,
        'fletcher4': Checksum.FLETCHER_4,
        'sha256': Checksum.SHA256,
    }
    mode = checksums
    root_dataset = complex_zpool.root_dataset
    zfile = root_dataset[mode][mode]
    assert zfile.dnode.blkptr[0].checksum_type == checksums[mode]
    zfile.read()

"""
python3 -m pytest --capture=tee-sys test_checksums.py
python3 -m pytest --capture=tee-sys tests/test_checksums.py 
"""