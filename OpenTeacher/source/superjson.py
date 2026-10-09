#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2013, Marten de Vries
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

"""A JSON module that dumps collections.Mapping and collections.Sequence
   inheriting objects too. It's meant to be used next to, not instead
   of, the builtin json module. (And that's why it only implements a
   subset of functions)

"""

import json
import collections

class _Dumper(object):
	def _abcToStandardTypes(self, obj):
		if isinstance(obj, collections.Mapping):
			return dict(obj)
		elif isinstance(obj, collections.Sequence):
			return list(obj)
		if self._default:
			return self._default(obj)
		raise TypeError("Couldn't convert '%s' to JSON." % obj)

	def dumps(self, obj, separators=None, default=None):
		self._default = default
		return json.dumps(
			obj,
			separators=separators,
			default=self._abcToStandardTypes
		)

dumps = _Dumper().dumps
