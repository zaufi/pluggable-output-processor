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

import os
import re
import sys

_FG_COLOR_IN_ESC_SEQ_RE = re.compile('([^\d])3(\d)')

def is_real_term():
    return sys.stdout.isatty()

def get_width():
    return os.get_terminal_size().columns if sys.stdout.isatty() else 100500

def move_above(lines):
    assert(isinstance(lines, int))
    return '\x1b[{}A'.format(lines)


def move_below(lines):
    assert(isinstance(lines, int))
    return '\x1b[{}B'.format(lines)


def move_to_col(col):
    assert(isinstance(col, int) and col < os.get_terminal_size().columns)
    return '\x1b[{}G'.format(col)


def pos_to_offset(line, requested_pos):
    ''' Get offset into a string for given position (column) skipping "invisible"
        escape sequences.

        TODO Consider other than color ESC sequences
    '''
    assert(isinstance(line, str) and isinstance(requested_pos, int) and requested_pos < len(line))
    inside_esc_seq = False
    current_pos = 0
    for i, c in enumerate(line):
        if c == '\x1b':                                     # Start of ESC sequence
            assert(not inside_esc_seq)
            inside_esc_seq = True
        elif inside_esc_seq:                                # Already in a ESC sequence
            if c == 'm':                                    # Is end of escape sequence?
                inside_esc_seq = False
        else:
            if current_pos == requested_pos:
                return i
            current_pos += 1
    assert(not 'Smth wrong w/ input sequence!')


def fg2bg(color):
    ''' Turn a foreground color into a background'''
    # TODO How to use .re.sub() instead? The problem: replace expression
    # must contain a reference to the first part (i.e. '\\1') and the next
    # char (we want to replace '3' --> '4') is a number, so finally we have
    # '\\14' -- right, it is an invalid reference...
    assert(isinstance(color, str))

    match = _FG_COLOR_IN_ESC_SEQ_RE.search(color)
    if match:
        color = color[:match.start() + 1] + '4' + color[match.start() + 2:]
    return color


def column_formatter(items_count, columns):
    ''' Generator yelding indices up to `items_count` in a way
        like *nix shells columnize lists
    '''
    rows = int(items_count / columns) + int(bool(items_count % columns))
    for row in range(0, rows):
        for idx in range(row, items_count, rows):
            yield idx
        yield -1
