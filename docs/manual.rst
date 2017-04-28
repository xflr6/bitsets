.. _manual:

User Guide
==========

Bitsets are **immutable ordered sets** drawn from a predefined **finite sequence**
of hashable items.

They are implemented as pure Python **integers** representing the rank of the
set in colexicographical order (a.k.a bit strings, powers of two, binary
strings). Hence, they can be very **space-efficient**, e.g. if a large number of
subsets from a collection needs to be present in memory. Furthermore, they can
also be compared, intersected, etc. using normal **bitwise operations** of
integers (``&, |, ^, ~``).


Installation
------------

:mod:`bitsets` is a pure-python package that runs both under Python 2.7 and 3.3+.
To install it with using pip_, run the following command:

.. code:: bash

    $ pip install bitsets

There are no other dependencies. Optionally, you can install Graphviz_ and this
`Python wrapper`_ to be able to draw Hasse diagrams of all possible sets from
a bitsets' object pool (see :ref:`advanced`).


Creation
--------

Use the :func:`~.bitset` function to create a class representing ordered
subsets from a fixed set of items (the *domain*):

.. code:: python

    >>> from bitsets import bitset

    >>> PYTHONS = ('Chapman', 'Cleese', 'Gilliam', 'Idle', 'Jones', 'Palin')

    >>> Pythons = bitset('Pythons', PYTHONS)

The domain needs to be a hashable duplicate-free sequence of at least one item
(usually, a ``tuple``).

The resulting class is an integer (``int`` or ``long`` depending on Python
version) subclass, so its instances (being integers) are **immutable and
hashable** and thus in many ways similar to Python's built-in
:class:`py:frozenset`.

.. code:: python

    >>> from bitsets._compat import integer_types

    >>> issubclass(Pythons, integer_types)
    True


Each domain item is mapped to a **power of two** (their *rank* in
colexicographical order):

.. code:: python

    >>> Pythons.fromint(0)
    Pythons()

    >>> [Pythons.fromint(1), Pythons.fromint(2), Pythons.fromint(4)]
    [Pythons(['Chapman']), Pythons(['Cleese']), Pythons(['Gilliam'])]

    >>> Pythons.fromint(3)
    Pythons(['Chapman', 'Cleese'])

    >>> Pythons.fromint(2 ** 6 - 1)
    Pythons(['Chapman', 'Cleese', 'Gilliam', 'Idle', 'Jones', 'Palin'])

    >>> Pythons.fromint((1 << 0) + (1 << 5))
    Pythons(['Chapman', 'Palin'])


The class provides access to the **minimal** (:attr:`~.Bitset.infimum`) and
**maximal** (:attr:`~.Bitset.supremum`) sets from its domain:

.. code:: python

    >>> Pythons.infimum
    Pythons()

    >>> Pythons.supremum
    Pythons(['Chapman', 'Cleese', 'Gilliam', 'Idle', 'Jones', 'Palin'])



Basic usage
-----------

Bitsets can be created from members, bit strings, boolean sequences, and
integers:

.. code:: python

    >>> Pythons(['Palin', 'Cleese'])
    Pythons(['Cleese', 'Palin'])

    >>> Pythons.frombits('101000')
    Pythons(['Chapman', 'Gilliam'])

    >>> Pythons.frombools([True, False, True, False, False, False])
    Pythons(['Chapman', 'Gilliam'])

    >>> Pythons.fromint(5)
    Pythons(['Chapman', 'Gilliam'])

Members always occur in the **definition order**.

Bitsets cannot contain items other than those from their domain:

.. code:: python

    >>> Pythons(['Brian'])
    Traceback (most recent call last):
    ....
    KeyError: 'Brian'

    >>> 'Spam' in Pythons(['Jones'])
    Traceback (most recent call last):
    ...
    KeyError: 'Spam'


Bitsets can be converted to members, bit strings, boolean sequences and
integers:

.. code:: python

    >>> Pythons(['Chapman', 'Gilliam']).members()
    ('Chapman', 'Gilliam')

    >>> Pythons(['Chapman', 'Gilliam']).bits()
    '101000'

    >>> Pythons(['Chapman', 'Gilliam']).bools()
    (True, False, True, False, False, False)

    >>> int(Pythons(['Chapman', 'Gilliam']))
    5


Sorting
-------

To facilitate sorting collections of bitsets, they have **key methods** for
different sort orders (:meth:`~.BitSet.shortlex`, :meth:`~.BitSet.shortcolex`,
:meth:`~.BitSet.longlex`, and :meth:`~.BitSet.longcolex`):

