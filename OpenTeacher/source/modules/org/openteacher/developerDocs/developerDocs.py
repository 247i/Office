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

class DeveloperDocumentationModule(object):
	"""A centralized place for all OpenTeacher developer documentation.
	   The directory tree of restructuredtext files that contains the
	   actual documentation is available via the
	   'developerDocumentationBaseDirectory' attribute.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(DeveloperDocumentationModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "devDocs"

	def enable(self):
		self.developerDocumentationBaseDirectory = self._mm.resourcePath("docs")

		self.active = True

	def disable(self):
		self.active = False

		del self.developerDocumentationBaseDirectory

def init(moduleManager):
	return DeveloperDocumentationModule(moduleManager)
