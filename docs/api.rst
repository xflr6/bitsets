.. _api:

API Reference
=============

.. autosummary::
    :nosignatures:

    ~bitsets.bitset
    bitsets.bases.BitSet
    bitsets.series.List
    bitsets.series.Tuple


bitset
------

.. autofunction:: bitsets.bitset


BitSet
------

.. autoclass:: bitsets.bases.BitSet
    :members:
        copy,
        frombools, frombits,
        members, bools, bits,
        atoms, inatoms,
        powerset,
        shortlex, longlex, shortcolex, longcolex,
        count, all, any,
        __len__, __iter__, __contains__,
        issubset, issuperset, isdisjoint,
        intersection, union, difference, symmetric_difference,
        complement


BitSet.List
-----------

.. autoclass:: bitsets.series.List
    :members:
        frommembers, frombools, frombits, fromints,
        members, bools, bits, ints,
        index_sets,
        reduce_and, reduce_or


BitSet.Tuple
------------

.. autoclass:: bitsets.series.Tuple
    :members:
        frommembers, frombools, frombits, fromints,
        members, bools, bits, ints,
        index_sets,
        reduce_and, reduce_or
