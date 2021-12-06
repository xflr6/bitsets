"""Create hasse diagrams."""

import graphviz

__all__ = ['bitset']

FILENAME = 'bs-{name}-{kind}.gv'

MEMBER_LABEL = False

NAME_GETTERS = [lambda b: f'b{b:d}', lambda b: b.bits()]

LABEL_GETTERS = {None: lambda b: '',
                 False: lambda b: b.bits(),
                 True: lambda b: '{{{}}}'.format(','.join(map(str, b.members()))),
                 'iching': lambda b: chr(HEXAGRAMS[b])}

HEXAGRAMS = [0x4dc1, 0x4dd6, 0x4dc7, 0x4dd3, 0x4dcf, 0x4de2, 0x4dec, 0x4dcb,
             0x4dce, 0x4df3, 0x4de6, 0x4df4, 0x4dfd, 0x4df7, 0x4dde, 0x4de0,
             0x4dc6, 0x4dc3, 0x4ddc, 0x4dfa, 0x4de7, 0x4dff, 0x4dee, 0x4dc5,
             0x4ded, 0x4dd1, 0x4def, 0x4df8, 0x4ddf, 0x4df1, 0x4ddb, 0x4deb,
             0x4dd7, 0x4dda, 0x4dc2, 0x4de9, 0x4df2, 0x4dd4, 0x4dd0, 0x4dd8,
             0x4de3, 0x4dd5, 0x4dfe, 0x4de4, 0x4df6, 0x4ddd, 0x4df0, 0x4dcc,
             0x4dd2, 0x4de8, 0x4dfb, 0x4dfc, 0x4df5, 0x4de5, 0x4df9, 0x4dc9,
             0x4dca, 0x4dd9, 0x4dc4, 0x4dc8, 0x4de1, 0x4dcd, 0x4dea, 0x4dc0]


def bitset(bs, member_label=None, filename=None, directory=None, format=None,
           render=False, view=False):
    """Graphviz source for the Hasse diagram of the domains' Boolean algebra."""
    if member_label is None:
        member_label = MEMBER_LABEL

    if filename is None:
        kind = 'members' if member_label else 'bits'
        filename = FILENAME.format(name=bs.__name__, kind=kind)

    dot = graphviz.Digraph(name=bs.__name__, comment=repr(bs),
                           filename=filename, directory=directory,
                           format=format, edge_attr={'dir': 'none'})

    node_name = NAME_GETTERS[0]

    if callable(member_label):
        node_label = member_label
    else:
        node_label = LABEL_GETTERS[member_label]

    for i in range(bs.supremum + 1):
        b = bs.fromint(i)
        name = node_name(b)
        dot.node(name, node_label(b))
        dot.edges((name, node_name(b & ~a)) for a in b.atoms(reverse=True))

    if render or view:
        dot.render(view=view)  # pragma: no cover
    return dot
