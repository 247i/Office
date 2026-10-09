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

class SortModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SortModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "listModifier"
		self.testType = "sort"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("sort.py",)
		self.priorities = {
			"default": 911,
		}

	def modifyList(self, indexes, list):
		def getFirstQuestion(word):
			try:
				return word["questions"][0]
			except IndexError:
				return None
		#always work on the indexes
		currentList = [list["items"][i] for i in indexes]
		newList = sorted(currentList, key=getFirstQuestion)
		return [list["items"].index(word) for word in newList]

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		#Translations
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
		self.name = _("Sort")

	def disable(self):
		self.active = False

		del self._modules
		del self.dataType
		del self.name

def init(moduleManager):
	return SortModule(moduleManager)
