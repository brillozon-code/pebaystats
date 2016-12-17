
import unittest   as ut
import nose.tools as nt

import numpy as np

from context import pebaystats
from pebaystats import dstats

class StatsTest(ut.TestCase):
    def test_repr(self):
        a = dstats()
        print("REPR: %s" % repr(a))
        nt.assert_equal(repr(a), "dstats(depth=4,width=1,n=0)")

        b = dstats(2,4)
        print("REPR: %s" % repr(b))
        nt.assert_equal(repr(b), "dstats(depth=2,width=4,n=0)")

        c = dstats(4,12)
        print("REPR: %s" % repr(c))
        nt.assert_equal(repr(c), "dstats(depth=4,width=12,n=0)")

        a.add(24)
        a.add(42)
        a.add(24)
        a.add(42)
        print("REPR: %s" % repr(a))
        nt.assert_equal(repr(a), "dstats(depth=4,width=1,n=4)")

    def test_str(self):
        a = dstats()
        print("STR: %s" % a)
        nt.assert_equal(repr(a), "dstats: 4 moments, 1 columns, 0 rows")

        b = dstats(2,4)
        print("STR: %s" % b)
        nt.assert_equal(repr(b), "dstats: 2 moments, 4 columns, 0 rows")

        c = dstats(4,12)
        print("STR: %s" % c)
        nt.assert_equal(repr(c), "dstats: 4 moments, 12 columns, 0 rows")

        a.add(24)
        a.add(42)
        a.add(24)
        a.add(42)
        print("STD: %s" % a)
        nt.assert_equal(repr(a), "dstats: 4 moments, 1 columns, 4 rows")

