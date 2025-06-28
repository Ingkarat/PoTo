from cerberus import Validator
from cerberus import errors
from cerberus.errors import ErrorTreeNode
from cerberus.errors import ValidationError
from cerberus.errors import BaseErrorHandler
from cerberus.errors import BasicErrorHandler
from cerberus.errors import ErrorTree

#ValidationError = errors.ValidationError
#BaseErrorHandler = errors.BaseErrorHandler
#BasicErrorHandler = errors.BasicErrorHandler
#ErrorTreeNode = errors.ErrorTreeNode
#ErrorTree = errors.ErrorTree

#ve = ValidationError(
#        ['zap', 'foo'], ['zap', 'schema', 'foo'], 0x24, 'type', 'string', True, ()
#    )

def test_PT_child_errors():
    ve = ValidationError(
            ['zap', 'foo'], ['zap', 'schema', 'foo'], 0x24, 'type', 'string', True, ()
    )
    ve.child_errors()

def test_PT_ve_definitions_errors():
    ve = ValidationError(
            ['zap', 'foo'], ['zap', 'schema', 'foo'], 0x24, 'type', 'string', True, ()
    )
    ve.definitions_errors()

def test_PT_ve_field():
    ve = ValidationError(
            ['zap', 'foo'], ['zap', 'schema', 'foo'], 0x24, 'type', 'string', True, ()
    )
    ve.field()

def test_PT_ve_is_group_error():
    ve = ValidationError(
            ['zap', 'foo'], ['zap', 'schema', 'foo'], 0x24, 'type', 'string', True, ()
    )
    ve.is_group_error()

def test_PT_ve_is_logic_error():
    ve = ValidationError(
            ['zap', 'foo'], ['zap', 'schema', 'foo'], 0x24, 'type', 'string', True, ()
    )
    ve.is_logic_error()

def test_PT_ve_is_normalization_error():
    ve = ValidationError(
            ['zap', 'foo'], ['zap', 'schema', 'foo'], 0x24, 'type', 'string', True, ()
    )
    ve.is_normalization_error()
"""
def test_PT_definitions_errors():
    ve = ValidationError(
            ['zap', 'foo'], ['zap', 'schema', 'foo'], 0x24, 'type', 'string', True, ()
        )
    ve.definitions_errors()
"""

def test_PT_et_depth():
    et = ErrorTreeNode()
    et.depth()

def test_PT_et_tree_type():
    et = ErrorTreeNode()
    et.tree_type()

def test_PT_et_add():
    et = ErrorTreeNode()
    error = ValidationError()
    et.add(error)

def test_PT_ett_add():
    ett = ErrorTree()
    error = ValidationError()
    ett.add(error)

def test_PT_ett_fetch_errors_from():
    ett = ErrorTree()
    # path: DocumentPath
    ett.fetch_errors_from(path)

def test_PT_ett_fetch_node_from():
    ett = ErrorTree()
    # path: DocumentPath
    ett.fetch_node_from(path)




def test_PT_emit():
    be = BaseErrorHandler()
    be.emit()

def test_PT_end():
    be = BaseErrorHandler()
    be.end()   

def test_PT_extend():
    be = BaseErrorHandler()
    ve = ValidationError(
            ['zap', 'foo'], ['zap', 'schema', 'foo'], 0x24, 'type', 'string', True, ()
        )
    be.extend([ve])   

def test_PT_start():
    be = BaseErrorHandler()
    be.start()

def test_PT_pretty_tree():
    bas = BasicErrorHandler()
    bas.pretty_tree()

def test_PT_bas_add():
    bas = BasicErrorHandler()
    # error !?
    bas.add(eror)

def test_PT_bas_clear():
    bas = BasicErrorHandler()
    bas.clear(eror)

