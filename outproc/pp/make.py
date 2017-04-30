# -*- coding: utf-8 -*-
#
# Output processor for `make`
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
#

from ..processing import Processor as ProcessorBase, force_processing, force_processing_requested
from .cmake import Processor as CMakeProcessor

import os
import re
import shlex
import sys


_KNOWN_COMPILERS = ['c++', 'g++', 'gcc']

_MAKE_MGS_RE = re.compile('make(\[[0-9]+\])?: ')
_MAKE_ERROR_MSG_RE = re.compile('make(\[[0-9]+\])?: \*\*\*')
_MAKE_MISC_PATH_RE = re.compile('.*(`.*\').*')


class Processor(ProcessorBase):

    @staticmethod
    def want_to_handle_current_command():
        # Try to handle an output if:
        # 0) `menuconfig` target is not specified in command line (when linux kernel get compiled)
        # 1) we are connected to a real terminal or force flag set in the current environment
        result = 'menuconfig' not in sys.argv \
          and 'oldconfig' not in sys.argv \
          and 'nconfig' not in sys.argv \
          and 'edit_cache' not in sys.argv \
          and (sys.stdout.isatty() or force_processing_requested())
        if result:
            force_processing()
        return result


    def __init__(self, config, binary):
        super().__init__(config, binary)
        self.error = config.get_color('error', 'normal+red')
        self.misc = config.get_color('misc', 'grey+bold')
        self.misc_path = config.get_color('misc-path', 'white')
        self.include = config.get_color('compiler-option-I', 'green')
        self.macro_define = config.get_color('compiler-option-D', 'yellow')
        self.macro_undefine = config.get_color('compiler-option-U', 'yellow')
        self.optimization = config.get_color('compiler-option-f', 'cyan')
        self.target_arch = config.get_color('compiler-option-m', 'magenta')
        self.warning = config.get_color('compiler-option-W', 'yellow+bold')
        self.lib_paths = config.get_color('compiler-option-L', 'green')
        self.cmake_processor = CMakeProcessor(config, binary)


    def _detect_make_message(self, line):
        if _MAKE_ERROR_MSG_RE.match(line):
            return (True, True)
        elif _MAKE_MGS_RE.match(line):
            return (True, False)
        return (False, False)


    def _colorize_with_misc(self, line):
        return self.misc + line + self.config.color.reset


    def _is_look_like_cmake_compile(self, line):
        ''' Try to parse possible cmake compile command line...
            maybe we can higlight gcc options?

            CMake + make produce compile commands in the following format:
                cd <work-dir> && <compiler> <options>

            This function will try to detect first 3 tokens, and if everything
            is found, the 4th assumed to be a compiler executable name...
        '''
        score = 0
        args = None
        try:
            args = shlex.split(line)
        except:
            return (False, [], 0)
        assert(args is not None)
        i = 0
        for arg in args:
            if score == 4:
                return (True, args, i)
            elif score == 0 and arg == 'cd' or arg == '\x1b[0mcd':
                score += 1
            if score == 0 and os.path.isfile(arg) and os.path.basename(arg) in _KNOWN_COMPILERS:
                score += 4
            elif score == 1 and os.path.isdir(arg):
                score += 1
            elif score == 2 and arg == '&&':
                score += 1
            elif score == 3 and os.path.isfile(arg) and os.path.basename(arg) in _KNOWN_COMPILERS:
                score += 1
            i += 1
        return (False, args, i)


    def _try_get_color_for_option(self, option):
        paint_next_arg = (len(option) == 2)
        if option.startswith('-I'):
            return (self.include, paint_next_arg)
        elif option.startswith('-L'):
            return (self.lib_paths, paint_next_arg)
        elif option.startswith('-D'):
            return (self.macro_define, paint_next_arg)
        elif option.startswith('-U'):
            return (self.macro_undefine, paint_next_arg)
        elif option.startswith('-f'):
            return (self.optimization, False)
        elif option.startswith('-m'):
            return (self.target_arch, False)
        elif option.startswith('-W') and not option.startswith('-Wl,'):
            return (self.warning, False)
        return (None, False)


    def _colorize_option(self, option, color, line, last_find_idx):
        assert(
                isinstance(option, str)
            and isinstance(color, str)
            and isinstance(line, str)
            and isinstance(last_find_idx, int)
          )
        # Find corresponding option at raw line
        pos = line.find(option, last_find_idx)
        assert(pos != -1)
        # Colorise it
        line = line[:pos] + color + line[pos:pos+len(option)] + self.config.color.reset + line[pos+len(option):]
        last_find_idx = pos + len(color) + len(self.config.color.reset)
        return (line, last_find_idx)


    def handle_line(self, line):
        is_make_message, is_error_message = self._detect_make_message(line)
        if is_make_message:
            line = self.misc + line
            if is_error_message:
                stars_idx = line.index('***')
                line = line[:stars_idx] + self.error + line[stars_idx:]
            else:
                # Highlight path enclosed in `'
                pos = line.find('`')
                if pos != -1:
                    close_pos = line.index("'")
                    assert(close_pos != -1)
                    close_pos += 1
                    line = line[:pos] + self.misc_path + line[pos:close_pos] + self.misc + line[close_pos:]
            line += self.config.color.reset
        # Lines started w/ '/usr/bin/make' paint w/ `misc' color
        elif line.startswith(self.binary):
            return self._colorize_with_misc(line)
        # Lines started w/ '/usr/bin/cmake' paint w/ `misc' color
        # (it is also a not interested information)
        elif line.startswith('/usr/bin/cmake'):
            return self._colorize_with_misc(line)
        elif self.cmake_processor.looks_like_cmake_line(line):
            return self.cmake_processor.handle_line(line)
        else:
            is_compiler_cmd_line, args, first_compiler_option_idx = self._is_look_like_cmake_compile(line)
            last_find_idx = 0
            option_color = None
            paint_next_arg = False
            if is_compiler_cmd_line:
                for i in range(first_compiler_option_idx, len(args)):
                    if paint_next_arg:
                        line, last_find_idx = self._colorize_option(args[i], option_color, line, last_find_idx)
                        paint_next_arg = False
                        continue
                    # Try to get color for current option
                    option_color, paint_next_arg = self._try_get_color_for_option(args[i])
                    if option_color is not None:
                        line, last_find_idx = self._colorize_option(args[i], option_color, line, last_find_idx)

        return line
