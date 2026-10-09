#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2013, Marten de Vries
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

import csv

class CsvLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(CsvLoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "load"
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("csv_.py",)

	@property
	def _parse(self):
		return self._modules.default("active", type="wordsStringParser").parse

	def getFileTypeOf(self, path):
		if path.endswith(".csv") or path.endswith(".tsv"):
			return "words"

	def load(self, path):
		with open(path, "rU") as f:
			data = f.read()
		encoding = chardet.detect(data)["encoding"]
		utf8Data = unicode(data, encoding=encoding, errors="ignore").encode("UTF-8")

		sniffer = csv.Sniffer()
		dialect = sniffer.sniff(utf8Data)
		reader = csv.reader(utf8Data.split("\n"), dialect)

		items = []
		for i, line in enumerate(reader):
			if not line:
				continue
			try:
				questions = self._parse(unicode(line[0], encoding="UTF-8"))
				answers = self._parse(unicode(line[1], encoding="UTF-8"))
			except IndexError:
				continue

			items.append({
				"id": i,
				"questions": questions,
				"answers": answers,
			})

		return {
			"resources": {},
			"list": {
				"items": items,
				"tests": [],
			},
		}

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is one of the file formats OpenTeacher can
		#TRANSLATORS: read.
		self.name = _("Spreadsheet")

	def enable(self):
		global chardet
		try:
			import chardet
		except ImportError:
			#fallback. Strongly recommended to use the real one,
			#though ;)
			class MyChardet(object):
				def detect(self, *args, **kwargs):
					return {"encoding": "UTF-8"}
			chardet = MyChardet()

		self.loads = {
			"csv": ["words"],
			"tsv": ["words"],
		}
		#no mimetype. Registering text/csv is too harsh.

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

def init(moduleManager):
	return CsvLoaderModule(moduleManager)
