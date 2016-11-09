from __future__ import print_function

import numpy as np
from pebaystats import pebaystats

def test_single_value():
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

test_single_value()


def test_aggregation():
    pstats = pebaystats.pebaystats(2,3)
    pstats.add(np.array([10,20,30]))
    pstats.add(np.array([10,20,30]))
    pstats.add(np.array([10,20,30]))
    pstats.add(np.array([10,20,30]))
    pstats.add(np.array([10,20,30]))
    print('lhs is: %s' % pstats.statistics(True))

    rhs = pebaystats.pebaystats(2,3)
    rhs.add(np.array([20,40,60]))
    rhs.add(np.array([20,40,60]))
    rhs.add(np.array([20,40,60]))
    rhs.add(np.array([20,40,60]))
    rhs.add(np.array([20,40,60]))
    print('rhs is: %s' % rhs.statistics(True))

    pstats.aggregate(rhs)
    print('stats are: %s' % pstats.statistics(True))

def guan_test():
    np.random.seed(0)

    # Test data
    test_arr = np.random.random((10,100))

    print('Test data has shape: %d, %d' % test_arr.shape)

    ### Expected intermediate output
    mid_mean = np.mean(test_arr,axis = 1)
    mid_var  = np.var(test_arr, axis = 1)

    ### Expected final output
    final_mean = np.mean(test_arr)
    final_var  = np.var(test_arr)

    statsobjects = [ pebaystats.pebaystats(2,1) for i in range(0,10) ]
    discard = [ statsobjects[i].add(test_arr[i,j]) 
                for j in range(0,100)
                for i in range(0,10) ]

    print('\nIntermediate Results\n')
    for i in range(0,10):
        values = statsobjects[i].statistics()
        print('Result %d mean: %11g, variance: %11g (M2/N: %11g/%d)' %(i,values[0],values[1],statsobjects[i].moments[1],statsobjects[i].n))
        print('Expected mean: %11g, variance: %11g' %(mid_mean[i],mid_var[i]))

    discard = [ statsobjects[0].aggregate(statsobjects[i]) for i in range(1,10) ]

    values = statsobjects[0].statistics()
    print('\nAggregated Results\n')
    print('Result   mean: %11g, variance: %11g' %(values[0],values[1]))
    print('Expected mean: %11g, variance: %11g' %(final_mean,final_var))

test_single_value()
test_aggregation()
guan_test()

