# visualize-examples.py

import bitsets
import bitsets.visualize

four = bitsets.bitset('four', (1, 2, 3, 4))

bitsets.visualize.bitset(four, render=True)

bitsets.visualize.bitset(four, member_label=True, render=True)
