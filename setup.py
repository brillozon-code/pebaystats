
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pebaystats',
      version='0.1',
      description='descriptive statistics using Pebay results',
      url='http://github.com/brillozon-code/pebaystats',
      author='brillozon',
      author_email='brillozon@gmail.com',
      license='MIT',
      packages=['pebaystats'],
      install_requires=[
        'numpy'
      ],
      zip_safe=False)

