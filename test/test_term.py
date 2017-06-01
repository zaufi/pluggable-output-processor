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
from outproc.config import Config
from outproc.term import column_formatter, fg2bg, pos_to_offset

# Standard imports
import pathlib


class term_module_tester:

    def setup_method(self):
        self.config = Config(pathlib.Path('doesnt-matter'))
        self.red_fg = self.config.get_color('some', 'red', with_reset=False)
        self.yellow_fg = self.config.get_color('some', 'yellow+bold')
        self.white_fg = self.config.get_color('some', 'white')


    def fg2bg_test(self):
        assert fg2bg(self.red_fg) == '\x1b[41m'


    def pos_to_offset_0_test(self):
        line = 'Hello Africa'
        colored = self.yellow_fg + line + self.config.color.reset
        #print('{}'.format(repr(colored)))

        pos = pos_to_offset(colored, 0)
        assert pos == 13
        assert colored[pos] == 'H'

        pos = pos_to_offset(colored, 6)
        assert pos == 19
        assert colored[pos] == 'A'

        pos = pos_to_offset(colored, len(line) - 1)
        assert pos == 24
        assert colored[pos] == 'a'


    def pos_to_offset_1_test(self):
        line = 'Hello Africa'
        colored = self.white_fg + ' ' + self.yellow_fg + line + self.config.color.reset
        pos = pos_to_offset(colored, 1)
        assert pos == 23
        assert colored[pos] == 'H'


    def bg_highlight_1_test(self):
        self.reg_bg = fg2bg(self.red_fg)
        line = 'Hello Africa'
        line = self.yellow_fg + line + self.config.color.reset

        pos = pos_to_offset(line, 0)
        assert line[pos] == 'H'
        line = line[:pos] + self.reg_bg + line[pos:pos+1] + self.config.color.normal_bg \
          + line[pos+1:]
        assert line == '\x1b[0m\x1b[33m\x1b[1m\x1b[41mH\x1b[48mello Africa\x1b[0m'

        pos = pos_to_offset(line, 6)
        assert line[pos] == 'A'
        line = line[:pos] + self.reg_bg + line[pos:pos+1] + self.config.color.normal_bg \
          + line[pos+1:]
        assert line == '\x1b[0m\x1b[33m\x1b[1m\x1b[41mH\x1b[48mello \x1b[41mA\x1b[48mfrica\x1b[0m'

        pos = pos_to_offset(line, 11)
        assert line[pos] == 'a'
        line = line[:pos] + self.reg_bg + line[pos:pos+1] + self.config.color.normal_bg \
          + line[pos+1:]
        assert line == '\x1b[0m\x1b[33m\x1b[1m\x1b[41mH\x1b[48mello \x1b[41mA\x1b[48mfric\x1b[41ma\x1b[48m\x1b[0m'


    def _format_range_as_to_columns(self, count, columns):
        result = ''
        line = ''
        for i in column_formatter(count, columns):
            if i == -1:
                #print(line)
                result += line + '\n'
                line = ''
            else:
                line += '{} '.format(i)
        return result


    def test_column_formatter_0(self):
        for i in column_formatter(0, 1):
            self.assertFalse()


    def column_formatter_1_2_test(self):
        expected = '0 \n'
        result = self._format_range_as_to_columns(1, 2)
        assert expected == result


    def column_formatter_10_4_test(self):
        expected = '0 3 6 9 \n1 4 7 \n2 5 8 \n'
        result = self._format_range_as_to_columns(10, 4)
        assert expected == result


    def column_formatter_10_3_test(self):
        expected = '0 4 8 \n1 5 9 \n2 6 \n3 7 \n'
        result = self._format_range_as_to_columns(10, 3)
        assert expected == result
