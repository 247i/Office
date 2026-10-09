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

class VocabulariumLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(VocabulariumLoaderModule, self).__init__(*args, **kwargs)

		self.type = "load"
		self.priorities = {
			"default": 430,
		}
		self._mm = moduleManager
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
		)
		self.filesWithTranslations = ("vocabularium.py",)

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
		#TRANSLATORS: it. See http://www.stilus.nl/vocabularium/ (Dutch)
		#TRANSLATORS: for more info on the program.
		self.name = _("Vocabularium")

	def enable(self):
		self.loads = {
			"voc": ["words"],
		}
		self.mimetype = "application/x-vocabularium"

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

	def _lines(self, f):
		return unicode(f.read(), encoding="UTF-16").split("\n")

	def getFileTypeOf(self, path):
		if path.endswith(".voc"):
			with open(path, "r") as f:
				if "vocabularium" in self._lines(f)[0].lower():
					return "words"

	def load(self, path):
		"""Tries to load .voc Vocabularium files. Based on the
		   information presented in this .doc document and observation
		   of files: http://www.stilus.nl/vocabularium/handl-2.doc

		"""
		list = {"items": []}
		with open(path, "r") as f:
			for i, line in enumerate(self._lines(f)):
				if i == 0:
					#header
					pass
				elif i == 1:
					#q & a language
					langs = [lang.strip() for lang in line.split(" ", 1)]
					list["questionLanguage"], list["answerLanguage"] = langs
				elif line.startswith("!"):
					if "title" not in list:
						#the first comment is used as title. In most
						#files, there is only one and it ís the title.
						#
						#without exclamation mark
						list["title"] = line[1:].strip()
				else:
					try:
						questions, answers = line.split("\t")
					except ValueError:
						#be lenient
						pass
					else:
						list["items"].append({
							"id": i,
							"questions": self._parse(questions),
							"answers": self._parse(answers),
						})

		return {
			"list": list,
			"resources": {},
		}

def init(moduleManager):
	return VocabulariumLoaderModule(moduleManager)
