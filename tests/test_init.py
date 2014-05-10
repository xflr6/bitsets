# test_init.py

import unittest

from bitsets import bitset


class TestBitset(unittest.TestCase):

    def test_init_empty_name(self):
        with self.assertRaisesRegexp(ValueError, 'empty'):
            bitset('', 'abc')

    def test_init_members_nosequence(self):
        with self.assertRaisesRegexp(ValueError, 'sequence'):
            bitset('Letters', set('abc'))

    def test_init_one_member(self):
        with self.assertRaisesRegexp(ValueError, 'two'):
            bitset('Letters', 'a')

    def test_init_wrong_base(self):
        with self.assertRaisesRegexp(ValueError, 'subclass'):
            bitset('Letters', 'abc', set)
