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

import sqlite3

class MnemosyneLoaderModule(object):
	"""A pretty basic mnemosyne importer. For now it imports everything
	   like it is a words file, which might not always be the best way of
	   dealing with mnemosyne files. Also, it does nothing with the
	   results in the database. But, in the end, it might work fine for
	   people who want to switch. :)

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(MnemosyneLoaderModule, self).__init__(*args, **kwargs)

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
		self.filesWithTranslations = ("mnemosyne.py",)

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
		#TRANSLATORS: it. See http://mnemosyne-proj.org/ for more info
		#TRANSLATORS: on it.
		self.name = _("Mnemosyne")

	def enable(self):
		self.loads = {"db": ["words"]}
		#no mimetype, .db is too generic to claim.

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

		del self._modules

	def getFileTypeOf(self, path):
		if path.endswith(".db"):
			return "words"

	def load(self, path):
		"""Based on reading out the db scheme of a file. The source code
		   of mnemosyne is also available, but it wasn't used for
		   writing this code.

		"""
		items = []
		with sqlite3.connect(path) as connection:
			cursor = connection.cursor()
			cursor.execute("SELECT question, answer FROM cards ORDER BY creation_time")
			for i, (question, answer) in enumerate(cursor.fetchall()):
				items.append({
					"id": i,
					"questions": self._parse(question),
					"answers": self._parse(answer)
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
	return MnemosyneLoaderModule(moduleManager)
