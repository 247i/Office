#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

class DutchNoteCalculatorModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(DutchNoteCalculatorModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "noteCalculator"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("dutch.py",)

		self.priorities = {
			"default": 935,
		}

	def _formatNote(self, note):
		if note == 10:
			#makes sure '10,0' isn't returned, since that's not a valid
			#dutch note. (It would mean that 10.8 would be possible,
			#which isn't.)
			return u"10"
		return (u"%0.1f" % note).replace(".", ",")

	def _calculateFloat(self, test):
		results = map(lambda x: 1 if x["result"] == "right" else 0, test["results"])
		total = len(results)
		amountRight = sum(results)

		return float(amountRight) / float(total) * 9 + 1

	def calculateNote(self, test):
		return self._formatNote(self._calculateFloat(test))

	def calculateAverageNote(self, tests):
		noteSum = sum((self._calculateFloat(test) for test in tests))
		return self._formatNote(noteSum / len(tests))

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

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
		self.name = _("Dutch")

	def disable(self):
		self.active = False

		del self._modules
		del self.name

def init(moduleManager):
	return DutchNoteCalculatorModule(moduleManager)
