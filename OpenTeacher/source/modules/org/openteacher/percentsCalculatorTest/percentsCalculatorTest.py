#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2013, Marten de Vries
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

import unittest

class TestCase(unittest.TestCase):
	def _test(self, input, output):
		for mod in self._mm.mods("active", type="percentsCalculator"):
			realOutput = mod.calculatePercents(input)
			try:
				self.assertEqual(output, realOutput)
			except AssertionError:
				print mod.__class__.__file__
				raise

	def _testAverage(self, input, output):
		for mod in self._mm.mods("active", type="percentsCalculator"):
			realOutput = mod.calculateAveragePercents(input)
			try:
				self.assertEqual(output, realOutput)
			except AssertionError:
				print mod.__class__.__file__
				raise

	def testWithNoResults(self):
		"""With no results, it's impossible to give a mark.
		   -> ZeroDivisionError should be raised to show that.

		"""
		with self.assertRaises(ZeroDivisionError):
			self._test({"results": []}, None)

	def testAverageWithNoTests(self):
		"""With no tests, it's impossible to calculate the average of
		   those tests -> ZeroDivisionError.

		"""
		with self.assertRaises(ZeroDivisionError):
			self._testAverage([], None)

	def testEverythingGood(self):
		self._test({"results": [
			{"result": "right"},
			{"result": "right"},
		]}, 100)

	def testTwoThird(self):
		self._test({"results": [
			{"result": "right"},
			{"result": "right"},
			{"result": "wrong"},
		]}, 67)

	def testAverage(self):
		self._testAverage([
			{"results": [{"result": "right"}]},
			{"results": [{"result": "wrong"}]}
		], 50)

	def testAverageOfAllWrong(self):
		self._testAverage([
			{"results": [{"result": "wrong"}]},
			{"results": [{"result": "wrong"}]}
		], 0)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="percentsCalculator"),
		)

	def enable(self):
		self.TestCase = TestCase
		self.TestCase._mm = self._mm
		self.active = True

	def disable(self):
		self.active = False
		del self.TestCase

def init(moduleManager):
	return TestModule(moduleManager)
