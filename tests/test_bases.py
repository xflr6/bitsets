import pickle
import re

import pytest


def test_reconstruct(Ints):  # noqa: N803
    assert pickle.loads(pickle.dumps(Ints('110011'))) == Ints('110011')


def test_repr_ints_cls(Ints):  # noqa: N803
    assert re.match(r"<class bitsets\.meta\.bitset\("
                    r"'Ints', \(1, 2, 3, 4, 5, 6\), "
                    r"0x[0-9a-fA-F]+, MemberBits, None, None"
                    r"\)>", repr(Ints))


def test_fromint(Ints):  # noqa: N803
    assert Ints.fromint(49) == Ints('100011')


def test_frommembers(Ints):  # noqa: N803
    assert Ints.frommembers([1, 5, 6]) == Ints('100011')


def test_frombools(Ints):  # noqa: N803
    assert Ints.frombools([True, '', None, 0, 'yes', 5]) == Ints('100011')


def test_frombits(Ints):  # noqa: N803
    assert Ints.frombits('100011') == Ints('100011')


def test_frombits_invalid(Ints):  # noqa: N803
    with pytest.raises(ValueError, match=r'too many bits'):
        Ints.frombits('1000001')


def test_copy(Ints):  # noqa: N803
    bs = Ints('100011')
    assert bs.copy() is bs
    changed = bs
    changed |= Ints('011100')
    assert changed == Ints('111111')
    assert bs == Ints('100011')


def test_int(Ints):  # noqa: N803
    assert Ints('100011').int == 49


def test_members(Ints):  # noqa: N803
    assert Ints('100011').members() == (1, 5, 6)


def test_members_as_set(Ints):  # noqa: N803
    assert Ints('110011').members(as_set=True) == frozenset([1, 2, 5, 6])


def test_bools(Ints):  # noqa: N803
    assert Ints('100011').bools() == (True, False, False, False, True, True)


def test_bits(Ints):  # noqa: N803
    assert Ints('100011').bits() == '100011'


def test_repr_ints(Ints):  # noqa: N803
    assert repr(Ints('100011')) == "Ints('100011')"


def test_atoms(Ints):  # noqa: N803
    assert list(Ints('100011').atoms()) == [Ints('100000'),
                                            Ints('000010'),
                                            Ints('000001')]


def test_atoms_reverse(Ints):  # noqa: N803
    assert list(Ints('100011').atoms(reverse=True)) == [Ints('000001'),
                                                        Ints('000010'),
                                                        Ints('100000')]


def test_inatoms(Ints):  # noqa: N803
    assert list(Ints('100011').inatoms()) == [Ints('010000'),
                                              Ints('001000'),
                                              Ints('000100')]


def test_inatoms_reverse(Ints):  # noqa: N803
    assert list(Ints('100011').inatoms(reverse=True)) == [Ints('000100'),
                                                          Ints('001000'),
                                                          Ints('010000')]


def test_powerset(Ints):  # noqa: N803
    triples = [i for i in Ints.supremum.powerset() if i.count() == 3]
    members = ['{:d}{:d}{:d}'.format(*t.members()) for t in triples]
    assert members == ['123', '124', '125', '126',
                              '134', '135', '136',
                                     '145', '146',
                                            '156',
                              '234', '235', '236',
                                     '245', '246',
                                            '256',
                                     '345', '346',
                                            '356',
                                            '456']
    msorted = ['{:d}{:d}{:d}'.format(*t.members()) for t in sorted(triples)]
    assert msorted == ['123',
                       '124', '134', '234',
                       '125', '135', '235', '145', '245', '345',
                       '126', '136', '236', '146', '246', '346', '156', '256', '356', '456']


def test_shortlex(Ints):  # noqa: N803
    uptotwo = [i for i in Ints.supremum.powerset() if i.count() <= 2]
    shortlex = [''.join(map(str, u.members()))
                for u in sorted(uptotwo, key=lambda u: u.shortlex())]
    assert shortlex == ['',
                        u'1', u'2', u'3', u'4', u'5', u'6',
                              '12', '13', '14', '15', '16',
                                    '23', '24', '25', '26',
                                          '34', '35', '36',
                                                '45', '46',
                                                      '56']


def test_longlex(Ints):  # noqa: N803
    uptotwo = [i for i in Ints.supremum.powerset() if i.count() <= 2]
    longlex = [''.join(map(str, u.members()))
               for u in sorted(uptotwo, key=lambda u: u.longlex())]
    assert longlex == ['12', '13', '14', '15', '16',
                             '23', '24', '25', '26',
                                   '34', '35', '36',
                                         '45', '46',
                                               '56',
                  '1', u'2', u'3', u'4', u'5', u'6',
                  '']


def test_shorcotlex(Ints):  # noqa: N803
    uptotwo = [i for i in Ints.supremum.powerset() if i.count() <= 2]
    shortcolex = [''.join(map(str, u.members()))
                  for u in sorted(uptotwo, key=lambda u: u.shortcolex())]
    assert shortcolex == ['',
                          '1', u'2', u'3', u'4', u'5', u'6',
                          '12',
                          '13', '23',
                          '14', '24', '34',
                          '15', '25', '35', '45',
                          '16', '26', '36', '46', '56']


