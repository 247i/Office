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
		def __init__(self, languages, setting, *args, **kwargs):
			super(SettingsWidget, self).__init__(*args, **kwargs)

			self._setting = setting

			for code in sorted(languages):
				self.addItem(languages[code], code)
			self.insertItem(0, _("System default"), None)
			self.insertSeparator(1)

			self.highlighted.connect(self._valueChanged)
			i = self.findData(setting["value"])
			if i == -1:
				#this can be the case when the setting is 'System default',
				#because that text is translated itself.
				self.setCurrentIndex(0)
			else:
				self.setCurrentIndex(i)

		def _valueChanged(self, index):
			item = self.model().item(index)
			self._setting["value"] = unicode(item.data(QtCore.Qt.UserRole).toString())
	return SettingsWidget

class SettingsWidgetModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SettingsWidgetModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "settingsWidget"

		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="friendlyTranslationNames"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("language.py",)

	@property
	def languages(self):
		return self._modules.default(
			"active",
			type="friendlyTranslationNames"
		).friendlyNames

	def createWidget(self, *args, **kwargs):
		return SettingsWidget(self.languages, *args, **kwargs)

	def _retranslate(self):
		"""this only installs the translator, but does not update the
		   settings widget. It's the callers responsibility to ask for
		   a new settings widget on retranslate().

		"""
		global _
		global ngettext

		#Install translator
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		global SettingsWidget
		SettingsWidget = getSettingsWidget()

		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.widgetType = "language"
		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self.widgetType

def init(moduleManager):
	return SettingsWidgetModule(moduleManager)
