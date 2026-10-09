#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Milan Boers
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

class CueCardLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(CueCardLoaderModule, self).__init__(*args, **kwargs)

		self.type = "load"
		self.priorities = {
			"default": 432,
		}
		self._mm = moduleManager
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
		)
		self.filesWithTranslations = ("cuecard.py",)

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
		#TRANSLATORS: This is one of the file formats OpenTeacher
		#TRANSLATORS: can read. It's named after the program that uses
		#TRANSLATORS: it. See http://www.wadeb.com/cuecard/
		#TRANSLATORS: for more info on the program.
		self.name = _("CueCard")

	def enable(self):
		self.loads = {
			"wcu": ["words"],
		}
		self.mimetype = "application/x-cuecard"

		self._modules = set(self._mm.mods(type="modules")).pop()
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

		del self.name
		del self.loads
		del self.mimetype

		del self._modules

	def getFileTypeOf(self, path):
		if path.endswith(".wcu"):
			return "words"

	def load(self, path):
		"""Tries to load .wcu CueCard files. Based on observation of the
		   file format, not on documentation. Seems like there is source
		   code available though.

		"""
		with open(path, "r") as f:
			root = ElementTree.parse(f).getroot()

		items = []
		for id, card in enumerate(root.findall("Card")):
			items.append({
				"id": id,
				"questions": self._parse(card.get("Question")),
				"answers": self._parse(card.get("Answer")),
			})

		return {
			"list": {
				"items": items,
			},
			"resources": {},
		}

def init(moduleManager):
	return CueCardLoaderModule(moduleManager)
