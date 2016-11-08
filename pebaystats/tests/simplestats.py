
from unittest import TestCase

import numpy as np
from pebaystats import pebaystats

class SimpleStats(TestCase):
    def test_single_value(self):
        pstats = pebaystats.pebaystats(4,3)
        pstats.add(np.array([10,20,30]))
        pstats.add(np.array([10,20,30]))
        pstats.add(np.array([10,20,30]))
        pstats.add(np.array([10,20,30]))
        pstats.add(np.array([10,20,30]))
        pstats.add(np.array([20,40,60]))
        pstats.add(np.array([20,40,60]))
        pstats.add(np.array([20,40,60]))
        pstats.add(np.array([20,40,60]))
        pstats.add(np.array([20,40,60]))
        print('stats are: %s' % pstats.statistics(True))


