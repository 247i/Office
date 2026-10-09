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
import itertools

class AbbyyLoaderModule(object):
	"""Loads ABBYY Lingvo Tutor files (.xml)"""

	def __init__(self, moduleManager, *args, **kwargs):
		super(AbbyyLoaderModule, self).__init__(*args, **kwargs)
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
		self.filesWithTranslations = ("abbyy.py",)

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
		self.name = _("ABBYY Lingvo Tutor")

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		#No mimetype. Claiming .xml is too harsh.
		self.loads = {"xml": ["words"]}

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.loads

	def getFileTypeOf(self, path):
		if path.endswith(".xml"):
			return "words"

	def load(self, path):
		wsp = self._modules.default("active", type="wordsStringParser")

		root = ElementTree.parse(open(path)).getroot()

		wordList = {
			"items": list(),
			"title": root.get("title", u""),
		}

		#a counter is used to suppply the ids. That's because ABBYY
		#Lingvo Tutor decided to not include ids anymore from version X5
		#on.
		counter = itertools.count()

		wordList["items"] = [
			{
				"id": next(counter),
				"questions": wsp.parse(wordTree.findtext("word") or u""),
				"answers": [[a.text or u"" for a in wordTree.findall("meanings/meaning/translations/word")]],
				"commentAfterAnswering": u", ".join(
					e.text or u""
					for e in wordTree.findall("meanings/meaning/examples/example")
				)
			}
			for wordTree in root.findall("card")
		]

		return {
			"resources": {},
			"list": wordList,
		}

def init(moduleManager):
	return AbbyyLoaderModule(moduleManager)
