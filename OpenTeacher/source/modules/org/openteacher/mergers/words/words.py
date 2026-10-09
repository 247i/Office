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

import copy
import contextlib

class WordsMergerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(WordsMergerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "merger"
		self.dataType = "words"

	def merge(self, baseLesson, otherLesson):
		merge = copy.deepcopy(baseLesson)
		with contextlib.ignored(KeyError):
			merge["list"]["items"].extend(otherLesson["list"]["items"])
		with contextlib.ignored(KeyError):
			merge["list"]["tests"].extend(otherLesson["list"]["tests"])

		return merge

	def enable(self):
		self.active = True

	def disable(self):
		self.active = False

def init(moduleManager):
	return WordsMergerModule(moduleManager)
