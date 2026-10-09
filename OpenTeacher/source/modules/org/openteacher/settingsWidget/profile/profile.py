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
	class SettingsWidget(QtGui.QComboBox):
		def __init__(self, profiles, setting, *args, **kwargs):
			super(SettingsWidget, self).__init__(*args, **kwargs)

			self._setting = setting

			# Add the options
			for profile in profiles:
				if not profile.desc["advanced"]:
					self.addItem(profile.desc["niceName"], profile.desc["name"])
			self.setCurrentIndex(self.findData(setting["value"]))
			self.currentIndexChanged.connect(self._valueChanged)

		def _valueChanged(self):
			self._setting["value"] = unicode(self.itemData(self.currentIndex()).toString())
	return SettingsWidget

class SettingsWidgetModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SettingsWidgetModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "settingsWidget"

		self.requires = (
			self._mm.mods(type="ui"),
		)
		self.uses = (
			self._mm.mods(type="profileDescription"),
		)

	def createWidget(self, *args, **kwargs):
		profiles = sorted(
			self._mm.mods("active", type="profileDescription"),
			key=lambda p: p.desc["niceName"]
		)
		return SettingsWidget(profiles, *args, **kwargs)

	def enable(self):
		global QtGui
		try:
			from PyQt4 import QtGui
		except ImportError:
			return
		global SettingsWidget
		SettingsWidget = getSettingsWidget()

		self.widgetType = "profile"
		self._modules = set(self._mm.mods(type="modules")).pop()

		self.active = True

	def disable(self):
		self.active = False

		del self.widgetType
		del self._modules

def init(moduleManager):
	return SettingsWidgetModule(moduleManager)
