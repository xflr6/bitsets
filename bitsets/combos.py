"""Powerset generators based on combining integers or sets."""

import collections

__all__ = ['shortlex', 'reverse_shortlex']


def shortlex(start, other, excludestart=False):
    """Yield all unions of start with other in shortlex order.

    >>> ['{:03b}'.format(s) for s in shortlex(0, [0b100, 0b010, 0b001])]
    ['000', '100', '010', '001', '110', '101', '011', '111']

    >>> ', '.join(''.join(sorted(s))
    ... for s in shortlex(set(), [{'a'}, {'b'}, {'c'}, {'d'}]))
    ', a, b, c, d, ab, ac, ad, bc, bd, cd, abc, abd, acd, bcd, abcd'

    >>> assert list(shortlex(set(), [{1}, {2}], excludestart=True)) == \
        [{1}, {2}, {1, 2}]
    """
    if not excludestart:
        yield start

    queue = collections.deque([(start, other)])

    while queue:
        current, other = queue.popleft()

        while other:
            first, other = other[0], other[1:]
            result = current | first

            yield result

            if other:
                queue.append((result, other))


def reverse_shortlex(end, other, excludeend=False):
    """Yield all intersections of end with other in reverse shortlex order.

    >>> ['{:03b}'.format(s) for s in reverse_shortlex(0b111, [0b011, 0b101, 0b110])]
    ['111', '011', '101', '110', '001', '010', '100', '000']

    >>> ', '.join(''.join(sorted(s))
    ... for s in reverse_shortlex({'a', 'b', 'c', 'd'},
    ... [{'b', 'c', 'd'}, {'a', 'c', 'd'}, {'a', 'b', 'd'}, {'a', 'b', 'c'}]))
    'abcd, bcd, acd, abd, abc, cd, bd, bc, ad, ac, ab, d, c, b, a, '

    >>> assert list(reverse_shortlex({1, 2}, [{1}, {2}], excludeend=True)) == \
        [{1}, {2}, set()]
    """
    if not excludeend:
        yield end

    queue = collections.deque([(end, other)])

    while queue:
        current, other = queue.popleft()

        while other:
            first, other = other[0], other[1:]
            result = current & first

            yield result

            if other:
                queue.append((result, other))
