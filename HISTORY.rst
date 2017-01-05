.. :changelog:

History
-------

0.1 (2016-11-13)
-------------------------------
* First release on PyPI

0.2 (2016-11-13)
-------------------------------
* Corrected some setup configuration issues

0.3 (2016-11-14)
-------------------------------
* Added support and tests for serialization

0.4 (2017-1-4)
-------------------------------
* Added repl() and str() support
* Added exceptions for unsupported methods and unsupported moments
* Handle divide by zero on a per column basis
* Improved setup processing

* Extended testing
   - started migrating to factored test dependencies
   - test columns with 0 variance
   - added SciPy for evaluating expected skew and kurtosis values
   - raise exceptions for unsupported moments

* Extensive documentation updates
   - added Makefile to generate documentation and create README
   - removed optional files
   - changed to classic theme
   - extended content and examples


