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

