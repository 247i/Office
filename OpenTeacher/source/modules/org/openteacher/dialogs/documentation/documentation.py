#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

import weakref
import os

def installQtClasses():
	global OpenTeacherWebPage, DocumentationDialog

	class OpenTeacherWebPage(QtWebKit.QWebPage):
		"""A QWebPage that tries to fetch the online page, and if that
		   doesn't succeed, fetches the offline page. It also supports
		   retranslated.

		"""
		def __init__(self, url, userAgent, getFallbackHtml, *args, **kwargs):
			super(OpenTeacherWebPage, self).__init__(*args, **kwargs)

			self.url = url
			self.userAgent = userAgent
			self.getFallbackHtml = getFallbackHtml

		def userAgentForUrl(self, url):
			return self.userAgent

		def updateStatus(self, ok):
			if not ok:
				html = self.getFallbackHtml()
				self.mainFrame().setHtml(html)

		def updateLanguage(self, language):
			request = QtNetwork.QNetworkRequest(QtCore.QUrl(self.url))
			request.setRawHeader("Accept-Language", language)
			self.mainFrame().load(request)

			self.loadFinished.connect(self.updateStatus)

	class DocumentationDialog(QtWebKit.QWebView):
		"""The documentation dialog. It shows the (html) user
		   documentation of OpenTeacher. First it tries to fetch the
		   online resource (it can be newer), otherwise it uses the
		   offline fallback.

		"""
		def __init__(self, url, userAgent, getFallbackHtml, *args, **kwargs):
			super(DocumentationDialog, self).__init__(*args, **kwargs)

			self.page = OpenTeacherWebPage(url, userAgent, getFallbackHtml)
			self.setPage(self.page)

		def retranslate(self):
			self.setWindowTitle(_("Documentation"))
			#self.page is retranslated by the updateLanguage call done on a
			#higher level

		def updateLanguage(self, language):
			self.page.updateLanguage(language)

class DocumentationModule(object):
	"""This module provides the documentation dialog."""

	def __init__(self, moduleManager, *args, **kwargs):
		super(DocumentationModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "documentation"
		self.requires = (
			self._mm.mods(type="metadata"),
			self._mm.mods(type="ui"),
			self._mm.mods(type="userDocumentation"),
			self._mm.mods(type="userDocumentationWrapper"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("documentation.py",)

	def _getFallbackHtml(self):
		userDocumentationModule = self._modules.default("active", type="userDocumentation")
		userDocumentationWrapperModule = self._modules.default("active", type="userDocumentationWrapper")

		baseUrl = "file://" + os.path.abspath(userDocumentationModule.resourcesPath)
		html = userDocumentationModule.getHtml(baseUrl)
		return userDocumentationWrapperModule.wrap(html)

	def show(self):
		uiModule = self._modules.default("active", type="ui")

		dialog = DocumentationDialog(
			self._metadata["documentationUrl"],
			self._metadata["userAgent"],
			self._getFallbackHtml
		)
		tab = uiModule.addCustomTab(dialog)
		dialog.tab = tab
		tab.closeRequested.handle(tab.close)

		self._activeDialogs.add(weakref.ref(dialog))
		self._retranslate()

	def enable(self):
		global QtCore, QtWebKit, QtNetwork
		try:
			from PyQt4 import QtCore, QtWebKit, QtNetwork
		except ImportError:
			return

		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._metadata = self._modules.default("active", type="metadata").metadata
		self._activeDialogs = set()

		#load translator
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
		#load translator
		global _
		global ngettext

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
			language = "en"
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
			language = translator.language

		for ref in self._activeDialogs:
			dialog = ref()
			if dialog is not None:
				dialog.retranslate()
				dialog.updateLanguage(language)
				dialog.tab.title = dialog.windowTitle()

	def disable(self):
		self.active = False

		del self._modules
		del self._metadata
		del self._activeDialogs

def init(moduleManager):
	return DocumentationModule(moduleManager)
