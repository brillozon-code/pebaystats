
import unittest   as ut
import nose.tools as nt

import numpy as np
import pickle
from scipy import stats
from copy  import deepcopy

from context import pebaystats
from pebaystats import dstats

class StatsTest(ut.TestCase):
    def test_small_all(self):
        print('\n\n  *** test_small_all ***\n')
        depth = 4
        cols  = 3
        pstats = dstats(depth,cols)

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

        stats = pstats.statistics(True)
        for moment in range(0,depth):
            for col in range(0,cols):
                print('col: %d, moment: %d, value: %22.15g' %
                      (col,moment+1,stats[moment,col]))

        nt.assert_equal(stats.shape[0], depth)
        nt.assert_equal(stats.shape[1], cols)

        nt.assert_almost_equal(stats[0,0], 15, places = 14)
        nt.assert_almost_equal(stats[0,1], 30, places = 14)
        nt.assert_almost_equal(stats[0,2], 45, places = 14)

        nt.assert_almost_equal(stats[1,0],  5, places = 14)
        nt.assert_almost_equal(stats[1,1], 10, places = 14)
        nt.assert_almost_equal(stats[1,2], 15, places = 14)

        nt.assert_almost_equal(stats[2,0],  1.27105748646260e-15, places = 14)
        nt.assert_almost_equal(stats[2,1],  3.59509347182254e-15, places = 14)
        nt.assert_almost_equal(stats[2,2], -1.56553681485797e-15, places = 14)

        nt.assert_almost_equal(stats[3,0], -2, places = 14)
        nt.assert_almost_equal(stats[3,1], -2, places = 14)
        nt.assert_almost_equal(stats[3,2], -2, places = 14)

    def test_no_variance_stats(self):
        print('\n\n  *** test_no_variance_stats ***\n')
        depth = 4
        cols  = 3
        pstats = dstats(depth,cols)

        pstats.add(np.array([10,20,30]))
        pstats.add(np.array([10,20,30]))
        pstats.add(np.array([10,20,30]))
        pstats.add(np.array([10,20,30]))
        pstats.add(np.array([10,20,30]))
        pstats.add(np.array([20,20,60]))
        pstats.add(np.array([20,20,60]))
        pstats.add(np.array([20,20,60]))
        pstats.add(np.array([20,20,60]))
        pstats.add(np.array([20,20,60]))

        stats = pstats.statistics(True)
        for moment in range(0,depth):
            for col in range(0,cols):
                print('col: %d, moment: %d, value: %22.15g' %
                      (col,moment+1,stats[moment,col]))

        nt.assert_equal(stats.shape[0], depth)
        nt.assert_equal(stats.shape[1], cols)

        nt.assert_almost_equal(stats[0,0], 15, places = 14)
        nt.assert_almost_equal(stats[0,1], 20, places = 14)
        nt.assert_almost_equal(stats[0,2], 45, places = 14)

        nt.assert_almost_equal(stats[1,0],  5, places = 14)
        nt.assert_almost_equal(stats[1,1],  0, places = 14)
        nt.assert_almost_equal(stats[1,2], 15, places = 14)

        nt.assert_almost_equal(stats[2,0],  1.27105748646260e-15, places = 14)
        nt.assert_true(np.isnan(stats[2,1]))
        nt.assert_almost_equal(stats[2,2], -1.56553681485797e-15, places = 14)

        nt.assert_almost_equal(stats[3,0], -2, places = 14)
        nt.assert_true(np.isnan(stats[3,1]))
        nt.assert_almost_equal(stats[3,2], -2, places = 14)

    def test_aggregation_all(self):
        print('\n\n  *** test_aggregation_all ***\n')
        depth = 4
        cols  = 3
        lhs = dstats(depth,cols)
        lhs.add(np.array([10,20,30]))
        lhs.add(np.array([10,20,30]))
        lhs.add(np.array([10,20,30]))
        lhs.add(np.array([10,20,30]))
        lhs.add(np.array([10,20,30]))
        print('lhs is: %s' % lhs.statistics(True))

        rhs = dstats(depth,cols)
        rhs.add(np.array([20,40,60]))
        rhs.add(np.array([20,40,60]))
        rhs.add(np.array([20,40,60]))
        rhs.add(np.array([20,40,60]))
        rhs.add(np.array([20,40,60]))
        print('rhs is: %s' % rhs.statistics(True))

        lhs.aggregate(rhs)

        stats = lhs.statistics(True)
        for moment in range(0,depth):
            for col in range(0,cols):
                print('col: %d, moment: %d, value: %22.15g' %
                      (col,moment+1,stats[moment,col]))

        full = dstats(depth,cols)
        full.add(np.array([10,20,30]))
        full.add(np.array([10,20,30]))
        full.add(np.array([10,20,30]))
        full.add(np.array([10,20,30]))
        full.add(np.array([10,20,30]))
        full.add(np.array([20,40,60]))
        full.add(np.array([20,40,60]))
        full.add(np.array([20,40,60]))
        full.add(np.array([20,40,60]))
        full.add(np.array([20,40,60]))
        print('FULL is: %s' % full.statistics(True))

        nt.assert_equal(stats.shape[0], depth)
        nt.assert_equal(stats.shape[1], cols)

        nt.assert_almost_equal(stats[0,0], 15, places = 14)
        nt.assert_almost_equal(stats[0,1], 30, places = 14)
        nt.assert_almost_equal(stats[0,2], 45, places = 14)

        nt.assert_almost_equal(stats[1,0],  5, places = 14)
        nt.assert_almost_equal(stats[1,1], 10, places = 14)
        nt.assert_almost_equal(stats[1,2], 15, places = 14)

        nt.assert_almost_equal(stats[2,0],  0, places = 14)
        nt.assert_almost_equal(stats[2,1],  0, places = 14)
        nt.assert_almost_equal(stats[2,2],  0, places = 14)

        nt.assert_almost_equal(stats[3,0], -3, places = 14)
        nt.assert_almost_equal(stats[3,1], -3, places = 14)
        nt.assert_almost_equal(stats[3,2], -3, places = 14)

    def test_aggregation_large(self):
        print('\n\n  *** test_aggregation_large ***\n')
        np.random.seed(0)

        ### Random data size
        rows =  10
        cols = 100

        ### Each accumulators size
        depth = 4
        width = 1

        ### Test data -- 10 rows of 100 columns each
        test_arr = np.random.random((rows,cols))

        print('Test data has shape: %d, %d' % test_arr.shape)

        ### Expected intermediate output
        mid_mean = np.mean(test_arr,axis = 1)
        mid_var  = np.var(test_arr, axis = 1)
        mid_skew = stats.skew(test_arr, axis = 1, bias = True)
        mid_kurt = stats.kurtosis(test_arr, axis = 1, bias = True)

        ### Expected final output
        final_mean = np.mean(test_arr)
        final_var  = np.var(test_arr)
        final_skew = stats.skew(test_arr,axis=None,bias=True)
        final_kurt = stats.kurtosis(test_arr,axis=None,fisher=True,bias=False)

        ### Create an object for each row and accumulate the data in that row
        statsobjects = [ dstats(depth,width) for i in range(0,rows) ]
        discard = [ statsobjects[i].add(test_arr[i,j]) 
                    for j in range(0,cols)
                    for i in range(0,rows)]

        print('\nIntermediate Results\n')
        for i in range(0,rows):
            values = statsobjects[i].statistics()
            print('Result %d mean: %11g, variance: %11g, skew: %11g, kurtosis: %11g' % (i,values[0],values[1],values[2],values[3]))
            print('Expected mean: %11g, variance: %11g, skew: %11g, kurtosis: %11g' %(mid_mean[i],mid_var[i],mid_skew[i],mid_kurt[i]))
            nt.assert_almost_equal(values[0], mid_mean[i], places = 14)
            nt.assert_almost_equal(values[1],  mid_var[i], places = 14)
            nt.assert_almost_equal(values[2], mid_skew[i], places = 14)
            nt.assert_almost_equal(values[3], mid_kurt[i], places = 14)

        ### Aggregate just a couple of intermediate results for diagnostic purposes.
        diag_mean = np.mean(test_arr[1:3,],axis=None)
        diag_var  = np.var(test_arr[1:3,],axis=None)
        diag_skew = stats.skew(test_arr[1:3,],axis=None,bias=True)
        diag_kurt = stats.kurtosis(test_arr[1:3,],axis=None,fisher=True,bias=True)

        ### Aggregate result into the index 0 accumulator
        discard = [ statsobjects[0].aggregate(statsobjects[i]) for i in range(1,rows) ]

        values = statsobjects[0].statistics()
        print('\nAggregated Results\n')
        print('Result    mean: %11g, variance: %11g, skew: %11g, kurtosis: %11g' % (values[0],values[1],values[2],values[3]))
        print('Expected  mean: %11g, variance: %11g, skew: %11g, kurtosis: %11g' % (final_mean,final_var,final_skew,final_kurt))
        nt.assert_almost_equal(values[0], final_mean, places = 14)
        nt.assert_almost_equal(values[1],  final_var, places = 14)
        nt.assert_almost_equal(values[2], final_skew, places = 14)
        nt.assert_almost_equal(values[3], final_kurt, places =  5)
        ## @TODO: Determine why the kurtosis accuracy is degraded.

    def test_serdes(self):
        print('\n\n  *** test_serdes ***\n')
        ds = dstats(4,9)
        dstr = pickle.dumps(ds)
        nt.assert_greater(len(dstr),100)
        print('\nserialized empty dstats to length: %s' % len(dstr))

        ds2 = pickle.loads(dstr)
        depth = ds2.moments.shape[0]
        width = ds2.moments.shape[1]

        # N.B. This call raises a RuntimeWarning when generating the
        #      expected NaN values.
        ds2_stats = ds2.statistics()
        print('\ndeserialized empty ds2 statistics:\n %s' % ds2_stats)

        discard = [ nt.assert_equals(ds2_stats[i][j],0) for i in range(0,depth) for j in range(0,width) ]

        ds2.add([1,2,3,4,10,6,7,8,9])
        ds2.add([9,8,7,6, 0,4,3,2,1])
        ds2_stats = ds2.statistics()
        print('\n2 element dstats statistics:\n %s' % ds2_stats)
        discard = [ nt.assert_equals(ds2_stats[0][i],5) for i in range(0,len(ds2_stats[0])) ]
        discard = [ nt.assert_equals(ds2_stats[1][i],[16,9,4,1,25,1,4,9,16][i]) for i in range(0,len(ds2_stats[1])) ]
        discard = [ nt.assert_equals(ds2_stats[2][i],0)  for i in range(0,len(ds2_stats[2])) ]
        discard = [ nt.assert_equals(ds2_stats[3][i],-2) for i in range(0,len(ds2_stats[3])) ]

        dstr2 = pickle.dumps(ds2)
        nt.assert_greater(len(dstr2),100)
        print('\nserialized 2 element dstats to length: %s' % len(dstr2))

        ds3 = pickle.loads(dstr2)
        ds3_stats = ds3.statistics()
        print('\ndeserialized 2 element statistics:\n %s' % ds3_stats)
        discard = [ nt.assert_equals(ds3_stats[0][i],5) for i in range(0,len(ds3_stats[0])) ]
        discard = [ nt.assert_equals(ds3_stats[1][i],[16,9,4,1,25,1,4,9,16][i]) for i in range(0,len(ds3_stats[1])) ]
        discard = [ nt.assert_equals(ds3_stats[2][i],0)  for i in range(0,len(ds3_stats[2])) ]
        discard = [ nt.assert_equals(ds3_stats[3][i],-2) for i in range(0,len(ds3_stats[3])) ]

    def test_state(self):
        print('\n\n  *** test_state ***\n')
        source = dstats(4,2)
        depth  = source.moments.shape[0]
        width  = source.moments.shape[1]
        state  = source.__get_state__()
        source_stats = source.statistics()
        print('source stats:\n%s' % source_stats)
        discard = [ nt.assert_equals(source_stats[i][j],0)
                        for i in range(0,depth)
                        for j in range(0,width) ]

        dest = dstats(1,1)
        dest.__set_state__(state)
        dest_stats = dest.statistics()
        print('dest stats:\n%s' % dest_stats)

        source.add([1,2])
        source.add([2,3])
        source.add([3.4])
        state = source.__get_state__()
        source_stats = source.statistics()
        print('source stats:\n%s' % source_stats)
        dest.__set_state__(state)
        dest_stats = dest.statistics()
        print('dest stats:\n%s' % dest_stats)
        discard = [ nt.assert_equals(source_stats[i][j],dest_stats[i][j])
                        for i in range(0,depth)
                        for j in range(0,width) ]


