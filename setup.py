
from setuptools import setup

import pebaystats

def readme():
    with open('README.rst') as f:
        return(f.read())

def history():
    with open('HISTORY.rst') as f:
        return(f.read())

def reqs():
    with open('requirements.txt') as f:
        return([ l.strip() for l in f.readlines() ])

long_desc = readme() + '\n\n' + history().replace('.. :changelog:', '')

requirements = reqs()

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
      tests_require=['nose', 'nose-cover3', 'scipy'],
      zip_safe=False)

