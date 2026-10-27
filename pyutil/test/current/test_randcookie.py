# -*- coding: utf-8; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import contextlib, io, sys, unittest
from unittest import mock

from pyutil.scripts import randcookie

def bits_to_bytes(bits):
    # "01" -> b"\x40": the bits, MSB first, padded with zero bits
    n = len(bits)
    return (int(bits, 2) << (-n % 8)).to_bytes((n + 7) // 8, "big")

class B2aL(unittest.TestCase):
    # The EXAMPLES table of
    # http://philzimmermann.com/docs/human-oriented-base-32-encoding.txt
    SPEC_VECTORS = [
        ("0", "y"),
        ("1", "o"),
        ("01", "e"),
        ("11", "a"),
        ("0000000000", "yy"),
        ("1000000010", "on"),
        ("10001011100010001000", "tqre"),
        ("111100001011111111000111", "6n9hq"),
        ("110101000111101000000100", "4t7ye"),
        # The table gives "6im5sd" here, but 11110 10101 01011 11011 11010
        # 00011 is "6im54d", which is also what zbase32.b2a_l() returns.
        ("111101010101011110111101000011", "6im54d"),
    ]

    def test_spec_vectors(self):
        for bits, expected in self.SPEC_VECTORS:
            self.assertEqual(randcookie.b2a_l(bits_to_bytes(bits), len(bits)), expected, bits)

    def test_unused_bits_are_ignored(self):
        # Like zbase32.b2a_l(), only the first lengthinbits bits count; the
        # rest of the last byte is treated as zero bits.
        self.assertEqual(randcookie.b2a_l(b"\xff", 1), "o")
        self.assertEqual(randcookie.b2a_l(b"\xff", 2), "a")
        self.assertEqual(randcookie.b2a_l(b"\xff\xff", 10), "99")
        self.assertEqual(randcookie.b2a_l(b"\xff\xff", 12), "99a")
        self.assertEqual(randcookie.b2a_l(b"\xff\xff", 16), "999o")

    def test_length(self):
        for l in range(0, 130):
            s = randcookie.b2a_l(b"\xa5" * ((l + 7) // 8), l)
            self.assertEqual(len(s), (l + 4) // 5)
            self.assertTrue(set(s) <= set(randcookie.ZBASE32_ALPHABET))

    def test_wrong_data_length(self):
        self.assertRaises(ValueError, randcookie.b2a_l, b"\x00\x00", 8)
        self.assertRaises(ValueError, randcookie.b2a_l, b"\x00", 9)

class Main(unittest.TestCase):
    def run_main(self, *args, data=None):
        out = io.StringIO()
        argv = ["randcookie"] + list(args)
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(out):
            if data is None:
                randcookie.main()
            else:
                with mock.patch("os.urandom", lambda n: data[:n]):
                    randcookie.main()
        return out.getvalue().strip()

    def test_default(self):
        # 64 bits: 13 characters in groups of 3-4-3-3
        cookie = self.run_main(data=b"\x00\x44\x32\x14\xc7\x42\x54\xb6")
        self.assertEqual(cookie, "ybn-drfg-8ej-kmc")
        cookie = self.run_main()
        self.assertEqual([len(g) for g in cookie.split("-")], [3, 4, 3, 3])
        self.assertTrue(set(cookie.replace("-", "")) <= set(randcookie.ZBASE32_ALPHABET))

    def test_bits_argument(self):
        cookie = self.run_main("12", data=b"\xff\xff")
        self.assertEqual(cookie, "99a")
        cookie = self.run_main("128")
        self.assertEqual(len(cookie.replace("-", "")), 26)
