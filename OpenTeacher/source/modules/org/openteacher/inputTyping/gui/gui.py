#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Cas Widdershoven
#	Copyright 2011-2013, Marten de Vries
#	Copyright 2008-2011, Milan Boers
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

import datetime
import weakref
import difflib

def installQtClasses():
	global InputTypingWidget

	class InputTypingWidget(QtGui.QWidget):
		def __init__(self, createController, getFadeTime, letterChosen, *args, **kwargs):
			super(InputTypingWidget, self).__init__(*args, **kwargs)

			self._controller = createController()
			self._getFadeTime = getFadeTime

			self._buildUi()
			self._connectToEvents(letterChosen)

		def _connectToEvents(self, letterChosen):
			#bind to controller events
			self._controller.clearInput.handle(self.inputLineEdit.clear)
			self._controller.enableInput.handle(lambda: self.inputLineEdit.setEnabled(True))
			self._controller.disableInput.handle(lambda: self.inputLineEdit.setEnabled(False))
			self._controller.focusInput.handle(self._onFocusInput)

			self._controller.showCorrection.handle(self._showCorrection)
			self._controller.hideCorrection.handle(self._hideCorrection)

			self._controller.enableCheck.handle(lambda: self.checkButton.setEnabled(True))
			self._controller.disableCheck.handle(lambda: self.checkButton.setEnabled(False))
			self._controller.enableSkip.handle(lambda: self.skipButton.setEnabled(True))
			self._controller.disableSkip.handle(lambda: self.skipButton.setEnabled(False))
			self._controller.enableCorrectAnyway.handle(lambda: self.correctButton.setEnabled(True))
			self._controller.disableCorrectAnyway.handle(lambda: self.correctButton.setEnabled(False))

			#make sure user actions are sent to the controller
			checkAnswer = lambda: self._controller.checkTriggered(self._userAnswer)
			self.checkButton.clicked.connect(checkAnswer)
			self.inputLineEdit.returnPressed.connect(checkAnswer)
			self.correctButton.clicked.connect(self._controller.correctAnywayTriggered)
			self.skipButton.clicked.connect(self._controller.skipTriggered)
			self.inputLineEdit.textEdited.connect(self._controller.userIsTyping)

			#make character input work
			letterChosen.handle(self.addLetter)

		def _buildUi(self):
			self.correctLabel = QtGui.QLabel(self)

			self.inputLineEdit = QtGui.QLineEdit(self)
			self.inputLineEdit.textEdited.connect(self._textEdited)

			self.skipButton = QtGui.QPushButton(self)
			self.checkButton = QtGui.QPushButton(self)
			self.checkButton.setShortcut(QtCore.Qt.Key_Return)
			self.correctButton = QtGui.QPushButton(self)

			mainLayout = QtGui.QGridLayout()
			mainLayout.addWidget(self.correctLabel, 0, 0, 1, 3)
			mainLayout.addWidget(self.inputLineEdit, 1, 0, 1, 2)
			mainLayout.addWidget(self.checkButton, 1, 2)
			mainLayout.addWidget(self.correctButton, 2, 1)
			mainLayout.addWidget(self.skipButton, 2, 2)
			self.setLayout(mainLayout)

		def _onFocusInput(self):
			def doWork():
				if self.inputLineEdit.isVisible():
					self.inputLineEdit.setFocus()

			#next event loop iteration, since isVisible() might not be
			#updated.
			QtCore.QTimer.singleShot(0, doWork)

		def _showCorrection(self, correction):
			self._startFading()
			self._showDiff(correction)

		def _startFading(self):
			self._timeLine = QtCore.QTimeLine(self._getFadeTime(), self)
			self._timeLine.setFrameRange(0, 255) #256 color steps
			self._timeLine.frameChanged.connect(self._fade)
			self._timeLine.finished.connect(self._controller.correctionShowingDone)
			self._timeLine.start()

		def _showDiff(self, correction):
			#show diff
			diff = self._buildDiff(correction, self._userAnswer)
			if diff:
				text = _("Correct answer: <b>{answers}</b> [{diff}]").format(answers=correction, diff=diff)
			else:
				text = _("Correct answer: <b>{answers}</b>").format(answers=correction)
			self.correctLabel.setText(text)

		@property
		def _userAnswer(self):
			return unicode(self.inputLineEdit.text())

		def _hideCorrection(self):
			self._timeLine.stop()
			self.inputLineEdit.setStyleSheet("")
			self.correctLabel.clear()

		def retranslate(self):
			self.checkButton.setText(_("Check!"))
			self.correctButton.setText(_("Correct anyway"))
			self.skipButton.setText(_("Skip"))

		def addLetter(self, letter):
			# Only the currently visible edit
			if self.inputLineEdit.isVisible():
				self.inputLineEdit.insert(letter)
				self.inputLineEdit.setFocus()

		def _textEdited(self, text):
			try:
				self._end
			except AttributeError:
				self._end = datetime.datetime.now()
			else:
				if not unicode(text).strip():
					del self._end

		def updateLessonType(self, lessonType):
			self._controller.lessonType = lessonType

		def _buildDiff(self, answers, givenAnswer):
			#Check if the input looks like the answer or the second answer.
			try:
				similar = difflib.get_close_matches(givenAnswer, [answers])[0]
			except IndexError:
				#It doesn't, set similar to None
				similar = None

			#If they look like each other.
			if similar:
				#Show the differences graphical
				output = ""
				for item in difflib.ndiff(givenAnswer, similar):
					if item.startswith('+ '):
						output += '<span style="color: #1da90b;"><u>%s</u></span>' % item[2:]
					elif item.startswith('- '):
						output += '<span style="color: #da0f0f;"><s>%s</s></span>' % item[2:]
					else:
						output += item[2:]
				return output

		def _fade(self, step):
			stylesheet = "QLineEdit {color: rgb(%s, %s, %s, %s)}" % (255, 00, 00, 255-step)
			self.inputLineEdit.setStyleSheet(stylesheet)

class InputTypingModule(object):
	_createController = property(lambda self: self._modules.default("active", type="inputTypingLogic").createController)

	def __init__(self, moduleManager, *args, **kwargs):
		super(InputTypingModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "typingInput"
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="settings"),
		)
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="inputTypingLogic"),
		)
		self.filesWithTranslations = ("gui.py",)

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._activeWidgets = set()

		#Register the fade duration setting
		DEFAULT_VALUE = 4000
		try:
			self._fadeDurationSetting = self._modules.default(type="settings").registerSetting(**{
				"internal_name": "org.openteacher.inputTyping.fadeDuration",
				"type": "number",
				"defaultValue": DEFAULT_VALUE,
			})
		except IndexError:
			self._fadeDurationSetting = {
				"value": DEFAULT_VALUE,
			}

		#Translations
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
		#Install translator inside the whole of these file
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

		#update all active widgets
		for ref in self._activeWidgets:
			wid = ref()
			if wid is not None:
				wid.retranslate()

		#update the setting
		self._fadeDurationSetting.update({
			"name": _("Fade duration when wrong (milliseconds)"),
			"category": _("Lesson"),
			"subcategory": _("Words lesson"),
		})

	def disable(self):
		self.active = False

		del self._modules
		del self._activeWidgets
		del self._fadeDurationSetting

	def createWidget(self, letterChosen):
		getFadeDuration = lambda: self._fadeDurationSetting["value"]
		it = InputTypingWidget(self._createController, getFadeDuration, letterChosen)
		self._activeWidgets.add(weakref.ref(it))
		it.retranslate()
		return it

def init(moduleManager):
	return InputTypingModule(moduleManager)
