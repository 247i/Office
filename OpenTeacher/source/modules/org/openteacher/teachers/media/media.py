#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Milan Boers
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

import datetime
import weakref
import contextlib

def installQtClasses():
	global TeachLessonTypeChooser, TeachWidget

	class TeachLessonTypeChooser(QtGui.QComboBox):
		"""The dropdown menu to choose lesson type"""

		currentIndexChanged = QtCore.pyqtSignal([int])

		def __init__(self,*args,**kwargs):
			super(TeachLessonTypeChooser, self).__init__(*args, **kwargs)

			self.retranslate()

		def retranslate(self):
			#disconnect the signal, so we can change some stuff without
			#other classes notice
			with contextlib.ignored(TypeError):
				#TypeError: not yet connected (first pass)
				super(TeachLessonTypeChooser, self).currentIndexChanged.disconnect(self.currentIndexChanged.emit)

			#save status
			i = self.currentIndex()

			#update data
			self.clear()
			self._lessonTypeModules = base._modules.sort("active", type="lessonType")
			for lessontype in self._lessonTypeModules:
				self.addItem(lessontype.name, lessontype)

			#restore status
			if i != -1:
				self.setCurrentIndex(i)

			#re-connect signal
			super(TeachLessonTypeChooser, self).currentIndexChanged.connect(self.currentIndexChanged.emit)

		@property
		def currentLessonType(self):
			"""Get the current lesson type"""

			return self._lessonTypeModules[self.currentIndex()]

	class TeachWidget(QtGui.QWidget):
		"""The teach tab"""

		lessonDone = QtCore.pyqtSignal()
		listChanged = QtCore.pyqtSignal([object])
		def __init__(self,*args, **kwargs):
			super(TeachWidget, self).__init__(*args, **kwargs)
			
			self.inLesson = False
			
			#draw the GUI
			
			top = QtGui.QHBoxLayout()
			
			self.label = QtGui.QLabel()
			self.lessonTypeChooser = TeachLessonTypeChooser()
			self.lessonTypeChooser.currentIndexChanged.connect(self.changeLessonType)

			top.addWidget(self.label)
			top.addWidget(self.lessonTypeChooser)
			
			self.nameLabel = QtGui.QLabel()
			font = QtGui.QFont()
			font.setPointSize(14)
			self.nameLabel.setFont(font)
			
			self.mediaDisplay = base._modules.default("active", type="mediaDisplay").createDisplay(True)
			
			self.questionLabel = QtGui.QLabel()
			
			self.answerField = QtGui.QLineEdit()
			self.answerField.returnPressed.connect(self.checkAnswerButtonClick)

			self.checkButton = QtGui.QPushButton()
			self.checkButton.clicked.connect(self.checkAnswerButtonClick)
			
			self.progress = QtGui.QProgressBar()
			
			bottomL = QtGui.QHBoxLayout()
			bottomL.addWidget(self.answerField)
			bottomL.addWidget(self.checkButton)
			bottomL.addWidget(self.progress)
			
			layout = QtGui.QVBoxLayout()
			layout.addLayout(top)
			layout.addWidget(self.mediaDisplay)
			layout.addWidget(self.nameLabel)
			layout.addWidget(self.questionLabel)
			layout.addLayout(bottomL)
			
			self.setLayout(layout)
			self.retranslate()

		def retranslate(self):
			#TRANSLATORS: lesson types are e.g. 'smart', 'all once' and 'interval'
			self.label.setText(_("Lesson type:"))
			#TRANSLATORS: a button which the user presses to tell the computer it should check his/her answer.
			self.checkButton.setText(_("Check"))

			self.lessonTypeChooser.retranslate()

		def initiateLesson(self, items):
			"""Starts the lesson"""

			self.items = items
			self.lesson = TeachMediaLesson(items, self)
			self.answerField.setFocus()
		
		def restartLesson(self):
			"""Restarts the lesson"""

			self.initiateLesson(self.items)
		
		def changeLessonType(self, index):
			"""What happens when you change the lesson type"""

			if self.inLesson:
				self.restartLesson()
		
		def stopLesson(self, showResults=True):
			"""Stops the lesson"""

			self.lesson.endLesson(showResults)
			del self.lesson
		
		def checkAnswerButtonClick(self):
			"""What happens when you click the check answer button"""

			self.lesson.checkAnswer()
			self.answerField.clear()
			self.answerField.setFocus()


