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

from etree import ElementTree

class TeachmasterLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TeachmasterLoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "load"
		self.priorities = {
			"default": 756,
		}
		
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("teachmaster.py",)

	@property
	def _parse(self):
		return self._modules.default("active", type="wordsStringParser").parse

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is the name of a file type OpenTeacher can
		#TRANSLATORS: read. It's named after the program with the same
		#TRANSLATORS: name. For more info on the program, see:
		#TRANSLATORS: http://www.teachmaster.de/cms/1-1-Home.html
		self.name = _("Teachmaster")

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.mimetype = "application/x-teachmaster"
		self.loads = {"vok2": ["words"]}

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.loads
		del self.mimetype

	def getFileTypeOf(self, path):
		if path.endswith(".vok2"):
			return "words"

	def load(self, path):
		"""Loads Teachmaster's .vok2 files. Lesson info is stored in
		   additional files, but that's not loaded. It might not map to
		   the OT result system either (not sure). For documentation on
		   the file format in German (translations are available, but
		   those aren't all complete/up-to-date):

		   http://www.teachmaster.de/wikka/DocumentationDEDateiformate

		"""
		with open(path, "r") as f:
			root = ElementTree.parse(f).getroot()

		list = {
			"items": [],
			"title": root.findtext("header/titel") or u"",
			"questionLanguage": root.findtext("header/spreins") or u"",
			"answerLanguage": root.findtext("header/sprzwei"),
		}

		for i, itemTree in enumerate(root.findall("vokabelsatz")):
			word = {
				"id": i,
				"questions": self._parse(itemTree.findtext("spreins") or u""),
				"answers": [],
				"comment": itemTree.findtext("bemerkung") or u"",
			}

			answer = itemTree.findtext("sprzwei")
			synonym = itemTree.findtext("synonym")
			if answer:
				word["answers"].append((answer,))
			if synonym:
				word["answers"].append((synonym,))

			list["items"].append(word)

		return {
			"resources": {},
			"list": list,
		}

def init(moduleManager):
	return TeachmasterLoaderModule(moduleManager)
