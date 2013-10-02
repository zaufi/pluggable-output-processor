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
from outproc.cpp_helpers import SimpleCppLexer, SnippetSanitizer

class SimpleCppLexerTester(unittest.TestCase):

    def setUp(self):
        pass


    def test_0(self):
        line = 'struct std::pair<ctm::task, ctm::task_manager::task_state>'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 8)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_1(self):
        line = 'void caos::ctm::task_manager::add_download_target(const boost::uuids::uuid&, std::deque<network::uri>&&, unsigned int)'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 16)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_2(self):
        line = 'the_only_identifier'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 1)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_3(self):
        line = 'LOG4CXX_DEBUG(m_logger, task_it->m_dl_queue.size() << " pages queued");'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 12)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_4(self):
        line = 'LOG4CXX_DEBUG(m_logger, " -> ");'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 6)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_5(self):
        line = 'LOG4CXX_DEBUG(m_logger, task_it->m_dl_queue.size() << u8" pages queued");'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 12)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)

    def test_6(self):
        line = 'LOG4CXX_DEBUG(m_logger, u8R" -> ");'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 6)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_7(self):
        line = 'std::cout << "deduced type: " << type_name(k) << std::endl;'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 10)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_8(self):
        line = 'http::connector m_connector;  // Connector instance to establish new HTTP connections'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 5)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_9(self):
        line = 'http::connector m_connector;  ///< Connector instance to establish new HTTP connections'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 5)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_10(self):
        line = 'void foo(int /*unused*/);'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 8)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_11(self):
        line = 'void foo(int /**** /unused/ ****/);'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 8)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_12(self):
        line = 'void foo(int /**** <<->> ****/);'
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 8)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_13(self):
        line = '''std::cout << __PRETTY_FUNCTION__ << ":\nname='"_ru << name << '\\'' << std::endl;'''
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 12)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)


    def test_14(self):
        line = '''QString("Using PCH file: %1%").arg(config().precompiledHeaderFile())'''
        tokens = SimpleCppLexer.tokenize_string(line)
        #print(tokens)
        self.assertEqual(len(tokens), 10)
        stmt = SimpleCppLexer.assemble_statement(tokens)
        self.assertEqual(stmt, line)



class CppSanitizerTester(unittest.TestCase):

    def setUp(self):
        pass


    def test_0(self):
        line = 'std::_Placeholder<1>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'std::placeholders::_1')


    def test_1(self):
        line = 'text before std::_Placeholder<12>, text after'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'text before std::placeholders::_12, text after')


    def test_2(self):
        line = 'text before std::_Placeholder<12>, text middle, std::_Placeholder<1>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'text before std::placeholders::_12, text middle, std::placeholders::_1')


    def test_3(self):
        line = 'template <class ... Args> void foo(Args&& ... args);'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class... Args> void foo(Args&&... args);')


    def test_4(self):
        line = 'void foo(long unsigned int, unsigned int, short unsigned int);'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'void foo(unsigned long, unsigned, unsigned short);')
