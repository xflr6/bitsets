# integers.py - basic integer manipulations

"""Bit manipulation for set rank and unrank."""

__all__ = ['indexes', 'reinverted']


def indexes(n):
    """Yield indexes unranking n in colexicographical order.

    >>> [tuple(indexes(i)) for i in range(8)]
    [(), (0,), (1,), (0, 1), (2,), (0, 2), (1, 2), (0, 1, 2)]
    """
    i = 0
    while n:
        if n & 1:
            yield i
        i += 1
        n >>= 1


def reinverted(n, r):
    """Integer with reversed and inverted bits of n assuming bit length r.

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


def unrank(n, sequence='abcdefghijklmnopqrstuvwxyz'):
    """Unrank n from sequence in colexicographical order.

    >>> [''.join(unrank(i)) for i in range(8)]
    ['', 'a', 'b', 'ab', 'c', 'ac', 'bc', 'abc']
    >>> unrank(147491)
    ['a', 'b', 'f', 'o', 'r']
    """
    return map(sequence.__getitem__, indexes(n))


def _test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    _test()
