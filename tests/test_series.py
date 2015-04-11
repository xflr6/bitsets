# test_series.py

import unittest

from bitsets.bases import BitSet
from bitsets.series import List, Tuple


class TestSeries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.Nums = BitSet._make_subclass('Nums', (1, 2, 3, 4, 5, 6), listcls=List, tuplecls=Tuple)

    @classmethod
    def tearDownClass(cls):
        del cls.Nums

    def test_class(self):
        self.assertTrue(issubclass(self.Nums.List, list))
        self.assertTrue(issubclass(self.Nums.Tuple, tuple))

    def test_classrepr(self):
        self.assertRegexpMatches(repr(self.Nums.List),
            "<class bitsets\.meta\.bitset_list\('Nums', \(1, 2, 3, 4, 5, 6\), 0x[0-9a-fA-F]+, BitSet, List, Tuple\)>")
        self.assertRegexpMatches(repr(self.Nums.Tuple),
            "<class bitsets\.meta\.bitset_tuple\('Nums', \(1, 2, 3, 4, 5, 6\), 0x[0-9a-fA-F]+, BitSet, List, Tuple\)>")

    def test_frombitsets(self):
        self.assertEqual(self.Nums.List.frombitsets([]), self.Nums.List())
        self.assertEqual(self.Nums.Tuple.frombitsets([]), self.Nums.Tuple())

    def test_frommembers(self):
        self.assertEqual(self.Nums.List.frommembers([(1, 3), (1, 2)]),
            self.Nums.List('101000', '110000'))

    def test_frombools(self):
        self.assertEqual(self.Nums.List.frombools([(True, False, True), (True, True, False)]),
            self.Nums.List('101000', '110000'))

    def test_frombits(self):
        self.assertEqual(self.Nums.List.frombits(['101000', '110000']),
            self.Nums.List('101000', '110000'))

    def test_fromints(self):
        self.assertEqual(self.Nums.List.fromints([5, 3]),
            self.Nums.List('101000', '110000'))

    def test_members(self):
        self.assertEqual(self.Nums.List('101000', '110000').members(),
            [(1, 3), (1, 2)])

    def test_members_as_set(self):
        self.assertEqual(self.Nums.List('101000').members(as_set=True),
            [frozenset([1, 3])])

    def test_bools(self):
        self.assertEqual(self.Nums.List('101000', '110000').bools(),
            [(True, False, True, False, False, False),
             (True, True, False, False, False, False)])

    def test_bits(self):
        self.assertEqual(self.Nums.List('101000', '110000').bits(),
            ['101000', '110000'])

    def test_ints(self):
        self.assertEqual(self.Nums.List('101000', '110000').ints(), [5, 3])

    def test_repr(self):
        self.assertEqual(repr(self.Nums.List('101000','110000')),
            "NumsList('101000', '110000')")
        self.assertEqual(repr(self.Nums.Tuple('101000','110000')),
            "NumsTuple('101000', '110000')")

    def test_index_sets(self):
        self.assertEqual(self.Nums.List('101000', '110000').index_sets(),
            [(0, 2), (0, 1)])

    def test_reduce_and(self):
        self.assertEqual(self.Nums.List('101000', '110000').reduce_and(),
            self.Nums([1]))

    def test_reduce_or(self):
        self.assertEqual(self.Nums.List('101000', '110000').reduce_or(),
            self.Nums([1, 2, 3]))
