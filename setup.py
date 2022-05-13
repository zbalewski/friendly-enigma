#!/usr/bin/env python
import sys
from setuptools import setup

VERSION = '0.0.2'
DESCRIPTION = "AY250 Final project: ephys processing pipeline."

CLASSIFIERS = list(filter(None, map(str.strip,
"""
Development Status :: 2 - Pre-Alpha
Intended Audience :: Education
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Scientific/Engineering
""".splitlines())))

setup(
        name="ephyspipeZB",
        version=VERSION,
        description=DESCRIPTION,
        long_description=DESCRIPTION,
        long_description_content_type="text/x-rst",
        classifiers=CLASSIFIERS,
        author="Zuzanna Balewski",
        author_email="balewski@berkeley.edu",
        url="https://github.com/zbalewski/friendly-enigma",
        python_requires='>=3',
        license="MIT",
        packages=['ephyspipe', 'ephyspipe.tests'],
        platforms=['any'],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        install_requires=['h5py==3.6.0',
                          'mat73==0.59',
                          'numpy==1.21.6',
                          'pandas==1.3.5',
                          'python-dateutil==2.8.2',
                          'pytz==2022.1',
                          'scipy==1.7.3',
                          'six==1.16.0']
)
