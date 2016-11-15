
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
    def test_small_all(self):
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

    def test_aggregation_all(self):
        depth = 2
        cols  = 3
        lhs = dstats(depth,cols)
        lhs.add(np.array([10,20,30]))
        lhs.add(np.array([10,20,30]))
        lhs.add(np.array([10,20,30]))
        lhs.add(np.array([10,20,30]))
        lhs.add(np.array([10,20,30]))
        print('lhs is: %s' % lhs.statistics(True))

        rhs = dstats(2,3)
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

        nt.assert_equal(stats.shape[0], depth)
        nt.assert_equal(stats.shape[1], cols)

        nt.assert_almost_equal(stats[0,0], 15, places = 14)
        nt.assert_almost_equal(stats[0,1], 30, places = 14)
        nt.assert_almost_equal(stats[0,2], 45, places = 14)

        nt.assert_almost_equal(stats[1,0],  5, places = 14)
        nt.assert_almost_equal(stats[1,1], 10, places = 14)
        nt.assert_almost_equal(stats[1,2], 15, places = 14)

    def test_aggregation_large(self):
        np.random.seed(0)

        ### Random data size
        rows =  10
        cols = 100

        ### Each accumulators size
        depth = 2
        width = 1

        ### Test data -- 10 rows of 100 columns each
        test_arr = np.random.random((rows,cols))

        print('Test data has shape: %d, %d' % test_arr.shape)

        ### Expected intermediate output
        mid_mean = np.mean(test_arr,axis = 1)
        mid_var  = np.var(test_arr, axis = 1)

        ### Expected final output
        final_mean = np.mean(test_arr)
        final_var  = np.var(test_arr)

        ### Create an object for each row and accumulate the data in that row
        statsobjects = [ dstats(depth,width) for i in range(0,rows) ]
        discard = [ statsobjects[i].add(test_arr[i,j]) 
                    for j in range(0,cols)
                    for i in range(0,rows)]

        print('\nIntermediate Results\n')
        for i in range(0,rows):
            values = statsobjects[i].statistics()
            print('Result %d mean: %11g, variance: %11g (M2/N: %11g/%d)' %(i,values[0],values[1],statsobjects[i].moments[1],statsobjects[i].n))
            print('Expected mean: %11g, variance: %11g' %(mid_mean[i],mid_var[i]))
            nt.assert_almost_equal(values[0], mid_mean[i], places = 14)
            nt.assert_almost_equal(values[1],  mid_var[i], places = 14)

        ### Aggregate result into the index 0 accumulator
        discard = [ statsobjects[0].aggregate(statsobjects[i]) for i in range(1,rows) ]

        values = statsobjects[0].statistics()
        print('\nAggregated Results\n')
        print('Result   mean: %11g, variance: %11g' %(values[0],values[1]))
        print('Expected mean: %11g, variance: %11g' %(final_mean,final_var))
        nt.assert_almost_equal(values[0], final_mean, places = 14)
        nt.assert_almost_equal(values[1],  final_var, places = 14)

    def test_serdes(self):
        ds = dstats(4,9)
        dstr = pickle.dumps(ds)
        nt.assert_greater(len(dstr),100)
        print('\nserialized empty dstats to length: %s' % len(dstr))

        ds2 = pickle.loads(dstr)
        ds2_stats = ds2.statistics()
        print('\nserialized statistics:\n %s' % ds2_stats)
        discard = [ nt.assert_equals(ds2_stats[0][i],0)       for i in range(0,len(ds2_stats[0])) ]
        discard = [ nt.assert_true(np.isnan(ds2_stats[i][j])) for i in range(1,ds2.depth) for j in range(0,ds2.width) ]

        ds2.add([1,2,3,4,10,6,7,8,9])
        ds2.add([9,8,7,6, 0,4,3,2,1])
        ds2_stats = ds2.statistics()
        print('\nserialized statistics:\n %s' % ds2_stats)
        discard = [ nt.assert_equals(ds2_stats[0][i],5) for i in range(0,len(ds2_stats[0])) ]
        discard = [ nt.assert_equals(ds2_stats[1][i],[16,9,4,1,25,1,4,9,16][i]) for i in range(0,len(ds2_stats[1])) ]
        discard = [ nt.assert_equals(ds2_stats[2][i],0)  for i in range(0,len(ds2_stats[2])) ]
        discard = [ nt.assert_equals(ds2_stats[3][i],-2) for i in range(0,len(ds2_stats[3])) ]

        dstr2 = pickle.dumps(ds2)
        nt.assert_greater(len(dstr2),100)
        print('\nserialized empty dstats to length: %s' % len(dstr2))

        ds3 = pickle.loads(dstr2)
        ds3_stats = ds3.statistics()
        print('\nserialized statistics:\n %s' % ds3_stats)
        discard = [ nt.assert_equals(ds3_stats[0][i],5) for i in range(0,len(ds3_stats[0])) ]
        discard = [ nt.assert_equals(ds3_stats[1][i],[16,9,4,1,25,1,4,9,16][i]) for i in range(0,len(ds3_stats[1])) ]
        discard = [ nt.assert_equals(ds3_stats[2][i],0)  for i in range(0,len(ds3_stats[2])) ]
        discard = [ nt.assert_equals(ds3_stats[3][i],-2) for i in range(0,len(ds3_stats[3])) ]

    def test_state(self):
        source = dstats(4,2)
        state  = source.__get_state__()
        source_stats = source.statistics()
        print('source stats:\n%s' % source_stats)
        discard = [ nt.assert_equals(source_stats[0][i],0) for i in range(0,len(source_stats[0])) ]
        discard = [ nt.assert_true(np.isnan(source_stats[i][j]))
                        for i in range(1,source.depth)
                        for j in range(0,source.width) ]

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
                        for i in range(0,source.depth)
                        for j in range(0,source.width) ]


