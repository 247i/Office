#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Marten de Vries
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

import sys

class ThemeModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(ThemeModule, self).__init__(*args, **kwargs)

		self._mm = moduleManager
		self.type = "theme"
		self.requires = (
			self._mm.mods(type="ui"),
		)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._uiModule = self._modules.default("active", type="ui")

		if "--blacknwhite" in sys.argv or "-bw" in sys.argv:
			self.installTheme()

		self.active = True

	def installTheme(self):
		stylesheet = u"""
			* {
				color:white;
				background-color:#444;
				alternate-background-color:#555;
				selection-background-color:#888;
			}

			QToolBar, QToolButton {
				background-color:#333;
			}
		"""

		self._uiModule.addStyleSheetRules(stylesheet)
		self._uiModule.setStyle("plastique")

	def disable(self):
		self.active = False

		del self._modules
		del self._uiModule

def init(moduleManager):
	return ThemeModule(moduleManager)
