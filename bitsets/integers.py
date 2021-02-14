# integers.py - basic integer manipulations

"""Bit manipulation for set rank and unrank."""

import string

__all__ = ['indexes', 'n', 'reinverted', 'rank', 'unrank', 'compress', 'bit_mask']


def indexes(n):
    """Yield index sets unranking n in colexicographical order.

    >>> [tuple(indexes(i)) for i in range(8)]
    [(), (0,), (1,), (0, 1), (2,), (0, 2), (1, 2), (0, 1, 2)]
    """
    i = 0
    while n:
        if n & 1:
            yield i
        i += 1
        n >>= 1


def indexes_optimized(n):
    """Yield index sets unranking n in colexicographical order. Faster version
    of ``indexes``.

    >>> [tuple(indexes_optimized(i)) for i in range(8)]
    [(), (0,), (1,), (0, 1), (2,), (0, 2), (1, 2), (0, 1, 2)]
    """
    for i, b in enumerate(bin(n)[:1:-1]):
        if b == '1':
            yield i


def n(indexes):
    """Return n ranking index sets in colexicographical order.

    >>> [n(ind) for ind in ((), (0,), (1,), (0, 1), (2,))]
    [0, 1, 2, 3, 4]
    """
    return sum(1 << i for i in indexes)


def reinverted(n, r):
    """Integer with reversed and inverted bits of n assuming bit length r.

    >>> reinverted(1, 6)
    31

    >>> [reinverted(x, 6) for x in [7, 11, 13, 14, 19, 21, 22, 25, 26, 28]]
    [7, 11, 19, 35, 13, 21, 37, 25, 41, 49]
    """
    result = 0
    r = 1 << (r - 1)
    while n:
        if not n & 1:
            result |= r
        r >>= 1
        n >>= 1
    if r:
        result |= (r << 1) - 1
    return result


def rank(items, sequence=string.ascii_lowercase):
    """Rank items from sequence in colexicographical order.

    >>> [rank(i) for i in ('', 'a', 'b', 'ab', 'c')]
    [0, 1, 2, 3, 4]

    >>> rank('spam')
    299009
    """
    items = set(items)
    return sum(1 << i for i, s in enumerate(sequence) if s in items)


def unrank(n, sequence=string.ascii_lowercase):
    """Unrank n from sequence in colexicographical order.

    >>> [''.join(unrank(i)) for i in range(8)]
    ['', 'a', 'b', 'ab', 'c', 'ac', 'bc', 'abc']

    >>> unrank(299009)
    ['a', 'm', 'p', 's']
    """
    return list(map(sequence.__getitem__, indexes(n)))


def compress(sequence, n):
    """Filter sequence items unranking n in colexicographical order.

    >>> list(compress(string.ascii_lowercase, 299009))
    ['a', 'm', 'p', 's']

    >>> list(compress('', 1))
    []
    """
    for s in sequence:
        if n & 1:
            yield s
        n >>= 1
        if not n:
            return


def bit_mask(n):
    """Return an integer of n bits length with all bits set.

    >>> bin(bit_mask(5))
    '0b11111'
    """
    return (1 << n) - 1
