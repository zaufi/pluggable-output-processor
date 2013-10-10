#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is a part of Pluggable Output Processor
#
# Copyright (c) 2013 Alex Turbov <i.zaufi@gmail.com>
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

import re
import os
import termcolor


class SimpleCppLexer(object):
    ''' Helper class to get C++ lexems to be highlighted'''

    _IDENTIFIER_RE = re.compile('[A-Za-z_][A-Za-z_0-9]*')
    # TODO A real expression to match numbers is much more complicated!
    # (and not so naive/stupid) Do we really need it? This one covers
    # most seen cases...
    _NUMBER_RE = re.compile('^(\d+(\.\d*)?(f|[uU]?[lL]{0,2})?)$')
    _STRING_RE = re.compile('(.*?)(("[^"]*)("(.*))?)')

    _KEYWORDS = [
        'alignof'
      , 'alignas'
      , 'asm'
      , 'auto'
      , 'break'
      , 'case'
      , 'catch'
      , 'class'
      , 'const_cast'
      , 'constexpr'
      , 'continue'
      , 'decltype'
      , 'default'
      , 'delete'
      , 'do'
      , 'dynamic_cast'
      , 'else'
      , 'enum'
      , 'explicit'
      , 'export'
      , 'false'
      , 'final'
      , 'for'
      , 'friend'
      , 'goto'
      , 'if'
      , 'inline'
      , 'namespace'
      , 'new'
      , 'noexcept'
      , 'nullptr'
      , 'operator'
      , 'override'
      , 'private'
      , 'protected'
      , 'public'
      , 'register'
      , 'reinterpret_cast'
      , 'return'
      , 'sizeof'
      , 'static_assert'
      , 'static_cast'
      , 'struct'
      , 'switch'
      , 'template'
      , 'this'
      , 'throw'
      , 'true'
      , 'try'
      , 'typedef'
      , 'typeid'
      , 'typename'
      , 'union'
      , 'using'
      , 'virtual'
      , 'while'
      ]

    _MODIFIERS = [
        'static'
      , 'thread_local'
      , 'extern'
      , 'const'
      , 'volatile'
      , 'mutable'
      ]

    _DATA_TYPES = [
        'bool'
      , 'char'
      , 'short'
      , 'int'
      , 'unsigned'
      , 'signed'
      , 'long'
      , 'float'
      , 'double'
      , 'char16_t'
      , 'char32_t'
      , 'wchar_t'
      , 'void'
      ]

    _STRING_PREFIXES = ['u', 'U', 'L', 'u8', 'R', 'uR', 'UR', 'u8R', 'LR']

    class Token:
        BUILTIN_TYPE = 0
        IDENTIFIER = 1
        KEYWORD = 2
        MODIFIER = 3
        PREPROCESSOR = 4
        STRING_LITERAL = 5
        NUMERIC_LITERAL = 6
        COMMENT = 7
        UNCATEGORIZED = -1

        __KIND_STRINGS = {
            BUILTIN_TYPE: 'BT'
          , IDENTIFIER: 'ID'
          , KEYWORD: 'KW'
          , MODIFIER: 'MOD'
          , PREPROCESSOR: '#'
          , STRING_LITERAL: 'ST'
          , NUMERIC_LITERAL: 'NUM'
          , COMMENT: 'CMNT'
          , UNCATEGORIZED: 'UC'
          }

        def __init__(self, token, kind):
            self.token = token
            self.kind = kind

        def __repr__(self):
            return "{}('{}')".format(self.__KIND_STRINGS[self.kind], self.token)


    @staticmethod
    def _categorize_token(tok, prev_token):
        #print('tok={}'.format(repr(tok)))
        token = None
        replace_prev = False
        # Handle keywords
        if tok in SimpleCppLexer._KEYWORDS:
            token = SimpleCppLexer.Token(tok, SimpleCppLexer.Token.KEYWORD)
        # Handle type modifiers
        elif tok in SimpleCppLexer._MODIFIERS:
            token = SimpleCppLexer.Token(tok, SimpleCppLexer.Token.MODIFIER)
        # Handle builtin data types
        elif tok in SimpleCppLexer._DATA_TYPES:
            token = SimpleCppLexer.Token(tok, SimpleCppLexer.Token.BUILTIN_TYPE)
        # Join scope access to a previous token if latter is identifier
        elif tok == '::' and prev_token and prev_token.kind == SimpleCppLexer.Token.IDENTIFIER:
            token = prev_token
            token.token += tok
            replace_prev = True
        elif SimpleCppLexer._NUMBER_RE.match(tok):
            token = SimpleCppLexer.Token(tok, SimpleCppLexer.Token.NUMERIC_LITERAL)
        elif SimpleCppLexer._IDENTIFIER_RE.match(tok):
            if prev_token and prev_token.kind == SimpleCppLexer.Token.IDENTIFIER:
                token = prev_token
                token.token += tok
                replace_prev = True
            elif prev_token and prev_token.kind == SimpleCppLexer.Token.STRING_LITERAL:
                token = prev_token
                token.token += tok
                replace_prev = True
            else:
                token = SimpleCppLexer.Token(tok, SimpleCppLexer.Token.IDENTIFIER)
        else:
            token = SimpleCppLexer.Token(tok, SimpleCppLexer.Token.UNCATEGORIZED)
        return (token, replace_prev)


    @staticmethod
    def tokenize_string(snippet):
        tokens = []

        # If first char on a line is '#' -- whole string is a preprocessor
        if snippet.lstrip().startswith('#'):
            tokens.append(SimpleCppLexer.Token(snippet, SimpleCppLexer.Token.PREPROCESSOR))
            return tokens

        in_string = False
        in_block_comment = False
        in_cpp_comment = False
        string_char = None
        #print("tokens={}".format(repr(re.split('(\W+)', snippet))))
        for tok in re.split('(\W+)', snippet):              # Split the whole snippet by elementary tokens
            if not tok:                                     # Last item can be empty
                continue                                    # Just skip it!

            # If we r in a C++ style comment...
            if in_cpp_comment:
                # Just merge everything till the end to a previous token
                assert(tokens[-1].kind == SimpleCppLexer.Token.COMMENT)
                tokens[-1].token += tok
                continue

            # Iterate over tokenized string and look for
            # quotes (string literals) and comments...
            last_tokenized_pos = 0
            seen_slash = False
            seen_star = False
            seen_backslash = False
            want_next = False
            for pos, c in enumerate(tok):
                assert(not in_cpp_comment)
                if seen_backslash:                          # Go to next char after backclash
                    seen_backslash = False                  # Ok, backslash was counted...
                    continue
                elif in_string:
                    assert(string_char and not seen_slash and not seen_star)
                    # Ok, we r at string now... Check if current char is a quote symbol
                    # Check if string ends...
                    if c == string_char:
                        assert(tokens)
                        # Join chars before (including a current) to a prev token
                        tokens[-1].token += tok[last_tokenized_pos:pos+1]
                        in_string = False                   # Drop the flag!
                        last_tokenized_pos = pos + 1
                    elif c == '\\':
                        seen_backslash = True
                elif in_block_comment:
                    if seen_star and c == '/':              # Is end of block comment?
                        in_block_comment = False            # Drop the flag!
                        assert(tokens)
                        tokens[-1].token += tok[last_tokenized_pos:pos+1]
                        last_tokenized_pos = pos + 1
                    seen_star = bool(c == '*')
                # Starting a block or C++ style comment?
                elif seen_slash and (c == '/' or c == '*'):
                    if c == '/':
                        in_cpp_comment = True
                    else:
                        in_block_comment = True
                    # Append anything before it as a separate token
                    before = None
                    if 0 < (pos - 1):                       # Is this not a token start?
                        before = tok[last_tokenized_pos:pos-1]
                    if before:
                        token, replace_prev = SimpleCppLexer._categorize_token(
                            before
                          , tokens[-1] if tokens else None
                          )
                        if replace_prev:
                            tokens[-1] = token
                        else:
                            tokens.append(token)
                    if in_cpp_comment:
                        comment_start_text = tok[pos-1:]
                    else:
                        comment_start_text = tok[pos-1:pos+1]
                        last_tokenized_pos = pos+1
                    tokens.append(SimpleCppLexer.Token(comment_start_text, SimpleCppLexer.Token.COMMENT))
                    if in_cpp_comment:                      # C++ comments do not require further parsing...
                        want_next = True                    # Order to go for next token after this loop
                        break                               # immediately!
                elif c == '"' or c == "'":
                    in_string = True
                    string_char = c
                    # Append anything before it as a separate token
                    before = None
                    if 0 < pos:                             # Is this not a token start?
                        before = tok[last_tokenized_pos:pos]
                    if before:
                        token, replace_prev = SimpleCppLexer._categorize_token(
                            before
                          , tokens[-1] if tokens else None
                          )
                        if replace_prev:
                            tokens[-1] = token
                        else:
                            tokens.append(token)
                    switch_prev_token =  tokens \
                      and tokens[-1].kind == SimpleCppLexer.Token.IDENTIFIER \
                      and tokens[-1].token in SimpleCppLexer._STRING_PREFIXES
                    if switch_prev_token:
                        tokens[-1].kind = SimpleCppLexer.Token.STRING_LITERAL
                        tokens[-1].token += c
                    else:
                        tokens.append(SimpleCppLexer.Token(c, SimpleCppLexer.Token.STRING_LITERAL))
                    last_tokenized_pos = pos+1
                else:
                    seen_slash = bool(c == '/')
                    seen_backslash = bool(c == '\\')
                    seen_star = bool(c == '*')

            if want_next:                                   # If we are at C++ style comment
                continue                                    # Go for next tokens immediately

            assert(not in_cpp_comment)
            if in_block_comment:
                assert(tokens and tokens[-1].kind == SimpleCppLexer.Token.COMMENT)
                tokens[-1].token += tok[last_tokenized_pos:len(tok)]
            elif in_string:
                assert(tokens and tokens[-1].kind == SimpleCppLexer.Token.STRING_LITERAL)
                tokens[-1].token += tok[last_tokenized_pos:len(tok)]
            elif tok[last_tokenized_pos:len(tok)]:
                token, replace_prev = SimpleCppLexer._categorize_token(
                    tok[last_tokenized_pos:len(tok)]
                  , tokens[-1] if tokens else None
                  )
                if replace_prev:
                    assert(tokens)
                    tokens[-1] = token
                else:
                    tokens.append(token)
        return tokens

    @staticmethod
    def assemble_statement(tokens):
        return ''.join([t.token for t in tokens])



