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

# Project specific imports

# Standard imports

log = None
try:
    import portage.output
    log = portage.output.EOutput()
except ImportError:
    class FakeLogger(object):
        def einfo(self, msg):
            print(' \x1b[0;32;1m*\x1b[0m {}'.format(msg))
        def eerror(self, msg):
            print(' \x1b[0;31;1m*\x1b[0m {}'.format(msg), file=sys.stderr)
        def ewarn(self, msg):
            print(' \x1b[0;33;1m*\x1b[0m {}'.format(msg))

    log = FakeLogger()
