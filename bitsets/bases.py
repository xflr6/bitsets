# bases.py - bitset base classes

"""Base classes for bitsets providing integer-like and set-like interface."""

from itertools import imap, compress, ifilter, ifilterfalse

import meta
import integers
import combos

__all__ = ['MemberBits', 'BitSet']


class MemberBits(long):
    """Subsets of a predefined domain as rank in colexicographical order.

    >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))

    >>> Ints.fromint(49)
    Ints('100011')

    >>> Ints('100011').int
    49L

    >>> triples = sorted(i for i in Ints.supremum.powerset() if i.count() == 3)
    >>> ['%d%d%d' % t.members() for t in triples]  # doctest: +NORMALIZE_WHITESPACE
    ['123',
     '124', '134', '234',
     '125', '135', '235', '145', '245', '345',
     '126', '136', '236', '146', '246', '346', '156', '256', '356', '456']
    """

    __metaclass__ = meta.MemberBitsMeta

    _indexes = integers.indexes

    _reinverted = integers.reinverted

    frombitset = fromint = classmethod(long.__new__)

    @classmethod
    def frommembers(cls, members=()):
        """Create a set from an iterable of members.

        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> Ints.frommembers([1, 5, 6])
        Ints('100011')
        """
        return cls.fromint(sum(imap(cls._map.__getitem__, set(members))))

    @classmethod
    def frombools(cls, bools=()):
        """Create a set from an iterable of boolean evaluable items.

        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> Ints.frombools([True, '', None, 0, 'yes', 5])
        Ints('100011')
        """
        return cls.fromint(sum(compress(cls._atoms, bools)))

    @classmethod
    def frombits(cls, bits='0'):
        """Create a set from binary string.

        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> Ints.frombits('100011')
        Ints('100011')
        """
        if len(bits) > cls._len:
            raise ValueError(bits)
        return cls.fromint(bits[::-1], 2)

    __new__ = frombits.__func__

    int = long.real

    def members(self):
        """Return the set members tuple.

        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> Ints('100011').members()
        (1, 5, 6)
        """
        return tuple(imap(self._members.__getitem__, self._indexes()))

    def bools(self):
        """Return the boolean sequence of set membership.

        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> Ints('100011').bools()
        (True, False, False, False, True, True)
        """
        return tuple(not not self & a for a in self._atoms)

    def bits(self):
        """Return the binary string of set membership.

        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> Ints('100011').bits()
        '100011'
        """
        return '{0:0{1}b}'.format(self, self._len)[::-1]

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.bits())

    def atoms(self):
        """Yield the singleton for every set member.

        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> list(Ints('100011').atoms())
        [Ints('100000'), Ints('000010'), Ints('000001')]
        """
        return ifilter(self.__and__, self._atoms)

    def inatoms(self):
        """Yield the singleton for every non-member.

        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> list(Ints('100011').inatoms())
        [Ints('010000'), Ints('001000'), Ints('000100')]
        """
        return ifilterfalse(self.__and__, self._atoms)

    def powerset(self, start=None, excludestart=False):
        """Yield combinations from start to self in short lexicographic order.

        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> triples = [i for i in Ints.supremum.powerset() if i.count() == 3]
        >>> ['%d%d%d' % t.members() for t in triples] # doctest: +NORMALIZE_WHITESPACE
        ['123', '124', '125', '126',
                '134', '135', '136',
                       '145', '146',
                              '156',
                '234', '235', '236',
                       '245', '246',
                              '256',
                       '345', '346',
                              '356',
                              '456']
        """
        if start is None:
            start = self.infimum
            other = self.atoms()
        else:
            if self | start != self:
                raise ValueError('%r is no subset of %r' % (start, self))
            other = self & ~start
            other = other.atoms()
        return imap(self.frombitset, combos.shortlex(start, list(other)))

    def shortlex(self):
        """Return sort key for short lexicographical order."""
        return bin(self).count('1'), self._reinverted(self._len)

    def longlex(self):
        """Return sort key for long lexicographical order."""
        return -bin(self).count('1'), self._reinverted(self._len)

    def shortcolex(self):
        """Return sort key for short colexicographical order."""
        return bin(self).count('1'), self.int

    def longcolex(self):
        """Return sort key for long colexicographical order."""
        return -bin(self).count('1'), self.int

    def count(self):
        """Returns the number of items in the set (cardinality).
        
        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> Ints('100011').count()
        3
        """
        return bin(self).count('1')

    def all(self):
        """Return True iff the set contains all domain items.

        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> Ints('111111').all() and not Ints('001010').all()
        True
        """
        return self == self.supremum

    def any(self):
        """Return True iff the set contains at least one items.

        >>> Ints = MemberBits.subclass('Ints', tuple(range(1, 7)))
        >>> Ints('100000').any() and not Ints('000000').any()
        True
        """
        return self != self.infimum


