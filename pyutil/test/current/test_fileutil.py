# -*- coding: utf-8; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import unittest

import os

from pyutil import fileutil

class FileUtil(unittest.TestCase):
    def mkdir(self, basedir, path, mode=0o777):
        fn = os.path.join(basedir, path)
        fileutil.make_dirs(fn, mode)

    def touch(self, basedir, path, mode=None, data="touch\n"):
        fn = os.path.join(basedir, path)
        f = open(fn, "w")
        f.write(data)
        f.close()
        if mode is not None:
            os.chmod(fn, mode)

    def test_du(self):
        basedir = "util/FileUtil/test_du"
        fileutil.make_dirs(basedir)
        d = os.path.join(basedir, "space-consuming")
        self.mkdir(d, "a/b")
        self.touch(d, "a/b/1.txt", data="a"*10)
        self.touch(d, "a/b/2.txt", data="b"*11)
        self.mkdir(d, "a/c")
        self.touch(d, "a/c/1.txt", data="c"*12)
        self.touch(d, "a/c/2.txt", data="d"*13)

        used = fileutil.du(basedir)
        self.assertEqual(10+11+12+13, used)

    def test_reopenable_tempfile_shutdown_after_move(self):
        # lineutil.lineify_file() moves the temporary file into place, after
        # which shutdown() (and __del__) must not fail.
        import tempfile
        rntf = fileutil.ReopenableNamedTemporaryFile()
        dest = os.path.join(tempfile.mkdtemp(), "moved")
        os.rename(rntf.name, dest)
        rntf.shutdown()
        rntf.shutdown()
        self.assertTrue(os.path.exists(dest))
        os.remove(dest)