.. code:: python

    >>> Pythons(['Idle']).shortlex() < Pythons(['Palin']).shortlex()
    True

These orderings are derived from the number of set members and the definition
order of the items.

.. code:: python

    >>> Digits = bitset('Digits', '12345')
    >>> onetwo = [d for d in Digits('12345').powerset() if d.count() in (1, 2)]

    >>> shortlex = sorted(onetwo, key=lambda d: d.shortlex())
    >>> [''.join(d) for d in shortlex]  # doctest: +NORMALIZE_WHITESPACE
    ['1',  '2',  '3',  '4',  '5',
          '12', '13', '14', '15',
                '23', '24', '25',
                      '34', '35',
                            '45']

    >>> shortcolex = sorted(onetwo, key=lambda d: d.shortcolex())
    >>> [''.join(d) for d in shortcolex]  # doctest: +NORMALIZE_WHITESPACE
    ['1',  '2',  '3',  '4',  '5',
     '12',
     '13', '23',
     '14', '24', '34',
     '15', '25', '35', '45']

Sorting a collection of bitsets without the use of a key function will order
them in **colexicographical order**.

.. code:: python

    >>> [''.join(d) for d in sorted(onetwo)]  # doctest: +NORMALIZE_WHITESPACE
    ['1',
     '2', '12',
     '3', '13', '23',
     '4', '14', '24', '34',
     '5', '15', '25', '35', '45']


Powersets
---------

Iterate over a bitsets' :meth:`~.BitSet.powerset` in short lexicographic order:

.. code:: python

    >>> for p in Pythons(['Palin', 'Idle']).powerset():
    ...     print(p.members())
    ()
    ('Idle',)
    ('Palin',)
    ('Idle', 'Palin')

This is the same order as generated by :mod:`py:itertools` recipes_
``powerset(iterable)``.


``frozenset`` compatibility
---------------------------

For convenience, bitsets provide the same methods as :class:`py:frozenset`
(i.e. :meth:`~.BitSet.issubset`, :meth:`~.BitSet.issuperset`,
:meth:`~.BitSet.isdisjoint`, :meth:`~.BitSet.intersection`,
:meth:`~.BitSet.union`, :meth:`~.BitSet.difference`,
:meth:`~.BitSet.symmetric_difference`, :meth:`~.BitSet.__len__`,
:meth:`~.BitSet.__iter__`, :meth:`~.BitSet.__bool__`,
:meth:`~.BitSet.__contains__`, and as a non-op :meth:`~.BitSet.copy`).

.. code:: python

    >>> 'Cleese' in Pythons(['Idle'])
    False

    >>> 'Idle' in Pythons(['Idle'])
    True

    >>> Pythons(['Chapman', 'Idle']).intersection(Pythons(['Idle', 'Palin']))
    Pythons(['Idle'])

Note, however that all the **operators methods** (``+, -, &, |`` etc.) retain
their **integer semantics**:

.. code:: python

    >>> print(Pythons(['Chapman', 'Idle']) - Pythons(['Idle']))
    1


In tight loops it might be worth to use **bitwise expressions** (``&, |, ^, ~``)
for set comparisons/operations instead of the :class:`py:frozenset`-compatible
methods:

.. code:: python

    >>> # is subset ?
    >>> Pythons(['Idle']) & Pythons(['Chapman', 'Idle']) == Pythons(['Idle'])
    True


Added functionality
-------------------

Differing from :class:`py:frozenset`, you can also retrieve the
:meth:`~.BitSet.complement` set of a bitset:

.. code:: python

    >>> Pythons(['Idle']).complement()
    Pythons(['Chapman', 'Cleese', 'Gilliam', 'Jones', 'Palin'])

    >>> Pythons().complement().complement()
    Pythons()


Test if a bitset is maximal (the :attr:`~.BitSet.supremum`):

.. code:: python

    >>> Pythons(['Idle']).all()
    False

    >>> Pythons(['Chapman', 'Cleese', 'Gilliam', 'Idle', 'Jones', 'Palin']).all()
    True


Test if a bitset is non-minimal (the :attr:`~.BitSet.infimum`), same as
``bool(bitset)``:

.. code:: python

    >>> Pythons(['Idle']).any()
    True

    >>> Pythons().any()
    False


.. _pip: https://pip.readthedocs.io
.. _Graphviz: http://www.graphviz.org
.. _Python wrapper: https://pypi.python.org/pypi/graphviz

.. _recipes: https://docs.python.org/2/library/itertools.html#recipes
