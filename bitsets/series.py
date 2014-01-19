# series.py - bitset sequences

"""Ordered collections of bitset instances."""

from itertools import imap

import meta
import bases

__all__ = ['List', 'Tuple']


class Series(object):
    """Abstract bitset sequence."""

    __metaclass__ = meta.SeriesMeta

    __slots__ = ()

    @classmethod
    def from_members(cls, members):
        """Series from iterable of member iterables."""
        return cls.from_bitsets(imap(cls.BitSet.from_members, members))
        
    @classmethod
    def from_bools(cls, bools):
        """Series from iterable of boolean evaluable iterables."""
        return cls.from_bitsets(imap(cls.BitSet.from_bools, bools))

    def __new__(cls, *bits):
        return cls.from_bitsets(imap(cls.BitSet.from_bits, bits))

    from_bits = classmethod(__new__)

    def members(self):
        """Return the series as list of set member tuples."""
        return [b.members() for b in self]

    def bools(self):
        """Return the series as list of boolean set membership sequences."""
        return [b.bools() for b in self]

    def bits(self):
        """Return the series as list of binary set membership strings."""
        return [b.bools() for b in self]

    def __repr__(self):
        items = ', '.join('%r' % b.bits() for b in self)
        return '%s(%s)' % (self.__class__.__name__, items)

    def reduce_and(self):
        return self.BitSet.reduce_and(self)

    def reduce_or(self):
        return self.BitSet.reduce_or(self)


class List(Series, list):
    """Mutable bitset sequence.

    >>> Ints = bases.BitSet.subclass('Ints', tuple(range(1, 7)), List, Tuple)
    >>> IntsList = Ints.List
    >>> issubclass(IntsList, list)
    True

    >>> IntsList.from_members([(1, 3), (1, 2)])
    IntsList('101000', '110000')

    >>> IntsList.from_bools([(True, False, True), (True, True, False)])
    IntsList('101000', '110000')

    >>> IntsList('100100', '000000')
    IntsList('100100', '000000')

    >>> IntsList.from_bits('100100', '000000')
    IntsList('100100', '000000')

    >>> IntsList.from_bitsets([Ints.from_bits('100100')])
    IntsList('100100')

    >>> IntsList('101000').members()
    [(1, 3)]

    >>> IntsList('101000').bools()
    [(True, False, True, False, False, False)]

    >>> IntsList('101000').bits()
    [(True, False, True, False, False, False)]

    >>> IntsList('100100', '000100').reduce_and()
    Ints([4])

    >>> IntsList('100100', '000100').reduce_or()
    Ints([1, 4])
    """

    __slots__ = ()

    _series = 'List'

    @classmethod
    def from_bitsets(cls, bitsets):
        self = list.__new__(cls, bitsets)
        list.__init__(self, bitsets)
        return self

    __new__ = list.__new__

    def __init__(self, *bits):
        list.__init__(self, imap(self.BitSet.from_bits, bits))


class Tuple(Series, tuple):
    """Immutable bitset sequence.

    >>> Ints = bases.BitSet.subclass('Ints', tuple(range(1, 7)), List, Tuple)
    >>> IntsTuple = Ints.Tuple
    >>> issubclass(IntsTuple, tuple)
    True

    >>> IntsTuple.from_members([(1, 3), (1, 2)])
    IntsTuple('101000', '110000')

    >>> IntsTuple.from_bools([(True, False, True), (True, True, False)])
    IntsTuple('101000', '110000')

    >>> IntsTuple('100100', '000000')
    IntsTuple('100100', '000000')

    >>> IntsTuple.from_bits('100100', '000000')
    IntsTuple('100100', '000000')

    >>> IntsTuple.from_bitsets([Ints.from_bits('100100')])
    IntsTuple('100100')

    >>> IntsTuple('101000').members()
    [(1, 3)]

    >>> IntsTuple('101000').bools()
    [(True, False, True, False, False, False)]

    >>> IntsTuple('101000').bits()
    [(True, False, True, False, False, False)]

    >>> IntsTuple('100100', '000100').reduce_and()
    Ints([4])

    >>> IntsTuple('100100', '000100').reduce_or()
    Ints([1, 4])
    """

    __slots__ = ()

    _series = 'Tuple'

    from_bitsets = classmethod(tuple.__new__)


def _test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    _test()
