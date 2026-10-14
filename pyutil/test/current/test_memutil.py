#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import io, unittest

from pyutil import memutil

def a_function():
    pass

class AClass:
    def a_method(self):
        pass

class MemUtilTestCase(unittest.TestCase):
    def test_estimate_mem_of_obj(self):
        for o in (b"abc", "abc", [1, 2], {1: 2}, 7, 2**100, 1.5, object()):
            self.assertTrue(memutil.estimate_mem_of_obj(o) > 0, o)
        self.assertTrue(memutil.estimate_mem_of_obj("abc") > memutil.estimate_mem_of_obj(b"abc"))

    def test_describe_object(self):
        self.assertIn("a_function", memutil.describe_object(a_function))
        self.assertIn("a_method", memutil.describe_object(AClass().a_method))
        self.assertIn("a_function", memutil.describe_object_with_dict_details(a_function))
        self.assertIn("a_method", memutil.describe_object_with_dict_details(AClass().a_method))

    def test_describe_dicts(self):
        d = {"a": 1, "b": [2]}
        self.assertTrue(memutil.describe_object_with_dict_details(d).startswith(str(dict)))
        desc = memutil.describe_dict(d)
        self.assertTrue(desc.startswith("<dict2-"), desc)
        self.assertIn(str(int), desc)
        self.assertIn(str(list), desc)

    def test_dump_description_of_object_refs(self):
        o = AClass()
        o.spam = "eggs"
        f = io.StringIO()
        memutil.dump_description_of_object_refs(o, f)
        self.assertIn("4:spam,", f.getvalue())

    def test_slope(self):
        self.assertEqual(memutil.linear_fit_slope([1, 2, 3], [2, 4, 6]), 2.0)
