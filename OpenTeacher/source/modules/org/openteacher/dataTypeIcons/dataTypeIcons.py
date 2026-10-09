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

class DataTypeIconsModule(object):
	"""This module provides icons for types of data OpenTeacher can
	   handle, one example is for 'words'.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(DataTypeIconsModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "dataTypeIcons"

	def findIcon(self, type):
		"""Returns a file path for the data type 'type'. Raises KeyError
		   if no icon can be found for 'type'.

		"""
		return {
			"words": self._mm.resourcePath("icons/words.png"),
			"topo": self._mm.resourcePath("icons/topo.png"),
			"media": self._mm.resourcePath("icons/media.png"),
		}[type]

	def enable(self):
		self.active = True

	def disable(self):
		self.active = False

def init(moduleManager):
	return DataTypeIconsModule(moduleManager)
