#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Milan Boers
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

import sqlite3
import re

class AnkiLoaderModule(object):
	"""A pretty basic anki importer. For now it imports everything like
	   it is a words file, which might not always be the best way of
	   dealing with anki files. Also, it does nothing with the results
	   in the database. But, in the end, it might work fine for people
	   who want to switch. :)

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(AnkiLoaderModule, self).__init__(*args, **kwargs)

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
		self.filesWithTranslations = ("anki.py",)

	@property
	def _parse(self):
		return self._modules.default("active", type="wordsStringParser").parse

	def _stripTags(self, html):
		"""Thanks mmmdreg! See: http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python"""

		return re.sub("<[^<]+?>", "", html)

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
		#TRANSLATORS: it. See http://ankisrs.net/ for more info on it.
		self.name = _("Anki")

	def enable(self):
		self.loads = {"anki": ["words"]}
		self.mimetype = "application/x-anki"

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
		if path.endswith(".anki"):
			return "words"

	def load(self, path):
		items = []
		with sqlite3.connect(path) as connection:
			cursor = connection.cursor()
			#DB scheme (also generatable from a file I guess...):
			#https://ankisrs.googlegroups.com/attach/244fa793e3ad8b52/anki.png?view=1&part=4
			cursor.execute("SELECT question, answer FROM cards ORDER BY created")
			for i, (question, answer) in enumerate(cursor.fetchall()):
				items.append({
					"id": i,
					"questions": self._parse(self._stripTags(question)),
					"answers": self._parse(self._stripTags(answer))
				})
			cursor.close()
		return {
			"resources": {},
			"list": {
				"items": items,
				"results": [],
			}
		}

def init(moduleManager):
	return AnkiLoaderModule(moduleManager)
