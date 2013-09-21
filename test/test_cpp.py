#!/usr/bin/env python
#
# Unit tests for `make` post-processor gcc command line matching regex
#

# Standard imports
import os
import sys
import termcolor
import unittest

sys.path.insert(0, '..')

# Project specific imports
import outproc
from outproc.cpp_helpers import SimpleCppLexer

class SimpleCppLexerTester(unittest.TestCase):

    def setUp(self):
        pass

    def test_0(self):
        line = 'struct std::pair<ctm::task, ctm::task_manager::task_state>'
        tokens = SimpleCppLexer.tokenize_string(line)
        print(tokens)
        self.assertEqual(len(tokens), 8)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)

    def test_1(self):
        line = 'void caos::ctm::task_manager::add_download_target(const boost::uuids::uuid&, std::deque<network::uri>&&, unsigned int)'
        tokens = SimpleCppLexer.tokenize_string(line)
        print(tokens)
        self.assertEqual(len(tokens), 16)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)

    def test_2(self):
        line = 'the_only_identifier'
        tokens = SimpleCppLexer.tokenize_string(line)
        print(tokens)
        self.assertEqual(len(tokens), 1)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)
