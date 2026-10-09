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

import itertools

class DomingoLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(DomingoLoaderModule, self).__init__(*args, **kwargs)

		self.type = "load"
		self.priorities = {
			#less impotant than vocabularium, which shares the same
			#extension!
			"default": 432,
		}
		self._mm = moduleManager
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
		)
		self.filesWithTranslations = ("domingo.py",)

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
		#TRANSLATORS: it. See http://www.domingo-online.de/ (German)
		#TRANSLATORS: for more info on the program.
		self.name = _("Domingo")

	def enable(self):
		self.loads = {
			"voc": ["words"],
		}
		self.mimetype = "application/x-domingo"

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
		if path.endswith(".voc"):
			#probably. Not the only one using this extension. Fixed by
			#the priorities in OT...
			return "words"

	def load(self, path):
		"""Tries to load .voc Domingo files. Based on observation of the
		   file format, not on documentation.

		"""
		#read file
		lines = []
		with open(path, "r") as f:
			for line in f:
				line = unicode(line, encoding="UTF-8").strip()
				if not line:
					break
				lines.append(line)

		items = []

		#iterate over two items at a time
		iterator = iter(lines)
		counter = itertools.count()
		for question, answer in itertools.izip(iterator, iterator):
			items.append({
				"id": next(counter),
				"questions": self._parse(question),
				"answers": self._parse(answer),
			})

		return {
			"list": {
				"items": items,
				"results": [],
			},
			"resources": {},
		}

def init(moduleManager):
	return DomingoLoaderModule(moduleManager)
