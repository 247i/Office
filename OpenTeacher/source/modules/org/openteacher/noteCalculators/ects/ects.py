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

class ECTSNoteCalculatorModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(ECTSNoteCalculatorModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "noteCalculator"
		self.requires = (
			self._mm.mods(type="percentsCalculator"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("ects.py",)

		self.priorities = {
			"default": 935,
		}

	def _convert(self, percents):
		i = bisect.bisect([30, 40, 50, 55, 60, 70], percents)
		return ["F", "FX", "E", "D", "C", "B", "A"][i]

	def calculateNote(self, test):
		return self._convert(self._percents(test))

	def calculateAverageNote(self, tests):
		return self._convert(self._averagePercents(tests))

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		pc = self._modules.default(
			"active",
			type="percentsCalculator"
		)
		self._percents = pc.calculatePercents
		self._averagePercents = pc.calculateAveragePercents

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
		self.name = _("ECTS")

	def disable(self):
		self.active = False

		del self.name
		del self._modules
		del self._percents
		del self._averagePercents

def init(moduleManager):
	return ECTSNoteCalculatorModule(moduleManager)
