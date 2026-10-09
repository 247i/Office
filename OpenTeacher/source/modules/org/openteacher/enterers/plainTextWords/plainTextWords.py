#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
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

import contextlib

def installQtClasses():
	global EnterPlainTextDialog

	class EnterPlainTextDialog(QtGui.QDialog):
		def __init__(self, parseList, charsKeyboard, *args, **kwargs):
			super(EnterPlainTextDialog, self).__init__(*args, **kwargs)

			self._parseList = parseList

			buttonBox = QtGui.QDialogButtonBox(
				QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok,
				parent=self
			)
			buttonBox.accepted.connect(self.accept)
			buttonBox.rejected.connect(self.reject)

			self._label = QtGui.QLabel()
			self._label.setWordWrap(True)
			#make sure the label doesn't claim too much space when e.g.
			#being full screen.
			self._label.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
			self._textEdit = QtGui.QTextEdit()

			splitter = QtGui.QSplitter()
			splitter.addWidget(self._textEdit)
			splitter.setStretchFactor(0, 3)
			if charsKeyboard:
				splitter.addWidget(charsKeyboard)
				splitter.setStretchFactor(1, 1)
				charsKeyboard.letterChosen.handle(self._addLetter)

			layout = QtGui.QVBoxLayout()
			layout.addWidget(self._label)
			layout.addWidget(splitter)
			layout.addWidget(buttonBox)
			self.setLayout(layout)

		def _addLetter(self, letter):
			self._textEdit.insertPlainText(letter)
			self._textEdit.setFocus(True)

		def retranslate(self):
			self._label.setText(_("Please enter the plain text in the text edit. Separate words with a new line and questions from answers with an equals sign ('=') or a tab."))
			self.setWindowTitle(_("Plain text words enterer"))

		def focus(self):
			self._textEdit.setFocus(True)

		@property
		def lesson(self):
			text = unicode(self._textEdit.toPlainText())
			try:
				return self._parseList(text)
			except ValueError:
				QtGui.QMessageBox.warning(
					self,
					_("Missing equals sign or tab"),
					_("Please make sure every line contains an '='-sign or tab between the questions and answers.")
				)

class PlainTextWordsEntererModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(PlainTextWordsEntererModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "plainTextWordsEnterer"
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="buttonRegister"),
			self._mm.mods(type="wordListStringParser"),
			self._mm.mods(type="loaderGui"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="charsKeyboard"),
		)
		x = 960
		self.priorities = {
			"all": x,
			"selfstudy": x,
			"student@home": x,
			"student@school": x,
			"teacher": x,
			"words-only": x,
			"code-documentation": x,
			"test-suite": x,
			"default": -1,
		}
		self.filesWithTranslations = ("plainTextWords.py",)

	@property
	def _charsKeyboard(self):
		try:
			return self._modules.default(
				"active",
				type="charsKeyboard"
			).createWidget()
		except IndexError:
			return

	def enable(self):
		global QtGui
		try:
			from PyQt4 import QtGui
		except ImportError:
			#stay disabled
			return
		installQtClasses()

		self._references = set()
		self._activeDialogs = set()

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._uiModule = self._modules.default("active", type="ui")

		self._button = self._modules.default("active", type="buttonRegister").registerButton("create")
		self._button.clicked.handle(self.createLesson)
		self._button.changePriority.send(self.priorities["all"])
		self._button.changeSize.send("small")

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
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

		self._button.changeText.send(_("Create words lesson by entering plain text"))
		for dialog in self._activeDialogs:
			dialog.retranslate()
			dialog.tab.title = dialog.windowTitle()

	def createLesson(self):
		parseList = self._modules.default(
			"active",
			type="wordListStringParser"
		).parseList

		eptd = EnterPlainTextDialog(parseList, self._charsKeyboard)
		self._activeDialogs.add(eptd)

		tab = self._uiModule.addCustomTab(eptd)
		tab.closeRequested.handle(tab.close)
		eptd.tab = tab

		self._retranslate()

		eptd.focus()
		eptd.accepted.connect(lambda: self._loadLesson(eptd.lesson))
		eptd.finished.connect(tab.close)
		eptd.finished.connect(lambda: self._activeDialogs.remove(eptd))

	def _loadLesson(self, lesson):
		if not lesson:
			return
		lesson["changed"] = True
		with contextlib.ignored(NotImplementedError):
			self._modules.default("active", type="loaderGui").loadFromLesson("words", lesson)

	def disable(self):
		self.active = False

		self._modules.default("active", type="buttonRegister").unregisterButton(self._button)

		del self._references
		del self._activeDialogs
		del self._modules
		del self._uiModule
		del self._button

def init(moduleManager):
	return PlainTextWordsEntererModule(moduleManager)
