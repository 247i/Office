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

import sys
import os
import platform
import logging
import warnings

qtLogger = logging.getLogger("qt")

class Action(object):
	"""A high-level interface to a menu and/or a toolbar item."""

	def __init__(self, createEvent, qtMenu, qtAction, *args, **kwargs):
		super(Action, self).__init__(*args, **kwargs)

		self._qtMenu = qtMenu
		self._qtAction = qtAction

		self.triggered = createEvent()
		self.toggled = createEvent()
		#lambda to prevent useless Qt arguments to pass
		self._qtAction.triggered.connect(lambda: self.triggered.send())
		self._qtAction.toggled.connect(self.toggled.send)

	def remove(self):
		self._qtMenu.removeAction(self._qtAction)
		self._qtMenu.menuActions.remove(self._qtAction)

	text = property(
		lambda self: unicode(self._qtAction.text()),
		lambda self, value: self._qtAction.setText(value)
	)

	enabled = property(
		lambda self: self._qtMenu.isEnabled(),
		lambda self, value: self._qtAction.setEnabled(value)
	)

class Menu(object):
	"""A high-level interface to a menu (as in File, Edit, etc.)."""

	def __init__(self, event, qtMenu, *args, **kwargs):
		super(Menu, self).__init__(*args, **kwargs)

		self._createEvent = event
		self._qtMenu = qtMenu
		self._qtMenu.menuActions = set()

	def _actionAfter(self, priority):
		actions = sorted(
			self._qtMenu.menuActions,
			key=lambda a: getattr(a, "menuPriority", 0)
		)
		for action in actions:
			if getattr(action, "menuPriority", 0) > priority:
				return action
		#explicit is better than implicit
		return None

	def addAction(self, priority):
		qtAction = QtGui.QAction(self._qtMenu)
		qtAction.menuPriority = priority
		self._qtMenu.insertAction(self._actionAfter(priority), qtAction)
		self._qtMenu.menuActions.add(qtAction)
		return Action(self._createEvent, self._qtMenu, qtAction)

	def addMenu(self, priority):
		qtSubMenu = QtGui.QMenu()
		self._qtMenu.insertMenu(self._actionAfter(priority), qtSubMenu)
		return Menu(self._createEvent, qtSubMenu)

	def remove(self):
		self._qtMenu.hide()

	text = property(
		lambda self: unicode(self._qtMenu.title()),
		lambda self, value: self._qtMenu.setTitle(value)
	)

	enabled = property(
		lambda self: self._qtMenu.isEnabled(),
		lambda self, value: self._qtMenu.setEnabled(value)
	)

class StatusViewer(object):
	"""A high-level interface to the status bar."""
	def __init__(self, statusBar, *args, **kwargs):
		super(StatusViewer, self).__init__(*args, **kwargs)

		self._statusBar = statusBar

	def show(self, message):
		self._statusBar.showMessage(message)

class FileTab(object):
	def __init__(self, moduleManager, tabWidget, widget, lastWidget, *args, **kwargs):
		super(FileTab, self).__init__(*args, **kwargs)

		self._modules = next(iter(moduleManager.mods(type="modules")))

		self._tabWidget = tabWidget
		self._widget = widget
		self._lastWidget = lastWidget

		self.closeRequested = self._modules.default(
			type="event"
		).createEvent()

		tabBar = self._tabWidget.tabBar()
		closeButton = tabBar.tabButton(self._index, QtGui.QTabBar.RightSide)
		if not closeButton:
			#the mac os x case
			closeButton = tabBar.tabButton(self._index, QtGui.QTabBar.LeftSide)
		closeButton.clicked.connect(lambda: self.closeRequested.send())
		closeButton.setShortcut(QtGui.QKeySequence.Close)

	@property
	def _index(self):
		return self._tabWidget.indexOf(self._widget.wrapperWidget)

	def close(self):
		self._tabWidget.removeTab(self._index)
		if self._lastWidget:
			self._tabWidget.setCurrentWidget(self._lastWidget)

	title = property(
		lambda self: self._tabWidget.tabText(self._index),
		lambda self, val: self._tabWidget.setTabText(self._index, val)
	)

