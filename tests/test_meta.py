# test_meta.py

import unittest

import pickle

from bitsets.bases import MemberBits
from bitsets.series import Series, List, Tuple


class TestMeta(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.Ints = MemberBits._make_subclass('Ints', (1, 2, 3, 4, 5, 6))

    @classmethod
    def tearDownClass(cls):
        del cls.Ints

    def test_make_subclass_invalid(self):
        with self.assertRaisesRegexp(RuntimeError, 'make_subclass'):
            self.Ints._make_subclass('Ints', (1, 2, 3, 4, 5, 6),
                None, None, None)

    def test_repr(self):
        self.assertEqual(repr(MemberBits),
            "<class 'bitsets.bases.MemberBits'>")

    def test_get_subclass(self):
        with self.assertRaises(RuntimeError):
            MemberBits._get_subclass('Ints', (1, 2, 3, 4, 5, 6),
                None, None, None)
        self.assertIsInstance(
            MemberBits._get_subclass('Ints', (1, 2, 3, 4, 5, 6),
                -1, None, None),
            MemberBits.__class__)

    def test_atomic(self):
        self.assertEqual(list(self.Ints.atomic(self.Ints('100011'))),
            [self.Ints('100000'), self.Ints('000010'), self.Ints('000001')])

    def test_inatomic(self):
        self.assertEqual(list(self.Ints.inatomic(self.Ints('100011'))),
            [self.Ints('010000'), self.Ints('001000'), self.Ints('000100')])


class TestSeriesMeta(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.Nums = MemberBits._make_subclass('Nums', (1, 2, 3, 4, 5, 6),
            listcls=List, tuplecls=Tuple)

    @classmethod
    def tearDownClass(cls):
        del cls.Nums

    def test_make_subclass_invalid(self):
        with self.assertRaisesRegexp(RuntimeError, 'make_subclass'):
            self.Nums.List._make_subclass('NumsList', List)

    def test_repr(self):
        self.assertEqual(repr(Series),
            "<class 'bitsets.series.Series'>")

    def test_reconstruct(self):
        self.assertIs(pickle.loads(pickle.dumps(self.Nums.Tuple)),
            self.Nums.Tuple)
