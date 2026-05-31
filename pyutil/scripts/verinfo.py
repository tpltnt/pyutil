#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-
import exceptions
class UsageError(exceptions.Exception): pass

import sys
from importlib.metadata import version, distribution, PackageNotFoundError

def main():
    if len(sys.argv) <= 1:
        raise UsageError("USAGE: verinfo DISTRIBUTIONNAME [PACKAGENAME]")
    DISTNAME=sys.argv[1]
    if len(sys.argv) >= 3:
        PACKNAME=sys.argv[2]
    else:
        PACKNAME=DISTNAME

    try:
        dist = distribution(DISTNAME)
        print(dist)
        print("version:", version(DISTNAME))
    except PackageNotFoundError:
        print("ERROR: Distribution '%s' not installed" % DISTNAME)
        return

    print("import %s;print %s => " % (PACKNAME, PACKNAME,))

    try:
        x = __import__(PACKNAME)
        print(x)
    except ImportError as e:
        print("ERROR importing %s: %s" % (PACKNAME, e))
        return

    print("import %s; print %s.__version__ => " % (PACKNAME, PACKNAME))
    print(getattr(x, "__version__", None))

if __name__ == "__main__":
    main()
