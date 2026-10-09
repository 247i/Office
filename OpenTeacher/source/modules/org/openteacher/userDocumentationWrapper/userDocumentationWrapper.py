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

class UserDocumentationWrapperModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(UserDocumentationWrapperModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "userDocumentationWrapper"
		self.requires = (
			self._mm.mods(type="metadata"),
		)

	def wrap(self, html):
		metadata = self._modules.default("active", type="metadata").metadata

		t = pyratemp.Template(filename=self._mm.resourcePath("wrapper.html"))
		return t(**{
			"content": html,
			"QColor": QtGui.QColor,
			"hue": metadata["mainColorHue"],
		})

	def enable(self):
		global pyratemp, QtGui
		try:
			from PyQt4 import QtGui
			import pyratemp
		except ImportError:
			return

		self._modules = next(iter(self._mm.mods(type="modules")))

		self.active = True

	def disable(self):
		self.active = False

		del self._modules

def init(moduleManager):
	return UserDocumentationWrapperModule(moduleManager)
