#!/usr/bin/env python

from distutils.core import setup

setup(name='binparse',
      version='1.1',
      description='Python bin struct parser',
      author='Geir Skjotskift',
      author_email='geir@underworld.no',
      py_modules=['binparse'],
      scripts=['example/crashdump64.py',],
      classifiers=[
	  'Development Status :: 4 - Beta',
	  'Intended Audience :: Developers',
	  "License :: OSI Approved :: ISC License (ISCL)",
	  'Programming Language :: Python',
	  ]
     )

