#!/usr/bin/env python
# visualize-examples.py

import bitsets
import bitsets.visualize

DIRECTORY = 'visualize-output'
FORMAT = 'pdf'

Four = bitsets.bitset('Four', (1, 2, 3, 4))

bitsets.visualize.bitset(Four, directory=DIRECTORY, format=FORMAT, render=True)

bitsets.visualize.bitset(Four, member_label=True, directory=DIRECTORY, format=FORMAT, render=True)