_BOOST_VARIANT_DETAILS_SNTZ_RE = re.compile('(T[0-9_]+)( = boost::detail::variant::void_);( T[0-9_]+\\2;)* (T[0-9_]+)\\2(;)?')
_BOOST_TAIL_OF_SOME_DETAILS_SNTZ_RE = re.compile('(, (boost::detail::variant::void_|mpl_::na))*>')
_GENERATED_TEMPLATE_PARAMS_SNTZ_RE = re.compile('((class|typename) +)?([A-Z][A-Za-z]*)([0-9]+)')
_GENERATED_FUNCTION_PARAMS_SNTZ_RE = re.compile('([A-Z][A-Za-z]*)([0-9]+)( [A-Za-z]+)(\\2)')
_STD_PLACEHOLDER = 'std::_Placeholder<'
_STD_PLACEHOLDERS_NS = 'std::placeholders::_'
_PARAMETER_PACK = ' ...'
# NOTE Order is important!
_BUILTIN_DATA_TYPES_MAPPING = [
    ('long unsigned int', 'unsigned long')
  , ('long int', 'long')
  , ('short int', 'short')
  , ('short unsigned int', 'unsigned short')
  , ('unsigned int', 'unsigned')
  ]


class SnippetSanitizer(object):

    def _boost_variant_details_cleaner(snippet):
        '''
            `Tn = boost::detail::variant::void_' parameters expansion inside of `[with'
        '''
        match = _BOOST_VARIANT_DETAILS_SNTZ_RE.search(snippet)
        if match:
            snippet = snippet[:match.start()] \
              + '{} to {}{}{}'.format(match.group(1), match.group(4), match.group(2), match.group(5)) \
              + snippet[match.end():]
        return snippet


    def _boost_remove_tail_of_some_details(snippet):
        return re.sub(_BOOST_TAIL_OF_SOME_DETAILS_SNTZ_RE, '>', snippet)


    def _format_matched_params(match, num_args):
        assert(match)
        kw = (match.group(1) if match.group(1) else '')
        result = kw + match.group(3) + match.group(4)
        if 1 < num_args:
            result += ', ..., ' + kw + match.group(3) + str(int(match.group(4)) + num_args)
        if num_args == 1:
            result += ', ' + kw + match.group(3) + str(int(match.group(4)) + num_args)
        return result


    def _generated_template_params_cleaner(snippet):
        '''
            `class Tn, ..., class Tm' template parameters
        '''
        last_match = None
        arg_num = 0
        delim = ''
        result = ''
        match = _GENERATED_TEMPLATE_PARAMS_SNTZ_RE.search(snippet)
        has_at_least_one_match = bool(match)
        while match:
            latest_match_pos = match.end()
            # Ok, smth found! Is there a previous match?
            do_match = True
            if last_match:
                do_remember_last_match = True
                do_flush = True
                # Check that previous match has same keyword and arg name
                if last_match.group(1) == match.group(1) and last_match.group(3) == match.group(3):
                    # Yep, same as previous!
                    # Check that a matched number is a next after the last match
                    if int(last_match.group(4)) + arg_num + 1 == int(match.group(4)):
                        arg_num += 1                        # Just increment next expected arg number
                        snippet = snippet[match.end():]     # Remove matched part from the input
                        do_match = False
                        match = _GENERATED_TEMPLATE_PARAMS_SNTZ_RE.search(snippet)
                        if snippet[0] == ',' and match and match.start() == 2:
                            do_flush = False
                        else:
                            do_remember_last_match = False
                if do_flush:
                    # Sequence of numbers is over! Flush the output!
                    result += delim + SnippetSanitizer._format_matched_params(last_match, arg_num)
                    if do_remember_last_match:
                        snippet = snippet[match.end():]     # Strip just matched text from the input
                        last_match = match                  # Remember this match for future
                        delim = ', '
                    else:
                        last_match = None
                        delim = ''
                    arg_num = 0
            else:
                assert(not arg_num)
                # Ok, first match!
                last_match = match                          # Remember for future use
                result += snippet[:match.start()]           # Append everything before a match to the result
                snippet = snippet[match.end():]             # Strip leading string from the input snippet
                if snippet[0] != ',':
                    result += (match.group(1) if match.group(1) else '') \
                      + match.group(3) + match.group(4)
                    last_match = None
                else:
                    do_match = False
                    match = _GENERATED_TEMPLATE_PARAMS_SNTZ_RE.search(snippet)
                    if match and match.start() != 2:
                        result += (last_match.group(1) if last_match.group(1) else '') \
                          + last_match.group(3) + last_match.group(4)
                        last_match = None

            if do_match:
                # Try to find again (more)...
                match = _GENERATED_TEMPLATE_PARAMS_SNTZ_RE.search(snippet)

        # If there was no matches at all...
        if not has_at_least_one_match:
            result = snippet                                # Set result to the original snippet
        else:
            if last_match is not None:
                result += delim + SnippetSanitizer._format_matched_params(last_match, arg_num) + snippet
            else:
                result += snippet
        return result


    def _template_decl_fixer_1(snippet):
        # TODO How to replace `class' w/ `typename'? All occurrences ...
        return snippet.replace('template<class ', 'template <class ') \
            .replace('template< typename ', 'template <typename ') \
            .replace('template<template ', 'template <template ')


    def _parameters_pack_fixer(snippet):
        '''Remove a space before '...'
            'class ... Args' to  'class... Args'
        '''
        idx = snippet.find(_PARAMETER_PACK)
        while idx != -1:
            # Do not remove space function declarations...
            if snippet[idx - 1] != ',':
                snippet = snippet[:idx] + snippet[idx+1:]
            idx = snippet.find(_PARAMETER_PACK, idx + len(_PARAMETER_PACK) - 1)
        return snippet


    def _hide_some_std_details(snippet):
        idx = snippet.find(_STD_PLACEHOLDER)
        while idx != -1:
            close_pos = snippet.find('>', idx)
            assert(close_pos != -1)
            snippet = snippet[:idx] \
              + _STD_PLACEHOLDERS_NS \
              + snippet[idx+len(_STD_PLACEHOLDER):close_pos] \
              + snippet[close_pos+1:]
            idx = snippet.find(_STD_PLACEHOLDER, idx + len(_STD_PLACEHOLDERS_NS))
        return snippet


    def _squeeze_right_angle_brackets(snippet):
        # Squeeze closing angle brackets
        pos = snippet.find('> >')
        while pos != -1:
            snippet = snippet[:pos] + '>>' + snippet[pos+3:]
            pos = snippet.find('> >', pos + 1)
        return snippet


    def _simplify_some_data_types(snippet):
        for what, to in _BUILTIN_DATA_TYPES_MAPPING:
            snippet = snippet.replace(what, to)
        return snippet


    _SANITIZERS = [
        _boost_variant_details_cleaner
      , _boost_remove_tail_of_some_details
      , _generated_template_params_cleaner
      , _template_decl_fixer_1
      , _parameters_pack_fixer
      , _hide_some_std_details
      , _squeeze_right_angle_brackets
      , _simplify_some_data_types
      ]


    @staticmethod
    def cleanup_snippet(snippet):
        for sanitizer in SnippetSanitizer._SANITIZERS:
            snippet = sanitizer(snippet)
        return snippet
