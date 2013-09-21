#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is a part of Pluggable Output Processor
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

import re
import os
import termcolor


class Config(object):
    ''' Simple configuration data accessor

        Every plugin may (and actually is) have a configuration data stored
        in a simple text file at ${prefix}/etc/outproc/.
        This class can read and give an access to that data in a easy to use way.
    '''

    _RGB_COLOR_SPEC_RE = re.compile('rgb\s*\(\s*([0-5])\s*,\s*([0-5])\s*,\s*([0-5])\s*\)')
    _GRAYSCALE_SPEC_RE = re.compile('gray\s*\(\s*([0-9]+)\s*\)')

    def __init__(self, filename):
        '''Read configuration data from a given file'''

        # Remember filename for future references (to show errors)
        self.filename = filename
        # Make an empty dict for configuration data
        self.data = {}

        # Set some predefined values
        self.normal_color = '\x1b[38m'
        self.reset_color = termcolor.RESET

        # NOTE Konsole terminal from KDE supports itallic font style
        termcolor.ATTRIBUTES['itallic'] = 3

        if not os.path.isfile(filename):
            return

        # Read the file line by line, and collect keys and values into an internal dict
        with open(filename) as ifs:
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
        '''Get string key value or default if absent'''
        assert(isinstance(key, str))
        assert(isinstance(default, str) or default is None)

        return self.data[key] if key in self.data else default


    def get_int(self, key, default=None):
        '''Get int key value or default if absent.
            Throw ValueError if not an integer.
        '''
        assert(isinstance(key, str))
        assert(isinstance(default, int) or default is None)

        try:
            return int(self.data[key]) if key in self.data else default
        except:
            raise ValueError(
                'Invalid value of key `{}`: expected integer, got "{}" [{}]'.
                format(key, self.data[key], self.filename)
              )


    def get_color(self, key, default):
        '''Get color key value or default if absent.
            Throw ValueError if not an integer.
        '''
        assert(isinstance(key, str))
        assert(isinstance(default, str) or default is not None)

        colors = [c.strip() for c in (self.data[key] if key in self.data else default).split('+')]
        result = ''

        # Handle special value 'none' as color inhibitor
        if 'none' in colors:
            return result

        need_reset = True
        for c in colors:
            if c == 'reset':
                result += ';0'
                need_reset = False
            elif c == 'normal':
                result += ';38'
            elif c in termcolor.COLORS:
                result += ';' + str(termcolor.COLORS[c])
            elif c in termcolor.ATTRIBUTES:
                result += ';' + str(termcolor.ATTRIBUTES[c])
            elif c in termcolor.HIGHLIGHTS:
                result += ';' + str(termcolor.HIGHLIGHTS[c])
            elif self._RGB_COLOR_SPEC_RE.match(c):
                # BUG Fucking Python! Why not to assign and check a variable inside of `if`
                # TODO Avoid double regex match
                match = self._RGB_COLOR_SPEC_RE.search(c)
                try:
                    r = self._validate_rgb_component(int(match.group(1)))
                    g = self._validate_rgb_component(int(match.group(2)))
                    b = self._validate_rgb_component(int(match.group(3)))
                    index = self._rgb_to_index(r, g, b)
                    result += ';38;5;' + str(index)
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
                    result += ';38;5;' + str(index)
                except ValueError:
                    raise RuntimeError(
                        'Invalid value of key `{}`: invalid grayscale color specification "{}" [{}]'.
                        format(key, c, self.filename)
                      )
            else:
                try:
                    index = int(c)
                    if 15 < index and index < 256:
                        result += ';38;5;' + c
                except ValueError:
                    raise RuntimeError(
                        'Invalid value of key `{}`: expected color specification "{}" [{}]'.
                        format(key, c, self.filename)
                      )
        return '\x1b[' + ('0' if need_reset else '') + result + 'm'


    def _validate_rgb_component(self, c):
        assert(isinstance(c, int))
        if c < 0 or 5 < c:
            raise ValueError('RGB component is out of range')
        return c


    def _rgb_to_index(self, r, g, b):
        return r * 36 + g * 6 + b + 16


    def _validate_grayscale(self, c):
        assert(isinstance(c, int))
        if c < 0 or 24 < c:
            raise ValueError('Grayscale index is out of range')
        return c


    def _grayscale_to_index(self, g):
        assert((232 + g) < 256)
        return 232 + g
