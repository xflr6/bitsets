# bitsets - implement ordered subsets of a finite domain

"""Ordered subsets of a predetermined finite domain."""

__title__ = 'bitsets'
__version__ = '0.1.1'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE.txt'
__copyright__ = 'Copyright (c) 2013-2014 Sebastian Bank'

import bases
import series

__all__ = ['bitset']


def bitset(name, members, cached=None, base=bases.BitSet, list=False, tuple=False):
    """Return concrete bitset subclass with given name and members.

    >>> Letters = bitset('Letters', 'abcdef', list=True, tuple=True)

    >>> Letters  # doctest: +ELLIPSIS
    <class meta.bitset('Letters', 'abcdef', 0x..., BitSet, List, Tuple)>

    >>> Letters.Tuple  # doctest: +ELLIPSIS
    <class meta.bitset_tuple('Letters', 'abcdef', 0x..., BitSet, List, Tuple)>

    >>> Letters.from_members('abf')
    Letters(['a', 'b', 'f'])
    """
    list = {False: None, True: series.List}.get(list, list)
    tuple = {False: None, True: series.Tuple}.get(tuple, tuple)
    created, cls = base._get_subclass(name, members, cached, list, tuple)
    return cls


def _test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    _test()
