#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import os, sys

# z-base-32, http://philzimmermann.com/docs/human-oriented-base-32-encoding.txt
ZBASE32_ALPHABET = "ybndrfg8ejkmcpqxot1uwisza345h769"

def b2a_l(data, lengthinbits):
    """
    Encode the first lengthinbits bits of data in z-base-32, using as few
    characters as hold that many bits.  data must be exactly long enough
    for lengthinbits; any bits after the first lengthinbits are ignored.

    This gives the same result as b2a_l() from the zbase32 package, which
    randcookie used to require but which does not install on Python 3.
    """
    if (lengthinbits + 7) // 8 != len(data):
        raise ValueError("lengthinbits (%d) does not fit exactly in %d bytes"
                         % (lengthinbits, len(data)))
    numquintets = (lengthinbits + 4) // 5
    # Keep the first lengthinbits bits and pad them with zero bits to a
    # whole number of quintets.
    n = int.from_bytes(data, "big") >> (len(data) * 8 - lengthinbits)
    n <<= numquintets * 5 - lengthinbits
    return "".join(ZBASE32_ALPHABET[(n >> (5 * i)) & 31]
                   for i in reversed(range(numquintets)))

def main():
    if len(sys.argv) > 1:
        l = int(sys.argv[1])
    else:
        l = 64

    bl = (l + 7) // 8

    s = b2a_l(os.urandom(bl), l)

    # insert some hyphens for easier memorization
    chs = 3 + (len(s)%8==0)
    i = chs
    while i < len(s)-1:
        s = s[:i] + "-" + s[i:]
        i += 1
        chs = 7-chs
        i += chs

    print(s)

if __name__ == '__main__':
    main()

