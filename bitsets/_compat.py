# _compat.py - Python 2/3 compatibility

import sys

PY2 = sys.version_info[0] == 2


if PY2:  # pragma: no cover
    long_int = long
    integer_types = (int, long)

    get_unbound_func = lambda unbound_method: unbound_method.__func__

    from itertools import imap as map
    from itertools import izip as zip
    from itertools import ifilter as filter
    from itertools import ifilterfalse as filterfalse

    def py2_bool_to_nonzero(cls):
        cls.__nonzero__ = cls.__bool__
        del cls.__bool__
        return cls

    import copy_reg as copyreg


else:  # pragma: no cover
    long_int = int
    integer_types = (int,)

    get_unbound_func = lambda func: func

    map = map
    zip = zip
    filter = filter
    from itertools import filterfalse

    def py2_bool_to_nonzero(cls):
        return cls

    import copyreg


def with_metaclass(meta, *bases):
    """From Jinja2 (BSD licensed).

    http://github.com/mitsuhiko/jinja2/blob/master/jinja2/_compat.py
    """
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})
