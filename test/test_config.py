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
        self.assertEqual(cfg.get_color('red', 'red'), '\x1b[0m\x1b[31m')
        self.assertEqual(cfg.get_color('red', 'red', with_reset=False), '\x1b[31m')
        self.assertEqual(cfg.get_color('error', 'normal'), '\x1b[0m\x1b[31m\x1b[1m')
        self.assertEqual(cfg.get_color('error', 'normal',with_reset=False), '\x1b[31m\x1b[1m')
        self.assertEqual(cfg.get_color('not-existed', 'normal'), '\x1b[0m\x1b[38m')
        self.assertEqual(cfg.get_color('some-int', 'reset'), '\x1b[0m\x1b[38;5;123m')
        self.assertEqual(cfg.get_color('none', 'none'), '')
        #self.assertEqual(cfg.get_color('invalid-color', 'red'), '\x1b[0;31m')
        # Try TrueColor specs
        self.assertEqual(cfg.get_color('true_rgb_red', 'red'), '\x1b[0m\x1b[38;2;255;0;0m')
        self.assertEqual(cfg.get_color('true_rgb_green', 'red'), '\x1b[0m\x1b[38;2;0;255;0m')
        self.assertEqual(cfg.get_color('true_rgb_blue', 'red'), '\x1b[0m\x1b[38;2;0;0;255m')
        with self.assertRaises(TypeError):
            cfg.get_color('red')


    def test_get_bool_value(self):
        cfg = outproc.Config(self.data_file('sample.conf'))
        self.assertEqual(cfg.get_bool('not-existed'), None)
        self.assertEqual(cfg.get_bool('not-existed', True), True)
        self.assertEqual(cfg.get_bool('not-existed', False), False)
        self.assertEqual(cfg.get_bool('true-bool-key-1'), True)
        self.assertEqual(cfg.get_bool('false-bool-key-1'), False)
        self.assertEqual(cfg.get_bool('true-bool-key-2'), True)
        self.assertEqual(cfg.get_bool('false-bool-key-2'), False)
        with self.assertRaises(ValueError):
            cfg.get_bool('some-int')
