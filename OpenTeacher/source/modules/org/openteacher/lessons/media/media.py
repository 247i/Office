#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Milan Boers
#	Copyright 2011-2013, Marten de Vries
#	Copyright 2011-2012, Cas Widdershoven
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
import weakref

#FIXME? Make the whole module make use of a .resources attribute like
#topo. It would make media savers and loaders a lot easier to write (see
#mediaHtml.py and the loader and saver otmd.py). Downside: breaks
#compatibility. :(
#
#Maybe a solution: deprecate the filename key and replace it by
#a 'resource' key. (and 'link' in the case of 'remote'), but give it a
#content for backward compatibility. Doesn't fix the clutter in the otmd
#savers, but the general problem would be solved by that I guess...

class MediaLessonModule(object):
	"""The module"""

	def __init__(self, mm,*args,**kwargs):
		super(MediaLessonModule, self).__init__(*args, **kwargs)
		
		self._mm = mm

		self.type = "lesson"
		x = 667
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

		self.dataType = "media"

		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="dataTypeIcons"),
		)
		self.requires = (
			self._mm.mods(type="event"),
			self._mm.mods(type="ui"),
			self._mm.mods(type="buttonRegister"),
			self._mm.mods(type="mediaEnterer"),
			self._mm.mods(type="mediaTeacher"),
			self._mm.mods(type="testsViewer"),
		)
		self.filesWithTranslations = ("media.py",)

	def enable(self):
		global QtGui
		try:
			from PyQt4 import QtGui
		except ImportError:
			return
		self._modules = set(self._mm.mods(type="modules")).pop()
		
		self._lessons = set()

		module = self._modules.default("active", type="buttonRegister")
		self._button = module.registerButton("create")
		self._button.clicked.handle(self.createLesson)
		try:
			iconPath = self._modules.default("active", type="dataTypeIcons").findIcon(self.dataType)
		except (IndexError, KeyError):
			pass
		else:
			self._button.changeIcon.send(iconPath)
		#reasonable priority
		self._button.changePriority.send(self.priorities["all"])

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
		del self.lessonCreated
		del self.lessonCreationFinished

	def createLesson(self):	
		module = self._modules.default("active", type="ui")

		self.enterWidget = self._modules.default("active", type="mediaEnterer").createMediaEnterer()
		self.teachWidget = self._modules.default("active", type="mediaTeacher").createMediaTeacher()
		self.resultsWidget = self._modules.default("active", type="testsViewer").createTestsViewer()

		self.fileTab = module.addFileTab(
			self.enterWidget,
			self.teachWidget,
			self.resultsWidget
		)

		lesson = Lesson(self._modules, self.fileTab, self.enterWidget, self.teachWidget, self.resultsWidget)
		self._lessons.add(weakref.ref(lesson))
		self.lessonCreated.send(lesson)

		#so it can set the changed property
		self.enterWidget.lesson = lesson

		self.lessonCreationFinished.send()
		return lesson
	
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
			
		self._button.changeText.send(_("Create media lesson"))
		for ref in self._lessons:
			lesson = ref()
			if lesson:
				lesson.retranslate()

class Lesson(object):
	"""Lesson object (that means: this teachwidget+enterwidget)"""

	def __init__(self, modules, fileTab, enterWidget, teachWidget, resultsWidget, *args, **kwargs):
		super(Lesson, self).__init__(*args, **kwargs)
		
		self._modules = modules
		
		self.enterWidget = enterWidget
		self.teachWidget = teachWidget
		self.resultsWidget = resultsWidget
		self.fileTab = fileTab

		#default
		self._changed = False

		self.stopped = self._modules.default(type="event").createEvent()
		
		self.module = self
		self.resources = {}
		self.dataType = "media"
		
		self.fileTab.closeRequested.handle(self.stop)
		self.fileTab.tabChanged.handle(self.tabChanged)
		self.teachWidget.lessonDone.connect(self.toEnterTab)
		self.teachWidget.listChanged.connect(self.teachListChanged)

		self.changedEvent = self._modules.default(type="event").createEvent()

		self.retranslate()

	def _updateTitle(self):
		title = self.list.get("title", u"")
		if not title:
			title = _("Unnamed")
		self.fileTab.title = _("Media lesson: %s") % title

	retranslate = _updateTitle

	@property
	def changed(self):
		return self._changed

	@changed.setter
	def changed(self, value):
		self._changed = value
		self._updateTitle()
		self.changedEvent.send()

	@changed.deleter
	def changed(self):
		del self._changed

	@property
	def list(self):
		return self.enterWidget.list

	@list.setter
	def list(self, list):
		# Load the list
		self.enterWidget.list = list
		# Update the widgets
		self.enterWidget.updateWidgets()
		# Update the results widget
		self.resultsWidget.updateList(list, "media")

	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, path):
		self._path = path
		# Update title
		self.fileTab.title = _("Media lesson: %s") % os.path.basename(self.path)

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

		#really stop
		self.fileTab.close()
		# Stop media playing
		self.enterWidget.mediaDisplay.stop()
		self.teachWidget.mediaDisplay.stop()
		self.stopped.send()
		return True
	
	def teachListChanged(self, list):
		# Update results widget
		self.resultsWidget.updateList(list, "media")
		self.changed = True
	
	def toEnterTab(self):
		self.fileTab.currentTab = self.enterWidget

	def tabChanged(self):
		"""First do checks that apply to all lessons. In case they don't
		   show any problems, the callback with media specific checks is
		   called.

		"""
		#FIXME 3.1: move into separate module since this uses QtGui?
		def callback():
			#media specific checks
			for item in self.enterWidget.list["items"]:
				if not item.get("question", "") or not item.get("answer", ""):
					QtGui.QMessageBox.critical(
						self.teachWidget,
						_("Empty question or answer"),
						_("Please enter at least one question and one answer for every item.")
					)
					self.fileTab.currentTab = self.enterWidget
					return

			#everything ok, initiate lesson.
			self.teachWidget.initiateLesson(self.enterWidget.list)

		#generic checks
		lessonDialogsModule = self._modules.default("active", type="lessonDialogs")
		lessonDialogsModule.onTabChanged(self.fileTab, self.enterWidget, self.teachWidget, callback)

def init(moduleManager):
	return MediaLessonModule(moduleManager)
