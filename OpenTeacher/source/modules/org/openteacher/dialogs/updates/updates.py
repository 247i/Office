#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
#	Copyright 2012, Milan Boers
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

import threading

def getUpdatesDialog():
	class UpdatesDialog(QtGui.QDialog):
		"""The updates dialog; it asks the user if he/she wants to
		   install updates.

		"""
		def __init__(self, updates, rememberChoice, *args, **kwargs):
			super(UpdatesDialog, self).__init__(*args, **kwargs)

			self._updatesLength = len(updates)

			self.label = QtGui.QLabel()
			self.checkBox = QtGui.QCheckBox()
			self.checkBox.setChecked(rememberChoice)
			buttonBox = QtGui.QDialogButtonBox(
				QtGui.QDialogButtonBox.No |
				QtGui.QDialogButtonBox.Yes
			)
			buttonBox.button(QtGui.QDialogButtonBox.Yes).setAutoDefault(True)
			buttonBox.button(QtGui.QDialogButtonBox.No).setAutoDefault(False)
			buttonBox.accepted.connect(self.accept)
			buttonBox.rejected.connect(self.reject)

			layout = QtGui.QVBoxLayout()
			layout.addWidget(self.label)
			layout.addStretch()
			layout.addWidget(self.checkBox)
			layout.addWidget(buttonBox)
			
			self.setLayout(layout)

		def retranslate(self):
			self.setWindowTitle(ngettext(
				"Update available",
				"Updates available",
				self._updatesLength
			))
			self.label.setText(ngettext(
				"There is %s update available, do you want to update?",
				"There are %s updates available, do you want to update?",
				self._updatesLength
			) % self._updatesLength)
			self.checkBox.setText(_("Remember my choice"))

		@property
		def rememberChoice(self):
			return self.checkBox.isChecked()
	return UpdatesDialog

class UpdatesDialogModule(object):
	"""Provides the updates dialog. It is completely self-contained, so
	   no public API.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(UpdatesDialogModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "updatesDialog"
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="updates"),
			self._mm.mods(type="dataStore"),
		)
		self.uses = (
			self._mm.mods(type="settings"),
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("updates.py",)

	def _retranslate(self):
		#Translations
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

		if hasattr(self, "_ud"):
			#if update dialog opened, retranslate
			self._ud.retranslate()
		if hasattr(self, "_tab"):
			#same situation
			self._tab.title = _("Updates")

		self._rememberChoiceSetting.update({
			"name": _("Remember if I want to install updates or not"),
			"category": _("Updates"),
		})

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		global UpdatesDialog
		UpdatesDialog = getUpdatesDialog()

		class Signals(QtCore.QObject):
			finishedFetching = QtCore.pyqtSignal()
		self._Signals = Signals()

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._dataStore = self._modules.default(type="dataStore").store

		try:
			settings = self._modules.default(type="settings")
		except IndexError, e:
			self._rememberChoiceSetting = {
				"value": False,
			}
		else:
			self._rememberChoiceSetting = settings.registerSetting(**{
				"internal_name": "org.openteacher.updatesDialog.rememberChoice",
				"type": "boolean",
				"defaultValue": False,
			})

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self._dataStore["org.openteacher.updatesDialog.userDidUpdatesLastTime"] = False
		self.active = True

		self._Signals.finishedFetching.connect(self._showUpdatesDialog)

		# Fetch updates thread
		self._thread = threading.Thread(target=self._checkUpdates)
		self._thread.start()

	def _checkUpdates(self):
		if self._rememberChoiceSetting["value"] and not self._dataStore["org.openteacher.updatesDialog.userDidUpdatesLastTime"]:
			#The user doesn't want to be bothered with updates
			return
		self._updatesMod = self._modules.default("active", type="updates")
		with contextlib.ignored(IOError):
			#IOError: error downloading updates, silently fail.
			self._updates = self._updatesMod.updates

		if not self._updates:
			return

		self._Signals.finishedFetching.emit()
	
	def _showUpdatesDialog(self):
		if self._rememberChoiceSetting["value"] and self._dataStore["org.openteacher.updatesDialog.userDidUpdatesLastTime"]:
			self._updatesMod.update()
		else:
			self._ud = UpdatesDialog(self._updates, self._rememberChoiceSetting["value"])
			self._tab = self._modules.default("active", type="ui").addCustomTab(self._ud)
			self._tab.closeRequested.handle(self._ud.rejected.emit)
			self._ud.accepted.connect(self._accepted)
			self._ud.rejected.connect(self._rejected)
			self._retranslate()

	def _accepted(self):
		self._rememberChoiceSetting["value"] = self._ud.rememberChoice
		self._tab.close()
		try:
			self._updatesMod.update()
		except SystemExit:
			QtGui.QMessageBox.information(None, _("Updating completed"), _("All updates were succesfully installed. In order for the changes to take effect, please restart the application."))
		self._dataStore["org.openteacher.updatesDialog.userDidUpdatesLastTime"] = True

	def _rejected(self):
		self._rememberChoiceSetting["value"] = self._ud.rememberChoice
		self._tab.close()
		self._dataStore["org.openteacher.updatesDialog.userDidUpdatesLastTime"] = False

	def disable(self):
		self.active = False

		self._thread.join()
		del self._thread

		#May not be set in one case
		with contextlib.ignored(AttributeError):
			del self._ud
			del self._tab
		#May not be set in another case
		with contextlib.ignored(AttributeError):
			del self._updatesMod
		#Always set
		del self._dataStore

def init(moduleManager):
	return UpdatesDialogModule(moduleManager)
