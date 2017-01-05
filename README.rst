
Information about repository and package maintenance actions can be found
on the `Wiki <https://github.com/brillozon-code/pebaystats/wiki>`_.

Install the package from PyPI using pip:

    bash> pip install pebaystats

pebaystats
----------

Provides a single pass generation of statistical moments.  This package is based on the formulas described in the document
`Formulas for Robust, One-Pass Parallel Computation of Covariances and Arbitrary-Order Statistical Moments, Phillipe Pébay, Sandia National Laboratories <http://infoserve.sandia.gov/sand_doc/2008/086212.pdf>`_

Read `"The Full Manual" <http://pebaystats.readthedocs.io/en/latest/>`_ for a more detailed description of this package.

The current implementation of this package allows computation of
statistical moments for more than one data set (column) at a time.
Currently only the first four moments are computed and the general
purpose algorithm from the source paper is not yet implemented.

.. note::
    The aggregation of kurtosis values appears to suffer some loss of
    accuracy when compared with the SciPy generated values.  This does
    not occur when accumulating simple data values, and the cause is not
    currently known.  I suspect this is an arithmetic precision effect,
    but have not investigated.

This Python implementation evolved from my C++ code which includes the
ability to remove/disaggregate data from the accumulators as well.  That
feature will eventually be migrated here.


Quick Start
===========

.. code:: python

    from __future__ import print_function

Import the aggregation object from the module.

.. code:: python

    from pebaystats import dstats

Create a few objects with various depths (number of moments) and widths
(number of columns to compute statistics for). Here the ``stats1`` and
``stats3`` objects each accumulate two moments for a single column of
data, and the ``stats2`` object collects 4 statistical moments for 4
columns of data.

.. code:: python

    stats1 = dstats(2,1)
    stats2 = dstats(4,4)
    stats3 = dstats(2,1)

Add individual data values to the single column accumulation of the
``stats1`` object. Print the object to view its state, which includes
the moment values so far accumulated. Also, print the list of lists
returned from the ``statistics()`` method call. Here you can see that
the mean is 2.0 and the variance is 0.0.

.. code:: python

    stats1.add(2)
    stats1.add(2)
    stats1.add(2)
    print('stats1: %s' % stats1)
    print('statistics: %s' % stats1.statistics())


.. parsed-literal::

    stats1: dstats: 2 moments, 1 columns, 3 rows
    [[ 2.]
     [ 0.]]
    statistics: [[ 2.]
     [ 0.]]


--------------

Add entire rows (multiple columns) of values to the ``stats2`` object.
View the accumulated results. Note that when the second moment
(``n * Var``) is 0, equivalent to a deviation of 0, the higher moments
are left in there initial 0 state. The higher statistics are set to a
``NaN`` value in this case.

.. code:: python

    stats2.add([1.2,2,3,9])
    stats2.add([4.5,6,7,9])
    stats2.add([8.9,0,1,9])
    stats2.add([2.3,4,5,9])
    print('stats2: %s' % stats2)
    print('statistics: %s' % stats2.statistics(True))


.. parsed-literal::

    stats2: dstats: 4 moments, 4 columns, 4 rows
    [[  4.22500000e+00   3.00000000e+00   4.00000000e+00   9.00000000e+00]
     [  3.47875000e+01   2.00000000e+01   2.00000000e+01   0.00000000e+00]
     [  6.73818750e+01   7.10542736e-15   7.10542736e-15   0.00000000e+00]
     [  5.75139658e+02   1.64000000e+02   1.64000000e+02   0.00000000e+00]]
    statistics: [[  4.22500000e+00   3.00000000e+00   4.00000000e+00   9.00000000e+00]
     [  2.94904646e+00   2.23606798e+00   2.23606798e+00   0.00000000e+00]
     [  6.56807734e-01   1.58882186e-16   1.58882186e-16              nan]
     [ -1.09897921e+00  -1.36000000e+00  -1.36000000e+00              nan]]


--------------

Remove data (*UNIMPLEMENTED*) from the ``stats2`` object.

.. code:: python

    # stats2.remove(1.2,2,3,9)

--------------

Load the ``stats3`` object with with data and view the results.

.. code:: python

    stats3.add(4)
    stats3.add(4)
    stats3.add(4)
    print('stats3: %s' % stats3)
    print('statistics: %s' % stats3.statistics())


.. parsed-literal::

    stats3: dstats: 2 moments, 1 columns, 3 rows
    [[ 4.]
     [ 0.]]
    statistics: [[ 4.]
     [ 0.]]


Now aggregate that object onto the first. This only works when the
shapes are the same.

.. code:: python

    stats1.aggregate(stats3)
    print('stast1: %s' % stats1)
    print('statistics: %s' % stats1.statistics(True))


.. parsed-literal::

    stast1: dstats: 2 moments, 1 columns, 6 rows
    [[ 3.]
     [ 6.]]
    statistics: [[ 3.]
     [ 1.]]

