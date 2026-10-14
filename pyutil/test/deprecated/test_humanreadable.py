#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import unittest

from pyutil.humanreadable import hr, brepr

def a_function():
    pass

class AClass:
    def a_method(self):
        pass

class HumanReadableTestCase(unittest.TestCase):
    def test_function(self):
        expected = '<a_function() at test_humanreadable.py:%d>' % (a_function.__code__.co_firstlineno,)
        self.assertEqual(hr(a_function), expected)
        self.assertEqual(hr([a_function]), '[' + expected + ']')

    def test_instance_method(self):
        expected = '<AClass.a_method() at test_humanreadable.py:%d>' % (AClass.a_method.__code__.co_firstlineno,)
        self.assertEqual(brepr.repr_instance_method(AClass().a_method, 1), expected)
