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

import distutils.core
import sys

distutils.core.setup(
    name             = 'outproc'
  , version          = '0.1'
  , description      = 'Pluggable Output Processor'
  , maintainer       = 'Alex Turbov'
  , maintainer_email = 'I.zaufi@gmail.com'
  , url              = 'https://github.com/zaufi/pluggable-output-processor'
  , packages         = ['outproc', 'outproc.pp']
  , scripts          = ['bin/outproc']
  , data_files       = [('/etc/outproc', ['conf/cmake.conf', 'conf/gcc.conf', 'conf/make.conf'])]
  , license          = 'GPL-3'
  , classifiers      = [
        'Development Status :: 4 - Beta'
      , 'Environment :: Console'
      , 'Intended Audience :: Developers'
      , 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
      , 'Natural Language :: English'
      , 'Operating System :: POSIX :: Linux'
      , 'Programming Language :: Python'
      , 'Programming Language :: Python :: 3'
      , 'Topic :: Utilities'
      ]
  )
