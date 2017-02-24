#!/usr/bin/env python

from distutils.core import setup

setup(name='binparse',
      version='1.0',
      description='Python bin struct parser',
      author='Geir Skjotskift',
      author_email='geir@underworld.no',
      py_modules=['binparse'],
      scripts=['example/crashdump64.py',],
     )
