pebaystats
----------

This package is based on the formulas described in the document
`Formulas for Robust, One-Pass Parallel Computation of Covariances and Arbitrary-Order Statistical Moments, Phillipe Pébay, Sandia National Laboratories <http://infoserve.sandia.gov/sand_doc/2008/086212.pdf>`_

To create an accumulator, do the following::

    >>>> import pebaystats as pbs
    >>>> stats1 = pbs.dstats(2,1)

    >>>> stats3 = pbs.dstats(4,3)

Add data values to the accumulator::

    >>>> stats1.add(24.5)
    >>>> stats1.add(42)

    >>>> stats3.add([24.5,23.4,65])
    >>>> stats3.add([24.5,23.4,65])
    >>>> stats3.add([25.4,65,23.4])

Remove data values from the accumulator::

    >>>> stats1.remove(24.5)

Extract the descriptive statistics from the accumulator::

    >>>> stats1.statistics(True)
    Data elements accumulated in stats1: 1

    array([[ 42.],
           [  0.]])

    >>>> stats3.statistics(True)
    Data elements accumulated in stats3: 3

    array([[ 24.8       ,  37.26666667,  51.13333333],
           [  0.42426407,  19.61042806,  19.61042806],
           [  0.19540667,  61.40667933, -61.40667933],
           [ -1.5       ,  -1.5       ,  -1.5       ]])

