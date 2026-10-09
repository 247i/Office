#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

import __builtin__

class ReverseModule(object):
	"""Reverses all indexes of items in a test."""

	def __init__(self, moduleManager, *args, **kwargs):
		super(ReverseModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "listModifier"
		self.testType = "reverse"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("reverse.py",)
		self.priorities = {
			"default": 848,
		}

	def modifyList(self, indexes, list):
		#always work on the indexes, and return a list object
		return __builtin__.list(reversed(indexes))

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.dataType = "all"
		self.active = True

	def _retranslate(self):
		#Translations
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
		self.name = _("Reverse")

	def disable(self):
		self.active = False

		del self._modules
		del self.dataType
		del self.name

def init(moduleManager):
	return ReverseModule(moduleManager)
