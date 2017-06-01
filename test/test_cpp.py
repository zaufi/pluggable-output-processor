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
    Unit tests for `make` post-processor gcc command line matching regex
'''

# Project specific imports
from context import make_data_filename
from outproc.cpp_helpers import SimpleCppLexer, SnippetSanitizer, CodeFormatter

# Standard imports
import pytest


def try_read_contents(filename):
    input_file = make_data_filename(filename)
    if input_file.exists():
        with input_file.open('r') as fd:
            return fd.read().strip()
    raise RuntimeError('File not found: {}'.format(input_file))


#def read_input_and_expected_output(name):
    #''' TODO Move to some shared module? '''
    #def _wrapper(fn):
        #fn.input = _try_read_contents(os.path.join(_DATA_DIR, name + '.input'))
        #fn.expected = _try_read_contents(os.path.join(_DATA_DIR, name + '.expected'))
        #return fn

    #return _wrapper


class simple_cpp_lexer_tester:

    @pytest.mark.parametrize(
        'input_line, expected_token_count'
      , [
            ('struct std::pair<ctm::task, ctm::task_manager::task_state>', 8)
          , ('void caos::ctm::task_manager::add_download_target(const boost::uuids::uuid&, std::deque<network::uri>&&, unsigned int)', 16)
          , ('the_only_identifier', 1)
          , ('LOG4CXX_DEBUG(m_logger, task_it->m_dl_queue.size() << " pages queued");', 12)
          , ('LOG4CXX_DEBUG(m_logger, " -> ");', 6)
          , ('LOG4CXX_DEBUG(m_logger, task_it->m_dl_queue.size() << u8" pages queued");', 12)
          , ('LOG4CXX_DEBUG(m_logger, u8R" -> ");', 6)
          , ('std::cout << "deduced type: " << type_name(k) << std::endl;', 10)
          , ('http::connector m_connector;  // Connector instance to establish new HTTP connections', 5)
          , ('http::connector m_connector;  ///< Connector instance to establish new HTTP connections', 5)
          , ('void foo(int /*unused*/);', 8)
          , ('void foo(int /**** /unused/ ****/);', 8)
          , ('''std::cout << __PRETTY_FUNCTION__ << ":\nname='"_ru << name << '\\'' << std::endl;''', 12)
          , ('''QString("Using PCH file: %1%").arg(config().precompiledHeaderFile())''', 10)
        ]
      )
    def tockenizer_and_assemble_test(self, input_line, expected_token_count):
        tokens = SimpleCppLexer.tokenize_string(input_line)
        assert len(tokens) == expected_token_count
        stmt = SimpleCppLexer.assemble_statement(tokens)
        assert stmt == input_line


class cpp_sanitizer_tester:


    @pytest.mark.parametrize(
        'input_line, output_line'
      , [
            (
                'std::_Placeholder<1>'
              , 'std::placeholders::_1'
            )
          , (
                'text before std::_Placeholder<12>, text after'
              , 'text before std::placeholders::_12, text after'
            )
          , (
                'text before std::_Placeholder<12>, text middle, std::_Placeholder<1>'
              , 'text before std::placeholders::_12, text middle, std::placeholders::_1'
            )
          , (
                'template <class ... Args> void foo(Args&& ... args);'
              , 'template <class... Args> void foo(Args&&... args);'
            )
          , (
                'template <class ... Args> void foo(Args&& ... args);'
              , 'template <class... Args> void foo(Args&&... args);'
            )
          , (
                'void foo(long unsigned int, unsigned int, short unsigned int);'
              , 'void foo(unsigned long, unsigned, unsigned short);'
            )
          , (
                'std::vector<std::pair<int, std::list<std::basic_string<char> > > >'
              , 'std::vector<std::pair<int, std::list<std::string>>>'
            )
          , (
                'std::vector<std::pair<int, std::list<std::basic_string<char16_t> > > >'
              , 'std::vector<std::pair<int, std::list<std::basic_string<char16_t>>>>'
            )
          , (
                'template <class A1>'
              , 'template <class A1>'
            )
          , (
                'template <class A1, class A2>'
              , 'template <class A1, class A2>'
            )
          , (
                'template <typename A1, typename A2>'
              , 'template <typename A1, typename A2>'
            )
          , (
                'template <class A1, class A2, class A3>'
              , 'template <class A1, ..., class A3>'
            )
          , (
                'template <class A1, class A2, class A3, class B>'
              , 'template <class A1, ..., class A3, class B>'
            )
          , (
                'template <class A1, class A2, class A3, class A5>'
              , 'template <class A1, ..., class A3, class A5>'
            )
          , (
                'template <class A1, class A2, class A3, class A5, class A6, class A7>'
              , 'template <class A1, ..., class A3, class A5, ..., class A7>'
            )
          , (
                'template <class A1, class A2, class A3, class B1, class C6, class C7, class C8>'
              , 'template <class A1, ..., class A3, class B1, class C6, ..., class C8>'
            )
          , (
                'Foo<A1, A2, A3>'
              , 'Foo<A1, ..., A3>'
            )
          , (
                'template <class A1, class A2, class A3, class B> class Foo<A1, A2, A3, B>'
              , 'template <class A1, ..., class A3, class B> class Foo<A1, ..., A3, B>'
            )
          , (
                'template <class F, class A1, class A2> boost::_bi::bind_t<boost::_bi::unspecified, F, typename boost::_bi::list_av_2<A1, A2>::type> boost::bind(F, A1, A2)'
              , 'template <class F, class A1, class A2> boost::_bi::bind_t<boost::_bi::unspecified, F, typename boost::_bi::list_av_2<A1, A2>::type> boost::bind(F, A1, A2)'
            )
          , (
                'template <class A1, class M, class T> boost::_bi::bind_t<typename boost::_bi::dm_result<M T::*, A1>::type, boost::_mfi::dm<M, T>, typename boost::_bi::list_av_1<A1>::type> boost::bind(M T::*, A1)'
              , 'template <class A1, class M, class T> boost::_bi::bind_t<typename boost::_bi::dm_result<M T::*, A1>::type, boost::_mfi::dm<M, T>, typename boost::_bi::list_av_1<A1>::type> boost::bind(M T::*, A1)'
            )
          , (
                'template <class A1, class B1, class A2, class B2, class A3, class B3> class Foo<A1, A2, A3, B1, B2, B3>'
              , 'template <class A1, class B1, class A2, class B2, class A3, class B3> class Foo<A1, ..., A3, B1, ..., B3>'
            )
          , (
                'foo(A1 a1)'
              , 'foo(A1 a1)'
            )
          , (
                'Int64'
              , 'Int64'
            )
          , (
                'before std::forward_list<int, std::allocator<int> > after'
              , 'before std::forward_list<int> after'
            )
          , (
                'Multiple std::forward_list<int, std::allocator<int> > matches std::vector<char, std::allocator<char>> here'
              , 'Multiple std::forward_list<int> matches std::vector<char> here'
            )
          , (
                'template <class Derived1, class V1, class TC1, class Reference1, class Difference1, class Derived2, class V2, class TC2, class Reference2, class Difference2> typename boost::iterators::detail::enable_if_interoperable<Derived1, Derived2, typename boost::mpl::apply2<boost::iterators::detail::always_bool2, Derived1, Derived2>::type>::type boost::iterators::operator!=(const boost::iterators::iterator_facade<Derived1, V1, TC1, Reference1, Difference1>&, const boost::iterators::iterator_facade<Derived2, V2, TC2, Reference2, Difference2>&)'
              , 'template <class Derived1, class V1, class TC1, class Reference1, class Difference1, class Derived2, class V2, class TC2, class Reference2, class Difference2> typename boost::iterators::detail::enable_if_interoperable<Derived1, Derived2, typename boost::mpl::apply2<boost::iterators::detail::always_bool2, Derived1, Derived2>::type>::type boost::iterators::operator!=(const boost::iterators::iterator_facade<Derived1, V1, TC1, Reference1, Difference1>&, const boost::iterators::iterator_facade<Derived2, V2, TC2, Reference2, Difference2>&)'
            )
        ]
      )
    def cleanup_snippet_test(self, input_line, output_line):
        result = SnippetSanitizer.cleanup_snippet(input_line)
        assert result == output_line



