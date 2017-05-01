# meta.py - dynamic class creation and unpickle reconstructors

"""Dynamic bitset class creation and retrieval."""

from ._compat import integer_types, zip, filter, filterfalse, register_reduce

__all__ = ['MemberBitsMeta', 'SeriesMeta']


@register_reduce
class MemberBitsMeta(type):

    __registry = {}

    def _make_subclass(self, name, members, id=None, listcls=None, tuplecls=None):
        if hasattr(self, '_members'):
            raise RuntimeError('%r attempt _make_subclass' % self)

        dct = {'_members': members}
        if id:
            dct['_id'] = id

        cls = type(name, (self,), dct)

        self.__registry[(cls.__name__, cls._members, cls._id)] = cls

        for scls, attr in [(listcls, 'List'), (tuplecls, 'Tuple')]:
            if scls is not None:
                scls = scls._make_subclass(name, cls)
                assert scls._series == attr
                setattr(cls, scls._series, scls)

        return cls

    def __new__(cls, name, bases, dct):
        dct.setdefault('__slots__', ())
        return super(MemberBitsMeta, cls).__new__(cls, name, bases, dct)

    def __init__(self, name, bases, dct):
        if not hasattr(self, '_members'):
            return

        self._len = len(self._members)

        self._atoms = tuple(self.fromint(1 << i) for i in range(self._len))
        self._map = dict(zip(self._members, self._atoms))

        self.infimum = self.fromint(0)  # all zeros
        self.supremum = self.fromint((1 << self._len) - 1)  # all ones

        if not hasattr(self, '_id'):
            self._id = id(self)

    def __repr__(self):
        if not hasattr(self, '_members'):
            return super(MemberBitsMeta, self).__repr__()

        return '<class %s.bitset(%r, %r, %#x, %s, %s, %s)>' % (self.__module__,
            self.__name__, self._members, self._id, self.__base__.__name__,
            self.List.__base__.__name__ if hasattr(self, 'List') else None,
            self.Tuple.__base__.__name__ if hasattr(self, 'Tuple') else None)

    def __reduce__(self):
        if not hasattr(self, '_members'):
            return self.__name__

        return bitset, (self.__name__, self._members, self._id, self.__base__,
            self.List.__base__ if hasattr(self, 'List') else None,
            self.Tuple.__base__ if hasattr(self, 'Tuple') else None)

    def _get_subclass(self, name, members, id, listcls, tuplecls):
        """Return or create class with name, members, and id (for unpickling)."""
        if not isinstance(id, integer_types):
            raise RuntimeError

        if (name, members, id) in self.__registry:  # enable roundtrip reprs
            return self.__registry[(name, members, id)]

        return self._make_subclass(name, members, id, listcls, tuplecls)

    def atomic(self, bitset):
        """Member singleton generator."""
        return filter(bitset.__and__, self._atoms)

    def inatomic(self, bitset):
        """Complement singleton generator."""
        return filterfalse(bitset.__and__, self._atoms)

    def reduce_and(self, bitsets):
        """Generalized intersection."""
        inters = self.supremum.copy()
        for b in bitsets:
            inters &= b
        return self.frombitset(inters)

    def reduce_or(self, bitsets):
        """Generalized union."""
        union = self.infimum.copy()
        for b in bitsets:
            union |= b
        return self.frombitset(union)


@register_reduce
class SeriesMeta(type):

    def _make_subclass(self, name, cls):
        if hasattr(self, 'BitSet'):
            raise RuntimeError('%r attempt _make_subclass' % self)

        dct = {'BitSet': cls}
        if '__slots__' in self.__dict__:
            dct['__slots__'] = self.__slots__
        return type('%s%s' % (name, self.__name__), (self,), dct)

    def __repr__(self):
        if not hasattr(self, 'BitSet'):
            return type.__repr__(self)

        bs = self.BitSet
        return '<class %s.bitset_%s(%r, %r, %#x, %s, %s, %s)>' % (self.__module__,
            self._series.lower(), bs.__name__, bs._members, bs._id, bs.__base__.__name__,
            bs.List.__base__.__name__ if hasattr(bs, 'List') else None,
            bs.Tuple.__base__.__name__ if hasattr(bs, 'Tuple') else None)

    def __reduce__(self):
        if not hasattr(self, 'BitSet'):
            return self.__name__

        bitset_series = {'List': bitset_list, 'Tuple': bitset_tuple}[self._series]
        bs = self.BitSet
        return bitset_series, (bs.__name__, bs._members, bs._id, bs.__base__,
            bs.List.__base__ if hasattr(bs, 'List') else None,
            bs.Tuple.__base__ if hasattr(bs, 'Tuple') else None)


def bitset(name, members, id, basecls, listcls, tuplecls):
    return basecls._get_subclass(name, members, id, listcls, tuplecls)


def bitset_list(name, members, id, basecls, listcls, tuplecls):
    return bitset(name, members, id, basecls, listcls, tuplecls).List


def bitset_tuple(name, members, id, basecls, listcls, tuplecls):
    return bitset(name, members, id, basecls, listcls, tuplecls).Tuple
