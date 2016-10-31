pebaystats
----------

To create an accumulator, do the following:

    >>> import pebaystats
    >>> accumulator = pebaystats()

Add data values to the accumulator:

    >>> accumulator.add(24.5)
    >>> accumulator.add([24.5,23.4,65])

Remove data values from the accumulator:

    >>> accumulator.remove(24.5)
    >>> accumulator.add([24.5,65])

Extract the descriptive statistics from the accumulator:

    >>> accumulator.statistics(True)

