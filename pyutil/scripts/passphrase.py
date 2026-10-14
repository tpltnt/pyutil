#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import argparse, math, random, sys

from pyutil.mathutil import div_ceil

from importlib import resources

def recursive_subset_sum(entropy_needed, wordlists):
    # Pick a minimalish set of numbers which sum to at least
    # entropy_needed.

    # Okay now what's the smallest number of words which will give us
    # at least this much entropy?
    entropy_of_biggest_wordlist = wordlists[-1][0]
    assert isinstance(entropy_of_biggest_wordlist, float), wordlists[-1]
    needed_words = div_ceil(entropy_needed, entropy_of_biggest_wordlist)
    # How much entropy do we need from each word?
    needed_entropy_per_word = entropy_needed / needed_words
    # What's the smallest wordlist that offers at least this much
    # entropy per word?
    for (wlentropy, wl) in wordlists:
        if wlentropy >= needed_entropy_per_word:
            break
    assert wlentropy >= needed_entropy_per_word, (wlentropy, needed_entropy_per_word)

    result = [(wlentropy, wl)]
    # If we need more, recurse...
    if wlentropy < entropy_needed:
        rest = recursive_subset_sum(entropy_needed - wlentropy, wordlists)
        result.extend(rest)
    return result

def gen_passphrase(entropy, allwords):
    maxlenwords = []
    i = 2 # The smallest set is words of length 1 or 2.
    while True:
        words = [x for x in allwords if len(x) <= i]
        # A dictionary need not have words of every length; skip the
        # empty sets (log2 of 0 is undefined).
        if words:
            maxlenwords.append((math.log(len(words), 2), words))
        if len(words) >= len(allwords):
            break
        i += 1

    sr = random.SystemRandom()
    passphrase = []

    wordlists_to_use = recursive_subset_sum(entropy, maxlenwords)

    passphraseentropy = 0.0
    for (wle, wl) in wordlists_to_use:
        passphrase.append(sr.choice(wl))
        passphraseentropy += wle

    return (u".".join(passphrase), passphraseentropy)

def main():
    parser = argparse.ArgumentParser(prog="passphrase", description="Create a random passphrase by picking a few random words.")

    parser.add_argument('-d', '--dictionary', help="what file to read a list of words from (or omit this option to use passphrase's bundled dictionary)", type=argparse.FileType('rb'), metavar="DICT")
    parser.add_argument('bits', help="how many bits of entropy minimum", type=float, metavar="BITS")
    args = parser.parse_args()

    dicti = args.dictionary
    if not dicti:
        dicti = resources.files("pyutil").joinpath("data/wordlist.txt").open("rb")
    allwords = set([x.decode('utf-8').strip().lower() for x in dicti.readlines()])

    passphrase, bits = gen_passphrase(args.bits, allwords)

    sys.stdout.write(passphrase)
    sys.stdout.write('\n')

    sys.stderr.write(u"This passphrase encodes about {:.0f} bits.\n".format(bits))
