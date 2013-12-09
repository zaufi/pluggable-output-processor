#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Output processor for `diff`
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
#

import os
import outproc
import outproc.term
import re
import sys


class Processor(outproc.Processor):

    @staticmethod
    def want_to_handle_current_command():
        result = False
        if '--color=always' in sys.argv:
            outproc.force_processing()
            del sys.argv[sys.argv.index('--color=always')]
            result = True
        elif sys.stdout.isatty() or outproc.force_processing_requested():
            result = True
        return result


    def __init__(self, config, binary):
        super().__init__(config, binary)
        self.added = config.get_color('added', 'green')
        self.removed = config.get_color('removed', 'red')
        self.address = config.get_color('address', 'cyan')
        self.filename_1 = config.get_color('filename-1', 'red')
        self.filename_2 = config.get_color('filename-2', 'green')


    def _colorize(self, color, line):
        return color + line + self.config.color.reset


    def handle_line(self, line):
        if line.startswith('--- '):
            return self._colorize(self.filename_1, line)
        if line.startswith('+++ '):
            return self._colorize(self.filename_2, line)
        if line.startswith('@@ '):
            return self._colorize(self.address, line)
        if line.startswith('-'):
            return self._colorize(self.removed, line)
        if line.startswith('+'):
            return self._colorize(self.added, line)
        return line
