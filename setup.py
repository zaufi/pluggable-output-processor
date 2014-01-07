#!/usr/bin/env python
#
# Install script for Pluggable Output Processor
#
# Copyright (c) 2013 Alex Turbov <i.zaufi@gmail.com>
#
# Pluggable Output Processor is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pluggable Output Processor is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import codecs

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import outproc


def readfile(filename):
    with codecs.open(filename, encoding='UTF-8') as f:
        return f.read()

setup(
    name             = 'outproc'
  , version          = outproc.__version__
  , description      = 'Pluggable Output Processor'
  , long_description = readfile('README.md')
  , maintainer       = 'Alex Turbov'
  , maintainer_email = 'I.zaufi@gmail.com'
  , url              = 'http://zaufi.github.io/pluggable-output-processor.html'
  , download_url     = 'https://github.com/zaufi/pluggable-output-processor/archive/version-{}.tar.gz'.format(outproc.__version__)
  , packages         = ['outproc', 'outproc.pp']
  , scripts          = ['bin/outproc']
  , data_files       = [
        ('/etc/outproc', ['conf/cmake.conf', 'conf/diff.conf', 'conf/gcc.conf', 'conf/make.conf', 'conf/mount.conf'])
      ]
  , license          = 'GNU General Public License v3 or later (GPLv3+)'
  , classifiers      = [
        'Development Status :: 4 - Beta'
      , 'Environment :: Console'
      , 'Intended Audience :: Developers'
      , 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
      , 'Natural Language :: English'
      , 'Operating System :: POSIX :: Linux'
      , 'Programming Language :: Python :: 3'
      , 'Topic :: Utilities'
      ]
  , install_requires = ['argparse', 'setuptools', 'termcolor']
  , test_suite       = 'test'
  , tests_require    = ['termcolor']
  )
