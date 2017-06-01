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
    Unit tests for Config class
'''

# Project specific imports
from context import make_data_filename
from outproc.config import Config

# Standard imports
import pytest


class config_tester:
    '''Unit tests for Config class'''

    def not_exitsted_file_test(self):
        cfg = Config(make_data_filename('not-existed-file'))
        assert cfg.get_string('not-existed', 'default') == 'default'
        assert cfg.get_int('not-existed', 123) == 123


    def get_string_value_test(self):
        cfg = Config(make_data_filename('sample.conf'))
        assert cfg.get_string('some') == 'value'
        assert cfg.get_string('not-existed', 'default') == 'default'
        assert cfg.get_string('some-int') == '123'


    def get_int_value_test(self):
        cfg = Config(make_data_filename('sample.conf'))
        assert cfg.get_int('some-int') == 123
        assert cfg.get_int('not-existed', 123) == 123
        with pytest.raises(ValueError):
            cfg.get_int('not-an-int', 123)


    def get_color_value_test(self):
        cfg = Config(make_data_filename('sample.conf'))
        assert cfg.get_color('red', 'red') == '\x1b[0m\x1b[31m'
        assert cfg.get_color('red', 'red', with_reset=False) == '\x1b[31m'
        assert cfg.get_color('error', 'normal') == '\x1b[0m\x1b[31m\x1b[1m'
        assert cfg.get_color('error', 'normal', with_reset=False) == '\x1b[31m\x1b[1m'
        assert cfg.get_color('not-existed', 'normal') == '\x1b[0m\x1b[38m'
        assert cfg.get_color('some-int', 'reset') == '\x1b[0m\x1b[38;5;123m'
        assert cfg.get_color('none', 'none') == ''
        # Try TrueColor specs
        assert cfg.get_color('true_rgb_red', 'red') == '\x1b[0m\x1b[38;2;255;0;0m'
        assert cfg.get_color('true_rgb_green', 'red') == '\x1b[0m\x1b[38;2;0;255;0m'
        assert cfg.get_color('true_rgb_blue', 'red') == '\x1b[0m\x1b[38;2;0;0;255m'
        with pytest.raises(TypeError):
            cfg.get_color('red')


    def get_bool_value_test(self):
        cfg = Config(make_data_filename('sample.conf'))
        assert cfg.get_bool('not-existed') is None
        assert cfg.get_bool('not-existed', True) == True
        assert cfg.get_bool('not-existed', False) == False
        assert cfg.get_bool('true-bool-key-1') == True
        assert cfg.get_bool('false-bool-key-1') == False
        assert cfg.get_bool('true-bool-key-2') == True
        assert cfg.get_bool('false-bool-key-2') == False
        with pytest.raises(ValueError):
            cfg.get_bool('some-int')
