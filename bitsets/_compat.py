# _compat.py - Python 2/3 compatibility

import sys

PY2 = sys.version_info[0] == 2


if PY2:
    long_int = long
    integer_types = (int, long) 

    get_unbound_func = lambda unbound_method: unbound_method.__func__
    
    from itertools import imap as map
    from itertools import izip as zip
    from itertools import ifilter as filter
    from itertools import ifilterfalse as filterfalse

    import copy_reg as copyreg

else:
    long_int = int
    integer_types = (int,) 

    get_unbound_func = lambda func: func 

    map = map
    zip = zip
    filter = filter
    from itertools import filterfalse

    import copyreg


def with_metaclass(meta, *bases):
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})
