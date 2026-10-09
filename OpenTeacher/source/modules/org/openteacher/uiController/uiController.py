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

import os
import sys
import contextlib
import logging

logger = logging.getLogger(__name__)

class UiControllerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(UiControllerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "uiController"
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="metadata"),
			self._mm.mods(type="execute"),
		)
		self.uses = (
			self._mm.mods(type="settingsDialog"),
			self._mm.mods(type="about"),
			self._mm.mods(type="documentation"),
			self._mm.mods(type="translator"),
			self._mm.mods(type="loader"),
			self._mm.mods(type="saver"),
			self._mm.mods(type="printer"),
			self._mm.mods(type="printDialog"),
			self._mm.mods(type="fileDialogs"),
			self._mm.mods(type="lessonTracker"),
			self._mm.mods(type="dataStore"),
			self._mm.mods(type="dialogShower"),
			self._mm.mods(type="reverser"),
		)
		self.filesWithTranslations = ("uiController.py",)
		self.priorities = {
			"student@home": 0,
			"student@school": 0,
			"teacher": 0,
			"words-only": 0,
			"selfstudy": 0,
			"all": 0,
			"default": -1,
		}

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		try:
			self._store = self._modules.default(type="dataStore").store
		except IndexError:
			self._store = {}
		try:
			self._fileDialogs = self._modules.default("active", type="fileDialogs")
		except IndexError:
			self._fileDialogs = None
		try:
			self._printDialog = self._modules.default("active", type="printDialog")		
		except IndexError:
			self._printDialog = None
		try:
			self._lessonTracker = self._modules.default("active", type="lessonTracker")
		except IndexError:
			self._lessonTracker = None
		try:
			self._loader = self._modules.default("active", type="loader")
		except IndexError:
			self._loader = None

		try:
			self._saver = self._modules.default("active", type="saver")
		except IndexError:
			self._saver = None
		self._execute = self._modules.default(type="execute")

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self._execute.startRunning.handle(self.run)

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

	def disable(self):
		self.active = False

		self._execute.startRunning.unhandle(self.run)

		del self._modules
		del self._fileDialogs
		del self._printDialog
		del self._lessonTracker
		del self._loader
		del self._saver
		del self._execute
		del self._store

	def run(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._uiModule = self._modules.default("active", type="ui")

		self._connectEvents()
		self._updateMenuItems()

		with contextlib.ignored(IndexError):
			self.open_(sys.argv[1])

		self._uiModule.run(self._onCloseRequested)
		self._disconnectEvents()

	def _onCloseRequested(self):
		for lesson in self._lessonTracker.lessons:
			#set the file tab focussed
			self._uiModule.currentFileTab = lesson.fileTab
			#try to close it
			if not lesson.stop():
				#not ready to stop, don't allow it.
				return False
		#ready to stop, allow it.
		return True

	def new(self):
		self._uiModule.showStartTab()

	@property
	def _lastPath(self):
		try:
			return self._store["org.openteacher.uiController.lastPath"]
		except KeyError:
			return os.path.expanduser("~")

	@_lastPath.setter
	def _lastPath(self, path):
		self._store["org.openteacher.uiController.lastPath"] = path

	def _showErrorAndPrintException(self, msg):
		logger.debug(u"Catched exception, showing nice error ('%s'):" % msg, exc_info=True)
		self._showError(msg)

	def _showError(self, msg):
		tab = self._uiModule.currentFileTab or self._uiModule.startTab
		try:
			self._modules.default("active", type="dialogShower").showError.send(tab, msg)
		except IndexError:
			#fallback
			print msg

	def _getFilePath(self, onSuccess, onError=None):
		usableExtensions = self._loader.usableExtensions
		self._fileDialogs.getLoadPath(
			onSuccess,
			self._lastPath,
			usableExtensions,
			onError=onError
		)

	def _handleLoadException(self, exc):
		if isinstance(exc, NotImplementedError):
			self._showErrorAndPrintException(_("Couldn't open the file, because the file type is unknown or it can't be shown."))
		elif isinstance(exc, IOError):
			self._showErrorAndPrintException(_("Couldn't open the file, is it still there and do we have the right to open it?"))
		else:
			self._showErrorAndPrintException(_("Couldn't open the file, it seems to be corrupted."))

	def open_(self, path=None):
		def onSuccess(chosenPath):
			try:
				self._loader.load(chosenPath)
			except Exception, e:
				self._handleLoadException(e)
			else:
				self._lastPath = chosenPath
				self._uiModule.statusViewer.show(_("File opened succesfully."))
		if path:
			onSuccess(path)
		else:
			self._getFilePath(onSuccess)

	def openInto(self):
		def onFinished(tab):
			self._uiModule.currentFileTab = tab

		def onSuccess(tab, path):
			onFinished(tab)

			currentLesson = self._lessonTracker.currentLesson
			dataType = currentLesson.dataType
			try:
				type, lessonData = self._loader.loadToLesson(path, [dataType])
			except NotImplementedError:
				self._showError(_("Can't merge files of different file types."))
			except Exception, e:
				self._handleLoadException(e)
			else:
				self._mergeIntoCurrentLesson(currentLesson, type, lessonData)

		lessonTab = self._lessonTracker.currentLesson.fileTab
		self._getFilePath(
			lambda path: onSuccess(lessonTab, path),
			onError=lambda: onFinished(lessonTab)
		)

	def _mergeIntoCurrentLesson(self, currentLesson, type, otherLessonData):
		merge = self._modules.default("active", type="merger", dataType=type).merge

		currentLessonData = merge({
			"list": currentLesson.list,
			"resources": currentLesson.resources,
		}, otherLessonData)
		currentLesson.list = currentLessonData["list"]
		currentLesson.resources = currentLessonData["resources"]

		self._uiModule.statusViewer.show(_("Opened file into the current list succesfully."))

	def _doSave(self, path):
		try:
			self._saver.save(path)
		except IOError:
			self._showErrorAndPrintException(_("Couldn't save the file, is there enough free disk space and do we have the right to write to the specified location?"))
		else:
			self._uiModule.statusViewer.show(_("File saved succesfully."))

	def save(self, path=None):
		if not path:
			try:
				path = self._lessonTracker.currentLesson.path
			except AttributeError:
				self.saveAs()
				return
		if path:
			self._doSave(path)
		else:
			self.saveAs()

	def saveAs(self):
		def onSuccess(path):
			self._lastPath = path
			self._doSave(path)

		self._fileDialogs.getSavePath(
			onSuccess,
			self._lastPath,
			#sort on names (not extensions)
			sorted(self._saver.usableExtensions, key=lambda ext: ext[1]),
			#default (== top most) extension
			self._saver.usableExtensions[0]
		)

	def print_(self):
		#Setup printer
		qtPrinter = self._printDialog.getConfiguredPrinter()
		if qtPrinter is None:
			return

		printer = self._modules.default("active", type="printer")
		printer.print_(qtPrinter)

	def _connectEvents(self): 
		#file
		self._uiModule.newAction.triggered.handle(self.new)
		self._uiModule.openAction.triggered.handle(self.open_)
		self._uiModule.openIntoAction.triggered.handle(self.openInto)
		self._uiModule.saveAction.triggered.handle(self.save)
		self._uiModule.saveAsAction.triggered.handle(self.saveAs)
		self._uiModule.printAction.triggered.handle(self.print_)
		self._uiModule.quitAction.triggered.handle(self.quit_)

		#edit
		self._uiModule.reverseAction.triggered.handle(self.reverse)
		self._uiModule.settingsAction.triggered.handle(self.settings)

		#view
		self._uiModule.fullscreenAction.toggled.handle(self.fullscreen)

		#help
		self._uiModule.aboutAction.triggered.handle(self.about)
		self._uiModule.documentationAction.triggered.handle(self.documentation)

		self._lessonTracker.lessonChanged.handle(self._updateMenuItems)

	def _disconnectEvents(self):
		self._uiModule.newAction.triggered.unhandle(self.new)
		self._uiModule.openAction.triggered.unhandle(self.open_)
		self._uiModule.openIntoAction.triggered.unhandle(self.openInto)
		self._uiModule.saveAction.triggered.unhandle(self.save)
		self._uiModule.saveAsAction.triggered.unhandle(self.saveAs)
		self._uiModule.printAction.triggered.unhandle(self.print_)
		self._uiModule.quitAction.triggered.unhandle(self.quit_)

		self._uiModule.reverseAction.triggered.unhandle(self.reverse)
		self._uiModule.settingsAction.triggered.unhandle(self.settings)

		self._uiModule.aboutAction.triggered.unhandle(self.about)
		self._uiModule.documentationAction.triggered.unhandle(self.documentation)

		self._lessonTracker.lessonChanged.unhandle(self._updateMenuItems)

	def _updateMenuItems(self):
		#subscribe self to the lesson (if it's there nothing happens
		#due to the internal implementation of event. Which is also
		#guaranteed by a test suite test, btw. So it's by design.)
		if hasattr(self._lessonTracker.currentLesson, "changedEvent"):
			self._lessonTracker.currentLesson.changedEvent.handle(self._updateMenuItems)

		#new, hide when already on the +-tab
		hideNew = self._uiModule.startTabActive
		self._uiModule.newAction.enabled = not hideNew

		#open
		try:
			openSupport = self._loader.openSupport
		except TypeError:
			openSupport = False
		openSupport = openSupport and self._fileDialogs is not None
		self._uiModule.openAction.enabled = openSupport

		#open into
		try:
			dataType = self._lessonTracker.currentLesson.dataType
		except AttributeError:
			openIntoSupport = False
		else:
			openIntoSupport = len(set(self._mm.mods("active", type="merger", dataType=dataType))) != 0
		openIntoSupport = openIntoSupport and openSupport
		self._uiModule.openIntoAction.enabled = openIntoSupport

		#save
		saveSupport = self._saver.saveSupport if self._saver else False
		saveSupport = saveSupport and self._fileDialogs is not None
		self._uiModule.saveAsAction.enabled = saveSupport

		try:
			enableSave = saveSupport and self._lessonTracker.currentLesson.changed
		except AttributeError:
			enableSave = saveSupport #assume changed
		self._uiModule.saveAction.enabled = enableSave

		#print
		try:
			printer = self._modules.default("active", type="printer")
		except IndexError:
			printSupport = False
		else:
			printSupport = printer.printSupport
		printSupport = printSupport and self._printDialog is not None
		self._uiModule.printAction.enabled = printSupport

		#reverse
		try:
			dataType = self._lessonTracker.currentLesson.dataType
		except AttributeError:
			reverserSupport = False
		else:
			reverserSupport = len(set(self._mm.mods("active", type="reverser", dataType=dataType))) != 0
		self._uiModule.reverseAction.enabled = reverserSupport

		#settings
		settingsSupport = len(set(self._mm.mods("active", type="settingsDialog"))) != 0
		self._uiModule.settingsAction.enabled = settingsSupport

		#about
		aboutSupport = len(set(self._mm.mods("active", type="about"))) != 0
		self._uiModule.aboutAction.enabled = aboutSupport

		#documentation
		docSupport = len(set(self._mm.mods("active", type="documentation"))) != 0
		self._uiModule.documentationAction.enabled = docSupport

	def reverse(self):
		l = self._lessonTracker.currentLesson
		reverse = self._modules.default("active", type="reverser", dataType=l.dataType).reverse
		theList = l.list
		reverse(theList)
		l.list = theList
		l.changed = True

	def settings(self):
		self._modules.default("active", type="settingsDialog").show()

	def fullscreen(self, bool):
		self._uiModule.setFullscreen(bool)

	def about(self):
		self._modules.default("active", type="about").show()

	def documentation(self):
		self._modules.default("active", type="documentation").show()

	def quit_(self):
		self._uiModule.interrupt()

def init(moduleManager):
	return UiControllerModule(moduleManager)
