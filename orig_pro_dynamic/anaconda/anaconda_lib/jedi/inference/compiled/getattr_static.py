"""
A static version of getattr.
This is a backport of the Python 3 code with a little bit of additional
information returned to enable Jedi to make decisions.
"""

import types

from jedi import debug
from jedi._compatibility import py_version

_sentinel = object()


def _check_instance(obj, attr):
    instance_dict = {}
    try:
        instance_dict = object.__getattribute__(obj, "__dict__")
    except AttributeError:
        pass
    return dict.get(instance_dict, attr, _sentinel)


def _check_class(klass, attr):
    for entry in _static_getmro(klass):
        if _shadowed_dict(type(entry)) is _sentinel:
            try:
                return entry.__dict__[attr]
            except KeyError:
                pass
    return _sentinel


def _is_type(obj):
    try:
        _static_getmro(obj)
    except TypeError:
        return False
    return True


def _shadowed_dict_newstyle(klass):
    dict_attr = type.__dict__["__dict__"]
    for entry in _static_getmro(klass):
        try:
            class_dict = dict_attr.__get__(entry)["__dict__"]
        except KeyError:
            pass
        else:
            if not (type(class_dict) is types.GetSetDescriptorType
                    and class_dict.__name__ == "__dict__"
                    and class_dict.__objclass__ is entry):
                return class_dict
    return _sentinel


def _static_getmro_newstyle(klass):
    mro = type.__dict__['__mro__'].__get__(klass)
    if not isinstance(mro, (tuple, list)):
        # There are unfortunately no tests for this, I was not able to
        # reproduce this in pure Python. However should still solve the issue
        # raised in GH #1517.
        debug.warning('mro of %s returned %s, should be a tuple' % (klass, mro))
        return ()
    return mro


if py_version >= 30:
    _shadowed_dict = _shadowed_dict_newstyle
    _get_type = type
    _static_getmro = _static_getmro_newstyle
else:
    def _shadowed_dict(klass):
        """
        In Python 2 __dict__ is not overwritable:

            class Foo(object): pass
            setattr(Foo, '__dict__', 4)

            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            TypeError: __dict__ must be a dictionary object

        It applies to both newstyle and oldstyle classes:

            class Foo(object): pass
            setattr(Foo, '__dict__', 4)
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            AttributeError: attribute '__dict__' of 'type' objects is not writable

        It also applies to instances of those objects. However to keep things
        straight forward, newstyle classes always use the complicated way of
        accessing it while oldstyle classes just use getattr.
        """
        if type(klass) is _oldstyle_class_type:
            return getattr(klass, '__dict__', _sentinel)
        return _shadowed_dict_newstyle(klass)

    class _OldStyleClass:
        pass

    _oldstyle_instance_type = type(_OldStyleClass())
    _oldstyle_class_type = type(_OldStyleClass)

    def _get_type(obj):
        type_ = object.__getattribute__(obj, '__class__')
        if type_ is _oldstyle_instance_type:
            # Somehow for old style classes we need to access it directly.
            return obj.__class__
        return type_

    def _static_getmro(klass):
        if type(klass) is _oldstyle_class_type:
            def oldstyle_mro(klass):
                """
                Oldstyle mro is a really simplistic way of look up mro:
                https://stackoverflow.com/questions/54867/what-is-the-difference-between-old-style-and-new-style-classes-in-python
                """
                yield klass
                for base in klass.__bases__:
                    for yield_from in oldstyle_mro(base):
                        yield yield_from

            return oldstyle_mro(klass)

        return _static_getmro_newstyle(klass)


def _safe_hasattr(obj, name):
    return _check_class(_get_type(obj), name) is not _sentinel


def _safe_is_data_descriptor(obj):
    return _safe_hasattr(obj, '__set__') or _safe_hasattr(obj, '__delete__')


def getattr_static(obj, attr, default=_sentinel):
    """Retrieve attributes without triggering dynamic lookup via the
       descriptor protocol,  __getattr__ or __getattribute__.

       Note: this function may not be able to retrieve all attributes
       that getattr can fetch (like dynamically created attributes)
       and may find attributes that getattr can't (like descriptors
       that raise AttributeError). It can also return descriptor objects
       instead of instance members in some cases. See the
       documentation for details.

       Returns a tuple `(attr, is_get_descriptor)`. is_get_descripter means that
       the attribute is a descriptor that has a `__get__` attribute.
    """
    instance_result = _sentinel
    if not _is_type(obj):
        klass = _get_type(obj)
        dict_attr = _shadowed_dict(klass)
        if (dict_attr is _sentinel or type(dict_attr) is types.MemberDescriptorType):
            instance_result = _check_instance(obj, attr)
    else:
        klass = obj

    klass_result = _check_class(klass, attr)

    if instance_result is not _sentinel and klass_result is not _sentinel:
        if _safe_hasattr(klass_result, '__get__') \
                and _safe_is_data_descriptor(klass_result):
            # A get/set descriptor has priority over everything.
            return klass_result, True

    if instance_result is not _sentinel:
        return instance_result, False
    if klass_result is not _sentinel:
        return klass_result, _safe_hasattr(klass_result, '__get__')

    if obj is klass:
        # for types we check the metaclass too
        for entry in _static_getmro(type(klass)):
            if _shadowed_dict(type(entry)) is _sentinel:
                try:
                    return entry.__dict__[attr], False
                except KeyError:
                    pass
    if default is not _sentinel:
        return default, False
    raise AttributeError(attr)
