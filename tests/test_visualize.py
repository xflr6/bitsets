# test_visualize.py

import bitsets.visualize


def test_label_func(Four):  # noqa: N803
    dot = bitsets.visualize.bitset(Four,
                                   member_label=lambda b: f'spam{b.real}spam')
    assert 'spam1spam' in str(dot)
