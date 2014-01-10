# series.py - bitset sequences

"""Ordered collections of BitSet instances."""

from itertools import imap

import meta
import bases

__all__ = ['List', 'Tuple']


class Series(object):

    __metaclass__ = meta.SeriesMeta

    __slots__ = ()

    @classmethod
    def from_bools(cls, bools):
        """Series from iterable of boolean evaluable iterables."""
        return cls.from_bitsets(imap(cls.BitSet.from_bools, bools))

    def __new__(cls, *bits):
        return cls.from_bitsets(imap(cls.BitSet.from_bits, bits))

    from_bits = classmethod(__new__)

    def bools(self):
        """Return the series as list of boolean set membership sequences."""
        return [b.bools() for b in self]

    def __repr__(self):
        items = ', '.join('%r' % b.bits() for b in self)
        return '%s(%s)' % (self.__class__.__name__, items)


class List(Series, list):
    """Sequence of bitsets.

    >>> Ints = bases.BitSet.subclass('Ints', tuple(range(1, 7)), Tuple, List)
    >>> IntsList = Ints.List

    >>> IntsList.from_bools([(True, False, True), (True, True, False)])
    IntsList('101000', '110000')

    >>> IntsList('100100', '000000')
    IntsList('100100', '000000')

    >>> IntsList.from_bits('100100', '000000')
    IntsList('100100', '000000')

    >>> IntsList.from_bitsets([Ints.from_bits('100100')])
    IntsList('100100')

    >>> IntsList('101000').bools()
    [(True, False, True, False, False, False)]

    """

    __slots__ = ()

    _series = 'List'

    __new__ = list.__new__

    def __init__(self, *bits):
        super(List, self).__init__(imap(self.BitSet.from_bits, bits))
        
    @classmethod
    def from_bitsets(cls, bitsets):
        self = cls.__new__(cls, bitsets)
        super(List, self).__init__(bitsets)
        return self


class Tuple(Series, tuple):
    """Immutable sequence of bitsets.

    >>> Ints = bases.BitSet.subclass('Ints', tuple(range(1, 7)), Tuple, List)
    >>> IntsTuple = Ints.Tuple

    >>> IntsTuple.from_bools([(True, False, True), (True, True, False)])
    IntsTuple('101000', '110000')

    >>> IntsTuple('100100', '000000')
    IntsTuple('100100', '000000')

    >>> IntsTuple.from_bits('100100', '000000')
    IntsTuple('100100', '000000')

    >>> IntsTuple.from_bitsets([Ints.from_bits('100100')])
    IntsTuple('100100')

    >>> IntsTuple('101000').bools()
    [(True, False, True, False, False, False)]
    """

    __slots__ = ()

    _series = 'Tuple'

    from_bitsets = classmethod(tuple.__new__)


def _test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    _test()
