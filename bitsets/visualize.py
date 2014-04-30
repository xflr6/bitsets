# visualize.py - create hasse diagrams

from ._compat import map

import graphviz

__all__ = ['bitset']

FILENAME = 'bs-%s-%s.gv'

MEMBER_LABEL = False

NAME_GETTERS = [lambda b: 'b%d' % b, lambda b: b.bits()]

LABEL_GETTERS = {
    None: lambda b: '',
    False: lambda b: b.bits(),
    True: lambda b: '{%s}' % ','.join(map(str, b.members())),
}


def bitset(bs, member_label=None, filename=None, directory=None, format=None,
           render=False, view=False):
    """Graphviz source for the Hasse diagram of the domains' Boolean algebra."""
    if member_label is None:
        member_label = MEMBER_LABEL

    if filename is None:
        kind = 'members' if member_label else 'bits'
        filename = FILENAME % (bs.__name__, kind)

    dot = graphviz.Digraph(
        name=bs.__name__,
        comment=repr(bs),
        filename=filename,
        directory=directory,
        format=format,
        edge_attr=dict(dir='none')
    )

    node_name = NAME_GETTERS[0]
    node_label = LABEL_GETTERS[member_label]

    for i in range(bs.supremum + 1):
        b = bs.fromint(i)
        name = node_name(b)
        dot.node(name, node_label(b))
        dot.edges((name, node_name(b & ~a)) for a in b.atoms(reverse=True))

    if render or view:
        dot.render(view=view)  # pragma: no cover
    return dot
