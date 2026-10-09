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

import os
import tempfile
import atexit
import weakref

class TeachTopoLessonModule(object):
	"""The module"""

	def __init__(self, moduleManager, *args, **kwargs):
		super(TeachTopoLessonModule, self).__init__(*args, **kwargs)
		
		self._mm = moduleManager
		self.counter = 1
		
		self.type = "lesson"
		x = 580
		self.priorities = {
			"all": x,
			"selfstudy": x,
			"student@home": x,
			"student@school": x,
			"teacher": x,
			"code-documentation": x,
			"test-suite": x,
			"default": -1,
		}
		
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="dataTypeIcons"),
		)
		self.requires = (
			self._mm.mods(type="event"),
			self._mm.mods(type="ui"),
			self._mm.mods(type="lessonDialogs"),
			self._mm.mods(type="buttonRegister"),
			self._mm.mods(type="topoTeacher"),
			self._mm.mods(type="topoEnterer"),
			self._mm.mods(type="testsViewer"),
		)
		self.filesWithTranslations = ("topo.py",)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		
		self._lessons = set()

		# Data type & icon
		self.dataType = "topo"

		# Add the button to start
		module = self._modules.default("active", type="buttonRegister")
		self._button = module.registerButton("create")
		try:
			iconPath = self._modules.default("active", type="dataTypeIcons").findIcon(self.dataType)
		except (IndexError, KeyError):
			pass
		else:
			self._button.changeIcon.send(iconPath)
		self._button.clicked.handle(self.createLesson)
		#reasonable priority
		self._button.changePriority.send(self.priorities["all"])

		# Signals
		self.lessonCreated = self._modules.default(type="event").createEvent()
		self.lessonCreationFinished = self._modules.default(type="event").createEvent()

		#setup translation
		global _
		global ngettext

		#load translator	
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()
		
		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._lessons
		del self._button
		del self.dataType
		del self.lessonCreated
		del self.lessonCreationFinished
		
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
			
		self._button.changeText.send(_("Create topography lesson"))
		for ref in self._lessons:
			lesson = ref()
			if lesson:
				lesson.retranslate()
	
	def createLesson(self):
		module = self._modules.default("active", type="ui")
		
		enterWidget = self._modules.default("active", type="topoEnterer").createTopoEnterer()
		teachWidget = self._modules.default("active", type="topoTeacher").createTopoTeacher()
		resultsWidget = self._modules.default("active", type="testsViewer").createTestsViewer()
		
		self.fileTab = module.addFileTab(
			enterWidget,
			teachWidget,
			resultsWidget
		)

		lesson = Lesson(self._modules, self.fileTab, enterWidget, teachWidget, resultsWidget, self.counter)
		self._lessons.add(weakref.ref(lesson))
		self.lessonCreated.send(lesson)

		#so they can send changedEvents
		enterWidget.lesson = lesson
		teachWidget.lesson = lesson

		self.counter += 1
		self.lessonCreationFinished.send()
		return lesson

class Lesson(object):
	"""Lesson object (that means: this techwidget+enterwidget)"""

	def __init__(self, modules, fileTab, enterWidget, teachWidget, resultsWidget, counter, *args, **kwargs):
		super(Lesson, self).__init__(*args, **kwargs)

		self._modules = modules
		self._tempFiles = set()
		atexit.register(self._removeTempFiles)

		self.enterWidget = enterWidget
		self.teachWidget = teachWidget
		self.resultsWidget = resultsWidget
		self.fileTab = fileTab
		self.counter = counter

		#default
		self._changed = False

		self.stopped = self._modules.default(type="event").createEvent()

		self.module = self
		self.dataType = "topo"

		fileTab.closeRequested.handle(self.stop)
		fileTab.tabChanged.handle(self.tabChanged)
		self.teachWidget.lessonDone.connect(self.toEnterTab)
		self.teachWidget.listChanged.connect(self.teachListChanged)

		self.changedEvent = self._modules.default(type="event").createEvent()

		self.retranslate()

	@property
	def changed(self):
		return self._changed

	@changed.setter
	def changed(self, value):
		self._changed = value
		self.changedEvent.send()

	@changed.deleter
	def changed(self):
		del self._changed

	@property
	def list(self):
		return self.enterWidget.list

	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, path):
		#TRANSLATORS: used as a label in case a filename of a topo
		#TRANSLATORS: lesson isn't available. (E.g. because it's
		#TRANSLATORS: downloaded from some kind of web service.)
		fileName = path or _("Import source")

		self.enterWidget.mapChooser.insertItem(0, fileName, unicode({'mapPath': self.resources["mapPath"], 'knownPlaces': ''}))
		self.enterWidget.mapChooser.setCurrentIndex(0)

		# Update title
		self.fileTab.title = _("Topo lesson: %s") % os.path.basename(path)

		self._path = path

	@list.setter
	def list(self, list):
		# Load the list
		self.enterWidget.list = list
		# Update the widgets
		self.enterWidget.updateWidgets()
		# Update results widget
		self.resultsWidget.updateList(list, "topo")

	@property
	def resources(self):
		fd, screenshotPath = tempfile.mkstemp()
		os.close(fd)
		self._tempFiles.add(screenshotPath)

		screenshot = self.enterWidget.enterMap.getScreenshot()
		screenshot.save(screenshotPath, "PNG")

		return {
			"mapPath": self.enterWidget.mapChooser.currentMap["mapPath"],
			"mapScreenshot": screenshotPath,
		}

	@resources.setter
	def resources(self, resources):
		self._resources = resources
	
	def stop(self):
		#close current lesson (if one). Just reuse all the logic.
		self.fileTab.currentTab = self.enterWidget
		self.tabChanged()
		if self.fileTab.currentTab == self.teachWidget:
			#the tab change wasn't allowed.
			return False

		#ask if the user wants to save
		if self.changed:
			lessonDialogsModule = self._modules.default("active", type="lessonDialogs")
			if not lessonDialogsModule.okToClose(parent=self.fileTab.currentTab):
				return False

		self.fileTab.close()
		self.stopped.send()

		return True
	
	def toEnterTab(self):
		self.fileTab.currentTab = self.enterWidget
	
	def teachListChanged(self, list):
		self.resultsWidget.updateList(list, "topo")
		self.changed = True
	
	def tabChanged(self):
		lessonDialogsModule = self._modules.default("active", type="lessonDialogs")
		lessonDialogsModule.onTabChanged(self.fileTab, self.enterWidget, self.teachWidget, lambda: self.teachWidget.initiateLesson(self.enterWidget.list, self.enterWidget.mapChooser.currentMap["mapPath"]))

	def _removeTempFiles(self):
		for file in self._tempFiles:
			os.remove(file)
			
	def retranslate(self):
		try:
			self.fileTab.title = _("Topo lesson: %s") % os.path.basename(self.path)
		except AttributeError:
			self.fileTab.title = _("Topo lesson: %s") % self.counter

def init(moduleManager):
	return TeachTopoLessonModule(moduleManager)
