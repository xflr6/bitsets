# bitsets - integer bits representing subsets of totally orderd finite set

"""Ordered subsets of a predetermined finite domain."""

from . import meta, bases, series

__all__ = ['bitset']

__title__ = 'bitsets'
__version__ = '0.7.13'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE.txt'
__copyright__ = 'Copyright (c) 2013-2016 Sebastian Bank'


def bitset(name, members, base=bases.BitSet, list=False, tuple=False):
    """Return a new bitset class with given name and members.

    Args:
        name: Name of the class to be created.
        members: Hashable sequence of allowed bitset members.
        base: Base class to derive the returned class from.
        list (bool): Include a custom class for bitset lists.
        tuple (bool): Include a custom class for bitset tuples.

    Example:
        >>> Letters = bitset('Letters', 'abcdef', list=True, tuple=True)
        >>> Letters  # doctest: +ELLIPSIS
        <class bitsets.meta.bitset('Letters', 'abcdef', 0x..., BitSet, List, Tuple)>
        >>> Letters('deadbeef')
        Letters(['a', 'b', 'd', 'e', 'f'])
    """
    if not name:
        raise ValueError('empty bitset name: %r' % name)

    if not hasattr(members, '__getitem__') or not hasattr(members, '__len__'):
        raise ValueError('non-sequence bitset members: %r' % members)

    if not len(members):
        raise ValueError('less than one bitset member: %r' % (members,))

    if len(set(members)) != len(members):
        raise ValueError('bitset members contains duplicates: %r' % (members,))

    if not issubclass(base.__class__, meta.MemberBitsMeta):
        raise ValueError('base does not subclass bitset.bases: %r' % base)

    list = {False: None, True: series.List}.get(list, list)
    tuple = {False: None, True: series.Tuple}.get(tuple, tuple)

    return base._make_subclass(name, members, listcls=list, tuplecls=tuple)