class LessonFileTab(FileTab):
	def __init__(self, *args, **kwargs):
		super(LessonFileTab, self).__init__(*args, **kwargs)

		#properties are defined in parent class
		self.tabChanged = self._modules.default(type="event").createEvent()
		self._widget.currentChanged.connect(lambda: self.tabChanged.send())

	def retranslate(self):
		"""Called by the uiController module."""
		self._widget.retranslate()

	currentTab = property(
		lambda self: self._widget.currentWidget(),
		lambda self, value: self._widget.setCurrentWidget(value)
	)

class GuiModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(GuiModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "ui"
		self.requires = (
			self._mm.mods(type="event"),
			self._mm.mods(type="startWidget"),
			self._mm.mods(type="metadata"),
		)
		self.uses = (
			self._mm.mods(type="buttonRegister"),
			self._mm.mods(type="translator"),
			self._mm.mods(type="settings"),
		)
		self.priorities = {
			"gtk": -1,
		}
		self.filesWithTranslations = ("gui.py", "ui.py")

	def _msgHandler(self, type, message):
		typeName = {
			QtCore.QtDebugMsg: "DEBUG",
			QtCore.QtWarningMsg: "WARNING",
			QtCore.QtCriticalMsg: "CRITICAL",
			QtCore.QtFatalMsg: "FATAL",
			QtCore.QtSystemMsg: "SYSTEM",
		}[type]
		qtLogger.debug("%s: %s" % (typeName, message))

	def enable(self):
		warnings.warn("On Ubuntu, when going out of fullscreen mode, the native menu bar isn't restored due to a Unity bug. Remove that check when it's fixed from gui.py.")

		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return

		QtCore.qInstallMsgHandler(self._msgHandler)
		if hasattr(QtGui.QApplication, "x11EventFilter") and os.getenv("DISPLAY") is None:
			#if on a system that could potentially support X11, but
			#doesn't have it installed/running, leave this mod disabled.
			#Otherwise the whole application crashes on a 'Can't connect
			#to display' error message.
			#
			#checking for x11EventFilter because that is only defined
			#when Q_WS_X11 is set. No other way as far as I know to get
			#the value of that property. :(
			return

		#prevents that calling enable() and disable() multiple times
		#segfaults.
		self._app = QtGui.QApplication.instance()
		if not self._app:
			self._app = QtGui.QApplication(sys.argv)

		self._modules = set(self._mm.mods(type="modules")).pop()
		createEvent = self._modules.default(type="event").createEvent

		self.tabChanged = createEvent()
		self.tabChanged.__doc__ = (
			"This ``Event`` allows you to detect when the user " +
			"switches to another tab."
		)
		self.applicationActivityChanged = createEvent()
		self.applicationActivityChanged.__doc__ = (
			"Handlers of this ``Event`` are called whenever the user " +
			"is switching between OpenTeacher and some other " +
			"program. They get one argument: ``'active'`` or " +
			"``'inactive'`` depending on if the user started to use " +
			"OpenTeacher or stopped using it."
		)

		self._ui = self._mm.import_("ui")
		self._ui.ICON_PATH = self._mm.resourcePath("icons/")

		# Add Aero glass option on Windows
		try:
			settings = self._modules.default(type="settings")
		except IndexError, e:
			self._aeroSetting = None
		else:
			if platform.system() == "Windows" and platform.version() >= 6.0:
				self._aeroSetting = settings.registerSetting(**{
					"internal_name": "org.openteacher.gui.aero",
					"name": "Use Aero glass (experimental)",
					"type": "boolean",
					"category": "User interface",
					"subcategory": "Effects",
					"defaultValue": False,
					"advanced": True,
				})
			else:
				self._aeroSetting = None

		#try to load translations for Qt itself
		qtTranslator = QtCore.QTranslator()
		qtTranslator.load(
			"qt_" + QtCore.QLocale.system().name(),
			QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
		)
		self._app.installTranslator(qtTranslator);

		self._widget = self._ui.OpenTeacherWidget(
			self._modules.default("active", type="startWidget").createStartWidget(),
			self._onCloseRequested,
			self._aeroSetting and self._aeroSetting["value"],
		)

		try:
			br = self._modules.default("active", type="buttonRegister")
		except IndexError:
			pass
		else:
			#add the open action as a load button too.
			self._loadButton = br.registerButton("load")
			self._loadButton.clicked.handle(lambda: self._widget.openAction.triggered.emit(False))
			#always the load button first.
			self._loadButton.changePriority.send(0)
			self._loadButton.changeSize.send("small")

		metadata = self._modules.default("active", type="metadata").metadata
		self._widget.setWindowTitle(metadata["name"])
		self._widget.setWindowIcon(QtGui.QIcon(metadata["iconPath"]))

		self._fileTabs = {}

		#Make menus accessable
		#file
		self.fileMenu = Menu(createEvent, self._widget.fileMenu)
		self.newAction = Action(createEvent, self._widget.fileMenu, self._widget.newAction)
		self.openAction = Action(createEvent, self._widget.fileMenu, self._widget.openAction)
		self.openIntoAction = Action(createEvent, self._widget.fileMenu, self._widget.openIntoAction)
		self.saveAction = Action(createEvent, self._widget.fileMenu, self._widget.saveAction)
		self.saveAsAction = Action(createEvent, self._widget.fileMenu, self._widget.saveAsAction)
		self.printAction = Action(createEvent, self._widget.fileMenu, self._widget.printAction)
		self.quitAction = Action(createEvent, self._widget.fileMenu, self._widget.quitAction)

		#edit
		self.editMenu = Menu(createEvent, self._widget.editMenu)
		self.reverseAction = Action(createEvent, self._widget.editMenu, self._widget.reverseAction)
		self.settingsAction = Action(createEvent, self._widget.editMenu, self._widget.settingsAction)

		#view
		self.viewMenu = Menu(createEvent, self._widget.viewMenu)
		self.fullscreenAction = Action(createEvent, self._widget.viewMenu, self._widget.fullscreenAction)

		#help
		self.helpMenu = Menu(createEvent, self._widget.helpMenu)
		self.documentationAction = Action(createEvent, self._widget.helpMenu, self._widget.docsAction)
		self.aboutAction = Action(createEvent, self._widget.helpMenu, self._widget.aboutAction)

		self._widget.tabWidget.currentChanged.connect(self._onTabChanged)
		self._widget.activityChanged.connect(
			lambda activity: self.applicationActivityChanged.send(
				"active" if activity else "inactive"
			)
		)

		#make the statusViewer available
		self.statusViewer = StatusViewer(self._widget.statusBar())

		#set application name (handy for e.g. Phonon)
		self._app.setApplicationName(metadata["name"])
		self._app.setApplicationVersion(metadata["version"])

		#load translator
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self._addingTab = False

		self.active = True

	def _onTabChanged(self):
		#when adding a tab, this triggers a bit too early. Because of
		#that, it's called manually by the functions that add a tab.
		if not self._addingTab:
			self.tabChanged.send()

	def disable(self):
		self.active = False

		try:
			br = self._modules.default("active", type="buttonRegister")
		except IndexError:
			pass
		else:
			#we don't unhandle the event, since PyQt4 does some weird
			#memory stuff making it impossible to find the right item,
			#and it's unneeded anyway.
			br.unregisterButton(self._loadButton)
			del self._loadButton

		del self._modules
		del self._ui
		del self._fileTabs
		del self._widget
		del self._aeroSetting
		del self._app

		del self.tabChanged
		del self.applicationActivityChanged

		del self.fileMenu
		del self.newAction
		del self.openAction
		del self.openIntoAction
		del self.saveAction
		del self.saveAsAction
		del self.printAction
		del self.quitAction

		del self.editMenu
		del self.reverseAction
		del self.settingsAction

		del self.viewMenu
		del self.fullscreenAction

		del self.helpMenu
		del self.documentationAction
		del self.aboutAction

		del self.statusViewer

		del self._addingTab

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

		self._ui._, self._ui.ngettext = _, ngettext
		self._widget.retranslate()
		
		for fileTab in self._fileTabs.values():
			if fileTab.__class__ == LessonFileTab:
				fileTab.retranslate()

		self._loadButton.changeText.send(_("Open from file"))

	def run(self, onCloseRequested):
		"""Starts the event loop of the Qt application. 
		   Can only be called once.

		"""
		self._closeCallback = onCloseRequested

		self._widget.show()
		self._app.exec_()

	def _onCloseRequested(self):
		#if not running, there's nothing that can be closed, so don't
		#check if the method exists. (The callback is assigned in
		#run().)
		return self._closeCallback()

	def interrupt(self):
		"""Closes all windows currently opened. (Including windows from
		   other modules.)

		"""
		self._app.closeAllWindows()

	def setFullscreen(self, bool):
		"""Enables or disables full screen depending on the ``bool``
		   argument.
   
		"""
		#native menubar enable/disable to keep it into view while
		#fullscreen in at least unity.
		if bool:
			self._widget.menuBar().setNativeMenuBar(False)
			self._widget.showFullScreen()
		else:
			if platform.linux_distribution()[0] != "Ubuntu":
				#on Unity, we don't re-enable the native menu bar,
				#because a re-enabled native menu bar doesn't work ok.
				self._widget.menuBar().setNativeMenuBar(True)
			self._widget.showNormal()

	@property
	def startTab(self):
		"""Gives access to the start tab widget."""

		return self._widget.tabWidget.startWidget

	def showStartTab(self):
		"""Changes the current tab to be the same as the one shown on
		   application start.

		"""
		self._widget.tabWidget.setCurrentWidget(self._widget.tabWidget.startWidget.wrapperWidget)

	def addFileTab(self, enterWidget=None, teachWidget=None, resultsWidget=None, previousTabOnClose=False):
		"""The same as ``addCustomTab``, except that it takes three
		   widgets (one for enteringItems, on for teaching them and one
		   for showing the teaching results) that are combined into a
		   single tab.

		"""
		widget = self._ui.LessonTabWidget(enterWidget, teachWidget, resultsWidget)

		return self.addCustomTab(widget, previousTabOnClose)

	def addCustomTab(self, widget, previousTabOnClose=False):
		"""Adds ``widget`` as a tab in the main window. If
		   ``previousTabOnClose`` is true, the currently visible tab is
		   shown again when the created tab is closed.
   
		"""

		if previousTabOnClose:
			lastWidget = self._widget.tabWidget.currentWidget()
		else:
			lastWidget = None

		self._addingTab = True
		self._widget.tabWidget.addTab(widget, "")
		self._addingTab = False

		args = (self._mm, self._widget.tabWidget, widget, lastWidget)

		if widget.__class__ == self._ui.LessonTabWidget:
			fileTab = LessonFileTab(*args)
		else:
			fileTab = FileTab(*args)
		self._fileTabs[widget.wrapperWidget] = fileTab

		self._onTabChanged()
		return fileTab

	@property
	def currentFileTab(self):
		"""Gives access to the currently shown file tab (if any,
		   otherwise this returns ``None``.)

		"""
		try:
			return self._fileTabs[self._widget.tabWidget.currentWidget()]
		except KeyError:
			return

	@currentFileTab.setter
	def currentFileTab(self, value):
		#reverse dictionary lookup.
		for widget, fileTab in self._fileTabs.iteritems():
			if fileTab == value:
				self._widget.tabWidget.setCurrentWidget(widget)

	def addStyleSheetRules(self, rules):
		"""Adds global Qt style sheet rules to the current QApplication.
		   An example use is to theme OpenTeacher.

		"""
		self._app.setStyleSheet(self._app.styleSheet() + "\n\n" + rules)

	def setStyle(self, style):
		"""Allows you to set an app-wide QStyle. Handy for theming."""

		self._app.setStyle(style)

	@property
	def qtParent(self):
		"""Only use this as widget parent, or for application
		global Qt settings, and don't be surprised if another
		module sets that setting differently.

		"""
		return self._widget

	@property
	def startTabActive(self):
		"""Tells you if the start tab is active at the moment this
		   property is accessed.

		"""
		return self._widget.tabWidget.startWidget.wrapperWidget == self._widget.tabWidget.currentWidget()

def init(moduleManager):
	return GuiModule(moduleManager)
