#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
#	Copyright 2011, Milan Boers
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

import os

class FileDialogsModule(object):
	"""The file dialogs; used to get filenames for loading and saving."""

	def __init__(self, moduleManager, *args, **kwargs):
		super(FileDialogsModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "fileDialogs"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="ui"),
		)

	def getSavePath(self, onSuccess, startdir, exts, default, onError=None):
		stringExts = []

		filters = [name + " (*." + ext + ")" for ext, name in exts]

		fileDialog = QtGui.QFileDialog()
		fileDialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
		fileDialog.setWindowTitle(_("Choose file to save"))
		fileDialog.setNameFilters(filters)
		fileDialog.selectNameFilter(default[1] + " (*." + default[0] + ")")
		fileDialog.setDirectory(startdir)

		tab = self._ui.addCustomTab(fileDialog, previousTabOnClose=True)
		tab.title = fileDialog.windowTitle()
		tab.closeRequested.handle(tab.close)
		fileDialog.finished.connect(tab.close)

		def onFileDialogAccepted():
			ext = unicode(fileDialog.selectedNameFilter().split("(*")[1].split(")")[0])
			filename = unicode(fileDialog.selectedFiles()[0])
			extensions = [u"." + e[0] for e in exts]
			if os.path.splitext(filename)[1] not in extensions:
				filename += ext
			onSuccess(filename)
		fileDialog.accepted.connect(onFileDialogAccepted)
		if onError:
			fileDialog.rejected.connect(onError)

	def getLoadPath(self, onSuccess, startdir, exts, fileType=None, onError=None):
		if not fileType:
			fileType = _("Lessons")
		stringExts = ("*." + ext for ext, name in exts)
		filter = u"%s (%s)" % (fileType, u" ".join(stringExts))

		fileDialog = QtGui.QFileDialog()
		fileDialog.setFileMode(QtGui.QFileDialog.ExistingFile)
		fileDialog.setWindowTitle(_("Choose file to open"))
		fileDialog.setFilter(filter)
		fileDialog.setDirectory(startdir)

		tab = self._ui.addCustomTab(fileDialog, previousTabOnClose=True)
		tab.title = fileDialog.windowTitle()
		tab.closeRequested.handle(tab.close)
		fileDialog.finished.connect(tab.close)

		def onFileDialogAccepted():
			onSuccess(unicode(fileDialog.selectedFiles()[0]))
		fileDialog.accepted.connect(onFileDialogAccepted)

		if onError:
			fileDialog.rejected.connect(onError)

	def enable(self):
		global QtGui
		try:
			from PyQt4 import QtGui
		except ImportError:
			#remain inactive
			return
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._ui = self._modules.default("active", type="ui")

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
		global _
		global ngettext
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
		del self._ui

def init(moduleManager):
	return FileDialogsModule(moduleManager)
