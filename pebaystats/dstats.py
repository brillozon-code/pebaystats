"""low complexity descriptive statistics 
"""
from __future__ import print_function

import numpy as np
from copy import deepcopy

class ExcessiveMoments(Exception):
    """Unsupported moment generation attempt.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value).replace("\\n", "\n")

class UnsupportedMethod(Exception):
    """Unsupported method.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value).replace("\\n", "\n")

class dstats(object):
    """implement Pebay's reduced complexity descriptive statistical moments

    Members
        :max_moment:  largest statistical moment to be calculated
        :n:           number of elements over which moments are calculated
        :moments:     list of current moment values

    .. todo:: add covariance calculations
    .. todo:: extend to general formulas
    """

    def __init__(self,max_moment=4,width=1):
        """return a new descriptive statistics accumulator
        """
        self.n       = 0
        self.moments = np.zeros((max_moment,width),dtype=np.float64)

    def __repr__(self):
        shape = self.moments.shape
        return("dstats(n=%d,moments=\n%s)" % (
                   self.n,self.moments))

    def __str__(self):
        shape = self.moments.shape
        return("dstats: %d moments, %d columns, %d rows\n%s" % (
                   shape[0],shape[1],self.n,self.moments))

    def __get_state__(self):
        """support for serialization

            :returns:  dictionary with internal state values
        """
        return {
            "n":       self.n,
            "moments": self.moments
        }

    def __set_state__(self,value):
        """support for deserialization

            Arguments
                :value: new state to set into the instance
        """
        if value is None:
            return
        self.n       = value.get("n",0)
        self.moments = value.get("moments",np.zeros((4,1),dtype=np.float64))

    def add(self,value):
        """add a (single) new value to each column of the aggregated statistics

            Arguments
                :value: row of data values to aggregate (numpy array of values)

        .. todo:: handle multiple rows for value
        """

        # Adjust the number of values in the data set.
        self.n += 1
        size    = self.n

        # Allow empty moments to simply count data elements.
        if self.moments.ndim == 0 or self.moments.shape[0] == 0:
            return

        # How much to calculate.
        shape = self.moments.shape
        depth = shape[0]

        # Get ready to calculate.
        delta        = value - self.moments[0]
        delta_over_n = delta / size

        if depth > 1:
            delta_delta_over_n = delta_over_n * delta

            # M2
            term2 = delta_delta_over_n * (size - 1.0)

            if depth > 2:
                M2 = self.moments[1]
                delta_delta_delta_over_n_n = delta_delta_over_n * delta_over_n

                # M3
                term3 = (delta_delta_delta_over_n_n
                            * (size - 1.0) * (size - 2.0)
                            - 3.0 * delta_over_n * M2)

                if depth > 3:
                    M3 = self.moments[2]

                    # M4
                    term4 = (delta_over_n * delta_delta_delta_over_n_n
                                * (size - 1.0) * (size * size - 3.0 * size + 3.0)
                                + 6.0 * delta_over_n * delta_over_n * M2
                                - 4.0 * delta_over_n * M3)

        # M1
        self.moments[0] += delta_over_n
        if depth == 1:
            return

        # M2
        self.moments[1] += term2
        if depth == 2:
            return

        # M3
        self.moments[2] += term3
        if depth == 3:
            return

        # M4
        self.moments[3] += term4
        if depth == 4:
            return

        # Supported depth exceeded.
        raise ExcessiveMoments('unsupported moments %d > 4' % self.moments.shape[0])

    def aggregate(self,rhs):
        """aggregate two dstat objects to hold the combined statistical moment values

            Arguments
                :rhs: the other accumulator object to be aggregated

        .. todo:: determine why the kurtosis accuracy is degraded for aggregation.
        """
        if rhs.n is None or rhs.n == 0:
            return
        if self.n == 0:
            self.n       = rhs.n
            self.moments = rhs.moments
            return

        # How much to calculate.
        shape = self.moments.shape
        depth = shape[0]

        n_1   = self.n
        n_2   = rhs.n
        n_new = n_1 + n_2

        # Update new value of M0.
        self.n = n_new

        mu_1  = self.moments[0]
        mu_2  = rhs.moments[0]
        delta_2_1 = mu_2 - mu_1

        # M1 (moments[0]) -- x-bar (average)
        self.moments[0] = mu_1 + n_2 * delta_2_1 / n_new

        if depth == 1:
            return

        # M2 (moments[1]) -- variance
        m2_1 = deepcopy(self.moments[1])
        m2_2 = rhs.moments[1]
        delta_2_1_up2 = delta_2_1 * delta_2_1

        self.moments[1] = m2_1 + m2_2 + n_1 * n_2 * delta_2_1_up2 / n_new

        if depth == 2:
            return

        # M3 (moments[2]) -- skew
        m3_1 = deepcopy(self.moments[2])
        m3_2 = rhs.moments[2]
        n_new_up2 = n_new * n_new
        n1_n2_n12 = n_1 * n_2 * (n_1 - n_2)
        delta_2_1_up3 = delta_2_1_up2 * delta_2_1

        self.moments[2] = m3_1 + m3_2 + \
            n1_n2_n12 * delta_2_1_up3 / n_new_up2 + \
            3 * (n_1 * m2_2 - n_2 * m2_1) * delta_2_1 / n_new

        if depth == 3:
            return

        # M4 (moments[3]) -- kurtosis
        m4_1 = self.moments[3]
        m4_2 = rhs.moments[3]
        delta_2_1_up4 = delta_2_1_up3 * delta_2_1

        self.moments[3] = m4_1 + m4_2 + \
            n1_n2_n12 * (n_1 - n_2) * delta_2_1_up4 / (n_new_up2 * n_new) + \
            6 * (n_1 * n_1 * m2_2 + n_2 * n_2 * m2_1) * delta_2_1_up2 / n_new_up2 + \
            4 * (n_1 * m3_2 - n_2 * m3_1) * delta_2_1 / n_new

        if depth == 4:
            return

        # Supported depth exceeded.
        raise ExcessiveMoments('unsupported moments %d > 4' % self.moments.shape[0])

    def remove(self,value):
        """remove a value from the aggregated statistics

            Arguments
                :value: value to be removed from the accumulated data elements

        .. todo:: implement remove method
        """
        raise UnsupportedMethod('Method remove() is not implemented')

    def statistics(self,calculateDeviation=False):
        """generate and return the descriptive statistic of the current
           aggregation

            Arguments
                :calculateDeviation: boolean flag that indicates whether the second
                                     result is the variance or deviation

            :return: array of the descriptive statistics (numpy array of float64)
        """
        result = deepcopy(self.moments)
        depth  = self.moments.shape[0]
        if depth <= 1:
            return(result)

        if self.n == 0:
            return(result)

        result[1] /= self.n
        if calculateDeviation:
            result[1] = np.sqrt(result[1])
        if depth == 2:
            return(result)

        if calculateDeviation:
            deviation = result[1]
        else:
            deviation = np.sqrt(result[1])

        mask = (self.moments[1] != 0)
        maskedDeviation = deviation[mask]
        result[2][ mask] /= (self.n * maskedDeviation * maskedDeviation * maskedDeviation)
        result[2][~mask]  = np.nan
        if depth == 3:
            return(result)

        maskedNvar = self.moments[1][mask]
        result[3][ mask] *= self.n / (maskedNvar * maskedNvar)
        result[3][ mask] -= 3.0
        result[3][~mask]  = np.nan
        if depth == 4:
            return(result)

        # Supported depth exceeded.
        raise ExcessiveMoments('unsupported moments %d > 4' % self.moments.shape[0])

