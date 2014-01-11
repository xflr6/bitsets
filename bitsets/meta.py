# meta.py - dynamic class creation and unpickle reconstructors

"""Dynamic bitset class creation and retrieval."""

from itertools import izip
import copy_reg

__all__ = ['MemberBitsMeta', 'SeriesMeta']


class MemberBitsMeta(type):

    __registry = {}

    def subclass(self, name, members, listcls=None, tuplecls=None):
        """Return first class with name and members or create (for doctests)."""
        matching = [cls for (cname, cmembers, cid), cls
            in self.__registry.iteritems()
            if cname == name and cmembers == members]

        if len(matching) == 1:
            return matching[0]
        elif matching:
            raise RuntimeError('Multiple classes matching %r' % matching)
        return self._make_subclass(name, members, None, listcls, tuplecls)

    def _get_subclass(self, name, members, id, listcls, tuplecls):
        """Return or create class with name, members, and id (for unpickling)."""
        if not isinstance(id, (int, long)):
            raise RuntimeError

        if (name, members, id) in self.__registry:
            # this enables roundtrip reprs
            return self.__registry[(name, members, id)]
        return self._make_subclass(name, members, id, listcls, tuplecls)

    def _make_subclass(self, name, members, id=None, listcls=None, tuplecls=None):
        if hasattr(self, '_members'):
            raise RuntimeError('%r attempt _make_subclass' % self)

        dct = {'_members': members}
        if id:
            dct['_id'] = id
        cls = type(name, (self,), dct)
        if listcls is not None:
            assert listcls._series == 'List'
            setattr(cls, listcls._series, listcls._make_subclass(name, cls))
        if tuplecls is not None:
            assert tuplecls._series == 'Tuple'
            setattr(cls, tuplecls._series, tuplecls._make_subclass(name, cls))
        return cls

    def __new__(self, name, bases, dct):
        dct['__slots__'] = ()
        return super(MemberBitsMeta, self).__new__(self, name, bases, dct)

    def __init__(self, name, bases, dct):
        if not hasattr(self, '_members'):
            return

        self._len = len(self._members)
        self._atoms = tuple(self.from_int(1 << i) for i in range(self._len))
        self._map = {i: s for i, s in izip(self._members, self._atoms)}

        self.infimum = self.from_int(0)  # all zeros
        self.supremum = self.from_int((1 << self._len) - 1)  # all ones

        if not hasattr(self, '_id'):
            self._id = id(self)

        self.__registry[(name, self._members, self._id)] = self

    def __repr__(self):
        if not hasattr(self, '_members'):
            return type.__repr__(self)

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


copy_reg.pickle(MemberBitsMeta, MemberBitsMeta.__reduce__)


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

        bs=self.BitSet
        return '<class %s.bitset_%s(%r, %r, %#x, %s, %s, %s)>' % (self.__module__,
            self._series.lower(), bs.__name__, bs._members, bs._id, bs.__base__.__name__,
            bs.List.__base__.__name__ if hasattr(bs, 'List') else None,
            bs.Tuple.__base__.__name__ if hasattr(bs, 'Tuple') else None)

    def __reduce__(self):
        if not hasattr(self, 'BitSet'):
            return self.__name__

        bitset_series = {'List': bitset_list, 'Tuple': bitset_tuple}[self._series]
        bs=self.BitSet
        return bitset_series, (bs.__name__, bs._members, bs._id, bs.__base__,
            bs.List.__base__ if hasattr(bs, 'List') else None,
            bs.Tuple.__base__ if hasattr(bs, 'Tuple') else None)


copy_reg.pickle(SeriesMeta, SeriesMeta.__reduce__)


def bitset(name, members, id, basecls, listcls, tuplecls):
    return basecls._get_subclass(name, members, id, listcls, tuplecls)


def bitset_list(name, members, id, basecls, listcls, tuplecls):
    return bitset(name, members, id, basecls, listcls, tuplecls).List


def bitset_tuple(name, members, id, basecls, listcls, tuplecls):
    return bitset(name, members, id, basecls, listcls, tuplecls).Tuple