def test_longcolex(Ints):  # noqa: N803
    uptotwo = [i for i in Ints.supremum.powerset() if i.count() <= 2]
    longcolex = [''.join(map(str, u.members()))
                 for u in sorted(uptotwo, key=lambda u: u.longcolex())]
    assert longcolex == ['12',
                         '13', '23',
                         '14', '24', '34',
                         '15', '25', '35', '45',
                         '16', '26', '36', '46', '56',
                         '1', u'2', u'3', u'4', u'5', u'6',
                         '']


@pytest.mark.parametrize('bits, other, expected', [
    ('111', '1', ['1', '11', '101', '111']),
    ('111', '11', ['11', '111']),
])
def test_powerset_start(Ints, bits, other, expected):  # noqa: N803
    assert list(Ints(bits).powerset(Ints(other))) == [Ints(e) for e in expected]


def test_powerset_invalid_start(Ints):  # noqa: N803
    with pytest.raises(ValueError, match=r'no subset'):
        Ints('1').powerset(Ints('111'))


def test_count(Ints):  # noqa: N803
    assert Ints('100011').count() == 3


def test_count_false(Ints):  # noqa: N803
    assert Ints('111011').count(False) == 1


@pytest.mark.parametrize('value', ['0', '1', 2, None, -1, object()])
def test_count_invalid(Ints, value):  # noqa: N803
    with pytest.raises(ValueError, match=r'True or False'):
        Ints('110011').count(value)


@pytest.mark.parametrize('bits, expected', [('111111', True), ('001010', False)])
def test_all(Ints, bits, expected):  # noqa: N803
    assert Ints(bits).all() is expected


@pytest.mark.parametrize('bits, expected', [('100000', True), ('000000', False)])
def test_any(Ints, bits, expected):  # noqa: N803
    assert Ints(bits).any() is expected


def test_repr_nums_cls(Nums):  # noqa: N803
    assert re.match(r"<class bitsets\.meta\.bitset\("
                    r"'Nums', \(1, 2, 3, 4, 5, 6\), "
                    r"0x[0-9a-fA-F]+, BitSet, List, Tuple"
                    r"\)>", repr(Nums))


@pytest.mark.parametrize('args, expected', [(([1],), True), ((), False)])
def test_bool(Nums, args, expected):  # noqa: N803
    assert bool(Nums(*args)) is expected


@pytest.mark.parametrize('args, expected', [(([1],), 1), ((), 0), (([1, 2],), 2)])
def test_len(Nums, args, expected):  # noqa: N803
    assert len(Nums(*args)) == expected


def test_iter(Nums):  # noqa: N803
    assert list(Nums([1, 2, 3])) == [1, 2, 3]


def test_contains(Nums):  # noqa: N803
    assert 1 in Nums([1, 2])
    assert 2 not in Nums([1])
    assert 1 not in Nums()


def test_contains_invalid(Nums):  # noqa: N803
    with pytest.raises(KeyError) as e:
        -1 in Nums()
    assert e.value.args == (-1,)


def test_repr(Nums):  # noqa: N803
    assert repr(Nums([1, 2, 3])) == 'Nums([1, 2, 3])'


def test_issubset(Nums):  # noqa: N803
    assert Nums([1]).issubset(Nums([1, 2]))
    assert not Nums([1]).issubset(Nums())


def test_issubset_members(Nums):  # noqa: N803
    assert Nums([1]).issubset([1, 2])
    assert not Nums([1]).issubset([])


def test_issuperset(Nums):  # noqa: N803
    assert Nums([1, 2]).issuperset(Nums([1]))
    assert not Nums().issuperset(Nums([1]))


def test_issuperset_members(Nums):  # noqa: N803
    assert Nums([1, 2]).issuperset([1])
    assert not Nums().issuperset([1])


def test_isdisjoint(Nums):  # noqa: N803
    assert Nums([1, 2]).isdisjoint(Nums([3, 4]))
    assert not Nums([1, 2]).isdisjoint(Nums([2, 3]))


def test_isdisjoint_members(Nums):  # noqa: N803
    assert Nums([1, 2]).isdisjoint([3, 4])
    assert not Nums([1, 2]).isdisjoint([2, 3])


def test_intersection(Nums):  # noqa: N803
    assert Nums([1, 2]).intersection(Nums([2, 3])) == Nums([2])


def test_intersection_members(Nums):  # noqa: N803
    assert Nums([1, 2]).intersection([2, 3]) == Nums([2])


def test_union(Nums):  # noqa: N803
    assert Nums([1, 2]).union(Nums([2, 3])) == Nums([1, 2, 3])


def test_union_members(Nums):  # noqa: N803
    assert Nums([1, 2]).union([2, 3]) == Nums([1, 2, 3])


def test_difference(Nums):  # noqa: N803
    assert Nums([1, 2]).difference(Nums([2, 3])) == Nums([1])


def test_difference_members(Nums):  # noqa: N803
    assert Nums([1, 2]).difference([2, 3]) == Nums([1])


def test_symmetric_difference(Nums):  # noqa: N803
    assert Nums([1, 2]).symmetric_difference(Nums([2, 3])) == Nums([1, 3])


def test_symmetric_difference_members(Nums):  # noqa: N803
    assert Nums([1, 2]).symmetric_difference([2, 3]) == Nums([1, 3])


def test_complement(Nums):  # noqa: N803
    assert Nums([1, 2]).complement() == Nums([3, 4, 5, 6])
