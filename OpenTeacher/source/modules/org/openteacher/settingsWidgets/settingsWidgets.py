#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Marten de Vries
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

class SettingsWidgetsModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SettingsWidgetsModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "settingsWidgets"

		self.uses = (
			self._mm.mods(type="settingsWidget"),
		)

	def enable(self):
		self.widgets = {}
		for settingsWidget in self._mm.mods("active", type="settingsWidget"):
			self.widgets[settingsWidget.widgetType] = settingsWidget.createWidget

		self.active = True

	def disable(self):
		self.active = False

		del self.widgets

def init(moduleManager):
	return SettingsWidgetsModule(moduleManager)
