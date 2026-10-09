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

import random
import weakref
import contextlib

def installQtClasses():
	global ShuffleAnswerTeachWidget

	class ShuffleAnswerTeachWidget(QtGui.QWidget):
		def __init__(self, inputWidget, compose, *args, **kwargs):
			super(ShuffleAnswerTeachWidget, self).__init__(*args, **kwargs)
			
			self.inputWidget = inputWidget
			self.compose = compose
			
			vbox = QtGui.QVBoxLayout()
			self.hintLabel = QtGui.QLabel()
			vbox.addWidget(self.hintLabel)
			vbox.addWidget(self.inputWidget)
			self.setLayout(vbox)

		def retranslate(self):
			with contextlib.ignored(AttributeError):
				self.setHint()

		#	Two solutions for the OpenTeacher 2.2 bug at 24-10-11:
		#	(the commented version isn't ported to 3.x)
		#
		#	def setHint(self, answer):
		#		hint = QtCore.QCoreApplication.translate("OpenTeacher", "Hint:") + u" "
		#		if len(answer) > 1 and not answer.strip(answer[0]): #If len(answer) == 1, it is always the same shuffled#			for i in range(255): #Avoid "while True"
		#				hintList = list(answer) #Make random.shuffle() possible
		#				random.shuffle(hintList) #The actual shuffling of the word
		#				if hintList != list(answer): #Check if the hint isn't the same as the answer
		#					hint += u"".join(hintList) #Put the shuffled word in a string
		#					self.ui.hintLabelShuffle.setText(hint) #Set the hint
		#				else:
		#					continue #It's the same; try again
		#		else:
		#			hint += u"." * len(answer) #It's only one character (0 should already be caught), so the hint string is only a dot
		#			self.ui.hintLabelShuffle.setText(hint) #Set the hint

		def setHint(self):
			hint = _("Hint:") + u" "

			#Shuffle list making sure that no letter gets at the same
			#position if possible.
			if "answers" in self.word:
				oldAnswer = list(self.compose(self.word["answers"]))
			else:
				oldAnswer = u""
			answer = oldAnswer[:]
			for i in range(len(answer) -1):
				j = i + 1 + int(random.random() * (len(answer) -i -1))

				answer[i], answer[j] = answer[j], answer[i]

			#Check if the word has a minimum length and could be shuffled.
			#If not, the hint is a few dots, as much as there are letters
			#in the answer
			if len(answer) <= 2 or oldAnswer == answer:
				hint += u"." * len(answer)
			else:
				hint += u"".join(answer)

			self.hintLabel.setText(hint)

		def updateLessonType(self, lessonType, *args, **kwargs):
			self.inputWidget.updateLessonType(lessonType, *args, **kwargs)

			lessonType.newItem.handle(self.newWord)

		def newWord(self, word):
			self.word = word
			self.setHint()

	return ShuffleAnswerTeachWidget

class ShuffleAnswerTeachTypeModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(ShuffleAnswerTeachTypeModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "teachType"
		self.priorities = {
			"default": 558,
		}
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="typingInput"),
			self._mm.mods(type="wordsStringComposer"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("shuffleAnswer.py",)

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

	def disable(self):
		self.active = False

		del self._modules
		del self._activeWidgets
		del self.dataType
		del self.name

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
		self.name = _("Shuffle answer")
		for widget in self._activeWidgets:
			r = widget()
			if r is not None:
				r.retranslate()

	def createWidget(self, tabChanged, letterChosen, addSideWidget, removeSideWidget):
		typingInput = self._modules.default("active", type="typingInput")

		inputWidget = typingInput.createWidget(letterChosen)
		compose = self._modules.default("active", type="wordsStringComposer").compose

		satw = ShuffleAnswerTeachWidget(inputWidget, compose)
		self._activeWidgets.add(weakref.ref(satw))
		return satw

def init(moduleManager):
	return ShuffleAnswerTeachTypeModule(moduleManager)
