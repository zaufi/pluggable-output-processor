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
#from context import data_dir_base, output_dir_base, preapre_properties
from onixs.bsci.cli import Application
from onixs.bsci.contextmanager import change_work_dir

# Standard imports
import os
import pathlib
import pytest
import sys
import unittest.mock


# Add CLI option
def pytest_addoption(parser):
    parser.addoption(
        '--save-patterns'
      , action='store_true'
        # TODO Better description
      , help='store matching patterns instead of checking them'
      )


def ensure_fresh_directory(directory):
    assert isinstance(directory, pathlib.Path)

    if directory.exists():
        # Remove previous results possible here
        shutil.rmtree(str(directory))

    directory.mkdir(parents=True)


@pytest.fixture(scope='function')
def output_dir(request):
    result = pathlib.Path(
        output_dir_base()
      , request.module.__name__
      )
    if request.cls is not None:
        result /= request.cls.__name__
    result /= request.function.__name__

    ensure_fresh_directory(result)

    yield result
