# -*- coding: utf-8 -*-
#
# Output processor for `cmake`
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
#

from ..processing import Processor as ProcessorBase
from ..term import move_above, get_size

import os
import re
import shlex


_SUCCESS_RE = re.compile('^-- (Check|Looking|Performing Test|Detecting).*-{1,2} (works|done|yes|found|Success)$')
_SUCCESS2_RE = re.compile('^-- Found .*:\s.*$')
_FAILURE_RE = re.compile('^-- .* - (not found|Failed)$')
_FATAL_RE = re.compile('^CMake Error.*')


class Processor(ProcessorBase):

    def __init__(self, config, binary):
        super().__init__(config, binary)
        self.success = config.get_color('success-test', 'green+bold')
        self.failure = config.get_color('fail-test', 'red+bold')
        self.fatal = config.get_color('fatal-error', 'red+bold')
        self.relaxed = config.get_bool('dash-dash-is-cmake', True)
        self.prev_line = None


    def _colorize(self, color, line):
        return color + line + self.config.color.reset


    def looks_like_cmake_line(self, line):
        return self.relaxed and line.startswith('-- ') \
          or _SUCCESS_RE.match(line) \
          or _SUCCESS2_RE.match(line)  \
          or _FAILURE_RE.match(line)   \
          or _FATAL_RE.match(line)


    def handle_line(self, line):
        move_code = ''
        if self.prev_line is not None and line.startswith(self.prev_line):
            # The line above is a begining of some test and here (in the `line`) a result of it
            # Move cursor to one line up and override it!
            lines = int(len(self.prev_line) / get_size()[1])
            move_code = move_above(lines)
        self.prev_line = line.strip()
        if _SUCCESS_RE.match(line) or _SUCCESS2_RE.match(line):
            return self._colorize(move_code + self.success, line)
        if _FAILURE_RE.match(line):
            return self._colorize(move_code + self.failure, line)
        if _FATAL_RE.match(line):
            return self._colorize(move_code + self.fatal, line)
        return line
