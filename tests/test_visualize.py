# test_visualize.py

import bitsets.visualize


def test_label_func(Four):
    get_label = lambda b: 'spam%sspam' % b.real
    dot = bitsets.visualize.bitset(Four, member_label=get_label)
    assert 'spam1spam' in str(dot)
