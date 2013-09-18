#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os

class Config(object):
    ''' Simple configuration data accessor

        Every plugin may (and actually is) have a configuration data stored
        in a simple text file at ${prefix}/etc/outproc/.
        This class can read and give an access to that data in a easy to use way.
    '''

    def __init__(self, filename):
        '''Read configuration data from a given file'''
        if not os.path.isfile(filename):
            raise RuntimeError('No such file {}'.format(filename))

        # Read the file line by line, and collect keys and values into an internal dict
        self.data = {}
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


    def get_string_with_default(self, key, default):
        assert(isinstance(key, str))
        assert(isinstance(default, str) or default is None)

        return self.data[key] if key in self.data else default
