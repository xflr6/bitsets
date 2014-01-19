# visualize.py

from itertools import imap

import graphviz

__all__ = ['bitset']

MEMBER_LABEL = False


name_getters = [lambda b: 'b%d' % b, lambda b: b.bits()]

label_getters = {
    False: lambda b: b.bits(),
    True: lambda b: '{%s}' % ','.join(imap(str, b.members())),
    None: lambda b: '',
}


def bitset(bs, member_label=None, filename=None, directory=None, render=False, view=False):
    if member_label is None:
        member_label = MEMBER_LABEL

    if filename is None:
        filename = 'bs-%s-%s.gv' % (bs.__name__, 'members' if member_label else 'bits')

    dot = graphviz.Digraph(
        name=bs.__name__,
        comment=repr(bs),
        filename=filename,
        directory=directory,
        edge_attr=dict(dir='none')
    )

    node_name =name_getters[0] 

    node_label = label_getters[member_label]

    for i in range(bs.supremum + 1):
        b = bs.from_int(i)
        name = node_name(b)
        dot.node(name, node_label(b))
        dot.edges((node_name(b | a), name) for a in bs._atoms if not b & a)

    if render or view:
        dot.render(view=view)
    return dot
