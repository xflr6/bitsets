# test_init.py

import pytest

from bitsets import bitset


def test_empty_name():
    with pytest.raises(ValueError, match=r'empty'):
        bitset('', 'abc')


def test_members_nonsequence():
    with pytest.raises(ValueError, match=r'sequence'):
        bitset('Letters', frozenset('abc'))


def test_no_member():
    with pytest.raises(ValueError, match=r'one'):
        bitset('Letters', '')


def test_duplicated_member():
    with pytest.raises(ValueError, match=r'duplicates'):
        bitset('Letters', 'abca')


def test_unhashable_members():
    with pytest.raises(TypeError, match=r'unhashable'):
        bitset('Letters', list('abc'))


def test_unhashable_member():
    with pytest.raises(TypeError, match=r'unhashable'):
        bitset('Letters', ([], None))


def test_wrong_base():
    with pytest.raises(ValueError, match=r'subclass'):
        bitset('Letters', 'abc', set)


def test_one_member():
    letter = bitset('Letter', 'a')
    assert letter('a').real == 1
    assert letter('').real == 0
