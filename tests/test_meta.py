# test_meta.py

import pickle

import pytest

import bitsets.series
from bitsets.bases import MemberBits


def test_memberbits_make_subclass_invalid(Ints):
    with pytest.raises(RuntimeError, match=r'make_subclass'):
        Ints._make_subclass('Ints', (1, 2, 3, 4, 5, 6), None, None, None)


def test_repr_ints_cls(Ints):
    assert repr(MemberBits) == "<class 'bitsets.bases.MemberBits'>"


def test_get_subclass_invalid_id(Ints):
    with pytest.raises(RuntimeError, match=r'non-integer id'):
        MemberBits._get_subclass('Ints', (1, 2, 3, 4, 5, 6), None, None, None)


def test_get_subclass(Ints):
    assert isinstance(
        MemberBits._get_subclass('Ints', (1, 2, 3, 4, 5, 6), -1, None, None),
        MemberBits.__class__)


@pytest.mark.parametrize('bits, expected', [
    ('000000', []),
    ('100011', ['100000', '000010', '000001']),
])
def test_atomic(Ints, bits, expected):
    assert list(Ints.atomic(Ints(bits))) == [Ints(e) for e in expected]


@pytest.mark.parametrize('bits, expected', [
    ('111111', []),
    ('100011', ['010000', '001000', '000100']),
])
def test_inatomic(Ints, bits, expected):
    assert list(Ints.inatomic(Ints(bits))) == [Ints(e) for e in expected]


@pytest.mark.parametrize('bits, expected', [
    ([], '111111'),
    (['111111', '111111',], '111111'),
    (['110011', '011110', '010010'], '010010'),
    (['100000', '001100', '000001'], '000000'),
])
def test_reduce_and(Ints, bits, expected):
    assert Ints.reduce_and(Ints(b) for b in bits) == Ints(expected)


@pytest.mark.parametrize('bits, expected', [
    ([], '000000'),
    (['111000', '000111'], '111111'),
    (['100001', '010010', '110011'], '110011'),
    (['100000', '001100', '000001'], '101101'),
])
def test_reduce_or(Ints, bits, expected):
    assert Ints.reduce_or(Ints(b) for b in bits) == Ints(expected)


def test_series_make_subclass_invalid(Nums):
    with pytest.raises(RuntimeError, match=r'make_subclass'):
        Nums.List._make_subclass('NumsList', Nums.List)


def test_repr_nums_cls(Nums):
    assert repr(bitsets.series.Series) == "<class 'bitsets.series.Series'>"


def test_reconstruct(Nums):
    assert pickle.loads(pickle.dumps(Nums.Tuple)) is Nums.Tuple
