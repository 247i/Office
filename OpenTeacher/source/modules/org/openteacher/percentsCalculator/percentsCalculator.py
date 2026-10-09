#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, 2013, Marten de Vries
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

class PercentsCalculatorModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(PercentsCalculatorModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "percentsCalculator"

	def enable(self):
		self.active = True

	def calculateAveragePercents(self, tests):
		"""Calculates the average score of all ``tests`` in percents"""

		percents = (self.calculatePercents(test) for test in tests)
		percentSum = sum(percents)
		return int(round(percentSum / float(len(tests))))

	def calculatePercents(self, test):
		"""Calculates the score of the user in the passed-in ``test``
		   in percents.

		"""
		results = map(lambda x: 1 if x["result"] == "right" else 0, test["results"])
		total = len(results)
		amountRight = sum(results)

		return int(round(float(amountRight) / total * 100))

	def disable(self):
		self.active = False

def init(moduleManager):
	return PercentsCalculatorModule(moduleManager)
