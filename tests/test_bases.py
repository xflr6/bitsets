# test_bases.py

import unittest

from bitsets.bases import MemberBits, BitSet


class TestMemberBits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.Ints = MemberBits._make_subclass('Ints', (1, 2, 3, 4, 5, 6))

    @classmethod
    def tearDownClass(cls):
        del cls.Ints

    def test_classrepr(self):
        self.assertRegexpMatches(repr(self.Ints),
            r"<class bitsets\.meta\.bitset\('Ints', \(1, 2, 3, 4, 5, 6\), 0x[0-9a-fA-F]+, MemberBits, None, None\)>")

    def test_fromint(self):
        self.assertEqual(self.Ints.fromint(49), self.Ints('100011'))

    def test_frommembers(self):
        self.assertEqual(self.Ints.frommembers([1, 5, 6]), self.Ints('100011'))

    def test_frombools(self):
        self.assertEqual(self.Ints.frombools([True, '', None, 0, 'yes', 5]),
            self.Ints('100011'))

    def test_frombits(self):
        self.assertEqual(self.Ints.frombits('100011'), self.Ints('100011'))

    def test_frombits_invalid(self):
        with self.assertRaisesRegexp(ValueError, 'too many bits'):
            self.Ints.frombits('1000001')

    def test_copy(self):
        bs = self.Ints('100011')
        self.assertIs(bs.copy(), bs)
        changed = bs
        changed |= self.Ints('011100')
        self.assertEqual(changed, self.Ints('111111'))
        self.assertEqual(bs, self.Ints('100011'))

    def test_int(self):
        self.assertEqual(self.Ints('100011').int, 49)

    def test_members(self):
        self.assertEqual(self.Ints('100011').members(), (1, 5, 6))

    def test_members_as_set(self):
        self.assertEqual(self.Ints('110011').members(as_set=True),
            frozenset([1, 2, 5, 6]))

    def test_bools(self):
        self.assertEqual(self.Ints('100011').bools(),
            (True, False, False, False, True, True))

    def test_bits(self):
        self.assertEqual(self.Ints('100011').bits(), '100011')

    def test_repr(self):
        self.assertEqual(repr(self.Ints('100011')), "Ints('100011')")

    def test_atoms(self):
        self.assertEqual(list(self.Ints('100011').atoms()),
            [self.Ints('100000'), self.Ints('000010'), self.Ints('000001')])

    def test_atoms_reverse(self):
        self.assertEqual(list(self.Ints('100011').atoms(reverse=True)),
            [self.Ints('000001'), self.Ints('000010'), self.Ints('100000')])

    def test_inatoms(self):
        self.assertEqual(list(self.Ints('100011').inatoms()),
            [self.Ints('010000'), self.Ints('001000'), self.Ints('000100')])

    def test_inatoms_reverse(self):
        self.assertEqual(list(self.Ints('100011').inatoms(reverse=True)),
            [self.Ints('000100'), self.Ints('001000'), self.Ints('010000')])

    def test_powerset(self):
        triples = [i for i in self.Ints.supremum.powerset() if i.count() == 3]
        self.assertEqual(['%d%d%d' % t.members() for t in triples],
            ['123', '124', '125', '126',
                    '134', '135', '136',
                           '145', '146',
                                  '156',
                    '234', '235', '236',
                           '245', '246',
                                  '256',
                           '345', '346',
                                  '356',
                                  '456'])
        self.assertEqual(['%d%d%d' % t.members() for t in sorted(triples)],
            ['123',
             '124', '134', '234',
             '125', '135', '235', '145', '245', '345',
             '126', '136', '236', '146', '246', '346', '156', '256', '356', '456'])

    def test_shortlex(self):
        uptotwo = [i for i in self.Ints.supremum.powerset() if i.count() <= 2]
        shortlex = [''.join(map(str, u.members()))
            for u in sorted(uptotwo, key=lambda u: u.shortlex())]
        self.assertEqual(shortlex,
            ['',  '1',  '2',  '3',  '4',  '5',  '6',
                       '12', '13', '14', '15', '16',
                             '23', '24', '25', '26',
                                   '34', '35', '36',
                                         '45', '46',
                                               '56'])

    def test_longlex(self):
        uptotwo = [i for i in self.Ints.supremum.powerset() if i.count() <= 2]
        longlex = [''.join(map(str, u.members()))
            for u in sorted(uptotwo, key=lambda u: u.longlex())]
        self.assertEqual(longlex,
            ['12', '13', '14', '15', '16',
                   '23', '24', '25', '26',
                         '34', '35', '36',
                               '45', '46',
                                     '56',
             '1',  '2',  '3',  '4',  '5',  '6',  ''])

    def test_shorcotlex(self):
        uptotwo = [i for i in self.Ints.supremum.powerset() if i.count() <= 2]
        shortcolex = [''.join(map(str, u.members()))
            for u in sorted(uptotwo, key=lambda u: u.shortcolex())]
        self.assertEqual(shortcolex,
            ['',  '1',  '2',  '3',  '4',  '5',  '6',
                  '12',
                  '13', '23',
                  '14', '24', '34',
                  '15', '25', '35', '45',
                  '16', '26', '36', '46', '56'])

    def test_longcolex(self):
        uptotwo = [i for i in self.Ints.supremum.powerset() if i.count() <= 2]
        longcolex = [''.join(map(str, u.members()))
            for u in sorted(uptotwo, key=lambda u: u.longcolex())]
        self.assertEqual(longcolex,
            ['12',
             '13', '23',
             '14', '24', '34',
             '15', '25', '35', '45',
             '16', '26', '36', '46', '56',
             '1',  '2',  '3',  '4',  '5',  '6',  ''])

    def test_powerset_start(self):
        result = self.Ints('111').powerset(self.Ints('1'))
        self.assertEqual(list(result),
            [self.Ints('1'), self.Ints('11'), self.Ints('101'),
             self.Ints('111')])

    def test_powerset_invalid_start(self):
        with self.assertRaisesRegexp(ValueError, 'no subset'):
            self.Ints('1').powerset(self.Ints('111'))

    def test_count(self):
        self.assertEqual(self.Ints('100011').count(), 3)

    def test_count_false(self):
        self.assertEqual(self.Ints('111011').count(False), 1)

    def test_count_invalid(self):
        with self.assertRaises(ValueError):
            self.Ints('110011').count('0')
        with self.assertRaises(ValueError):
            self.Ints('110011').count('1')
        with self.assertRaises(ValueError):
            self.Ints('110011').count(2)

    def test_all(self):
        self.assertTrue(self.Ints('111111').all())
        self.assertFalse(self.Ints('001010').all())

    def test_any(self):
        self.assertTrue(self.Ints('100000').any())
        self.assertFalse(self.Ints('000000').any())


class TestBitSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.Nums = BitSet._make_subclass('Nums', (1, 2, 3, 4, 5, 6))

    @classmethod
    def tearDownClass(cls):
        del cls.Nums

    def test_classrepr(self):
        self.assertRegexpMatches(repr(self.Nums),
            r"<class bitsets\.meta\.bitset\('Nums', \(1, 2, 3, 4, 5, 6\), 0x[0-9a-fA-F]+, BitSet, None, None\)>")

    def test_bool(self):
        self.assertTrue(self.Nums([1]))
        self.assertFalse(self.Nums())

    def test_len(self):
        self.assertEqual(len(self.Nums([1])), 1)
        self.assertEqual(len(self.Nums()), 0)

    def test_iter(self):
        self.assertEqual(list(self.Nums([1, 2, 3])), [1, 2, 3])

    def test_contains(self):
        self.assertTrue(1 in self.Nums([1, 2]))
        self.assertFalse(2 in self.Nums([1]))
        self.assertFalse(1 in self.Nums())

    def test_contains_invalid(self):
        with self.assertRaises(KeyError) as cm:
            -1 in self.Nums()
        self.assertEqual(cm.exception.args, (-1,))

    def test_repr(self):
        self.assertEqual(repr(self.Nums([1, 2, 3])), 'Nums([1, 2, 3])')

    def test_issubset(self):
        self.assertTrue(self.Nums([1]).issubset(self.Nums([1, 2])))
        self.assertFalse(self.Nums([1]).issubset(self.Nums()))

    def test_issubset_members(self):
        self.assertTrue(self.Nums([1]).issubset([1, 2]))
        self.assertFalse(self.Nums([1]).issubset([]))

    def test_issuperset(self):
        self.assertTrue(self.Nums([1, 2]).issuperset(self.Nums([1])))
        self.assertFalse(self.Nums().issuperset(self.Nums([1])))

    def test_issuperset_members(self):
        self.assertTrue(self.Nums([1, 2]).issuperset([1]))
        self.assertFalse(self.Nums().issuperset([1]))

    def test_isdisjoint(self):
        self.assertTrue(self.Nums([1, 2]).isdisjoint(self.Nums([3, 4])))
        self.assertFalse(self.Nums([1, 2]).isdisjoint(self.Nums([2, 3])))

    def test_isdisjoint_members(self):
        self.assertTrue(self.Nums([1, 2]).isdisjoint([3, 4]))
        self.assertFalse(self.Nums([1, 2]).isdisjoint([2, 3]))

    def test_intersection(self):
        self.assertEqual(self.Nums([1, 2]).intersection(self.Nums([2, 3])),
            self.Nums([2]))

    def test_intersection_members(self):
        self.assertEqual(self.Nums([1, 2]).intersection([2, 3]),
            self.Nums([2]))

    def test_union(self):
        self.assertEqual(self.Nums([1, 2]).union(self.Nums([2, 3])),
            self.Nums([1, 2, 3]))

    def test_union_members(self):
        self.assertEqual(self.Nums([1, 2]).union([2, 3]),
            self.Nums([1, 2, 3]))

    def test_difference(self):
        self.assertEqual(self.Nums([1, 2]).difference(self.Nums([2, 3])),
            self.Nums([1]))

    def test_difference_members(self):
        self.assertEqual(self.Nums([1, 2]).difference([2, 3]),
            self.Nums([1]))

    def test_symmetric_difference(self):
        self.assertEqual(self.Nums([1, 2]).symmetric_difference(self.Nums([2, 3])),
            self.Nums([1, 3]))

    def test_symmetric_difference_members(self):
        self.assertEqual(self.Nums([1, 2]).symmetric_difference([2, 3]),
            self.Nums([1, 3]))

    def test_complement(self):
        self.assertEqual(self.Nums([1, 2]).complement(),
            self.Nums([3, 4, 5, 6]))
