#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012-2013, Marten de Vries
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
import datetime
import contextlib

def installQtClasses():
	global ExerciseWidget, InstructionsWidget, LoginWidget, MasterWidget, ReadOnlyStringModel

	class ExerciseWidget(QtGui.QWidget):
		finished = QtCore.pyqtSignal([object, object])

		def __init__(self, createKeyboardWidget, *args, **kwargs):
			super(ExerciseWidget, self).__init__(*args, **kwargs)

			textFont = QtGui.QFont()
			textFont = QtGui.QFont("Ubuntu Monospace")
			textFont.setStyleHint(QtGui.QFont.TypeWriter)
			textFont.setPointSize(16)

			statusFont = QtGui.QFont()
			statusFont.setPointSize(16)

			self._textLabel = QtGui.QLabel()
			self._textLabel.setFont(textFont)
			self._statusLabel = QtGui.QLabel()
			self._statusLabel.setFont(statusFont)
			self._keyboardWidget = createKeyboardWidget()

			layout = QtGui.QVBoxLayout()
			layout.addWidget(self._textLabel)
			layout.addWidget(self._statusLabel)
			layout.addWidget(self._keyboardWidget)
			self.setLayout(layout)

			self.setFocusPolicy(QtCore.Qt.StrongFocus)
			self._active = False

		def start(self, keyboardLayout, text):
			self._keyboardWidget.setKeyboardLayout(keyboardLayout)
			self._text = text

			#startTime is set after the first keyboard strike
			self._startTime = None
			self._amountOfMistakes = 0
			self._pos = 0
			self._active = True
			self._update()

		def _update(self):
			done = self._text[:self._pos]
			try:
				future = self._text[self._pos + 1:]
				current = self._text[self._pos]
			except IndexError:
				future = self._text[self._pos:]
				current = ""

			self._textLabel.setText("<span style='color:gray'>%s</span><span style='color:black; text-decoration: underline'>%s</span><span style='color:gray'>%s</span>" % (done, current, future))
			self._keyboardWidget.setWrongKey(None)
			if not current:
				self._active = False
				time = (datetime.datetime.now() - self._startTime).total_seconds()
				self.finished.emit(time, self._amountOfMistakes)
			else:
				self._keyboardWidget.setCurrentKey(self._charToKeyName(current))
				self._statusLabel.setText("")

		def _charToKeyName(self, char):
			return char.replace(" ", "Space").replace("\t", "Tab").replace("\r", "Enter").replace(u"\x08", "Back-\nspace")

		def keyPressEvent(self, event):
			if not self._active:
				return
			if not self._startTime:
				self._startTime = datetime.datetime.now()
			keyInput = unicode(event.text())
			if self._text[self._pos:].startswith(keyInput):
				self._pos += len(keyInput)
				self._update()
			else:
				self._amountOfMistakes += 1
				self._keyboardWidget.setWrongKey(self._charToKeyName(keyInput[-1]))
				self._statusLabel.setText(_("That's a mistake :(."))

	class NewUserDialog(QtGui.QDialog):
		def __init__(self, model, KeyboardWidget, *args, **kwargs):
			super(NewUserDialog, self).__init__(*args, **kwargs)

			self._model = model

			self._explanationLabel = QtGui.QLabel()
			self._userNameLabel = QtGui.QLabel()
			self._userNameTextBox = QtGui.QLineEdit()
			self._layoutLabel = QtGui.QLabel()
			self._layoutComboBox = QtGui.QComboBox()
			self._previewLabel = QtGui.QLabel()
			self._keyboardWidget = KeyboardWidget()

			buttons = QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel
			buttonBox = QtGui.QDialogButtonBox(buttons)

			layout = QtGui.QFormLayout()
			layout.addRow(self._explanationLabel)
			layout.addRow(self._userNameLabel, self._userNameTextBox)
			layout.addRow(self._previewLabel, self._keyboardWidget)
			layout.addRow(self._layoutLabel, self._layoutComboBox)
			layout.addRow(buttonBox)

			self.setLayout(layout)

			self._layoutComboBox.highlighted.connect(self._updatePreview)
			self._layoutComboBox.currentIndexChanged.connect(self._updatePreview)
			buttonBox.accepted.connect(self.accepted.emit)
			buttonBox.rejected.connect(self.rejected.emit)

			self.retranslate()

		def clear(self):
			self._userNameTextBox.clear()
			if self._layoutComboBox.count():
				self._layoutComboBox.setCurrentIndex(0)
				self._updatePreview(0)

		def retranslate(self):
			self._explanationLabel.setText(_("Please choose a user name and the keyboard layout you want to learn."))
			self._userNameLabel.setText(_("Username:"))
			self._layoutLabel.setText(_("Keyboard layout:"))
			#TRANSLATORS: Split the line as closest to the middle as
			#TRANSLATORS: possible, not necessarily between 'Keyboard
			#TRANSLATORS: layout' and 'preview'. Thanks :)
			self._previewLabel.setText(_("Keyboard layout\npreview:"))

			#update on next event loop iteration, when the retranslate
			#of the model is handled.
			QtCore.QTimer.singleShot(0, self._updateComboBox)

		def _updatePreview(self, index):
			layoutName = unicode(self._layoutComboBox.itemData(index).toString())
			layout = getattr(self._model, layoutName)
			self._keyboardWidget.setKeyboardLayout(layout)

		def _updateComboBox(self):
			self._layoutComboBox.clear()
			for internalName, name in self._model.layouts:
				self._layoutComboBox.addItem(name, internalName)
			self._updatePreview(0)

		@property
		def username(self):
			return unicode(self._userNameTextBox.text())

		@property
		def layout(self):
			i = self._layoutComboBox.currentIndex()
			return unicode(self._layoutComboBox.itemData(i).toString())

	class ReadOnlyStringModel(QtGui.QStringListModel):
		def flags(self, *args, **kwargs):
			return QtCore.QAbstractItemModel.flags(self, *args, **kwargs)

	class LoginWidget(QtGui.QWidget):
		userChosen = QtCore.pyqtSignal([object])
		newUserRequested = QtCore.pyqtSignal()

		def __init__(self, model, *args, **kwargs):
			super(LoginWidget, self).__init__(*args, **kwargs)

			self._label = QtGui.QLabel()

			qtModel = ReadOnlyStringModel(model.usernames)
			listView = QtGui.QListView()
			listView.setModel(qtModel)
			listView.clicked.connect(self._userClicked)
			self._newUserButton = QtGui.QPushButton()
			self._newUserButton.clicked.connect(self.newUserRequested.emit)

			vbox = QtGui.QVBoxLayout()
			vbox.addWidget(self._label)
			vbox.addWidget(listView)
			vbox.addWidget(self._newUserButton)
			self.setLayout(vbox)

			self.retranslate()

		def retranslate(self):
			self._label.setText(_("Welcome, please choose your account by clicking on it."))
			self._newUserButton.setText(_("I am a new user"))

		def _userClicked(self, index):
			username = index.data(QtCore.Qt.DisplayRole).toString()
			self.userChosen.emit(unicode(username))

	class InstructionsWidget(QtGui.QWidget):
		exerciseStartRequested = QtCore.pyqtSignal()
		def __init__(self, model, *args, **kwargs):
			super(InstructionsWidget, self).__init__(*args, **kwargs)

			self._model = model

			self._levelLabel = QtGui.QLabel()
			self._levelLabelLabel = QtGui.QLabel()
			self._speedLabel = QtGui.QLabel()
			self._speedLabelLabel = QtGui.QLabel()
			self._mistakesLabel = QtGui.QLabel()
			self._mistakesLabelLabel = QtGui.QLabel()

			layout = QtGui.QFormLayout()
			layout.addRow(self._levelLabelLabel, self._levelLabel)
			layout.addRow(self._speedLabelLabel, self._speedLabel)
			layout.addRow(self._mistakesLabelLabel, self._mistakesLabel)

			self._instructionLabel = QtGui.QLabel()
			self._instructionLabel.setWordWrap(True)
			self._button = QtGui.QPushButton()
			self._button.clicked.connect(self.exerciseStartRequested.emit)

			vbox = QtGui.QVBoxLayout()
			vbox.addWidget(self._instructionLabel)
			vbox.addLayout(layout)
			vbox.addWidget(self._button)
			self.setLayout(vbox)

			self.retranslate()

		def updateInstruction(self):
			instr = self._model.currentInstruction(self.username)
			try:
				self._levelLabel.setText(u"%s/%s" % (
					self._model.level(self.username),
					self._model.maxLevel(self.username),
				))
			except IndexError:
				self._levelLabel.hide()
			else:
				self._levelLabel.show()

			try:
				self._speedLabel.setText(u"%s/%s" % (
					self._model.speed(self.username),
					self._model.targetSpeed(self.username),
				))
			except IndexError:
				self._speedLabelLabel.hide()
			else:
				self._speedLabelLabel.show()

			try:
				self._mistakesLabel.setText(unicode(self._model.amountOfMistakes(self.username)))
			except IndexError:
				self._mistakesLabelLabel.hide()
			else:
				self._mistakesLabelLabel.show()
			self._instructionLabel.setText(instr)

		def retranslate(self):
			self._levelLabelLabel.setText(_("Level"))
			self._speedLabelLabel.setText(_("Speed (words per minute)"))
			self._mistakesLabelLabel.setText(_("Amount of mistakes"))
			self._button.setText(_("Start exercise"))
			with contextlib.ignored(AttributeError):
				#requires self.username, which might not be set yet.
				self.updateInstruction()

	class MasterWidget(QtGui.QStackedWidget):
		def __init__(self, model, createKeyboardWidget, *args, **kwargs):
			super(MasterWidget, self).__init__(*args, **kwargs)

			self._model = model

			#setup other widgets, connect signals
			self._loginWidget = LoginWidget(self._model)
			self._newUserDialog = NewUserDialog(self._model, createKeyboardWidget)
			self._instructionsWidget = InstructionsWidget(self._model)
			self._exerciseWidget = ExerciseWidget(createKeyboardWidget)

			self._loginWidget.userChosen.connect(self._userKnown)
			self._loginWidget.newUserRequested.connect(self._showNewUser)
			self._newUserDialog.accepted.connect(self._newUser)
			self._newUserDialog.rejected.connect(self._showLoginWidget)
			self._instructionsWidget.exerciseStartRequested.connect(self._startExercise)
			self._exerciseWidget.finished.connect(self._exerciseDone)

			#add widgets and set current widget
			self.addWidget(self._loginWidget)
			self.addWidget(self._newUserDialog)
			self.addWidget(self._instructionsWidget)
			self.addWidget(self._exerciseWidget)

			if self._model.usernames:
				self._showLoginWidget()
			else:
				self._showNewUser()

		def _showLoginWidget(self):
			self.setCurrentWidget(self._loginWidget)

		def _showNewUser(self, clear=True):
			if clear:
				self._newUserDialog.clear()
			self.setCurrentWidget(self._newUserDialog)

		def _newUser(self):
			username = self._newUserDialog.username
			layout = self._newUserDialog.layout
			try:
				self._model.registerUser(username, layout)
			except self._model.UsernameEmptyError:
				QtGui.QMessageBox.critical(
					self,
					_("Username empty"),
					_("The username should not be empty. Please try again.")
				)
				self._showNewUser(clear=False)
			except self._model.UsernameTakenError:
				QtGui.QMessageBox.critical(
					self,
					_("Username taken"),
					_("That username is already taken. Please try again."),
				)
				self._showNewUser(clear=False)
			else:
				self._userKnown(username)

		def _userKnown(self, username):
			self._username = username
			self._instructionsWidget.username = username
			self._showInstruction()

		def _exerciseDone(self, time, amountOfMistakes):
			self._model.setResult(self._username, time, amountOfMistakes)
			self._showInstruction()

		def _showInstruction(self):
			self._instructionsWidget.updateInstruction()
			self.setCurrentWidget(self._instructionsWidget)

		def _startExercise(self):
			layout = self._model.layout(self._username)
			exercise = self._model.currentExercise(self._username)

			self._exerciseWidget.start(layout, exercise)
			self.setCurrentWidget(self._exerciseWidget)

		def retranslate(self):
			self._loginWidget.retranslate()
			self._instructionsWidget.retranslate()

class TypingTutorModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TypingTutorModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "typingTutor"
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="buttonRegister"),
			self._mm.mods(type="typingTutorModel"),
			self._mm.mods(type="typingTutorKeyboard"),
		)
		x = 700
		self.priorities = {
			"default": -1,
			"code-documentation": x,
			"all": x,
			"selfstudy": x,
			"student@home": x,
			"student@school": x,
			"teacher": x,
			"test-suite": x,
		}
		self.filesWithTranslations = ("main.py",)

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = next(iter(self._mm.mods(type="modules")))

		self._uiModule = self._modules.default("active", type="ui")

		self._buttonRegister = self._modules.default("active", type="buttonRegister")

		self._button = self._buttonRegister.registerButton("create")
		self._button.clicked.handle(self._show)
		self._button.changeIcon.send(self._mm.resourcePath("typingTutor.png"))
		self._button.changePriority.send(self.priorities["all"])

		self._widgetRefs = set()
		self._tabRefs = set()

		#translations
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

		self._button.changeText.send(_("Typing Tutor"))

		for ref in self._widgetRefs:
			wid = ref()
			if wid:
				wid.retranslate()

		for ref in self._tabRefs:
			tab = ref()
			if tab:
				tab.title = _("Typing Tutor")

	_model = property(lambda self: self._modules.default("active", type="typingTutorModel").model)
	_createKeyboardWidget = property(lambda self: self._modules.default("active", type="typingTutorKeyboard").createKeyboardWidget)

	def _show(self):
		widget = MasterWidget(self._model, self._createKeyboardWidget)
		tab = self._uiModule.addCustomTab(widget)
		tab.closeRequested.handle(tab.close)

		self._tabRefs.add(weakref.ref(tab))
		self._widgetRefs.add(weakref.ref(widget))

		self._retranslate()

	def disable(self):
		self.active = False

		del self._modules
		del self._buttonRegister
		del self._button
		del self._uiModule
		del self._widgetRefs
		del self._tabRefs

def init(moduleManager):
	return TypingTutorModule(moduleManager)
