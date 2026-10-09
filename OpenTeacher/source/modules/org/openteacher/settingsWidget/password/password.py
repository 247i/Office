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

def getSettingsWidget():
	class SettingsWidget(QtGui.QLineEdit):
		def __init__(self, setting, *args, **kwargs):
			super(SettingsWidget, self).__init__(*args, **kwargs)

			self._setting = setting

			self.setEchoMode(QtGui.QLineEdit.Password)
			self.setText(setting["value"])
			self.textChanged.connect(self._valueChanged)

		def _valueChanged(self, text):
			self._setting["value"] = unicode(text)
	return SettingsWidget

class SettingsWidgetModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SettingsWidgetModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "settingsWidget"

		self.requires = (
			self._mm.mods(type="ui"),
		)

	def createWidget(self, *args, **kwargs):
		return SettingsWidget(*args, **kwargs)

	def enable(self):
		global QtGui
		try:
			from PyQt4 import QtGui
		except ImportError:
			return
		global SettingsWidget
		SettingsWidget = getSettingsWidget()

		self.widgetType = "password"
		self.active = True

	def disable(self):
		self.active = False

		del self.widgetType

def init(moduleManager):
	return SettingsWidgetModule(moduleManager)