class TeachMediaLesson(object):	
	"""The lesson itself (being teached)"""

	def __init__(self,itemList,teachWidget,*args,**kwargs):
		super(TeachMediaLesson, self).__init__(*args, **kwargs)
		
		self.teachWidget = teachWidget
		
		self.itemList = itemList
		self.lessonType = self.teachWidget.lessonTypeChooser.currentLessonType.createLessonType(self.itemList,range(len(itemList["items"])))
		
		self.lessonType.newItem.handle(self.nextQuestion)
		self.lessonType.lessonDone.handle(self.endLesson)
		
		self.lessonType.start()
		
		self.teachWidget.inLesson = True
		
		# Reset the progress bar
		self.teachWidget.progress.setValue(0)
	
	def checkAnswer(self):
		"""Check whether the given answer was right or wrong"""

		# Set the end of the thinking time
		self.endThinkingTime = datetime.datetime.now()
		
		active = {
			"start": self.startThinkingTime,
			"end": self.endThinkingTime
		}
		
		if self.currentItem["answer"] == self.teachWidget.answerField.text():
			# Answer was right
			self.lessonType.setResult({
					"itemId": self.currentItem["id"],
					"result": "right",
					"givenAnswer": unicode(self.teachWidget.answerField.text()),
					"active": active
				})
			# Progress bar
			self._updateProgressBar()
		else:
			# Answer was wrong
			self.lessonType.setResult({
					"itemId": self.currentItem["id"],
					"result": "wrong",
					"givenAnswer": unicode(self.teachWidget.answerField.text()),
					"active": active
				})
		
		self.teachWidget.listChanged.emit(self.itemList)
			
	def nextQuestion(self, item):
		"""What happens when the next question should be asked"""

		# set the next question
		self.currentItem = item
		# set the question field
		self.teachWidget.questionLabel.setText(self.currentItem["question"])
		# set the name field
		self.teachWidget.nameLabel.setText(self.currentItem["name"])
		# set the mediawidget to the right location
		self.teachWidget.mediaDisplay.showMedia(self.currentItem["filename"], self.currentItem["remote"], True)
		# Set the start of the thinking time to now
		self.startThinkingTime = datetime.datetime.now()
		# Delete the end of the thinking time
		with contextlib.ignored(AttributeError):
			del self.endThinkingTime

	def endLesson(self, showResults=True):
		"""Ends the lesson"""

		self.teachWidget.inLesson = False

		# stop media
		self.teachWidget.mediaDisplay.clear()
		
		# Update and go to results widget, only if the test is progressing
		try:
			self.itemList["tests"][-1]
		except IndexError:
			pass
		else:
			if showResults:
				with contextlib.ignored(IndexError):
					# Go to results widget
					module = base._modules.default("active", type="resultsDialog")
					module.showResults(self.itemList, "media", self.itemList["tests"][-1])
		
		self.teachWidget.lessonDone.emit()
	
	def _updateProgressBar(self):
		"""Updates the progress bar"""

		self.teachWidget.progress.setMaximum(self.lessonType.totalItems+1)
		self.teachWidget.progress.setValue(self.lessonType.askedItems)

class MediaTeacherModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(MediaTeacherModule, self).__init__(*args, **kwargs)
		
		global base
		base = self
		
		self._mm = moduleManager
		
		self.type = "mediaTeacher"
		self.priorities = {
			"default": 520,
		}
		
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="resultsDialog"),
		)
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="mediaDisplay"),
		)
		self.filesWithTranslations = ("media.py",)
	
	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()

		self._widgets = set()

		#setup translation
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
			translator.languageChangeDone.handle(self._retranslateWhenFirstRetranslateIsOver)
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

	def _retranslateWhenFirstRetranslateIsOver(self):
		for ref in self._widgets:
			widget = ref()
			if widget is not None:
				widget.retranslate()

	def disable(self):
		self.active = False

		del self._modules
		del self._widgets
	
	def createMediaTeacher(self):
		tw = TeachWidget()
		self._widgets.add(weakref.ref(tw))
		return tw

def init(moduleManager):
	return MediaTeacherModule(moduleManager)
