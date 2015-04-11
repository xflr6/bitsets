# test_init.py

import unittest

from bitsets import bitset


class TestBitset(unittest.TestCase):

    def test_empty_name(self):
        with self.assertRaisesRegexp(ValueError, 'empty'):
            bitset('', 'abc')

    def test_members_nonsequence(self):
        with self.assertRaisesRegexp(ValueError, 'sequence'):
            bitset('Letters', frozenset('abc'))

    def test_no_member(self):
        with self.assertRaisesRegexp(ValueError, 'one'):
            bitset('Letters', '')

    def test_duplicated_member(self):
        with self.assertRaisesRegexp(ValueError, 'duplicates'):
            bitset('Letters', 'abca')

    def test_unhashable_members(self):
        with self.assertRaisesRegexp(TypeError, 'unhashable'):
            bitset('Letters', list('abc'))

    def test_unhashable_member(self):
        with self.assertRaisesRegexp(TypeError, 'unhashable'):
            bitset('Letters', ([], None))

    def test_wrong_base(self):
        with self.assertRaisesRegexp(ValueError, 'subclass'):
            bitset('Letters', 'abc', set)

    def test_one_member(self):
        letter = bitset('Letter', 'a')
        self.assertEqual(letter('a').real, 1)
        self.assertEqual(letter('').real, 0)
