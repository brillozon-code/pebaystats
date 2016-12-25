=======
Usage
=======

To use the statistical accumulators in a project, first import the
statistical accumulator object and instantiate it.  Then add and
aggregate data into it.  Examine the contents at any time::

        from pebaystats import dstats

        value = dstats()
        value.add(1)
        value.add(2)
        value.add(3)
        result = value.statistics()

