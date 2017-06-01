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
    Unit tests for `make` post-processor gcc command line matching regex
'''

# Project specific imports
from outproc.pp.gcc import _LOCATION_RE

# Standard imports
import pytest


class complier_cli_match_tester:

    @pytest.mark.parametrize(
        'input_line, expected_start, expected_end'
      , [
            ('/work/xxx/xxx-devel/task_manager.cc: In member function', 0, 36)
          , (' from /work/xxx/xxx-devel/task.hh:18,', 6, 37)
          , ('apply_apply.cc:11:27: error: \'zzT\' was not declared in this scope', 0, 21)
          , ('In file included from /work/xxx/xxx-devel/details/pre_task.hh:23:0,', 22, 67)
        ]
      )
    def location_matcher_test(self, input_line, expected_start, expected_end):
        match = _LOCATION_RE.search(input_line)
        assert bool(match)
        assert match.start() == expected_start
        assert match.end() == expected_end
