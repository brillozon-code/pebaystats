
import unittest   as ut
import nose.tools as nt
from nose.tools import raises

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

    @raises(pebaystats.UnsupportedMethod)
    def test_unsupported(self):
        print('\n\n  *** test_unsupported_method ***\n')
        a = dstats()
        a.add(5)
        a.remove(5)

    @raises(pebaystats.ExcessiveMoments)
    def test_excessive_add(self):
        print('\n\n  *** test_excessive_add ***\n')
        a = dstats(5,1)
        a.add(5)

    @raises(pebaystats.ExcessiveMoments)
    def test_excessive_aggregate(self):
        print('\n\n  *** test_excessive_aggregate ***\n')
        a = dstats()
        a.__set_state__({"n":6,"moments":np.zeros((5,1),np.float64)})
        b = dstats()
        b.__set_state__({"n":2,"moments":np.zeros((5,1),np.float64)})
        a.aggregate(b)

    @raises(pebaystats.ExcessiveMoments)
    def test_excessive_statistics(self):
        print('\n\n  *** test_excessive_statistics ***\n')
        a = dstats(5,1)
        a.__set_state__({"n":6,"moments":np.zeros((5,1),np.float64)})
        a.statistics()


