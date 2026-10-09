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

class TopoTestTypeModule(object):
	PLACE_NAME, CORRECT = xrange(2)
	def __init__(self, moduleManager, *args, **kwargs):
		super(TopoTestTypeModule, self).__init__(*args, **kwargs)

		self._mm = moduleManager
		
		self.type = "testType"
		self.dataType = "topo"
		
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("topo.py",)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		#install translator for the first time and make sure it's re-
		#installed on a language change.
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True
		
	def _retranslate(self):
		#(re)install the translator, for use in every method
		#('property').
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
			_("Place name"),
			#TRANSLATORS: A label of a table column that indicates of the answer of the user was correct.
			_("Correct")
		]
	
	def _itemForResult(self, result):
		for item in self._list["items"]:
			if result["itemId"] == item["id"]:
				return item
	
	def data(self, row, column):
		result = self._test["results"][row]
		
		item = self._itemForResult(result)
		if column == self.PLACE_NAME:
			return item["name"]
		elif column == self.CORRECT:
			return result["result"] == "right"

def init(moduleManager):
	return TopoTestTypeModule(moduleManager)
