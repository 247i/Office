#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Marten de Vries
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

class PrintModule(object):
	def __init__(self, moduleManager):
		self._mm = moduleManager

		self.type = "print"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="metadata"),
			self._mm.mods(type="wordsHtmlGenerator"),
		)
		self.filesWithTranslations = ("words.py",)
	
	def enable(self):
		global QtWebKit
		try:
			from PyQt4 import QtWebKit
		except ImportError:
			return
		self._modules = set(self._mm.mods(type="modules")).pop()

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.prints = ["words"]

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

	def disable(self):
		self.active = False

		del self._modules
		del self.prints

	def print_(self, type, lesson, printer):
		html = self._modules.default(
			"active",
			type="wordsHtmlGenerator"
		).generate(lesson)

		name = self._modules.default("active", type="metadata").metadata["name"]
		printer.setCreator(name)
		try:
			printer.setDocName(lesson.list["title"])
		except KeyError:
			printer.setDocName(_("Untitled word list"))

		self._printer = printer
		self._doc = QtWebKit.QWebView()
		self._doc.loadFinished.connect(self._loadFinished)
		self._doc.setHtml(html)

	def _loadFinished(self, ok):
		self._doc.print_(self._printer)

def init(moduleManager):
	return PrintModule(moduleManager)
