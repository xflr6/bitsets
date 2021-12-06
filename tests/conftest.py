import pytest

import bitsets


@pytest.fixture(scope='session')
def Ints():  # noqa: N802
    return bitsets.bases.MemberBits._make_subclass('Ints', (1, 2, 3, 4, 5, 6))


@pytest.fixture(scope='session')
def Nums():  # noqa: N802
    return bitsets.bases.BitSet._make_subclass('Nums', (1, 2, 3, 4, 5, 6),
                                               listcls=bitsets.series.List,
                                               tuplecls=bitsets.series.Tuple)


@pytest.fixture(scope='session')
def Four():  # noqa: N802
    return bitsets.bitset('Four', (1, 2, 3, 4))
