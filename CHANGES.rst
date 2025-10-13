Changelog
=========


Version 0.9.1 (in development)
------------------------------





Version 0.9
-----------

Switch to pyproject.toml. This changes the source distribution format from ``.zip``
to PEP 625 compliant ``.tar.gz`` (https://peps.python.org/pep-0625/).

Drop Python 3.7, 3.8, and 3.9 support and tag Python 3.11, 3.12, 3.13, and 3.14 support.


Version 0.8.4
-------------

Drop Python 3.6 support.


Version 0.8.3
-------------

Tag Python 3.10 support.


Version 0.8.2
-------------

Drop obsolete ``_compat.py`` (accidentally included in the last distribution).


Version 0.8.1
-------------

Drop ``bdist_wheel = universal`` to avoid ``py2`` in the wheel filename.


Version 0.8
-----------

Drop Python 2 support.

Drop Python 3.5 support and tag Python 3.9 support.

Add ``indexes_optimized`` for faster iteration over bitset members (PR: Johnnie
Gray).


Version 0.7.16
--------------

Tag Python 3.8 support.


Version 0.7.15
--------------

Drop Python 3.4 support.


Version 0.7.14
--------------

Tag Python 3.7 support, add simple tox config.


Version 0.7.13
--------------

Use compatible release version specifiers (bump optional ``graphviz`` to ~=0.7).


Version 0.7.12
--------------

Drop Python 3.3 support.

Include LICENSE.txt file in wheel.


Version 0.7.11
--------------

Port tests from nose/unittest to pytest, add Travis CI and coveralls.

Update meta data, tag Python 3.6 support.


Version 0.7.10
--------------

Use private ``_int`` attribute for internal unboxing purposes. 

Relax ``bitsets`` and ``graphivz`` dependencies to < 1.0.

Improved documentation.


Version 0.7.9
-------------

Raise an error if ``bitset`` members have duplicates.

Extended and improved documentation, added Sphinx-based API reference.

Improved unittests.


Version 0.7.8
-------------

Added ``integers.n()`` and ``integers.rank()``.

Make ``.iter_set()`` available on series as ``.index_sets()`` method.


Version 0.7.7
-------------

Made ``.indexes()`` available on bitsets as ``.iter_set()`` method.

Added ``transform`` module providing additional integer (un)packing tools.


Version 0.7.6
-------------

Added optional ``as_set`` parameter to ``.members()`` method returning a ``frozenset``.


Version 0.7.5
-------------

Added optional boolean value argument to ``.count()`` method.

Added ``integers.bit_mask()``.


Version 0.7.4
-------------

Support domains of just one element (minimum was two).


Version 0.7.3
-------------

Added ``integers.compress()``.

Added ``.copy()`` method (improve ``set`` compatibility).


Version 0.7.2
-------------

Support custom label function in visualization.


Version 0.7.1
-------------

Fixed ``.powerset()`` failing with start argument.

Fixed ``bool(bitset)`` never False under py3.


Version 0.7
-----------

Added Python 3.3+ support.

Fixed (un)pickling with protocol 2 and higher.

Added ``.fromints()`` and ``.ints()`` methods to collections.


Version 0.6.1
-------------

Made optional dependency mentioned in ``README.rst`` a version range.


Version 0.6
-----------

Added ``reverse`` argument to ``.atoms()`` and ``.inatoms()``, improved visualization edge order.

Changed series ``frombitsets`` argument to iterable argument instead of ``*args``, fixed bits method.

Improved doctests.


Version 0.5.1
-------------

Some cleanup.


Version 0.5
-----------

Added ``.atoms()`` and ``.inatoms()`` method.

Backwards incompatible: renamed ``from_spam`` methods to ``fromspam``.


Version 0.4
-----------

Add ``reduce_and``, ``reduce_or`` on series and as class-only methods on all bitsets.

Improved visualization using ``graphviz`` 0.2 with new api.


Version 0.3
-----------

Added visualization.


Version 0.2
-----------

Added ``.all()`` and ``.any()`` methods, improved ``__nonzero__``.

Improved documentation.


Version 0.1.4
-------------

Coerce ``other`` argument of ``frozenset``-compatible methods to bitset.


Version 0.1.3
-------------

Fixed empty bitset ``__contains__``  to raise ``KeyError`` with non-member.

Support constructor override by ``series.List`` subclass.

Package info and documentation refinements.


Version 0.1.2
-------------

Constructor always returns a new subclass (obsoleted ``cached`` argument).

Bitset instances can no more get instance dicts (enforce empty ``__slots__``).

Full set of construction and conversion methods for bitset sequences.

Remove sanity assertions from set methods.

Improve documentation.


Version 0.1.1
-------------

Fixed ``.from_members()`` with string arguments.


Version 0.1
-----------

First public release.
