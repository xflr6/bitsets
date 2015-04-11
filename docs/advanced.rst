.. _advanced:

Advanced Usage
==============


Visualization
-------------

With the help of the optional Graphviz_ graph layout library and this `Python
interface`__, the ``bitsets.visualize`` module can create **Hasse diagrams** of
all bitsets from your domain:

.. __: http://pypi.python.org/pypi/graphviz

Download and install Graphviz_. Then install the Python interface:

.. code:: bash

    $ pip install "graphviz>=0.3, <0.5"

Make sure that the ``bin`` directory of Graphviz is on your system path.

.. code:: python

    >>> from bitsets import visualize
    >>> Four = bitset('Four', (1, 2, 3, 4))

    >>> dot = visualize.bitset(Four)

    >>> print(dot.source)  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    // <class bitsets.meta.bitset('Four', (1, 2, 3, 4), 0x..., BitSet, None, None)>
    digraph Four {
    	edge [dir=none]
    		b0 [label=0000]
    		b1 [label=1000]
    			b1 -> b0
    		b2 [label=0100]
    			b2 -> b0
    		b3 [label=1100]
    			b3 -> b1
    			b3 -> b2
    ...

.. image:: hasse-bits.png
    :align: center


Show members instead of bits:

.. code:: python

    >>> dot = visualize.bitset(Four, member_label=True)

    >>> print(dot.source)  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    // <class bitsets.meta.bitset('Four', (1, 2, 3, 4), 0x..., BitSet, None, None)>
    digraph Four {
    	edge [dir=none]
    		b0 [label="{}"]
    		b1 [label="{1}"]
    			b1 -> b0
    		b2 [label="{2}"]
    			b2 -> b0
    		b3 [label="{1,2}"]
    			b3 -> b1
    			b3 -> b2
    ...

.. image:: hasse-members.png
    :align: center

Remember that the graphs have ``2 ** domain_size`` nodes.


Containers
----------

When activated, each bitset class comes with tailored **collection classes**
(bitset list and bitset tuple) for its instances.

.. code:: python

    >>> Letters = bitset('Letters', 'abcdef', list=True)

    >>> Letters.List.frommembers(['a', 'bcd', 'ef'])
    LettersList('100000', '011100', '000011')

The collection classes have convenience methods for set **intersection** and
**union**:

.. code:: python

    >>> import string

    >>> Ascii = bitset('Ascii', string.ascii_lowercase, list=True)
    >>> ascii = Ascii.List.frommembers(['spam', 'eggspam', 'ham'])

    >>> ascii.reduce_and()
    Ascii(['a', 'm'])

    >>> ascii.reduce_or()
    Ascii(['a', 'e', 'g', 'h', 'm', 'p', 's'])


Customization
-------------

To use a **customized bitset class**, extend one of the classes from the
``bitsets.bases`` module and pass it to the ``bitset`` function.

.. code:: python

    >>> import bitsets

    >>> class ProperSet(bitsets.bases.BitSet):
    ...     def issubset_proper(self, other):
    ...         return self & other == self != other

    >>> Ints = bitset('Ints', (1, 2, 3, 4, 5, 6), base=ProperSet)

    >>> issubclass(Ints, ProperSet)
    True

    >>> Ints([1]).issubset_proper(Ints([1, 2]))
    True

    >>> Ints([1, 2]).issubset_proper(Ints([1, 2]))
    False



To use a **customized bitset collection class**, extend one of the classes from
the ``bitsets.series`` module and pass it to the ``bitset`` function.

.. code:: python

    >>> from functools import reduce
    >>> import operator

    >>> class ReduceList(bitsets.series.List):
    ...     def intersection(self):
    ...         return self.BitSet.fromint(reduce(operator.and_, self))
    ...     def union(self):
    ...         return self.BitSet.fromint(reduce(operator.or_, self))

    >>> Nums = bitset('Nums', (1, 2, 3), list=ReduceList)

    >>> issubclass(Nums.List, ReduceList)
    True

    >>> numslist = Nums.List.frommembers([(1, 2, 3), (1, 2), (2, 3)])

    >>> numslist.intersection()
    Nums([2])

    >>> numslist.union()
    Nums([1, 2, 3])

Note that since version 0.4, this very functionality was added to the
``bitsets.series`` classes as ``reduce_and`` and ``reduce_or`` methods (see
above).


Persistence
-----------

Bitset classes, collection classes and their instances are **pickleable**:

.. code:: python

    >>> import pickle

    >>> pickle.loads(pickle.dumps(Pythons)) is Pythons
    True

    >>> pickle.loads(pickle.dumps(Pythons()))
    Pythons()

    >>> pickle.loads(pickle.dumps(Pythons(), protocol=pickle.HIGHEST_PROTOCOL))
    Pythons()

    >>> pickle.loads(pickle.dumps(Letters.List)) is Letters.List
    True

    >>> pickle.loads(pickle.dumps(Letters.List()))
    LettersList()

As long as customized bitset collection classes are defined at the top-level of
an importable module, the class and its instances are pickleable.

.. code:: python

    >>> pickle.loads(pickle.dumps(Nums.List)) is Nums.List  # doctest: +SKIP
    True

    >>> pickle.loads(pickle.dumps(Nums.List()))  # doctest: +SKIP
    NumsList()


.. _Graphviz: http://www.graphviz.org
