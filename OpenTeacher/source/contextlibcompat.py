#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
#
#	This file is part of OpenTeacher.
#
#	OpenTeacher is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	OpenTeacher is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with OpenTeacher.  If not, see <http://www.gnu.org/licenses/>.

#adds some functionality of Python 3 to Python 2.

import warnings
import contextlib

@contextlib.contextmanager
def ignored(*errors):
    try:
        yield
    except errors:
        pass

realClosing = contextlib.closing
def closing(thing):
	warnings.warn("Almost all uses of contextlib.closing can be removed after Python 2.6 support is dropped.")
	return realClosing(thing)

contextlib.ignored = ignored
contextlib.closing = closing
