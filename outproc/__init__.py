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

import sys
import traceback

# Inject nested module into the scope
from outproc.config import Config


SYSCONFDIR = '/etc/outproc'

log = None
try:
    import portage.output
    log = portage.output.EOutput()
except ImportError:
    class FakeLogger(object):
        def einfo(self, msg):
            print(msg)
        def eerror(self, msg):
            print(msg, file=sys.stderr)
        def ewarn(self, msg):
            print(msg)

    log = FakeLogger()


class Processor(object):

    def __init__(self, config, binary):
        self.config = config
        self.binary = binary

    def handle_line(self, line):
        return line

    def eof(self):
        pass

    @staticmethod
    def config_file_name(module_name):
        return module_name + '.conf'


def report_error_with_backtrace(intro_message):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    log.eerror(
        '{} due {} exception: {}'.format(
            intro_message
          , exc_type.__name__
          , exc_value
          )
        )
    for t in traceback.extract_tb(exc_traceback)[1:]:
        log.eerror('  {}:{}: at {}'.format(t[0], t[1], t[2]))
        log.eerror('    {}'.format(t[3]))
