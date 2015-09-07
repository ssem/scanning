#!/usr/bin/env python
from distutils.core import setup

setup(name="slowscan",
      version="alpha",
      author="ssem",
      scripts=["bin/create_ranges",
               "bin/slowscan"],
      packages=["slowscan"],)
