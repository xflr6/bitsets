# meta.py - dynamic class creation and unpickle reconstructors

from itertools import izip
import copy_reg

__all__ = ['MemberBitsMeta', 'SeriesMeta']


class MemberBitsMeta(type):

    __registry = {}

    def subclass(self, name, members, list=None, tuple=None):
        created, cls = self._get_subclass(name, members, None, list, tuple)
        return cls

    def _get_subclass(self, name, members, id, listcls, tuplecls):
        if (name, members, id) in self.__registry:
            return False, self.__registry[(name, members, id)]
        elif id is not None:  # force create
            return True, self._make_subclass(name, members, id, listcls, tuplecls)

        # try first match
        matching = [cls for (cname, cmembers, cid), cls in self.__registry.iteritems()
            if cname == name and cmembers == members]
        if len(matching) == 1:
            return False, matching[0]
        elif matching:
            raise RuntimeError('Multiple classes matching %r' % matching)
        return True, self._make_subclass(name, members, id, listcls, tuplecls)

    def _make_subclass(self, name, members, id, listcls, tuplecls):
        if hasattr(self, '_members'):
            raise RuntimeError('%r attempt _make_subclass' % self)

        dct = {'__slots__': self.__slots__, '_members': members}
        if id:
            dct['_id'] = id
        cls = type(name, (self,), dct)
        if listcls is not None:
            setattr(cls, listcls._series, listcls._make_subclass(name, cls))
        if tuplecls is not None:
            setattr(cls, tuplecls._series, tuplecls._make_subclass(name, cls))
        return cls

    def __init__(self, name, bases, dct):
        if not hasattr(self, '_members'):
            return

        self._len = len(self._members)
        self._atoms = tuple(self.from_int(1 << i) for i in range(self._len))
        self._map = {i: s for i, s in izip(self._members, self._atoms)}
        self.infimum = self.from_int(0)
        self.supremum = self.from_int((1 << self._len) - 1)

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


class SeriesMeta(type):

    def _make_subclass(self, name, cls):
        if hasattr(self, 'BitSet'):
            raise RuntimeError('%r attempt _make_subclass' % self)

        assert self._series in ('List', 'Tuple')
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


copy_reg.pickle(MemberBitsMeta, MemberBitsMeta.__reduce__)
copy_reg.pickle(SeriesMeta, SeriesMeta.__reduce__)


def bitset(name, members, id, basecls, listcls, tuplecls):
    if not isinstance(id, (int, long)):
        raise RuntimeError

    created, cls = basecls._get_subclass(name, members, id, listcls, tuplecls)
    return cls


def bitset_list(name, members, id, basecls, listcls, tuplecls):
    return bitset(name, members, id, basecls, listcls, tuplecls).List


def bitset_tuple(name, members, id, basecls, listcls, tuplecls):
    return bitset(name, members, id, basecls, listcls, tuplecls).Tuple
