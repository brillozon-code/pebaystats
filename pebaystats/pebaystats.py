"""low complexity descriptive statistics 
"""
from __future__ import print_function

import numpy as np
from copy import deepcopy

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
        self.n       = np.int64(0)
        self.depth   = np.int32(max_moment)
        self.width   = np.int64(width)
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

            Arguments:
                value - row of data values to aggregate.  This must be a
                        Numpy array of values.
        """

        # Adjust the number of values in the data set.
        self.n += 1
        size = self.n

        # Check for the first value added to the data set.
        if self.depth == 0:
            return

        # Get ready to calculate.
        delta        = value - self.moments[0]
        delta_over_n = delta / size
        term2        = np.float64(0.0)
        term3        = np.float64(0.0)
        term4        = np.float64(0.0)

        if self.depth > 1:
            delta_delta_over_n = delta_over_n * delta

            # M2
            term2 = delta_delta_over_n * (size - 1.0)

            if self.depth > 2:
                M2 = self.moments[1]
                delta_delta_delta_over_n_n = delta_delta_over_n * delta_over_n

                # M3
                term3 = (delta_delta_delta_over_n_n
                            * (size - 1.0) * (size - 2.0)
                            - 3.0 * delta_over_n * M2)

                if self.depth > 3:
                    M3 = self.moments[2]

                    # M4
                    term4 = (delta_over_n * delta_delta_delta_over_n_n
                                * (size - 1.0) * (size * size - 3.0 * size + 3.0)
                                + 6.0 * delta_over_n * delta_over_n * M2
                                - 4.0 * delta_over_n * M3)

        # M1
        self.moments[0] += delta_over_n
        if self.depth == 1:
            return

        # M2
        self.moments[1] += term2
        if self.depth == 2:
            return

        # M3
        self.moments[2] += term3
        if self.depth == 3:
            return

        # M4
        self.moments[3] += term4
        if self.depth == 4:
            return

    def aggregate(self,rhs):
        n_1 = self.n
        n_2 = rhs.n
        n_new = n_1 + n_2

        mu_1 = self.moments[0]
        mu_2 = rhs.moments[0]
        delta_2_1 = mu_2 - mu_1

        # M1 (moments[0]) -- x-bar (average)
        mu_new = mu_1 + n_2 * delta_2_1 / n_new

        # M2 (moments[1]) -- variance
        m2_new = self.moments[1] + rhs.moments[1] + n_1 * n_2 * delta_2_1 * delta_2_1 / n_new

        # Store the newly generated aggregation values into our storage.
        self.n          = n_new
        self.moments[0] = mu_new
        self.moments[1] = m2_new

        if(self.depth > 2):
            raise BadAggregation

    def remove(self,value):
        """remove a value from the aggregated statistics
        """
        pass

    def statistics(self,calculateDeviation=False):
        """generate and return the descriptive statistic of the current
           aggregation
        """
        result = deepcopy(self.moments)
        if self.depth <= 1:
            return(result)

        result[1] /= self.n
        if calculateDeviation:
            result[1] = np.sqrt(result[1])
        if self.depth == 2:
            return(result)

        # @TODO: handle heterogeneous deviations.
        deviation = np.sqrt(result[1])
        if deviation.any() == 0:
            # @TODO: check that we don't need to explicitly set the
            #        higher moments to zero.
            return(result)

        result[2] /= (self.n * deviation * deviation * deviation)
        if self.depth == 3:
            return(result)

        result[3] *= self.n / (self.moments[1] * self.moments[1])
        result[3] -= 3.0

        return(result)

