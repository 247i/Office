#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Cas Widdershoven
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

def installQtClasses():
	global RepeatAnswerTeachWidget

	class RepeatScreenWidget(QtGui.QWidget):
		def __init__(self, repeatAnswerTeachWidget, compose, getFadeDuration, *args, **kwargs):
			super(RepeatScreenWidget, self).__init__(*args, **kwargs)

			self._repeatAnswerTeachWidget = repeatAnswerTeachWidget
			self._compose = compose
			self._getFadeDuration = getFadeDuration

			self.showAnswerScreen = QtGui.QVBoxLayout()
			self.answerLabel = QtGui.QLabel()
			self.showAnswerScreen.addWidget(self.answerLabel)
			self.setLayout(self.showAnswerScreen)

		def fade(self, callback):
			self.answerLabel.setText(self._compose(self.word["answers"]))
			timer = QtCore.QTimeLine(self._getFadeDuration(), self)
			timer.setFrameRange(0, 255)
			timer.frameChanged.connect(self.fadeAction)
			timer.finished.connect(callback)
			timer.start()

		def fadeAction(self, frame):
			palette = QtGui.QPalette()
			color = palette.windowText().color()
			color.setAlpha(255 - frame)
			palette.setColor(QtGui.QPalette.WindowText, color)

			self.answerLabel.setPalette(palette)

	class StartScreenWidget(QtGui.QWidget):
		def __init__(self, *args, **kwargs):
			super(StartScreenWidget, self).__init__(*args, **kwargs)

			self.label = QtGui.QLabel()
			self.startButton = QtGui.QPushButton()

			self.startScreen = QtGui.QVBoxLayout()
			self.startScreen.addWidget(self.label)
			self.startScreen.addWidget(self.startButton)
			self.setLayout(self.startScreen)
			
			self.retranslate()

		def retranslate(self):
			self.label.setText(_("Click the button to start"))
			self.startButton.setText(_("Start!"))

	class RepeatAnswerTeachWidget(QtGui.QStackedWidget):
		def __init__(self, inputWidget, compose, getFadeDuration, tabChanged, *args, **kwargs):
			super(RepeatAnswerTeachWidget, self).__init__(*args, **kwargs)

			#make start screen
			self.startScreen = StartScreenWidget(self)
			self.startScreen.startButton.clicked.connect(self.startRepeat)
			self.addWidget(self.startScreen)

			#make "show answer" screen
			self.repeatScreen = RepeatScreenWidget(self, compose, getFadeDuration)
			self.addWidget(self.repeatScreen)

			#make input screen
			self.inputWidget = inputWidget
			self.addWidget(self.inputWidget)

			tabChanged.connect(lambda: self.setCurrentWidget(self.startScreen))

		def retranslate(self):
			self.startScreen.retranslate()

		def _onRepeatFinished(self):
			self.setCurrentWidget(self.inputWidget)

		def startRepeat(self):
			self.setCurrentWidget(self.repeatScreen)
			self.repeatScreen.fade(self._onRepeatFinished)

		def updateLessonType(self, lessonType, *args, **kwargs):
			self.inputWidget.updateLessonType(lessonType, *args, **kwargs)
			lessonType.newItem.handle(self.newWord)

		def newWord(self, word):
			self.repeatScreen.word = word
			if self.isVisible():
				self.startRepeat()

class RepeatAnswerTeachTypeModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(RepeatAnswerTeachTypeModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "teachType"
		self.priorities = {
			"default": 651,
		}
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="typingInput"),
			self._mm.mods(type="wordsStringComposer"),
		)
		self.uses = (
			self._mm.mods(type="settings"),
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("repeatAnswer.py",)

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()

		self._activeWidgets = set()

		DEFAULT_VALUE = 3000
		#Register fade duration setting
		try:
			self._fadeDurationSetting = self._modules.default(type="settings").registerSetting(**{
				"internal_name": "org.openteacher.teachTypes.repeatAnswer.fadeDuration",
				"type": "number",
				"defaultValue": DEFAULT_VALUE,
			})
		except IndexError:
			self._fadeDuration = {
				"value": DEFAULT_VALUE,
			}

		#Register for retranslating
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		#translate everything for the first time
		self._retranslate()

		self.dataType = "words"
		self.active = True

	def _retranslate(self):
		#Install translator for this file
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

		#Translate name for 'the outside world'
		self.name = _("Repeat answer")

		#Translate the setting
		self._fadeDurationSetting.update({
			"name": _("Repeat mode fade duration (milliseconds)"),
			"category": _("Lesson"),
			"subcategory": _("Words lesson"),
		})

		#Translate all instances of widgets
		for widget in self._activeWidgets:
			r = widget()
			if r is not None:
				r.retranslate()

	def disable(self):
		self.active = False

		del self._modules
		del self._activeWidgets
		del self.dataType
		del self.name
		del self._fadeDurationSetting

	def createWidget(self, tabChanged, letterChosen, addSideWidget, removeSideWidget):
		typingInput = self._modules.default("active", type="typingInput")
		inputWidget = typingInput.createWidget(letterChosen)

		ratw = RepeatAnswerTeachWidget(
			inputWidget,
			self._modules.default("active", type="wordsStringComposer").compose,
			self._getFadeDuration,
			tabChanged,
		)
		self._activeWidgets.add(weakref.ref(ratw))
		return ratw

	def _getFadeDuration(self):
		return self._fadeDurationSetting["value"]

def init(moduleManager):
	return RepeatAnswerTeachTypeModule(moduleManager)
