# visualize.py

from itertools import imap
import operator

import graphviz

__all__ = ['bitset']

DIRECTORY = 'graphs'

MEMBER_LABELS = False

label_getters = {
    False: operator.methodcaller('bits'),
    True: lambda b: '{%s}' % ','.join(imap(str, b.members())),
    None: lambda b: '',
}


def bitset(bs, member_labels=MEMBER_LABELS, directory=DIRECTORY,
        save=False, compile=False, view=False):
    dot = graphviz.Digraph(comment=bs, key=bs.__name__, directory=directory,
        edge_attr={'dir':'none'})

    get_key = lambda b: 'b%d' % b

    get_label = label_getters[member_labels]
    
    for i in range(bs.supremum + 1):
        b = bs.from_int(i)
        key = get_key(b)
        dot.node(key, get_label(b))
        for a in bs._atoms:
            if not b & a:
                dot.edge(get_key(b | a), key)

    if save or compile or view:
        dot.save(compile=compile, view=view)
    return dot
