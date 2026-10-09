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

import weakref
import copy
import platform

def installQtClasses():
	global CategoryTab, SettingsDialog

	class CategoryTab(QtGui.QWidget):
		"""A category tab. It consists out of subcategory group boxes,
		   which contain the actual settings.

		"""
		def __init__(self, byKey, widgets, name, inCategory, *args, **kwargs):
			super(CategoryTab, self).__init__(*args, **kwargs)

			self.byKey = byKey
			self._widgets = widgets

			self.setWindowTitle(name)
			vbox = QtGui.QVBoxLayout()

			categories = self.byKey("subcategory", inCategory)
			for name in sorted(categories.keys()):			
				w = self.createSubcategoryGroupBox(name, categories[name])
				vbox.addWidget(w)

			vbox.addStretch()
			self.setLayout(vbox)

		def createSubcategoryGroupBox(self, name, inSubcategory):
			groupBox = QtGui.QGroupBox(name)
			groupBoxLayout = QtGui.QFormLayout()
			for setting in sorted(inSubcategory, key=lambda s: s["name"]):
				try:
					createWidget = self._widgets[setting["type"]]
				except KeyError:
					continue
				try:
					groupBoxLayout.addRow(
						setting["name"],
						createWidget(setting)
					)
				except KeyError:
					continue
			groupBox.setLayout(groupBoxLayout)
			return groupBox

		def retranslate(self):
			pass

	class SettingsDialog(QtGui.QTabWidget):
		"""The actual settings dialog. It consists of category tabs."""

		def __init__(self, byKey, settings, widgets, *args, **kwargs):
			super(SettingsDialog, self).__init__(*args, **kwargs)

			self.settings = settings
			self.byKey = byKey
			self.widgets = widgets

			#Setup widget
			self.setTabPosition(QtGui.QTabWidget.South)
			if platform.system() != "Darwin":
				#Document mode, south tabs & a corner button gives
				#misdrawings in Mac OS X.
				self.setDocumentMode(True)

			self.advancedButton = QtGui.QPushButton()
			self.advancedButton.clicked.connect(self.advanced)

			self.simpleButton = QtGui.QPushButton()
			self.simpleButton.clicked.connect(self.simple)

			# Go to simple mode
			self.simple()

			#Used to track if the widget needs to be updated because of
			#retranslation. We can't do that directly, because then the
			#language box in which the language is selected is also updated
			#immediately, rendering it unusable. Instead, we do it when the
			#widget is hidden (see the eventFilter method.)
			self._updateNeeded = False

			#so the focus can be tracked
			self.installEventFilter(self)

		def retranslate(self):
			self.setWindowTitle(_("Settings"))
			self.simpleButton.setText(_("Simple mode"))
			self.advancedButton.setText(_("Advanced mode"))
			self._updateNeeded = True

		def createCategoryTab(self, *args, **kwargs):
			tab = CategoryTab(self.byKey, *args, **kwargs)
			self.addTab(tab, tab.windowTitle())

		def eventFilter(self, object, event, *args, **kwargs):
			if event.type() == QtCore.QEvent.Hide and self._updateNeeded:
				tabIndex = self.currentIndex()
				self.update()
				self._updateNeeded = False
				#Reset the index
				self.setCurrentIndex(tabIndex)
				return True
			else:
				return False

		def update(self):
			# Copy settings
			settings = copy.copy(self.settings)
			if self.simpleMode:
				for setting in self.settings:
					if "advanced" in setting and setting["advanced"]:
						settings.remove(setting)

			self.clear()
			categories = self.byKey("category", settings)
			for name in sorted(categories.keys()):
				self.createCategoryTab(self.widgets, name, categories[name])

		def advanced(self):
			self.setCornerWidget(
				self.simpleButton,
				QtCore.Qt.BottomRightCorner
			)

			self.simpleMode = False

			self.update()

			self.simpleButton.show()

		def simple(self):
			self.setCornerWidget(
				self.advancedButton,
				QtCore.Qt.BottomRightCorner
			)

			self.simpleMode = True

			self.update()

			self.advancedButton.show()

class SettingsDialogModule(object):
	"""The settings dialog, which shows all registered settings in the
	   UI.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(SettingsDialogModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "settingsDialog"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="settings"),
			self._mm.mods(type="settingsWidgets"),
			self._mm.mods(type="settingsFilterer"),
		)
		self.filesWithTranslations = ("settings.py",)

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			#remain inactive
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._uiModule = self._modules.default("active", type="ui")
		self._settings = self._modules.default(type="settings")
		self._settingsWidgets = self._modules.default("active", type="settingsWidgets")
		self._settingsFilterer = self._modules.default("active", type="settingsFilterer")

		self._activeDialogs = set()

		#install translator
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
			#so text of settings is also updated.
			translator.languageChangeDone.handle(self._retranslate)
		self._retranslate()

		self.active = True

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
		for ref in self._activeDialogs:
			dialog = ref()
			if dialog is not None:
				dialog.retranslate()
				dialog.tab.title = dialog.windowTitle()

	def disable(self):
		self.active = False

		del self._modules
		del self._uiModule
		del self._settings
		del self._settingsWidgets
		del self._settingsFilterer
		del self._activeDialogs

	def show(self):
		"""Shows the settings dialog. Normally there's no need to call
		   this manually, but it's possible.

		"""
		dialog = SettingsDialog(
			self._settingsFilterer.byKey,
			self._settings.registeredSettings,
			self._settingsWidgets.widgets
		)
		self._activeDialogs.add(weakref.ref(dialog))

		self.tab = self._uiModule.addCustomTab(dialog)
		dialog.tab = self.tab
		self.tab.closeRequested.handle(self.tab.close)

		self._retranslate()

def init(moduleManager):
	return SettingsDialogModule(moduleManager)
