# _compat.py - Python 2/3 compatibility

import sys

PY2 = sys.version_info.major == 2


if PY2:
    long_int = long
    integer_types = (int, long)

    unichr = unichr

    def get_unbound_func(unbound_method):
        return unbound_method.__func__

    from itertools import imap as map, izip as zip, ifilter as filter
    from itertools import ifilterfalse as filterfalse, izip_longest as zip_longest

    def py2_bool_to_nonzero(cls):
        cls.__nonzero__ = cls.__bool__
        del cls.__bool__
        return cls

    import copy_reg as copyreg


else:
    long_int = int
    integer_types = (int,)

    unichr = chr

    def get_unbound_func(func):
        return func

    map, zip, filter = map, zip, filter
    from itertools import filterfalse, zip_longest

    def py2_bool_to_nonzero(cls):
        return cls

    import copyreg


def register_reduce(mcls):
    """Register __reduce__ as reduction function for mcls instances."""
    copyreg.pickle(mcls, mcls.__reduce__)
    return mcls


def with_metaclass(meta, *bases):
    """From Jinja2 (BSD licensed).

    https://github.com/mitsuhiko/jinja2/blob/master/jinja2/_compat.py
    """
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})
