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


    def test_5(self):
        line = 'std::vector<std::pair<int, std::list<std::string> > >'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'std::vector<std::pair<int, std::list<std::string>>>')


    def test_6(self):
        line = 'std::vector<std::pair<int, std::list<std::basic_string<char16_t> > > >'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'std::vector<std::pair<int, std::list<std::basic_string<char16_t>>>>')


    def test_7(self):
        line = 'template <class A1>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, line)


    def test_8(self):
        line = 'template <class A1, class A2>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, line)


    def test_9(self):
        line = 'template <class A1, class A2, class A3>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, ..., class A3>')


    def test_10(self):
        line = 'template <class A1, class A2, class A3, class A5>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, ..., class A3, class A5>')


    def test_11(self):
        line = 'template <class A1, class A2, class A3, class A5, class A6, class A7>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, ..., class A3, class A5, ..., class A7>')


    def test_12(self):
        line = 'Foo<A1, A2, A3>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'Foo<A1, ..., A3>')


    def test_13(self):
        line = 'template <class A1, class A2, class A3> class Foo<A1, A2, A3>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, ..., class A3> class Foo<A1, ..., A3>')


    def test_14(self):
        line = 'template <class A1, class A2, class A3, class B>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, ..., class A3, class B>')


    def test_15(self):
        line = 'template <class A1, class A2, class A3, class B> class Foo<A1, A2, A3, B>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, ..., class A3, class B> class Foo<A1, ..., A3, B>')


    def test_16(self):
        line = 'template <class F, class A1, class A2> boost::_bi::bind_t<boost::_bi::unspecified, F, typename boost::_bi::list_av_2<A1, A2>::type> boost::bind(F, A1, A2)'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, line)


    def test_17(self):
        line = 'template <class A1, class M, class T> boost::_bi::bind_t<typename boost::_bi::dm_result<M T::*, A1>::type, boost::_mfi::dm<M, T>, typename boost::_bi::list_av_1<A1>::type> boost::bind(M T::*, A1)'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, line)


    def test_18(self):
        line = 'template <class A1, class A2, class A3, class B1, class C6, class C7, class C8>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, ..., class A3, class B1, class C6, ..., class C8>')


    def test_19(self):
        line = 'foo(A1 a1)'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'foo(A1 a1)')


    def test_20(self):
        line = 'Int64'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'Int64')
