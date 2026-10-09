#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2008-2011, Milan Boers
#	Copyright 2009-2012, Marten de Vries
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

class MediaTestTypeModule(object):
	NAME, QUESTION, ANSWER, GIVEN_ANSWER, CORRECT = xrange(5)
	def __init__(self, moduleManager, *args, **kwargs):
		super(MediaTestTypeModule, self).__init__(*args, **kwargs)

		self._mm = moduleManager
		
		self.type = "testType"
		self.dataType = "media"
		
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("media.py",)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self.active = True
		
		#setup translation
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
	def header(self):
		return [
			_("Name"),
			_("Question"),
			_("Answer"),
			_("Given answer"),
			#TRANSLATORS: the label of a table column that shows if the user answered a word in the same row correctly.
			_("Correct")
		]
	
	def _itemForResult(self, result):
		for item in self._list["items"]:
			if result["itemId"] == item["id"]:
				return item
	
	def data(self, row, column):
		result = self._test["results"][row]
		
		item = self._itemForResult(result)
		if column == self.NAME:
			return item["name"]
		if column == self.QUESTION:
			return item["question"]
		if column == self.ANSWER:
			return item["answer"]
		if column == self.GIVEN_ANSWER:
			return result["givenAnswer"]
		elif column == self.CORRECT:
			return result["result"] == "right"

def init(moduleManager):
	return MediaTestTypeModule(moduleManager)
