# test_meta.py

import pickle

import pytest

import bitsets.series
from bitsets.bases import MemberBits


def test_memberbits_make_subclass_invalid(Ints):
    with pytest.raises(RuntimeError) as e:
        Ints._make_subclass('Ints', (1, 2, 3, 4, 5, 6),
            None, None, None)
    e.match(r'make_subclass')


def test_repr_ints_cls(Ints):
    assert repr(MemberBits) == "<class 'bitsets.bases.MemberBits'>"


def test_get_subclass(Ints):
    with pytest.raises(RuntimeError):
        MemberBits._get_subclass('Ints', (1, 2, 3, 4, 5, 6),
            None, None, None)
    assert isinstance(
        MemberBits._get_subclass('Ints', (1, 2, 3, 4, 5, 6),
            -1, None, None),
        MemberBits.__class__)


def test_atomic(Ints):
    assert list(Ints.atomic(Ints('100011'))) == \
           [Ints('100000'), Ints('000010'), Ints('000001')]


def test_inatomic(Ints):
    assert list(Ints.inatomic(Ints('100011'))) == \
           [Ints('010000'), Ints('001000'), Ints('000100')]


def test_reduce_and(Ints):
    assert Ints.reduce_and([]) == Ints('111111')
    assert Ints.reduce_and([Ints('110011'), Ints('011110'), Ints('010010')]) == \
           Ints('010010')
    assert Ints.reduce_and([]) == Ints('111111')


def test_reduce_or(Ints):
    assert Ints.reduce_or([]) == Ints('000000')
    assert Ints.reduce_or([Ints('100001'), Ints('010010'), Ints('110011')]) == \
           Ints('110011')
    assert Ints.reduce_or([]) == Ints('000000')


def test_series_make_subclass_invalid(Nums):
    with pytest.raises(RuntimeError) as e:
        Nums.List._make_subclass('NumsList', Nums.List)
    e.match(r'make_subclass')


def test_repr_nums_cls(Nums):
    assert repr(bitsets.series.Series) == "<class 'bitsets.series.Series'>"


def test_reconstruct(Nums):
    assert pickle.loads(pickle.dumps(Nums.Tuple)) is Nums.Tuple
