#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import random, sys, traceback, unittest

from pyutil.assertutil import _assert

from pyutil import dictutil

# The int objects themselves (small ints are cached), so that the tests
# below compare by identity without a SyntaxWarning for 'is' with a literal.
THREE, SEVEN, EIGHT = 3, 7, 8

class EqButNotIs:
    def __init__(self, x):
        self.x = x
        self.hash = int(random.randrange(0, 2**31))
    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.x,)
    def __hash__(self):
        return self.hash
    def __le__(self, other):
        return self.x <= other
    def __lt__(self, other):
        return self.x < other
    def __ge__(self, other):
        return self.x >= other
    def __gt__(self, other):
        return self.x > other
    def __ne__(self, other):
        return self.x != other
    def __eq__(self, other):
        return self.x == other

class Testy(unittest.TestCase):
    def _help_test_empty_dict(self, klass):
        d1 = klass()
        d2 = klass({})

        self.assertTrue(d1 == d2, "klass: %s, d1: %r, d2: %r" % (klass, d1, d2,))
        self.assertTrue(len(d1) == 0)
        self.assertTrue(len(d2) == 0)

    def _help_test_nonempty_dict(self, klass):
        # Python 2 allowed comparison between str and int,
        # therefore mixing values of different types in ValueOrderedDict
        # would work. It's now a TypeError in Python 3.
        #d1 = klass({'a': 1, 'b': "eggs", 3: "spam",})
        d1 = klass({'a': '1', 'b': "eggs", 3: "spam",})
        d2 = klass({'a': '1', 'b': "eggs", 3: "spam",})

        self.assertTrue(d1 == d2)
        self.assertTrue(len(d1) == 3, "%s, %s" % (len(d1), d1,))
        self.assertTrue(len(d2) == 3)

    def _help_test_eq_but_notis(self, klass):
        d = klass({'a': 3, 'b': EqButNotIs(3), 'c': 3})
        d.pop('b')

        d.clear()
        d['a'] = 3
        d['b'] = EqButNotIs(3)
        d['c'] = 3
        d.pop('b')

        d.clear()
        d['b'] = EqButNotIs(3)
        d['a'] = 3
        d['c'] = 3
        d.pop('b')

        d.clear()
        d['a'] = EqButNotIs(3)
        d['c'] = 3
        d['a'] = 3

        d.clear()
        fake3 = EqButNotIs(3)
        fake7 = EqButNotIs(7)
        d[fake3] = fake7
        d[3] = 7
        d[3] = 8
        # note: we want 'is' and not '=='
        _assert(any(x for x in d.values() if x is EIGHT))
        _assert(any(x for x in d.values() if x is fake7))
        _assert(not any(x for x in d.values() if x is SEVEN)) # The real 7 should have been ejected by the d[3] = 8.
        _assert(any(x for x in d if x is fake3))
        _assert(any(x for x in d if x is THREE))
        d[fake3] = 8

        d.clear()
        d[3] = 7
        fake3 = EqButNotIs(3)
        fake7 = EqButNotIs(7)
        d[fake3] = fake7
        d[3] = 8
        _assert(any(x for x in d.values() if x is EIGHT))
        _assert(any(x for x in d.values() if x is fake7))
        _assert(not any(x for x in d.values() if x is SEVEN)) # The real 7 should have been ejected by the d[3] = 8.
        _assert(any(x for x in d if x is fake3))
        _assert(any(x for x in d if x is THREE))
        d[fake3] = 8

    def test_em(self):
        for klass in (dictutil.UtilDict, dictutil.NumDict, dictutil.ValueOrderedDict,):
            # print "name of class: ", klass
            for helper in (self._help_test_empty_dict, self._help_test_nonempty_dict, self._help_test_eq_but_notis,):
                # print "name of test func: ", helper
                helper(klass)

    def test_move(self):
        d1 = {'a': 1, 'b': 2}
        d2 = {}
        dictutil.move('a', d1, d2, strict=True)
        self.assertEqual(d1, {'b': 2})
        self.assertEqual(d2, {'a': 1})
        self.assertRaises(KeyError, dictutil.move, 'a', d1, d2, strict=True)

    def test_subtract(self):
        # d1 bigger than d2
        self.assertEqual(dictutil.subtract({1: 1, 2: 2, 3: 3}, {2: 0, 4: 0}), {1: 1, 3: 3})
        # d1 not bigger than d2: deletes from d1 while walking its keys
        self.assertEqual(dictutil.subtract({1: 1, 2: 2}, {1: 0, 2: 0, 3: 0}), {})

    def test_items_sorted_by_key(self):
        for klass in (dictutil.UtilDict, dictutil.NumDict,):
            d = klass({'b': 2, 'a': 1})
            self.assertEqual(d.items_sorted_by_key(), [('a', 1), ('b', 2)])

    def test_numdict(self):
        d = dictutil.NumDict()
        d.inc('a')
        d.add_num('b', 5)
        d.add_num('c', 2)
        self.assertEqual(d.sum(), 8)
        self.assertEqual(d.item_with_largest_value(), ('b', 5))

def suite():
    suite = unittest.makeSuite(Testy, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()
