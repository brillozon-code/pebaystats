
from setuptools import setup

import pebaystats

import pkg_resources
try:
        release = pkg_resources.get_distribution('pebaystats').version
except pkg_resources.DistributionNotFound:
        print 'To build the documentation, The distribution information of sandman'
        print 'Has to be available.  Either install the package into your'
        print 'development environment or run "setup.py develop" to setup the'
        print 'metadata.  A virtualenv is recommended!'
        sys.exit(1)
del pkg_resources

version = '.'.join(release.split('.')[:2])

def readme():
    with open('README.rst') as f:
        return f.read()

def history():
    with open('HISTORY.rst') as f:
        return f.read()

long_desc = readme() + '\n\n' + history().replace('.. :changelog:', '')

requirements = [ l.strip() for l in open('requirements.txt').readlines() ]

setup(name='pebaystats',
      # version='0.1',
      # version=version,
      version=pebaystats.__version__,
      description='descriptive statistics using Pebay results',
      long_description=long_desc,
      url='http://github.com/brillozon-code/pebaystats',
      download_url='https://github.com/brillozon-code/pebaystats/archive/0.1.tar.gz',
      author='Mike Martinez',
      author_email='brillozon@gmail.com',
      license='Apache License 2.0',
      classifiers = [
          "Intended Audience :: Science/Research",
          "Programming Language :: Python :: 2.7",
          "Topic :: Scientific/Engineering :: Mathematics"
          ],
      packages=['pebaystats'],
      install_requires=requirements,
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      zip_safe=False)

