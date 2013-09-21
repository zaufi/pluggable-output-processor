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
    _NUMBER_RE = re.compile('^(\d+(\.\d*)?f?)$')
    _KEYWORDS = [
        'struct'
      , 'class'
      , 'enum'
      , 'union'
      , 'typedef'
      , 'using'
      , 'typename'
      , 'namespace'
      , 'template'
      , 'if'
      , 'else'
      , 'do'
      , 'while'
      , 'switch'
      , 'case'
      , 'for'
      , 'inline'
      , 'register'
      , 'auto'
      , 'throw'
      , 'try'
      , 'catch'
      , 'noexcept'
      , 'friend'
      , 'virtual'
      , 'override'
      , 'final'
      , 'public'
      , 'protected'
      , 'private'
      , 'sizeof'
      , 'alignof'
      , 'decltype'
      , 'return'
      , 'operator'
      , 'true'
      , 'false'
      , 'this'
      , 'static_cast'
      , 'const_cast'
      , 'dynamic_cast'
      , 'reinterpret_cast'
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
      , 'long'
      , 'float'
      , 'double'
      , 'char16_t'
      , 'char32_t'
      , 'wchar_t'
      , 'void'
      ]

    class Token:
        BUILTIN_TYPE = 0
        IDENTIFIER = 1
        KEYWORD = 2
        MODIFIER = 3
        PREPROCESSOR = 4
        STRING_LITERAL = 5
        NUMERIC_LITERAL = 6
        UNCATEGORIZED = -1

        __KIND_STRINGS = {
            BUILTIN_TYPE: 'BT'
          , IDENTIFIER: 'ID'
          , KEYWORD: 'KW'
          , MODIFIER: 'MOD'
          , PREPROCESSOR: '#'
          , STRING_LITERAL: 'ST'
          , NUMERIC_LITERAL: 'NUM'
          , UNCATEGORIZED: 'UC'
          }

        def __init__(self, token, kind):
            self.token = token
            self.kind = kind

        def __repr__(self):
            return "{}('{}')".format(self.__KIND_STRINGS[self.kind], self.token)


    @staticmethod
    def tokenize_string(snippet):
        tokens = []

        # If first char on a line is '#' -- whole string is a preprocessor
        if snippet.lstrip().startswith('#'):
            tokens.append(SimpleCppLexer.Token(snippet, SimpleCppLexer.Token.PREPROCESSOR))
            return tokens

        merge_identifier = False
        for tok in re.split('(\W+)', snippet):              # Split the whole snippet by elementary tokens
            if not tok:                                     # Last item can be empty
                continue                                    # Just skip it!
            elif tok in SimpleCppLexer._KEYWORDS:
                tokens.append(SimpleCppLexer.Token(tok, SimpleCppLexer.Token.KEYWORD))
            elif tok in SimpleCppLexer._MODIFIERS:
                tokens.append(SimpleCppLexer.Token(tok, SimpleCppLexer.Token.MODIFIER))
            elif tok in SimpleCppLexer._DATA_TYPES:
                tokens.append(SimpleCppLexer.Token(tok, SimpleCppLexer.Token.BUILTIN_TYPE))
            elif tok == '::' and tokens and tokens[-1].kind == SimpleCppLexer.Token.IDENTIFIER:
                tokens[-1].token = tokens[-1].token + tok
                merge_identifier = True
            elif SimpleCppLexer._NUMBER_RE.match(tok):
                tokens.append(SimpleCppLexer.Token(tok, SimpleCppLexer.Token.NUMERIC_LITERAL))
            elif SimpleCppLexer._IDENTIFIER_RE.match(tok):
                if merge_identifier:
                    tokens[-1].token = tokens[-1].token + tok
                    merge_identifier = False
                else:
                    tokens.append(SimpleCppLexer.Token(tok, SimpleCppLexer.Token.IDENTIFIER))
            else:
                tokens.append(SimpleCppLexer.Token(tok, SimpleCppLexer.Token.UNCATEGORIZED))
        return tokens

    @staticmethod
    def assemble_statement(tokens):
        return ''.join([t.token for t in tokens])



_BOOST_VARIANT_DETAILS_SNTZ_RE = re.compile('(T[0-9_]+)( = boost::detail::variant::void_);( T[0-9_]+\\2;)* (T[0-9_]+)\\2(;)?')
_GENERATED_TEMPLATE_PARAMS_SNTZ_RE = re.compile('(class|typename) ([A-Z])([0-9]+),( \\1 \\2[0-9]+,)* \\1 \\2([0-9]+)')
_GENERATED_TEMPLATE_PARAMS_INST_SNTZ_RE = re.compile('([A-Z])([0-9]+),( \\1[0-9]+,)* \\1([0-9]+)')


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


    def _generated_template_params_cleaner(snippet):
        '''
            `class Tn, ..., class Tm' template parameters
        '''
        match = _GENERATED_TEMPLATE_PARAMS_SNTZ_RE.search(snippet)
        if match:
            snippet = snippet[:match.start()] \
                + '{} {}{}, ..., {} {}{}'.format(
                    match.group(1)
                  , match.group(2)
                  , match.group(3)
                  , match.group(1)
                  , match.group(2)
                  , match.group(5)
                  ) \
                + snippet[match.end():]
        return snippet


    def _generated_template_params_inst_cleaner(snippet):
        ''' - `Tn, ..., Tm' template parameters '''
        match = _GENERATED_TEMPLATE_PARAMS_INST_SNTZ_RE.search(snippet)
        while match:
            snippet = snippet[:match.start()] \
                + '{}{}, ..., {}{}'.format(
                    match.group(1)
                  , match.group(2)
                  , match.group(1)
                  , match.group(4)
                  ) \
                + snippet[match.end():]
            match = _GENERATED_TEMPLATE_PARAMS_INST_SNTZ_RE.search(snippet)
        return snippet


    _SANITIZERS = [
        _boost_variant_details_cleaner
      , _generated_template_params_cleaner
      , _generated_template_params_inst_cleaner
      ]


    @staticmethod
    def cleanup_snippet(snippet):
        for sanitizer in SnippetSanitizer._SANITIZERS:
            snippet = sanitizer(snippet)
        return snippet
