#!/usr/bin/env python

from distutils.core import setup

setup(name='rccontrol',
      version='0.1',
      description='Python scripts for controlling RC Car',
      author='KONNO Katsuyuki',
      author_email='konno.katsuyuki@nifty.com',
      url='http://github.com/konchan/rccontrol.git',
      py_modules = ['rccontrol', 'servo', 'esc'],
      package_dir = ['': 'src']
     )