# bases.py - bitset base classes

"""Base classes for bitsets providing integer-like and set-like interface."""

from itertools import compress

from ._compat import long_int, get_unbound_func, map, filter, filterfalse,\
     py2_bool_to_nonzero, with_metaclass

from . import meta, integers, combos

__all__ = ['MemberBits', 'BitSet']

__new__ = long_int.__new__


class MemberBits(with_metaclass(meta.MemberBitsMeta, long_int)):
    """Subsets of a predefined domain as rank in colexicographical order.

    >>> Ints = MemberBits._make_subclass('Ints', (1, 2, 3, 4, 5, 6))

    >>> Ints  # doctest: +ELLIPSIS
    <class bitsets.meta.bitset('Ints', (1, 2, 3, 4, 5, 6), 0x..., MemberBits, None, None)>

    >>> Ints('100011')
    Ints('100011')


    >>> Ints.frommembers([1, 5, 6])
    Ints('100011')

    >>> Ints.frombools([True, '', None, 0, 'yes', 5])
    Ints('100011')

    >>> Ints.frombits('100011')
    Ints('100011')

    >>> Ints.fromint(49)
    Ints('100011')


    >>> Ints('100011').members()
    (1, 5, 6)

    >>> Ints('100011').bools()
    (True, False, False, False, True, True)

    >>> Ints('100011').bits()
    '100011'

    >>> print(Ints('100011').int)
    49


    >>> list(Ints('100011').atoms())
    [Ints('100000'), Ints('000010'), Ints('000001')]

    >>> list(Ints('100011').inatoms())
    [Ints('010000'), Ints('001000'), Ints('000100')]


    >>> triples = [i for i in Ints.supremum.powerset() if i.count() == 3]

    >>> ['%d%d%d' % t.members() for t in triples]  # doctest: +NORMALIZE_WHITESPACE
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

    >>> ['%d%d%d' % t.members() for t in sorted(triples)]  # doctest: +NORMALIZE_WHITESPACE
    ['123',
     '124', '134', '234',
     '125', '135', '235', '145', '245', '345',
     '126', '136', '236', '146', '246', '346', '156', '256', '356', '456']


    >>> uptotwo = [i for i in Ints.supremum.powerset() if i.count() <= 2]

    >>> [''.join(map(str, u.members())) for u in
    ... sorted(uptotwo, key=lambda u: u.shortlex())]  # doctest: +NORMALIZE_WHITESPACE
    ['',  '1',  '2',  '3',  '4',  '5',  '6',
               '12', '13', '14', '15', '16',
                     '23', '24', '25', '26',
                           '34', '35', '36',
                                 '45', '46',
                                       '56']

    >>> [''.join(map(str, u.members())) for u in
    ... sorted(uptotwo, key=lambda u: u.shortcolex())]  # doctest: +NORMALIZE_WHITESPACE
    ['',  '1',  '2',  '3',  '4',  '5',  '6',
          '12',
          '13', '23',
          '14', '24', '34',
          '15', '25', '35', '45',
          '16', '26', '36', '46', '56']

    >>> [''.join(map(str, u.members())) for u in
    ... sorted(uptotwo, key=lambda u: u.longlex())]  # doctest: +NORMALIZE_WHITESPACE
    ['12', '13', '14', '15', '16',
           '23', '24', '25', '26',
                 '34', '35', '36',
                       '45', '46',
                             '56',
     '1',  '2',  '3',  '4',  '5',  '6',  '']

    >>> [''.join(map(str, u.members())) for u in
    ... sorted(uptotwo, key=lambda u: u.longcolex())]  # doctest: +NORMALIZE_WHITESPACE
    ['12',
     '13', '23',
     '14', '24', '34',
     '15', '25', '35', '45',
     '16', '26', '36', '46', '56',
     '1',  '2',  '3',  '4',  '5',  '6',  '']


    >>> Ints('100011').count()
    3

    >>> Ints('111111').all() and not Ints('001010').all()
    True

    >>> Ints('100000').any() and not Ints('000000').any()
    True
    """

    _indexes = integers.indexes

    _reinverted = integers.reinverted

    frombitset = fromint = classmethod(long_int.__new__)

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
            raise ValueError('%r: too many bits.' % bits)
        return cls.fromint(bits[::-1], 2)

    __new__ = frombits.__func__

    def __reduce__(self):
        return __new__, (self.__class__, self.real)

    def copy(self):
        """Return the set unchanged (as its is immutable)."""
        return self

    int = long_int.real

    def members(self):
        """Return the set members tuple."""
        return tuple(map(self._members.__getitem__, self._indexes()))

    def bools(self):
        """Return the boolean sequence of set membership."""
        return tuple(not not self & a for a in self._atoms)

    def bits(self):
        """Return the binary string of set membership."""
        return '{0:0{1}b}'.format(self, self._len)[::-1]

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.bits())

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
                raise ValueError('%r is no subset of %r' % (start, self))
            other = self.fromint(self & ~start)
            other = other.atoms()
        return map(self.frombitset, combos.shortlex(start, list(other)))

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
        """Returns the number of items in the set (cardinality)."""
        return bin(self).count('1')

    def all(self):
        """Return True iff the set contains all domain items."""
        return self == self.supremum

    def any(self):
        """Return True iff the set contains at least one items."""
        return self != self.infimum


@py2_bool_to_nonzero
class BitSet(MemberBits):
    """Ordered container of unique elements from a predefined domain.

    >>> Nums = BitSet._make_subclass('Nums', (1, 2, 3, 4, 5, 6))

    >>> Nums  # doctest: +ELLIPSIS
    <class bitsets.meta.bitset('Nums', (1, 2, 3, 4, 5, 6), 0x..., BitSet, None, None)>

    >>> Nums([1, 2, 3])
    Nums([1, 2, 3])


    >>> list(Nums([1, 2, 3]))
    [1, 2, 3]

    >>> 1 in Nums([1, 2]) and 2 not in Nums([1]) and 1 not in Nums()
    True

    >>> -1 in Nums()
    Traceback (most recent call last):
    ...
    KeyError: -1


    >>> Nums([1]).issubset(Nums([1, 2])) and not Nums([1]).issubset(Nums())
    True

    >>> Nums([1, 2]).issuperset(Nums([1])) and not Nums().issuperset(Nums([1]))
    True

    >>> Nums([1, 2]).isdisjoint(Nums([3, 4])) and not Nums([1]).isdisjoint(Nums([1]))
    True


    >>> Nums([1, 2]).intersection(Nums([2, 3]))
    Nums([2])

    >>> Nums([1, 2]).union(Nums([2, 3]))
    Nums([1, 2, 3])

    >>> Nums([1, 2]).difference(Nums([2, 3]))
    Nums([1])

    >>> Nums([1, 2]).symmetric_difference(Nums([2, 3]))
    Nums([1, 3])


    >>> Nums([1, 2]).complement()
    Nums([3, 4, 5, 6])
    """

    __new__ = MemberBits.frommembers.__func__

    __bool__ = get_unbound_func(MemberBits.any)

    __len__ = get_unbound_func(MemberBits.count)

    def __iter__(self):
        """Iterate over the set members."""
        return map(self._members.__getitem__, self._indexes())

    def __contains__(self, member):
        """Set membership."""
        return self._map[member] & self

    def __repr__(self):
        members = list(map(self._members.__getitem__, self._indexes()))
        arg = '%r' % members if members else ''
        return '%s(%s)' % (self.__class__.__name__, arg)

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
