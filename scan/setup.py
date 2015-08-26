#!/usr/bin/env python

from distutils.core import setup

setup(name="scan",
      version="1",
      author="ssem",
      scripts=["bin/create_ranges",
               "bin/scan"],
      packages=["scan"],)
