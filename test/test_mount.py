# -*- coding: utf-8 -*-
#
# This file is a part of Pluggable Output Processor
#
# Copyright (c) 2013-2017 Alex Turbov <i.zaufi@gmail.com>
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

'''
    Unit tests for terminal helpers
'''

# Project specific imports
from context import outproc
from outproc.config import Config
from outproc.pp.mount import Processor

# Standard imports
import pathlib
import sys
import termcolor


class mount_processor_tester:

    def setup_method(self):
        self.config = Config(pathlib.Path('doesnt-matter'))
        self.pp = Processor(self.config, 'mount')


    def long_mounts_list_test(self):
        lines = self.pp.handle_block(b'/dev/sdb2 on / type btrfs (rw,noatime)\n')
        lines = self.pp.eof()

        print('lines={}'.format(repr(lines)))
        #assert 0
