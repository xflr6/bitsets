# test_bitsets.py

import unittest

from bitsets import bitset


class TestBitsets(unittest.TestCase):

    def test_init_empty_name(self):
        with self.assertRaises(ValueError):
            bitset('', 'abc')

    def test_init_members_nosequence(self):
        with self.assertRaises(ValueError):
            bitset('Letters', set('abc'))

    def test_init_one_member(self):
        with self.assertRaises(ValueError):
            bitset('Letters', 'a')

    def test_init_wrong_base(self):
        with self.assertRaises(ValueError):
            bitset('Letters', 'abc', set)
