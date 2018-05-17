#!/usr/bin/env python
from distutils.core import setup

setup(name="fastscan",
      version="alpha",
      author="ssem",
      scripts=["bin/fastscan"],
      data_files=[("dicts", ["fastscan/dicts/users.txt",
                             "fastscan/dicts/passwords.txt"])],
      packages=["fastscan"],)
