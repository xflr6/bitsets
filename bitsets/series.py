# series.py - bitset sequences

"""Ordered collections of bitset instances."""

from itertools import imap

import meta

__all__ = ['List', 'Tuple']


class Series(object):
    """Bitset sequence.

    >>> import bases

    >>> Nums = bases.BitSet._make_subclass('Nums', (1, 2, 3, 4, 5, 6), listcls=List, tuplecls=Tuple)

    >>> Nums.List  # doctest: +ELLIPSIS
    <class bitsets.meta.bitset_list('Nums', (1, 2, 3, 4, 5, 6), 0x..., BitSet, List, Tuple)>

    >>> Nums.Tuple  # doctest: +ELLIPSIS
    <class bitsets.meta.bitset_tuple('Nums', (1, 2, 3, 4, 5, 6), 0x..., BitSet, List, Tuple)>

    >>> Nums.List('101000','110000')
    NumsList('101000', '110000')

    >>> Nums.Tuple('101000','110000')
    NumsTuple('101000', '110000')


    >>> issubclass(Nums.List, list) and issubclass(Nums.Tuple, tuple)
    True

    >>> Nums.List.frombitsets([]), Nums.Tuple.frombitsets([])
    (NumsList(), NumsTuple())
    

    >>> Nums.List.frommembers([(1, 3), (1, 2)])
    NumsList('101000', '110000')

    >>> Nums.List.frombools([(True, False, True), (True, True, False)])
    NumsList('101000', '110000')

    >>> Nums.List.frombits(['101000', '110000'])
    NumsList('101000', '110000')


    >>> Nums.List('101000', '110000').members()
    [(1, 3), (1, 2)]

    >>> Nums.List('101000', '110000').bools()  # doctest: +NORMALIZE_WHITESPACE
    [(True, False, True, False, False, False),
     (True, True, False, False, False, False)]

    >>> Nums.List('101000', '110000').bits()
    ['101000', '110000']


    >>> Nums.List('101000', '110000').reduce_and()
    Nums([1])

    >>> Nums.List('101000', '110000').reduce_or()
    Nums([1, 2, 3])
    """

    __metaclass__ = meta.SeriesMeta

    __slots__ = ()

    @classmethod
    def frommembers(cls, members):
        """Series from iterable of member iterables."""
        return cls.frombitsets(imap(cls.BitSet.frommembers, members))
        
    @classmethod
    def frombools(cls, bools):
        """Series from iterable of boolean evaluable iterables."""
        return cls.frombitsets(imap(cls.BitSet.frombools, bools))

    @classmethod
    def frombits(cls, bits):
        """Series from binary string arguments."""
        return cls.frombitsets(imap(cls.BitSet.frombits, bits))

    def members(self):
        """Return the series as list of set member tuples."""
        return [b.members() for b in self]

    def bools(self):
        """Return the series as list of boolean set membership sequences."""
        return [b.bools() for b in self]

    def bits(self):
        """Return the series as list of binary set membership strings."""
        return [b.bits() for b in self]

    def __repr__(self):
        items = ', '.join('%r' % b.bits() for b in self)
        return '%s(%s)' % (self.__class__.__name__, items)

    def reduce_and(self):
        """Return the intersection of all series elements."""
        return self.BitSet.reduce_and(self)

    def reduce_or(self):
        """Return the union of all series elements."""
        return self.BitSet.reduce_or(self)


class List(Series, list):
    """Mutable bitset sequence."""

    __slots__ = ()

    _series = 'List'

    @classmethod
    def frombitsets(cls, bitsets):
        self = list.__new__(cls, bitsets)
        list.__init__(self, bitsets)
        return self

    __new__ = list.__new__

    def __init__(self, *bits):
        list.__init__(self, imap(self.BitSet.frombits, bits))


class Tuple(Series, tuple):
    """Immutable bitset sequence."""

    __slots__ = ()

    _series = 'Tuple'

    frombitsets = classmethod(tuple.__new__)

    def __new__(cls, *bits):
        return tuple.__new__(cls, imap(cls.BitSet.frombits, bits))
