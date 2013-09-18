#!/usr/bin/env python
#
# Unit tests for Config class
#

# Standard imports
import os
import sys
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
        try:
            cfg = outproc.Config('not-existed-file')
            self.assertTrue(False)
        except:
            self.assertTrue(True)


    def test_get_sample_value(self):
        cfg = outproc.Config(self.data_file('sample.conf'))
        self.assertEqual(cfg.get_string_with_default('some', None), 'value')
        self.assertEqual(cfg.get_string_with_default('not-existed', 'default'), 'default')
