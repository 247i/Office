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

import csv

class CsvSaverModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(CsvSaverModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "save"
		x = 925
		self.priorities = {
			"default": x,
		}
		self.requires = (
			self._mm.mods(type="wordsStringComposer"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("csv_.py",)

	def _retranslate(self):
		global _, ngettext
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is one of the file types OpenTeacher can
		#TRANSLATORS: export to.
		self.name = _("Spreadsheet")

	def enable(self):
		self.saves = {"words": ["csv"]}

		#Translations
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

		del self._modules
		del self.name
		del self.saves

	@property
	def _compose(self):
		return self._modules.default(
			"active",
			type="wordsStringComposer"
		).compose

	def save(self, type, lesson, path):
		with open(path, "w") as f:
			writer = csv.writer(f)

			ql = lesson.list.get("questionLanguage", u"").encode("UTF-8")
			al = lesson.list.get("answerLanguage", u"").encode("UTF-8")
			#write header
			questionsHeader = ql or _("Questions").encode("UTF-8")
			answersHeader = al or _("Answers").encode("UTF-8")
			writer.writerow([questionsHeader, answersHeader])
			#write items
			for item in lesson.list.get("items", []):
				questions = self._compose(item.get("questions", [])).encode("UTF-8")
				answers = self._compose(item.get("answers", [])).encode("UTF-8")
				writer.writerow([questions, answers])

		lesson.path = None

def init(moduleManager):
	return CsvSaverModule(moduleManager)
