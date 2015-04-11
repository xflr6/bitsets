Bitsets
=======

|PyPI version| |License| |Supported Python| |Format| |Downloads|

This package provides a memory-efficient pure-python **immutable ordered set
data type** for working with large numbers of subsets from a predetermined pool
of objects.

Given a name and a tuple of hashable objects, the ``bitset()``-function returns
a custom integer subclass for creating ordered subsets from the object pool.
Each instance is a Python integer where the presence/absence of the *nth* pool
item is its *nth* bit being set/unset (a.k.a. bit strings, powers of two, rank
in *colexicographical* order).

Being just a regular (long) integer with some convenience methods for
translating between unique object collections and bit patterns allows to
perform certain tasks in a more natural way, e.g. sorting a collection of sets
lexicographically, or enumerating possible combinations in an ordered fashion.


Links
-----

- GitHub: http://github.com/xflr6/bitsets
- PyPI: http://pypi.python.org/pypi/bitsets
- Download: http://pypi.python.org/pypi/bitsets#downloads
- Documentation: http://bitsets.readthedocs.org
- Changelog: http://bitsets.readthedocs.org/en/latest/changelog.html
- Issue Tracker: http://github.com/xflr6/bitsets/issues


Installation
------------

This package runs under Python 2.7 and 3.3+ and has no required dependencies,
use pip_ to install:

.. code:: bash

    $ pip install bitsets


Quickstart
----------

Create a class for sets taken from your pool of objects:

.. code:: python

    >>> from bitsets import bitset

    >>> PYTHONS = ('Chapman', 'Cleese', 'Gilliam', 'Idle', 'Jones', 'Palin')

    >>> Pythons = bitset('Pythons', PYTHONS)


Access its maximal and minimal instances. Retrieve instance members in
definition order:

.. code:: python

    >>> Pythons.supremum
    Pythons(['Chapman', 'Cleese', 'Gilliam', 'Idle', 'Jones', 'Palin'])

    >>> Pythons.infimum
    Pythons()

    >>> Pythons(['Idle', 'Gilliam', 'Idle', 'Idle']).members()
    ('Gilliam', 'Idle')


Translate to/from bit string, boolean sequence, and int:

.. code:: python

    >>> Pythons(['Chapman', 'Gilliam']).bits()
    '101000'

    >>> Pythons.frombits('101000')
    Pythons(['Chapman', 'Gilliam'])

    >>> Pythons(['Chapman', 'Gilliam']).bools()
    (True, False, True, False, False, False)

    >>> Pythons.frombools([True, None, 1, False, 0])
    Pythons(['Chapman', 'Gilliam'])
    
    >>> int(Pythons(['Chapman', 'Gilliam']))
    5

    >>> Pythons.fromint(5)
    Pythons(['Chapman', 'Gilliam'])
    

Set operation and comparison methods (cf. build-in ``frozenset``):

.. code:: python

    >>> Pythons(['Jones', 'Cleese', 'Idle']).intersection(Pythons(['Idle']))
    Pythons(['Idle'])

    >>> Pythons(['Idle']).union(Pythons(['Jones', 'Cleese']))
    Pythons(['Cleese', 'Idle', 'Jones'])

    >>> Pythons.supremum.difference(Pythons(['Chapman', 'Cleese']))
    Pythons(['Gilliam', 'Idle', 'Jones', 'Palin'])

    >>> Pythons(['Palin', 'Jones']).symmetric_difference(Pythons(['Cleese', 'Jones']))
    Pythons(['Cleese', 'Palin'])

    >>> Pythons(['Gilliam']).issubset(Pythons(['Cleese', 'Palin']))
    False

    >>> Pythons(['Cleese', 'Palin']).issuperset(Pythons())
    True


Further reading
---------------

- http://wiki.python.org/moin/BitManipulation
- http://wiki.python.org/moin/BitArrays

- http://en.wikipedia.org/wiki/Bit_array
- http://en.wikipedia.org/wiki/Bit_manipulation

- http://en.wikipedia.org/wiki/Lexicographical_order
- http://en.wikipedia.org/wiki/Colexicographical_order


See also
--------

- bitarray_ |--| efficient boolean array implemented as C extension
- bitstring_ |--| pure-Python bit string based on ``bytearray``
- BitVector_ |--| pure-Python bit array based on unsigned short ``array``
- Bitsets_ |--| Cython interface to fast bitsets in Sage
- bitfield_ |--| Cython positive integer sets
- intbitset_ |--| integer bit sets as C extension 
- gmpy2_ |--| fast arbitrary precision integer arithmetic


License
-------

Bitsets is distributed under the `MIT license`_.

.. _pip: http://pip.readthedocs.org

.. _bitarray: http://pypi.python.org/pypi/bitarray
.. _bitstring: http://pypi.python.org/pypi/bitstring
.. _BitVector: http://pypi.python.org/pypi/BitVector
.. _Bitsets: http://www.sagemath.org/doc/reference/data_structures/sage/data_structures/bitset.html
.. _bitfield: http://pypi.python.org/pypi/bitfield
.. _intbitset: http://pypi.python.org/pypi/intbitset
.. _gmpy2: http://pypi.python.org/pypi/gmpy2

.. _MIT license: http://opensource.org/licenses/MIT


.. |--| unicode:: U+2013


.. |PyPI version| image:: https://pypip.in/v/bitsets/badge.svg
    :target: https://pypi.python.org/pypi/bitsets
    :alt: Latest PyPI Version
.. |License| image:: https://pypip.in/license/bitsets/badge.svg
    :target: https://pypi.python.org/pypi/bitsets
    :alt: License
.. |Supported Python| image:: https://pypip.in/py_versions/bitsets/badge.svg
    :target: https://pypi.python.org/pypi/bitsets
    :alt: Supported Python Versions
.. |Format| image:: https://pypip.in/format/bitsets/badge.svg
    :target: https://pypi.python.org/pypi/bitsets
    :alt: Format
.. |Downloads| image:: https://pypip.in/d/bitsets/badge.svg
    :target: https://pypi.python.org/pypi/bitsets
    :alt: Downloads
