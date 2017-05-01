# conftest.py

import pytest

import bitsets


@pytest.fixture(scope='session')
def Ints():
    return bitsets.bases.MemberBits._make_subclass('Ints', (1, 2, 3, 4, 5, 6))


@pytest.fixture(scope='session')
def Nums():
    return bitsets.bases.BitSet._make_subclass('Nums', (1, 2, 3, 4, 5, 6),
                                               listcls=bitsets.series.List,
                                               tuplecls=bitsets.series.Tuple)


@pytest.fixture(scope='session')
def Four():
    return bitsets.bitset('Four', (1, 2, 3, 4))
