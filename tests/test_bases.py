# test_bases.py

import re

import pytest


def test_repr_ints_cls(Ints):
    assert re.match(r"<class bitsets\.meta\.bitset\('Ints', \(1, 2, 3, 4, 5, 6\), 0x[0-9a-fA-F]+, MemberBits, None, None\)>",
                    repr(Ints))


def test_fromint(Ints):
    assert Ints.fromint(49) == Ints('100011')


def test_frommembers(Ints):
    assert Ints.frommembers([1, 5, 6]) == Ints('100011')


def test_frombools(Ints):
    assert Ints.frombools([True, '', None, 0, 'yes', 5]) == Ints('100011')


def test_frombits(Ints):
    assert Ints.frombits('100011') == Ints('100011')


def test_frombits_invalid(Ints):
    with pytest.raises(ValueError) as e:
        Ints.frombits('1000001')
    e.match(r'too many bits')


def test_copy(Ints):
    bs = Ints('100011')
    assert bs.copy() is bs
    changed = bs
    changed |= Ints('011100')
    assert changed == Ints('111111')
    assert bs == Ints('100011')


def test_int(Ints):
    assert Ints('100011').int == 49


def test_members(Ints):
    assert Ints('100011').members() == (1, 5, 6)


def test_members_as_set(Ints):
    assert Ints('110011').members(as_set=True) == frozenset([1, 2, 5, 6])


def test_bools(Ints):
    assert Ints('100011').bools() == (True, False, False, False, True, True)


def test_bits(Ints):
    assert Ints('100011').bits() == '100011'


def test_repr_ints(Ints):
    assert repr(Ints('100011')) == "Ints('100011')"


def test_atoms(Ints):
    assert list(Ints('100011').atoms()) == \
           [Ints('100000'), Ints('000010'), Ints('000001')]


def test_atoms_reverse(Ints):
    assert list(Ints('100011').atoms(reverse=True)) == \
           [Ints('000001'), Ints('000010'), Ints('100000')]


def test_inatoms(Ints):
    assert list(Ints('100011').inatoms()) == \
           [Ints('010000'), Ints('001000'), Ints('000100')]


def test_inatoms_reverse(Ints):
    assert list(Ints('100011').inatoms(reverse=True)) == \
           [Ints('000100'), Ints('001000'), Ints('010000')]


def test_powerset(Ints):
    triples = [i for i in Ints.supremum.powerset() if i.count() == 3]
    assert ['%d%d%d' % t.members() for t in triples] == \
           ['123', '124', '125', '126',
                   '134', '135', '136',
                          '145', '146',
                                 '156',
                   '234', '235', '236',
                          '245', '246',
                                 '256',
                          '345', '346',
                                 '356',
                                 '456']
    assert ['%d%d%d' % t.members() for t in sorted(triples)] == \
           ['123',
            '124', '134', '234',
            '125', '135', '235', '145', '245', '345',
            '126', '136', '236', '146', '246', '346', '156', '256', '356', '456']


def test_shortlex(Ints):
    uptotwo = [i for i in Ints.supremum.powerset() if i.count() <= 2]
    shortlex = [''.join(map(str, u.members()))
        for u in sorted(uptotwo, key=lambda u: u.shortlex())]
    assert shortlex == \
           ['',  '1',  '2',  '3',  '4',  '5',  '6',
                      '12', '13', '14', '15', '16',
                            '23', '24', '25', '26',
                                  '34', '35', '36',
                                        '45', '46',
                                              '56']


def test_longlex(Ints):
    uptotwo = [i for i in Ints.supremum.powerset() if i.count() <= 2]
    longlex = [''.join(map(str, u.members()))
        for u in sorted(uptotwo, key=lambda u: u.longlex())]
    assert longlex == \
           ['12', '13', '14', '15', '16',
                  '23', '24', '25', '26',
                        '34', '35', '36',
                              '45', '46',
                                    '56',
            '1',  '2',  '3',  '4',  '5',  '6',  '']


def test_shorcotlex(Ints):
    uptotwo = [i for i in Ints.supremum.powerset() if i.count() <= 2]
    shortcolex = [''.join(map(str, u.members()))
        for u in sorted(uptotwo, key=lambda u: u.shortcolex())]
    assert shortcolex == \
           ['',  '1',  '2',  '3',  '4',  '5',  '6',
            '12',
            '13', '23',
            '14', '24', '34',
            '15', '25', '35', '45',
            '16', '26', '36', '46', '56']


