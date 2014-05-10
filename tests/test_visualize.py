# test_visualize.py

import unittest

import bitsets
import bitsets.visualize


class TestBitSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.Four = bitsets.bitset('Four', (1, 2, 3, 4))

    @classmethod
    def tearDownClass(cls):
        del cls.Four

    def test_label_func(self):
        get_label = lambda b: 'spam%sspam' % b.real
        dot = bitsets.visualize.bitset(self.Four, member_label=get_label)
        self.assertIn('spam1spam', str(dot))
