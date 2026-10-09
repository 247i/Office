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

class LoaderGuiModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(LoaderGuiModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "loaderGui"
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="loader"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("loaderGui.py",)

	def enable(self):
		global QtGui
		try:
			from PyQt4 import QtGui
		except ImportError:
			return
		self._modules = next(iter(self._mm.mods(type="modules")))
		self._uiModule = self._modules.default("active", type="ui")

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
		global _, ngettext
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

	def disable(self):
		self.active = False

		del self._modules
		del self._uiModule

	def loadFromLesson(self, type, lessonData):
		try:
			self._modules.default(
				"active",
				type="loader"
			).loadFromLesson(type, lessonData)
		except NotImplementedError:
			QtGui.QMessageBox.critical(
				self._uiModule.qtParent,
				_("Can't show the result"),
				_("Can't open the resultive word list, because it can't be shown.")
			)
			raise

def init(moduleManager):
	return LoaderGuiModule(moduleManager)
