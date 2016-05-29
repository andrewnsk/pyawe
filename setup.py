#!/usr/bin/env python

from setuptools import setup
from pyawe import constants

setup(
    name='pyawe',
    version=constants.PYAWE_VERSION,
    description='A Python wrapper for 2x16 display ',
    author='Andrew Dorokhin',
    author_email='andrewnorilsk@gmail.com',
    url='http://github.com/andrewnsk/pyawe',
    packages=['pyawe', 'tests.unit'],
    long_description="""\
      A Python wrapper for 2x16 display
      """,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    package_data={
        '': ['*.txt']
    },
    keywords='openweathermap Python wrapper for 2x16 display',
    license='MIT',
    test_suite='tests', requires=['pyawe']
)
