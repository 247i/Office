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

import unittest

class WordsStringParserTestCase(unittest.TestCase):
	def _test(self, input, output):
		for mod in self._mm.mods("active", type="wordsStringParser"):
			data = mod.parse(input)
			self.assertEqual(data, output)

	def testSingleWord(self):
		self._test(
			u"one",
			[[u"one"]]
		)

	def testMultipleWords(self):
		self._test(
			u"one, two",
			[[u"one", u"two"]]
		)

	def testMultipleSemicolonWords(self):
		self._test(
			u"one; two",
			[[u"one", u"two"]]
		)
	
	def testObligatoryWords(self):
		self._test(
			u"1. one 2. two",
			[[u"one"], [u"two"]]
		)
	
	def testObligatoryAndMultipleWords(self):
		self._test(
			u"1. one, uno 2. two",
			[[u"one", u"uno"], [u"two"]]
		)

	def testWrongObligatoryNumbers(self):
		self._test(
			u"1. one 3. two",
			[[u"one"], [u"two"]]
		)

	def testNonASCIILetters(self):
		self._test(
			u"être",
			[[u"être"]]
		)

	def testNumbersWithSpacesOnly(self):
		self._test(
			u"1. 2. 3. 4. ",
			[],
		)

	def testHundredWithSpace(self):
		self._test(
			u"100 ",
			[[u"100"]],
		)

	def testNumber(self):
		self._test(
			u"1.000.000",
			[[u"1.000.000"]],
		)

	def testCommasOnly(self):
		self._test(
			u",,,",
			[],
		)

	def testSemicolonOnly(self):
		self._test(
			u";;;",
			[],
		)

	def testNumberEscaping(self):
		self._test(
			u"I like to say \\1. and \\2. You too?",
			[["I like to say \\1. and \\2. You too?"]]
		)

	def testCommaEscaping(self):
		self._test(
			u"one\\, two",
			[["one\\, two"]]
		)

	def testSemicolonEscaping(self):
		self._test(
			u"one\\; two",
			[["one\\; two"]]
		)

	def testMultipleDigitObligatoryNumber(self):
		self._test(
			u"9999999999999999999. one 2222222222222222222222222222. two",
			[["one"], ["two"]]
		)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.uses = (
			self._mm.mods(type="wordsStringParser"),
		)

	def enable(self):
		self.TestCase = WordsStringParserTestCase
		self.TestCase._mm = self._mm
		self.active = True

	def disable(self):
		self.active = False
		del self.TestCase

def init(moduleManager):
	return TestModule(moduleManager)
