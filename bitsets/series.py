"""Sequences (ordered collections) of bitset instances."""

from . import meta

__all__ = ['List', 'Tuple']


class Series(metaclass=meta.SeriesMeta):
    """Bitset sequence."""

    __slots__ = ()

    @classmethod
    def frommembers(cls, members):
        """Series from iterable of member iterables."""
        return cls.frombitsets(map(cls.BitSet.frommembers, members))

    @classmethod
    def frombools(cls, bools):
        """Series from iterable of boolean evaluable iterables."""
        return cls.frombitsets(map(cls.BitSet.frombools, bools))

    @classmethod
    def frombits(cls, bits):
        """Series from binary string arguments."""
        return cls.frombitsets(map(cls.BitSet.frombits, bits))

    @classmethod
    def fromints(cls, ints):
        """Series from integer rank arguments."""
        return cls.frombitsets(map(cls.BitSet.fromint, ints))

    def members(self, as_set=False):
        """Return the series as list of set member tuples/frozensets."""
        return [b.members(as_set) for b in self]

    def bools(self):
        """Return the series as list of boolean set membership sequences."""
        return [b.bools() for b in self]

    def bits(self):
        """Return the series as list of binary set membership strings."""
        return [b.bits() for b in self]

    def ints(self):
        """Return the series as list of integers ranks."""
        return [b.int for b in self]

    def __repr__(self):
        items = ', '.join(f'{b.bits()!r}' for b in self)
        return f'{self.__class__.__name__}({items})'

    def index_sets(self, as_set=False):
        """Return the series as list of index set tuples."""
        indexes = frozenset if as_set else tuple
        return [indexes(b.iter_set()) for b in self]

    def reduce_and(self):
        """Return the intersection of all series elements."""
        return self.BitSet.reduce_and(self)

    def reduce_or(self):
        """Return the union of all series elements."""
        return self.BitSet.reduce_or(self)


class List(Series, list):
    """Mutable bitset sequence.

    Args:
        *bits(str): Strings with the binary membership representation.
    """

    __slots__ = ()

    _series = 'List'

    @classmethod
    def frombitsets(cls, bitsets):
        self = list.__new__(cls, bitsets)
        list.__init__(self, bitsets)
        return self

    __new__ = list.__new__

    def __init__(self, *bits):
        list.__init__(self, map(self.BitSet.frombits, bits))


class Tuple(Series, tuple):
    """Immutable bitset sequence.

    Args:
        *bits(str): Strings with the binary membership representation.
    """

    __slots__ = ()

    _series = 'Tuple'

    frombitsets = classmethod(tuple.__new__)

    def __new__(cls, *bits):
        return tuple.__new__(cls, map(cls.BitSet.frombits, bits))
