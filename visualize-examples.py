# visualize-examples.py

import bitsets
import bitsets.visualize

Four = bitsets.bitset('Four', (1, 2, 3, 4))

bitsets.visualize.bitset(Four, render=True)

bitsets.visualize.bitset(Four, member_label=True, render=True)
