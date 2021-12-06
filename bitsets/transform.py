"""Convert between larger integers and chunks of smaller integers and booleans.

Note: chunks have little-endian bit-order
      like gmpy2.(un)pack, but reverse of numpy.(un)packbits
"""

from itertools import compress, zip_longest

__all__ = ['chunkreverse', 'pack', 'unpack', 'packbools', 'unpackbools']

NBITS = {'B': 8, 'H': 16, 'L': 32, 'Q': 64}

ATOMS = {r: [1 << i for i in range(r)] for r in NBITS.values()}

ATOMS.update((t, ATOMS[r]) for t, r in NBITS.items())

NBITS.update({r: r for r in NBITS.values()})

RBYTES = [int('{0:08b}'.format(i)[::-1], 2) for i in range(256)]


def chunkreverse(integers, dtype='L'):
    """Yield integers of dtype bit-length reverting their bit-order.

    >>> list(chunkreverse([0b10000000, 0b11000000, 0b00000001], 'B'))
    [1, 3, 128]

    >>> list(chunkreverse([0x8000, 0xC000, 0x0001], 'H'))
    [1, 3, 32768]
    """
    if dtype in ('B', 8):
        return map(RBYTES.__getitem__, integers)

    fmt = '{0:0%db}' % NBITS[dtype]

    return (int(fmt.format(chunk)[::-1], 2) for chunk in integers)


def pack(chunks, r=32):
    """Return integer concatenating integer chunks of r > 0 bit-length.

    >>> pack([0, 1, 0, 1, 0, 1], 1)
    42

    >>> pack([0, 1], 8)
    256

    >>> pack([0, 1], 0)
    Traceback (most recent call last):
        ...
    ValueError: pack needs r > 0
    """
    if r < 1:
        raise ValueError('pack needs r > 0')

    n = shift = 0

    for c in chunks:
        n += c << shift
        shift += r

    return n


def unpack(n, r=32):
    """Yield r > 0 bit-length integers splitting n into chunks.

    >>> list(unpack(42, 1))
    [0, 1, 0, 1, 0, 1]

    >>> list(unpack(256, 8))
    [0, 1]

    >>> list(unpack(2, 0))
    Traceback (most recent call last):
        ...
    ValueError: unpack needs r > 0
    """
    if r < 1:
        raise ValueError('unpack needs r > 0')

    mask = (1 << r) - 1

    while n:
        yield n & mask
        n >>= r


def packbools(bools, dtype='L'):
    """Yield integers concatenating bools in chunks of dtype bit-length.

    >>> list(packbools([False, True, False, True, False, True], 'B'))
    [42]
    """
    r = NBITS[dtype]
    atoms = ATOMS[dtype]

    for chunk in zip_longest(*[iter(bools)] * r, fillvalue=False):
        yield sum(compress(atoms, chunk))


def unpackbools(integers, dtype='L'):
    """Yield booleans unpacking integers of dtype bit-length.

    >>> list(unpackbools([42], 'B'))
    [False, True, False, True, False, True, False, False]
    """
    atoms = ATOMS[dtype]

    for chunk in integers:
        for a in atoms:
            yield not not chunk & a
