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

import os
import pathlib
import re
import termcolor


class Config:
    ''' Simple configuration data accessor

        Every plugin may (and actually is) have a configuration data stored
        in a simple text file at ${prefix}/etc/outproc/.
        This class can read and give an access to that data in a easy to use way.
    '''

    # TODO Use gamed groups
    _RGB_COLOR_SPEC_RE = re.compile('rgb\s*\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)')
    _RGB_HEX_COLOR_SPEC_RE = re.compile('rgb\s*\(\s*([0-9]{6})\s*\)')
    _GRAYSCALE_SPEC_RE = re.compile('gray\s*\(\s*([0-9]+)\s*\)')

    def __init__(self, filename):
        ''' Read configuration data from a given file '''

        assert isinstance(filename, pathlib.Path)

        # Remember filename for future references (to show errors)
        self.filename = filename
        # Make an empty dict for configuration data
        self.data = {}

        # Set some predefined values
        # TODO Replace w/ `enum`
        class dummy:
            pass
        self.color = dummy
        setattr(self.color, 'normal', '\x1b[38m')
        setattr(self.color, 'normal_bg', '\x1b[48m')
        setattr(self.color, 'reset', termcolor.RESET)

        # NOTE Konsole terminal from KDE supports itallic font style
        termcolor.ATTRIBUTES['itallic'] = 3

        if not filename.exists():
            return

        # Read the file line by line, and collect keys and values into an internal dict
        # TODO Use configparser
        with filename.open() as ifs:
            for l in ifs.readlines():
                # Strip possible comment lines
                line_str = l.strip()
                if not line_str or line_str.startswith('#'):
                    continue
                # Split by first '=' char
                key, value = [item.strip() for item in line_str.split('=', 1)]
                # TODO Check for duplicate keys?
                self.data[key] = value


    def get_string(self, key, default=None):
        ''' Get string key value or default if absent '''
        assert isinstance(key, str)
        assert isinstance(default, str) or default is None

        return self.data[key] if key in self.data else default


    def get_int(self, key, default=None):
        ''' Get int key value or default if absent.
            Throw ValueError if not an integer.
        '''
        assert isinstance(key, str)
        assert isinstance(default, int) or default is None

        try:
            return int(self.data[key]) if key in self.data else default
        except:
            raise ValueError(
                'Invalid value of key `{}`: expected integer, got "{}" [{}]'.
                format(key, self.data[key], self.filename)
              )


    def get_bool(self, key, default=None):
        ''' Get int key value or default if absent.
            Throw ValueError if not an integer.
        '''
        assert isinstance(key, str)
        assert isinstance(default, bool) or default is None

        if key in self.data:
            value = self.data[key]
            if value == 'true' or value == '1':
                return True
            if value == 'false' or value == '0':
                return False
            raise ValueError(
                'Invalid value of key `{}`: expected boolean, got "{}" [{}]'.
                format(key, value, self.filename)
              )
        return default


    def get_color(self, key, default, with_reset=True):
        '''Get color key value or default if absent.
            Throw ValueError if not an integer.
        '''
        assert isinstance(key, str)
        assert isinstance(default, str) or default is not None

        colors = [c.strip() for c in (self.data[key] if key in self.data else default).split('+')]
        result = ''

        # Handle special value 'none' as color inhibitor
        if 'none' in colors:
            return result

        if with_reset:
            result = '\x1b[0m'

        for c in colors:
            #
            result += '\x1b['
            #
            if c == 'reset':
                result += '0'
            elif c == 'normal':
                result += '38'
            elif c in termcolor.COLORS:
                result += str(termcolor.COLORS[c])
            elif c in termcolor.ATTRIBUTES:
                result += str(termcolor.ATTRIBUTES[c])
            elif c in termcolor.HIGHLIGHTS:
                result += str(termcolor.HIGHLIGHTS[c])
            elif self._RGB_COLOR_SPEC_RE.match(c):
                # BUG Fucking Python! Why not to assign and check a variable inside of `if`
                # TODO Avoid double regex match
                match = self._RGB_COLOR_SPEC_RE.search(c)
                try:
                    r = self._validate_rgb_component(int(match.group(1)))
                    g = self._validate_rgb_component(int(match.group(2)))
                    b = self._validate_rgb_component(int(match.group(3)))
                    if r <= 5 and g <= 5 and b <= 5:
                        index = self._rgb_to_index(r, g, b)
                        result += '38;5;' + str(index)
                    else:
                        result += '38;2;{};{};{}'.format(r, g, b)
                except ValueError:
                    raise RuntimeError(
                        'Invalid value of key `{}`: invalid RGB color specification "{}" [{}]'.
                        format(key, c, self.filename)
                      )
            elif self._GRAYSCALE_SPEC_RE.match(c):
                # BUG Fucking Python! Why not to assign and check a variable inside of `if`
                # TODO Avoid double regex match
                match = self._GRAYSCALE_SPEC_RE.search(c)
                try:
                    g = self._validate_grayscale(int(match.group(1)))
                    index = self._grayscale_to_index(g)
                    result += '38;5;' + str(index)
                except ValueError:
                    raise RuntimeError(
                        'Invalid value of key `{}`: invalid grayscale color specification "{}" [{}]'.
                        format(key, c, self.filename)
                      )
            else:
                try:
                    index = int(c)
                    if 15 < index and index < 256:
                        result += '38;5;' + c
                except ValueError:
                    raise RuntimeError(
                        'Invalid value of key `{}`: expected color specification, got "{}" [{}]'.
                        format(key, c, self.filename)
                      )
            # Form the partial result
            result += 'm'
        return result


    def _validate_rgb_component(self, c):
        assert isinstance(c, int)
        if c < 0 or 255 < c:
            raise ValueError('RGB component is out of range')
        return c


    def _rgb_to_index(self, r, g, b):
        return r * 36 + g * 6 + b + 16


    def _validate_grayscale(self, c):
        assert isinstance(c, int)
        if c < 0 or 24 < c:
            raise ValueError('Grayscale index is out of range')
        return c


    def _grayscale_to_index(self, g):
        assert (232 + g) < 256
        return 232 + g
