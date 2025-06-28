import imp
import os
import sys
import types
from pytest import raises
from invoke import Config
from invoke.loader import Loader, FilesystemLoader as FSLoader
from invoke.exceptions import CollectionNotFound
from _util import support

def _BasicLoader_find(self, name):
    (self.fd, self.path, self.desc) = t = imp.find_module(name, [support])
    return t

def Loader__exhibits_default_config_object(self):
    loader = _BasicLoader()
    assert isinstance(loader.config, Config)
    assert loader.config.tasks.collection_name == 'tasks'

def Loader__returns_module_and_location(self):
    (mod, path) = _BasicLoader().load('namespacing')
    assert isinstance(mod, types.ModuleType)
    assert path == support

def Loader__may_configure_config_via_constructor(self):
    config = Config({'tasks': {'collection_name': 'mytasks'}})
    loader = _BasicLoader(config=config)
    assert loader.config.tasks.collection_name == 'mytasks'

def Loader__adds_module_parent_dir_to_sys_path(self):
    _BasicLoader().load('namespacing')

def Loader__doesnt_dupliate_parent_dir_addition(self):
    _BasicLoader().load('namespacing')
    _BasicLoader().load('namespacing')
    assert sys.path.count(support) == 1

def Loader__closes_opened_file_object(self):
    loader = _BasicLoader()
    loader.load('foo')
    assert loader.fd.closed

def Loader__can_load_package(self):
    loader = _BasicLoader()
    loader.load('package')

def Loader__load_name_defaults_to_config_tasks_collection_name(self):
    """load() name defaults to config.tasks.collection_name"""

    class MockLoader(_BasicLoader):

        def find(self, name):
            assert name == 'simple_ns_list'
            return super(MockLoader, self).find(name)
    config = Config({'tasks': {'collection_name': 'simple_ns_list'}})
    loader = MockLoader(config=config)
    (mod, path) = loader.load()
    assert mod.__file__ == os.path.join(support, 'simple_ns_list.py')

def FilesystemLoader__setup(self):
    self.loader = FSLoader(start=support)

def FilesystemLoader__discovery_start_point_defaults_to_cwd(self):
    assert FSLoader().start == os.getcwd()

def FilesystemLoader__exposes_start_point_as_attribute(self):
    assert FSLoader().start == os.getcwd()

def FilesystemLoader__start_point_is_configurable_via_kwarg(self):
    start = '/tmp/'
    assert FSLoader(start=start).start == start

def FilesystemLoader__start_point_is_configurable_via_config(self):
    config = Config({'tasks': {'search_root': 'nowhere'}})
    assert FSLoader(config=config).start == 'nowhere'

def FilesystemLoader__raises_CollectionNotFound_if_not_found(self):
    with raises(CollectionNotFound):
        FSLoader(start=support).load('nope')

def FilesystemLoader__raises_ImportError_if_found_collection_cannot_be_imported(self):
    with raises(ImportError):
        FSLoader(start=support).load('oops')

def FilesystemLoader__searches_towards_root_of_filesystem(self):
    directly = FSLoader(start=support).load('foo')
    deep = os.path.join(support, 'ignoreme', 'ignoremetoo')
    indirectly = FSLoader(start=deep).load('foo')
    assert directly == indirectly