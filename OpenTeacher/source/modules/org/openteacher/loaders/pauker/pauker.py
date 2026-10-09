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
import gzip
import contextlib

class PaukerLoaderModule(object):
	"""Loads .pau.gz and .xml.gz files (the format of Pauker)"""

	def __init__(self, moduleManager, *args, **kwargs):
		super(PaukerLoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "load"
		x = 761
		self.priorities = {
			"default": x,
		}
		
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("pauker.py",)

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
		#TRANSLATORS: More info: http://pauker.sourceforge.net/
		self.name = _("Pauker")

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.mimetype = "application/x-pauker"
		self.loads = {
			"pau": ["words"],
			"pau.gz": ["words"],
			"xml.gz": ["words"],
		}

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.mimetype
		del self.loads

	def getFileTypeOf(self, path):
		for ext in self.loads.keys():
			if path.endswith(ext):
				return "words"

	@property
	def _parse(self):
		return self._modules.default("active", type="wordsStringParser").parse

	def load(self, path):
		if path.endswith(".pau"):
			with open(path) as f:
				root = ElementTree.parse(f).getroot()
		else:
			with contextlib.closing(gzip.open(path)) as f:
				root = ElementTree.parse(f).getroot()

		wordList = {
			#only the first line, because a description can be pretty
			#long in Pauker...
			"title": (root.findtext("Description") or u"").split("\n")[0].strip(),
			"items": [],
		}
		cards = root.findall("Batch//Card")
		if cards is not None:
			for id, card in enumerate(cards):
				questions = self._parse(
					(card.findtext("FrontSide") or u"").strip() or
					(card.findtext("FrontSide/Text") or u"").strip() or
					u""
				)
				answers = self._parse(
					(card.findtext("BackSide") or u"").strip() or
					(card.findtext("BackSide/Text") or u"").strip() or
					(card.findtext("ReverseSide") or u"").strip() or
					(card.findtext("ReverseSide/Text") or u"").strip() or
					u""
				)

				wordList["items"].append({
					"id": id,
					"questions": questions,
					"answers": answers
				})

		return {
			"resources": {},
			"list": wordList,
		}

def init(moduleManager):
	return PaukerLoaderModule(moduleManager)