class BitSet(MemberBits):
    """Ordered container of unique elements from a predefined domain.

    >>> Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))

    >>> Numbers([1, 2, 3])
    Numbers([1, 2, 3])
    """

    __new__ = MemberBits.frommembers.__func__

    __len__ = MemberBits.count.__func__

    __nonzero__ = MemberBits.any.__func__

    def __repr__(self):
        members = map(self._members.__getitem__, self._indexes())
        arg = '%r' % members if members else ''
        return '%s(%s)' % (self.__class__.__name__, arg)

    def __iter__(self):
        """Iterator over the set members.

        >>> Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))
        >>> list(Numbers([1, 2, 3]))
        [1, 2, 3]
        """
        return imap(self._members.__getitem__, self._indexes())

    def __contains__(self, member):
        """Set membership.

        >>> Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))
        >>> assert 1 in Numbers([1, 2]) and 2 not in Numbers([1])
        >>> assert 1 not in Numbers()

        >>> -1 in Numbers()
        Traceback (most recent call last):
        ...
        KeyError: -1
        """
        return self._map[member] & self
        
    def issubset(self, other):
        """Inverse set containment.

        >>> Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))
        >>> assert Numbers([1]).issubset(Numbers([1, 2]))
        >>> assert not Numbers([1]).issubset(Numbers())
        """
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self & other == self

    def issuperset(self, other):
        """Set containment.

        >>> Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))
        >>> assert Numbers([1, 2]).issuperset(Numbers([1]))
        >>> assert not Numbers().issuperset(Numbers([1]))
        """
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self | other == self

    def isdisjoint(self, other):
        """Set disjointness.

        >>> Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))
        >>> assert Numbers([1, 2]).isdisjoint(Numbers([3, 4]))
        >>> assert not Numbers([1]).isdisjoint(Numbers([1]))
        """
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return not self & other

    def intersection(self, other):
        """Set intersection.

        >>> Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))
        >>> Numbers([1, 2]).intersection(Numbers([2, 3]))
        Numbers([2])
        """
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self.frombitset(self & other)

    def union(self, other):
        """Set union.

        >>> Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))
        >>> Numbers([1, 2]).union(Numbers([2, 3]))
        Numbers([1, 2, 3])
        """
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self.frombitset(self | other)

    def difference(self, other):
        """Set difference.

        >>> Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))
        >>> Numbers([1, 2]).difference(Numbers([2, 3]))
        Numbers([1])
        """
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self.frombitset(self & ~other)

    def symmetric_difference(self, other):
        """Symmetric set difference.

        >>> Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))
        >>> Numbers([1, 2]).symmetric_difference(Numbers([2, 3]))
        Numbers([1, 3])
        """
        if not isinstance(other, self.__class__):
            other = self.frommembers(other)
        return self.frombitset(self ^ other)

    def complement(self):
        """Complement set.

        >>> Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))
        >>> Numbers([1, 2]).complement()
        Numbers([3, 4, 5, 6])
        """
        return self.frombitset(self ^ self.supremum)


def _test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    _test()
    Numbers = BitSet.subclass('Numbers', tuple(range(1, 7)))
