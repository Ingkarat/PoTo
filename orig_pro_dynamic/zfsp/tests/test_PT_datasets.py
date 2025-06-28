from zfsp.zfs.datasets import Dataset
from zfsp.zfs.datasets import ChildDatasets

def test_PT_child_datasets():
    ds = Dataset()
    ds.child_datasets()

def test_PT_snapshot_names():
    ds = Dataset()
    ds.snapshot_names()

def test_PT_snapshots():
    ds = Dataset()
    ds.snapshots()

def test_PT_entries():
    ds = Dataset()
    ds.entries()

def test_PT_keys():
    ds = Dataset()
    ds.keys()

def test_PT_items():
    ds = Dataset()
    ds.items()

def test_PT_attributes():
    ds = Dataset()
    ds.attributes(key)

def test_PT_root_directory():
    ds = Dataset()
    ds.root_directory()

def test_PT_ChildDatasets_keys():
    cd = ChildDatasets()
    cd.keys()

def test_PT_ChildDatasets_items():
    cd = ChildDatasets()
    cd.items()

