#!/usr/bin/env python
import sys
from setuptools import setup

VERSION = '0.0.1'
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
        install_requires=[]
)
