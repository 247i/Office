#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012, Marten de Vries
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
import datetime

class TestCase(unittest.TestCase):
	def _checkCreatedAndRemoveFromLessonData(self, lessonData):
		for item in lessonData["list"]["items"]:
			self.assertIsInstance(item["created"], datetime.datetime)
			del item["created"]
		return lessonData

	def _test(self, input, expectedOutput, parseLenient=False):
		for mod in self._mm.mods("active", type="wordListStringParser"):
			lessonData = mod.parseList(input, parseLenient)
			lessonData = self._checkCreatedAndRemoveFromLessonData(lessonData)
			self.assertEqual(lessonData["list"]["items"], expectedOutput)

	def testBasicStructure(self):
		expectedOutput = {
			"resources": {},
			"list": {
				"items": [],
				"tests": [],
			}
		}

		for mod in self._mm.mods("active", type="wordListStringParser"):
			self.assertEqual(
				mod.parseList(u""),
				expectedOutput
			)

	def testBlankLines(self):
		self._test(u"\n" * 3, [])

	def testEqualSeparated(self):
		self._test(
			u"a = b",
			[{
				"id": 0,
				"questions": [[u"a"]],
				"answers": [[u"b"]],
			}]
		)

	def testNumber(self):
		self._test(
			u"100 = hundred",
			[{
				"id": 0,
				"questions": [[u"100"]],
				"answers": [[u"hundred"]],
			}]
		)

	def testTabSeparated(self):
		self._test(
			u"a\tb",
			[{
				"id": 0,
				"questions": [[u"a"]],
				"answers": [[u"b"]],
			}]
		)

	def testNoSeparator(self):
		with self.assertRaises(ValueError):
			self._test(
				u"ab",
				None
			)

	def testNoSeparatorAndLenientParsing(self):
		self._test(
			"ab",
			[],
			parseLenient=True
		)

	def testMultipleSeparators(self):
		self._test(
			u"a = = b",
			[{
				"id": 0,
				"questions": [["a"]],
				"answers": [["= b"]],
			}],
		)

	def testEscapedSeparator(self):
		self._test(
			u"""
a \== b
a \\\t   \t = b
			""",
			[
				{
					"id": 0,
					"questions": [[u"a \="]],
					"answers": [[u"b"]],
				},
				{
					"id": 1,
					"questions": [[u"a \\"]],
					"answers": [[u"= b"]],
				},
			]
		)

	def testNonAscii(self):
		self._test(
			u"é = à",
			[{
				"id": 0,
				"questions": [[u"é"]],
				"answers": [[u"à"]],
			}]
		)

	def testEmptyValues(self):
		self._test(
			"""
een =
=one
			""",
			[
				{"id": 0, "questions": [["een"]], "answers": []},
				{"id": 1, "questions": [], "answers": [["one"]]},
			]
		)

	def testRealWorldExample(self):
		self._test(
			"""
een = 1. one, uno 2. a
twee = two
drie = three

vier	four
vijf	five
3 \= 2 + 1 = three equals two plus one
			""",
			[
				{
					"id": 0,
					"questions": [["een"]],
					"answers": [["one", "uno"], ["a"]]
				},
				{"id": 1, "questions": [["twee"]], "answers": [["two"]]},
				{"id": 2, "questions": [["drie"]], "answers": [["three"]]},
				{"id": 3, "questions": [["vier"]], "answers": [["four"]]},
				{"id": 4, "questions": [["vijf"]], "answers": [["five"]]},
				{
					"id": 5,
					"questions": [["3 \= 2 + 1"]],
					"answers": [["three equals two plus one"]],
				},
			]
		)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="wordListStringParser"),
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
