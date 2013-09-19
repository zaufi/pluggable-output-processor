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

import os
import termcolor

class Config(object):
    ''' Simple configuration data accessor

        Every plugin may (and actually is) have a configuration data stored
        in a simple text file at ${prefix}/etc/outproc/.
        This class can read and give an access to that data in a easy to use way.
    '''

    def __init__(self, filename):
        '''Read configuration data from a given file'''

        # Remember filename for future references (to show errors)
        self.filename = filename
        # Make an empty dict for configuration data
        self.data = {}
        # Set some predefined values
        self.normal_color = termcolor.RESET
        # NOTE Konsole terminal from KDE supports itallic font style
        termcolor.ATTRIBUTES['itallic'] = 3

        if not os.path.isfile(filename):
            return

        # Read the file line by line, and collect keys and values into an internal dict
        with open(filename) as ifs:
            for l in ifs.readlines():
                # Strip possible comment lines
                line_str = l.strip()
                if line_str.startswith('#'):
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
            raise ValueError('Invalid value of key `{}`: expected integer, got "{}"'.format(key, self.data[key]))


    def get_color(self, key, default):
        '''Get color key value or default if absent.
            Throw ValueError if not an integer.
        '''
        assert(isinstance(key, str))
        assert(isinstance(default, str) or default is not None)

        def _make_color_string(s):
            return '\x1b[{}m'.format(s)

        colors = [c.strip() for c in (self.data[key] if key in self.data else default).split(',')]
        result = ''

        for c in colors:
            if c == 'normal':
                result += termcolor.RESET
            elif c in termcolor.COLORS:
                result += _make_color_string(termcolor.COLORS[c])
            elif c in termcolor.ATTRIBUTES:
                result += _make_color_string(termcolor.ATTRIBUTES[c])
            elif c in termcolor.HIGHLIGHTS:
                result += _make_color_string(termcolor.HIGHLIGHTS[c])
            else:
                raise ValueError('Invalid value of key `{}`: expected color specification, got "{}"'.format(key, self.data[key]))
        return result
