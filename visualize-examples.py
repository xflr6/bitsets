#!/usr/bin/env python
# visualize-examples.py

import bitsets
import bitsets.visualize

ARGS = {'directory': 'visualize-output', 'format': 'pdf'}

Four = bitsets.bitset('Four', (1, 2, 3, 4))

bitsets.visualize.bitset(Four, render=True, **ARGS)

bitsets.visualize.bitset(Four, member_label=True, render=True, **ARGS)

Six = bitsets.bitset('Six', (1, 2, 3, 4, 5, 6))

dot = bitsets.visualize.bitset(Six, member_label='iching', **ARGS)
dot.graph_attr.update(ranksep='1.2', splines='false')
dot.node_attr.update(shape='none', fontname='DejaVu Sans', fontsize='24')
dot.render()
