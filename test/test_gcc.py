#!/usr/bin/env python
#
# Unit tests for `make` post-processor gcc command line matching regex
#

# Standard imports
import sys
import unittest

sys.path.insert(0, '..')

# Project specific imports
import outproc
from outproc.pp.gcc import _LOCATION_RE

class ComplierCmdLineMatchTester(unittest.TestCase):

    def setUp(self):
        pass

    def test_location_matcher_0(self):
        line = "/work/xxx/xxx-devel/task_manager.cc: In member function"
        #print('testing> "{}"'.format(line))
        match = _LOCATION_RE.search(line)
        #print(match.groups())

        self.assertTrue(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), 36)


    def test_location_matcher_1(self):
        line = " from /work/xxx/xxx-devel/task.hh:18,"
        #print('testing> "{}"'.format(line))
        match = _LOCATION_RE.search(line)
        #print(match.groups())

        self.assertTrue(match)
        self.assertEqual(match.start(), 6)
        self.assertEqual(match.end(), 37)


    def test_location_matcher_2(self):
        line = "apply_apply.cc:11:27: error: 'zzT' was not declared in this scope"
        #print('testing> "{}"'.format(line))
        match = _LOCATION_RE.search(line)
        #print(match.groups())

        self.assertTrue(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), 21)


    def test_location_matcher_3(self):
        line = 'In file included from /work/xxx/xxx-devel/details/pre_task.hh:23:0,'
        #print('testing> "{}"'.format(line))
        match = _LOCATION_RE.search(line)
        #print(match.groups())

        self.assertTrue(match)
        self.assertEqual(match.start(), 22)
        self.assertEqual(match.end(), 67)
