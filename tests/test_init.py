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

    def test_init_no_member(self):
        with self.assertRaisesRegexp(ValueError, 'one'):
            bitset('Letters', '')

    def test_init_wrong_base(self):
        with self.assertRaisesRegexp(ValueError, 'subclass'):
            bitset('Letters', 'abc', set)

    def test_init_one_member(self):
        letter = bitset('Letter', 'a')
        self.assertEqual(letter('a').real, 1)
        self.assertEqual(letter('').real, 0)
