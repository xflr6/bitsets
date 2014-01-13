Bitsets
========

|PyPI version| |License|

Bitsets are **ordered sets** which are subsets of a predefined
**finite domain** of hashable items.

They are implemented as python **integers** representing the rank
of the set in colexicographical order (a.k.a bit strings,
binary strings). Hence, they are very **space-efficient** e.g. if
a large number of subsets from a collection needs to be present
in memory. Furthermore, they can be compared, intersected, etc.
using normal **bitwise operations** of integers.


Installation
------------

.. code:: bash

    $ pip install bitsets


Creation
--------

Use the ``bitset`` function to create a class representing ordered
subsets from a fixed set of items (the domain):

.. code:: python

    >>> from bitsets import bitset

    >>> Pythons = bitset('Pythons', ('Chapman', 'Cleese', 'Gilliam', 'Idle', 'Jones', 'Palin'))

The domain collection needs to be a hashable sequence (e.g. a ``tuple``).

The resulting class is an integer (``long``) subclass, so its instances
(being integers) are **immutable and hashable** and thus in many ways
similar to pythons built-in ``frozenset``.

.. code:: python

   >>> issubclass(Pythons, long)
   True


The class provides access to the **minimal** (``infimum``) and **maximal**
(``supremum``) sets from its domain:

.. code:: python

    >>> Pythons.infimum
    Pythons()

    >>> Pythons.supremum
    Pythons(['Chapman', 'Cleese', 'Gilliam', 'Idle', 'Jones', 'Palin'])


Basic usage
-----------

Bitsets can be created from members, bit strings, boolean sequences,
and integers. Members always occur in the **definition order**:

.. code:: python

    >>> Pythons(['Palin', 'Cleese'])
    Pythons(['Cleese', 'Palin'])

    >>> Pythons.from_bits('101000')
    Pythons(['Chapman', 'Gilliam'])

    >>> Pythons.from_bools([True, False, True, False, False, False])
    Pythons(['Chapman', 'Gilliam'])

    >>> Pythons.from_int(5)
    Pythons(['Chapman', 'Gilliam'])


Bitsets cannot contain items other than those from their domain:

.. code:: python

    >>> Pythons(['Brian'])
    Traceback (most recent call last):
    ....
    KeyError: 'Brian'


Bitsets can be converted to members, bit strings, boolean sequences
and integers:

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

To facilitate sorting collections of bitsets, they have **key methods**
for different sort orders (``shortlex``, ``longlex``, ``shortcolex``,
and ``longcolex``):

.. code:: python

    >>> Pythons(['Idle']).shortlex() < Pythons(['Palin']).shortlex()
    True

Sorting a collection of bitsets without using a keyfunction will order
them in **colexicographical order**.


Powersets
---------

Iterate over a bitsets' ``powerset`` in short lexicographic order:

.. code:: python

    >>> for p in Pythons(['Palin', 'Idle']).powerset():
    ...     print p.members()
    ()
    ('Idle',)
    ('Palin',)
    ('Idle', 'Palin')


``frozenset`` compatibility
---------------------------

For convenience, bitsets provide the same methods as ``frozenset``
(i.e. ``issubset``, ``issuperset``, ``isdisjoint``, ``intersection``,
``union``, ``difference``, ``symmetric_difference``, ``__len__``,
``__iter__``, ``__nonzero__``, and ``__contains__``).

.. code:: python

    >>> 'Cleese' in Pythons(['Idle'])
    False

    >>> 'Idle' in Pythons(['Idle'])
    True

    >>> Pythons(['Chapman', 'Idle']).intersection(Pythons(['Idle', 'Palin']))
    Pythons(['Idle'])

Note, however that all the **operators methods** retain their **integer semantics**:

.. code:: python

    >>> Pythons(['Chapman', 'Idle']) - Pythons(['Idle'])
    1L


That is, because in tight loops it might be worth to use **bitwise
expressions** for set comparisons/operation instead of the
``frozenset``-compatible methods:

.. code:: python

    >>> # is subset ?
    >>> Pythons(['Idle']) & Pythons(['Chapman', 'Idle']) == Pythons(['Idle'])
    True


Differing from ``frozenset``, you can also retrieve the ``complement`` set
of a bitset:

.. code:: python

    >>> Pythons(['Idle']).complement()
    Pythons(['Chapman', 'Cleese', 'Gilliam', 'Jones', 'Palin'])

    >>> Pythons().complement().complement()
    Pythons()


Advanced usage
--------------

To use a **customized bitset**, extend a class from the ``bitsets.bases``
module and pass it to the ``bitset`` function.

.. code:: python

    >>> import bitsets

    >>> class ProperSet(bitsets.bases.BitSet):
    ...     def issubset_proper(self, other):
    ...         return self & other == self != other

    >>> Ints = bitsets.bitset('Ints', tuple(range(1, 7)), base=ProperSet)

    >>> issubclass(Ints, ProperSet)
    True

    >>> Ints([1]).issubset_proper(Ints([1, 2]))
    True


When activated, each bitset class comes with tailored **collection
classes** (bitset list and bitset tuple) for its instances.

.. code:: python

    >>> Letters = bitsets.bitset('Letters', 'abcdef', list=True)

    >>> Letters.List.from_members(['a', 'bcd', 'ef'])
    LettersList('100000', '011100', '000011')


To use a **customized bitset collection class**, extend a class
from the ``bitsets.series`` module and pass it to the ``bitset`` function

.. code:: python

    >>> class ReduceList(bitsets.series.List):
    ...     def intersection(self):
    ...         return self.BitSet.from_int(reduce(long.__and__, self))
    ...     def union(self):
    ...         return self.BitSet.from_int(reduce(long.__or__, self))

    >>> Nums = bitsets.bitset('Nums', (1, 2, 3), list=ReduceList)

    >>> issubclass(Nums.List, ReduceList)
    True

    >>> numslist = Nums.List.from_members([(1, 2, 3), (1, 2), (2, 3)])

    >>> numslist.intersection()
    Nums([2])

    >>> numslist.union()
    Nums([1, 2, 3])


Bitset classes, collection classes and their instances are **pickleable**:

.. code:: python

    >>> import pickle

    >>> pickle.loads(pickle.dumps(Pythons)) is Pythons
    True

    >>> pickle.loads(pickle.dumps(Pythons()))
    Pythons()

    >>> pickle.loads(pickle.dumps(Nums.List)) is Nums.List  # doctest: +SKIP
    True

    >>> pickle.loads(pickle.dumps(Nums.List()))  # doctest: +SKIP
    NumsList()


Further reading
---------------

- http://wiki.python.org/moin/BitManipulation

- http://en.wikipedia.org/wiki/Bit_array
- http://en.wikipedia.org/wiki/Bit_manipulation

- http://en.wikipedia.org/wiki/Lexicographical_order
- http://en.wikipedia.org/wiki/Colexicographical_order


License
-------

Bitsets is distributed under the `MIT license
<http://opensource.org/licenses/MIT>`_.

.. |PyPI version| image:: https://pypip.in/v/bitsets/badge.png
    :target: https://pypi.python.org/pypi/bitsets
    :alt: Latest PyPI Version
.. |License| image:: https://pypip.in/license/bitsets/badge.png
    :target: https://pypi.python.org/pypi/bitsets
    :alt: License
