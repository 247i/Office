#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Marten de Vries
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

class KvtmlLoaderModule(object):
	"""Loads .kvtml files (the format of various KDE programs)"""

	def __init__(self, moduleManager, *args, **kwargs):
		super(KvtmlLoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "load"
		self.priorities = {
			"default": 770,
		}
		
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("kvtml.py",)

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is the name of a file format OT can read.
		self.name = _("KDE Vocabulary Document")

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.loads = {"kvtml": ["words"]}
		self.mimetype = "application/x-kvtml"

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.loads
		del self.mimetype

	def getFileTypeOf(self, path):
		if path.endswith(".kvtml"):
			return "words"

	@property
	def _parse(self):
		return self._modules.default("active", type="wordsStringParser").parse

	def load(self, path):
		root = ElementTree.parse(open(path)).getroot()
		if root.get("version", "").startswith("2"):
			return self._load2x(root)
		return self._load1x(root)

	def _load2x(self, root):
		list = {
			"items": [],
			"title": root.findtext("information/title") or u"",
			"questionLanguage": root.findtext("identifiers/identifier[@id='0']/name") or u"",
			"answerLanguage": root.findtext("identifiers/identifier[@id='1']/name") or u"",
		}
		for entry in root.findall("entries/entry"):
			word = {
				"id": entry.get("id"),
				"questions": self._parse(entry.findtext("translation[@id='0']/text") or u""),
				"answers": self._parse(entry.findtext("translation[@id='1']/text") or u""),
			}
			if word["questions"] or word["answers"]:
				list["items"].append(word)
		return {"resources": {}, "list": list}

	def _load1x(self, root):
		wordList = {
			"items": [],
			"title": root.get("title", u""),
		}

		for i, wordTree in enumerate(root.findall("e")):
			word = {
				"id": i,
				"questions": self._parse(wordTree.findtext("o")),
				"answers": self._parse(wordTree.findtext("t")),
			}
			wordList["items"].append(word)

		return {
			"resources": {},
			"list": wordList,
		}

def init(moduleManager):
	return KvtmlLoaderModule(moduleManager)
