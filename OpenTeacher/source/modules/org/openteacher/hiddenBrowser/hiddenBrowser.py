#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#	Copyright 2011-2012, Cas Widdershoven
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

import contextlib

def installQtClasses():
	global WebBrowserWidget

	class WebBrowserWidget(QtGui.QWidget):
		def __init__(self, resourcePath, startPage, *args, **kwargs):
			super(WebBrowserWidget, self).__init__(*args, **kwargs)

			self._startPage = startPage

			vbox = QtGui.QVBoxLayout()
			
			hidelo = QtGui.QHBoxLayout()
			self.hideSelfButton = QtGui.QPushButton()
			self.hideOthersButton = QtGui.QPushButton()
			hidelo.addWidget(self.hideSelfButton)
			hidelo.addWidget(self.hideOthersButton)
			
			urllo = QtGui.QHBoxLayout()
			
			previousButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(
				"back",
				QtGui.QIcon(resourcePath("icons/back.png"))
			), "")
			nextButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(
				"forward",
				QtGui.QIcon(resourcePath("icons/forward.png"))
			), "")
			reloadButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(
				"reload",
				QtGui.QIcon(resourcePath("icons/reload.png"))
			), "")
			self.urlbar = QtGui.QLineEdit()
			
			urllo.addWidget(previousButton)
			urllo.addWidget(nextButton)
			urllo.addWidget(reloadButton)
			urllo.addWidget(self.urlbar)
			
			self.webview = QtWebKit.QWebView()
			self.webview.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True);
			
			vbox.addLayout(hidelo)
			vbox.addLayout(urllo)
			vbox.addWidget(self.webview)
			
			self.setLayout(vbox)
			
			self.hideSelfButton.clicked.connect(self.hideSelf)
			self.hideOthersButton.clicked.connect(self.hideOthers)
			previousButton.clicked.connect(self.webview.back)
			nextButton.clicked.connect(self.webview.forward)
			reloadButton.clicked.connect(self.webview.reload)
			self.urlbar.returnPressed.connect(self.loadUrl)
			self.webview.urlChanged.connect(
				lambda url: self.urlbar.setText(url.toString())
			)

			self.webview.load(QtCore.QUrl(self._startPage))

			#finally
			self.retranslate()

		def retranslate(self):
			self.hideSelfButton.setText(_("Hide the browser!"))
			self.hideOthersButton.setText(_("Hide the others; make space for the browser"))

		def loadUrl(self, *args):
			with contextlib.ignored(KeyError): self.webview.setHtml(eval("7b2261626f75743a6d6f7a696c6c61223a20223c626f6479207374796c653d276261636b67726f756e642d636f6c6f723a6d61726f6f6e3b636f6c6f723a77686974653b666f6e742d66616d696c793a73657269663b666f6e742d7374796c653a6974616c69633b273e3c68313e4966206f6e6c7920517420776f756c64206a75737420737570706f7274204765636b6f2e2e2e3c2f68313e3c2f626f64793e222c2261626f75743a6368726f6d65223a20226d65682e222c2261626f75743a6f70657261223a20224f706572613f2057686174277320746861743f20536f6d657468696e6720656469626c65204920686f70653f222c2261626f75743a756e697665727365223a20223432222c2261626f75743a6965223a20223c626f6479207374796c653d276261636b67726f756e642d636f6c6f723a6c696d653b636f6c6f723a70696e6b3b666f6e742d66616d696c793a637572736976653b273e3c68313e25733c2f68313e3c2f626f64793e222025202822426c656768212022202a20313030292c2261626f75743a6f70656e74656163686572223a20223c7363726970743e73657454696d656f75742866756e6374696f6e202829207b77696e646f772e6c6f636174696f6e3d272573273b7d2c2033303030293c2f7363726970743e3c68313e596179213c2f68313e2220252073656c662e5f7374617274506167652c7d".decode("hex"))[unicode(self.urlbar.text())]); return

			if not unicode(self.urlbar.text()).startswith(u"http://"):
				#add http:// if it's not there yet
				self.url = QtCore.QUrl(u"http://" + self.urlbar.text(), QtCore.QUrl.TolerantMode)
			else:
				#otherwise just parse the url directly
				self.url = QtCore.QUrl(self.urlbar.text(), QtCore.QUrl.TolerantMode)
			#and load it
			self.webview.load(self.url)

		def hideSelf(self):
			#FIXME (3.1): Make sure this works via a nice module interface,
			#because this breaks as soon as a very small change is made. (It
			#already did once...)

			#show other side widgets
			sizes = self.parentWidget().sizes()
			sizes[self.parentWidget().indexOf(self)] = 0
			if not sum(sizes):
				for i in range(len(sizes)):
					sizes[i] = 1
				sizes[self.parentWidget().indexOf(self)] = 0
			self.parentWidget().setSizes(sizes)

			#show other widgets
			sizes = self.parentWidget().parentWidget().sizes()
			for i in range(len(sizes)):
				sizes[i] = 1
			self.parentWidget().parentWidget().setSizes(sizes)

		def hideOthers(self):
			#FIXME 3.1: see hideSelf.

			#hide other side widgets
			sizes = self.parentWidget().sizes()
			size = sizes[self.parentWidget().indexOf(self)]
			for i in range(len(sizes)):
				sizes[i] = 0
			sizes[self.parentWidget().indexOf(self)] = size
			self.parentWidget().setSizes(sizes)

			#hide other widgets
			sizes = self.parentWidget().parentWidget().sizes()
			size = sizes[self.parentWidget().parentWidget().indexOf(self.parentWidget())]
			for i in range(len(sizes)):
				sizes[i] = 0
			sizes[self.parentWidget().parentWidget().indexOf(self.parentWidget())] = size
			self.parentWidget().parentWidget().setSizes(sizes)
	return WebBrowserWidget

class HiddenBrowserModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(HiddenBrowserModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager
		
		self.type = "webbrowser"
		
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="metadata"),
		)
		self.uses = (
			self._mm.mods(type="settings"),
			self._mm.mods(type="lesson"),
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("hiddenBrowser.py",)
		x = 940
		self.priorities = {
			"all": x,
			"student@home": x,
			"code-documentation": x,
			"test-suite": x,
			"default": -1,
		}

	def _lessonAdded(self, lesson):
		self._lessons.add(lesson)
		self._addSideWidgetToLessonIfNecessary(lesson)

	def _addSideWidgetToLessonIfNecessary(self, lesson):
		if self._enabled["value"]:
			with contextlib.ignored(AttributeError):
				#AttributeError: in case the lesson doesn't support sideWidgets
				lesson.addTeachSideWidget(self.browser)

	def _removeSideWidgetFromLessonIfNecessary(self, lesson):
		if not self._enabled["value"]:
			with contextlib.ignored(AttributeError):
				#AttributeError: in case the lesson doesn't support sideWidgets
				lesson.removeTeachSideWidget(self.browser)

	def enable(self):
		global QtCore, QtGui, QtWebKit
		try:
			from PyQt4 import QtCore, QtGui, QtWebKit
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()

		with contextlib.ignored(IndexError):
			#Keeps track of all created lessons
			for module in self._mm.mods("active", type="lesson"):
				module.lessonCreated.handle(self._lessonAdded)

		try:
			self._enabled = self._modules.default(type="settings").registerSetting(**{
				"internal_name": "org.openteacher.hiddenBrowser.enabled",
				"type": "boolean",
				"defaultValue": False,
				"callback": {
					"args": ("active",),
					"kwargs": {
						"type": "webbrowser"
					},
					"method": "updateActive"
				},
			})
		except IndexError:
			self._enabled = {
				"value": False,
			}
		metadata = self._modules.default("active", type="metadata").metadata
		
		#Register for retranslating
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		#translate everything for the first time
		self._retranslate()

		#FIXME 3.1: This object is now built even if the webview is
		#never shown. Since building it is quite heavy (e.g. a Java
		#VM starts if installed), that should be delayed.
		self.browser = WebBrowserWidget(self._mm.resourcePath, metadata["website"])
		
		self._lessons = set()
		
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
			
		self._enabled.update({
			"name": _("Enable hidden browser (hide it by moving the slider)"),
		})
		with contextlib.ignored(AttributeError):
			#AttributeError: first time it's not there
			self.browser.retranslate()
	
	def updateActive(self, *args, **kwargs):
		#Add the web browser to every lesson
		for lesson in self._lessons:
			self._addSideWidgetToLessonIfNecessary(lesson)
			self._removeSideWidgetFromLessonIfNecessary(lesson)
	
	def disable(self):
		self.active = False
		
		del self._modules
		del self._enabled
		del self._lessons
		del self.browser

def init(moduleManager):
	return HiddenBrowserModule(moduleManager)