class code_formatter_tester:

    @pytest.mark.parametrize(
        'input_file, expected_file, width'
      , [
            ('SimpleCodeFormatter.test_0.input', 'SimpleCodeFormatter.test_0.expected', 20)
          , ('SimpleCodeFormatter.test_1.input', 'SimpleCodeFormatter.test_1.expected', 30)
          , ('SimpleCodeFormatter.test_2.input', 'SimpleCodeFormatter.test_2.expected', 30)
          , ('SimpleCodeFormatter.test_3.input', 'SimpleCodeFormatter.test_3.expected', 30)
          , ('SimpleCodeFormatter.test_4.input', 'SimpleCodeFormatter.test_4.expected', 30)
          , ('SimpleCodeFormatter.test_5.input', 'SimpleCodeFormatter.test_5.expected', 30)
          , ('SimpleCodeFormatter.test_6.input', 'SimpleCodeFormatter.test_6.expected', 30)
          , ('SimpleCodeFormatter.test_7.input', 'SimpleCodeFormatter.test_7.expected', 30)
          , ('SimpleCodeFormatter.test_8.input', 'SimpleCodeFormatter.test_8.expected', 30)
          , ('SimpleCodeFormatter.test_9.input', 'SimpleCodeFormatter.test_9.expected', 40)
          , ('SimpleCodeFormatter.test_9a.input', 'SimpleCodeFormatter.test_9a.expected', 36)
          , ('SimpleCodeFormatter.test_10.input', 'SimpleCodeFormatter.test_10.expected', 30)
          , ('SimpleCodeFormatter.test_10a.input', 'SimpleCodeFormatter.test_10a.expected', 30)
          , ('SimpleCodeFormatter.test_10b.input', 'SimpleCodeFormatter.test_10b.expected', 27)
          , ('SimpleCodeFormatter.test_10c.input', 'SimpleCodeFormatter.test_10c.expected', 20)
          , ('SimpleCodeFormatter.test_11.input', 'SimpleCodeFormatter.test_11.expected', 25)
          , ('SimpleCodeFormatter.test_12.input', 'SimpleCodeFormatter.test_12.expected', 150)
        ]
      )
    def snippet_format_test(self, input_file, expected_file, width):
        input_text = try_read_contents(input_file)
        expected_text = try_read_contents(expected_file)

        formatter = CodeFormatter(width)
        result = formatter.pretty_format(input_text)

        assert result == expected_text

    def print_test(self):
        formatter = CodeFormatter(150)
        snippet='template<class Derived1, class V1, class TC1, class Reference1, class Difference1, class Derived2, class V2, class TC2, class Reference2, class Difference2> typename boost::iterators::detail::enable_if_interoperable<Derived1, Derived2, typename boost::mpl::apply2<boost::iterators::detail::always_bool2, Derived1, Derived2>::type>::type boost::iterators::operator!=(const boost::iterators::iterator_facade<Derived1, V1, TC1, Reference1, Difference1>&, const boost::iterators::iterator_facade<Derived2, V2, TC2, Reference2, Difference2>&)'
        result = formatter.pretty_format(snippet)
        print('result={}'.format(result))
