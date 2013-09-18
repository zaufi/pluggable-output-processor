#!/usr/bin/env python
#
# Install script for `outproc`
#

import distutils.core
import sys

# this affects the names of all the directories we do stuff with
sys.path.insert(0, './')
import chewy

distutils.core.setup(
    name             = 'outproc'
  , version          = '0.1'
  , description      = 'Pluggable Output Processor'
  , maintainer       = 'Alex Turbov'
  , maintainer_email = 'I.zaufi@gmail.com'
  , url              = 'https://github.com/zaufi/pluggable-output-processor'
  , packages         = ['outproc']
  , scripts          = ['bin/outproc']
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
