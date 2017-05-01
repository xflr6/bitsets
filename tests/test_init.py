# test_init.py

import pytest

from bitsets import bitset


def test_empty_name():
    with pytest.raises(ValueError) as e:
        bitset('', 'abc')
    e.match(r'empty')


def test_members_nonsequence():
    with pytest.raises(ValueError) as e:
        bitset('Letters', frozenset('abc'))
    e.match(r'sequence')


def test_no_member():
    with pytest.raises(ValueError) as e:
        bitset('Letters', '')
    e.match(r'one')


def test_duplicated_member():
    with pytest.raises(ValueError) as e:
        bitset('Letters', 'abca')
    e.match(r'duplicates')


def test_unhashable_members():
    with pytest.raises(TypeError) as e:
        bitset('Letters', list('abc'))
    e.match(r'unhashable')


def test_unhashable_member():
    with pytest.raises(TypeError) as e:
        bitset('Letters', ([], None))
    e.match(r'unhashable')


def test_wrong_base():
    with pytest.raises(ValueError) as e:
        bitset('Letters', 'abc', set)
    e.match(r'subclass')


def test_one_member():
    letter = bitset('Letter', 'a')
    assert letter('a').real == 1
    assert letter('').real == 0
