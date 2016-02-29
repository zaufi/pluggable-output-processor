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
from outproc.cpp_helpers import SimpleCppLexer, SnippetSanitizer, CodeFormatter

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def _try_read_contents(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as fd:
            return fd.read().strip()
    raise unittest.SkipTest('File not found: {}'.format(filename))


def read_input_and_expected_output(name):
    ''' TODO Move to some shared module? '''
    def _wrapper(fn):
        fn.input = _try_read_contents(os.path.join(_DATA_DIR, name + '.input'))
        fn.expected = _try_read_contents(os.path.join(_DATA_DIR, name + '.expected'))
        return fn

    return _wrapper


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
        line = 'std::vector<std::pair<int, std::list<std::basic_string<char> > > >'
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


    def test_7a(self):
        line = 'template <typename A1>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, line)


    def test_8(self):
        line = 'template <class A1, class A2>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, line)


    def test_8a(self):
        line = 'template <typename A1, typename A2>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, line)


    def test_8b(self):
        line = 'template <typename A1, class A2>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, line)


    def test_9(self):
        line = 'template <class A1, class A2, class A3>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, ..., class A3>')


    def test_10(self):
        line = 'template <class A1, class A2, class A3, class B>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, ..., class A3, class B>')


    def test_10a(self):
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
        line = 'template <class A1, class A2, class A3, class B> class Foo<A1, A2, A3, B>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, ..., class A3, class B> class Foo<A1, ..., A3, B>')


    def test_15(self):
        line = 'template <class F, class A1, class A2> boost::_bi::bind_t<boost::_bi::unspecified, F, typename boost::_bi::list_av_2<A1, A2>::type> boost::bind(F, A1, A2)'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, line)


    def test_16(self):
        line = 'template <class A1, class M, class T> boost::_bi::bind_t<typename boost::_bi::dm_result<M T::*, A1>::type, boost::_mfi::dm<M, T>, typename boost::_bi::list_av_1<A1>::type> boost::bind(M T::*, A1)'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, line)


    def test_17(self):
        line = 'template <class A1, class A2, class A3, class B1, class C6, class C7, class C8>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, ..., class A3, class B1, class C6, ..., class C8>')


    def test_18(self):
        line = 'template <class A1, class B1, class A2, class B2, class A3, class B3> class Foo<A1, A2, A3, B1, B2, B3>'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class A1, class B1, class A2, class B2, class A3, class B3> class Foo<A1, ..., A3, B1, ..., B3>')


    def test_19(self):
        line = 'foo(A1 a1)'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'foo(A1 a1)')


    def test_20(self):
        line = 'Int64'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'Int64')


    def test_21(self):
        line = 'before std::forward_list<int, std::allocator<int> > after'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'before std::forward_list<int> after')


    def test_22(self):
        line = 'Multiple std::forward_list<int, std::allocator<int> > matches std::vector<char, std::allocator<char>> here'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'Multiple std::forward_list<int> matches std::vector<char> here')


    def test_23(self):
        line = 'template <class Derived1, class V1, class TC1, class Reference1, class Difference1, class Derived2, class V2, class TC2, class Reference2, class Difference2> typename boost::iterators::detail::enable_if_interoperable<Derived1, Derived2, typename boost::mpl::apply2<boost::iterators::detail::always_bool2, Derived1, Derived2>::type>::type boost::iterators::operator!=(const boost::iterators::iterator_facade<Derived1, V1, TC1, Reference1, Difference1>&, const boost::iterators::iterator_facade<Derived2, V2, TC2, Reference2, Difference2>&)'
        result = SnippetSanitizer.cleanup_snippet(line)
        self.assertEqual(result, 'template <class Derived1, class V1, class TC1, class Reference1, class Difference1, class Derived2, class V2, class TC2, class Reference2, class Difference2> typename boost::iterators::detail::enable_if_interoperable<Derived1, Derived2, typename boost::mpl::apply2<boost::iterators::detail::always_bool2, Derived1, Derived2>::type>::type boost::iterators::operator!=(const boost::iterators::iterator_facade<Derived1, V1, TC1, Reference1, Difference1>&, const boost::iterators::iterator_facade<Derived2, V2, TC2, Reference2, Difference2>&)')


class SimpleCodeFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = CodeFormatter(100)


    @read_input_and_expected_output('SimpleCodeFormatter.test_0')
    def test_0(self):
        formatter = CodeFormatter(20)
        result = formatter.pretty_format(self.test_0.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_0.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_1')
    def test_1(self):
        formatter = CodeFormatter(30)
        result = formatter.pretty_format(self.test_1.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_1.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_2')
    def test_2(self):
        formatter = CodeFormatter(30)
        result = formatter.pretty_format(self.test_2.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_2.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_3')
    def test_3(self):
        formatter = CodeFormatter(30)
        result = formatter.pretty_format(self.test_3.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_3.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_4')
    def test_4(self):
        formatter = CodeFormatter(30)
        result = formatter.pretty_format(self.test_4.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_4.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_5')
    def test_5(self):
        formatter = CodeFormatter(30)
        result = formatter.pretty_format(self.test_5.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_5.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_6')
    def test_6(self):
        formatter = CodeFormatter(30)
        result = formatter.pretty_format(self.test_6.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_6.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_7')
    def test_7(self):
        formatter = CodeFormatter(30)
        result = formatter.pretty_format(self.test_7.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_7.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_8')
    def test_8(self):
        formatter = CodeFormatter(30)
        result = formatter.pretty_format(self.test_8.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_8.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_9')
    def test_9(self):
        formatter = CodeFormatter(40)
        result = formatter.pretty_format(self.test_9.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_9.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_9a')
    def test_9a(self):
        formatter = CodeFormatter(36)
        result = formatter.pretty_format(self.test_9a.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_9a.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_10')
    def test_10(self):
        formatter = CodeFormatter(30)
        result = formatter.pretty_format(self.test_10.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_10.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_10a')
    def test_10a(self):
        formatter = CodeFormatter(30)
        result = formatter.pretty_format(self.test_10a.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_10a.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_10b')
    def test_10b(self):
        formatter = CodeFormatter(27)
        result = formatter.pretty_format(self.test_10b.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_10b.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_10c')
    def test_10c(self):
        formatter = CodeFormatter(20)
        result = formatter.pretty_format(self.test_10c.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_10c.expected)

    @read_input_and_expected_output('SimpleCodeFormatter.test_11')
    def test_11(self):
        formatter = CodeFormatter(25)
        result = formatter.pretty_format(self.test_11.input)
        print('result={}'.format(result))
        self.assertEqual(result, self.test_11.expected)

    def test_print(self):
        formatter = CodeFormatter(150)
        snippet='template<class Derived1, class V1, class TC1, class Reference1, class Difference1, class Derived2, class V2, class TC2, class Reference2, class Difference2> typename boost::iterators::detail::enable_if_interoperable<Derived1, Derived2, typename boost::mpl::apply2<boost::iterators::detail::always_bool2, Derived1, Derived2>::type>::type boost::iterators::operator!=(const boost::iterators::iterator_facade<Derived1, V1, TC1, Reference1, Difference1>&, const boost::iterators::iterator_facade<Derived2, V2, TC2, Reference2, Difference2>&)'
        result = formatter.pretty_format(snippet)
        print('result={}'.format(result))
