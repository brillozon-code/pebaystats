
import unittest   as ut
import nose.tools as nt

import numpy as np
import pickle

import os, sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath('.') + '/pebaystats/tests/')
sys.path.insert(0, os.path.abspath('.') + '/tests/')
sys.path.insert(0, os.path.abspath('.') + '/../')

from pebaystats import dstats

class StatsTest(ut.TestCase):
    def test_repr(self):
        a = dstats()
        print("REPR: %s" % repr(a))

        b = dstats(2,4)
        print("REPR: %s" % repr(b))

        c = dstats(4,12)
        print("REPR: %s" % repr(c))

        a.add(24)
        a.add(42)
        a.add(24)
        a.add(42)
        print("REPR: %s" % repr(a))

    def test_str(self):
        a = dstats()
        print("STR: %s" % a)

        b = dstats(2,4)
        print("STR: %s" % b)

        c = dstats(4,12)
        print("STR: %s" % c)

        a.add(24)
        a.add(42)
        a.add(24)
        a.add(42)
        print("STD: %s" % a)

