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

class VTrainTxtLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(VTrainTxtLoaderModule, self).__init__(*args, **kwargs)

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
		self.filesWithTranslations = ("vtrainTxt.py",)
		#for test suite purposes
		self.format = "vtrain"

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
		#TRANSLATORS: it. See http://www.vtrain.net/ for more info on
		#TRANSLATORS: the program.
		self.name = _("VTrain")

	def enable(self):
		self.loads = {
			"txt": ["words"],
		}
		#no mime type: claiming .txt doesn't make sense.

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
		if path.endswith(".txt"):
			with open(path, "r") as f:
				data = f.read()
				#A heuristic. Adapt as necessary.
				amountOfLineEnds = data.count("|")
				amountOfSeparators = data.count("=")
				if amountOfLineEnds and amountOfLineEnds == amountOfSeparators:
					return "words"

	def load(self, path):
		"""Tries to load .txt VTrain files. Based on observation of the
		    file format, and the following description send by mail by
		    the author of VTrain:

			'VTrain uses customizable separators after the front and
			after the back of each flashcard. By default, the
			separators are "=" and "|". You can use these separators to
			import and export flashcards (File menu).

			the horse=el caballo|
			the house=la casa|
			...'

		"""
		items = []

		#read file
		with open(path, "r") as f:
			data = unicode(f.read(), encoding="ISO-8859-1")
			for i, line in enumerate(data.split(u"|")):
				try:
					questions, answers = line.split(u"=")
				except ValueError:
					#shouldn't happen, but just in case someone e.g.
					#accidentally adds a newline at the end of the file.
					continue
				items.append({
					"id": i,
					"questions": self._parse(questions),
					"answers": self._parse(answers),
				})

		return {
			"list": {
				"items": items,
				"results": [],
			},
			"resources": {},
		}

def init(moduleManager):
	return VTrainTxtLoaderModule(moduleManager)
