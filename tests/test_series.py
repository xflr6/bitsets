# test_series.py

import re


def test_class(Nums):
    assert issubclass(Nums.List, list)
    assert issubclass(Nums.Tuple, tuple)


def test_classrepr(Nums):
    assert re.match(r"<class bitsets\.meta\.bitset_list\("
                    r"'Nums', \(1, 2, 3, 4, 5, 6\), "
                    r"0x[0-9a-fA-F]+, BitSet, List, Tuple"
                    r"\)>", repr(Nums.List))
    assert re.match(r"<class bitsets\.meta\.bitset_tuple\("
                    r"'Nums', \(1, 2, 3, 4, 5, 6\), "
                    r"0x[0-9a-fA-F]+, BitSet, List, Tuple"
                    r"\)>", repr(Nums.Tuple))


def test_frombitsets(Nums):
    assert Nums.List.frombitsets([]) == Nums.List()
    assert Nums.Tuple.frombitsets([]) == Nums.Tuple()


def test_frommembers(Nums):
    assert Nums.List.frommembers([(1, 3), (1, 2)]) == Nums.List('101000', '110000')


def test_frombools(Nums):
    assert Nums.List.frombools([(True, False, True), (True, True, False)]) == \
           Nums.List('101000', '110000')


def test_frombits(Nums):
    assert Nums.List.frombits(['101000', '110000']) == Nums.List('101000', '110000')


def test_fromints(Nums):
    assert Nums.List.fromints([5, 3]) == Nums.List('101000', '110000')


def test_members(Nums):
    assert Nums.List('101000', '110000').members() == [(1, 3), (1, 2)]


def test_members_as_set(Nums):
    assert Nums.List('101000').members(as_set=True) == [frozenset([1, 3])]


def test_bools(Nums):
    assert Nums.List('101000', '110000').bools() == \
           [(True, False, True, False, False, False),
            (True, True, False, False, False, False)]


def test_bits(Nums):
    assert Nums.List('101000', '110000').bits() == ['101000', '110000']


def test_ints(Nums):
    assert Nums.List('101000', '110000').ints() == [5, 3]


def test_repr(Nums):
    assert repr(Nums.List('101000', '110000')) == "NumsList('101000', '110000')"
    assert repr(Nums.Tuple('101000', '110000')) == "NumsTuple('101000', '110000')"


def test_index_sets(Nums):
    assert Nums.List('101000', '110000').index_sets() == [(0, 2), (0, 1)]


def test_reduce_and(Nums):
    assert Nums.List('101000', '110000').reduce_and() == Nums([1])


def test_reduce_or(Nums):
    assert Nums.List('101000', '110000').reduce_or() == Nums([1, 2, 3])
