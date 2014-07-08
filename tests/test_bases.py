# test_bases.py

import unittest

from bitsets.bases import MemberBits, BitSet


class TestMemberBits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.Ints = MemberBits._make_subclass('Ints', (1, 2, 3, 4, 5, 6))

    @classmethod
    def tearDownClass(cls):
        del cls.Ints

    def test_frombits_invalid(self):
        with self.assertRaisesRegexp(ValueError, 'too many bits'):
            self.Ints.frombits('1000001')

    def test_copy(self):
        bs = self.Ints('100011')
        self.assertIs(bs.copy(), bs)
        changed = bs
        changed |= self.Ints('011100')
        self.assertEqual(changed, self.Ints('111111'))
        self.assertEqual(bs, self.Ints('100011'))

    def test_inatoms_reverse(self):
        self.assertEqual(list(self.Ints('100011').inatoms(reverse=True)),
            [self.Ints('000100'), self.Ints('001000'), self.Ints('010000')])

    def test_powerset_invalid_start(self):
        with self.assertRaisesRegexp(ValueError, 'no subset'):
            self.Ints('1').powerset(self.Ints('111'))

    def test_powerset_with_start(self):
        result = self.Ints('111').powerset(self.Ints('1'))
        self.assertEqual(list(result),
            [self.Ints('1'), self.Ints('11'), self.Ints('101'),
             self.Ints('111')])

    def test_count_invalid(self):
        with self.assertRaises(ValueError):
            self.Ints('110011').count('0')
        with self.assertRaises(ValueError):
            self.Ints('110011').count('1')
        with self.assertRaises(ValueError):
            self.Ints('110011').count(2)


class TestBitSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.Nums = BitSet._make_subclass('Nums', (1, 2, 3, 4, 5, 6))

    @classmethod
    def tearDownClass(cls):
        del cls.Nums

    def test_bool(self):
        self.assertTrue(self.Nums([1]))
        self.assertFalse(self.Nums())

    def test_len(self):
        self.assertEqual(len(self.Nums([1])), 1)
        self.assertEqual(len(self.Nums()), 0)

    def test_issubset(self):
        self.assertTrue(self.Nums([1]).issubset(self.Nums([1, 2])))
        self.assertFalse(self.Nums([1]).issubset(self.Nums()))

    def test_issubset_members(self):
        self.assertTrue(self.Nums([1]).issubset([1, 2]))
        self.assertFalse(self.Nums([1]).issubset([]))

    def test_issuperset(self):
        self.assertTrue(self.Nums([1, 2]).issuperset(self.Nums([1])))
        self.assertFalse(self.Nums().issuperset(self.Nums([1])))

    def test_issuperset_members(self):
        self.assertTrue(self.Nums([1, 2]).issuperset([1]))
        self.assertFalse(self.Nums().issuperset([1]))

    def test_isdisjoint(self):
        self.assertTrue(self.Nums([1, 2]).isdisjoint(self.Nums([3, 4])))
        self.assertFalse(self.Nums([1, 2]).isdisjoint(self.Nums([2, 3])))

    def test_isdisjoint_members(self):
        self.assertTrue(self.Nums([1, 2]).isdisjoint([3, 4]))
        self.assertFalse(self.Nums([1, 2]).isdisjoint([2, 3]))

    def test_intersection(self):
        self.assertEqual(self.Nums([1, 2]).intersection(self.Nums([2, 3])),
            self.Nums([2]))

    def test_intersection_members(self):
        self.assertEqual(self.Nums([1, 2]).intersection([2, 3]),
            self.Nums([2]))

    def test_union(self):
        self.assertEqual(self.Nums([1, 2]).union(self.Nums([2, 3])),
            self.Nums([1, 2, 3]))

    def test_union_members(self):
        self.assertEqual(self.Nums([1, 2]).union([2, 3]),
            self.Nums([1, 2, 3]))

    def test_difference(self):
        self.assertEqual(self.Nums([1, 2]).difference(self.Nums([2, 3])),
            self.Nums([1]))

    def test_difference_members(self):
        self.assertEqual(self.Nums([1, 2]).difference([2, 3]),
            self.Nums([1]))

    def test_symmetric_difference(self):
        self.assertEqual(self.Nums([1, 2]).symmetric_difference(self.Nums([2, 3])),
            self.Nums([1, 3]))

    def test_symmetric_difference_members(self):
        self.assertEqual(self.Nums([1, 2]).symmetric_difference([2, 3]),
            self.Nums([1, 3]))
