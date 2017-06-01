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
    Helper functions reusable by various tests
'''

# Project specific imports

# Standard imports
import os
import pathlib
import platform
import re
import sys
import warnings

# NOTE DO NOT REMOVE
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_data_dir = pathlib.Path(__file__).parent / 'data'


def data_dir_base():
    return _data_dir


def output_dir_base():
    return data_dir_base() / 'output'


def make_data_filename(filename):
    return data_dir_base() / filename


def _match_expected_output(filename, output):
    if not output:
        return

    transformed_output = ' '.join(output.splitlines())
    if filename.exists():
        # ATTENTION Python >= 3.5 only!
        with filename.open('r') as inp:
            content = ' '.join(inp.read().splitlines())
            what = re.compile(content)
            print('content={}'.format(repr(content)))
            assert bool(what.match(transformed_output))
    else:
        warnings.warn('There is no file to match `{}`'.format(filename), RuntimeWarning)


def match_expected_output(test_name, stdout, stderr):
    _match_expected_output(make_data_filename('{}-{}.out'.format(test_name, platform.system())), stdout)
    _match_expected_output(make_data_filename('{}-{}.err'.format(test_name, platform.system())), stderr)
