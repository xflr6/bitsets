# bases.py - bitset base classes

"""Base classes for bitsets providing integer-like and set-like interface."""

from itertools import compress, filterfalse

from . import combos
from . import integers
from . import meta

__all__ = ['MemberBits', 'BitSet']

__new__ = int.__new__


class MemberBits(int, metaclass=meta.MemberBitsMeta):
    """Subsets of a predefined domain as rank in colexicographical order.

    Args:
        bits: String with the binary membership representation.
    """

    _indexes = integers.indexes_optimized

    _reinverted = integers.reinverted

    frombitset = fromint = classmethod(int.__new__)

    @classmethod
    def frommembers(cls, members=()):
        """Create a set from an iterable of members."""
        return cls.fromint(sum(map(cls._map.__getitem__, set(members))))

    @classmethod
    def frombools(cls, bools=()):
        """Create a set from an iterable of boolean evaluable items."""
        return cls.fromint(sum(compress(cls._atoms, bools)))

    @classmethod
    def frombits(cls, bits='0'):
        """Create a set from binary string."""
        if len(bits) > cls._len:
            raise ValueError(f'too many bits {bits!r}')
        return cls.fromint(bits[::-1], 2)

    __new__ = frombits.__func__

    def __reduce__(self):
        return __new__, (self.__class__, self._int)

    def copy(self):
        """Return the set unchanged (as its is immutable)."""
        return self

    int = _int = int.real

    iter_set = integers.indexes

    def members(self, as_set=False):
        """Return the set members tuple/frozenset."""
        if as_set:
            return frozenset(map(self._members.__getitem__, self._indexes()))
        return tuple(map(self._members.__getitem__, self._indexes()))

    def bools(self):
        """Return the boolean sequence of set membership."""
        return tuple(not not self & a for a in self._atoms)

    def bits(self):
        """Return the binary string of set membership."""
        return '{0:0{1}b}'.format(self, self._len)[::-1]

    def __repr__(self):
        return f'{self.__class__.__name__}({self.bits()!r})'

    def atoms(self, reverse=False):
        """Yield the singleton for every set member."""
        if reverse:
            return filter(self.__and__, reversed(self._atoms))
        return filter(self.__and__, self._atoms)

    def inatoms(self, reverse=False):
        """Yield the singleton for every non-member."""
        if reverse:
            return filterfalse(self.__and__, reversed(self._atoms))
        return filterfalse(self.__and__, self._atoms)

    def powerset(self, start=None, excludestart=False):
        """Yield combinations from start to self in short lexicographic order."""
        if start is None:
            start = self.infimum
            other = self.atoms()
        else:
            if self | start != self:
                raise ValueError(f'{start!r} is no subset of {self!r}')
            other = self.fromint(self & ~start).atoms()
        return map(self.frombitset, combos.shortlex(start, list(other)))

    def shortlex(self):
        """Return sort key for short lexicographical order."""
        return bin(self).count('1'), self._reinverted(self._len)

    def longlex(self):
        """Return sort key for long lexicographical order."""
        return -bin(self).count('1'), self._reinverted(self._len)

    def shortcolex(self):
        """Return sort key for short colexicographical order."""
        return bin(self).count('1'), self._int

    def longcolex(self):
        """Return sort key for long colexicographical order."""
        return -bin(self).count('1'), self._int

    def count(self, value=True):
        """Returns the number of present/absent members."""
        if value not in (True, False):
            raise ValueError(f'can only count True or False, not {value!r}')
        return bin(self)[2:].count('01'[value])

    def all(self):
        """Return True iff the set contains all domain items."""
        return self == self.supremum

    def any(self):
        """Return True iff the set contains at least one item."""
        return self != self.infimum


class BitSet(MemberBits):
    """Ordered container of unique elements from a predefined domain.

    Args:
        members: Iterable of domain members.
    Raises:
        KeyError: if a member is not in the domain of the set.
    """

    __new__ = MemberBits.frommembers.__func__

    __bool__ = MemberBits.any

    def __len__(self):
        """Return the number of items in the set (cardinality)."""
        return bin(self).count('1')

    def __iter__(self):
        """Iterate over the set members."""
        return map(self._members.__getitem__, self._indexes())

    def __contains__(self, member):
        """Set membership.

        Raises:
            KeyError: if member is not in the domain of the set.
        """
        return self._map[member] & self

    def __repr__(self):
        members = list(map(self._members.__getitem__, self._indexes()))
        arg = repr(members) if members else ''
        return f'{self.__class__.__name__}({arg})'

    def issubset(self, other):
        """Inverse set containment."""
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self & other == self

    def issuperset(self, other):
        """Set containment."""
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self | other == self

    def isdisjoint(self, other):
        """Set disjointness."""
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return not self & other

    def intersection(self, other):
        """Set intersection."""
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self.frombitset(self & other)

    def union(self, other):
        """Set union."""
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self.frombitset(self | other)

    def difference(self, other):
        """Set difference."""
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self.frombitset(self & ~other)

    def symmetric_difference(self, other):
        """Symmetric set difference."""
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self.frombitset(self ^ other)

    def complement(self):
        """Complement set."""
        return self.frombitset(self ^ self.supremum)
