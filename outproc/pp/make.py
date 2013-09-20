#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Output processor for `make`
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

import re
import outproc

_MAKE_MGS_RE = re.compile('make(\[[0-9]+\])?: ')
_MAKE_ERROR_MSG_RE = re.compile('make(\[[0-9]+\])?: \*\*\*')


class Processor(outproc.Processor):

    def __init__(self, config, binary):
        super().__init__(config, binary)
        self.error = config.get_color('error', 'normal,red,itallic')
        self.misc = config.get_color('misc', 'grey,bold')


    def _detect_make_message(self, line):
        if _MAKE_ERROR_MSG_RE.match(line):
            return (True, True)
        elif _MAKE_MGS_RE.match(line):
            return (True, False)
        return (False, False)


    def _colorize_with_misc(self, line):
        return self.misc + line + self.config.normal_color


    def handle_line(self, line):
        is_make_message, is_error_message = self._detect_make_message(line)
        if is_make_message:
            line = self.misc + line
            if is_error_message:
                stars_idx = line.index('***')
                line = line[:stars_idx] + self.error + line[stars_idx:]
            line += self.config.reset_color
        elif line.startswith('/usr/bin/cmake'):
            return self._colorize_with_misc(line)

        return line
