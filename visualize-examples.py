#!/usr/bin/env python
# visualize-examples.py

import bitsets
import bitsets.visualize

DIRECTORY = 'visualize-output'


Four = bitsets.bitset('Four', (1, 2, 3, 4))

bitsets.visualize.bitset(Four, render=True, directory=DIRECTORY)

bitsets.visualize.bitset(Four, member_label=True, render=True, directory=DIRECTORY)
