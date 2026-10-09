#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Milan Boers
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

import weakref

class ResultsDialogModule(object):
	"""An in the main window embedded dialog that can be used to view
	   test results.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(ResultsDialogModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "resultsDialog"
		self.requires = (
			self._mm.mods(type="testViewer"),
			self._mm.mods(type="ui"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChangeDone.handle(self._retranslate)

		self._dialogs = set()

		self.active = True

	def _retranslate(self):
		for ref in self._dialogs:
			dialog = ref()
			if dialog:
				dialog.tab.title = dialog.windowTitle()

	def disable(self):
		self.active = False

		del self._modules
		del self._dialogs

	def showResults(self, list, dataType, test):
		"""Show results of a test. It's assumes that list has the type
		   'dataType', and that 'test' is a test about it.

		"""
		resultsWidget = self._modules.default(
			"active",
			type="testViewer"
		).createTestViewer(list, dataType, test)

		uiModule = self._modules.default(type="ui")
		tab = uiModule.addCustomTab(resultsWidget)
		tab.title = resultsWidget.windowTitle()
		tab.closeRequested.handle(tab.close)
		resultsWidget.tab = tab

		self._dialogs.add(weakref.ref(resultsWidget))

def init(moduleManager):
	return ResultsDialogModule(moduleManager)
