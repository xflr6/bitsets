# test_visualize.py

import bitsets.visualize


def test_label_func(Four):
    dot = bitsets.visualize.bitset(Four,
                                   member_label=lambda b: 'spam%sspam' % b.real)
    assert 'spam1spam' in str(dot)
