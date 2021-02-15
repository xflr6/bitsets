# bitsets - integer bits representing subsets of totally orderd finite set

"""Ordered subsets of a predetermined finite domain."""

from . import bases
from . import meta
from . import series

__all__ = ['bitset']

__title__ = 'bitsets'
__version__ = '0.8.2'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE.txt'
__copyright__ = 'Copyright (c) 2013-2021 Sebastian Bank'


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
        raise ValueError(f'empty bitset name: {name!r}')

    if not hasattr(members, '__getitem__') or not hasattr(members, '__len__'):
        raise ValueError(f'non-sequence bitset members: {members!r}')

    if not len(members):
        raise ValueError(f'less than one bitset member: {members!r}')

    if len(set(members)) != len(members):
        raise ValueError(f'bitset members contains duplicates: {members!r}')

    if not issubclass(base.__class__, meta.MemberBitsMeta):
        raise ValueError(f'base does not subclass bitset.bases: {base!r}')

    list = {False: None, True: series.List}.get(list, list)
    tuple = {False: None, True: series.Tuple}.get(tuple, tuple)

    return base._make_subclass(name, members, listcls=list, tuplecls=tuple)
