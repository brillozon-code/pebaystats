
import unittest   as ut
import nose.tools as nt

import numpy as np

from context import pebaystats
from pebaystats import dstats

class StatsTest(ut.TestCase):
    def test_repr(self):
        print('\n\n  *** test_repr ***\n')
        a = dstats()
        print("REPR: %s" % repr(a))
        nt.assert_equal(repr(a), "dstats(n=0,moments=\n[[ 0.]\n [ 0.]\n [ 0.]\n [ 0.]])")

        b = dstats(2,4)
        print("REPR: %s" % repr(b))
        nt.assert_equal(repr(b), "dstats(n=0,moments=\n[[ 0.  0.  0.  0.]\n [ 0.  0.  0.  0.]])")

        c = dstats(4,12)
        print("REPR: %s" % repr(c))
        nt.assert_equal(repr(c), "dstats(n=0,moments=\n[[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]\n [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]\n [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]\n [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]])")

        a.add(24)
        a.add(42)
        a.add(24)
        a.add(42)
        print("REPR: %s" % repr(a))
        nt.assert_equal(repr(a), "dstats(n=4,moments=\n[[    33.]\n [   324.]\n [     0.]\n [ 26244.]])")

    def test_str(self):
        print('\n\n  *** test_str ***\n')
        a = dstats()
        print("STR: %s" % a)
        nt.assert_equal(str(a), "dstats: 4 moments, 1 columns, 0 rows\n[[ 0.]\n [ 0.]\n [ 0.]\n [ 0.]]")

        b = dstats(2,4)
        print("STR: %s" % b)
        nt.assert_equal(str(b), "dstats: 2 moments, 4 columns, 0 rows\n[[ 0.  0.  0.  0.]\n [ 0.  0.  0.  0.]]")

        c = dstats(4,12)
        print("STR: %s" % c)
        nt.assert_equal(str(c), "dstats: 4 moments, 12 columns, 0 rows\n[[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]\n [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]\n [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]\n [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]]")

        a.add(24)
        a.add(42)
        a.add(24)
        a.add(42)
        print("STD: %s" % a)
        nt.assert_equal(str(a), "dstats: 4 moments, 1 columns, 4 rows\n[[    33.]\n [   324.]\n [     0.]\n [ 26244.]]")

