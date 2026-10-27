# -*- coding: utf-8; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import unittest

from pyutil.scripts import passphrase

class Passphrase(unittest.TestCase):
    def test_no_short_words(self):
        # A dictionary without any one- or two-letter words used to raise
        # "ValueError: math domain error" (log2 of an empty word set).
        allwords = set(["%s%s%s" % (a, b, c) for a in "abcd" for b in "abcd" for c in "abcd"])
        phrase, bits = passphrase.gen_passphrase(20, allwords)
        self.assertGreaterEqual(bits, 20)
        for word in phrase.split("."):
            self.assertIn(word, allwords)

    def test_mixed_lengths(self):
        allwords = set(["a", "bb", "ccc", "dddd", "eeeee", "ffffff"])
        phrase, bits = passphrase.gen_passphrase(5, allwords)
        self.assertGreaterEqual(bits, 5)
        for word in phrase.split("."):
            self.assertIn(word, allwords)
