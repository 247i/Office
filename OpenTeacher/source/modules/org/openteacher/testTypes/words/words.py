#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2008-2011, Milan Boers
#	Copyright 2009-2013, Marten de Vries
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

class WordsTestTypeModule(object):
	QUESTION, ANSWER, GIVEN_ANSWER, CORRECT = xrange(4)
	def __init__(self, moduleManager, *args, **kwargs):
		super(WordsTestTypeModule, self).__init__(*args, **kwargs)

		self._mm = moduleManager
		
		self.type = "testType"
		self.dataType = "words"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="wordsStringComposer"),
		)
		self.filesWithTranslations = ("words.py",)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		#install translator for the first time and make sure it's updated
		#when the language is changed.
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
		#(re)install the translator
		global _
		global ngettext

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

	def disable(self):
		self.active = False

		del self._modules
	
	def updateList(self, list, test):
		self._list = list
		self._test = test
	
	@property
	def funFacts(self):
		return [
			(_("Word most done wrong:"), self._mostDoneWrong)
		]
	
	@property
	def _mostDoneWrong(self):
		# Get the id of the item most done wrong
		mostWrong = 0
		mostWrongId = None
		
		for item in self._list["items"]:
			wrong = 0
			for result in self._test["results"]:
				if item["id"] == result["itemId"] and result["result"] == "wrong":
					wrong += 1
			if wrong > mostWrong:
				mostWrong = wrong
				mostWrongId = item["id"]
		
		# Get the question of the item most done wrong
		for item in self._list["items"]:
			if item["id"] == mostWrongId:
				return self._modules.default(
					"active",
					type="wordsStringComposer"
				).compose(item["questions"])
	
	@property
	def properties(self):
		return [
			(_("Title:"), "title"),
			(_("Question language:"), "questionLanguage"),
			(_("Answer language:"), "answerLanguage")
		]
	
	@property
	def header(self):
		return [
			_("Question"),
			_("Answer"),
			_("Given answer"),
			#TRANSLATORS: a label of a table column that tells if the user had the answer correct by showing a checkbox.
			_("Correct")
		]
	
	def _itemForResult(self, result):
		for item in self._list["items"]:
			if result["itemId"] == item["id"]:
				return item

	def data(self, row, column):
		compose = self._modules.default(
			"active",
			type="wordsStringComposer"
		).compose

		result = self._test["results"][row]

		item = self._itemForResult(result)
		if column == self.QUESTION:
			return compose(item.get("questions"), [])
		elif column == self.ANSWER:
			return compose(item.get("answers", []))
		elif column == self.GIVEN_ANSWER:
			try:
				return result["givenAnswer"]
			except KeyError:
				#TRANSLATORS: - means 'none' here. If there's a better
				#symbol for that in your language, please go ahead and
				#use it. Or if both aren't sufficient, just translate
				#the word 'none' or 'empty' or whatever you think is
				#appropriate.
				return _("-")
		elif column == self.CORRECT:
			return result["result"] == "right"

def init(moduleManager):
	return WordsTestTypeModule(moduleManager)