def test_longcolex(Ints):
    uptotwo = [i for i in Ints.supremum.powerset() if i.count() <= 2]
    longcolex = [''.join(map(str, u.members()))
        for u in sorted(uptotwo, key=lambda u: u.longcolex())]
    assert longcolex == \
           ['12',
            '13', '23',
            '14', '24', '34',
            '15', '25', '35', '45',
            '16', '26', '36', '46', '56',
            '1',  '2',  '3',  '4',  '5',  '6',  '']


def test_powerset_start(Ints):
    result = Ints('111').powerset(Ints('1'))
    assert list(result) == [Ints('1'), Ints('11'), Ints('101'), Ints('111')]


def test_powerset_invalid_start(Ints):
    with pytest.raises(ValueError) as e:
        Ints('1').powerset(Ints('111'))
    e.match(r'no subset')


def test_count(Ints):
    assert Ints('100011').count() == 3


def test_count_false(Ints):
    assert Ints('111011').count(False) == 1


def test_count_invalid(Ints):
    with pytest.raises(ValueError):
        Ints('110011').count('0')
    with pytest.raises(ValueError):
        Ints('110011').count('1')
    with pytest.raises(ValueError):
        Ints('110011').count(2)


def test_all(Ints):
    assert Ints('111111').all() is True
    assert Ints('001010').all() is False


def test_any(Ints):
    assert Ints('100000').any() is True
    assert Ints('000000').any() is False


def test_repr_nums_cls(Nums):
    assert re.match(r"<class bitsets\.meta\.bitset\('Nums', \(1, 2, 3, 4, 5, 6\), 0x[0-9a-fA-F]+, BitSet, List, Tuple\)>",
                    repr(Nums))


def test_bool(Nums):
    assert bool(Nums([1])) is True
    assert bool(Nums()) is False


def test_len(Nums):
    assert len(Nums([1])) == 1
    assert len(Nums()) == 0


def test_iter(Nums):
    assert list(Nums([1, 2, 3])) == [1, 2, 3]


def test_contains(Nums):
    assert 1 in Nums([1, 2])
    assert 2 not in Nums([1])
    assert 1 not in Nums()


def test_contains_invalid(Nums):
    with pytest.raises(KeyError) as e:
        -1 in Nums()
    assert e.value.args == (-1,)


def test_repr(Nums):
    assert repr(Nums([1, 2, 3])) == 'Nums([1, 2, 3])'


def test_issubset(Nums):
    assert Nums([1]).issubset(Nums([1, 2]))
    assert not Nums([1]).issubset(Nums())


def test_issubset_members(Nums):
    assert Nums([1]).issubset([1, 2])
    assert not Nums([1]).issubset([])


def test_issuperset(Nums):
    assert Nums([1, 2]).issuperset(Nums([1]))
    assert not Nums().issuperset(Nums([1]))


def test_issuperset_members(Nums):
    assert Nums([1, 2]).issuperset([1])
    assert not Nums().issuperset([1])


def test_isdisjoint(Nums):
    assert Nums([1, 2]).isdisjoint(Nums([3, 4]))
    assert not Nums([1, 2]).isdisjoint(Nums([2, 3]))


def test_isdisjoint_members(Nums):
    assert Nums([1, 2]).isdisjoint([3, 4])
    assert not Nums([1, 2]).isdisjoint([2, 3])


def test_intersection(Nums):
    assert Nums([1, 2]).intersection(Nums([2, 3])) == Nums([2])


def test_intersection_members(Nums):
    assert Nums([1, 2]).intersection([2, 3]) == Nums([2])


def test_union(Nums):
    assert Nums([1, 2]).union(Nums([2, 3])) == Nums([1, 2, 3])


def test_union_members(Nums):
    assert Nums([1, 2]).union([2, 3]) == Nums([1, 2, 3])


def test_difference(Nums):
    assert Nums([1, 2]).difference(Nums([2, 3])) == Nums([1])


def test_difference_members(Nums):
    assert Nums([1, 2]).difference([2, 3]) == Nums([1])


def test_symmetric_difference(Nums):
    assert Nums([1, 2]).symmetric_difference(Nums([2, 3])) == Nums([1, 3])


def test_symmetric_difference_members(Nums):
    assert Nums([1, 2]).symmetric_difference([2, 3]) == Nums([1, 3])


def test_complement(Nums):
    assert Nums([1, 2]).complement() == Nums([3, 4, 5, 6])
