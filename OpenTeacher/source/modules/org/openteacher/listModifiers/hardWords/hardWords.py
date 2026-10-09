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

class HardWordsModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(HardWordsModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "listModifier"
		self.testName = "hardWords"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("hardWords.py",)
		self.priorities = {
			"default": 823,
		}

	def modifyList(self, indexes, list):
		self._list = list
		newIndexes = filter(self._isHardWord, indexes)
		del self._list
		return newIndexes

	def _isHardWord(self, index):
		results = self._resultsFor(self._list["items"][index])

		if len(results) == 0:
			return True

		wrongResults = filter(lambda x: x["result"] == "wrong", results)
		amountWrong = len(wrongResults)
		return amountWrong > len(results) / 2.0

	def _resultsFor(self, word):
		results = []
		try:
			for test in self._list["tests"]:
				results.extend(test)
		except KeyError:
			pass
		return filter(lambda result: result["itemId"] == word["id"], results)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()
		self.dataType = "words"
		self.active = True

	def _retranslate(self):
		#Translations
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: %% will automatically be converted to a single
		#%-sign
		self.name = _("Only hard words (<50%% right)") % ()

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.dataType

def init(moduleManager):
	return HardWordsModule(moduleManager)
