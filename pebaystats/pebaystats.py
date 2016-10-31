""" Copyright 2016 Michael James Martinez
"""

import numpy as np

class pebaystats(object):
    """implement Pebay's reduced complexity descriptive statistical moments

    Attributes:
        max_moment -- largest statistical moment to be calculated
        n          -- number of elements over which moments are calculated
        moments    -- list of current moment values
    """

    def __init__(self,max_moment=4,width=1):
        """return a new descriptive statistics accumulator
        """
        self.n       = 0
        self.depth   = max_moment
        self.moments = np.zeros((1+max_moment,width),dtype=np.float64)

    def n(self,new_n=None):
        """access and possibly modify the number of elements in the
           aggregated statistics
        """
        if new_n is not None:
            self.n = new_n
        return self.n

    def add(self,value):
        """add a new value to the aggregated statistics
        """
        pass

    def remove(self,value):
        """remove a value from the aggregated statistics
        """
        pass

    def statistics(self,calculateDeviation=False):
        """generate and return the descriptive statistic of the current
           aggregation
        """
        pass
