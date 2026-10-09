#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#	Copyright 2011-2013, Marten de Vries
#	Copyright 2011, Milan Boers
#	Copyright 2012, Cas Widdershoven
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
import contextlib

def installQtClasses():
	global ThinkWidget, AnswerWidget, InMindTeachWidget

	class ThinkWidget(QtGui.QWidget):
		def __init__(self, *args, **kwargs):
			super(ThinkWidget, self).__init__(*args, **kwargs)
			
			self.label = QtGui.QLabel()
			self.label.setWordWrap(True)
			self.viewAnswerButton = QtGui.QPushButton()
			self.skipButton = QtGui.QPushButton()
			
			mainLayout = QtGui.QVBoxLayout()
			mainLayout.addWidget(self.label)
			mainLayout.addWidget(self.viewAnswerButton)
			mainLayout.addWidget(self.skipButton)
			
			self.setLayout(mainLayout)

		def retranslate(self):
			self.label.setText(_("Think about the answer, and press the 'View answer' button when you're done."))
			self.viewAnswerButton.setText(_("View answer"))
			self.skipButton.setText(_("Skip"))

	class AnswerWidget(QtGui.QWidget):
		def __init__(self, *args, **kwargs):
			super(AnswerWidget, self).__init__(*args, **kwargs)

			self.label = QtGui.QLabel()
			self.rightButton = QtGui.QPushButton()
			self.wrongButton = QtGui.QPushButton()

			bottomLayout = QtGui.QHBoxLayout()
			bottomLayout.addWidget(self.rightButton)
			bottomLayout.addWidget(self.wrongButton)

			mainLayout = QtGui.QVBoxLayout()
			mainLayout.addWidget(self.label)
			mainLayout.addLayout(bottomLayout)
			
			self.setLayout(mainLayout)

		def retranslate(self):
			self.rightButton.setText(_("I was right"))
			self.wrongButton.setText(_("I was wrong"))

	class InMindTeachWidget(QtGui.QStackedWidget):
		def __init__(self, compose, *args, **kwargs):
			super(InMindTeachWidget, self).__init__(*args, **kwargs)

			self._compose = compose

			self.thinkWidget = ThinkWidget()
			self.answerWidget = AnswerWidget()

			self.addWidget(self.thinkWidget)
			self.addWidget(self.answerWidget)

			#connect some events
			self.thinkWidget.viewAnswerButton.clicked.connect(self.startAnswering)
			self.answerWidget.rightButton.clicked.connect(self.setRight)
			self.answerWidget.wrongButton.clicked.connect(self.setWrong)

		def retranslate(self):
			self.thinkWidget.retranslate()
			self.answerWidget.retranslate()
			
			curWid = self.currentWidget()
			with contextlib.ignored(AttributeError):
				self.newItem(self._currentWord)
			self.setCurrentWidget(curWid)

		def updateLessonType(self, lessonType):
			self.lessonType = lessonType

			#connect lesson type specific events
			self.lessonType.newItem.handle(self.newItem)
			self.lessonType.lessonDone.handle(self.lessonDone)
			self.thinkWidget.skipButton.clicked.connect(self.lessonType.skip)

		def lessonDone(self):
			#forget the old lessonType to be fresh for a new lesson
			self.lessonType.newItem.unhandle(self.newItem)
			self.lessonType.lessonDone.unhandle(self.lessonDone)
			self.thinkWidget.skipButton.clicked.disconnect(self.lessonType.skip)

		def _constructResult(self):
			return {
				"itemId": self._currentWord["id"],
				"active": {
					"start": self.start,
					"end": self.end,
				},
			}

		def setRight(self):
			result = self._constructResult()
			result["result"] = "right"
			self.lessonType.setResult(result)

		def setWrong(self):
			result = self._constructResult()
			result["result"] = "wrong"
			self.lessonType.setResult(result)

		def newItem(self, word):
			self._currentWord = word
			self.answerWidget.label.setText(
				_("Translation: ") + self._compose(word["answers"])
			)
			self.start = datetime.datetime.now()
			self.setCurrentWidget(self.thinkWidget)

		def startAnswering(self):
			self.end = datetime.datetime.now()
			self.setCurrentWidget(self.answerWidget)

class InMindTeachTypeModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(InMindTeachTypeModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "teachType"

		self.priorities = {
			"default": 514,
		}
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="wordsStringComposer"),
		)
		self.filesWithTranslations = ("inMind.py",)

	def enable(self):
		global QtGui
		try:
			from PyQt4 import QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()

		self._activeWidgets = set()

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.dataType = "words"
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
		self.name = _("Think answer")
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

	@property
	def _compose(self):
		return self._modules.default(
			"active",
			type="wordsStringComposer"
		).compose

	def createWidget(self, tabChanged, letterChosen, addSideWidget, removeSideWidget):
		imtw = InMindTeachWidget(self._compose)
		self._activeWidgets.add(weakref.ref(imtw))
		self._retranslate()
		return imtw

def init(moduleManager):
	return InMindTeachTypeModule(moduleManager)
