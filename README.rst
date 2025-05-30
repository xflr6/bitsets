Bitsets
=======

|PyPI version| |License| |Supported Python| |Wheel|

|Build| |Codecov| |Readthedocs-stable| |Readthedocs-latest|

This package provides a memory-efficient pure-python **immutable ordered set
data type** for working with large numbers of subsets from a predetermined pool
of objects.

Given a name and a tuple of hashable objects, the ``bitset()``-function returns
a custom integer subclass for creating ordered subsets from the object pool.
Each instance is a Python integer where the presence/absence of the *nth* pool
item is its *nth* bit being set/unset (a.k.a. bit strings, powers of two, rank
in *colexicographical* order).

Being just a regular (arbitrary precision) integer with some convenience
methods for translating between unique object collections and bit patterns
allows to perform certain tasks in a more natural way, e.g. sorting a
collection of sets lexicographically, or enumerating possible combinations in
an ordered fashion.


Links
-----

- GitHub: https://github.com/xflr6/bitsets
- PyPI: https://pypi.org/project/bitsets/
- Documentation: https://bitsets.readthedocs.io
- Changelog: https://bitsets.readthedocs.io/en/latest/changelog.html
- Issue Tracker: https://github.com/xflr6/bitsets/issues
- Download: https://pypi.org/project/bitsets/#files


Installation
------------

This package runs under Python 3.9+ and has no required dependencies,
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

- https://wiki.python.org/moin/BitManipulation
- https://wiki.python.org/moin/BitArrays

- https://en.wikipedia.org/wiki/Bit_array
- https://en.wikipedia.org/wiki/Bit_manipulation

- https://en.wikipedia.org/wiki/Lexicographical_order
- https://en.wikipedia.org/wiki/Colexicographical_order


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


.. _pip: https://pip.readthedocs.io

.. _bitarray: https://pypi.org/project/bitarray/
.. _bitstring: https://pypi.org/project/bitstring/
.. _BitVector: https://pypi.org/project/BitVector/
.. _Bitsets: https://www.sagemath.org/doc/reference/data_structures/sage/data_structures/bitset.html
.. _bitfield: https://pypi.org/project/bitfield/
.. _intbitset: https://pypi.org/project/intbitset/
.. _gmpy2: https://pypi.org/project/gmpy2/

.. _MIT license: https://opensource.org/licenses/MIT


.. |--| unicode:: U+2013


.. |PyPI version| image:: https://img.shields.io/pypi/v/bitsets.svg
    :target: https://pypi.org/project/bitsets/
    :alt: Latest PyPI Version
.. |License| image:: https://img.shields.io/pypi/l/bitsets.svg
    :target: https://github.com/xflr6/bitsets/blob/master/LICENSE.txt
    :alt: License
.. |Supported Python| image:: https://img.shields.io/pypi/pyversions/bitsets.svg
    :target: https://pypi.org/project/bitsets/
    :alt: Supported Python Versions
.. |Wheel| image:: https://img.shields.io/pypi/wheel/bitsets.svg
    :target: https://pypi.org/project/bitsets/#files
    :alt: Wheel format

.. |Build| image:: https://github.com/xflr6/bitsets/actions/workflows/build.yaml/badge.svg?branch=master
    :target: https://github.com/xflr6/bitsets/actions/workflows/build.yaml?query=branch%3Amaster
    :alt: Build
.. |Codecov| image:: https://codecov.io/gh/xflr6/bitsets/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/xflr6/bitsets
    :alt: Codecov
.. |Readthedocs-stable| image:: https://readthedocs.org/projects/bitsets/badge/?version=stable
    :target: https://bitsets.readthedocs.io/en/stable/?badge=stable
    :alt: Readthedocs stable
.. |Readthedocs-latest| image:: https://readthedocs.org/projects/bitsets/badge/?version=latest
    :target: https://bitsets.readthedocs.io/en/latest/?badge=latest
    :alt: Readthedocs latest
