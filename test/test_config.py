#!/usr/bin/env python
#
# Unit tests for Config class
#

# Standard imports
import os
import sys
import termcolor
import unittest

sys.path.insert(0, '..')

# Project specific imports
import outproc

class ConfigTester(unittest.TestCase):
    '''Unit tests for Config class'''

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    def setUp(self):
        pass


    def data_file(self, filename):
        return os.path.join(self.data_dir, filename)


    def test_not_exitsted_file(self):
        cfg = outproc.Config('not-existed-file')
        self.assertEqual(cfg.get_string('not-existed', 'default'), 'default')
        self.assertEqual(cfg.get_int('not-existed', 123), 123)


    def test_get_string_value(self):
        cfg = outproc.Config(self.data_file('sample.conf'))
        self.assertEqual(cfg.get_string('some'), 'value')
        self.assertEqual(cfg.get_string('not-existed', 'default'), 'default')
        self.assertEqual(cfg.get_string('some-int'), '123')


    def test_get_int_value(self):
        cfg = outproc.Config(self.data_file('sample.conf'))
        self.assertEqual(cfg.get_int('some-int'), 123)
        self.assertEqual(cfg.get_int('not-existed', 123), 123)
        with self.assertRaises(ValueError):
            cfg.get_int('not-an-int', 123)


    def test_get_color_value(self):
        cfg = outproc.Config(self.data_file('sample.conf'))
        self.assertEqual(cfg.get_color('red', 'red'), '\x1b[31m')
        self.assertEqual(cfg.get_color('error', 'normal'), '\x1b[31;1m')
        self.assertEqual(cfg.get_color('not-existed', 'normal'), '\x1b[38m')
        self.assertEqual(cfg.get_color('some-int', 'reset'), '\x1b[38;5;123m')
        with self.assertRaises(TypeError):
            cfg.get_color('red')
