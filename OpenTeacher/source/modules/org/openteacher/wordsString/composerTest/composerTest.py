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

import unittest

class WordsStringComposerTestCase(unittest.TestCase):
	def _test(self, input, output):
		for mod in self._mm.mods("active", type="wordsStringComposer"):
			string = mod.compose(input)
			self.assertEqual(string, output)

	def testEmpty(self):
		self._test([], u"")

	def testSingleWord(self):
		self._test(
			[[u"one"]],
			u"one"
		)

	def testNumber(self):
		self._test(
			[[u"100"]],
			u"100",
		)

	def testMultipleWords(self):
		self._test(
			[[u"one", u"two"]],
			u"one, two"
		)
	
	def testObligatoryWords(self):
		self._test(
			[[u"one"], [u"two"]],
			u"1. one 2. two"
		)
	
	def testObligatoryAndMultipleWords(self):
		self._test(
			[[u"one", u"uno"], [u"two"]],
			u"1. one, uno 2. two"
		)

	def testNonASCIILetters(self):
		self._test(
			[[u"être"]],
			u"être"
		)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.uses = (
			self._mm.mods(type="wordsStringComposer"),
		)

	def enable(self):
		self.TestCase = WordsStringComposerTestCase
		self.TestCase._mm = self._mm

		self.active = True

	def disable(self):
		self.active = False

		del self.TestCase

def init(moduleManager):
	return TestModule(moduleManager)
