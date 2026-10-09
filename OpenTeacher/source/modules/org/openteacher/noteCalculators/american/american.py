#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Cas Widdershoven
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

import bisect

class AmericanNoteCalculatorModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(AmericanNoteCalculatorModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "noteCalculator"

		self.requires = (
			self._mm.mods(type="percentsCalculator"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("american.py",)

		self.priorities = {
			"default": 935,
		}

	def _convert(self, percents):
		i = bisect.bisect([60, 63, 67, 70, 73, 77, 80, 83, 87, 90, 93, 97], percents)
		return ["F", "D-", "D", "D+", "C-", "C", "C+", "B-", "B", "B+", "A-", "A", "A+"][i]

	def calculateNote(self, test):
		return self._convert(self._calculatePercents(test))

	def calculateAverageNote(self, tests):
		return self._convert(self._calculateAveragePercents(tests))

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		pc = self._modules.default(
			"active",
			type="percentsCalculator"
		)
		self._calculatePercents = pc.calculatePercents
		self._calculateAveragePercents = pc.calculateAveragePercents

		#Connect to the languageChanged event so retranslating is done.
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
		#Load translations
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		self.name = _("American")

	def disable(self):
		self.active = False
		del self.name
		del self._modules
		del self._calculatePercents
		del self._calculateAveragePercents

def init(moduleManager):
	return AmericanNoteCalculatorModule(moduleManager)
